package org.example.videocurator.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Clock;
import org.example.videocurator.application.CuratorService;
import org.example.videocurator.oauth.WindowsTokenVault;
import org.example.videocurator.persistence.DraftStore;
import org.example.videocurator.provider.*;
import org.example.videocurator.quota.QuotaService;
import org.springframework.context.annotation.*;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.support.TransactionTemplate;

@Configuration
public class AppConfig {
  @Bean
  ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule())
        .disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }

  @Bean
  Clock clock() {
    return Clock.systemUTC();
  }

  @Bean
  TransactionTemplate transactionTemplate(PlatformTransactionManager manager) {
    return new TransactionTemplate(manager);
  }

  @Bean
  WindowsTokenVault vault(ObjectMapper json, Environment e) {
    return new WindowsTokenVault(json, e.getProperty("curator.profile", "local-user"));
  }

  @Bean
  YouTubeProvider provider(ObjectMapper json, Environment e, WindowsTokenVault vault) {
    String mode = e.getProperty("curator.mode", "fixture");
    return switch (mode) {
      case "fixture" -> new FixtureYouTubeProvider(json);
      case "live" -> new OfficialYouTubeProvider(json, vault);
      default -> throw new IllegalArgumentException("CURATOR_MODE must be fixture or live");
    };
  }

  @Bean
  QuotaService quota(JdbcTemplate db, TransactionTemplate tx, Clock clock, Environment e) {
    return new QuotaService(
        db,
        tx,
        clock,
        e.getProperty("curator.general-limit", Long.class, 10000L),
        e.getProperty("curator.search-limit", Long.class, 100L));
  }

  @Bean
  DraftStore drafts(JdbcTemplate db, TransactionTemplate tx, ObjectMapper json, Clock clock) {
    return new DraftStore(db, tx, json, clock);
  }

  @Bean
  CuratorService curator(
      YouTubeProvider provider, QuotaService quota, DraftStore drafts, Clock clock) {
    return new CuratorService(provider, quota, drafts, clock);
  }
}
