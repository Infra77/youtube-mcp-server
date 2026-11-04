package org.example.videocurator.mcp;

import static org.example.videocurator.domain.Models.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.modelcontextprotocol.spec.McpSchema.*;
import java.time.Instant;
import java.util.*;
import java.util.function.Supplier;
import org.example.videocurator.application.CuratorService;
import org.example.videocurator.domain.*;
import org.springaicommunity.mcp.annotation.*;
import org.springframework.stereotype.Component;

@Component
public class CuratorTools {
  private final CuratorService service;
  private final ObjectMapper json;

  public CuratorTools(CuratorService service, ObjectMapper json) {
    this.service = service;
    this.json = json;
  }

  private CallToolResult call(Supplier<Object> fn) {
    Map<String, Object> envelope = new LinkedHashMap<>();
    envelope.put("schemaVersion", 1);
    envelope.put("requestId", UUID.randomUUID().toString());
    envelope.put("asOf", Instant.now().toString());
    envelope.put("fixture", service.fixture());
    boolean error = false;
    try {
      envelope.put("status", "ok");
      envelope.put("data", fn.get());
    } catch (CuratorException e) {
      error = true;
      envelope.put("status", "error");
      envelope.put("code", e.code());
      envelope.put("message", e.getMessage());
      envelope.put("retryable", false);
    } catch (Exception e) {
      error = true;
      envelope.put("status", "error");
      envelope.put("code", "INTERNAL_ERROR");
      envelope.put(
          "message",
          "Operation could not complete safely. Inspect local configuration and durable write state; no automatic retry.");
    }
    try {
      return new CallToolResult(
          List.of(new TextContent(json.writeValueAsString(envelope))), error, envelope, Map.of());
    } catch (Exception e) {
      return new CallToolResult("Result serialization failed safely.", true);
    }
  }

  @McpTool(
      name = "get_video_overview",
      description =
          "Read official video metadata. Overview is metadata-derived, never a transcript summary.")
  public CallToolResult overview(
      @McpToolParam(required = true, description = "YouTube URL or 11-character video ID")
          String videoInput) {
    return call(() -> service.overview(videoInput));
  }

  @McpTool(
      name = "find_similar_videos",
      description =
          "Rank locally computed metadata-similar videos, with component scores; no YouTube writes.")
  public CallToolResult similar(
      @McpToolParam(required = true) String videoInput,
      @McpToolParam(required = true, description = "1 through 20") int limit) {
    return call(() -> service.similar(videoInput, limit));
  }

  @McpTool(
      name = "find_similar_channels",
      description = "Resolve channel ID, URL or @handle and rank metadata-similar channels.")
  public CallToolResult channels(
      @McpToolParam(required = true) String channelInput,
      @McpToolParam(required = true) int limit) {
    return call(() -> service.channels(channelInput, limit));
  }

  @McpTool(
      name = "recommend_for_me",
      description =
          "Recommend using the selected account's sampled likes, subscriptions and playlists, with coverage.")
  public CallToolResult recommend(@McpToolParam(required = true) int limit) {
    return call(() -> service.recommend(limit));
  }

  @McpTool(
      name = "analyze_my_engagement",
      description =
          "Analyze sampled authorized collections. Optional periods use YYYY-MM-DD; publication dates are never like dates.")
  public CallToolResult analyze(
      @McpToolParam(required = false) String startA,
      @McpToolParam(required = false) String endA,
      @McpToolParam(required = false) String startB,
      @McpToolParam(required = false) String endB) {
    return call(() -> service.analyze(startA, endA, startB, endB));
  }

  @McpTool(
      name = "plan_playlist",
      description =
          "Persist an immutable private playlist proposal. Does NOT create anything on YouTube. Language means declared audio-language metadata.")
  public CallToolResult plan(
      @McpToolParam(required = true) String topic,
      @McpToolParam(required = true) long targetSeconds,
      @McpToolParam(required = true) long maxVideoSeconds,
      @McpToolParam(required = true) String language,
      @McpToolParam(required = true) int maxVideos) {
    return call(
        () ->
            service.plan(
                new Constraints(topic, targetSeconds, maxVideoSeconds, language, maxVideos),
                "typed MCP constraints"));
  }

  @McpTool(
      name = "plan_playlist_from_text",
      description =
          "Parse bounded requests such as Make a 2-hour English playlist on Fourier transforms, maximum 20 minutes per video. Ambiguity returns NEEDS_CLARIFICATION.")
  public CallToolResult planText(@McpToolParam(required = true) String requestText) {
    return call(() -> service.plan(PlaylistSelector.parse(requestText), requestText));
  }

  @McpTool(
      name = "get_playlist_draft",
      description =
          "Read exact persisted proposal, fingerprint, expiry and write status for selected account.")
  public CallToolResult draft(@McpToolParam(required = true) String draftId) {
    return call(() -> service.draft(draftId));
  }

  @McpTool(
      name = "commit_playlist",
      description =
          "Create ONLY an exact draft already approved interactively by the human in the local CLI. No confirmed/account/token parameter is accepted.")
  public CallToolResult commit(@McpToolParam(required = true) String draftId) {
    return call(() -> service.commit(draftId));
  }

  @McpTool(
      name = "get_quota_status",
      description = "Read local project quota ledger and Pacific reset date; does not call Google.")
  public CallToolResult quota() {
    return call(service::quota);
  }
}
