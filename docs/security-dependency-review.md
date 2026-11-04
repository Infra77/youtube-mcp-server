# Dependency review — completion remediation

Generate a CycloneDX BOM with the pinned plugin and run scripts/dependency_audit.py. It submits only public Maven package coordinates/versions to OSV and fails on unresolved findings or network errors. Gitleaks 8.30.1 is checksum-verified by install-quality-tools.ps1. Its one scoped ignore is prose in the original extracted handbook, not a credential; generated/private tool folders are excluded from source scans. Release contents must be scanned separately.

The original Boot 3.5.7 dependency tree had advisory matches. Boot 3.5.16 and explicit Jackson 2.21.7, Logback 1.5.34, Log4j 2.25.5, PostgreSQL driver 42.7.12 replace affected versions while retaining Spring AI 1.1.8. See current generated inventory for transitive versions.

GHSA-8jxr-pr72-r468 concerns DNS rebinding of an HTTP MCP server. The shipped server has web-application-type none and stdio true, no web MCP starter. The advisory also explicitly identifies Spring AI as a protected configuration. The scan retains a not-affected disposition only while those transport conditions hold; a remote transport change reopens it. Independent human review of this applicability decision remains required, not silently preapproved.

Source: https://github.com/modelcontextprotocol/java-sdk/security/advisories/GHSA-8jxr-pr72-r468 . OSV API: https://google.github.io/osv.dev/api/ . This is a dated known-advisory review, not a claim of vulnerability-free code. Refresh before release and triage every new finding with evidence; no blanket allowlist.
