package org.example.videocurator.quota;

/** Reviewed defaults, overridable only by operator JVM configuration, never MCP input. */
public final class CostCatalog {
  private CostCatalog() {}

  public static long read() {
    return cost("curator.cost.read", 1);
  }

  public static long write() {
    return cost("curator.cost.write", 50);
  }

  public static long search() {
    return cost("curator.cost.search", 1);
  }

  private static long cost(String key, long fallback) {
    long value = Long.getLong(key, fallback);
    if (value < 1 || value > 10000) throw new IllegalStateException("Invalid operator quota cost");
    return value;
  }
}
