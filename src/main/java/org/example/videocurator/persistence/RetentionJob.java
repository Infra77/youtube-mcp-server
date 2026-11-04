package org.example.videocurator.persistence;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Runs on startup and hourly while the process is active; never mutates YouTube. */
@Component
public final class RetentionJob {
  private final DraftStore store;

  public RetentionJob(DraftStore store) {
    this.store = store;
  }

  @Scheduled(initialDelay = 0, fixedDelay = 3600000)
  public void clean() {
    store.cleanupExpired();
  }
}
