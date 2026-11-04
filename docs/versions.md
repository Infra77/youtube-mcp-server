# Pinned local build

Verified from resolved Maven artifacts and official versioned documentation, 2026-10-31:

| Component | Version |
|---|---|
| Java | Temurin 21.0.13+9, archive SHA-256 checked against release metadata |
| Maven wrapper | 3.9.11, wrapper scripts 3.3.4 |
| Spring Boot | 3.5.7 |
| Spring AI | 1.1.8 |
| MCP Java SDK | 0.18.3 (BOM-managed) |
| PostgreSQL image | postgres:16-alpine (observed server 16.15) |
| Flyway | 11.7.2 (Boot-managed) |
| PostgreSQL JDBC | 42.7.8 (Boot-managed) |
| Testcontainers | 1.21.3 |
| WireMock standalone | 3.13.1 |
| JNA | 5.18.1 |

This is a compatible tested line, not a claim of latest releases or a completed vulnerability audit.
Spring AI 1.1 corresponds to Boot 3.5; the versioned [server documentation](https://docs.spring.io/spring-ai/reference/1.1/api/mcp/mcp-server-boot-starter-docs.html)
defines the chosen stdio starter. Upgrade only with dependency review and protocol/DB regression tests.
Container tag patch drift remains a reproducibility limitation; record pulled image digest in release evidence.

## Completion revision

Current pom.xml is authoritative: Spring Boot 3.5.16, Spring AI 1.1.8, Jackson BOM 2.21.7,
Logback 1.5.34, Log4j 2.25.5 and PostgreSQL JDBC 42.7.12. Java 21/Maven wrapper remain.
MCP SDK stays on the tested Spring AI managed line; the HTTP-only DNS-rebinding advisory has a
recorded stdio-only applicability decision requiring independent review. See security-dependency-review.md.
