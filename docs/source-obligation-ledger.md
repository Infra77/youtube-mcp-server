# M2-S01 source obligation ledger

Prepared 2026-11-05; reconciled 2026-11-06 (Asia/Calcutta), AI-assisted for Kulshresth / htserhsluk (M2).
Package issue: https://github.com/Infra77/youtube-mcp-server/issues/3
Human review and final merge: pending. This inventory is not acceptance signoff.

All original pages were read: SDLC (S), 3 pages; Project (P), 2 pages; Handbook (H), 53 pages.
Page references are one-based. Client originals remain private; this ledger paraphrases the
obligations and distinguishes them from implementation choices. Source originals are obtained
through the authorized owner as described in reference/README.md, not downloaded from public Git.

## Numbered obligation inventory (41 IDs)

There are 26 client-numbered IDs (5 FR, 8 TQ, 6 SB, 7 SE), five locally numbered SK IDs
whose underlying workflows are required, and ten project-owned NFR IDs. All 41 appear in
the current traceability CSV. Presence is not acceptance or proof of test coverage.

| ID | Authority | Required acceptance preserved |
|---|---|---|
| FR-1 | P p1 section 2 | Video URL/ID produces ranked metadata-similar videos through MCP. |
| FR-2 | P p1 section 2 | Channel URL/handle/ID produces ranked similar channels. |
| FR-3 | P p1 section 2 | Recommendations use likes, subscriptions AND playlists; authorized sampled coverage is explicit. |
| FR-4 | P p1 section 2 | All three sources support top channels/categories, durations, trends and period comparisons where timestamps support them. Unavailable is not zero or invented watch history. |
| FR-5 | P pp1-2 section 2 | Natural-language topic/total/per-video/language constraints; exact preview; explicit human confirmation before creating in the authorized account. |
| TQ-1 | P p2 section 4 | Units cover modules/services/tools, similarity, duration parsing and constraints. |
| TQ-2 | P p2 section 4 | Integration covers component interactions including the production provider boundary. |
| TQ-3 | P p2 section 4 | Each FR has system tests through MCP, not only direct service tests. |
| TQ-4 | P p2 section 4 | Named cases for malformed IDs, private/deleted, missing tags, quota, no channel, expired token and rate limiting. |
| TQ-5 | P p2 section 4 | Ordinary CI uses mocks/fixtures; live tests run separately on a schedule with fixed budget. A disabled workflow is not completion. |
| TQ-6 | P p2 section 4 | Track each request cost; insufficient full-workflow budget rejects before any API call. |
| TQ-7 | S p2 section 5 | Run skill evaluations before every stage and record actual results. |
| TQ-8 | S p2 section 5 | Maintain tests as changes occur; significant defects get regression tests. |
| SB-1 | S p1 section 1 | Interlinked notes also link requirements, issues and PRs. |
| SB-2 | S p1 section 1 | Each stage has a retrospective describing outcomes and improvements. |
| SB-3 | S p1 section 1 | Every ADR and skill cites a relevant distilled note. |
| SB-4 | S p1 section 1 | Repository-root AGENTS.md. |
| SB-5 | S p1 section 1 | All brain changes, including AI changes, go through PR review. |
| SB-6 | S p1 section 1 | Every real member authors notes with visible commit history. |
| SE-1 | S p1 section 2 | Maintain SRS with FR, NFR and SK requirements. |
| SE-2 | S p1 section 2 | Architecture/design with appropriate UML/ER diagrams. |
| SE-3 | S p1 section 2 | Significant decisions in docs/adr with cited brain notes. |
| SE-4 | S p1 section 2 | Development plan and task breakdown. |
| SE-5 | S p1 section 2 | Requirement-to-issue-to-PR-to-test-to-skill-to-note chain. |
| SE-6 | S p1 section 2 | External dependencies isolated behind a provider interface. |
| SE-7 | S p2 section 2 | User and developer API documentation. OpenAPI is an example, not a requirement to add REST. |
| SK-01 | S p1 section 1; H pp19-20,47 | brain-ingest records attributable sources, provenance, links and runs; unknown author/date stays unknown. |
| SK-02 | S p1 section 1; H pp25,47 | brain-refine organizes PARA, merges duplicates and repairs links without losing sources. |
| SK-03 | S p1 section 1; H pp25,47 | brain-query gives grounded answers and drafts SRS/ADRs with citations and uncertainty. |
| SK-04 | S p2 section 3; H pp28,48 | local-check builds, tests, starts server, invokes a read-only operation and reports each step. |
| SK-05 | P p2 section 3; H pp40-41 | Video overview, similarities, proposal/confirmation, creation, short playlist analysis. Metadata overview must not impersonate transcript access. |
| NFR-01 | Team choice; H p20 | Protect credentials in OS vault; none in Git/logs/chat/MCP outputs. Supports client security obligation. |
| NFR-02 | Team choice; H p20 | Repeatable ranking/selection and stable tie-breaking. |
| NFR-03 | Team choice; H p20 | Explained components and missing-data caveats. |
| NFR-04 | Team choice; H pp20,27-28 | Atomic whole-workflow reservation across configured active quota dimensions. Supports TQ-6. |
| NFR-05 | Team choice; H pp20,38-39 | Immutable drafts, account-bound one-use grants, durable journal and conservative recovery. Supports FR-5. |
| NFR-06 | Team choice; H pp20,45 | Clean supported-machine reproduction without Google credentials for fixtures. |
| NFR-07 | Team choice; H pp20,45 | Minimal personal data, documented retention/deletion and revocation. |
| NFR-08 | Team choice; H p20 | Typed actionable errors without raw upstream bodies or secrets. |
| NFR-09 | Team choice; H p20 | Bounded candidates, sampling, pagination and retries. |
| NFR-10 | Team choice; H p20 | Tested compatible MCP stack, discovery/resources and actual host evidence. |

## Mandatory obligations outside the numbered matrix

| Source | Obligation and verification needed |
|---|---|
| P p1 section 1 | Genuine MCP tools AND resources plus usable Agent Skills. Skill files and MCP prompts are distinct; host discovery must be demonstrated. |
| P p2 section 2 | Compute similarity from metadata; no watch-history or direct related endpoint claims. |
| P p2 section 4 security | Least scopes/safe storage, no repository secrets, all-parameter validation, metadata injection resistance, no real personal fixtures/logs. |
| P p2 section 5 | Official API only; caching and fixtures; no extra projects to evade quota. Preserve the source's 10,000-unit statement as provenance, verify current actual costs separately. |
| P p2 section 5 | Support Testing-mode reauthorization and no-channel failure. Source's seven-day statement is not a permanent credential guarantee. |
| S p1 section 1 | Obsidian PARA, index and run log; three brain workflows. |
| S p2 section 4 | Meaningful contributions by every member, branching policy, issues for all work/defects, review for all PR changes, changelog and tags. |
| S p2 section 4 | Every-PR build, lint, tests, secret scan, skill schema validation and brain schema/link validation. |
| S p2 section 6 | Human reviews all AI-generated PR changes; members understand merged work; significant AI sessions recorded; no secrets supplied to AI. |
| S p2 section 7 | Stage 1 SRS, PARA/index/log, at least ten genuinely ingested research notes, AGENTS, repository and CI skeleton. |
| S p2 section 7 | Stage 2 architecture/diagrams, actual refine/query workflows and local-check v1. |
| S p3 section 7 | Stage 3 CI/test evidence, product skill and tests, defect/regression log and stage reviews. |
| S p3 section 7 | Stage 4 live FRs in a client, end-to-end product skill, live local-check/query, trace walkthrough and final tag. |

## Findings against the imported baseline

1. SRS authority section says a local-only deviation is authorized. That describes earlier work,
   not a waiver of current shared-repository obligations. Replace with historical provenance and
   explicit current plan authority; preserve all mandatory remote/human acceptance gates.
2. assumptions.md says GitHub is deferred and Google is unconfigured, and mentions two people.
   Reconcile with the three-member plan, actual import PR, and historical 3 November consent/live
   observations. Those observations do not authorize this workstation or establish complete live acceptance.
3. handbook-amendments.md items 1 and 4 repeat obsolete local-only/no-Google statements.
   Add a dated superseding entry; preserve earlier decisions as history and private original PDFs.
4. SRS summarizes but does not make every unnumbered client obligation readily auditable.
   Link a supplemental source-obligation ledger; explicitly preserve every-PR CI, actual scheduled
   live execution, no quota evasion, stage evidence and human comprehension.
5. Scope policy must clearly retain Java 21, Windows DPAPI for live use, PostgreSQL 16,
   one configured local account, no custom frontend, integer-second upper-bound duration,
   strict declared audio language (unknown excluded), 50-item maximum, exact immutable preview,
   shorter-than-target disclosure and refusal/error behavior. These are implementation choices,
   not verbatim client mandates. Client FR-5 remains mandatory regardless of those choices.
6. Current traceability has all 41 rows, but many legacy L-* IDs and DEFERRED PRs. Do not
   fabricate links or replace historical IDs wholesale: M2-S01 maps audit closure issues;
   M1-S02 owns broad backlog migration and validator strengthening. Preserve old IDs explicitly.
7. validate_traceability.py checks presence/paths, not exact unique ID equality, real review
   status or semantic assertions. Run it but do not call a PASS exhaustive acceptance proof.
8. docs/reference/README.md appropriately excludes private source originals from public import;
   remediation-status.md's portability wording should not imply those PDFs ship in Git.

## Audit closure issue preparation

The 18 issues below were created after authenticated duplicate inspection; real URLs follow. Each records
acceptance criteria, requirement IDs, actual owner/reviewer, related legacy backlog IDs and links
to its execution packages. No issue number below is invented.

| Audit | Closure scope | Primary packages | Related historical steps |
|---|---|---|---|
| A1 | Credential generation, disconnect, lifecycle | M1-S05/S09 | L-24,L-39 |
| A2 | Bounded account-keyed metadata cache | M3-S05,M1-S08 | L-16,L-22,L-23 |
| A3 | OAuth/DPAPI negative tests | M1-S05 | L-24,L-37,L-39 |
| A4 | Exact production-provider and MCP assertions | M1-S08,M2-S07/S08 | L-22,L-26,L-27,L-28,L-29,L-38 |
| A5 | Five actual-host skill evaluations at stages | M2-S03/S06/S10/S11,M3-S13 | L-35,L-41 |
| A6 | Relevance labels and bounded performance | M1/M2/M3-S07 | L-15,L-26,L-27,L-28,L-36 |
| A7 | Persisted exclusions and draft diagnostics | M2-S05/S08 | L-30,L-31,L-32 |
| A8 | Proposed/confirmed partial result totals | M2-S05,M1-S10 | L-32,L-39 |
| A9 | Retention and safe data deletion | M3-S05/S10/S12 | L-14,L-24,L-47 |
| A10 | Quality gates and reviewed scans | M3-S02,M2-S06,M3-S11/S14 | L-09,L-17,L-40,L-42 |
| A11 | Source/contract/scope documentation | M2-S01/S02,all S04,M2-S13/S15 | L-00,L-07,L-13,L-43,L-45 |
| B1 | Real authorized Google acceptance | M1-S09,all S12 | L-24,L-43,L-45 |
| B2 | Actual host and complete skill demo | M2-S10/S12,M3-S13 | L-33,L-34,L-45 |
| B3 | Independent supported machines | M3-S01,all S13 | L-01,L-44 |
| B4 | Genuine human review/authorship | All packages and stage gates | L-03,L-05,L-06,L-45 |
| C | GitHub/CI/scheduled workflow/release | M1-S01/S02,M3-S02/S09/S11 | L-02,L-05,L-08,L-09,L-40,L-46 |
| D1 | Partial-write recovery without duplicates | M1-S04/S10 | L-14,L-32,L-39 |
| D2 | Bounded pagination and truthful coverage | M3-S05,M1-S08 | L-22,L-23,L-28 |


## Real audit tracking links

| Audit | GitHub issue | Coordination owner |
|---|---|---|
| A1 | https://github.com/Infra77/youtube-mcp-server/issues/4 | Infra77 |
| A2 | https://github.com/Infra77/youtube-mcp-server/issues/5 | abhinavbhatia2006 |
| A3 | https://github.com/Infra77/youtube-mcp-server/issues/6 | Infra77 |
| A4 | https://github.com/Infra77/youtube-mcp-server/issues/7 | Infra77 |
| A5 | https://github.com/Infra77/youtube-mcp-server/issues/8 | htserhsluk |
| A6 | https://github.com/Infra77/youtube-mcp-server/issues/9 | abhinavbhatia2006 |
| A7 | https://github.com/Infra77/youtube-mcp-server/issues/10 | htserhsluk |
| A8 | https://github.com/Infra77/youtube-mcp-server/issues/11 | htserhsluk |
| A9 | https://github.com/Infra77/youtube-mcp-server/issues/12 | abhinavbhatia2006 |
| A10 | https://github.com/Infra77/youtube-mcp-server/issues/13 | abhinavbhatia2006 |
| A11 | https://github.com/Infra77/youtube-mcp-server/issues/14 | htserhsluk |
| B1 | https://github.com/Infra77/youtube-mcp-server/issues/15 | Infra77 |
| B2 | https://github.com/Infra77/youtube-mcp-server/issues/16 | htserhsluk |
| B3 | https://github.com/Infra77/youtube-mcp-server/issues/17 | abhinavbhatia2006 |
| B4 | https://github.com/Infra77/youtube-mcp-server/issues/18 | Infra77 |
| C | https://github.com/Infra77/youtube-mcp-server/issues/19 | Infra77 |
| D1 | https://github.com/Infra77/youtube-mcp-server/issues/20 | Infra77 |
| D2 | https://github.com/Infra77/youtube-mcp-server/issues/21 | abhinavbhatia2006 |
