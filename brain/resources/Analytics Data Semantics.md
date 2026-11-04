---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-4]
source_urls: ["client:Project_1_YouTube_MCP.pdf; handbook:chapter-12"]
---
# Analytics Data Semantics
## Question and finding
Liked-video publication dates are not like timestamps. Trends use playlist-item additions and subscription timestamps only. Report sampled coverage, unknown timestamps and unsupported history. Do not infer watch time.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
