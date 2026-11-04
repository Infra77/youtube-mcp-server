package org.example.videocurator;

import static org.example.videocurator.domain.Models.*;
import static org.junit.jupiter.api.Assertions.*;

import java.time.*;
import java.util.*;
import org.example.videocurator.application.Analytics;
import org.example.videocurator.oauth.WindowsTokenVault;
import org.example.videocurator.quota.QuotaService;
import org.junit.jupiter.api.Test;

class SemanticsTest {
  @Test
  void rfcPkceKnownVectorAndState() {
    assertEquals(
        "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
        WindowsTokenVault.challenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"));
    assertTrue(WindowsTokenVault.stateMatches("expected", "expected"));
    assertFalse(WindowsTokenVault.stateMatches("expected", "wrong"));
    assertFalse(WindowsTokenVault.stateMatches("expected", null));
  }

  @Test
  void quotaDateUsesPacificDst() {
    assertEquals(
        LocalDate.of(2026, 3, 7),
        QuotaService.quotaDate(Clock.fixed(Instant.parse("2026-03-08T07:59:59Z"), ZoneOffset.UTC)));
    assertEquals(
        LocalDate.of(2026, 3, 8),
        QuotaService.quotaDate(Clock.fixed(Instant.parse("2026-03-08T08:00:00Z"), ZoneOffset.UTC)));
  }

  @Test
  void analyticsNoInventedLikeHistory() {
    var p =
        new PersonalData(
            List.of(new Video("FIXTURE0001", "test", "", "channel", "27", List.of(), 600, "en")),
            List.of(),
            List.of(),
            List.of(
                new Event(
                    "PLAYLIST_ITEM_ADDED_AT",
                    "FIXTURE0001",
                    Instant.parse("2026-01-15T00:00:00Z"))),
            Map.of("truncated", false));
    var report = Analytics.analyze(p, "2026-01-01", "2026-02-01", "2026-02-01", "2026-03-01");
    assertEquals(Map.of("PLAYLIST_ITEM_ADDED_AT:2026-01", 1L), report.get("trendsBySourceMonth"));
    assertFalse(report.toString().contains("LIKED_AT"));
    assertTrue(report.get("periodComparison").toString().contains("unavailable"));
  }
}
