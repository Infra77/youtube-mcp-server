package org.example.videocurator.domain;

import java.net.URI;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.*;

public final class Input {
  private Input() {}

  public static void require(boolean condition, String message) {
    if (!condition) throw new CuratorException("INVALID_INPUT", message);
  }

  public static int limit(int value) {
    require(value >= 1 && value <= 20, "limit must be 1–20");
    return value;
  }

  public static String video(String input) {
    String raw = bounded(input);
    if (raw.matches("[A-Za-z0-9_-]{11}")) return raw;
    URI u = youtubeUri(raw);
    String path = u.getPath();
    String id = null;
    if (Set.of("youtu.be", "www.youtu.be").contains(u.getHost().toLowerCase(Locale.ROOT)))
      id = path.substring(1);
    else if (path.equals("/watch")) {
      var values = new ArrayList<String>();
      if (u.getRawQuery() != null)
        for (String part : u.getRawQuery().split("&")) {
          String[] kv = part.split("=", 2);
          if (decode(kv[0]).equals("v")) values.add(kv.length == 2 ? decode(kv[1]) : "");
        }
      require(values.size() == 1, "Exactly one video ID query parameter is required.");
      id = values.getFirst();
    } else if (path.matches("/(shorts|embed)/[A-Za-z0-9_-]{11}"))
      id = path.substring(path.lastIndexOf('/') + 1);
    require(id != null && id.matches("[A-Za-z0-9_-]{11}"), "Invalid video URL or ID.");
    return id;
  }

  public static String channel(String input) {
    String s = bounded(input);
    if (s.matches("UC[A-Za-z0-9_-]{22}") || s.matches("@[\\p{L}\\p{N}_.-]{3,30}")) return s;
    URI u = youtubeUri(s);
    String p = u.getPath();
    require(
        !u.getHost().toLowerCase(Locale.ROOT).contains("youtu.be"), "Unsupported channel host.");
    if (p.matches("/channel/UC[A-Za-z0-9_-]{22}")) return p.substring(9);
    if (p.matches("/@[\\p{L}\\p{N}_.-]{3,30}")) return p.substring(1);
    throw new CuratorException(
        "UNSUPPORTED_CHANNEL_URL",
        "Use a channel ID, /channel/ URL or @handle; custom aliases are unsupported.");
  }

  private static String bounded(String s) {
    require(s != null && !s.isBlank() && s.length() <= 2048, "Input is missing or too long.");
    return s.trim();
  }

  private static URI youtubeUri(String raw) {
    try {
      URI u = URI.create(raw);
      require(
          u.getScheme() != null
              && Set.of("https", "http").contains(u.getScheme())
              && u.getHost() != null
              && u.getUserInfo() == null
              && u.getPort() == -1
              && u.getFragment() == null,
          "Invalid YouTube URL.");
      require(
          Set.of("youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be")
              .contains(u.getHost().toLowerCase(Locale.ROOT)),
          "Unapproved video host.");
      require(
          u.getRawPath() != null && !u.getRawPath().contains("%"), "Encoded path is unsupported.");
      return u;
    } catch (IllegalArgumentException e) {
      throw new CuratorException("INVALID_INPUT", "Malformed URL.");
    }
  }

  private static String decode(String s) {
    try {
      return URLDecoder.decode(s, StandardCharsets.UTF_8);
    } catch (IllegalArgumentException e) {
      throw new CuratorException("INVALID_INPUT", "Malformed query encoding.");
    }
  }

  public static long duration(String iso) {
    try {
      Duration d = Duration.parse(iso);
      require(d.getSeconds() > 0 && d.getNano() == 0, "Duration must be positive whole seconds.");
      return d.getSeconds();
    } catch (Exception e) {
      throw new CuratorException(
          "INVALID_DURATION", "Unknown, zero or invalid fixed video duration.");
    }
  }
}
