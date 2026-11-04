# Skill workflow evaluations — 2026-11-01

Evaluator: Codex authoring agent, with deterministic artifact/protocol checks. These are not an
independent agent benchmark and do not prove that a particular AI host automatically imports skills.
No live Google account or real approval was used. [Machine-readable results](evidence/skill-evaluations.json).

| Skill | Case | Outcome |
|---|---|---|
| brain-ingest | undated-source | PASS |
| brain-ingest | missing-source | PASS |
| brain-refine | move-preserves-source | PASS |
| brain-refine | conflicting-evidence | PASS |
| brain-query | grounded-answer | PASS |
| brain-query | unsupported-question | PASS |
| brain-refine | validated-result | PASS |
| brain-refine | broken-link-detected | PASS |
| video-to-playlist | fixture-orchestration-order | PASS |
| video-to-playlist | missing-approval | PASS |
| video-to-playlist | truthful-fixture-result | PASS |
| local-check | historical-build-failure | PASS |
| local-check | executed-workflow | PASS |

brain-ingest was applied to an actual synthetic undated input; the resulting note explicitly retains
unknown author/date. Missing-source handling produced an explanation and no invented research note.
brain-refine moved the note while preserving bytes/basename, retained a contradictory synthetic claim
for review, and validated the vault. A deliberately broken link caused the isolated validator to fail.
brain-query answers were authored after reading the actual quota/stdout/OAuth notes; an unsupported
viewing-history question was explicitly declined. Those two answers are author-reviewed outcomes,
not assertions that a string-matching test measures language-model reasoning.

video-to-playlist checks use the real MCP transcript for workflow order, missing-grant rejection and
truthful fixture outcomes. PostgreSQL tests separately assert no writes and replay safety. The positive
grant is a test administrator simulation; interactive live human consent remains a separate gate.
local-check ran the real build/test/start/read workflow. An actual earlier failing build is retained as
negative evidence; the final successful report is separate. Further independent skill/host evaluation
is required at human stage submission. No historical stage submission or PR review was invented.
