# Maintenance and operator recovery

Run local-check after source/dependency changes. Keep notes, traceability and regression cases current.
Review Spring AI/MCP compatibility, Google endpoint/scope/quota rules and dependency advisories before
upgrading. Re-run packaged protocol discovery after SDK updates. Do not expose this server over HTTP
without a new authorization/user-isolation architecture and ADR.

Use cleanup regularly to delete expired uncommitted drafts. Use delete-data when finished with a
profile; it deletes local proposals/grants/journals, not remote playlists or Google account activity.
Retain only necessary local evidence; this prototype has explicit operator-driven cleanup, not a
background retention service. Review current YouTube retention rules before use beyond coursework.

If a write is PARTIAL/NEEDS_MANUAL_REVIEW or remains CREATING after a crash, inspect its journal
and the account directly. Do not edit approvals or rerun inserts to force completion. Confirm which
remote resources exist, resolve them manually, and obtain a fresh approval for any new proposal.
Abandoned quota reservations are conservatively retained for their quota day; they do not consume
the next Pacific day's ledger. No automatic reset claims actual Google Console usage.

PostgreSQL backup: use pg_dump locally, protect the backup as private user data and exclude it from
source/evidence bundles. Never delete the Compose volume as a troubleshooting shortcut. OAuth
credentials are bound to Windows CurrentUser and require reauthorization on another OS/user.

Future additions need a measured requirement: global optimizer, public metadata cache, richer
pagination, remote authenticated MCP, or additional secure OS vaults. No Redis/Kafka/Kubernetes/UI
is needed for this local assignment.

## Revised retention and recovery (ADR-0010)

The service runs cleanup at startup and hourly; run `admin.ps1 cleanup` before reusing an installation that has been offline. Expired uncommitted drafts are removed, and all draft metadata/grants/journals are deleted seven days after creation. Quota rows older than seven Pacific days are removed. Inspect unresolved writes before the seven-day deadline. Remote playlists are never deleted by cleanup. Local records removed by retention cannot be used to justify replay.

Stop all other writers before recovery. `admin.ps1 -Mode live repair DRAFT_ID` previews the known partial playlist and requires the full REPAIR fingerprint. It checks the remote list is an exact prefix and appends only missing items. A diverged playlist or unknown create ID requires human inspection; `resolve DRAFT_ID` records manual resolution without a YouTube mutation. A crash during repair stays REPAIRING and requires inspection; never force a state with SQL. New operations still require new immutable drafts and approval.

On reauthorization restart the MCP process. Old processes reject changed credential generations. Logout removes local credentials even when network revocation fails, and reports the actual outcome. If the vault is unreadable, `delete-account-data CHANNEL_ID` provides an interactive orphan-data removal path. Revoke a still-active grant in Google's account settings if remote revocation was not confirmed. Keep all credentials and raw private account reports outside repository/evidence.
