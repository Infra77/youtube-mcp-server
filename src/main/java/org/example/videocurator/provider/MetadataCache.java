package org.example.videocurator.provider;

import com.fasterxml.jackson.databind.JsonNode;
import java.time.*;
import java.util.*;

/** Per-process, account-keyed metadata only. No tokens or personal collections. */
public final class MetadataCache {
  private record Entry(Instant expires, JsonNode data) {}

  private final Clock clock;
  private final Duration ttl;
  private final int maximum;
  private final LinkedHashMap<String, Entry> entries = new LinkedHashMap<>();

  public MetadataCache(Clock clock, Duration ttl, int maximum) {
    if (ttl.isNegative() || ttl.isZero() || maximum < 1) throw new IllegalArgumentException();
    this.clock = clock;
    this.ttl = ttl;
    this.maximum = maximum;
  }

  public synchronized JsonNode get(String key) {
    entries.values().removeIf(e -> !e.expires().isAfter(clock.instant()));
    var e = entries.get(key);
    return e == null ? null : e.data().deepCopy();
  }

  public synchronized void put(String key, JsonNode data) {
    get(key);
    entries.remove(key);
    while (entries.size() >= maximum) entries.remove(entries.keySet().iterator().next());
    entries.put(key, new Entry(clock.instant().plus(ttl), data.deepCopy()));
  }
}
