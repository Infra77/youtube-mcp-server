# OAuth scope review — 2026-11-02

Public search, channels and ID video lookup do not inherently need user delegation; this implementation uses the selected authorized profile for one consistent identity boundary. The initial build does not add a separate API-key credential surface.

| Operation | User delegation | Scope decision |
|---|---|---|
| videos.list(myRating=like) | Required | youtube.force-ssl supports the unified workflow |
| subscriptions.list(mine=true) | Required | same selected profile |
| playlists.list(mine=true), private playlistItems.list | Required for private account data | same selected profile |
| playlists.insert, playlistItems.insert | Required | youtube.readonly cannot authorize writes; youtube.force-ssl is an explicitly supported insert scope |
| channels.list(mine=true) | Required | verifies selected channel before write |

Do not request youtubepartner or unrelated account/email scopes. A separate read-only product would use narrower consent, but the required product includes approved writes. Desktop client secret is not a confidential server credential. Human reviewer must verify the current method pages before live use; document any changed scopes as an ADR and re-consent.

Sources: https://developers.google.com/identity/protocols/oauth2/native-app and https://developers.google.com/youtube/v3/docs/playlistItems/insert ; method index https://developers.google.com/youtube/v3/docs/ . Policies: https://developers.google.com/youtube/terms/developer-policies . Current compliance review is still a release gate; this technical table is not legal signoff.
