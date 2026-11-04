---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-5]
source_urls: ["handbook:chapters-14-and-56"]
---
# Playlist Approval Invariants
## Question and finding
Persist immutable ordered proposals and canonical SHA-256 digests. Bind one-time approval to account, digest and expiry. Claim creation rights atomically before remote mutation. Journal intent before every write. Ambiguous remote responses require review, never blind retry.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
