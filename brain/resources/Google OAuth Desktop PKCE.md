---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-3, FR-5]
source_urls: ["https://developers.google.com/identity/protocols/oauth2/native-app"]
---
# Google OAuth Desktop PKCE
## Question and finding
Installed applications are public clients. Use an ephemeral loopback receiver, unpredictable state, S256 PKCE and browser consent. Keep refresh credentials in Windows-protected storage, separate from model arguments.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
