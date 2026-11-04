---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-1, FR-2]
source_urls: ["handbook:chapter-9"]
---
# TF-IDF and Cosine Similarity
## Question and finding
Use a shared seed-plus-candidate corpus, smoothed IDF log((N+1)/(df+1))+1, normalized term frequency, and cosine with zero for empty vectors. Stable ties sort by ID. Missing tags must not imply perfect agreement. Weight text, tags, category, duration and language with documented constants.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
