# M2 packaging privacy fix

Date: 2026-11-06 (Asia/Calcutta). AI-assisted work for Kulshresth / htserhsluk (M2).
Human review and merge: pending. Issue: https://github.com/Infra77/youtube-mcp-server/issues/3

Goal: fix the release-file disclosure reproduced during M1 import review, after the user explicitly
requested the correction. Inputs: the three private source documents, source-contract audit,
packaging/verifier code, [[CI Fixture Isolation]] and [[Codex Project Boundaries]].

Finding: Git ignore rules protected the import but did not protect filesystem-based ZIP creation.
Synthetic private PDFs, credential JSON and environment files were included. The new policy
excludes private paths and rejects contaminated archives before extraction. It preserves public
documentation and placeholder environment templates. No real private file was used for tests.

Checks: both packaging regression tests pass, including nine source roots and verifier refusal
cases; quality coordinator self-test passes 11 cases; documentation and development traceability
checks pass. The baseline's 47 Java tests passed before this Python-only fix; no new Java-suite
execution is claimed for this change. No live Google action, review submission or merge occurred.

This fix is on M2's own branch based on the reviewed import, not attributed to M1. It does not
complete M2-S01 or make the agent's self-check an independent human review. The earlier AI review
must be updated and the changed commit reviewed before any approval is recorded.
