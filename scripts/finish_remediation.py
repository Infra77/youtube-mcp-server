"""Refresh current handover text without rewriting historical execution evidence."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1]
def write(p,t):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def append(p,t):
 p=R/p;p.write_text(p.read_text(encoding='utf-8')+'\n'+t.strip()+'\n',encoding='utf-8')
write('docs/acceptance-status.md','''# Acceptance status — 2026-11-03

This is a remediated local review candidate, not final client acceptance. Read test-results.md for
the actually executed current test counts and docs/remediation-status.md for audit closure.

Implemented locally: all five FRs through MCP; strict approval and quota; protected OAuth; credential
generation checks; local deletion even when revoke fails; bounded five-minute account-keyed metadata
cache; two-page sampled personal reads; schema-2 exclusions/URLs; proposed-versus-confirmed write
results; exact-prefix human-authorized partial repair; manual ambiguous resolution; startup/hourly
retention; expanded OAuth/provider/database tests; relevance benchmark; strict schema/trace/secret
quality gates. No Google call is required by ordinary tests.

Still required for final acceptance: actual team human review and authorship, real skill-host runs at
four stage gates, Google setup/consent/live FR verification and real approved write, chosen-host demo,
independent machines, actual GitHub protections/issues/PRs/CI/scheduled live run and final tag.
The portable ../plan.md assigns every obligation to three people over 16 days. The agent cannot
replace real Google consent, a typed human playlist grant or another person's review.

Windows-only DPAPI live vault, declared metadata-language policy, supported bounded text grammar,
private playlists and heuristic optimization are explicit scope choices. Sampling is up to two pages
per personal source within 50 likes/30 subscriptions/5 playlists x 30 items. Unknown create outcomes
are never replayed; only known PARTIAL exact-prefix playlists can be repaired with fresh CLI approval.
The quota ledger estimates project usage and cannot observe other Google clients' spending.

Final command: python scripts/release_gate.py --final. PENDING gates must remain pending until actual
evidence and human review exist. No final date or passing test count overrides those obligations.
''')
write('docs/remediation-status.md','''# Completion-audit remediation — 2026-11-03

The 2 November audit remains a historical record outside the project. This document records code
changes made in response, not retrospective human signoff. Original source PDFs are portable under
docs/reference; unchanged originals also remain outside the project on the initial workstation.

| Audit | Local changes | Remaining independent acceptance |
|---|---|---|
| A1 | File-generation-bound access; restart on reauth; logout always deletes locally; orphan deletion | live lifecycle and human security review |
| A2 | 128-entry/five-minute account-keyed metadata cache; no charge on hits | live quota/cache review |
| A3 | Local loopback OAuth exchange, denial/state, scope/refresh, revoke and replacement regression tests | native vault and full adversarial matrix peer review |
| A4 | Additional official endpoint/collection/paging/creation/readback tests | expanded exact FR assertions and independent coverage review in plan |
| A5 | Concrete per-skill positive/negative cases, strict validation, honest coordinator failure checks | actual supported-host evaluations at each stage; no generated substitute |
| A6 | Four synthetic relevance cases and bounded 50-candidate timing test | independent labels and channel/profile/noise cases in plan |
| A7 | Schema-2 persisted exclusion diagnostics and canonical links | peer schema/host review |
| A8 | Proposed/confirmed counts and per-video status; repair tests | live approved small playlist demonstration |
| A9 | Startup/hourly and manual seven-day retention, immediate local deletion | policy review and independent lifecycle tests |
| A10 | Gitleaks, OSV/SBOM review, patched dependencies, stricter local pipeline/final evidence gate | real CI, history/package review and complete traceability |
| A11 | SRS sections, deployment diagram, scope/contract/recovery docs | team/client review and source-to-code walkthrough |
| B1–B4/C | Explicit acceptance manifest and 48-package team schedule | real Google/host/machines/humans/GitHub events |
| D1 | Console-only exact-prefix repair and manual resolution | peer fault/recovery review, no ambiguous replay |
| D2 | At most two pages within item bounds, repeated-token rejection and budget update | live collection coverage review |

Do not equate this table with every issue closed. All required independent and external evidence is
assigned in plan.md. The final gate deliberately fails until those obligations are satisfied.
''')
append('README.md','''## Completion remediation and team execution

Start with [current audit disposition](docs/remediation-status.md), [acceptance status](docs/acceptance-status.md)
and [ADR-0010](docs/adr/0010.md). The owner-provided plan.md sits next to the project and contains
16 member steps for each of three real participants (48 packages). It treats the existing code as an
honest baseline, not a fabricated 16-day development history. Original source PDFs are preserved in
docs/reference for portable review; confirm client permission before publishing them publicly.

Run quality tooling setup from docs/setup-windows.md, then local-check. Final acceptance uses
scripts/release_gate.py --final and actual linked evidence; it is not implied by a successful build.
''')
append('CHANGELOG.md','''## Local completion remediation — 2026-11-03 (review candidate)

- Bind cached tokens to credential generation; always perform local disconnect cleanup and report remote revoke separately.
- Add bounded metadata cache and two-page personal sampling with full worst-case quota reservations.
- Persist schema-2 exclusions and URLs; report proposed/confirmed item totals and per-video statuses.
- Add human-authorized known-prefix repair, manual resolution and seven-day scheduled retention.
- Expand OAuth, provider and database regressions and synthetic relevance/timing evaluation.
- Upgrade compatible vulnerable dependency versions; retain a documented HTTP-only advisory applicability review.
- Add Gitleaks, strict skill cases/schema, traceability and final acceptance gates; portable 48-package team plan.
- These changes have no fabricated Google acceptance, PR review, skill-host evaluation or final release tag.
''')
append('docs/versions.md','''## Completion revision

Current pom.xml is authoritative: Spring Boot 3.5.16, Spring AI 1.1.8, Jackson BOM 2.21.7,
Logback 1.5.34, Log4j 2.25.5 and PostgreSQL JDBC 42.7.12. Java 21/Maven wrapper remain.
MCP SDK stays on the tested Spring AI managed line; the HTTP-only DNS-rebinding advisory has a
recorded stdio-only applicability decision requiring independent review. See security-dependency-review.md.
''')
append('docs/ci-local.md','''## Revised local gates

local-check delegates to quality_pipeline.py and starts with clean package, then tests, formatting,
documentation, traceability, strict skill YAML/cases, Gitleaks and actual MCP launch/read. Networked
CycloneDX/OSV checks are separate and included in final release review. The coordinator self-test
proves failure propagation, not actual host skill behavior. No fake independent skill report is created.
The plan schedules creation and actual execution of PR CI and fixed-budget scheduled live checks.
''')
append('AGENTS.md','''
Completion plan: the owner authorizes future member-invoked GitHub work on the common repository
they supply. Until a member invokes a named package with its repo/auth context, keep changes local.
Never infer another person's identity or human review. Read ../plan.md and docs/remediation-status.md
for the 48 packages. All final gates require actual evidence; no agent may type live approval for a human.
''')
append('brain/log.md','''## 2026-11-03 — resumed verification and team handover
Resumed after approval-service limits and interruptions. Preserved Docker runtime socket directories
without deleting volumes and recovered the local engine. Reran real PostgreSQL/MCP integration checks.
Created a portable plan with 16 packages for each of three members, review rotation, evidence gates,
Google/human prerequisites and complete audit mapping. No historical contribution or approval invented.
''')
# Keep one-time source rewriting utilities outside the delivered runtime/source distribution.
archive=R/'target/remediation-authoring';archive.mkdir(parents=True,exist_ok=True)
for name in ['remediate_core.py','remediate_provider.py','remediation_docs.py']:
 p=R/'scripts'/name
 if p.exists():shutil.move(str(p),str(archive/name))
# Every changed handbook step receives an explicit detailed revision, preserving prior notes.
for n in [7,10,13,14,15,16,17,18,22,23,24,28,31,32,34,35,36,37,38,39,40,41,42,43,44,45,46,47]:
 p=R.parent/'notes'/f'step {n}.md'
 with p.open('a',encoding='utf-8') as f:f.write(f'''
## Completion remediation — 3 November 2026

This step was reassessed against the original client PDFs and the 53-page handbook, not marked
complete merely because this note exists. See project docs/remediation-status.md and ADR-0010 for
the exact finding-to-change mapping. The local revision now contains credential-generation checks,
disconnect fallback, bounded cache and pagination, schema-2 exclusions/URLs, precise partial-write
counts, exact-prefix repair and explicit retention. Tests exercise local OAuth exchanges, official
provider contracts, database behavior and packaged MCP. Full executed counts and failures are
recorded in docs/test-results.md; older reports in this note remain historical, not current signoff.

Quality tooling now distinguishes source validation, actual execution and human acceptance. The
final manifest remains pending for real Google consent/playlist creation, selected-host skill runs,
independent machines and genuine three-person GitHub review/history. The external plan.md assigns
all those tasks with commands, evidence paths, dependencies and peer-review rules. Future agents
must execute the appropriate M1/M2/M3 step, record real results and add focused detail here when
this handbook step changes. No automated report substitutes for explicit human authorization.
''')
print('Current handover text refreshed; historical notes preserved')
