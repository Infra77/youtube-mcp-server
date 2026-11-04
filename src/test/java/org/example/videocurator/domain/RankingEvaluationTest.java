package org.example.videocurator.domain;

import static org.example.videocurator.domain.Models.*;
import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.*;
import java.util.*;
import org.junit.jupiter.api.Test;

class RankingEvaluationTest {
  private Video video(String id, String text) {
    return new Video(id, text, "", "UC0000000000000000000000", "27", List.of(), 600, "en");
  }

  @Test
  void labeledPrecisionAndRepresentativeTiming() throws Exception {
    String[][] cases = {
      {
        "discrete convolution",
        "discrete convolution worked examples",
        "discrete convolution tutorial"
      },
      {
        "linear algebra matrices",
        "linear algebra matrices exercises",
        "linear algebra matrices introduction"
      },
      {
        "binary search algorithm",
        "binary search algorithm implementation",
        "binary search algorithm complexity"
      },
      {
        "electric circuits voltage",
        "electric circuits voltage exercises",
        "electric circuits voltage fundamentals"
      }
    };
    double precision = 0;
    long started = System.nanoTime();
    for (var c : cases) {
      var seed = video("SEED0000001", c[0]);
      var ranked =
          Ranking.videos(
              seed,
              List.of(
                  video("RELEVANT001", c[1]),
                  video("RELEVANT002", c[2]),
                  video("DISTRACT001", "celebrity daily vlog"),
                  video("DISTRACT002", "banana cooking recipe")),
              2);
      precision += ranked.stream().filter(v -> v.video().id().startsWith("RELEVANT")).count() / 2.0;
    }
    precision /= cases.length;
    assertEquals(1.0, precision);
    var fifty = new ArrayList<Video>();
    for (int i = 0; i < 50; i++)
      fifty.add(
          video(String.format(Locale.ROOT, "CANDID%05d", i), "discrete convolution example " + i));
    for (int i = 0; i < 100; i++) {
      var ranked = Ranking.topic("discrete convolution", fifty);
      PlaylistSelector.select(
          ranked, new Constraints("discrete convolution", 7200, 1200, "en", 50));
    }
    double millis = (System.nanoTime() - started) / 1_000_000.0;
    assertTrue(millis < 10000, "100 bounded workflows exceeded 10 seconds");
    Files.createDirectories(Path.of("target/evidence"));
    Files.writeString(
        Path.of("target/evidence/ranking-evaluation.json"),
        "{\"status\":\"PASS\",\"precisionAt2\":"
            + precision
            + ",\"labeledCases\":4,\"candidateLimit\":50,\"iterations\":100,\"elapsedMillis\":"
            + millis
            + ",\"labels\":\"synthetic author labels; human relevance review required\"}");
  }
}
