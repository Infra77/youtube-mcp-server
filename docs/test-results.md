# Executed verification - 3 November 2026

**47 Java tests passed, with zero failures, errors or skips.** The full local pipeline
ran clean package, verify (including PostgreSQL Testcontainers and packaged MCP), formatting,
documentation, traceability, strict skill/case schema validation, Gitleaks and MCP startup/read.
After the final CLI help-text change, package reran all 32 unit tests successfully; the 15
integration results are from the preceding full verify. [Actual cases](evidence/test-summary.json).

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| DomainTest | 8 | 0 | 0 | 0 |
| RankingEvaluationTest | 1 | 0 | 0 | 0 |
| MetadataCacheTest | 1 | 0 | 0 | 0 |
| OAuthLifecycleTest | 7 | 0 | 0 | 0 |
| ProviderTest | 10 | 0 | 0 | 0 |
| SemanticsTest | 3 | 0 | 0 | 0 |
| ServiceTest | 2 | 0 | 0 | 0 |
| DatabaseIT | 14 | 0 | 0 | 0 |
| McpProtocolIT | 1 | 0 | 0 | 0 |

[Local pipeline](evidence/local-check.json), [MCP protocol](evidence/mcp-protocol.json),
[startup/read smoke](evidence/smoke.json), [coordinator negative cases](evidence/local-check-negative.json),
[ranking benchmark](evidence/ranking-evaluation.json), [dependency audit](evidence/dependency-audit.json)
and [runtime BOM](evidence/bom.json) record the executed checks. The ranking cases are synthetic;
they do not replace independent relevance evaluation. Gitleaks found no leaks in its configured scope.
OSV checked 66 exact Maven components: no undispositioned known advisory; one HTTP-only MCP advisory
is retained as not applicable to stdio, with independent human review still required.

[Package verification](evidence/package-check.json) records the final archive hash and an actual
extracted PowerShell launcher probe on this machine. It is not independent-machine acceptance.
Skill schemas and coordinator checks are not real agent-host behavioral evaluations.

Google setup/consent, native credential lifecycle, live FR-1 through FR-5, personally approved
playlist creation, host skill runs, peer review, independent machines, GitHub controls/CI/history
and final signoff remain explicit gates in acceptance-evidence.json and the external plan.md.
