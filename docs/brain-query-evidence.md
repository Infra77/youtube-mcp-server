# Brain-query applied — 2026-10-31
Question: Why stdio, and what changes if we expose /mcp?
Answer: [[MCP Stdio Semantics]] defines a host-launched process and protocol-only stdout.
[[Google OAuth Desktop PKCE]] binds Google access to one locally selected credential, not remote
callers. ADR-0001 chooses that narrower local trust boundary. A hosted endpoint would need a distinct
MCP client authentication layer, user isolation and TLS; Google OAuth alone would not provide those.
[[Codex Project Boundaries]] excludes that expansion. No remote server or PR evidence is claimed.
