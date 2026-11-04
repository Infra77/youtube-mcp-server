package org.example.videocurator.domain;

import static org.example.videocurator.domain.Models.*;

import java.util.*;
import java.util.stream.Collectors;

public final class Ranking {
  private static final Set<String> STOP =
      Set.of("a", "an", "the", "of", "and", "to", "in", "for", "with", "on", "is");

  public static Map<String, Double> terms(String text) {
    var counts = new TreeMap<String, Double>();
    for (String t : Objects.toString(text, "").toLowerCase(Locale.ROOT).split("[^\\p{L}\\p{N}]+"))
      if (!t.isBlank() && !STOP.contains(t)) counts.merge(t, 1.0, Double::sum);
    double total = counts.values().stream().mapToDouble(x -> x).sum();
    if (total > 0) counts.replaceAll((k, v) -> v / total);
    return counts;
  }

  public static List<Map<String, Double>> vectors(List<String> docs) {
    var tf = docs.stream().map(Ranking::terms).toList();
    var df = new HashMap<String, Integer>();
    tf.forEach(m -> m.keySet().forEach(t -> df.merge(t, 1, Integer::sum)));
    return tf.stream()
        .map(
            m -> {
              var v = new TreeMap<String, Double>();
              m.forEach(
                  (k, x) -> v.put(k, x * (Math.log((docs.size() + 1.0) / (df.get(k) + 1.0)) + 1)));
              return (Map<String, Double>) v;
            })
        .toList();
  }

  public static double cosine(Map<String, Double> a, Map<String, Double> b) {
    double dot = 0, na = 0, nb = 0;
    for (var e : a.entrySet()) {
      dot += e.getValue() * b.getOrDefault(e.getKey(), 0.0);
      na += e.getValue() * e.getValue();
    }
    for (double x : b.values()) nb += x * x;
    return na == 0 || nb == 0 ? 0 : Math.max(0, Math.min(1, dot / Math.sqrt(na * nb)));
  }

  public static List<RankedVideo> videos(Video seed, List<Video> raw, int limit) {
    var candidates =
        raw.stream()
            .filter(v -> !v.id().equals(seed.id()))
            .collect(Collectors.toMap(Video::id, v -> v, (a, b) -> a, TreeMap::new))
            .values()
            .stream()
            .toList();
    var texts = new ArrayList<String>();
    texts.add(seed.text());
    candidates.forEach(v -> texts.add(v.text()));
    var vec = vectors(texts);
    var result = new ArrayList<RankedVideo>();
    for (int i = 0; i < candidates.size(); i++) {
      Video v = candidates.get(i);
      var a = new HashSet<>(seed.tags());
      var b = new HashSet<>(v.tags());
      var union = new HashSet<>(a);
      union.addAll(b);
      a.retainAll(b);
      double tag = union.isEmpty() ? 0 : (double) a.size() / union.size();
      double category = knownEqual(seed.category(), v.category());
      double language = knownEqual(seed.language(), v.language());
      double duration =
          seed.seconds() > 0 && v.seconds() > 0
              ? (double) Math.min(seed.seconds(), v.seconds())
                  / Math.max(seed.seconds(), v.seconds())
              : 0;
      double text = cosine(vec.getFirst(), vec.get(i + 1));
      result.add(
          new RankedVideo(
              v,
              .55 * text + .20 * tag + .10 * category + .10 * duration + .05 * language,
              Map.of(
                  "text",
                  text,
                  "tags",
                  tag,
                  "category",
                  category,
                  "duration",
                  duration,
                  "language",
                  language)));
    }
    return result.stream()
        .sorted(
            Comparator.comparingDouble(RankedVideo::score)
                .reversed()
                .thenComparing(r -> r.video().id()))
        .limit(limit)
        .toList();
  }

  private static double knownEqual(String a, String b) {
    return a != null && !a.isBlank() && a.equals(b) ? 1 : 0;
  }

  public static List<RankedVideo> topic(String topic, List<Video> videos) {
    return videos(new Video("topic-seed", topic, "", "", "", List.of(), 0, ""), videos, 50);
  }
}
