package org.example.videocurator.provider;

import static org.example.videocurator.domain.Models.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import org.example.videocurator.domain.CuratorException;
import org.example.videocurator.quota.CostCatalog;
import org.example.videocurator.quota.QuotaService.Reservation;

public final class FixtureYouTubeProvider implements YouTubeProvider {
  private final List<Video> videos;
  private final List<Channel> channels;
  public final AtomicInteger calls = new AtomicInteger(), writes = new AtomicInteger();
  private final Map<String, List<String>> playlists = new HashMap<>();

  public FixtureYouTubeProvider(ObjectMapper json) {
    try (var in = getClass().getResourceAsStream("/fixtures/videos.json")) {
      videos = List.of(json.readValue(in, Video[].class));
    } catch (Exception e) {
      throw new IllegalStateException("Synthetic fixtures unavailable", e);
    }
    channels =
        List.of(
            new Channel(
                "UC0000000000000000000000", "Fixture Math", "Fourier convolution mathematics"),
            new Channel(
                "UC1111111111111111111111",
                "Fixture Signals",
                "Fourier discrete signal processing"),
            new Channel("UC2222222222222222222222", "Fixture Cooking", "Cooking banana recipes"));
  }

  private void read(Reservation r) {
    r.general(CostCatalog.read());
    calls.incrementAndGet();
  }

  public Video video(String id, Reservation r) {
    read(r);
    return videos.stream()
        .filter(v -> v.id().equals(id))
        .findFirst()
        .orElseThrow(
            () -> new CuratorException("VIDEO_UNAVAILABLE", "Video is unavailable or private."));
  }

  public List<Video> searchVideos(String topic, Reservation r) {
    r.search();
    calls.incrementAndGet();
    read(r);
    return videos;
  }

  public Channel channel(String selector, Reservation r) {
    read(r);
    return channels.stream()
        .filter(
            c ->
                c.id().equals(selector)
                    || selector.equals("@ExampleMath") && c == channels.getFirst())
        .findFirst()
        .orElseThrow(() -> new CuratorException("CHANNEL_UNAVAILABLE", "No channel matched."));
  }

  public List<Channel> searchChannels(String topic, Reservation r) {
    r.search();
    calls.incrementAndGet();
    read(r);
    return channels;
  }

  public PersonalData personal(Reservation r) {
    for (int i = 0; i < 5; i++) read(r);
    return new PersonalData(
        List.of(videos.getFirst()),
        List.of(channels.getFirst()),
        List.of(videos.get(1)),
        List.of(
            new Event(
                "SUBSCRIPTION_ADDED_AT",
                channels.getFirst().id(),
                Instant.parse("2026-01-15T00:00:00Z")),
            new Event(
                "PLAYLIST_ITEM_ADDED_AT",
                videos.get(1).id(),
                Instant.parse("2026-02-15T00:00:00Z"))),
        Map.of(
            "likesFetched",
            1,
            "subscriptionsFetched",
            1,
            "playlistsFetched",
            1,
            "playlistItemsFetched",
            1,
            "truncated",
            false));
  }

  public synchronized String insertPlaylist(String title, String privacy, Reservation r) {
    r.general(CostCatalog.write());
    writes.incrementAndGet();
    String id = "fixture-playlist-" + UUID.randomUUID();
    playlists.put(id, new ArrayList<>());
    return id;
  }

  public synchronized String insertItem(
      String playlist, String video, int position, Reservation r) {
    r.general(CostCatalog.write());
    writes.incrementAndGet();
    playlists.computeIfAbsent(playlist, k -> new ArrayList<>()).add(video);
    return "fixture-item-" + position;
  }

  public synchronized List<String> playlistVideoIds(String id, Reservation r) {
    read(r);
    return List.copyOf(playlists.getOrDefault(id, List.of()));
  }

  public String account() {
    return "fixture-account";
  }

  public boolean fixture() {
    return true;
  }
}
