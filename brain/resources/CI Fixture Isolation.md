---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [TQ-5, TQ-7]
source_urls: ["client:SDLC_and_Workflow.pdf"]
---
# CI Fixture Isolation
## Question and finding
Ordinary checks run only with synthetic fixtures. Database behavior needs real disposable PostgreSQL. Protocol tests must launch the packaged stdio server. A fixture result is not evidence of a real YouTube mutation.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
