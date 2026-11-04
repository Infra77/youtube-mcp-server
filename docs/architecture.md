# Architecture
Existing AI host → SDK MCP stdio adapter → application services → pure domain algorithms.
Services depend on YouTubeProvider, quota ledger, draft store and TokenVault boundaries.
OfficialYouTubeProvider uses fixed Google API origins. FixtureYouTubeProvider never contacts Google.
PostgreSQL stores drafts, grants, write journal and quota ledger. Flyway owns versioned schema.
The separate local CLI performs Google OAuth and interactive proposal approval; it is not a tool.
Windows DPAPI protects credential bytes; token material never enters tool results.
MCP runs synchronously with bounded request sizes. SQL state transitions are short transactions;
remote API operations execute outside transactions. Persist write intent before sending a mutation.
An interrupted/ambiguous write is stopped for reconciliation/manual review, not blindly retried.
Production and fixture accounts are distinct. Fixture mode is explicit and reports synthetic data.
See diagrams and ADRs. No public listener exists except temporary OAuth loopback during consent.
