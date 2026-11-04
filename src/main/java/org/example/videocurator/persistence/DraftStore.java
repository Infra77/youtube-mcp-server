package org.example.videocurator.persistence;

import static org.example.videocurator.domain.Models.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.sql.Timestamp;
import java.time.*;
import java.util.*;
import org.example.videocurator.domain.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.support.TransactionTemplate;

public final class DraftStore {
  private final JdbcTemplate db;
  private final TransactionTemplate tx;
  private final ObjectMapper json;
  private final Clock clock;

  public DraftStore(JdbcTemplate db, TransactionTemplate tx, ObjectMapper json, Clock clock) {
    this.db = db;
    this.tx = tx;
    this.json = json;
    this.clock = clock;
  }

  public record Draft(
      UUID id,
      Proposal proposal,
      String fingerprint,
      String state,
      String remoteId,
      List<Map<String, Object>> journal) {}

  public String canonical(Proposal p) {
    try {
      return json.writeValueAsString(p);
    } catch (Exception e) {
      throw new IllegalStateException("Proposal serialization failed");
    }
  }

  public String digest(String canonical) {
    try {
      return HexFormat.of()
          .formatHex(
              MessageDigest.getInstance("SHA-256")
                  .digest(canonical.getBytes(StandardCharsets.UTF_8)));
    } catch (Exception e) {
      throw new IllegalStateException(e);
    }
  }

  public Draft save(Proposal p) {
    UUID id = UUID.randomUUID();
    String text = canonical(p);
    db.update(
        "INSERT INTO drafts(id,account,proposal,fingerprint,expires_at) VALUES (?,?,?,?,?)",
        id,
        p.account(),
        text,
        digest(text),
        Timestamp.from(p.expiresAt()));
    return get(id, p.account());
  }

  public Draft get(UUID id, String account) {
    var rows = db.queryForList("SELECT * FROM drafts WHERE id=? AND account=?", id, account);
    if (rows.isEmpty())
      throw new CuratorException("DRAFT_NOT_FOUND", "No draft for this local account.");
    var r = rows.getFirst();
    String text = (String) r.get("proposal");
    if (!digest(text).equals(r.get("fingerprint")))
      throw new CuratorException("DRAFT_MISMATCH", "Stored proposal fingerprint does not match.");
    try {
      return new Draft(
          id,
          json.readValue(text, Proposal.class),
          (String) r.get("fingerprint"),
          (String) r.get("state"),
          (String) r.get("remote_id"),
          db.queryForList(
              "SELECT step,status,remote_id,error_code FROM write_journal WHERE draft_id=? ORDER BY step",
              id));
    } catch (CuratorException e) {
      throw e;
    } catch (Exception e) {
      throw new CuratorException("DRAFT_INVALID", "Stored proposal cannot be read safely.");
    }
  }

  /** Only called by the interactive CLI, never registered as an MCP tool. */
  public void approve(UUID id, String account, String phrase) {
    tx.executeWithoutResult(
        s -> {
          db.queryForList("SELECT id FROM drafts WHERE id=? FOR UPDATE", id);
          Draft d = get(id, account);
          if (!d.state().equals("PROPOSED"))
            throw new CuratorException("DRAFT_STATE", "Only a proposed draft can be approved.");
          if (!d.proposal().expiresAt().isAfter(clock.instant()))
            throw new CuratorException("DRAFT_EXPIRED", "Draft expired.");
          if (!MessageDigest.isEqual(
              ("APPROVE " + d.fingerprint()).getBytes(StandardCharsets.UTF_8),
              Objects.toString(phrase, "").getBytes(StandardCharsets.UTF_8)))
            throw new CuratorException("APPROVAL_MISMATCH", "Typed fingerprint did not match.");
          Instant expires = clock.instant().plusSeconds(600);
          if (expires.isAfter(d.proposal().expiresAt())) expires = d.proposal().expiresAt();
          db.update(
              "INSERT INTO approvals(draft_id,account,fingerprint,expires_at) VALUES (?,?,?,?)",
              id,
              account,
              d.fingerprint(),
              Timestamp.from(expires));
          db.update("UPDATE drafts SET state='APPROVED' WHERE id=?", id);
        });
  }

  public boolean claim(UUID id, String account) {
    return Boolean.TRUE.equals(
        tx.execute(
            s -> {
              db.queryForList("SELECT id FROM drafts WHERE id=? FOR UPDATE", id);
              Draft d = get(id, account);
              if (d.state().equals("CREATED")) return false;
              if (!d.proposal().expiresAt().isAfter(clock.instant()))
                throw new CuratorException("DRAFT_EXPIRED", "Draft expired.");
              if (!d.state().equals("APPROVED"))
                throw new CuratorException(
                    d.state().equals("PROPOSED") ? "APPROVAL_REQUIRED" : "WRITE_REVIEW_REQUIRED",
                    "Local approval required, or prior write needs reconciliation; no replay attempted.");
              int n =
                  db.update(
                      "UPDATE approvals SET consumed_at=? WHERE draft_id=? AND account=? AND fingerprint=? AND consumed_at IS NULL AND expires_at>?",
                      Timestamp.from(clock.instant()),
                      id,
                      account,
                      d.fingerprint(),
                      Timestamp.from(clock.instant()));
              if (n != 1)
                throw new CuratorException(
                    "APPROVAL_REQUIRED", "Valid unconsumed exact-draft approval required.");
              db.update("UPDATE drafts SET state='CREATING' WHERE id=?", id);
              return true;
            }));
  }

  public void journal(UUID id, String step, String status, String remote, String error) {
    db.update(
        "INSERT INTO write_journal(draft_id,step,status,remote_id,error_code) VALUES (?,?,?,?,?) ON CONFLICT(draft_id,step) DO UPDATE SET status=EXCLUDED.status,remote_id=EXCLUDED.remote_id,error_code=EXCLUDED.error_code,updated_at=now()",
        id,
        step,
        status,
        remote,
        error);
  }

  public void state(UUID id, String state, String remote, String error) {
    db.update(
        "UPDATE drafts SET state=?,remote_id=COALESCE(?,remote_id),error_code=? WHERE id=?",
        state,
        remote,
        error,
        id);
  }

  public int deleteAccount(String account) {
    return db.update("DELETE FROM drafts WHERE account=?", account);
  }

  /** Fresh local human authorization; no model-facing route. Only a finished partial attempt. */
  public void claimRepair(UUID id, String account, String phrase) {
    tx.executeWithoutResult(
        s -> {
          db.queryForList("SELECT id FROM drafts WHERE id=? FOR UPDATE", id);
          Draft d = get(id, account);
          if (!d.state().equals("PARTIAL") || d.remoteId() == null)
            throw new CuratorException(
                "WRITE_REVIEW_REQUIRED",
                "Only a partial attempt with a known playlist can be repaired. Never resume an active/ambiguous create.");
          if (!("REPAIR " + d.fingerprint()).equals(phrase))
            throw new CuratorException(
                "APPROVAL_MISMATCH", "Review and type the exact repair fingerprint.");
          db.update("UPDATE drafts SET state='REPAIRING' WHERE id=?", id);
          journal(id, "998-repair", "HUMAN_AUTHORIZED", null, null);
        });
  }

  public void resolve(UUID id, String account, String phrase) {
    tx.executeWithoutResult(
        s -> {
          db.queryForList("SELECT id FROM drafts WHERE id=? FOR UPDATE", id);
          Draft d = get(id, account);
          if (!Set.of("PARTIAL", "NEEDS_MANUAL_REVIEW", "CREATING", "REPAIRING").contains(d.state())
              || !("RESOLVE " + d.fingerprint()).equals(phrase))
            throw new CuratorException(
                "APPROVAL_MISMATCH",
                "Stop all writers, inspect the remote account and type the exact resolution fingerprint.");
          db.update("UPDATE drafts SET state='RESOLVED' WHERE id=?", id);
          journal(id, "999-resolution", "MANUALLY_RESOLVED", d.remoteId(), null);
        });
  }

  public int cleanupExpired() {
    return tx.execute(
        s -> {
          int removed =
              db.update(
                  "DELETE FROM drafts WHERE (expires_at<? AND state IN ('PROPOSED','APPROVED')) OR created_at<?",
                  Timestamp.from(clock.instant()),
                  Timestamp.from(clock.instant().minus(Duration.ofDays(7))));
          db.update(
              "DELETE FROM quota_reservations WHERE quota_date<?",
              java.sql.Date.valueOf(
                  org.example.videocurator.quota.QuotaService.quotaDate(clock).minusDays(7)));
          db.update(
              "DELETE FROM quota_buckets WHERE quota_date<?",
              java.sql.Date.valueOf(
                  org.example.videocurator.quota.QuotaService.quotaDate(clock).minusDays(7)));
          return removed;
        });
  }
}
