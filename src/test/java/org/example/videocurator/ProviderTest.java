package org.example.videocurator;

import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.tomakehurst.wiremock.WireMockServer;
import java.net.URI;
import org.example.videocurator.domain.CuratorException;
import org.example.videocurator.oauth.TokenVault;
import org.example.videocurator.provider.OfficialYouTubeProvider;
import org.example.videocurator.quota.QuotaService.Reservation;
import org.junit.jupiter.api.*;

class ProviderTest {
  WireMockServer http;
  OfficialYouTubeProvider provider;
  Reservation budget;

  @BeforeEach
  void setup() {
    http = new WireMockServer(0);
    http.start();
    TokenVault vault = mock(TokenVault.class);
    when(vault.accessToken()).thenReturn("synthetic-test-value");
    provider =
        new OfficialYouTubeProvider(new ObjectMapper(), vault, URI.create(http.baseUrl() + "/"));
    budget = mock(Reservation.class);
  }

  @AfterEach
  void close() {
    http.stop();
  }

  @Test
  void mapsVideoAndMissingTagsWithOfficialQuery() {
    http.stubFor(
        get(urlPathEqualTo("/videos"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"id\":\"FIXTURE0001\",\"snippet\":{\"title\":\"Synthetic\",\"defaultAudioLanguage\":\"en\"},\"contentDetails\":{\"duration\":\"PT20M\"}}]}")));
    var v = provider.video("FIXTURE0001", budget);
    assertEquals(1200, v.seconds());
    assertTrue(v.tags().isEmpty());
    http.verify(
        getRequestedFor(urlPathEqualTo("/videos"))
            .withQueryParam("id", equalTo("FIXTURE0001"))
            .withQueryParam("part", equalTo("snippet,contentDetails"))
            .withHeader("Authorization", matching("Bearer .+")));
    verify(budget).general(1);
  }

  @Test
  void deletedAndPrivateVideoUnavailable() {
    http.stubFor(get(anyUrl()).willReturn(okJson("{\"items\":[]}")));
    assertEquals(
        "VIDEO_UNAVAILABLE",
        assertThrows(CuratorException.class, () -> provider.video("FIXTURE0001", budget)).code());
  }

  @Test
  void prescribedNegativeErrorsAreSafeAndNeverRetried() {
    String[][] cases = {
      {"quotaExceeded", "QUOTA_EXHAUSTED"},
      {"youtubeSignupRequired", "YOUTUBE_CHANNEL_REQUIRED"},
      {"invalidCredentials", "AUTH_EXPIRED_OR_REVOKED"},
      {"rateLimitExceeded", "RATE_LIMITED"},
      {"insufficientPermissions", "MISSING_SCOPE"}
    };
    for (var c : cases) {
      http.resetAll();
      http.stubFor(
          get(anyUrl())
              .willReturn(
                  aResponse()
                      .withStatus(403)
                      .withBody(
                          "{\"error\":{\"errors\":[{\"reason\":\""
                              + c[0]
                              + "\"}],\"message\":\"sensitive-upstream-value\"}}")));
      var e = assertThrows(CuratorException.class, () -> provider.video("FIXTURE0001", budget));
      assertEquals(c[1], e.code());
      assertFalse(e.getMessage().contains("sensitive-upstream-value"));
      http.verify(1, getRequestedFor(anyUrl()));
    }
  }

  @Test
  void malformedAnd429() {
    http.stubFor(get(anyUrl()).willReturn(ok("bad-json")));
    assertEquals(
        "UPSTREAM_INVALID",
        assertThrows(CuratorException.class, () -> provider.video("FIXTURE0001", budget)).code());
    http.resetAll();
    http.stubFor(get(anyUrl()).willReturn(aResponse().withStatus(429).withBody("{}")));
    assertEquals(
        "RATE_LIMITED",
        assertThrows(CuratorException.class, () -> provider.video("FIXTURE0001", budget)).code());
  }

  @Test
  void writeEndpointAndBody() {
    http.stubFor(
        post(urlPathEqualTo("/playlistItems")).willReturn(okJson("{\"id\":\"synthetic-item\"}")));
    assertEquals(
        "synthetic-item", provider.insertItem("synthetic-playlist", "FIXTURE0001", 0, budget));
    http.verify(
        postRequestedFor(urlPathEqualTo("/playlistItems"))
            .withRequestBody(
                matchingJsonPath("$.snippet.resourceId.kind", equalTo("youtube#video")))
            .withRequestBody(matchingJsonPath("$.snippet.position", equalTo("0"))));
    verify(budget).general(50);
  }

  @Test
  void cacheHitAvoidsUpstreamCharge() {
    http.stubFor(
        get(urlPathEqualTo("/videos"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"id\":\"FIXTURE0001\",\"snippet\":{},\"contentDetails\":{\"duration\":\"PT1M\"}}]}")));
    provider.video("FIXTURE0001", budget);
    provider.video("FIXTURE0001", budget);
    http.verify(1, getRequestedFor(urlPathEqualTo("/videos")));
    verify(budget, times(1)).general(1);
  }

  @Test
  void searchHydratesAndChannelHandleUsesOfficialParameters() {
    http.stubFor(
        get(urlPathEqualTo("/search"))
            .withQueryParam("type", equalTo("video"))
            .willReturn(okJson("{\"items\":[{\"id\":{\"videoId\":\"FIXTURE0001\"}}]}")));
    http.stubFor(
        get(urlPathEqualTo("/videos"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"id\":\"FIXTURE0001\",\"snippet\":{\"title\":\"math\"},\"contentDetails\":{\"duration\":\"PT1M\"}}]}")));
    assertEquals("FIXTURE0001", provider.searchVideos("math", budget).getFirst().id());
    http.stubFor(
        get(urlPathEqualTo("/channels"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"id\":\"UC0000000000000000000000\",\"snippet\":{\"title\":\"math\"}}]}")));
    assertEquals("math", provider.channel("@Math", budget).title());
    http.verify(
        getRequestedFor(urlPathEqualTo("/channels")).withQueryParam("forHandle", equalTo("@Math")));
    http.stubFor(
        get(urlPathEqualTo("/search"))
            .withQueryParam("type", equalTo("channel"))
            .willReturn(
                okJson("{\"items\":[{\"id\":{\"channelId\":\"UC0000000000000000000000\"}}]}")));
    assertEquals(1, provider.searchChannels("math", budget).size());
  }

  @Test
  void personalReadsAllSourcesWithBoundedPaginationAndTruthfulTimestamps() {
    http.stubFor(
        get(urlPathEqualTo("/videos"))
            .withQueryParam("myRating", equalTo("like"))
            .willReturn(okJson("{\"items\":[],\"nextPageToken\":\"second\"}")));
    http.stubFor(
        get(urlPathEqualTo("/videos"))
            .withQueryParam("pageToken", equalTo("second"))
            .willReturn(okJson("{\"items\":[]}")));
    http.stubFor(
        get(urlPathEqualTo("/subscriptions"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"snippet\":{\"resourceId\":{\"channelId\":\"UC0000000000000000000000\"},\"publishedAt\":\"2026-01-01T00:00:00Z\",\"title\":\"math\"}}]}")));
    http.stubFor(
        get(urlPathEqualTo("/playlists"))
            .willReturn(okJson("{\"items\":[{\"id\":\"synthetic-list\"}]}")));
    http.stubFor(
        get(urlPathEqualTo("/playlistItems"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"snippet\":{\"publishedAt\":\"2026-02-01T00:00:00Z\"},\"contentDetails\":{\"videoId\":\"FIXTURE0001\"}}]}")));
    http.stubFor(
        get(urlPathEqualTo("/videos"))
            .withQueryParam("id", equalTo("FIXTURE0001"))
            .willReturn(
                okJson(
                    "{\"items\":[{\"id\":\"FIXTURE0001\",\"snippet\":{},\"contentDetails\":{\"duration\":\"PT1M\"}}]}")));
    var data = provider.personal(budget);
    assertEquals(1, data.subscriptions().size());
    assertEquals(1, data.playlistVideos().size());
    assertEquals(2, data.events().size());
    assertEquals(false, data.coverage().get("truncated"));
    http.verify(
        1,
        getRequestedFor(urlPathEqualTo("/videos")).withQueryParam("pageToken", equalTo("second")));
    assertEquals("PLAYLIST_ITEM_ADDED_AT", data.events().get(1).source());
  }

  @Test
  void repeatedPaginationTokenStopsWithinBound() {
    http.stubFor(get(anyUrl()).willReturn(okJson("{\"items\":[],\"nextPageToken\":\"repeat\"}")));
    assertEquals(
        "UPSTREAM_INVALID",
        assertThrows(CuratorException.class, () -> provider.personal(budget)).code());
    http.verify(2, getRequestedFor(urlPathEqualTo("/videos")));
  }

  @Test
  void playlistCreationAndReadbackContracts() {
    http.stubFor(
        post(urlPathEqualTo("/playlists")).willReturn(okJson("{\"id\":\"synthetic-list\"}")));
    assertEquals("synthetic-list", provider.insertPlaylist("math", "private", budget));
    http.verify(
        postRequestedFor(urlPathEqualTo("/playlists"))
            .withQueryParam("part", equalTo("snippet,status"))
            .withRequestBody(matchingJsonPath("$.status.privacyStatus", equalTo("private"))));
    http.stubFor(
        get(urlPathEqualTo("/playlistItems"))
            .willReturn(
                okJson("{\"items\":[{\"contentDetails\":{\"videoId\":\"FIXTURE0001\"}}]}")));
    assertEquals(
        java.util.List.of("FIXTURE0001"), provider.playlistVideoIds("synthetic-list", budget));
    http.stubFor(get(urlPathEqualTo("/channels")).willReturn(okJson("{\"items\":[]}")));
    assertEquals(
        "ACCOUNT_MISMATCH",
        assertThrows(CuratorException.class, () -> provider.verifyAccount(budget)).code());
  }
}
