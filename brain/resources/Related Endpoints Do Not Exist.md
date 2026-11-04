---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-1, FR-2]
source_urls: ["client:Project_1_YouTube_MCP.pdf"]
---
# Related Endpoints Do Not Exist
## Question and finding
The client requirement explicitly says there are no related-video or related-channel endpoints. Compute similarity locally using official metadata. Never describe it as the private YouTube recommendation score.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
