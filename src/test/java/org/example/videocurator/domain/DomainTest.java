package org.example.videocurator.domain;

import static org.example.videocurator.domain.Models.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import org.junit.jupiter.api.Test;

class DomainTest {
  @Test
  void parsesSupportedIdsAndRejectsHostAndAmbiguousParameters() {
    for (String s :
        List.of(
            "ABCDEF12345",
            "https://youtu.be/ABCDEF12345",
            "https://WWW.YOUTUBE.COM/watch?v=ABCDEF12345&list=x",
            "https://youtube.com/shorts/ABCDEF12345")) assertEquals("ABCDEF12345", Input.video(s));
    for (String s :
        List.of(
            "https://youtube.com.evil.test/watch?v=ABCDEF12345",
            "https://youtube.com/watch?v=ABCDEF12345&v=other123456",
            "http://user@youtube.com/watch?v=ABCDEF12345",
            "https://youtube.com/%77atch?v=ABCDEF12345",
            "nope")) assertThrows(CuratorException.class, () -> Input.video(s));
  }

  @Test
  void durationIsExactAndPositive() {
    assertEquals(93600, Input.duration("P1DT2H"));
    assertEquals(45, Input.duration("PT45S"));
    for (String s : List.of("PT0S", "-PT1S", "PT0.5S", "bad"))
      assertThrows(CuratorException.class, () -> Input.duration(s));
  }

  @Test
  void tfidfAndZeroVectors() {
    var v =
        Ranking.vectors(
            List.of(
                "convolution discrete example", "convolution discrete example", "banana cooking"));
    assertEquals(1, Ranking.cosine(v.get(0), v.get(1)), 1e-9);
    assertEquals(0, Ranking.cosine(v.get(0), v.get(2)));
    assertEquals(0, Ranking.cosine(Map.of(), Map.of()));
  }

  @Test
  void hardConstraintsAndUnknownLanguage() {
    var candidates =
        List.of(
            rank("AAAAAAAAAAA", 1200, "en", 1),
            rank("BBBBBBBBBBB", 1201, "en", 2),
            rank("CCCCCCCCCCC", 600, "", 3));
    var selected =
        PlaylistSelector.select(candidates, new Constraints("math", 1200, 1200, "en", 5));
    assertEquals(1200, selected.totalSeconds());
    assertEquals(1, selected.videos().size());
    assertEquals("AAAAAAAAAAA", selected.videos().getFirst().id());
  }

  @Test
  void selectorDeterministicAndRepairsGreedyUnderfill() {
    var a = rank("AAAAAAAAAAA", 1200, "en", 1);
    var b = rank("BBBBBBBBBBB", 660, "en", .8);
    var c = rank("CCCCCCCCCCC", 660, "en", .7);
    var limits = new Constraints("math", 1320, 1320, "en", 5);
    assertEquals(
        PlaylistSelector.select(List.of(a, b, c), limits),
        PlaylistSelector.select(List.of(c, a, b), limits));
    assertEquals(0, PlaylistSelector.select(List.of(a, b, c), limits).shortfallSeconds());
  }

  @Test
  void textGrammarDoesNotGuessAmbiguousNumbers() {
    assertEquals(
        7200,
        PlaylistSelector.parse(
                "Make a 2-hour English playlist on Fourier transforms, maximum 20 minutes per video")
            .targetSeconds());
    assertThrows(
        CuratorException.class,
        () -> PlaylistSelector.parse("six 20-minute videos in a 2-hour playlist"));
    assertThrows(
        CuratorException.class, () -> PlaylistSelector.parse("Create a playlist on calculus"));
    assertThrows(
        CuratorException.class,
        () ->
            PlaylistSelector.parse(
                "Make a 9223372036854775807-hour English playlist on math, maximum 20 minutes per video"));
  }

  @Test
  void handlesAndAliases() {
    assertEquals("@ExampleMath", Input.channel("https://youtube.com/@ExampleMath"));
    assertThrows(CuratorException.class, () -> Input.channel("https://youtube.com/c/custom"));
  }

  @Test
  void languageRegionIsNotSilentlyRelaxedAndMalformedMetadataIsExcluded() {
    var choices =
        List.of(
            rank("AAAAAAAAAAA", 600, "en-GB", 3),
            rank("BBBBBBBBBBB", 600, "en-US", 2),
            rank("CCCCCCCCCCC", 600, "-", 4));
    var exact = PlaylistSelector.select(choices, new Constraints("math", 1800, 600, "en-US", 3));
    assertEquals(List.of("BBBBBBBBBBB"), exact.videos().stream().map(Video::id).toList());
    var primary = PlaylistSelector.select(choices, new Constraints("math", 1800, 600, "en", 3));
    assertEquals(2, primary.videos().size());
  }

  private RankedVideo rank(String id, long seconds, String language, double score) {
    return new RankedVideo(
        new Video(id, "math", "", "UC0000000000000000000000", "27", List.of(), seconds, language),
        score,
        Map.of());
  }
}
