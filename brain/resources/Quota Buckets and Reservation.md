---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [TQ-6]
source_urls: ["https://developers.google.com/youtube/data/determine_quota_cost"]
---
# Quota Buckets and Reservation
## Question and finding
The currently read quota calculator separates search calls from general units. Read calls generally cost one general unit; playlist and playlist-item inserts cost 50. Reserve the entire bounded workflow before its first request, including possible reads and writes. Daily reset is Pacific midnight. Actual Cloud Console limits remain unverified.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
