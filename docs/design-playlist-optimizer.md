# Playlist selection v1
Hard cap is targetSeconds, not an assertion of exact duration. Return shortfall explicitly.
Primary language requests such as en accept en-US/en-GB metadata; explicit region requests such as
en-US require the complete declared tag. Missing or malformed language tags are excluded.
Filter invalid duration, language mismatch/unknown, duplicates and per-video maximum first.
Sort descending relevance then stable ID, add while within time/count caps. Then execute one
deterministic one-for-two replacement pass, choosing the largest positive combined relevance gain
that fits time and item count. At 50 candidates the O(n^3) bound is small and avoids a large dynamic
programming table. The 20 vs 11+11 minute regression now fills the 22-minute target and improves
combined score. This is still a heuristic, not a global optimality claim. Zero topic-text score is
excluded before selection, so a language-matching but unrelated result cannot fill remaining time.
Return NO_FEASIBLE_PLAYLIST when empty, never create an empty success draft.
Fingerprint canonical JSON of immutable account/title/privacy/constraints/order/durations/expiry/version.
The normalized values, source request text and metadata-language caveat appear in the preview.
