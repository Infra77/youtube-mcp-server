from bootstrap_docs import write, ROOT, notes
from record_step import record

details = {
0: ('Scope and assumptions','Read both client PDFs and the handbook. Separated required FR/TQ/SB/SE obligations from handbook architecture choices. Chose one account per local process, strict metadata-language filtering, integer-second upper-bound totals, private playlists, 30-minute drafts and 10-minute approvals. Recorded that Google Cloud is absent and GitHub is deferred.','docs/assumptions.md, docs/SRS.md'),
1: ('Windows workstation','Inspected the actual machine: Java 25 and Docker Desktop were installed; the Docker engine was stopped. Started Docker with user approval. Downloaded Temurin JDK 21.0.13+9 from its official release metadata and compared SHA-256 before extraction under .tools. Located Maven bundled with IntelliJ to generate the project wrapper. Avoided changing global Java settings.',' .tools/jdk-release.json, .tools/jdk-21.0.13+9; docs/setup-windows.md will document the final launcher'),
2: ('Shared GitHub repository','Deferred by explicit user instruction. No repository, account, collaborator, remote branch protection or PR was created. This is an authorized scope deferral and must not be marked as completed client SDLC evidence.','docs/handbook-amendments.md'),
3: ('Canonical project and PARA vault','Created one project directory containing docs, scripts, infra, tests, fixtures and brain. The brain has inbox/projects/areas/resources/archive, an index and operation log. External detailed step notes live in SE/notes, separately from the internal knowledge vault. Added ignores for downloaded tooling, build output and credentials.','brain/index.md, brain/log.md, .gitignore, .gitattributes'),
4: ('AGENTS project contract','Wrote the contributor contract before application code: Java21/stdio-only, official API only, stdout isolation, exact-draft approval, no live ordinary tests, source-linked ADRs, truthful evidence and no secrets. The user-authorized GitHub deferral is explicit so future work does not fabricate PRs.','AGENTS.md; brain/inbox/Codex Project Boundaries.md'),
5: ('Local work and review pattern','Translated the handbook GitHub workflow into numbered local work IDs, factual evidence and reviewable files. Remote review, second contributor authorship and merge histories are pending. AI-generated artifacts remain subject to human review; no self-approval is claimed.','docs/development-plan.md; AGENTS.md'),
6: ('Research and brain-ingest','Read the provided sources and official Spring AI, Google OAuth, videos.list, playlistItems.insert and quota documentation. Applied the brain-ingest workflow: created fourteen research notes with source identity, review date, author, requirement IDs, distilled findings, implementation consequences, open evidence and related links. Local document sources use client:/handbook: provenance rather than fabricated web URLs.','brain/inbox/*.md; brain/log.md; .agents/skills/brain-ingest/SKILL.md'),
7: ('SRS baseline','Preserved FR-1 through FR-5, specified measurable project NFRs, all five SKs, the SE/SB obligations and TQ-1 through TQ-8. Defined unavailable-data behavior, live acceptance limitations and scope exclusions. Distinguished source mandates from chosen approval timeouts and bounded sampling.','docs/SRS.md'),
8: ('Backlog and traceability design','Mapped handbook steps 0–47 to local work IDs L-00 through L-47. Kept the four client stages unchanged. Issue/PR evidence will be DEFERRED, not made-up numbers; executable tests are attached to traceability as they are implemented.','docs/development-plan.md'),
9: ('Local quality-gate skeleton','Prepared local documentation validation and the ordered build/test plan. Hosted GitHub Actions are deferred. The local equivalent must compile, test, validate notes and skills, scan for credential mistakes, and exercise actual MCP; skeleton existence is not a green build.','scripts/validate_docs.py; docs/test-plan.md'),
}
for n,(title,action,files) in details.items():
    record(n,title,'Deferred' if n in (2,5) else 'Local artifact complete; review pending',action,files,
           'Inspected written artifacts. Java checksum matched and Docker returned both client and server versions. Documentation validator results are recorded separately; application tests are not yet claimed.',
           'Source extraction, explicit scope, workstation foundation, PARA research, skills baseline and SRS are present. No YouTube API request or playlist mutation has been performed.',
           'GitHub and human review remain deferred; live Google requires user setup. This stage cannot claim the original remote review gate passed.')

for title,*_ in notes:
    source=ROOT/'brain/inbox'/f'{title}.md'
    target=ROOT/'brain/resources'/f'{title}.md'
    if source.exists(): source.replace(target)
with (ROOT/'brain/log.md').open('a',encoding='utf-8') as f:
    f.write('\n2026-10-31: brain-refine moved fourteen distilled inbox notes into resources. Basenames preserved, so wikilinks remain stable; no source content discarded. GitHub review deferred.\n')
write('docs/architecture.md','''# Architecture
Existing AI host → SDK MCP stdio adapter → application services → pure domain algorithms.
Services depend on YouTubeProvider, quota ledger, draft store and TokenVault boundaries.
OfficialYouTubeProvider uses fixed Google API origins. FixtureYouTubeProvider never contacts Google.
PostgreSQL stores drafts, grants, write journal and quota ledger. Flyway owns versioned schema.
The separate local CLI performs Google OAuth and interactive proposal approval; it is not a tool.
Windows DPAPI protects credential bytes; token material never enters tool results.
MCP runs synchronously with bounded request sizes. SQL state transitions are short transactions;
remote API operations execute outside transactions. Persist write intent before sending a mutation.
An interrupted/ambiguous write is stopped for reconciliation/manual review, not blindly retried.
Production and fixture accounts are distinct. Fixture mode is explicit and reports synthetic data.
See diagrams and ADRs. No public listener exists except temporary OAuth loopback during consent.
''')
adrs=[
('Java 21 and stdio','MCP Stdio Semantics','Use a single Maven module, Spring Boot 3.5 and compatible Spring AI 1.1. Pin published patch versions. Choose stdio over hosted HTTP to retain the local account trust boundary. Cost: users need a local Java process.'),
('Official provider boundary','YouTube Endpoint Matrix','Use an allowlisted official HTTP adapter behind YouTubeProvider and a separate fixture implementation. Reject scraping and arbitrary endpoint tools. Cost: metadata cannot establish spoken-content summaries.'),
('PostgreSQL durability','Postgres Crash Recovery','Use PostgreSQL 16 with JDBC/Flyway for proposals, approvals, journals and quotas. Database row locks protect concurrent claims. In-memory/H2 state is not sufficient evidence of production crash/locking semantics.'),
('Explainable ranking','TF-IDF and Cosine Similarity','Use smoothed corpus TF-IDF, cosine and weighted metadata features (0.55 text, 0.20 tags, 0.10 category, 0.10 duration, 0.05 language). Missing categorical evidence gives zero, stable ties use IDs. No model or vector database.'),
('Local PKCE and DPAPI','Google OAuth Desktop PKCE','Separate browser authorization CLI from MCP. Use state, S256 PKCE, ephemeral loopback, bounded callback lifetime and Windows DPAPI CurrentUser credential protection. Unsupported OS vaults fail closed. Request youtube.force-ssl for required read/write operations, not partner scope.'),
('Exact proposal approval','Playlist Approval Invariants','Approval requires a real interactive console and review of complete immutable proposal. Bind digest, account and expiry. Commit accepts only draft ID. Atomic state claim prevents duplicate commits; remote ambiguous outcomes require review.'),
('Two-bucket bounded preflight','Quota Buckets and Reservation','Reserve all calls in a workflow before any provider request. Separate search and general budgets; Pacific quota dates; configurable costs. Consume budget before attempted calls and settle unused portions. Conservative abandoned reservations favor safety over automatic recovery.'),
('Honest metadata semantics','Analytics Data Semantics','Overview uses metadata, not transcript. Trends use playlist/subscription added timestamps, never video publication for likes. Strict language matches declared defaultAudioLanguage, with explicit caveat that speech is not independently verified.')]
for i,(title,note,decision) in enumerate(adrs,1):
    write(f'docs/adr/{i:04d}.md',f'# ADR-{i:04d}: {title}\n\nStatus: accepted for local implementation, human review pending. Date: 2026-10-31.\n\n## Context\nSee [[{note}]] and docs/SRS.md.\n\n## Decision and alternatives\n{decision}\n\n## Verification\nTests must exercise the described boundary, including negative and concurrent cases where relevant. Results are recorded in docs/test-results.md. GitHub issue/PR: DEFERRED.')
write('docs/diagrams/architecture.mmd','''flowchart TD
 Host[Existing AI host] -->|MCP stdio| MCP[Spring AI adapter]
 MCP --> Service[Application services]
 Service --> Domain[Pure domain]
 Service --> Port[YouTubeProvider]
 Port --> Google[Official YouTube API]
 Port --> Fixture[Synthetic fixtures]
 Service --> DB[(PostgreSQL)]
 CLI[Local human CLI] --> DB
 CLI --> Vault[Windows DPAPI vault]
 Port --> Vault
''')
write('docs/diagrams/playlist-sequence.mmd','''sequenceDiagram
 actor Human
 participant Host
 participant MCP
 participant DB as PostgreSQL
 participant Google
 Human->>Host: Natural-language constraints
 Host->>MCP: plan_playlist
 MCP->>DB: Reserve read quota
 MCP->>Google: Search and hydrate
 MCP->>DB: Persist immutable draft
 MCP-->>Host: Full proposal and fingerprint
 Host-->>Human: Review proposal
 Human->>DB: CLI creates scoped approval
 Host->>MCP: commit_playlist(draftId)
 MCP->>DB: Atomic claim and full quota reserve
 MCP->>DB: Journal write intent
 MCP->>Google: Create and insert ordered items
 MCP->>DB: Persist each result
 MCP-->>Host: CREATED or partial/manual-review state
''')
write('docs/diagrams/erd.mmd','''erDiagram
 drafts ||--o| approvals : authorizes
 drafts ||--o{ write_journal : records
 quota_buckets ||--o{ quota_reservations : reserves
 drafts { uuid id PK string account string fingerprint string state }
 approvals { uuid draft_id PK string account string fingerprint timestamp consumed_at }
 write_journal { uuid draft_id FK string step string status string remote_id }
 quota_buckets { date quota_date PK string bucket PK long reserved long consumed }
 quota_reservations { uuid id PK date quota_date string bucket long amount long used }
''')
write('docs/diagrams/components.mmd','''classDiagram
 class YouTubeProvider { <<interface>> }
 class FixtureYouTubeProvider
 class OfficialYouTubeProvider
 class CuratorService
 class DraftStore
 class QuotaService
 YouTubeProvider <|.. FixtureYouTubeProvider
 YouTubeProvider <|.. OfficialYouTubeProvider
 CuratorService --> YouTubeProvider
 CuratorService --> DraftStore
 CuratorService --> QuotaService
''')
write('docs/design-ranking.md','''# Ranking v1
Bounded corpus: seed plus at most 50 hydrated candidates; normalized lowercase Unicode letters/numbers,
stopwords, title repeated twice, tags once, description capped at 2000 characters.
TF=count/total; IDF=log((N+1)/(df+1))+1. Cosine zero for empty vectors.
Score=.55 cosine+.20 tag Jaccard+.10 known category agreement+.10 min/max positive duration
+ .05 known language agreement. Empty tags/category/language do not count as matches.
Stable sorting: descending score then ID. Exclude seed, unavailable candidates and duplicates.
Channel ranking uses title/description cosine and stable ID ties. Subscriber counts are not quality.
Personal profile combines normalized source text vectors, weights .45 likes/.30 subscriptions/.25
playlist items, renormalizing available sources with coverage warnings. Exclude known videos.
''')
write('docs/design-playlist-optimizer.md','''# Playlist selection v1
Hard cap is targetSeconds, not an assertion of exact duration. Return shortfall explicitly.
Filter invalid duration, language mismatch/unknown, duplicates and per-video maximum first.
Sort descending relevance then stable ID, add while within time/count caps. A deterministic
single-item replacement pass may improve total score without violating constraints. Greedy is
not globally optimal; the 20 vs 11+11 minute case is an explicit known limitation to test.
Do not add a dynamic program without measured value and bounded memory/time.
Return NO_FEASIBLE_PLAYLIST when empty, never create an empty success draft.
Fingerprint canonical JSON of immutable account/title/privacy/constraints/order/durations/expiry/version.
The normalized values, source request text and metadata-language caveat appear in the preview.
''')
write('docs/design-analytics.md','''# Analytics semantics
All outputs identify sampled counts, missing timestamps and collection bounds.
Top channel/category counts use deduplicated liked and playlist videos; subscriptions have a separate
channel count. Durations: positive known seconds, median, short <=600, medium <=1200, long >1200.
Trends count playlist-item additions and subscription additions by month. Compare half-open UTC
date intervals [start,end). No valid event evidence means unavailable, not invented history.
Liked-video publication timestamps never enter engagement trends. No watch-time metric exists.
''')
write('docs/security-threat-model.md','''# Threat model
Assets: refresh credentials, private metadata, account integrity, approval grants and quota.
AI tool input and all video metadata are untrusted. No model argument selects account or grants consent.
URL parsing checks exact host/path, rejects userinfo/ports/fragments ambiguity and never fetches user URLs.
Provider origins are fixed in production; loopback override is test-only. SQL uses bound parameters.
CLI requires a real console, previews exact account/privacy/items/digest, and verifies the typed phrase.
Fingerprint, expiry and account are checked again in the database claim. Same-OS-user code/DB access
is a trusted local boundary, not a defense against arbitrary malicious local administrators.
Write intent persists before network send; ambiguous response fails closed for manual reconciliation.
No raw provider bodies or exception text are returned to the model. Logs must omit private collections.
DPAPI credentials are scoped to CurrentUser and live outside source; .env is ignored. Logout revokes
and removes credentials; data deletion removes local account drafts/grants/journals.
Scope youtube.force-ssl supports required operations. No partner scope, password collection or OOB flow.
Live acceptance is pending the user's Google setup. Production retention must be checked against
current YouTube developer policy before deployment beyond coursework.
''')
write('docs/test-plan.md','''# Test plan
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
''')
write('docs/brain-query-evidence.md','''# Brain-query applied — 2026-10-31
Question: Why stdio, and what changes if we expose /mcp?
Answer: [[MCP Stdio Semantics]] defines a host-launched process and protocol-only stdout.
[[Google OAuth Desktop PKCE]] binds Google access to one locally selected credential, not remote
callers. ADR-0001 chooses that narrower local trust boundary. A hosted endpoint would need a distinct
MCP client authentication layer, user isolation and TLS; Google OAuth alone would not provide those.
[[Codex Project Boundaries]] excludes that expansion. No remote server or PR evidence is claimed.
''')
for n,title,files in [(10,'Headless architecture','docs/architecture.md; docs/diagrams'),(11,'Traceable architecture decisions','docs/adr/0001.md through 0008.md'),(12,'Brain refine and query','brain/resources; docs/brain-query-evidence.md; brain/log.md'),(13,'MCP contract design','docs/SRS.md; handbook chapter 36'),(14,'Durable schema design','docs/diagrams/erd.mmd; ADR-0003'),(15,'Algorithm contracts','docs/design-ranking.md; docs/design-playlist-optimizer.md; docs/design-analytics.md'),(16,'Quota workflow design','ADR-0007; docs/security-threat-model.md'),(17,'Testing strategy','docs/test-plan.md'),(18,'Local-check specification',' .agents/skills/local-check/SKILL.md')]:
    record(n,title,'Design complete; runtime evidence pending',
           f'Authored and reviewed the design in {files}. The decision is derived from the handbook and cited brain notes. Defined input boundaries, state transitions and failure behavior before application implementation. Separated fixtures from live access and local human approval from AI-generated requests.',
           files,'Document inspection only at this design gate. Runtime tests will verify the contracts during Stage 3.',
           'Stage 1 local artifacts and Stage 2 designs exist. Fourteen notes have been refined without renaming links. Eight ADRs establish implementation boundaries.',
           'Human review/GitHub evidence deferred. Live Google cannot run until user setup. No code/test success is inferred from this design note.')
print('Recorded steps 0–18 and Stage 2 design artifacts.')
