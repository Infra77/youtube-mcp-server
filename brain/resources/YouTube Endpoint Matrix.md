---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [FR-1, FR-2, FR-3, FR-4, FR-5]
source_urls: ["https://developers.google.com/youtube/v3/docs/videos/list"]
---
# YouTube Endpoint Matrix
## Question and finding
Search returns candidates; videos.list hydrates canonical metadata. myRating=like requires authorization. Read subscriptions and playlists separately. Use playlists.insert and playlistItems.insert only after approval.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
