# Local quality gates and authorized GitHub bootstrap

The owner authorized M1-S01 on Infra77/youtube-mcp-server on 4 November 2026. Main now requires
a human peer approval, stale-review dismissal and no force-push/deletion. Actions use read-only
default token permissions and GitHub-owned actions only. No hosted CI run is claimed yet; M3-S02
creates/verifies real PR jobs and adds their actual required check contexts.

scripts/local-check.ps1 is the executed local equivalent: package, tests, formatting,
documentation links, supplemental source secret scan, actual server startup and read-only MCP call.
validate_traceability.py checks source/test/skill/note paths and explicit deferred statuses.

The secret scanner detects selected common credential forms and tests itself with an ephemeral
synthetic key. It is supplemental and not a replacement for an audited hosted scanner or security review.
The full Maven suite uses WireMock, fictional provider data and disposable PostgreSQL only.

When GitHub is authorized, translate these commands into restricted-permission PR workflows, require
human review, add audited secret/dependency scanning, and archive sanitized reports. A separate
scheduled live workflow must use a dedicated account and an explicit fixed quota gate; it must stay
disabled until credentials and review exist. Live tests must never become a PR merge prerequisite.

## Revised local gates

local-check delegates to quality_pipeline.py and starts with clean package, then tests, formatting,
documentation, traceability, strict skill YAML/cases, Gitleaks and actual MCP launch/read. Networked
CycloneDX/OSV checks are separate and included in final release review. The coordinator self-test
proves failure propagation, not actual host skill behavior. No fake independent skill report is created.
The plan schedules creation and actual execution of PR CI and fixed-budget scheduled live checks.
