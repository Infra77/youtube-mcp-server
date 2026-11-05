---
type: research
status: draft
author: htserhsluk (AI-assisted; human inspection pending)
reviewed: 2026-11-06
requirements: [SE-1, SB-1, FR-3, FR-4, FR-5, TQ-5, TQ-8]
source_urls: ["client:Project_1_YouTube_MCP.pdf", "client:SDLC_and_Workflow.pdf", "handbook:YouTube_Intelligence_MCP_Server_Only_Handbook.pdf"]
---
# Client Obligations and Implementation Choices

## Question
Which parts of the existing implementation can change without silently dropping a client obligation?

## Source-grounded findings
The Project PDF (pp1-2) requires all five FRs, official API use, constrained preview/confirmation,
the product workflow, tests and quota controls. The SDLC PDF (pp1-3) additionally requires the
brain, skills, genuine PR reviews, team authorship, staged evidence and release history. The
handbook explicitly distinguishes assignment requirements from decisions/examples (pp1-2,20-21,52).
It cannot waive the clients' obligations. Numeric SK IDs are local labels for required workflows;
NFR IDs and precise technical bounds are project decisions supporting those obligations.

For FR-3, likes, subscriptions and playlists are three required inputs, not interchangeable
options. For FR-4, missing timestamps cannot be replaced by video publication dates or zero
activity. For FR-5, an upper-bound duration interpretation is a declared policy: a shorter valid
selection must disclose its shortfall and be shown before confirmation. Metadata-language
agreement is evidence about declared metadata, not proof of spoken language.

The handbook's Windows/Java/Postgres/CLI design is an implementation choice; the client still
requires explicit human confirmation and secure account access. Likewise, a local test report
cannot replace the separate scheduled live workflow required by TQ-5. A recorded historical
demo cannot prove an entire composite acceptance gate without its remaining checks.

## Original implication from this audit
Source authority should be recorded separately from implementation evidence. A 41-row matrix
can contain every identifier yet omit unnumbered security, CI and stage obligations. This is why
the source ledger has both numbered and unnumbered inventories, with page references and real
audit issues. Path-existence validation is useful but cannot establish semantic test coverage.

The packaging finding is a practical example: ignoring private PDFs in Git does not protect a
ZIP built by recursively copying the filesystem. A distribution boundary needs its own checks,
including regression tests using synthetic private-file sentinels rather than real credentials.

## Evidence and remaining questions
[M2-S01 issue](https://github.com/Infra77/youtube-mcp-server/issues/3),
[source ledger](../../docs/source-obligation-ledger.md),
[execution](../../docs/execution/day-01/member-2.md).
All original source pages were read privately. Public redistribution of originals is prohibited.
The note was prepared with AI assistance for M2; it does not claim human comprehension or
independent review before the responsible members inspect and decide.

Related: [[Codex Project Boundaries]], [[Analytics Data Semantics]],
[[Language and Duration Metadata]], [[M2 Packaging Privacy Fix]].
