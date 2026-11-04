package org.example.videocurator;

import static org.junit.jupiter.api.Assertions.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.*;
import org.example.videocurator.provider.MetadataCache;
import org.junit.jupiter.api.Test;

class MetadataCacheTest {
  @Test
  void expiryBoundsAccountIsolationAndDefensiveCopies() {
    class MutableClock extends Clock {
      Instant now = Instant.EPOCH;

      public ZoneId getZone() {
        return ZoneOffset.UTC;
      }

      public Clock withZone(ZoneId z) {
        return this;
      }

      public Instant instant() {
        return now;
      }
    }
    var clock = new MutableClock();
    var cache = new MetadataCache(clock, Duration.ofMinutes(5), 2);
    var value = new ObjectMapper().createObjectNode().put("title", "original");
    cache.put("account-A:video", value);
    value.put("title", "changed");
    assertEquals("original", cache.get("account-A:video").path("title").asText());
    assertNull(cache.get("account-B:video"));
    cache.put("b", value);
    cache.put("c", value);
    assertNull(cache.get("account-A:video"));
    clock.now = clock.now.plusSeconds(301);
    assertNull(cache.get("b"));
    assertNull(cache.get("c"));
  }
}
