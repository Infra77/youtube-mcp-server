package org.example.videocurator.oauth;

import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.tomakehurst.wiremock.WireMockServer;
import java.net.*;
import java.net.http.*;
import java.nio.file.*;
import java.time.*;
import java.util.*;
import org.example.videocurator.domain.CuratorException;
import org.example.videocurator.quota.QuotaService.Reservation;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;

class OAuthLifecycleTest {
  @TempDir Path temp;
  WireMockServer server;
  ObjectMapper json = new ObjectMapper();
  HttpClient http = HttpClient.newHttpClient();
  Path file;

  @BeforeEach
  void start() throws Exception {
    server = new WireMockServer(0);
    server.start();
    file = temp.resolve("synthetic.dpapi");
  }

  @AfterEach
  void stop() {
    server.stop();
  }

  WindowsTokenVault vault(java.util.function.Consumer<URI> browser) {
    return new WindowsTokenVault(
        json,
        file,
        http,
        Clock.systemUTC(),
        b -> b.clone(),
        b -> b.clone(),
        URI.create(server.baseUrl()),
        browser);
  }

  void credential(String account) throws Exception {
    Files.writeString(
        file,
        "{\"clientId\":\"synthetic\",\"clientSecret\":\"synthetic\",\"refreshToken\":\"synthetic\",\"account\":\""
            + account
            + "\"}");
  }

  void token() {
    server.stubFor(
        post(urlEqualTo("/token"))
            .willReturn(
                okJson(
                    "{\"access_token\":\"synthetic-access\",\"refresh_token\":\"synthetic-refresh\",\"expires_in\":3600,\"scope\":\""
                        + WindowsTokenVault.SCOPE
                        + "\"}")));
  }

  Map<String, String> query(URI uri) {
    var m = new HashMap<String, String>();
    for (String p : uri.getRawQuery().split("&")) {
      var a = p.split("=", 2);
      m.put(a[0], URLDecoder.decode(a[1], java.nio.charset.StandardCharsets.UTF_8));
    }
    return m;
  }

  int callback(String uri) {
    try {
      return http.send(
              HttpRequest.newBuilder(URI.create(uri)).GET().build(),
              HttpResponse.BodyHandlers.discarding())
          .statusCode();
    } catch (Exception e) {
      throw new AssertionError(e);
    }
  }

  Path client() throws Exception {
    var p = temp.resolve("client.json");
    Files.writeString(
        p, "{\"installed\":{\"client_id\":\"synthetic\",\"client_secret\":\"synthetic\"}}");
    return p;
  }

  @Test
  void cachedTokenCannotOutliveCredentialReplacementOrDeletion() throws Exception {
    credential("account-A");
    token();
    var v = vault(null);
    assertEquals("account-A", v.account());
    assertEquals("synthetic-access", v.accessToken());
    credential("account-B");
    assertEquals(
        "AUTH_PROFILE_CHANGED", assertThrows(CuratorException.class, v::accessToken).code());
    var fresh = vault(null);
    assertEquals("account-B", fresh.account());
    fresh.accessToken();
    Files.delete(file);
    assertEquals("AUTH_REQUIRED", assertThrows(CuratorException.class, fresh::accessToken).code());
  }

  @Test
  void refreshIsCachedAndInvalidGrantIsSafe() throws Exception {
    credential("account-A");
    token();
    var v = vault(null);
    v.accessToken();
    v.accessToken();
    server.verify(1, postRequestedFor(urlEqualTo("/token")));
    server.resetAll();
    server.stubFor(
        post(urlEqualTo("/token"))
            .willReturn(
                aResponse()
                    .withStatus(400)
                    .withBody("{\"error\":\"invalid_grant\",\"secret\":\"DO-NOT-LEAK\"}")));
    var e = assertThrows(CuratorException.class, () -> vault(null).accessToken());
    assertEquals("AUTH_EXPIRED_OR_REVOKED", e.code());
    assertFalse(e.toString().contains("DO-NOT-LEAK"));
  }

  @Test
  void failedRevocationStillRemovesLocalCredential() throws Exception {
    credential("account-A");
    server.stubFor(post(urlEqualTo("/revoke")).willReturn(aResponse().withStatus(400)));
    var result = vault(null).logout();
    assertEquals(true, result.get("localCredentialRemoved"));
    assertNotEquals("confirmed", result.get("remoteRevocation"));
    assertFalse(Files.exists(file));
  }

  @Test
  void successfulRevocationAndUnreadableVaultBothRemoveLocalFile() throws Exception {
    credential("account-A");
    server.stubFor(post(urlEqualTo("/revoke")).willReturn(ok("")));
    assertEquals("confirmed", vault(null).logout().get("remoteRevocation"));
    assertFalse(Files.exists(file));
    Files.writeString(file, "corrupted");
    assertEquals(true, vault(null).logout().get("localCredentialRemoved"));
    assertFalse(Files.exists(file));
  }

  @Test
  void fullLoopbackPkceExchangeRejectsWrongStateAndPersistsVerifiedAccount() throws Exception {
    token();
    server.stubFor(
        get(urlPathEqualTo("/channels"))
            .willReturn(okJson("{\"items\":[{\"id\":\"UC0000000000000000000000\"}]}")));
    var v =
        vault(
            uri -> {
              var q = query(uri);
              assertEquals("S256", q.get("code_challenge_method"));
              assertTrue(q.get("code_challenge").length() > 30);
              assertEquals(400, callback(q.get("redirect_uri") + "?state=wrong&code=synthetic"));
              assertEquals(
                  400,
                  callback(
                      q.get("redirect_uri")
                          + "?state="
                          + q.get("state")
                          + "&state=duplicate&code=synthetic"));
              assertEquals(
                  200,
                  callback(q.get("redirect_uri") + "?state=" + q.get("state") + "&code=synthetic"));
            });
    v.login(client());
    assertEquals("UC0000000000000000000000", v.verifyAndSave(mock(Reservation.class)));
    assertEquals("UC0000000000000000000000", v.account());
    server.verify(
        postRequestedFor(urlEqualTo("/token")).withRequestBody(containing("code_verifier=")));
  }

  @Test
  void deniedConsentDoesNotOverwriteExistingCredential() throws Exception {
    credential("old-account");
    byte[] before = Files.readAllBytes(file);
    var v =
        vault(
            uri -> {
              var q = query(uri);
              callback(q.get("redirect_uri") + "?state=" + q.get("state") + "&error=access_denied");
            });
    assertThrows(CuratorException.class, () -> v.login(client()));
    assertArrayEquals(before, Files.readAllBytes(file));
  }

  @Test
  void missingScopeAndRefreshTokenDoNotOverwriteCredential() throws Exception {
    credential("old-account");
    var before = Files.readAllBytes(file);
    for (String response :
        List.of("{\"scope\":\"other\"}", "{\"scope\":\"" + WindowsTokenVault.SCOPE + "\"}")) {
      server.stubFor(post(urlEqualTo("/token")).willReturn(okJson(response)));
      var v =
          vault(
              uri -> {
                var q = query(uri);
                callback(q.get("redirect_uri") + "?state=" + q.get("state") + "&code=synthetic");
              });
      assertThrows(CuratorException.class, () -> v.login(client()));
      assertArrayEquals(before, Files.readAllBytes(file));
    }
  }
}
