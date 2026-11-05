# Handbook amendments — 2026-10-31
Original PDF remains the authoritative supplied handbook; this versioned companion records
implementation-specific adjustments without rewriting client requirements.
1. User-authorized local-only workflow replaces GitHub execution for now. Steps 2 and 5 and
remote portions of 8, 9, 40 and 46 are deferred. Local backlog IDs and checks are real evidence,
but are not mislabeled Issues, PRs, peer review or hosted CI.
2. Folder is youtube-intelligence-mcp; artifact remains educational-video-curator-mcp.
3. Installed Java 25 is not substituted for Java 21. Use a verified project-local Java 21 toolchain.
4. Google Cloud has not been configured. Fixture acceptance proceeds; live stage gates remain pending.
All future algorithm/performance changes require evidence and an ADR before adding them here.

5. Step 31: the regression dataset (20-minute score 1 versus two 11-minute scores .8/.7 under
22 minutes) demonstrates greedy underfill. Implement a single bounded one-for-two local swap;
it improves total relevance and fills this case, while retaining deterministic hard constraints.
See ADR-0009. This is not claimed to solve every knapsack instance optimally.
6. Windows Java selector compatibility: use the short project target directory for
jdk.net.unixdomain.tmpdir. Actual WireMock tests failed with inherited temp paths and passed with
this setting; do not disable network tests as a workaround.
7. Step 32 recovery is conservative: persisted partial/ambiguous writes require manual inspection.
Automatic repair is deferred because non-idempotent Google writes have no safe universal replay key.
8. Quota method costs can be overridden by operator JVM properties curator.cost.read/write/search;
defaults are the verified 1/50/1 catalog. Bounds and charges use the same catalog.

## Completion remediation — 2026-11-02

Supersedes earlier manual-only recovery, single-page sampling and unbounded terminal-draft retention descriptions. ADR-0010 defines generation-bound credentials, unconditional local disconnect, five-minute bounded metadata cache, two-page personal sampling, schema-2 exclusion/confirmed-write results, known-prefix CLI repair, manual resolution and seven-day cleanup. Quality scripts now include real Gitleaks, OSV inventory review, strict skill YAML/cases, traceability and final external evidence gates. Full behavioral skill and live/human acceptance remain real steps in ../plan.md, not claimed historical executions.

## Team execution clarification - M2-S01, 2026-11-05

Items 1 and 4 describe the historical local phase and are superseded for current execution.
GitHub work is authorized through the shared three-member plan; its required PRs, human reviews,
CI, scheduled live run and release evidence cannot be waived by this handbook companion.
Historical Google consent and limited live demonstrations occurred on the original workstation;
see live-demo-status-2026-11-04.md for their limits. They do not authorize other members or prove
all live/host/stage gates. The client PDFs remain authoritative and privately supplied; do not
include originals or extracted source text in public Git imports or release archives.

The current source ledger records exact client page references, all 41 numbered IDs and
unnumbered obligations. Handbook weights, SQL/code examples, technology selections and numeric
bounds are design choices, not new client mandates. Two-developer examples do not replace the
actual three-member plan. Future changes still require the applicable ADR, evidence and review.
