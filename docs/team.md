# Team and repository

Repository: https://github.com/Infra77/youtube-mcp-server

| Member | Name | GitHub login | Status |
|---|---|---|---|
| M1 | Aksha Jain (user-supplied branch label) | Infra77 (authenticated and admin verified) | Import in progress; issue #1 |
| M2 | Kulshresth | htserhsluk | Authenticated write access; M2-S01 and AI-assisted import review in progress |
| M3 | Pending member-provided name | abhinavbhatia2006 | Collaborator access verified 6 November; assigned M2-S01 review |

Member 1 requested branch `Aksha Jain`. Git forbids spaces in branch names, so `Aksha-Jain`
is the member's branch in this shared repository, not a separate repository. The current M1-S01
import PR uses that branch as the user-requested exception to the plan's example m1/d01-* naming.
After merge, use short task branches from reviewed main for subsequent packages. Never force-push
main or invent peer identities, author contributions or reviews. The owner chose MIT in the existing
repository; preserve its license. Client-document redistribution permission is separate.

M1 reviews M3, M2 reviews M1, M3 reviews M2. At each review offer the two options in the plan:
human-led review or agent technical analysis followed by actual human inspection and decision.
AI analysis alone does not meet the SDLC human-review requirement. Authenticate via browser login;
never send tokens/passwords to chat. Other members join under their own accounts.

The existing Google authorization belongs to the owner's friend. It is not a shared team credential.
Fixture builds need no Google credentials. A separate authorized account/profile and owner consent
are needed for each intended live use. Never import desktop-client.json or a DPAPI vault.

M2 explicitly requested branch `Kulshresth`. Its first commit is the packaging privacy correction
23fec77, followed by the M2-S01 source audit. While PR #2 is unmerged, the M2 PR is a dependent
review against `Aksha-Jain`, not a claim of a reviewed-main baseline. Final integration and
package completion require the reviewed dependency and M3 review.
