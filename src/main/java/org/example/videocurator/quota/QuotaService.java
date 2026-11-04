package org.example.videocurator.quota;

import java.time.*;
import java.util.*;
import org.example.videocurator.domain.CuratorException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.support.TransactionTemplate;

/** Durable project-wide quota; conservative outstanding reservations survive crashes. */
public final class QuotaService {
  public static final String GENERAL = "GENERAL_UNITS", SEARCH = "SEARCH_CALLS";
  private final JdbcTemplate db;
  private final TransactionTemplate tx;
  private final Clock clock;
  private final long generalLimit, searchLimit;

  public QuotaService(
      JdbcTemplate db, TransactionTemplate tx, Clock clock, long generalLimit, long searchLimit) {
    this.db = db;
    this.tx = tx;
    this.clock = clock;
    this.generalLimit = generalLimit;
    this.searchLimit = searchLimit;
  }

  public static LocalDate quotaDate(Clock clock) {
    return LocalDate.now(clock.withZone(ZoneId.of("America/Los_Angeles")));
  }

  public Reservation reserve(long general, long searches) {
    if (general < 0 || searches < 0) throw new IllegalArgumentException("Negative quota plan");
    return tx.execute(
        s -> {
          LocalDate day = quotaDate(clock);
          UUID id = UUID.randomUUID();
          for (String bucket : List.of(GENERAL, SEARCH)) {
            long limit = bucket.equals(GENERAL) ? generalLimit : searchLimit,
                amount = bucket.equals(GENERAL) ? general : searches;
            db.update(
                "INSERT INTO quota_buckets(quota_date,bucket,configured_limit) VALUES (?,?,?) ON CONFLICT DO NOTHING",
                day,
                bucket,
                limit);
            var row =
                db.queryForMap(
                    "SELECT * FROM quota_buckets WHERE quota_date=? AND bucket=? FOR UPDATE",
                    day,
                    bucket);
            long consumed = ((Number) row.get("consumed")).longValue(),
                reserved = ((Number) row.get("reserved")).longValue();
            long stored = ((Number) row.get("configured_limit")).longValue();
            if (amount > Math.min(limit, stored) - consumed - reserved)
              throw new CuratorException(
                  "QUOTA_BUDGET_EXCEEDED",
                  "Insufficient " + bucket + " for complete workflow; no API call made.");
            db.update(
                "UPDATE quota_buckets SET reserved=reserved+? WHERE quota_date=? AND bucket=?",
                amount,
                day,
                bucket);
            db.update(
                "INSERT INTO quota_reservations(id,quota_date,bucket,amount) VALUES (?,?,?,?)",
                id,
                day,
                bucket,
                amount);
          }
          return new Reservation(id, day);
        });
  }

  public List<Map<String, Object>> status() {
    return db.queryForList(
        "SELECT bucket,configured_limit,consumed,reserved,quota_date FROM quota_buckets WHERE quota_date=? ORDER BY bucket",
        quotaDate(clock));
  }

  public final class Reservation implements AutoCloseable {
    private final UUID id;
    private final LocalDate day;
    private boolean closed;

    private Reservation(UUID id, LocalDate day) {
      this.id = id;
      this.day = day;
    }

    public void general(long cost) {
      attempt(GENERAL, cost);
    }

    public void search() {
      attempt(SEARCH, CostCatalog.search());
    }

    private void attempt(String bucket, long cost) {
      if (cost <= 0) throw new IllegalArgumentException("Invalid cost");
      tx.executeWithoutResult(
          s -> {
            if (!day.equals(quotaDate(clock)))
              throw new CuratorException(
                  "QUOTA_DAY_CHANGED",
                  "Quota day changed; start a new read workflow or review interrupted write.");
            int n =
                db.update(
                    "UPDATE quota_reservations SET used=used+? WHERE id=? AND bucket=? AND NOT settled AND used+?<=amount",
                    cost,
                    id,
                    bucket,
                    cost);
            if (n != 1)
              throw new CuratorException("QUOTA_PLAN_EXCEEDED", "Call exceeds reserved plan.");
            db.update(
                "UPDATE quota_buckets SET reserved=reserved-?,consumed=consumed+? WHERE quota_date=? AND bucket=?",
                cost,
                cost,
                day,
                bucket);
          });
    }

    public void close() {
      if (closed) return;
      tx.executeWithoutResult(
          s -> {
            var rows =
                db.queryForList(
                    "SELECT * FROM quota_reservations WHERE id=? ORDER BY bucket FOR UPDATE", id);
            for (var row : rows)
              if (!Boolean.TRUE.equals(row.get("settled"))) {
                long unused =
                    ((Number) row.get("amount")).longValue()
                        - ((Number) row.get("used")).longValue();
                db.update(
                    "UPDATE quota_buckets SET reserved=reserved-? WHERE quota_date=? AND bucket=?",
                    unused,
                    day,
                    row.get("bucket"));
                db.update(
                    "UPDATE quota_reservations SET settled=true WHERE id=? AND bucket=?",
                    id,
                    row.get("bucket"));
              }
          });
      closed = true;
    }
  }
}
