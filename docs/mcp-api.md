# MCP API v1

Transport: stdio using Spring AI 1.1.8 / maintained Java MCP SDK. The host performs initialize,
initialized notification, tools/list and tools/call. No HTTP endpoint or OpenAPI service is provided.

| Tool | Required input | Result / side effects |
|---|---|---|
| get_video_overview | videoInput | Official metadata overview; source label and URL |
| find_similar_videos | videoInput, limit 1–20 | Explained locally ranked candidates |
| find_similar_channels | channelInput, limit 1–20 | Resolved channel and cosine-ranked candidates |
| recommend_for_me | limit 1–20 | Authorized sampled profile recommendations and coverage |
| analyze_my_engagement | none; optionally startA/endA/startB/endB | Aggregates and half-open UTC period comparisons |
| plan_playlist | topic, targetSeconds, maxVideoSeconds, language, maxVideos | Local immutable private draft; no YouTube mutation |
| plan_playlist_from_text | requestText | Parsed draft or NEEDS_CLARIFICATION |
| get_playlist_draft | draftId | Exact proposal, digest, expiry, state and journal |
| commit_playlist | draftId only | Requires local human grant; creates and verifies playlist |
| get_quota_status | none | Local two-bucket ledger; no Google request |

Every tool returns JSON text and structured content: schemaVersion, requestId, asOf, fixture,
status, and data on success. Domain errors set MCP isError=true plus code/message/retryable=false.
An external write may return an ok envelope with data.state PARTIAL/NEEDS_MANUAL_REVIEW; hosts
must inspect this business outcome and must not call it successful creation.

Five resources use youtube-intelligence:// URIs: about, limitations, ranking-method, quota-policy,
playlist-policy. Prompt video_to_playlist_guidance provides the same safety sequence as the product skill.
None contains private collections. Actual generated input schemas are captured by the protocol test.

Error examples: INVALID_INPUT, UNSUPPORTED_CHANNEL_URL, VIDEO_UNAVAILABLE, INSUFFICIENT_PROFILE,
NEEDS_CLARIFICATION, NO_FEASIBLE_PLAYLIST, AUTH_REQUIRED, AUTH_EXPIRED_OR_REVOKED, MISSING_SCOPE,
YOUTUBE_CHANNEL_REQUIRED, QUOTA_BUDGET_EXCEEDED, QUOTA_EXHAUSTED, RATE_LIMITED, APPROVAL_REQUIRED,
DRAFT_EXPIRED, DRAFT_MISMATCH, WRITE_REVIEW_REQUIRED. Errors omit raw upstream bodies and credentials.

Natural-language grammar: `Make a 2-hour English playlist on Fourier transforms, maximum 20 minutes per video`.
Make/Create/Build, hour/minute totals, second/minute/hour maxima and English/Hindi/Spanish/French
are recognized. Other phrasings ask for clarification; the AI host can fill the validated typed tool.

User/account identity, quota configuration and approval are never tool arguments.

## Schema revision 2 additions

Video and channel objects include canonical `url`. Proposal `schemaVersion=2` adds `exclusions` mapping candidate ID to DURATION/LANGUAGE_UNVERIFIED/CAPACITY/replacement reason. No feasible selection returns NO_FEASIBLE_PLAYLIST; no draft is persisted. Every successful envelope retains requestId/asOf/fixture fields.

Commit result: state, draftId, playlistId, playlistUrl (empty in fixture mode), journal, proposedItemCount, proposedTotalSeconds, confirmedItemCount, confirmedTotalSeconds and items[{videoId,url,position,status}]. ATTEMPTED means outcome unknown; NOT_ATTEMPTED means no journaled attempt. Only CREATED plus successful readback establishes complete success. RESOLVED means human reconciliation, not completed creation. Old ambiguous itemCount/totalSeconds summary fields are removed.

Recovery commands are CLI-only: repair requires an existing PARTIAL known playlist and fresh typed fingerprint; resolve records manual resolution. Neither is exposed as a tool. AUTH_PROFILE_CHANGED requires restarting the server after reauthorization. The exact generated input schemas are retained in the protocol evidence, and the daily plan requires export/review in the evaluator host.
