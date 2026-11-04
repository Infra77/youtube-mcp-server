# Test plan
TQ-1: JUnit parsing, TF-IDF, missingness, deterministic planner, text grammar and analytics.
TQ-2: WireMock official adapter HTTP/error mapping; real PostgreSQL Flyway/locks via Testcontainers.
TQ-3: maintained Java MCP client starts packaged JAR; initialize/list/resources/read/all FR calls.
TQ-4: invalid IDs, unavailable videos, missing tags, quota, channel-required, expired auth, rate limit.
TQ-5: fixture provider and WireMock only; live mode never selected in ordinary checks.
TQ-6: insufficient either bucket => no provider call; concurrent reservations and Pacific date tests.
TQ-7: five skill positive/negative evaluations with artifacts and honest manual/automated labels.
TQ-8: docs/defects.md links each significant defect to a regression test.
Security: approval absence/mismatch/expiry/account mismatch/replay, injected metadata, safe errors.
Full local command: mvnw.cmd clean verify; documentation validator and secret checks separately.
No Docker skipping in acceptance; unavailable infrastructure is a failed prerequisite.
Live run is separate, explicitly enabled, and bounded; not yet possible without Google Cloud setup.
