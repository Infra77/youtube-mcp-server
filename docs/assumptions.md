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
The current contributor is Codex acting for the user. Human review and two-person contribution are
pending, not simulated. GitHub, PRs, issues, branch protections and release tags are deferred by user.
Google Cloud is not configured (user confirmed). Live OAuth and live YouTube acceptance remain pending.
