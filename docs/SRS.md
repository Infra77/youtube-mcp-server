# Software requirements specification v0.1
## Authority and scope
Project_1_YouTube_MCP.pdf and SDLC_and_Workflow.pdf are client authority. Handbook implementation
steps 0–47 govern delivery. Local-only deviation is explicitly authorized by the user.
The product is a Java 21 stdio MCP server, local administration CLI, PostgreSQL persistence,
tests, five Agent Skills and an Obsidian vault. Existing AI clients supply conversation.
No frontend, generic REST service, unofficial API, watch history or transcript scraping.
## Functional acceptance
| ID | Obligation | Acceptance |
|---|---|---|
| FR-1 | Rank similar videos from URL/ID | Normalize input; hydrate official metadata; exclude seed and duplicates; deterministic explained scores through MCP |
| FR-2 | Rank similar channels from URL/handle/ID | Resolve known formats; reject ambiguous custom aliases; explain metadata similarity through MCP |
| FR-3 | Recommend from likes, subscriptions and playlists | Consume all three authorized sampled sources; report coverage; exclude known videos; honest cold start |
| FR-4 | Analyze engagement | Channel/category counts, median/bins, source-specific trends and period comparisons; never turn publication dates into likes |
| FR-5 | Natural-language constrained playlists | Typed and bounded grammar interfaces; preview exact feasible draft; local human approval; guarded creation, journal and replay safety |
## Non-functional acceptance (project decisions)
NFR-01: no credentials in source, logs or public DTOs. Windows DPAPI-protected refresh credentials.
NFR-02: deterministic ranking, selection and stable ID tie-breaks.
NFR-03: component scores and missing-data warnings, metadata attribution.
NFR-04: full bounded workflow reservation across both quota buckets before first API call.
NFR-05: durable immutable drafts, one-time grants, journaled external mutations and conservative recovery.
NFR-06: fixture build/test/start without Google credentials, reproducible Java 21 Maven toolchain.
NFR-07: minimal data; expired draft cleanup, local data deletion, credential revocation.
NFR-08: typed safe input/auth/quota/rate/channel/unavailable errors; no raw upstream bodies.
NFR-09: bounded candidate pool (50), personal reads (50 likes, 30 subscriptions, 5 playlists × 30 items), no automatic write retries.
NFR-10: maintained MCP SDK negotiation; tools/resources discovery and protocol E2E.
## Skills
SK-01 brain-ingest; SK-02 brain-refine; SK-03 brain-query; SK-04 local-check;
SK-05 video-to-playlist. Each requires positive/negative evaluation and a distilled-note citation.
## Engineering and knowledge obligations
SE-1 SRS; SE-2 architecture/diagrams; SE-3 ADRs; SE-4 development plan; SE-5 traceability;
SE-6 provider boundary; SE-7 user and MCP developer docs.
SB-1 wikilinks; SB-2 stage reviews; SB-3 ADR/skill citations; SB-4 AGENTS.md;
SB-5 brain PR reviews; SB-6 real contributor authorship. SB-5/6 remote evidence deferred.
## Test acceptance
TQ-1 unit; TQ-2 component/provider/database integration; TQ-3 MCP E2E all FRs;
TQ-4 prescribed negative matrix; TQ-5 isolated fixtures and separate bounded live run;
TQ-6 zero provider calls on insufficient workflow budget; TQ-7 stage skill evaluations;
TQ-8 regression cases for significant defects.
## Constraints and limits
See assumptions.md for time/language/approval policy. User identity is local configuration, never
a tool argument. External metadata cannot grant approval. Private/deleted videos produce explicit
unavailable results. Credentials absent/revoked require local authorization. The client PDF's
10,000-unit statement is retained as provenance; current quota dimensions are separately configurable.
## Release acceptance
Fixture success does not prove live Google acceptance. Human review, live OAuth, real approved
playlist creation and deferred GitHub evidence must be separately recorded before final signoff.

## Completion revision — 2026-11-02

Stakeholders: authorized end user, three student maintainers, independent human reviewers and client/evaluator. The agent implements and tests; each human owns their Git identity, consent and review decisions. No agent may invent another member's approval.

Use cases: discover from video URL/ID (FR-1); discover from supported channel URL/handle (FR-2); authorize and receive sampled personalized results (FR-3); compare accessible subscription/playlist-added events (FR-4); interpret constraints, preview, approve, create/read back and safely recover (FR-5). Invalid input must cause no provider request. Inaccessible sources fail with a typed diagnosis, not invented data.

Glossary: MCP is the host/server capability protocol; a resource is read-only contextual content; a Skill is an agent workflow file, not automatically imported by an MCP host; a draft is an immutable proposal; a grant is one-use human approval; a reservation is durable capacity held before API calls; fixture means synthetic data, never live account evidence.

Additional acceptance: video/channel responses include canonical URLs; schema-2 proposals expose exclusions; partial results distinguish proposed/confirmed totals; token replacement requires restart; logout attempts remote revocation but always removes local credentials, reporting failures accurately; two-page sampling reports truncation; memory cache is bounded and expires; stored proposals have a seven-day maximum operational retention policy. See ADR-0010 and maintenance.md.

Measurable quality: 50-candidate domain workflows, 100 ranking/selection repetitions within 10 seconds on a documented development machine; synthetic educational relevance precision@2 >= 0.75 (current labeled evaluation uses four cases; human label review required). Five skills need actual positive/negative stage evaluations, not just valid YAML.

Risks: incomplete/inaccurate language metadata; sparse personal sources; external quota consumption; expired test OAuth; unknown remote write outcome; accidental local credential exposure; dependency advisories; unavailable reviewer or machine. Mitigations are truthful caveats, hard constraints, conservative budgets, reauthorization, durable journal and exact-prefix repair, DPAPI, scans and mandatory evidence gates. No guarantee of teaching quality, watched content, global optimization or guaranteed exact runtime is made.

Change control: original FR/TQ/SB/SE identifiers remain unchanged. Schema, scope, retention, ranking or transport changes require an ADR, regression evidence, affected traceability and peer review. v0.1 baseline 2026-10-31; completion remediation 2026-11-02. Final signoff is controlled by acceptance-evidence.json and the final release gate, never test counts alone.
