package org.example.videocurator;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.time.Clock;
import org.example.videocurator.application.CuratorService;
import org.example.videocurator.domain.CuratorException;
import org.example.videocurator.persistence.DraftStore;
import org.example.videocurator.provider.YouTubeProvider;
import org.example.videocurator.quota.QuotaService;
import org.junit.jupiter.api.Test;

class ServiceTest {
  @Test
  void invalidInputsCauseNoProviderOrQuotaCall() {
    var provider = mock(YouTubeProvider.class);
    var quota = mock(QuotaService.class);
    var s = new CuratorService(provider, quota, mock(DraftStore.class), Clock.systemUTC());
    assertThrows(CuratorException.class, () -> s.similar("https://evil.example/video", 4));
    assertThrows(CuratorException.class, () -> s.channels("bad", 4));
    assertThrows(CuratorException.class, () -> s.analyze(null, "2026-03-01", null, null));
    assertThrows(
        CuratorException.class,
        () -> s.analyze("2026-03-01", "2026-01-01", "2026-02-01", "2026-03-01"));
    verifyNoInteractions(provider, quota);
  }

  @Test
  void everyReadWorkflowRejectsBeforeProviderWhenPreflightFails() {
    var provider = mock(YouTubeProvider.class);
    var quota = mock(QuotaService.class);
    when(quota.reserve(anyLong(), anyLong()))
        .thenThrow(new CuratorException("QUOTA_BUDGET_EXCEEDED", "No budget"));
    var s = new CuratorService(provider, quota, mock(DraftStore.class), Clock.systemUTC());
    assertThrows(CuratorException.class, () -> s.overview("FIXTURE0001"));
    assertThrows(CuratorException.class, () -> s.similar("FIXTURE0001", 5));
    assertThrows(CuratorException.class, () -> s.channels("@ExampleMath", 5));
    assertThrows(CuratorException.class, () -> s.recommend(5));
    assertThrows(CuratorException.class, () -> s.analyze(null, null, null, null));
    verifyNoInteractions(provider);
  }
}
