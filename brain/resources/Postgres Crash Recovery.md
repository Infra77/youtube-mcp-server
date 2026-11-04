---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [NFR-05]
source_urls: ["handbook:chapters-6-and-56"]
---
# Postgres Crash Recovery
## Question and finding
A local SQL transaction cannot roll back a remote YouTube write. Lock state only for short local transitions. Persist remote identifiers and item progress. Concurrent commits must not both create. Leave ambiguous attempts visible after restart.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
