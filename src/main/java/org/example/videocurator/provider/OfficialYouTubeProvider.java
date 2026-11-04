package org.example.videocurator.provider;

import static org.example.videocurator.domain.Models.*;

import com.fasterxml.jackson.databind.*;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.*;
import java.util.*;
import org.example.videocurator.domain.*;
import org.example.videocurator.oauth.TokenVault;
import org.example.videocurator.quota.CostCatalog;
import org.example.videocurator.quota.QuotaService.Reservation;

public final class OfficialYouTubeProvider implements YouTubeProvider {
  private final ObjectMapper json;
  private final TokenVault vault;
  private final HttpClient http;
  private final URI base;
  private final MetadataCache cache =
      new MetadataCache(Clock.systemUTC(), Duration.ofMinutes(5), 128);

  public OfficialYouTubeProvider(ObjectMapper json, TokenVault vault) {
    this(json, vault, URI.create("https://www.googleapis.com/youtube/v3/"));
  }

  /**
   * Alternate origin is restricted to loopback for WireMock, never selected from tool arguments.
   */
  public OfficialYouTubeProvider(ObjectMapper json, TokenVault vault, URI base) {
    if (!base.toString().equals("https://www.googleapis.com/youtube/v3/")
        && !("http".equals(base.getScheme())
            && Set.of("127.0.0.1", "localhost").contains(base.getHost())))
      throw new IllegalArgumentException("Unapproved API origin");
    this.json = json;
    this.vault = vault;
    this.base = base;
    http =
        HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .followRedirects(HttpClient.Redirect.NEVER)
            .build();
  }

  private JsonNode request(
      String method, String path, Map<String, String> params, Object body, Reservation r) {
    String account =
        vault.account(); // Validate credential generation before considering cached metadata.
    String bearer = vault.accessToken(); // authorization must succeed before quota is consumed
    String query =
        params.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .map(e -> enc(e.getKey()) + "=" + enc(e.getValue()))
            .reduce((a, b) -> a + "&" + b)
            .orElse("");
    boolean cacheable =
        method.equals("GET")
            && (path.equals("search")
                || path.equals("channels") && !params.containsKey("mine")
                || path.equals("videos") && params.containsKey("id"));
    String cacheKey = account + ":" + path + "?" + query;
    if (cacheable) {
      var hit = cache.get(cacheKey);
      if (hit != null) return hit;
    }
    try {
      var b =
          HttpRequest.newBuilder(base.resolve(path + "?" + query))
              .timeout(Duration.ofSeconds(25))
              .header("Authorization", "Bearer " + bearer)
              .header("Accept", "application/json");
      if (method.equals("POST"))
        b.header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(body)));
      else b.GET();
      if (path.equals("search")) r.search();
      else r.general(method.equals("POST") ? CostCatalog.write() : CostCatalog.read());
      var response =
          http.send(b.build(), HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
      if (response.body().length() > 2_000_000)
        throw new CuratorException("UPSTREAM_INVALID", "Upstream response exceeded size limit.");
      JsonNode data;
      try {
        data = json.readTree(response.body());
      } catch (Exception e) {
        throw new CuratorException("UPSTREAM_INVALID", "Upstream returned malformed JSON.");
      }
      if (response.statusCode() < 200 || response.statusCode() >= 300)
        throw mapError(response.statusCode(), data);
      if (data == null || !data.isObject())
        throw new CuratorException("UPSTREAM_INVALID", "Upstream response shape invalid.");
      if (cacheable) cache.put(cacheKey, data);
      return data;
    } catch (CuratorException e) {
      throw e;
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
      throw new CuratorException(
          "UPSTREAM_AMBIGUOUS", "Request interrupted; write outcome may be unknown.");
    } catch (Exception e) {
      throw new CuratorException(
          "UPSTREAM_AMBIGUOUS",
          "Network outcome is unknown; writes are not automatically retried.");
    }
  }

  public static CuratorException mapError(int status, JsonNode data) {
    String reason = data.path("error").path("errors").path(0).path("reason").asText();
    String code =
        switch (reason) {
          case "quotaExceeded", "dailyLimitExceeded" -> "QUOTA_EXHAUSTED";
          case "youtubeSignupRequired" -> "YOUTUBE_CHANNEL_REQUIRED";
          case "invalidCredentials", "authError" -> "AUTH_EXPIRED_OR_REVOKED";
          case "insufficientPermissions" -> "MISSING_SCOPE";
          case "rateLimitExceeded", "userRateLimitExceeded" -> "RATE_LIMITED";
          case "videoNotFound" -> "VIDEO_UNAVAILABLE";
          default ->
              status == 401
                  ? "AUTH_EXPIRED_OR_REVOKED"
                  : status == 429
                      ? "RATE_LIMITED"
                      : status >= 500 ? "UPSTREAM_TEMPORARY" : "UPSTREAM_REJECTED";
        };
    return new CuratorException(
        code,
        "YouTube request failed (HTTP "
            + status
            + "). Reauthorize for auth errors; create a YouTube channel for YOUTUBE_CHANNEL_REQUIRED. No automatic write retry.");
  }

  private static String enc(String s) {
    return URLEncoder.encode(s, StandardCharsets.UTF_8);
  }

  private String text(JsonNode n, String key, int limit) {
    String s = n.path(key).asText("");
    return s.substring(0, Math.min(limit, s.length())).replaceAll("[\\p{Cntrl}&&[^\\n\\t]]", "");
  }

  private Video toVideo(JsonNode n) {
    var s = n.path("snippet");
    var tags = new ArrayList<String>();
    if (s.path("tags").isArray())
      for (var t : s.path("tags")) {
        if (tags.size() == 30) break;
        tags.add(t.asText().substring(0, Math.min(100, t.asText().length())));
      }
    long duration = 0;
    try {
      duration = Input.duration(n.path("contentDetails").path("duration").asText());
    } catch (CuratorException ignored) {
    }
    if (!s.path("liveBroadcastContent").asText("none").equals("none")) duration = 0;
    return new Video(
        n.path("id").asText(),
        text(s, "title", 200),
        text(s, "description", 2000),
        s.path("channelId").asText(),
        s.path("categoryId").asText(),
        tags,
        duration,
        text(s, "defaultAudioLanguage", 20));
  }

  private Channel toChannel(JsonNode n) {
    return new Channel(
        n.path("id").asText(),
        text(n.path("snippet"), "title", 200),
        text(n.path("snippet"), "description", 2000));
  }

  private List<JsonNode> items(String path, Map<String, String> params, Reservation r) {
    JsonNode data = request("GET", path, params, null, r);
    if (!data.path("items").isArray())
      throw new CuratorException("UPSTREAM_INVALID", "Missing items array.");
    var out = new ArrayList<JsonNode>();
    data.path("items").forEach(out::add);
    return out;
  }

  private List<Video> hydrate(List<String> ids, Reservation r) {
    if (ids.isEmpty()) return List.of();
    return items(
            "videos",
            Map.of(
                "part",
                "snippet,contentDetails",
                "id",
                String.join(",", ids.stream().distinct().limit(50).toList())),
            r)
        .stream()
        .map(this::toVideo)
        .toList();
  }

  public Video video(String id, Reservation r) {
    return hydrate(List.of(id), r).stream()
        .findFirst()
        .orElseThrow(
            () ->
                new CuratorException(
                    "VIDEO_UNAVAILABLE", "Video is unavailable, private or deleted."));
  }

  public List<Video> searchVideos(String topic, Reservation r) {
    return hydrate(
        items(
                "search",
                Map.of("part", "snippet", "type", "video", "maxResults", "50", "q", topic),
                r)
            .stream()
            .map(n -> n.path("id").path("videoId").asText())
            .filter(s -> s.matches("[A-Za-z0-9_-]{11}"))
            .toList(),
        r);
  }

  public Channel channel(String selector, Reservation r) {
    return items(
            "channels",
            Map.of("part", "snippet", selector.startsWith("@") ? "forHandle" : "id", selector),
            r)
        .stream()
        .findFirst()
        .map(this::toChannel)
        .orElseThrow(
            () -> new CuratorException("CHANNEL_UNAVAILABLE", "No accessible matching channel."));
  }

  public List<Channel> searchChannels(String topic, Reservation r) {
    var ids =
        items(
                "search",
                Map.of("part", "snippet", "type", "channel", "maxResults", "50", "q", topic),
                r)
            .stream()
            .map(n -> n.path("id").path("channelId").asText())
            .filter(s -> s.matches("UC[A-Za-z0-9_-]{22}"))
            .distinct()
            .toList();
    if (ids.isEmpty()) return List.of();
    return items("channels", Map.of("part", "snippet", "id", String.join(",", ids)), r).stream()
        .map(this::toChannel)
        .toList();
  }

  private record Page(List<JsonNode> items, boolean truncated) {}

  /** At most two pages, never beyond the stated item cap. Repeated tokens fail closed. */
  private Page page(String path, Map<String, String> params, Reservation r) {
    int cap = Integer.parseInt(params.get("maxResults"));
    var result = new ArrayList<JsonNode>();
    var tokens = new HashSet<String>();
    String next = "";
    for (int i = 0; i < 2; i++) {
      var query = new HashMap<>(params);
      query.put("maxResults", Integer.toString(Math.min((cap + 1) / 2, cap - result.size())));
      if (!next.isEmpty()) query.put("pageToken", next);
      var data = request("GET", path, query, null, r);
      if (!data.path("items").isArray())
        throw new CuratorException("UPSTREAM_INVALID", "Missing collection items.");
      for (var n : data.path("items")) {
        if (result.size() >= cap) break;
        result.add(n);
      }
      next = data.path("nextPageToken").asText("");
      if (next.isEmpty()) return new Page(result, false);
      if (!tokens.add(next))
        throw new CuratorException("UPSTREAM_INVALID", "Repeated pagination token.");
      if (result.size() >= cap) break;
    }
    return new Page(result, !next.isEmpty());
  }

  public PersonalData personal(Reservation r) {
    var likes =
        page(
            "videos",
            Map.of("part", "snippet,contentDetails", "myRating", "like", "maxResults", "50"),
            r);
    var subscriptions =
        page("subscriptions", Map.of("part", "snippet", "mine", "true", "maxResults", "30"), r);
    var lists = page("playlists", Map.of("part", "snippet", "mine", "true", "maxResults", "5"), r);
    var channels = new ArrayList<Channel>();
    var events = new ArrayList<Event>();
    for (var n : subscriptions.items()) {
      var sn = n.path("snippet");
      String id = sn.path("resourceId").path("channelId").asText();
      channels.add(new Channel(id, text(sn, "title", 200), text(sn, "description", 2000)));
      events.add(new Event("SUBSCRIPTION_ADDED_AT", id, instant(sn.path("publishedAt").asText())));
    }
    var videos = new LinkedHashMap<String, Video>();
    int itemCount = 0;
    boolean truncated = likes.truncated() || subscriptions.truncated() || lists.truncated();
    for (var list : lists.items()) {
      var p =
          page(
              "playlistItems",
              Map.of(
                  "part",
                  "snippet,contentDetails",
                  "playlistId",
                  list.path("id").asText(),
                  "maxResults",
                  "30"),
              r);
      truncated |= p.truncated();
      itemCount += p.items().size();
      var ids = new ArrayList<String>();
      for (var n : p.items()) {
        String id = n.path("contentDetails").path("videoId").asText();
        if (id.matches("[A-Za-z0-9_-]{11}")) {
          ids.add(id);
          events.add(
              new Event(
                  "PLAYLIST_ITEM_ADDED_AT",
                  id,
                  instant(n.path("snippet").path("publishedAt").asText())));
        }
      }
      for (Video v : hydrate(ids, r)) videos.putIfAbsent(v.id(), v);
    }
    return new PersonalData(
        likes.items().stream().map(this::toVideo).toList(),
        channels,
        List.copyOf(videos.values()),
        events,
        Map.of(
            "likesFetched",
            likes.items().size(),
            "subscriptionsFetched",
            channels.size(),
            "playlistsFetched",
            lists.items().size(),
            "playlistItemsFetched",
            itemCount,
            "truncated",
            truncated,
            "samplingPolicy",
            "at most two pages per source: 50 likes, 30 subscriptions, 5 playlists x 30 items"));
  }

  private Instant instant(String s) {
    try {
      return Instant.parse(s);
    } catch (Exception e) {
      return null;
    }
  }

  public String insertPlaylist(String title, String privacy, Reservation r) {
    return requiredId(
        request(
            "POST",
            "playlists",
            Map.of("part", "snippet,status"),
            Map.of("snippet", Map.of("title", title), "status", Map.of("privacyStatus", privacy)),
            r));
  }

  public String insertItem(String playlist, String video, int position, Reservation r) {
    return requiredId(
        request(
            "POST",
            "playlistItems",
            Map.of("part", "snippet"),
            Map.of(
                "snippet",
                Map.of(
                    "playlistId",
                    playlist,
                    "position",
                    position,
                    "resourceId",
                    Map.of("kind", "youtube#video", "videoId", video))),
            r));
  }

  private String requiredId(JsonNode n) {
    String id = n.path("id").asText();
    if (id.isBlank() || id.length() > 160)
      throw new CuratorException(
          "UPSTREAM_AMBIGUOUS", "Write response did not contain a valid resource ID.");
    return id;
  }

  public List<String> playlistVideoIds(String id, Reservation r) {
    return items(
            "playlistItems",
            Map.of("part", "contentDetails", "playlistId", id, "maxResults", "50"),
            r)
        .stream()
        .map(n -> n.path("contentDetails").path("videoId").asText())
        .toList();
  }

  public void verifyAccount(Reservation r) {
    var mine = items("channels", Map.of("part", "id", "mine", "true"), r);
    if (mine.stream().noneMatch(n -> n.path("id").asText().equals(account())))
      throw new CuratorException(
          "ACCOUNT_MISMATCH", "Authorized channel differs from saved proposal account.");
  }

  public String account() {
    return vault.account();
  }

  public boolean fixture() {
    return false;
  }
}
