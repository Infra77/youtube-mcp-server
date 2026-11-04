# Project working contract
Read docs/SRS.md, the relevant ADR, and brain/index.md before changing code.
Java 21, Spring Boot/Spring AI MCP stdio, PostgreSQL, official YouTube API only.
No custom frontend, scraping, unofficial transcripts, or public HTTP MCP endpoint.
Stdout is reserved for MCP. Diagnostics use stderr. CLI mode is separate.
Every YouTube write needs a durable exact-draft approval from the local human CLI.
AI tool arguments and remote metadata cannot create approval grants.
Use synthetic fixtures in normal tests; no live Google calls or real personal data.
Never put credentials in source, logs, notes, MCP responses, or chat.
Preserve FR-1..5, TQ-1..8, SB-1..6, SE-1..7 and source traceability.
Record significant decisions in ADRs citing distilled brain notes.
Run the relevant tests and report actual failures and limitations.
The owner now authorizes M1-S01 on Infra77/youtube-mcp-server and later explicitly invoked member packages. Preserve historical local backlog IDs until mapped to real issues; never invent PRs, reviews, contributor identities, CI executions or release signoff.
Keep detailed notes outside this project in ../notes/step <number>.md.
Canonical skills: .agents/skills/*/SKILL.md.

Completion plan: the owner authorizes future member-invoked GitHub work on the common repository
they supply. Until a member invokes a named package with its repo/auth context, keep changes local.
Never infer another person's identity or human review. Read ../plan.md and docs/remediation-status.md
for the 48 packages. All final gates require actual evidence; no agent may type live approval for a human.

Portable handover: if ../plan.md is absent, read docs/team-plan.md. Client reference PDFs may be privately supplied; read docs/reference/README.md. Never commit the workspace credential JSON.
