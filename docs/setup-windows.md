# Windows setup and reproducibility

Prerequisites: JDK 21, Docker Desktop with Linux containers, Python 3 for local validators, and an
existing MCP client. No Node, frontend, paid model API or GitHub account is needed for this local build.
Obsidian is optional as an editor; open the brain directory as its vault.

The current workspace has a checksum-verified Temurin 21.0.13+9 under `.tools`; scripts discover it.
On another machine install a trusted JDK 21 and set JAVA_HOME. The Maven wrapper pins 3.9.11 and
downloads dependencies on the first build. `.tools/m2` is the project-local dependency cache.

From a PowerShell terminal in the project:

```powershell
.\scripts\start-db.ps1
.\scripts\build.ps1
.\scripts\local-check.ps1
```

Start-db generates `.local/db-password` once and injects it without printing it. Never send this file
to an assistant or put it in source control. Docker binds PostgreSQL only to 127.0.0.1:55432.
`docker compose -f infra/compose.yaml down` stops containers; `down -v` destroys the database volume.
Testcontainers starts separate disposable databases, not that persistent volume.

On this workstation Java's selector failed with `Unable to establish loopback connection` under the
inherited temporary directory. Setting `jdk.net.unixdomain.tmpdir` to the shorter project `target`
directory fixed the actual HTTP tests. Maven test configuration and launch scripts carry this setting.
Keep checkout paths short on Windows. This is a path compatibility fix, not a disabled network test.
For a deeply nested unpacked release, set CURATOR_SOCKET_DIR to an existing short writable temporary
directory before launching (for example your normal Windows temporary directory). Launchers and the
smoke probe honor this override. It changes only Java's internal socket location, not stored user data.

Docker 29 requires a compatible Docker API. Failsafe sets api.version=1.44 for the pinned test client.
If Docker is unavailable, integration acceptance fails; no skip-on-missing-Docker is enabled.

Run `.\scripts\start-mcp.ps1 -Mode fixture` only under an MCP host, or use the smoke harness.
A waiting terminal is expected: stdio servers consume JSON-RPC, not typed chat sentences.
Live setup is separate: see [Google setup](google-cloud-setup.md).

## Quality prerequisites

Run `python -m pip install -r scripts/requirements-quality.txt` and `scripts/install-quality-tools.ps1` once. local-check now starts with a clean package and checks tests, formatting, links, traceability, skill YAML/cases, Gitleaks and MCP smoke. Run `python scripts/quality_pipeline.py --self-test` for coordinator failure reporting. Generate a fresh BOM using `scripts/build.ps1 -Goals @('org.cyclonedx:cyclonedx-maven-plugin:2.9.1:makeAggregateBom')`, then `python scripts/dependency_audit.py` for the networked advisory review.
