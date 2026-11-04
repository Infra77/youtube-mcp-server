package org.example.videocurator;

import static org.example.videocurator.domain.Models.*;
import static org.junit.jupiter.api.Assertions.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.time.*;
import java.util.*;
import java.util.concurrent.*;
import org.example.videocurator.application.*;
import org.example.videocurator.domain.*;
import org.example.videocurator.persistence.DraftStore;
import org.example.videocurator.provider.*;
import org.example.videocurator.quota.QuotaService;
import org.flywaydb.core.Flyway;
import org.junit.jupiter.api.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.transaction.support.TransactionTemplate;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.*;

@Testcontainers
class DatabaseIT {
  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

  JdbcTemplate db;
  TransactionTemplate tx;
  ObjectMapper json;
  Clock clock;
  QuotaService quota;
  DraftStore store;
  FixtureYouTubeProvider provider;
  CuratorService service;

  @BeforeEach
  void setup() {
    var ds =
        new DriverManagerDataSource(
            postgres.getJdbcUrl(), postgres.getUsername(), postgres.getPassword());
    Flyway.configure().dataSource(ds).load().migrate();
    db = new JdbcTemplate(ds);
    db.execute("TRUNCATE drafts,approvals,write_journal,quota_buckets,quota_reservations CASCADE");
    tx = new TransactionTemplate(new DataSourceTransactionManager(ds));
    json = new ObjectMapper().registerModule(new JavaTimeModule());
    clock = Clock.systemUTC();
    quota = new QuotaService(db, tx, clock, 10000, 100);
    store = new DraftStore(db, tx, json, clock);
    provider = new FixtureYouTubeProvider(json);
    service = new CuratorService(provider, quota, store, clock);
  }

  @Test
  void migrationAndFingerprintRoundtrip() {
    var d = plan();
    assertEquals(d, store.get(d.id(), provider.account()));
    assertEquals(64, d.fingerprint().length());
    assertThrows(CuratorException.class, () -> store.get(d.id(), "other-account"));
  }

  private DraftStore.Draft plan() {
    return service.plan(new Constraints("Fourier", 1800, 1200, "en", 3), "test");
  }

  @Test
  void unapprovedAndInjectedMetadataNeverWrites() {
    var d = plan();
    assertEquals(
        "APPROVAL_REQUIRED",
        assertThrows(CuratorException.class, () -> service.commit(d.id().toString())).code());
    assertEquals(0, provider.writes.get());
  }

  @Test
  void approvedCommitReadbackAndReplay() {
    var d = plan();
    store.approve(d.id(), provider.account(), "APPROVE " + d.fingerprint());
    service.commit(d.id().toString());
    assertEquals("CREATED", store.get(d.id(), provider.account()).state());
    int writes = provider.writes.get();
    service.commit(d.id().toString());
    assertEquals(writes, provider.writes.get());
    assertEquals(d.proposal().videos().size() + 1, writes);
  }

  @Test
  void fingerprintTamperAndWrongPhrase() {
    var d = plan();
    assertThrows(
        CuratorException.class, () -> store.approve(d.id(), provider.account(), "APPROVE wrong"));
    db.update("UPDATE drafts SET proposal=proposal||' ' WHERE id=?", d.id());
    assertEquals(
        "DRAFT_MISMATCH",
        assertThrows(CuratorException.class, () -> store.get(d.id(), provider.account())).code());
  }

  @Test
  void expiredApproval() {
    var d = plan();
    store.approve(d.id(), provider.account(), "APPROVE " + d.fingerprint());
    db.update("UPDATE approvals SET expires_at=now()-interval '1 minute'");
    assertEquals(
        "APPROVAL_REQUIRED",
        assertThrows(CuratorException.class, () -> service.commit(d.id().toString())).code());
    assertEquals(0, provider.writes.get());
  }

  @Test
  void eachInsufficientBucketRejectsBeforeAnyProviderCall() {
    for (var limits : List.of(new long[] {10000, 0}, new long[] {1, 100})) {
      var q = new QuotaService(db, tx, clock, limits[0], limits[1]);
      var s = new CuratorService(provider, q, store, clock);
      assertEquals(
          "QUOTA_BUDGET_EXCEEDED",
          assertThrows(CuratorException.class, () -> s.similar("FIXTURE0001", 5)).code());
      assertEquals(0, provider.calls.get());
    }
  }

  @Test
  void concurrentReservationsCannotOverspend() throws Exception {
    var q = new QuotaService(db, tx, clock, 1, 1);
    var ready = new CountDownLatch(1);
    try (var pool = Executors.newFixedThreadPool(2)) {
      Callable<Boolean> run =
          () -> {
            ready.await();
            try {
              q.reserve(1, 1);
              return true;
            } catch (CuratorException e) {
              return false;
            }
          };
      var a = pool.submit(run);
      var b = pool.submit(run);
      ready.countDown();
      assertNotEquals(a.get(), b.get());
    }
    assertEquals(
        1L,
        db.queryForObject(
            "SELECT reserved FROM quota_buckets WHERE bucket='GENERAL_UNITS'", Long.class));
  }

  @Test
  void concurrentCommitsWriteOnce() throws Exception {
    var d = plan();
    store.approve(d.id(), provider.account(), "APPROVE " + d.fingerprint());
    var gate = new CountDownLatch(1);
    try (var pool = Executors.newFixedThreadPool(2)) {
      Callable<Object> run =
          () -> {
            gate.await();
            try {
              return service.commit(d.id().toString());
            } catch (CuratorException e) {
              return e.code();
            }
          };
      var a = pool.submit(run);
      var b = pool.submit(run);
      gate.countDown();
      a.get();
      b.get();
    }
    assertEquals(d.proposal().videos().size() + 1, provider.writes.get());
    assertEquals("CREATED", store.get(d.id(), provider.account()).state());
  }

  @Test
  void quotaAttemptSettlesAndCrashConservativelyRetains() {
    var r = quota.reserve(5, 2);
    r.general(1);
    r.close();
    assertEquals(
        0L,
        db.queryForObject(
            "SELECT reserved FROM quota_buckets WHERE bucket='GENERAL_UNITS'", Long.class));
    assertEquals(
        1L,
        db.queryForObject(
            "SELECT consumed FROM quota_buckets WHERE bucket='GENERAL_UNITS'", Long.class));
    quota.reserve(3, 0);
    assertEquals(
        3L,
        db.queryForObject(
            "SELECT reserved FROM quota_buckets WHERE bucket='GENERAL_UNITS'", Long.class));
  }

  @Test
  void expiredCleanupAndAccountDeletion() {
    var d = plan();
    db.update("UPDATE drafts SET expires_at=now()-interval '1 minute' WHERE id=?", d.id());
    assertEquals(1, store.cleanupExpired());
    var next = plan();
    store.approve(next.id(), provider.account(), "APPROVE " + next.fingerprint());
    assertEquals(1, store.deleteAccount(provider.account()));
    assertEquals(0, db.queryForObject("SELECT count(*) FROM approvals", Integer.class));
  }

  @Test
  void partialWriteSurvivesRestartAndCannotBlindlyReplay() {
    var faulty = org.mockito.Mockito.spy(provider);
    org.mockito.Mockito.doThrow(
            new CuratorException("QUOTA_EXHAUSTED", "Synthetic upstream quota failure"))
        .when(faulty)
        .insertItem(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.eq(1),
            org.mockito.ArgumentMatchers.any());
    var s = new CuratorService(faulty, quota, store, clock);
    var d = s.plan(new Constraints("Fourier", 3000, 1200, "en", 3), "test");
    store.approve(d.id(), provider.account(), "APPROVE " + d.fingerprint());
    s.commit(d.id().toString());
    var reloaded = new DraftStore(db, tx, json, clock).get(d.id(), provider.account());
    assertEquals("PARTIAL", reloaded.state());
    assertNotNull(reloaded.remoteId());
    assertEquals(
        "WRITE_REVIEW_REQUIRED",
        assertThrows(CuratorException.class, () -> s.commit(d.id().toString())).code());
    org.mockito.Mockito.verify(faulty, org.mockito.Mockito.times(1))
        .insertPlaylist(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.any());
  }

  @Test
  void ambiguousCreateDoesNotRetry() {
    var faulty = org.mockito.Mockito.spy(provider);
    org.mockito.Mockito.doThrow(
            new CuratorException("UPSTREAM_AMBIGUOUS", "Synthetic lost response"))
        .when(faulty)
        .insertPlaylist(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.any());
    var s = new CuratorService(faulty, quota, store, clock);
    var d = plan();
    store.approve(d.id(), provider.account(), "APPROVE " + d.fingerprint());
    s.commit(d.id().toString());
    assertEquals("NEEDS_MANUAL_REVIEW", store.get(d.id(), provider.account()).state());
    assertThrows(CuratorException.class, () -> s.commit(d.id().toString()));
    org.mockito.Mockito.verify(faulty, org.mockito.Mockito.times(1))
        .insertPlaylist(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.any());
  }

  @Test
  void partialReportAndHumanRepairReconcileBeforeAppending() {
    var faulty = org.mockito.Mockito.spy(provider);
    org.mockito.Mockito.doThrow(new CuratorException("QUOTA_EXHAUSTED", "Synthetic"))
        .when(faulty)
        .insertItem(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.eq(1),
            org.mockito.ArgumentMatchers.any());
    var s = new CuratorService(faulty, quota, store, clock);
    var d = s.plan(new Constraints("Fourier", 3000, 1200, "en", 3), "test");
    store.approve(d.id(), provider.account(), "APPROVE " + d.fingerprint());
    var result = (Map<?, ?>) s.commit(d.id().toString());
    assertEquals(1, result.get("confirmedItemCount"));
    assertEquals(d.proposal().videos().size(), result.get("proposedItemCount"));
    assertThrows(CuratorException.class, () -> s.repair(d.id().toString(), "REPAIR wrong"));
    org.mockito.Mockito.doCallRealMethod()
        .when(faulty)
        .insertItem(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.eq(1),
            org.mockito.ArgumentMatchers.any());
    var repaired = (Map<?, ?>) s.repair(d.id().toString(), "REPAIR " + d.fingerprint());
    assertEquals("CREATED", repaired.get("state"));
    assertEquals(d.proposal().videos().size(), repaired.get("confirmedItemCount"));
    org.mockito.Mockito.verify(faulty, org.mockito.Mockito.times(1))
        .insertPlaylist(
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.anyString(),
            org.mockito.ArgumentMatchers.any());
  }

  @Test
  void retentionRemovesOldTerminalDraftsAndDiagnosticsSurviveRoundtrip() {
    var d = plan();
    assertNotNull(d.proposal().exclusions());
    assertEquals(2, d.proposal().schemaVersion());
    store.state(d.id(), "CREATED", "synthetic", null);
    db.update("UPDATE drafts SET created_at=now()-interval '8 days' WHERE id=?", d.id());
    assertEquals(1, store.cleanupExpired());
    assertThrows(CuratorException.class, () -> store.get(d.id(), provider.account()));
  }
}
