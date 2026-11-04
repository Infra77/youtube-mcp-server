# Live Google setup — pending user action

No Google project or credentials were available during implementation. Fixture tests cannot complete
this acceptance gate. Do these steps yourself locally; never paste credentials into chat or notes.

1. In one Google Cloud project enable **YouTube Data API v3**. Do not create extra projects for quota.
2. Configure the OAuth consent application and add your dedicated demo account as a test user where
   required. Create an OAuth client of type **Desktop app**.
3. Download its client JSON to a private directory outside this repository. Ensure the Google account
   has a usable YouTube channel. Check the project's actual quota limits and remaining usage.
4. In your own terminal set `GOOGLE_CLIENT_FILE` to that local JSON path and `CURATOR_PROFILE` to a
   simple local profile name, then run:

```powershell
$env:GOOGLE_CLIENT_FILE = 'C:\your-private-directory\desktop-client.json'
$env:CURATOR_PROFILE = 'local-user'
.\scripts\admin.ps1 -Mode live auth login
.\scripts\admin.ps1 -Mode live auth status
```

The login opens Google's own consent page. It uses a temporary loopback callback with state and
PKCE, then verifies the channel within quota. Refresh credentials are stored encrypted by Windows
DPAPI CurrentUser under LOCALAPPDATA/EducationalVideoCurator. Existing credentials are retained if
repeat consent provides no refresh token. No tokens enter the project database or MCP arguments.

Scope: youtube.force-ssl is needed for this product's authorized reads and playlist insert operations.
Testing-mode refresh credentials may expire; reauthorize when told AUTH_EXPIRED_OR_REVOKED.
The installed desktop client is public; its client-secret field is not treated as a confidential server key.

Configure the MCP host to launch the script with `-Mode live` and the same profile and DB environment.
Start with read-only tools. For writes, review the exact proposal and run:

```powershell
.\scripts\admin.ps1 -Mode live approve YOUR_DRAFT_UUID
```

Type the complete displayed approval fingerprint yourself. Approval alone does not create a playlist;
the host then invokes commit_playlist. Live writes are not performed by setup or tests automatically.
Record the actual result and quota cost in a sanitized demo report only after success.

Disconnect with `admin.ps1 -Mode live auth logout` (interactive confirmation). This revokes the
credential and deletes local drafts. `delete-data` deletes local account data while retaining the grant;
it does not delete remote playlists. `cleanup` removes expired uncommitted proposals.

Official references: [desktop OAuth](https://developers.google.com/identity/protocols/oauth2/native-app),
[quota costs](https://developers.google.com/youtube/data/determine_quota_cost),
[playlist-item insert scopes](https://developers.google.com/youtube/v3/docs/playlistItems/insert).

## Disconnect clarification

Logout always attempts local removal, even when Google revocation fails; inspect remoteRevocation. Restart running MCP after login/logout. For unreadable vaults use interactive delete-account-data with the exact channel ID. Do not send client JSON or tokens to any agent. The 16-day plan schedules Google setup early; GitHub credentials do not authorize Google consent.

## Current local setup update — 4 November 2026

The original workstation has completed Google consent and live Codex tool demonstrations. Read [current live evidence](live-demo-status-2026-11-04.md) for scope and remaining checks. The local Desktop client file is now in the workspace parent as desktop-client.json; exclude it from every Git import and handover archive. Historical pending-setup instructions above remain useful for new machines, but do not describe the completed setup on this workstation.
