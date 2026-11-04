package org.example.videocurator.application;

import static org.example.videocurator.domain.Models.*;

import java.time.*;
import java.util.*;
import org.example.videocurator.domain.Input;

public final class Analytics {
  public static Map<String, Object> analyze(
      PersonalData p, String startA, String endA, String startB, String endB) {
    var videos = new TreeMap<String, Video>();
    p.likes().forEach(v -> videos.put(v.id(), v));
    p.playlistVideos().forEach(v -> videos.put(v.id(), v));
    var channelCounts = new TreeMap<String, Long>();
    var categories = new TreeMap<String, Long>();
    var bins = new TreeMap<String, Long>();
    var trends = new TreeMap<String, Long>();
    var subscriptions = new TreeMap<String, Long>();
    var durations = new ArrayList<Long>();
    for (Video v : videos.values()) {
      channelCounts.merge(v.channelId().isBlank() ? "UNKNOWN" : v.channelId(), 1L, Long::sum);
      categories.merge(v.category().isBlank() ? "UNKNOWN" : v.category(), 1L, Long::sum);
      if (v.seconds() > 0) {
        durations.add(v.seconds());
        bins.merge(
            v.seconds() <= 600
                ? "short_0_600"
                : v.seconds() <= 1200 ? "medium_601_1200" : "long_1201_plus",
            1L,
            Long::sum);
      } else bins.merge("unknown", 1L, Long::sum);
    }
    p.subscriptions().forEach(c -> subscriptions.merge(c.id(), 1L, Long::sum));
    Collections.sort(durations);
    for (Event e : p.events())
      if (e.addedAt() != null)
        trends.merge(
            e.source() + ":" + YearMonth.from(e.addedAt().atZone(ZoneOffset.UTC)), 1L, Long::sum);
    var result = new LinkedHashMap<String, Object>();
    result.put("coverage", p.coverage());
    result.put("channelCounts", channelCounts);
    result.put("categoryCounts", categories);
    result.put("subscriptionCounts", subscriptions);
    result.put("durationBins", bins);
    result.put(
        "medianSeconds",
        durations.isEmpty()
            ? "unavailable"
            : durations.size() % 2 == 1
                ? durations.get(durations.size() / 2)
                : (durations.get(durations.size() / 2 - 1) + durations.get(durations.size() / 2))
                    / 2.0);
    result.put("trendsBySourceMonth", trends);
    result.put(
        "unknownEventTimestamps", p.events().stream().filter(e -> e.addedAt() == null).count());
    if (startA != null && !startA.isBlank()) {
      Instant a = day(startA), b = day(endA), c = day(startB), d = day(endB);
      Input.require(a.isBefore(b) && c.isBefore(d), "Each period start must precede its end.");
      var comparisons = new TreeMap<String, Object>();
      for (String source : List.of("SUBSCRIPTION_ADDED_AT", "PLAYLIST_ITEM_ADDED_AT")) {
        var events =
            p.events().stream()
                .filter(e -> e.source().equals(source) && e.addedAt() != null)
                .toList();
        comparisons.put(
            source,
            events.isEmpty()
                ? Map.of("status", "unavailable")
                : Map.of(
                    "status",
                    "sampled_events_only",
                    "periodA",
                    events.stream()
                        .filter(e -> !e.addedAt().isBefore(a) && e.addedAt().isBefore(b))
                        .count(),
                    "periodB",
                    events.stream()
                        .filter(e -> !e.addedAt().isBefore(c) && e.addedAt().isBefore(d))
                        .count()));
      }
      result.put("periodComparison", comparisons);
    } else result.put("periodComparison", Map.of("status", "not_requested"));
    result.put(
        "warnings",
        List.of(
            "No watch history or like timestamps are available.",
            "Counts and trends describe sampled accessible records, not all viewing activity."));
    return result;
  }

  public static Instant day(String s) {
    try {
      return LocalDate.parse(s).atStartOfDay(ZoneOffset.UTC).toInstant();
    } catch (Exception e) {
      throw new org.example.videocurator.domain.CuratorException(
          "INVALID_INPUT", "Dates must use YYYY-MM-DD.");
    }
  }
}
