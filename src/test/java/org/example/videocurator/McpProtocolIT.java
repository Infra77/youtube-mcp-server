package org.example.videocurator;

import static org.junit.jupiter.api.Assertions.*;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import io.modelcontextprotocol.client.*;
import io.modelcontextprotocol.client.transport.*;
import io.modelcontextprotocol.json.jackson.JacksonMcpJsonMapper;
import io.modelcontextprotocol.spec.McpSchema.*;
import java.nio.file.*;
import java.time.*;
import java.util.*;
import org.example.videocurator.persistence.DraftStore;
import org.junit.jupiter.api.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.*;
import org.springframework.transaction.support.TransactionTemplate;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.*;

@Testcontainers
class McpProtocolIT {
  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

  final ObjectMapper json = new ObjectMapper().registerModule(new JavaTimeModule());
  McpSyncClient client;
  final List<Object> evidence = new ArrayList<>();

  @BeforeEach
  void start() {
    var env = new HashMap<String, String>(System.getenv());
    env.put("DB_JDBC_URL", postgres.getJdbcUrl());
    env.put("DB_USERNAME", postgres.getUsername());
    env.put("DB_PASSWORD", postgres.getPassword());
    env.put("CURATOR_MODE", "fixture");
    var args = new ArrayList<String>();
    args.add("-Djdk.net.unixdomain.tmpdir=" + Path.of("target").toAbsolutePath());
    args.addAll(List.of("-jar", Path.of("target/curator.jar").toAbsolutePath().toString(), "mcp"));
    var params =
        ServerParameters.builder(
                Path.of(
                        System.getProperty("java.home"),
                        "bin",
                        System.getProperty("os.name").startsWith("Windows") ? "java.exe" : "java")
                    .toString())
            .args(args)
            .env(env)
            .build();
    var transport = new StdioClientTransport(params, new JacksonMcpJsonMapper(json));
    transport.setStdErrorHandler(
        line -> {
          System.err.println(line.replace(postgres.getPassword(), "<redacted>"));
        });
    client = McpClient.sync(transport).requestTimeout(Duration.ofSeconds(40)).build();
    assertNotNull(client.initialize());
  }

  @AfterEach
  void close() throws Exception {
    if (client != null) client.closeGracefully();
    Files.createDirectories(Path.of("target/evidence"));
    json.writerWithDefaultPrettyPrinter()
        .writeValue(Path.of("target/evidence/mcp-protocol.json").toFile(), evidence);
  }

  private JsonNode call(String tool, Map<String, Object> args, boolean error) throws Exception {
    var response = client.callTool(new CallToolRequest(tool, args));
    assertEquals(error, Boolean.TRUE.equals(response.isError()), tool + ": " + response);
    var content = (TextContent) response.content().getFirst();
    JsonNode envelope = json.readTree(content.text());
    evidence.add(Map.of("tool", tool, "arguments", args, "response", envelope));
    return envelope;
  }

  @Test
  void allFunctionalRequirementsThroughRealMcpClient() throws Exception {
    var tools = client.listTools().tools();
    assertEquals(10, tools.size());
    evidence.add(Map.of("tools", tools));
    var resources = client.listResources().resources();
    assertEquals(5, resources.size());
    assertFalse(
        client
            .readResource(new ReadResourceRequest("youtube-intelligence://limitations"))
            .contents()
            .isEmpty());
    assertEquals(1, client.listPrompts().prompts().size());
    call("get_quota_status", Map.of(), false);
    assertEquals(
        "video_metadata",
        call("get_video_overview", Map.of("videoInput", "FIXTURE0001"), false)
            .path("data")
            .path("source")
            .asText());
    assertFalse(
        call("find_similar_videos", Map.of("videoInput", "FIXTURE0001", "limit", 4), false)
            .path("data")
            .path("candidates")
            .isEmpty());
    assertFalse(
        call("find_similar_channels", Map.of("channelInput", "@ExampleMath", "limit", 3), false)
            .path("data")
            .path("channels")
            .isEmpty());
    assertFalse(
        call("recommend_for_me", Map.of("limit", 3), false)
            .path("data")
            .path("recommendations")
            .isEmpty());
    assertTrue(
        call(
                "analyze_my_engagement",
                Map.of(
                    "startA",
                    "2026-01-01",
                    "endA",
                    "2026-02-01",
                    "startB",
                    "2026-02-01",
                    "endB",
                    "2026-03-01"),
                false)
            .path("data")
            .has("periodComparison"));
    var proposal =
        call(
                "plan_playlist",
                Map.of(
                    "topic",
                    "Fourier transforms",
                    "targetSeconds",
                    1800,
                    "maxVideoSeconds",
                    1200,
                    "language",
                    "en",
                    "maxVideos",
                    3),
                false)
            .path("data");
    String id = proposal.path("id").asText();
    assertEquals(
        "APPROVAL_REQUIRED",
        call("commit_playlist", Map.of("draftId", id), true).path("code").asText());
    call("get_playlist_draft", Map.of("draftId", id), false);
    // Test-only local administrator simulation against the real durable grant path. No live
    // account.
    var ds =
        new DriverManagerDataSource(
            postgres.getJdbcUrl(), postgres.getUsername(), postgres.getPassword());
    var db = new JdbcTemplate(ds);
    var store =
        new DraftStore(
            db,
            new TransactionTemplate(new DataSourceTransactionManager(ds)),
            json,
            Clock.systemUTC());
    store.approve(
        UUID.fromString(id), "fixture-account", "APPROVE " + proposal.path("fingerprint").asText());
    var result = call("commit_playlist", Map.of("draftId", id), false).path("data");
    assertEquals("CREATED", result.path("state").asText());
    assertEquals("", result.path("playlistUrl").asText());
    assertEquals(
        result.path("playlistId"),
        call("commit_playlist", Map.of("draftId", id), false).path("data").path("playlistId"));
    call(
        "plan_playlist_from_text",
        Map.of(
            "requestText",
            "Make a 2-hour English playlist on Fourier transforms, maximum 20 minutes per video"),
        false);
    assertEquals(
        "NEEDS_CLARIFICATION",
        call("plan_playlist_from_text", Map.of("requestText", "Make a playlist"), true)
            .path("code")
            .asText());
    assertEquals(
        "INVALID_INPUT",
        call("find_similar_videos", Map.of("videoInput", "bad", "limit", 5), true)
            .path("code")
            .asText());
    assertEquals(
        "VIDEO_UNAVAILABLE",
        call("get_video_overview", Map.of("videoInput", "DELETED0000"), true)
            .path("code")
            .asText());
  }
}
