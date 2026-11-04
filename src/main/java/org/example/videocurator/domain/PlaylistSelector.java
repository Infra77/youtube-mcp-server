package org.example.videocurator.domain;

import static org.example.videocurator.domain.Models.*;

import java.util.*;
import java.util.regex.Pattern;

public final class PlaylistSelector {
  public static Selection select(List<RankedVideo> candidates, Constraints c) {
    var chosen = new ArrayList<Video>();
    var seen = new HashSet<String>();
    var excluded = new TreeMap<String, String>();
    long used = 0;
    var ranked =
        candidates.stream()
            .sorted(
                Comparator.comparingDouble(RankedVideo::score)
                    .reversed()
                    .thenComparing(r -> r.video().id()))
            .toList();
    for (var r : ranked) {
      Video v = r.video();
      if (!seen.add(v.id())) continue;
      String reason =
          v.seconds() <= 0 || v.seconds() > c.maxVideoSeconds()
              ? "DURATION"
              : !languageMatches(v.language(), c.language())
                  ? "LANGUAGE_UNVERIFIED"
                  : chosen.size() >= c.maxVideos() || used + v.seconds() > c.targetSeconds()
                      ? "CAPACITY"
                      : null;
      if (reason != null) excluded.put(v.id(), reason);
      else {
        chosen.add(v);
        used += v.seconds();
      }
    }
    // One bounded one-for-two improvement pass: O(n^3), n <= 50 at the service boundary.
    // This repairs common greedy underfill without an exponential subset search.
    var byId = new HashMap<String, RankedVideo>();
    for (var item : ranked) byId.putIfAbsent(item.video().id(), item);
    var chosenIds = new HashSet<String>();
    chosen.forEach(video -> chosenIds.add(video.id()));
    double bestGain = 0;
    Video remove = null, addA = null, addB = null;
    if (chosen.size() < c.maxVideos())
      for (Video old : chosen)
        for (int i = 0; i < ranked.size(); i++)
          for (int j = i + 1; j < ranked.size(); j++) {
            Video a = ranked.get(i).video(), b = ranked.get(j).video();
            if (a.id().equals(b.id()) || chosenIds.contains(a.id()) || chosenIds.contains(b.id()))
              continue;
            if (!"CAPACITY".equals(excluded.get(a.id()))
                || !"CAPACITY".equals(excluded.get(b.id()))) continue;
            double gain =
                ranked.get(i).score() + ranked.get(j).score() - byId.get(old.id()).score();
            if (used - old.seconds() + a.seconds() + b.seconds() <= c.targetSeconds()
                && gain > bestGain + 1e-12) {
              bestGain = gain;
              remove = old;
              addA = a;
              addB = b;
            }
          }
    if (remove != null) {
      chosen.remove(remove);
      chosen.add(addA);
      chosen.add(addB);
      used = used - remove.seconds() + addA.seconds() + addB.seconds();
      excluded.put(remove.id(), "REPLACED_FOR_HIGHER_COMBINED_RELEVANCE");
      excluded.remove(addA.id());
      excluded.remove(addB.id());
      chosen.sort(
          Comparator.comparingDouble((Video v) -> byId.get(v.id()).score())
              .reversed()
              .thenComparing(Video::id));
    }
    if (chosen.isEmpty())
      throw new CuratorException(
          "NO_FEASIBLE_PLAYLIST", "No candidates satisfy the hard constraints.");
    return new Selection(List.copyOf(chosen), used, c.targetSeconds() - used, Map.copyOf(excluded));
  }

  private static boolean languageMatches(String declared, String requested) {
    if (declared == null || !declared.matches("[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*")) return false;
    return requested.contains("-")
        ? declared.equalsIgnoreCase(requested)
        : declared.split("-")[0].equalsIgnoreCase(requested);
  }

  public static Constraints parse(String text) {
    Input.require(
        text != null && text.length() <= 1000, "Request must contain at most 1000 characters.");
    var pattern =
        Pattern.compile(
            "(?i)^\\s*(?:make|create|build) (?:a )?(\\d+)[ -]?(hour|minute|min)s? (English|Hindi|Spanish|French) playlist on (.{1,200}?), (?:maximum|max) (\\d+) (minute|min|second|hour)s? per video[.!]?\\s*$");
    var m = pattern.matcher(text);
    if (!m.matches())
      throw new CuratorException(
          "NEEDS_CLARIFICATION",
          "Use: Make a 2-hour English playlist on Fourier transforms, maximum 20 minutes per video; or provide typed constraints.");
    try {
      long total =
          Math.multiplyExact(
              Long.parseLong(m.group(1)), (m.group(2).equalsIgnoreCase("hour") ? 3600 : 60));
      long maximum =
          Math.multiplyExact(
              Long.parseLong(m.group(5)),
              switch (m.group(6).toLowerCase(Locale.ROOT)) {
                case "hour" -> 3600;
                case "second" -> 1;
                default -> 60;
              });
      String lang =
          Map.of("english", "en", "hindi", "hi", "spanish", "es", "french", "fr")
              .get(m.group(3).toLowerCase(Locale.ROOT));
      return new Constraints(m.group(4), total, maximum, lang, 50);
    } catch (NumberFormatException | ArithmeticException e) {
      throw new CuratorException("INVALID_INPUT", "Duration is too large.");
    }
  }
}
