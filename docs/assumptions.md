# Scope and assumptions — handbook step 0
The two client PDFs control requirements. The 53-page handbook controls implementation sequence.
The local project directory is youtube-intelligence-mcp; Maven artifact is educational-video-curator-mcp.
One OS user and one locally selected OAuth account per process. No hosted service or frontend.
Total duration means an upper bound, in integer seconds; return shortfall explicitly.
Language is a strict match against declared audio-language metadata, never proof of spoken content.
Unknown audio language is excluded when a language is required. Maximum 50 playlist items.
Drafts expire in 30 minutes; approval expires in 10 minutes or at draft expiry, whichever is earlier.
Private playlist privacy is the default. Titles, constraints, account, order, duration, expiry and policy
are fingerprinted. Approval is only granted after interactive local review.

Supported live runtime: Windows, Java 21, PostgreSQL 16, with a Windows CurrentUser DPAPI vault.
Fixture runs need no Google credentials; portability of fixture tests does not imply another OS
supports the live credential vault. Stakeholders are the authorized user/account owner, three
student maintainers, assigned human reviewers and the client/evaluator.

Current team workflow supersedes the original local-only phase: one shared repository,
member-owned branches/issues/PRs, actual peer review, staged evaluations and a reviewed final tag.
Prior local AI-assisted work remains explicitly identified as a baseline, not reconstructed
incremental development or human authorship. M2 is htserhsluk; peer review remains M1->M2,
M2->M3, M3->M1 (author->reviewer). Pending gates remain pending until evidence exists.

Historical Google consent, live public reads and two approved native-host creations were observed
on the original workstation on 3 November 2026. See [live handover](live-demo-status-2026-11-04.md).
Those observations are partial evidence, not full live acceptance or consent for this machine.
The authorized account belongs to the original owner's friend; members do not share its vault.

Failure behavior: invalid inputs stop before provider calls; unsupported text requests
clarification; no feasible candidates produce an explicit error; inaccessible personal sources
produce typed failure rather than fabricated completeness. Empty usable profiles are cold start.
Missing event timestamps remain unknown; publication dates are not like/watch timestamps.
Insufficient workflow budget stops before API calls. Missing/expired/mismatched human grants
cannot authorize writes. Partial and ambiguous writes preserve truthful state and require the
documented repair/reconciliation path; no blind retry or false completed playlist claim.

Client obligations and chosen implementation policies are distinguished in the
[source obligation ledger](source-obligation-ledger.md). No scope assumption waives a mandatory
client requirement. The source PDFs stay privately supplied and must not enter public packages.
