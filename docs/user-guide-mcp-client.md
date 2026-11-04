# Use with an existing MCP client

The project provides no custom chat interface. Use an existing host that launches stdio MCP servers.
Configure a command equivalent to:

```json
{
  "mcpServers": {
    "educational-video-curator": {
      "command": "powershell.exe",
      "args": ["-NoProfile", "-File", "C:\\absolute\\project\\scripts\\start-mcp.ps1", "-Mode", "fixture"]
    }
  }
}
```

Replace the absolute path locally; each host's import/configuration mechanism may differ. The launcher
loads the ignored local DB credential and starts the JAR without printing a banner. Start PostgreSQL first.
Default fixture mode is safe for rehearsal and uses only fictional IDs. `FIXTURE0001` and `@ExampleMath`
are example fixture inputs, not real video/channel identities. Every response labels fixture status.

Discover ten tools and five resources. Ask for a metadata overview, similar videos/channels, personal
recommendations and source-aware analysis. The personal results in fixture mode are synthetic.

Ask: `Make a 2-hour English playlist on Fourier transforms, maximum 20 minutes per video`.
The tool returns a private immutable proposal, ordered items, actual runtime, shortfall and fingerprint.
Review every material field. If you want to proceed, run the approval CLI yourself in a terminal:

```powershell
.\scripts\admin.ps1 -Mode fixture approve YOUR_DRAFT_UUID
```

The fixture approval demonstrates the real grant logic but does not authorize any live YouTube write.
Then ask the host to commit that draft ID. A successful fixture result has no real playlist URL.
Live authorization and approval use `-Mode live`; see [Google setup](google-cloud-setup.md).

The commit tool never accepts `confirmed=true` as consent. A replay of CREATED returns the saved
result. PARTIAL/NEEDS_MANUAL_REVIEW are not completed playlists; do not blindly retry them.
For an interrupted attempt, inspect `get_playlist_draft` and the YouTube account directly. The local
journal identifies confirmed items. Resolve uncertain remote effects manually before planning a new
draft; this release deliberately does not implement automatic non-idempotent write repair.

Skills live in `.agents/skills`; a host must explicitly support/import those filesystem skills.
The prompt video_to_playlist_guidance offers the sequence through MCP without claiming universal skill discovery.
