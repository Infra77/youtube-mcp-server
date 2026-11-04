---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-5]
source_urls: ["handbook:chapters-8-and-13"]
---
# Language and Duration Metadata
## Question and finding
ISO-8601 duration is parsed to exact positive whole seconds. Unknown or live duration cannot satisfy hard constraints. relevanceLanguage is a search hint, not evidence of speech. Declared audio language is a metadata policy, with an explicit caveat.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
