package org.example.videocurator.oauth;

import com.fasterxml.jackson.databind.*;
import com.sun.jna.platform.win32.Crypt32Util;
import com.sun.net.httpserver.HttpServer;
import java.awt.Desktop;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.*;
import java.time.*;
import java.util.*;
import java.util.concurrent.*;
import org.example.videocurator.domain.CuratorException;
import org.example.videocurator.quota.CostCatalog;

/** Credential bytes never have a public JSON representation or diagnostic toString. */
public final class WindowsTokenVault implements TokenVault {
  public static final String SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl";
  private final ObjectMapper json;
  private final Path file;
  private final HttpClient http;
  private String cached;
  private String credentialGeneration;
  private java.util.function.UnaryOperator<byte[]> protect = Crypt32Util::cryptProtectData;
  private java.util.function.UnaryOperator<byte[]> unprotect = Crypt32Util::cryptUnprotectData;
  private Clock clock = Clock.systemUTC();
  private URI testOrigin;
  private java.util.function.Consumer<URI> browser;

  // Package-private test seam: never selected through environment or MCP arguments.
  WindowsTokenVault(
      ObjectMapper json,
      Path file,
      HttpClient http,
      Clock clock,
      java.util.function.UnaryOperator<byte[]> protect,
      java.util.function.UnaryOperator<byte[]> unprotect,
      URI testOrigin,
      java.util.function.Consumer<URI> browser) {
    if (!"http".equals(testOrigin.getScheme())
        || !Set.of("127.0.0.1", "localhost").contains(testOrigin.getHost()))
      throw new IllegalArgumentException("Tests must use loopback");
    this.json = json;
    this.file = file;
    this.http = http;
    this.clock = clock;
    this.protect = protect;
    this.unprotect = unprotect;
    this.testOrigin = testOrigin;
    this.browser = browser;
  }

  private String endpoint(String live, String path) {
    return testOrigin == null ? live : testOrigin.resolve(path).toString();
  }

  private void invalidate() {
    cached = null;
    expiry = Instant.EPOCH;
  }

  private Instant expiry = Instant.EPOCH;

  public WindowsTokenVault(ObjectMapper json, String profile) {
    if (!profile.matches("[A-Za-z0-9_-]{1,60}"))
      throw new CuratorException("INVALID_PROFILE", "Invalid local profile name.");
    this.json = json;
    String local = System.getenv("LOCALAPPDATA");
    file =
        Path.of(
            local == null ? System.getProperty("user.home") : local,
            "EducationalVideoCurator",
            profile + ".dpapi");
    http =
        HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .followRedirects(HttpClient.Redirect.NEVER)
            .build();
  }

  private void requireWindows() {
    if (testOrigin == null && !System.getProperty("os.name").startsWith("Windows"))
      throw new CuratorException(
          "VAULT_UNSUPPORTED", "This credential vault supports Windows DPAPI only.");
  }

  private JsonNode load() {
    requireWindows();
    try {
      byte[] encrypted = Files.readAllBytes(file);
      String generation =
          HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(encrypted));
      if (credentialGeneration != null && !credentialGeneration.equals(generation)) {
        invalidate();
        throw new CuratorException(
            "AUTH_PROFILE_CHANGED",
            "Credential changed. Restart this MCP process before using the new authorization.");
      }
      byte[] bytes = unprotect.apply(encrypted);
      credentialGeneration = generation;
      try {
        return json.readTree(bytes);
      } finally {
        Arrays.fill(bytes, (byte) 0);
      }
    } catch (CuratorException e) {
      throw e;
    } catch (Exception e) {
      invalidate();
      throw new CuratorException(
          "AUTH_REQUIRED",
          "Run the local auth login command; credentials are absent or unreadable.");
    }
  }

  public String account() {
    return load().path("account").asText();
  }

  public synchronized String accessToken() {
    JsonNode c = load(); // Always check deletion/replacement, even while the token is cached.
    if (cached != null && expiry.isAfter(clock.instant().plusSeconds(60))) return cached;
    var data =
        post(
            endpoint("https://oauth2.googleapis.com/token", "/token"),
            Map.of(
                "client_id",
                c.path("clientId").asText(),
                "client_secret",
                c.path("clientSecret").asText(),
                "refresh_token",
                c.path("refreshToken").asText(),
                "grant_type",
                "refresh_token"));
    cached = data.path("access_token").asText();
    if (cached.isBlank())
      throw new CuratorException("AUTH_EXPIRED_OR_REVOKED", "Reauthorize locally.");
    expiry = clock.instant().plusSeconds(data.path("expires_in").asLong(3600));
    return cached;
  }

  public Map<String, Object> status() {
    try {
      return Map.of(
          "authorized",
          true,
          "account",
          account(),
          "scope",
          SCOPE,
          "storage",
          "Windows DPAPI CurrentUser",
          "liveTokenChecked",
          false);
    } catch (CuratorException e) {
      return Map.of("authorized", false, "code", e.code());
    }
  }

  private static String enc(String s) {
    return URLEncoder.encode(s, StandardCharsets.UTF_8);
  }

  private static String form(Map<String, String> fields) {
    return fields.entrySet().stream()
        .map(e -> enc(e.getKey()) + "=" + enc(e.getValue()))
        .reduce((a, b) -> a + "&" + b)
        .orElse("");
  }

  private JsonNode post(String endpoint, Map<String, String> fields) {
    try {
      var response =
          http.send(
              HttpRequest.newBuilder(URI.create(endpoint))
                  .timeout(Duration.ofSeconds(30))
                  .header("Content-Type", "application/x-www-form-urlencoded")
                  .POST(HttpRequest.BodyPublishers.ofString(form(fields)))
                  .build(),
              HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() != 200)
        throw new CuratorException(
            "AUTH_EXPIRED_OR_REVOKED", "Google authorization failed; run auth login again.");
      return response.body().isBlank() ? json.createObjectNode() : json.readTree(response.body());
    } catch (CuratorException e) {
      throw e;
    } catch (Exception e) {
      throw new CuratorException(
          "AUTH_NETWORK_ERROR",
          "Authorization network operation failed. No credential details are logged.");
    }
  }

  private String random() {
    byte[] b = new byte[32];
    new SecureRandom().nextBytes(b);
    return Base64.getUrlEncoder().withoutPadding().encodeToString(b);
  }

  public static String challenge(String verifier) {
    try {
      return Base64.getUrlEncoder()
          .withoutPadding()
          .encodeToString(
              MessageDigest.getInstance("SHA-256")
                  .digest(verifier.getBytes(StandardCharsets.US_ASCII)));
    } catch (Exception e) {
      throw new IllegalStateException(e);
    }
  }

  public static boolean stateMatches(String expected, String actual) {
    return actual != null
        && MessageDigest.isEqual(
            expected.getBytes(StandardCharsets.UTF_8), actual.getBytes(StandardCharsets.UTF_8));
  }

  public void login(Path clientFile) {
    requireWindows();
    HttpServer receiver = null;
    try {
      JsonNode client = json.readTree(Files.readString(clientFile)).path("installed");
      String clientId = client.path("client_id").asText(),
          secret = client.path("client_secret").asText();
      if (clientId.isBlank())
        throw new CuratorException(
            "OAUTH_CONFIG_INVALID", "Expected Google Desktop installed client JSON.");
      String state = random(), verifier = random();
      var callback = new CompletableFuture<String>();
      receiver = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
      String redirect = "http://127.0.0.1:" + receiver.getAddress().getPort() + "/callback";
      receiver.createContext(
          "/callback",
          exchange -> {
            int status = 400;
            String message = "Authorization callback rejected.";
            try {
              var params = new HashMap<String, String>();
              String query = exchange.getRequestURI().getRawQuery();
              if (!exchange.getRequestMethod().equals("GET")
                  || !exchange.getRequestURI().getPath().equals("/callback")
                  || query == null
                  || query.length() > 8192) throw new IllegalArgumentException();
              for (String entry : query.split("&")) {
                String[] pair = entry.split("=", 2);
                String k = URLDecoder.decode(pair[0], StandardCharsets.UTF_8),
                    v = pair.length == 2 ? URLDecoder.decode(pair[1], StandardCharsets.UTF_8) : "";
                if (params.putIfAbsent(k, v) != null) throw new IllegalArgumentException();
              }
              if (stateMatches(state, params.get("state")) && params.containsKey("error")) {
                callback.completeExceptionally(new IllegalStateException("Consent declined"));
              }
              if (stateMatches(state, params.get("state"))
                  && !params.containsKey("error")
                  && !Objects.toString(params.get("code"), "").isBlank()) {
                callback.complete(params.get("code"));
                status = 200;
                message = "Authorization received. Return to your terminal.";
              }
            } catch (Exception ignored) {
            }
            byte[] response = message.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
            exchange.sendResponseHeaders(status, response.length);
            exchange.getResponseBody().write(response);
            exchange.close();
          });
      receiver.start();
      var params = new LinkedHashMap<String, String>();
      params.put("client_id", clientId);
      params.put("redirect_uri", redirect);
      params.put("response_type", "code");
      params.put("scope", SCOPE);
      params.put("access_type", "offline");
      params.put("prompt", "consent");
      params.put("state", state);
      params.put("code_challenge", challenge(verifier));
      params.put("code_challenge_method", "S256");
      if (browser == null && !Desktop.isDesktopSupported())
        throw new CuratorException(
            "BROWSER_REQUIRED", "Run authorization on a Windows desktop with a browser.");
      URI authorization =
          URI.create(
              endpoint("https://accounts.google.com/o/oauth2/v2/auth", "/authorize")
                  + "?"
                  + form(params));
      if (browser != null) browser.accept(authorization);
      else Desktop.getDesktop().browse(authorization);
      String code = callback.get(180, TimeUnit.SECONDS);
      JsonNode tokens =
          post(
              endpoint("https://oauth2.googleapis.com/token", "/token"),
              Map.of(
                  "client_id",
                  clientId,
                  "client_secret",
                  secret,
                  "code",
                  code,
                  "code_verifier",
                  verifier,
                  "redirect_uri",
                  redirect,
                  "grant_type",
                  "authorization_code"));
      if (!Arrays.asList(tokens.path("scope").asText().split(" ")).contains(SCOPE))
        throw new CuratorException("MISSING_SCOPE", "The required YouTube scope was not granted.");
      String refresh = tokens.path("refresh_token").asText();
      if (refresh.isBlank())
        throw new CuratorException(
            "AUTH_REFRESH_MISSING",
            "Google did not issue a refresh credential; existing local credentials were retained. Review consent and authorize again.");
      cached = tokens.path("access_token").asText();
      expiry = clock.instant().plusSeconds(tokens.path("expires_in").asLong(3600));
      // Channel verification is performed by the caller through the quota-accounted provider after
      // saving a temporary in-memory credential.
      pending =
          json.createObjectNode()
              .put("clientId", clientId)
              .put("clientSecret", secret)
              .put("refreshToken", refresh)
              .put("account", "");
    } catch (CuratorException e) {
      throw e;
    } catch (Exception e) {
      throw new CuratorException(
          "AUTH_FAILED",
          "Authorization did not complete within the local flow. Existing credentials were retained.");
    } finally {
      if (receiver != null) receiver.stop(0);
    }
  }

  private com.fasterxml.jackson.databind.node.ObjectNode pending;

  public String verifyAndSave(org.example.videocurator.quota.QuotaService.Reservation budget) {
    if (pending == null) throw new CuratorException("AUTH_REQUIRED", "Run login first.");
    try {
      budget.general(CostCatalog.read());
      var response =
          http.send(
              HttpRequest.newBuilder(
                      URI.create(
                          endpoint(
                              "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
                              "/channels?part=id&mine=true")))
                  .timeout(Duration.ofSeconds(20))
                  .header("Authorization", "Bearer " + cached)
                  .GET()
                  .build(),
              HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() != 200)
        throw new CuratorException(
            "AUTH_VERIFICATION_FAILED", "Unable to verify authorized YouTube channel.");
      String account = json.readTree(response.body()).path("items").path(0).path("id").asText();
      if (!account.matches("UC[A-Za-z0-9_-]{22}"))
        throw new CuratorException(
            "YOUTUBE_CHANNEL_REQUIRED",
            "Create a YouTube channel for this Google account, then authorize again.");
      pending.put("account", account);
      Files.createDirectories(file.getParent());
      byte[] plain = json.writeValueAsBytes(pending);
      byte[] encrypted;
      try {
        encrypted = protect.apply(plain);
      } finally {
        Arrays.fill(plain, (byte) 0);
      }
      Path temp = Files.createTempFile(file.getParent(), "credential-", ".dpapi");
      Files.write(temp, encrypted);
      Files.move(temp, file, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
      pending = null;
      credentialGeneration = null;
      invalidate();
      return account;
    } catch (CuratorException e) {
      throw e;
    } catch (Exception e) {
      throw new CuratorException("AUTH_SAVE_FAILED", "Protected authorization could not be saved.");
    }
  }

  /** Local removal is unconditional; remote revocation failure is explicitly reported. */
  public Map<String, Object> logout() {
    String remote = "not_confirmed";
    try {
      JsonNode c = load();
      post(
          endpoint("https://oauth2.googleapis.com/revoke", "/revoke"),
          Map.of("token", c.path("refreshToken").asText()));
      remote = "confirmed";
    } catch (CuratorException e) {
      remote = e.code();
    } finally {
      invalidate();
      pending = null;
      try {
        Files.deleteIfExists(file);
      } catch (Exception e) {
        throw new CuratorException(
            "AUTH_DELETE_FAILED", "Local credential removal failed; inspect local permissions.");
      }
    }
    return Map.of("localCredentialRemoved", true, "remoteRevocation", remote);
  }
}
