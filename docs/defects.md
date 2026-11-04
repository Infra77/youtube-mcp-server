# Defect and regression log

| ID | Finding | Fix / evidence |
|---|---|---|
| D-001 | Scheme-less input produced NullPointerException from immutable Set.contains(null) | Explicit scheme-null guard; DomainTest.parsesSupportedIdsAndRejectsHostAndAmbiguousParameters |
| D-002 | Windows inherited temporary socket path broke Java selector startup | Short jdk.net.unixdomain.tmpdir; five WireMock tests passed after change; setup documentation updated |
| D-003 | Example wikilink in brain-query skill was treated as a nonexistent research citation | Replaced placeholder with plain prose; validate_docs.py passes |
| D-004 | First packaged MCP initialization timed out because headless configuration had no ObjectMapper bean | Explicit JavaTime-enabled ObjectMapper bean; protocol regression rerun required |
| D-005 | Partial date arguments were ignored when startA was absent | Require either all four dates or none; ServiceTest validates no provider call |
| D-006 | Regional language constraint was relaxed to primary language; malformed tag could index an empty split | Exact region matching and malformed-tag exclusion; DomainTest.languageRegionIsNotSilentlyRelaxedAndMalformedMetadataIsExcluded |

D-004 was subsequently verified by the passing packaged MCP test and standalone smoke probe.

All issue/PR references are DEFERRED by the user's local-only instruction. These are actual observed
failures; no fabricated ticket numbers. Full reports are in target; sanitized summaries go in docs/test-results.md.

## Completion-audit regressions — 2026-11-02

- Credential file replacement/deletion was bypassed by cached access-token reuse: OAuthLifecycleTest.cachedTokenCannotOutliveCredentialReplacementOrDeletion.
- Failed revoke prevented local disconnect: OAuthLifecycleTest.failedRevocationStillRemovesLocalCredential.
- Planner exclusions disappeared at service boundary: DatabaseIT.retentionRemovesOldTerminalDraftsAndDiagnosticsSurviveRoundtrip.
- Partial result used proposed counts without labeling: DatabaseIT.partialReportAndHumanRepairReconcileBeforeAppending.
- Production caching absent: MetadataCacheTest and ProviderTest.cacheHitAvoidsUpstreamCharge.
- Collection pagination absent: ProviderTest.personalReadsAllSourcesWithBoundedPaginationAndTruthfulTimestamps and repeatedPaginationTokenStopsWithinBound.
- Terminal drafts had no retention limit: DatabaseIT.retentionRemovesOldTerminalDraftsAndDiagnosticsSurviveRoundtrip.
- Initial OAuth test encryption seam returned the same byte array that was then wiped; fixed the synthetic protection adapter to return a copy. This was a test defect, not a DPAPI bypass.
- Docker startup failed on a stale Windows runtime socket; preserved/recreated its run directory, with no volume deletion. Test infrastructure failures are not skipped tests.
