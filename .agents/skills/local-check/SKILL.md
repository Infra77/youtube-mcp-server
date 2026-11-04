---
name: local-check
description: Build, test and launch the local Java server and invoke a read-only MCP tool.
---
# local-check

Research basis: [[CI Fixture Isolation]].

Run scripts/local-check.ps1. It must build the JAR, execute automated tests, launch the fixture stdio server, initialize MCP, discover tools and invoke get_quota_status. Record separate exit codes and PASS/FAIL. Stop and report failures or timeouts, close child processes, and label fixture evidence. Never replace a protocol call with an echo or HTTP health check.

Evaluation cases: evals/local-check/cases.json (repository-relative).
