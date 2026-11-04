package org.example.videocurator.domain;

import java.time.Instant;
import java.util.List;
import java.util.Map;

public final class Models {
  private Models() {}

  @com.fasterxml.jackson.annotation.JsonIgnoreProperties(value = "url", allowGetters = true)
  public record Video(
      String id,
      String title,
      String description,
      String channelId,
      String category,
      List<String> tags,
      long seconds,
      String language) {
    public Video {
      tags = tags == null ? List.of() : List.copyOf(tags);
    }

    @com.fasterxml.jackson.annotation.JsonProperty("url")
    public String url() {
      return "https://www.youtube.com/watch?v=" + id;
    }

    public String text() {
      return title + " " + title + " " + String.join(" ", tags) + " " + description;
    }
  }

  public record Channel(String id, String title, String description) {
    @com.fasterxml.jackson.annotation.JsonProperty("url")
    public String url() {
      return "https://www.youtube.com/channel/" + id;
    }

    public String text() {
      return title + " " + description;
    }
  }

  public record Event(String source, String entityId, Instant addedAt) {}

  public record PersonalData(
      List<Video> likes,
      List<Channel> subscriptions,
      List<Video> playlistVideos,
      List<Event> events,
      Map<String, Object> coverage) {}

  public record RankedVideo(Video video, double score, Map<String, Double> components) {}

  public record Constraints(
      String topic, long targetSeconds, long maxVideoSeconds, String language, int maxVideos) {
    public Constraints {
      if (topic == null
          || topic.isBlank()
          || topic.length() > 200
          || topic.chars().anyMatch(c -> c < 32))
        throw new CuratorException(
            "INVALID_INPUT", "Topic must contain 1–200 printable characters.");
      if (targetSeconds < 1
          || targetSeconds > 86400
          || maxVideoSeconds < 1
          || maxVideoSeconds > 86400
          || maxVideos < 1
          || maxVideos > 50)
        throw new CuratorException(
            "INVALID_INPUT", "Duration must be 1–86400 seconds and maxVideos 1–50.");
      if (language == null || !language.matches("[a-z]{2,3}(-[A-Za-z]{2,8})?"))
        throw new CuratorException(
            "NEEDS_CLARIFICATION", "Provide an explicit language code such as en.");
    }
  }

  public record Selection(
      List<Video> videos,
      long totalSeconds,
      long shortfallSeconds,
      Map<String, String> exclusions) {}

  public record Proposal(
      int schemaVersion,
      String account,
      String title,
      String privacy,
      Constraints constraints,
      List<Video> videos,
      long totalSeconds,
      long shortfallSeconds,
      Instant expiresAt,
      String policy,
      String requestText,
      Map<String, String> exclusions) {
    public Proposal {
      exclusions =
          exclusions == null
              ? Map.of()
              : java.util.Collections.unmodifiableMap(new java.util.TreeMap<>(exclusions));
      videos = List.copyOf(videos);
    }
  }
}
