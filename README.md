# Educational Video Curator MCP

Java 21 headless MCP server implementing video/channel similarity, personalized recommendations,
honest engagement analysis and human-approved playlist creation through the official YouTube API.
No custom frontend. Existing MCP hosts provide conversation.

**Status:** local review candidate being imported through M1-S01. Google consent and two
approved native-MCP playlist demonstrations have occurred; full team/skill/live acceptance is still
pending. See [test results](docs/test-results.md), [acceptance status](docs/acceptance-status.md),
[team](docs/team.md) and [bootstrap issue](https://github.com/Infra77/youtube-mcp-server/issues/1).
Client PDFs and credentials are intentionally excluded from this public repository.

## Run locally on Windows

Start Docker Desktop, install JDK 21 and Python 3, then open PowerShell in this directory:

```powershell
.\scripts\start-db.ps1
.\scripts\build.ps1
.\scripts\local-check.ps1
```

This workspace already contains a project-local verified JDK and Maven cache. Other machines use
JAVA_HOME. Build output is target/curator.jar. Ordinary tests use fictional data and disposable
PostgreSQL containers, never live Google. The persistent local database listens on 127.0.0.1:55432.

Configure your host to launch scripts/start-mcp.ps1 with `-Mode fixture`. Rehearsal inputs:
`FIXTURE0001`, `@ExampleMath`. Fixture results are explicitly labeled and never provide fake live URLs.
For live use, follow [Google setup](docs/google-cloud-setup.md) yourself; never send credentials to chat.

## Read and inspect

- [Windows setup](docs/setup-windows.md), [MCP user guide](docs/user-guide-mcp-client.md), [tool API](docs/mcp-api.md)
- [SRS](docs/SRS.md), [architecture](docs/architecture.md), [decisions](docs/adr/0001.md), [threat model](docs/security-threat-model.md)
- [Traceability](docs/traceability.csv), [testing](docs/test-plan.md), [defects](docs/defects.md), [versions](docs/versions.md)
- [Second brain](brain/index.md): open brain/ in Obsidian; canonical skills are .agents/skills/
- [Handbook amendments](docs/handbook-amendments.md), [demo](docs/demo-script.md), [maintenance](docs/maintenance.md)
- Detailed learning notes live **outside** this project in ../notes/step 0.md through step 47.md.

Every YouTube write requires the user to review the immutable proposal and type its full fingerprint
in the separate local approval CLI. commit_playlist only accepts the saved draft ID. Partial and
ambiguous writes are journaled and require review; they are never blindly retried.

## Completion remediation and team execution

Start with [current audit disposition](docs/remediation-status.md), [acceptance status](docs/acceptance-status.md)
and [ADR-0010](docs/adr/0010.md). The owner-provided plan.md sits next to the project and contains
16 member steps for each of three real participants (48 packages). It treats the existing code as an
honest baseline, not a fabricated 16-day development history. Original source PDFs are preserved in
docs/reference for portable review; confirm client permission before publishing them publicly.

Run quality tooling setup from docs/setup-windows.md, then local-check. Final acceptance uses
scripts/release_gate.py --final and actual linked evidence; it is not implied by a successful build.

## Current local setup update — 4 November 2026

The original workstation has completed Google consent and live Codex tool demonstrations. Read [current live evidence](docs/live-demo-status-2026-11-04.md) for scope and remaining checks. The local Desktop client file is now in the workspace parent as desktop-client.json; exclude it from every Git import and handover archive. Historical pending-setup instructions above remain useful for new machines, but do not describe the completed setup on this workstation.
