"""Generate the portable, explicit 48-work-package completion plan requested by the owner."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
intro=r'''# 16-day completion plan for three members

Prepared 3 November 2026; updated 4 November 2026 after live Codex/YouTube demonstrations. Day 1 means the team's chosen start date; do not backdate work. There are **16 steps per member, 48 work packages in total**, one package for each of three members every day. `M2-S07` means Member 2, Step 7, on Day 7. The package numbers are NOT the handbook's Steps 0–47.

## Instructions for a new AI agent

The user may say: **"Complete step 7 of member 2. Repository: OWNER/REPO. My GitHub session is authenticated."** Execute M2-S07 below, including the common execution procedure, tests, evidence, commit/PR preparation and assigned review. Do not execute another member's work under this member's identity. Inspect existing evidence first and resume an unfinished package without duplicating issues, branches, PRs or uploads. If it is already complete, verify its actual merged commit/checks and report that result; do not generate cosmetic commits.

You receive this plan and a local `youtube-intelligence-mcp` folder. Locate the folder rather than assuming the original author's Windows username/path. `PROJECT` below means that folder. `WORKSPACE` means its parent. Keep this canonical `plan.md` in WORKSPACE; keep shared execution evidence inside PROJECT so other members can see it through the repository. Original PDFs are copied unchanged into `PROJECT/docs/reference/` to make the folder portable. The user's external `notes/` folder may also be supplied; it is not a dependency for building the program.

Read, in order: `AGENTS.md`; the three reference PDFs; `docs/SRS.md`; `docs/acceptance-status.md`; `docs/remediation-status.md` when present; `docs/adr/0010.md`; `brain/index.md`; this plan's common procedure and your work package. The two client PDFs are authoritative. The 53-page handbook supplies execution and verification steps. Its section/chapter numbers differ from its explicit Steps 0–47. `docs/handbook-amendments.md` records implementation decisions; it cannot waive a client requirement.

## Workable approach: agent execution with required human checkpoints

Use this workflow for every member and every daily package. The agent should perform all authorized automated work and ask for a person's involvement only where an actual requirement, unavailable access or human decision makes it necessary. A package prompt starts the work; it does not itself satisfy human review, Google consent or playlist confirmation.

1. **Member starts the package.** Supply the member number, step number, common repository URL and an already authenticated GitHub session. Example: "Complete M2-S07 using this plan. Repository: OWNER/REPO. My GitHub session is authenticated. Complete all automated work, identify any required human checkpoint, and resume after it is satisfied." Do not send passwords, tokens or OAuth client JSON in chat.
2. **Agent completes the automated work.** Read the context and prerequisites, inspect existing evidence, implement or correct the work, run checks, prepare documentation and evidence, and prepare the issue/commit/PR required by the package. Agents can also configure CI, prepare releases and run independent-machine checks when connected to the appropriate actual machine. Do not ask the member to perform work the agent can already do within its authorization and access.
3. **Agent presents a concrete human checkpoint when necessary.** State the package ID, the exact action needed, why it is required and where that requirement comes from, the prepared artifact or PR to inspect, and the expected nonsecret confirmation. Use `WAITING_FOR_HUMAN` in the execution record. Finish independent substeps while waiting; do not perform work that depends on an approval before receiving it. Do not request credentials in chat or substitute an AI-generated approval for the human action.
4. **The appropriate person acts.** Complete sign-in/MFA/Google consent when needed; inspect the exact live playlist and personally enter its CLI confirmation; or genuinely review and understand the assigned PR and authorize the review outcome. A peer review must come from the assigned other member, not the author's account. GitHub authentication alone does not prove that a person reviewed or understood a change.
5. **Agent resumes and verifies.** Resume the same package without duplicating issues, branches or PRs. Verify the resulting authorization, review/check status or other observable evidence without exposing secrets. Run the remaining checks, address review findings, merge only when the required approvals/checks pass, and record the actual evidence and handoff. Mark the package DONE only when all its completion conditions are satisfied.

### Review choice required at every review checkpoint

This rule applies to all 48 packages, their assigned peer reviews, stage reviews, security/design reviews and final acceptance reviews. Before starting the review, offer the responsible member these two options (reuse a choice already explicitly given for that review):

- **Option A — I will review it myself.** The agent supplies the exact PR/head commit, changed files, relevant requirements, test results and a focused checklist. The assigned human inspects the changes, asks questions and records their decision.
- **Option B — Have the agent review it on my behalf.** The agent performs the technical review, checks the change against all three supplied documents, reproduces relevant checks and prepares detailed findings and a recommended decision. This delegates the technical analysis; the responsible human still inspects the relevant changes and findings, resolves questions and makes the required human review decision before approval/merge.

Suggested agent question: "For this review, would you like to (A) review the changes yourself using my checklist, or (B) have me perform the technical review on your behalf and present the findings for your inspection and decision? Option B still requires your actual review before SDLC human approval can be recorded."

For Option B, read `docs/reference/SDLC_and_Workflow.pdf`, `docs/reference/Project_1_YouTube_MCP.pdf` and `docs/reference/YouTube_Intelligence_MCP_Server_Only_Handbook.pdf`, plus applicable handbook amendments. Identify the relevant source sections, requirement IDs and handbook steps; distinguish client obligations from implementation choices. Inspect the exact diff and affected surrounding code, tests, skills, brain notes and documentation. Check correctness, regressions, security/privacy, quota, approval boundaries and traceability as applicable. Reproduce meaningful tests; report failures, missing coverage and checks that could not run. Produce findings with file/line references, severity, evidence and a suggested fix; explain why each finding matters. Recommend approve/request-changes only for the reviewed commit and explicitly label the report AI-assisted. Re-review affected work after fixes or head changes.

Record the selected option, reviewed commit, AI findings (if used), actual tests, the responsible human's own review outcome and unresolved findings in the package evidence. Until the human has actually inspected the changes/findings and decided, use `AI_REVIEW_COMPLETE / HUMAN_REVIEW_PENDING`, keep the human gate pending and do not merge on that basis. Choosing Option B is not advance approval of unseen work. An agent reviewing its own implementation is self-checking, not independent peer review; the assigned peer remains responsible for the independent review. Never impersonate another member or claim an agent-only analysis was a human review.

**Source constraint:** SDLC Section 6 explicitly says, "A human shall review every AI-generated change in a PR." It also requires members to explain merged work. Thus neither the project document nor handbook can make an agent-only review satisfy that client requirement. If the client formally changes this requirement, record the approved scope change and update the plan/acceptance rules explicitly; until then, preserve the human gate. This review choice does not delegate Google consent, MFA, live playlist confirmation or a client's own acceptance decision.

### Expected human checkpoints

| When | Human involvement | What the agent can prepare or execute |
|---|---|---|
| Day 1, all members | Authenticate accounts, provide the common repository and access to each member's workstation; authorize any permissions the agent cannot already configure. | Repository/bootstrap setup, dependency installation where permitted, permissions configuration, baseline checks and PR preparation. |
| Every day, all members | Read and understand assigned AI-generated changes and provide genuine peer-review decisions. | Diff analysis, test reproduction, review summaries, suggested comments and fixes. The SDLC requires a human to review every AI-generated PR change. |
| M1-S09 and later reauthorization if required | Google sign-in, MFA and account-owner consent. | Cloud/API/OAuth setup through an authorized session, CLI preparation and bounded verification. |
| M2-S09; M1-S12 and M2-S12; later live writes or repairs | Review the exact account, playlist contents and privacy, then personally enter the required approval or repair phrase. | Preview, validation, refusal tests, and creation/readback after valid approval. FR-5 requires explicit confirmation; the current handbook implementation uses a human-operated CLI. |
| Stage reviews and Days 13-16 | Explain the work, participate in demonstrations, and give genuine review/acceptance decisions. | Run demonstrations and independent-machine checks, prepare walkthroughs, collect permitted evidence and reconcile outstanding findings. |

The three client/handbook documents remain authoritative. Completing 48 prompts or reaching Day 16 is not proof of correctness. Final completion means all required functionality, tests, evidence, human reviews and acceptance gates actually pass. If any mandatory condition remains unmet, report NOT COMPLETE with the exact remaining action. Do not remove required human checkpoints merely to make the schedule unattended.

## Current handover update — 4 November 2026

Read this update before executing any package. It supersedes earlier statements that Google setup, authorization and all host demonstrations have never occurred. It does not mark a whole stage or work package complete. See `docs/live-demo-status-2026-11-04.md` for sanitized observations and limits.

### What has actually been demonstrated

- On 3 November, the owner configured a Google Cloud project, enabled YouTube Data API v3, created a Desktop OAuth client and added the intended Google account as a test user. The authorized account belongs to the owner's friend; it is not automatically a shared team service account. The account owner completed browser sign-in/consent; local authorization status and subsequent live public reads succeeded. Refresh credentials use the existing Windows DPAPI CurrentUser vault under the `local-user` profile.
- Codex was configured as the local stdio MCP host with server name `educational-video-curator`, PowerShell `scripts/start-mcp.ps1 -Mode live`, startup timeout 60 seconds and tool timeout 90 seconds. The global configuration is in the current Windows user's `.codex/config.toml`. Initial checks used a direct MCP probe; later calls used the native Codex MCP tools. Native quota status, playlist planning, draft inspection and commit were observed. The full five-skill evaluation has not been demonstrated by these calls.
- Live public overview and similar-video requests succeeded for a Fourier-transform video and a separate entertainment video. Two live proposals were previewed in chat, personally approved in the separate terminal, and committed through the native MCP tool. The server reported `CREATED` with all items confirmed: 11 videos/3320 seconds for Fourier transforms and 10 videos/8366 seconds for number theory for cryptographic engineering. These observations are tool-reported success, not an independent browser check by a reviewer. Private playlist URLs, account IDs and raw private journals are intentionally omitted from shared evidence.
- The first browser-login attempt opened no page. `scripts/admin.ps1` was updated to pass `-Djava.awt.headless=false` only for `auth login`; a retry with a persistent visible terminal succeeded. The causal contribution of the flag versus terminal lifetime was not isolated. The launcher change needs a reproducible regression and inclusion in the next tested release archive; the older ZIP predates it.
- Live selection revealed a quality gap: very short clips (six/eight seconds), an exam-preparation video and metadata/spoken-language uncertainty can pass current bounds. Human approval of those exact demos does not establish that this is a good engineering curriculum. M1/M2/M3-S07 must address relevance and educational usefulness with explicit policy, representative labels and regressions. Do not silently change an approved immutable draft or promise verified spoken English from metadata alone.

### Local credential location and portability

At the user's request, the Desktop client JSON is now copied to `WORKSPACE/desktop-client.json`, outside PROJECT. On the original computer this is `C:\Users\Lenovo_Owner\Downloads\SE\desktop-client.json`. Only its location belongs in instructions; never print or upload its contents. Ignore rules exist in WORKSPACE and PROJECT for desktop-client.json/client_secret JSON and DPAPI files. The original downloaded copy was retained. The local login helper now points to the workspace copy.

Do not include this file when sharing the outer workspace, creating a ZIP or importing the project to GitHub. Git ignore rules do not protect an arbitrary ZIP or file transfer. Each other member supplies an authorized local Desktop client path and signs in separately if live access is needed. Do not copy the friend's DPAPI vault or assume consent transfers between people/machines. Fixture runs require no Google credential. The JSON alone does not authorize a YouTube account.

For an authorized login or renewal on the original machine, from PROJECT run:

```powershell
$env:GOOGLE_CLIENT_FILE = Join-Path (Split-Path (Get-Location).Path -Parent) 'desktop-client.json'
$env:CURATOR_PROFILE = 'local-user'
.\scripts\admin.ps1 -Mode live auth login
```

The account owner completes sign-in and consent. Ask for readiness before starting the short-lived browser flow. Restart/reconnect MCP after changing credentials. Do not log out, revoke, replace the profile or rerun writes just to repeat a completed demonstration without coordinating with the account owner.

### Resume from observations, not assumptions

As of 4 November, the saved Codex configuration still specifies live mode, but the active chat does not expose the server tools. Configuration on disk is not proof that the process or Docker is running. Before a demonstration check Docker/PostgreSQL, reload the Codex MCP connection if needed, and invoke the native read-only `get_quota_status`. A direct protocol probe may diagnose problems, but must be labeled separately from native host execution. Never create a replacement playlist merely because a host connection was restarted.

Reuse the completed setup on this machine when it is valid. M1-S09 now verifies/reconciles existing setup and fills missing lifecycle evidence; it must not blindly create a second Cloud project or client. M1/M2-S12 reuse the historical demo as partial evidence, then complete missing live FR-2/3/4, host/skill and replay checks on the reviewed candidate with consent and a fixed quota budget. Live FR-3/4 access concerns the friend's personal data and requires appropriate account-owner authorization and sanitized evidence.

Still outstanding: independent security/human reviews, all prescribed live lifecycle/negative/replay cases, native full product-skill and stage evaluations, all three independent machines, genuine team GitHub history/PRs/CI, the scheduled live workflow and final release signoff. Keep composite acceptance gates pending until all their parts are verified. The previous 47-test result predates the desktop-launcher fix; do not claim a new full regression or rebuilt archive from these demonstrations alone. All 48 packages and their review choices remain required; inspect existing work and complete missing obligations rather than manufacture duplicate work.

## Product and present state

Build a headless Java 21 MCP stdio server, not a website. An existing AI host supplies chat and invokes tools. Use only official YouTube Data API v3. PostgreSQL 16/Flyway holds immutable proposals, grants, write journals and quota. Google authorization is a separate Windows desktop CLI using loopback, state, S256 PKCE and DPAPI. Never send tokens/client JSON/DB passwords through chat, Git, PRs, evidence or MCP arguments.

FR-1 ranks similar videos from URL/ID. FR-2 ranks channels from URL/handle/ID. FR-3 uses all three authorized signals: likes, subscriptions and playlists. FR-4 reports truthful top channels/categories, duration preferences and source-supported trends/period comparisons. FR-5 accepts topic/time/max-video/language constraints, shows an exact immutable preview and creates a real playlist only after explicit human approval. No watch-history endpoint, first-party related-video endpoint or arbitrary transcript download is available; use metadata-derived overviews and honest unknowns.

Ten tools, five resources and one prompt already exist. Five canonical skills live under `.agents/skills/`: brain-ingest, brain-refine, brain-query, local-check and video-to-playlist. `brain/` is the Obsidian PARA vault with research, index, log and stage retrospectives. Existing code includes quota reservation, deterministic ranking, hard constraints, typed errors and fixture-based MCP tests. Completion remediation adds credential-generation invalidation, local disconnect despite remote revoke failure, bounded account-keyed metadata caching, two-page sampling, exclusion diagnostics, proposed/confirmed result totals, known-prefix partial repair and retention. Inspect current test results; do not assume an earlier 31-test count describes this revision.

The project began as local AI-assisted work. **Do not pretend the upcoming 16 days are the original incremental development history.** The first import is an honest existing implementation baseline. Subsequent commits are real review, fixes, tests, evaluations and acceptance work. Historical notes are retrospective, not evidence that earlier human stage gates took place. All four stages are revalidated in this schedule.

## Inputs, authentication and unavoidable human actions

Each member normally supplies only the common repository URL and an already authenticated GitHub session, plus their member number/step request. Prefer `gh auth login --web`/the OS credential manager. Inspect `gh auth status` without printing token values. Never ask for a raw PAT in chat, insert a token into a remote URL, or copy another member's credential. Infer the account with `gh api user`; verify the remote and permissions before changing anything. Git commit identity must be that real member's verified identity, using their GitHub noreply address when appropriate. The agent may prepare changes as an assistant, but must not impersonate peer authors or reviewers.

On Day 1 record the member-number-to-GitHub-login mapping in `docs/team.md`. The three participants establish this by each running their own Day 1 package; later agents read the mapping. Do not invent absent members. Member 1 is repository/bootstrap and integration lead; Member 2 is domain/UX-contract and documentation lead; Member 3 is quality/security/reproducibility lead. Responsibilities rotate through peer reviews; every member must understand the whole system.

**GitHub credentials do not provide Google authorization or human judgment.** The following remain genuine human actions, even when an agent prepares and navigates everything around them:

- Repository owner grants the other two users access and accepts any organization/branch-protection settings requiring their account privileges.
- A designated owner supplies a Google account/project, accepts any Google terms/consent and signs in locally. The agent can guide or operate authorized setup, but cannot invent an account, complete MFA or consent for an absent person. No additional paid service is required by the application; do not accept charges without authorization.
- The human reviews a real playlist's exact content/account/privacy and personally types the CLI approval/repair phrase. An agent must not type it or generate a live approval in SQL.
- Another human reads/explains AI-generated changes and gives the required peer approval. An agent may analyze and draft review comments; its analysis alone is not the SDLC-mandated human review.
- Each participant has a supported machine and can launch Docker and their chosen AI host. A second directory on one machine is not three-machine reproduction.

Identify these prerequisites on Day 1, not Day 16. When one is missing, finish independent work and record `WAITING_FOR_HUMAN` with the exact action needed. Do not substitute fake evidence or bypass a gate. The schedule completes the project by Day 16 **only if these prerequisites and checks are actually satisfied**. A missed prerequisite moves the completion date; the agent must not declare completion merely because the calendar reached Day 16.

## Source obligations and end state

- Project PDF: FR-1–5; product skill's overview→similarity→preview/confirmation→create→analysis; TQ-1–6; official API, caching, quota, reauthorization and no-channel handling; OAuth/secret/input/injection/privacy tests.
- SDLC PDF: SB-1–6, SE-1–7, five skills, TQ-7/8, every-PR quality gates, real member authorship, reviewed changes, AI session records, four staged deliverable/review packages and final release tag.
- Handbook: explicit Steps 0–47, four stage gates, clean-machine reproduction, source-linked learning, full tool/resource contracts, accountable live demonstration, controlled recovery, policy review and maintenance.
- Completion audit: A1 credential lifecycle; A2 cache; A3 OAuth tests; A4 production provider coverage; A5 skill evaluations; A6 relevance/performance; A7 exclusions; A8 partial counts; A9 retention; A10 quality gates; A11 documentation; B1 Google/live; B2 host demo; B3 independent machine; B4 human/team; C GitHub; D1 recovery and D2 pagination. Every one has an owner and closure package below.

## Common execution procedure — mandatory for EVERY package

1. **Synchronize safely.** Inspect `git status`, current branch, remote, open PRs/issues and `docs/execution/`. Preserve uncommitted user work. If the supplied folder has no Git history, only M1-S01 initializes/imports it. Other members clone the common repository to a separate directory and use their supplied folder only to compare missing artifacts. Never overwrite a remote repository from a stale local copy or force-push main.
2. **Establish task context.** Read the source requirements, package-specific files, dependencies and latest relevant ADRs. Find/create one issue titled `[M?-S??] <work package>` with requirement IDs, acceptance criteria, owner and reviewer. Reuse an existing issue. Link real IDs; never fabricate examples as evidence.
3. **Branch and implement.** Start from current reviewed main on `mN/dDD-short-description`. Keep one reviewable scope. If earlier work already implements the feature, inspect it, add missing tests/docs or verify it with reproducible evidence instead of rebuilding it. Significant changes require an ADR linked to a distilled brain note. Bug fixes require a regression. Do not weaken assertions or skip Docker tests to obtain green results.
4. **Verify.** Execute the package's checks and relevant common commands below. Retain actual exit codes, test counts, commit SHA, tool versions and safe results. Never paste real personal collections into a committed transcript. Source-only docs changes need link/schema checks, not an unnecessary full suite unless an affected contract requires it.
5. **Record learning and evidence.** Write `docs/execution/day-DD/member-N.md` using the template below, update `docs/traceability.csv`, applicable `docs/acceptance-evidence.json` entries and brain/log.md. Each member authors at least one substantive original research/learning note early and later updates it from reviewed findings. Write significant AI sessions with goal, inputs, what worked, failures and human changes. Append detailed external `WORKSPACE/notes/step <handbook-no>.md` when a handbook step changes; shared evidence inside Git remains canonical across members.
6. **Commit and request review.** Inspect the exact diff and run the scanner before staging. Stage only intended source/docs/evidence, never `.local`, `.tools`, credentials, raw account data, build logs or large duplicated release output. Use a meaningful commit such as `test(oauth): reject profile replacement during cached access [M1-S05]`. Use a body file for multiline PR descriptions. Open a draft/ready PR with problem/result, requirement/issue/ADR/note links, actual validation, quota/security effect and unresolved limits. Request the assigned peer. Do not self-approve or merge while checks/review fail.
7. **Perform the assigned peer review.** Offer Option A (human-led review) or Option B (agent technical review on the human’s behalf, followed by actual human inspection/decision), as defined above. M1 reviews M3's work, M2 reviews M1's, and M3 reviews M2's. Inspect source and tests, reproduce meaningful checks, explain the design and record findings. The human operating the reviewer account must actually review and authorize the approval; agents must label AI-assisted findings honestly. Authors fix requests, then reviewers recheck the new head. On Day 1 M1 returns in the review window to review M3; do not leave it until Day 2.
8. **Merge and hand off.** Once required human approval and all checks pass, merge with a history policy preserving real authorship, close the issue and update links in evidence. Rebase/update conflicting branches and rerun affected checks. Record merged SHA and remaining dependencies. Do not claim a package `DONE` while its PR is unreviewed or its mandatory evidence is absent.

The user invoking a package authorizes its described repository work on the provided repository, including issues, branches and PR preparation; it does not authorize bypassing protections, deploying a public service, sharing credentials or impersonating another participant. If the repository has existing policies, obey the stricter applicable reviewed policy. Keep public publishing and real writes subject to their specific consent boundaries.

## Daily schedule and dependency rule

Use a common six-to-eight-hour workday: first 30 minutes sync/issues; about three hours implementation/evaluation; one-to-two hours verification/evidence; final two hours reciprocal human review/fixes/merge. All three work every day. M1→M2→M3 is the default merge order when their work touches shared files; independent branches may run concurrently. A package depending on an unmerged artifact reads the PR for review but waits for its reviewed merge before building a new final baseline. Reserve Days 14–15 for defects and rehearsals; release is not the place to hide unfinished fixes.

## Standard commands (PowerShell, from PROJECT)

```powershell
git status --short
gh auth status
gh api user --jq .login
python -m pip install -r scripts/requirements-quality.txt
.\scripts\install-quality-tools.ps1
.\scripts\start-db.ps1
.\scripts\build.ps1 -Goals @('-B','-ntp','clean','verify')
.\scripts\build.ps1 -Goals @('spotless:check')
.\scripts\local-check.ps1
python scripts/validate_docs.py
python scripts/validate_traceability.py
python scripts/validate_skills.py
python scripts/quality_pipeline.py --self-test
.\scripts\build.ps1 -Goals @('org.cyclonedx:cyclonedx-maven-plugin:2.9.1:makeAggregateBom')
python scripts/dependency_audit.py
python scripts/release_gate.py
python scripts/release_gate.py --final
```

The last command is expected to fail until all external evidence is genuinely complete. Current scripts evolve during this plan: if a command is defective, fix it through its owning issue and regression, do not edit the report to PASS. On Linux CI use the Maven wrapper/appropriate shell and no DPAPI live credentials. Do not assume a Windows .exe scanner runs on Linux; install a pinned native build with verified checksum. All fixture CI is credential-free; network access for dependency downloads/advisory updates is separate from denying live Google API/OAuth calls during tests.

## Evidence template

Every `docs/execution/day-DD/member-N.md` must contain: package ID; real author/reviewer logins; timestamp/timezone; input commit; requirement and handbook-step IDs; files read; concrete changes/findings; command/exit-code/test table; synthetic/live distinction; source citations; issue/PR/check URLs; merged commit; human review outcome; nonsecret quota counts if live; failed attempts and regressions; remaining blockers; next package. Mark facts as OBSERVED, IMPLEMENTED or PENDING rather than treating planned work as executed. Do not record access tokens, email addresses, raw private playlists or private collection contents. Store an allowed demo playlist URL only with owner consent; otherwise store a redacted verification record and private evidence locator.

## Day 16 coordination — avoid circular approvals

Day 16 packages have three phases and must be resumed as peers finish. First M1 prepares the frozen release candidate and release PR **without tagging or publishing**. M2 demonstrates that exact candidate and records pre-release human acceptance; M3 independently audits it and records pre-release go/no-go. All three complete reciprocal reviews in the shared review window. Then M1 merges the reviewed release metadata, checks the final gate and publishes the tag/assets. Finally M2 and M3 verify the published tag/assets and append post-release evidence in a documentation-only follow-up PR. No member waits for the final published tag before performing the pre-release review. No member's package is DONE until its post-release obligations finish. The release signoff gate refers to actual pre-release approval of the frozen candidate; tag/asset evidence is added after publication without rebuilding or silently replacing tagged binaries.

## Four submission gates

Stage 1 closes at end of Day 3: reviewed requirements, PARA/index/log, >=10 sourced ingest notes with all three real authors represented, AGENTS, issues and genuine green baseline CI; skill evaluations recorded.

Stage 2 closes at end of Day 6: reviewed architecture/diagrams/ADRs/contracts/database/security/quota, actual refine/query use, local-check v1 and evaluations.

Stage 3 closes at end of Day 11: all FRs through MCP, full required negative/provider/OAuth/DB tests, all five skills evaluated, regression log, green CI, separate live workflow and stage review. Live credentials are never needed for PR CI.

Stage 4 closes at end of Day 16: all live/client/product/local-check/brain-query demonstrations, three-member understanding and independent reproduction, full traceability, compliant reviewed final package and actual release tag. At each gate rerun the available skills in the supported host with stage-specific positive and negative evidence; do not simply copy the prior stage's report.

## Work packages
'''
# day, member: (title, requirement mapping, focus, concrete actions, validation, completion)
days=[
[
('Repository and identity bootstrap','SB-4/5/6, SE-4/5; handbook 0–5, 8–9','AGENTS.md; README; .gitignore; docs/reference; docs/team.md',
'Inspect the supplied repository URL before modifying it. For an empty repo create an honest existing-implementation import branch, retain the original documents subject to client sharing rights, and scan the import. Establish main and invite/verify the other two actual accounts; record member mapping as they join. Configure PR-only changes, at least one peer approval, stale-approval dismissal, required checks once named, no force-push/deletion and restricted Actions permissions. Create four milestones and requirement/security/skill/bug labels. Start Google prerequisites now: identify one project owner, dedicated demo account and a usable YouTube channel; record setup actions needed, never credentials.',
'Authenticated user/remote match; staged secret scan; branch-rule/API evidence; baseline builds or a specific setup issue. Review M3-S01 after its PR exists.',
'One real import PR, explicit pre-existing-code provenance, team mapping started, protected workflow configured without inventing historical commits.'),
('Source contract and scope review','FR-1–5, SE-1, SB-1; handbook 0, 6–8','All three PDFs; docs/SRS.md; docs/assumptions.md; docs/traceability.csv',
'Read all 58 original pages and inventory every FR/TQ/SB/SE/SK/NFR. Verify distinctions between mandatory client requirements and handbook design examples. Compare current SRS with the source; retain acceptance conditions for exact preview, confirmation, all three personal sources and honest temporal data. Document stakeholders, supported Windows scope, upper-bound runtime, declared language and known failure behavior. Create audit closure issues A1–A11/B1–B4/C/D1/D2 mapped to real backlog IDs. Review the baseline import in M1-S01 with the human and flag anything not understood.',
'Source page references and 41-ID matrix checked; no silently dropped obligation; docs/link checks pass.',
'Reviewed requirements diff and exhaustive obligation ledger, not a generic project proposal.'),
('Independent workstation and baseline inventory','NFR-06, TQ-1–4, SE-7; handbook 1, 3, 19–20, 44','README; setup-windows; build/local-check; pom.xml; evidence',
'Clone the common repo independently with your own identity; never reuse the author’s .tools/.local. Install Java21/Docker/Python/Obsidian/quality tools from trusted sources and verify versions. Open only brain/ as the Obsidian vault. Start a new database volume, run clean verify and local-check, and record actual failures. Compare tool/resource discovery with docs. Inventory current test coverage and outstanding audit items. Review M2-S01 and explain one FR acceptance criterion in your own words.',
'Fresh-machine commands and versions recorded; no real Google credentials; failures get issues rather than skipped tests.',
'Independent baseline report and reproducibility fixes if needed; genuine member-authored learning note.')],
[
('Real issue board and traceability migration','SE-4/5, SB-1/5, TQ-8; handbook 5, 8','docs/development-plan.md; traceability.csv; validate_traceability.py',
'Create/reuse issues for all 48 packages and audit closures with requirements, acceptance, owner, dependencies and milestone. Replace local L identifiers with a preserved local-ID column plus actual issue URLs; never discard provenance. Teach the validator development versus final modes: valid reviewed PR URLs accepted, unresolved mandatory evidence rejected only at final gate. Check duplicate/missing IDs and actual test methods, not file existence alone. Document branching, review rotation and merge policy. Review M3-S02.',
'Validator tests for missing ID, missing path, invalid/fake URL and unresolved final status; current development matrix passes.',
'Usable issue board and traceability capable of representing genuine GitHub evidence.'),
('Ten-source research and source-grounded SRS','SB-1/3/6, SE-1, SK-01; handbook 6–7','brain-ingest skill; brain/resources; SRS; source notes',
'Invoke brain-ingest in the supported agent host, not a script that writes predetermined answers. Review the existing 14 notes against their cited sources; refresh changing technical claims from official documentation. Ingest at least three new useful sources including one missing author/date; preserve unknown provenance and log each run. Ensure every team member authors or substantively revises at least one research note through their own PR. Draft concrete success/misuse acceptance cases for each FR and skill from notes. Review M1-S02.',
'At least ten genuine sourced notes total; no fabricated authors/dates; YAML/wikilinks pass; ingest positive/refusal transcript retained.',
'Reviewed research and SRS, with actual skill use and human contributor evidence.'),
('Credential-free PR quality pipeline','TQ-1–5/8; SDLC CI; handbook 9, 17, 40','pom.xml; scripts/quality_pipeline.py; validators; .github/workflows/ci.yml',
'Create real PR and main-push CI on a runner with Docker. Pin actions by verified commit SHA, restrict permissions, install Java21 and required Python/scanner tooling. Run build, formatting, tests including Testcontainers and packaged MCP, audited secret scan, strict skill and brain validation, traceability and artifact publication. Keep Google credentials unavailable and explicitly deny Google API/OAuth network during test execution while allowing loopback/container tests. Add dependency advisory review as a separate networked job. Avoid pull_request_target executing untrusted PR code with secrets. Review M2-S02.',
'Run workflow on a real PR; retain successful checks and intentional-failure evidence in a disposable branch; validate that negative tests cannot reach Google.',
'Real CI skeleton/gates, not an unexecuted YAML file. Report runner limitations honestly and fix them.')],
[
('Stage 1 security and authorship review','SB-5/6, AI policy; handbook Stage 1 gate','Import diff; team.md; notes; Git history; SRS',
'Inspect all imported secret-sensitive paths and source/fixture data. Verify three distinct real commit identities and substantive note contributions. Confirm every merged change has a human peer review. Demonstrate the human lead can explain account/token/channel/MCP identity and why a model-confirmed boolean is insufficient. Resolve baseline review defects with regressions where code changes. Review M3-S03 and check stage evidence comes from actual runs.',
'Gitleaks source/history scan; human review log with code locations and questions; unresolved security issues remain open.',
'Reviewed baseline and truthful contributor history; no fake daily or retroactive commits.'),
('Stage 1 skill evaluations and requirement freeze','TQ-7, SK-01–05, SE-1; handbook 6–9, Stage 1 gate','evals; skills; SRS; docs/evidence/stages/stage-1',
'Run all five available skills against an isolated checkout in the selected skill-capable host. At minimum cover real ingest/unknown-source refusal, refine/link preservation, grounded/unsupported query, local-check success/failure and fixture product approval boundary. Capture what the agent actually did, not only its instructions. Repair skills/cases for observed failures. If a host cannot import skills, choose a supported one for skill evaluations; MCP prompt equivalence alone is not skill discovery evidence. Review M1-S03.',
'Per-case inputs, tool/file traces, forbidden-action checks, host/version and verdict; no main-vault pollution.',
'Actual Stage 1 evaluations and a reviewed SRS acceptance baseline.'),
('Stage 1 submission gate and retrospective','SB-2, TQ-7; SDLC Stage 1; handbook chapter 32','Stage 1 Review; acceptance-evidence; traceability; CI',
'Audit M1/M2 outputs against the Stage 1 checklist: protected repository, authorship, ten sourced ingest notes, PARA/index/log, reviewed SRS, AGENTS, issue board and green PR CI. Review M2-S03, independently spot-check evaluation outputs and source citations. Write a new dated Stage 1 revalidation record distinguishing original retrospective work from current team review. Update only gates actually satisfied, with real URLs. If a required gate fails, assign it immediately and hold stage submission.',
'All stage artifacts accessible at one reviewed commit; validation and hosted checks pass; three members acknowledge understanding.',
'Signed current Stage 1 bundle with exact commit and no unresolved mandatory entry.')],
[
('Architecture, deployment and database design review','SE-2/3/6; handbook 10–11, 14','architecture.md; diagrams; V1/V2 migrations; provider/vault/store boundaries',
'Review the complete host→stdio→service→provider→YouTube flow, separate CLI, DPAPI and Postgres boundaries. Check architecture/class/sequence/ER/deployment diagrams match actual classes and states including recovery. Test blank-database migrations and migration replay; never edit a released historical migration to hide a defect. Document schema invariants and local trusted-user boundary. Use a brain-query response to draft an ADR amendment grounded in actual notes. Review M3-S04.',
'Editable diagrams render; migration tests pass; every ADR cites a relevant distilled note.',
'Reviewed architecture and persistence contract including recovery/retention semantics.'),
('MCP schemas and result contract','FR-1–5, SE-7, NFR-03/10; handbook 13, 25, 33','CuratorTools; Models; KnowledgeResources; mcp-api; protocol tests',
'Export exact tool input schemas, resources and prompt metadata through a real MCP client. Document required/optional fields, bounds, response envelopes, canonical URLs, exclusion reasons, partial counts, error codes and fixture caveats. Add assertions for correct schema names, not only the number of tools. Verify resources/read and prompts/get, no secrets/private collections, and no tool accepts account/token/approval overrides. Check old persisted schema handling and document breaking output changes. Review M1-S04.',
'Contract fixtures and versioned schema reference agree with actual packaged process; malformed/unknown arguments fail safely.',
'Usable developer and host contract with success/error examples and compatibility evidence.'),
('Independent threat and scope review','Security, NFR-01/07, SE-3; handbook 17, 19, 43','threat model; oauth-scope-review; ADR-0010; dependency review',
'Review least privilege method-by-method against current official pages. Inspect OAuth redirect/state/PKCE, local file permissions, scope validation, credential-generation binding, SQL parameterization, host allowlists and logs. Threat-model metadata injection, cross-account access, cache isolation, malicious PRs and partial writes. Verify the HTTP-only MCP advisory disposition against actual stdio configuration; reopen it if transport differs. Write tests/issues for concrete threats and an original security note. Review M2-S04.',
'Threat-to-control-to-test table; scoped dependency dispositions with source/date/reviewer; no blanket scanner suppression.',
'Reviewed security design and explicit remaining issues rather than an unsupported safety claim.')],
[
('OAuth lifecycle and local privacy regressions','A1/A3, TQ-2/4, NFR-01/07; handbook 24, 37, 39','WindowsTokenVault; AdminCli; OAuthLifecycleTest',
'Inspect and extend the local fake OAuth exchange tests: cached-token replacement/deletion, consent denial, callback path/method/state/duplicate params, expiry refresh, invalid_grant, missing scope/refresh credential, corrupted vault, save failure, network failure and logout cleanup. Verify production DPAPI on Windows using only synthetic credentials and preserve existing user data. Ensure orphan-account deletion is interactive and token values never enter errors/logs. Fix actual failures before live use. Review M3-S05.',
'OAuth lifecycle tests execute without Google; native vault tests on supported Windows; log redaction assertions and state mismatch no-write checks.',
'Credential lifecycle reviewed and tested end-to-end locally, not just helper functions.'),
('Selection, preview and canonical draft design','A7/A8, FR-5, TQ-1; handbook 15, 30–32','Models; PlaylistSelector; DraftStore; CuratorService; optimizer docs',
'Verify total-as-upper-bound and exact-language policy, max counts/durations, unknown/live metadata, duplicates and deterministic ties. Confirm exclusions survive service persistence and MCP serialization. Check canonical digest includes every material choice and sorted exclusion map. Old draft bytes must not be silently rehashed/reapproved. Add tests for changed title/privacy/order/expiry, zero candidates and large/ambiguous natural-language numbers. Confirm partial results enumerate proposed versus confirmed videos. Review M1-S05.',
'Boundary tests and exact stored/reloaded proposal checks; no successful empty draft or implicit relaxation.',
'Auditable proposal and response contract ready for human review.'),
('Quota, cache and retention design verification','A2/A9, TQ-6, NFR-04/07/09; handbook 14, 16, 23','QuotaService; CostCatalog; MetadataCache; RetentionJob; maintenance',
'Review full worst-case plans including two-page sampling, repair reads/writes, auth channel verification and cache misses. Verify atomic two-bucket reservation under concurrency and Pacific-day change. Test cache TTL/cap/account separation, no personal collection caching, zero charge on cache hits and conservative preflight behavior. Verify seven-day retention for all draft states, startup/hourly cleanup and immediate deletion; protect unresolved-write safety and operator notification. Test cleanup versus an active workflow before expiry. Review M2-S05.',
'Actual cost/request assertions and DB concurrency tests; retention tests cover each state/cascade and old quota rows.',
'Quota/cache/retention contract consistent with docs, tests and policy review.')],
[
('Actual brain-refine and brain-query design workflow','SK-02/03, SB-1/3, TQ-7; handbook 12','brain inbox/resources; skills; ADRs; evals',
'Use actual brain-refine to deduplicate/move Stage 1 notes in an isolated branch, preserve sources and repair backlinks. Use brain-query to explain stdio versus remote HTTP and draft a design ADR; compare its claims with source notes. Include conflicting-note and missing-evidence cases. Keep before/after diffs and host traces, then submit reviewed changes to the real vault. Review M3-S06 and test the relevant design walkthrough yourself.',
'Real workflow artifacts, no fabricated citations, link validation and reviewer-edited ADR.',
'Demonstrated use of the brain as a design tool, not just a collection of files.'),
('Local-check failure paths and Stage 2 skill runs','SK-04, TQ-7; handbook 18, 35, Stage 2 gate','quality_pipeline; smoke.py; local-check skill; stage-2 evals',
'Run local-check on a fresh fixture checkout and exercise failing build, missing tool, startup timeout and nonprotocol stdout using isolated test variants. Assert overall FAIL/nonzero exit, later phases NOT_RUN and child termination; distinguish coordinator unit tests from actual skill-run behavior. Evaluate all five skills again at Stage 2 with the updated design, recording each positive/negative outcome. Improve scripts/skill instructions when evidence shows confusion. Review M1-S06.',
'Bounded negative runs and cleanup verified; five-step successful report; stage-specific host transcripts.',
'Evaluated local-check v1 and genuine Stage 2 skill evidence.'),
('Stage 2 design review gate','SE-2–7, SB-2, TQ-7; handbook chapter 42','Stage 2 Review; diagrams; contracts; traceability',
'Review M2-S06. Assemble architecture/ER/sequence/deployment, ADRs, interfaces/schema, threat/scope/quota/retention plans and refine/query/local-check evidence. Require each member to draw/explain the process and approval boundary to another member. Resolve review issues in small PRs, ensure CI is green and create dated Stage 2 revalidation with real authors/reviewers. Update gates only after checking artifacts at the reviewed commit.',
'No missing design artifact or unresolved critical security assumption; actual skill runs referenced.',
'Signed Stage 2 bundle and clear handoff into implementation verification.')],
[
('FR-1 production ranking and explainability','FR-1, A4/A6, TQ-1–3; handbook 26, 36–38','Ranking; CuratorService.similar; ProviderTest; labeled fixtures',
'Review candidate generation and hydration, excluded seed/deleted IDs, duplicate handling, normalized feature components and stable ties. Extend labeled cases with educational near-matches, keyword spam/popularity distractors and missing tags/categories/language. Measure precision@k with recorded expected labels and test the same expectations through MCP. Ensure cached data cannot misrepresent freshness and result links are canonical. Review M3-S07.',
'Exact ranked expectations and zero-write assertions; measured relevance results with labels independently reviewed.',
'FR-1 accepted on fixture contracts and ready for the later live check.'),
('FR-2 and personalized ranking quality','FR-2/3, A4/A6, TQ-1–3; handbook 27–28','channel parser/search; recommend; profile weighting; fixtures',
'Verify URL/handle/raw-ID resolution, unsupported legacy aliases and accurate channel hydration. Add labeled channel similarity cases. For recommendations assert each of likes/subscriptions/playlists changes the profile, duplicate known videos are excluded, cold start is explicit and source coverage/truncation is truthful. Test missing/inaccessible sources as typed failure or explicitly reviewed reduced coverage. Add personal weighting and deterministic tie tests. Have another member inspect labels rather than calling synthetic labels a user study. Review M1-S07.',
'Channel and personalized result assertions through MCP plus provider HTTP contracts; quality threshold and limitations documented.',
'FR-2/3 algorithms have relevance evidence beyond nonempty result checks.'),
('Benchmark and independent label review','A6, NFR-02/03, TQ-1; handbook 15, 36, 47','RankingEvaluationTest; design-ranking; benchmark evidence',
'Review M2-S07 and independently inspect all video/channel/profile labels. Record disagreements and update expected labels by reasoned human consensus, not to match output. Run representative 50-candidate ranking/selection repetitions with machine specs, warmup policy and actual timings. Add high-noise/long-description and input-order permutations. Confirm no provider calls occur in inner scoring loops. Compare requirements with measured outcomes and fix inefficient or misleading behavior.',
'Precision@k and timing report tied to commit and machine; threshold failures open defects, not adjusted silently.',
'Reviewed quality/performance baseline and explainable algorithm limitations.')],
[
('Official provider HTTP contracts and pagination','A4/D2, SE-6, TQ-2/4; handbook 22, 37','OfficialYouTubeProvider; ProviderTest; quota plans',
'Cover every production endpoint with WireMock: video IDs/batches, search, handle/channel lookup, likes, subscriptions, playlists/items, insert playlist/item, account verification and readback. Assert exact parameters, scoped headers without logging values, response mapping, omitted deleted IDs, malformed JSON and errors. Exercise second page, repeated token, item cap and truncated coverage. Keep every extra call within preflight. Verify no arbitrary origin can come from a tool input. Review M3-S08.',
'All endpoint contract tests and full-workflow call counts; no Google access; unknown upstream fields handled safely.',
'Production adapter verified separately from fixture E2E.'),
('FR-4 analytical correctness and natural language','FR-4/5, A4/A7, TQ-1/3/4; handbook 29–31','Analytics; parser; MCP tests; design-analytics',
'Use a known fixture with likes, subscriptions and playlist-added events across two periods. Assert exact top counts, category counts, medians/bins, unknown timestamps and comparisons; distinguish unavailable from zero. Test all-or-none date arguments and invalid ranges with no provider call. Verify text grammar success and ambiguity behavior and that normalized constraints appear in preview. Do not infer watch/like dates from publication. Review M1-S08.',
'Exact analytics through MCP, no false history, no silent constraint defaults or mismatched parsing.',
'FR-4 and text-planning acceptance evidence with understandable data coverage.'),
('Injection, validation and privacy adversarial review','TQ-4, NFR-01/08, A3/A4; handbook 19, 39','Input; CLI display; tool schema; fixtures; logs',
'Review M2-S08. Test hostile video titles/descriptions, terminal controls, oversized/Unicode inputs, deceptive hosts/userinfo/ports, malformed channel IDs, unknown tool parameters and forged confirmed/account/token fields. Inject a synthetic secret into an exception and assert it is absent in stdout/stderr/MCP artifacts. Confirm scripts sanitize evidence and fixtures contain no real user data. Check local approval displays every material field and cannot be invoked as an MCP tool. Add regressions for actual findings.',
'Adversarial tests fail closed with zero unauthorized writes; safe typed errors and log assertions.',
'Reviewed input/injection/privacy boundary, not merely a scanner PASS.')],
[
('Google project and real OAuth bootstrap','B1, FR-3/5, handbook 1, 24, 43','google-cloud-setup; scope review; CLI; private local credential location',
'Using the designated owner’s authorized browser/session, configure one Cloud project, enable YouTube Data API v3, consent/test users and Desktop OAuth client; confirm channel availability and actual quota buckets. Ask the human only for sign-in/MFA/consent actions that cannot be delegated. Keep the downloaded JSON outside the repo. Run real CLI login/status, a bounded public read, refresh/re-login and revoke/local deletion checks. Reauthorize if needed for later tasks; restart MCP after credential changes. Record method/status/quota and redacted identity proof, not tokens or account collections. Review M3-S09.',
'Real browser consent and account binding; no-channel/expired-token behavior covered by fixtures plus real lifecycle observations where feasible.',
'Verified authorized live account and safe local credential lifecycle; historical approved writes are recorded separately, with no unnecessary new write in this package.'),
('Human approval and exact-draft verification','FR-5, A7/A8, NFR-05; handbook 31–32','AdminCli; DraftStore; proposal/approval tests',
'Review the actual terminal preview with a human: account, privacy, title, every ordered URL/duration/language, exclusions/shortfall, expiry and digest. Test wrong/expired/mismatched grants, cross-account attempts, replay and concurrent claims against real disposable PostgreSQL. Verify no database transaction spans network calls. Recheck schema-1 compatibility and schema-2 canonical fingerprints. Prepare the exact real playlist preview procedure for Day 12; do not authorize it yourself. Review M1-S09.',
'Tests prove one-use binding and no provider writes without the grant; human confirms preview is understandable.',
'Approval boundary independently reviewed and ready for controlled live acceptance.'),
('Scheduled live test isolation and fixed budget','TQ-5/6, C; handbook 17, 40','CI; live workflow; quota config; selected dedicated runner',
'Create a separate scheduled/manual workflow for bounded read-only live checks on a dedicated secured runner/account. Never run it on PR events or untrusted branch code. Prefer a maintained Windows runner using its local DPAPI profile; do not publish refresh tokens to generic hosted CI. Set a small explicit per-run budget, reserve before any call, serialize runs and produce sanitized status/quota evidence. Add a deliberate zero-budget test proving zero provider calls. If credentials/runner are not ready, keep fail-closed and open the blocker; do not call a disabled workflow completed. Review M2-S09.',
'Trigger a real controlled run after M1 setup; demonstrate fixed-budget rejection; scheduled trigger configured with a recorded next run and actual subsequent evidence before final release.',
'Separate live workflow with actual execution evidence and no credential exposure or write automation.')],
[
('Partial writes, reconciliation and recovery','D1, A8, FR-5, NFR-05; handbook 32, 39','repair/resolve CLI; CuratorService; write journal; DatabaseIT',
'Test failures before create, lost create response, item failure, lost item response, crash states and mismatched readback. Known partial repair must require a fresh human phrase, atomically claim, verify identity, read remote order and append only the missing approved suffix. No known ID means no blind retry. Reject non-prefix/foreign/active state. Test repeated repair and competing attempts. Verify manual resolution never claims completed creation. Document stopping other writers and the seven-day evidence deadline. Review M3-S10.',
'Fault-injection tests and exact remote mock call counts; no duplicated playlist/item; safe truthful partial statuses.',
'Recovery implementation and operator playbook accepted, or a documented unresolved defect blocking release.'),
('Product skill complete workflow in actual host','SK-05, TQ-7, FR-1/5; handbook 34–35','video-to-playlist skill; host config; eval cases',
'Import/invoke the actual skill in a supported agent host with the fixture server. Capture overview caveat, similar videos, constraints, exact preview, genuine approval stop, fixture-only test grant, commit/readback and short analysis. Test injected confirmation, insufficient quota and no-channel cases. Ensure the host never runs the human approval command. If the host only supports prompts, demonstrate the prompt but separately use a skill-capable host for required skill evaluation. Refine instructions based on actual behavior. Review M1-S10.',
'Ordered host trace and user-visible result inspected; no fake live link; positive and forbidden-behavior cases pass.',
'Product skill behavioral evidence, beyond reused JUnit calls.'),
('Clean-package and retention/deletion verification','A9, B3, NFR-06/07; handbook 42, 44, 47','package scripts; retention tests; local deletion; source scan',
'Review M2-S10. Build and extract a fresh package to a clean directory without copied credentials/cache. Verify checksums, launchers, required scripts and README-only setup. Test migrations on an empty volume, actual MCP discovery/resource reads and safe read-only calls. Test all retention/deletion states including unreadable local credential recovery, and verify private data does not enter ZIP. Ensure packaging clears or recreates staging safely so removed files cannot survive in a later archive. Document any required tools or path-length settings.',
'Extracted-package source and binary checks; scanner on package, no secrets; retention/recovery evidence preserved safely.',
'Portable candidate and reviewed deletion/retention behavior.')],
[
('Full regression matrix and defect closure','TQ-1–6/8, A3/A4/A10; handbook 36–40','test-plan; defects; CI; test reports',
'Map each prescribed negative case to a named assertion: malformed IDs, private/deleted, missing tags, quotaExceeded, signup required, token expiry/revocation and rate limits. Close uncovered production paths and add regressions for significant defects. Run clean fixture tests through all layers including actual MCP. Verify concurrency and quota no-call assertions, not merely exception presence. Record exact counts and no unintended skips. Review M3-S11.',
'Full reviewed test matrix and green CI at the current head; unresolved defects retain owners and block affected requirements.',
'Stage 3 test evidence is comprehensive and current.'),
('Stage 3 all-five-skill evaluation','TQ-7, SK-01–05, SB-2; handbook 41','stage-3 eval directory; skills; actual host',
'Run all five skills at the Stage 3 candidate in an isolated checkout with a positive and negative case each. Use the concrete eval JSON scenarios, real agent execution and independently inspected output. Include actual local-check failure/timeout, source contradiction and no-approval product refusal. Record model/host/version/input commit and failures. Fix defective skills or scripts through PRs; do not label YAML validation behavioral success. Review M1-S11.',
'All cases have actual artifacts/traces and peer verdicts; no copied Stage 1/2 reports.',
'Complete current Stage 3 skill evaluation bundle.'),
('Stage 3 submission and CI audit','SDLC Stage 3, SB-2, TQ-5/7/8; handbook 40–41','Stage 3 Review; Actions settings; dependency/secret reports',
'Review M2-S11 and audit CI permissions, pinned actions, required checks, test artifacts, Google denial and scheduled-live isolation. Refresh dependency scan; inspect every finding and transport-specific disposition with a human. Check every significant defect has a regression and real issue/PR. Verify skill evaluation results and source traceability. Publish a dated Stage 3 review with remaining live/human gates accurately separated; all implementation/test defects must be closed before submission.',
'Green build/lint/test/secret/skill/brain/trace gates; complete skill results and actual CI URLs.',
'Signed Stage 3 bundle with no hidden test or security failure.')],
[
('Controlled live FR-1–FR-5 and approved write','B1, FR-1–5, TQ-6; handbook 43–45','demo-script; live account; CLI approval; quota evidence',
'Confirm actual Cloud remaining limits and choose a small bounded private playlist (2–3 items, not a large quota-consuming demo). Exercise live video/channel ranking, authorized recommendations from all three sources and truthful analytics with safe accounts. Preview normalized constraints; deliberately attempt an unapproved commit and observe refusal. The human then reviews/types the exact approval. Create, read back every ordered video and repeat commit to prove no duplicate. Preserve sanitized state/count/quota evidence and an allowed link; never claim success before the API and journal confirm it. Review M3-S12.',
'All five live results observed through MCP; explicit human approval and actual saved playlist/readback/replay proven.',
'Real-account functional acceptance, not fixture substitution.'),
('Existing AI-client configuration and live product skill','B2, SK-05, NFR-10; handbook 33–34, 45','user-guide-mcp-client; selected host; real MCP process',
'Configure the evaluator’s chosen existing AI host with absolute launcher paths and private environment setup. Demonstrate initialize/tools/resources/read/prompt and all documented error displays. Run video-to-playlist end to end with the dedicated profile, including metadata-derived overview and short saved-playlist analysis. The human grants approval independently; the host must wait. Capture sanitized screenshots/transcript where allowed and host/version/config structure without secrets. Fix host compatibility defects and documentation. Review M1-S12.',
'Actual host behavior recorded; not merely Java SDK success; fixture/live labels and privacy/caveats remain clear.',
'Evaluator-client and live product-skill acceptance evidence.'),
('Policy, scope, privacy and data-deletion acceptance','A9/A11, B1/B4, security; handbook 43, 47','current Google policies; threat model; retention/deletion guides',
'Review official current API policies, scope requirements, cache/retention/deletion and derived-metric restrictions against the actual product. Record the educational metadata-ranking purpose and escalate a real incompatibility to client review rather than declaring coursework exempt. Verify source attribution/canonical links, consent behavior and minimal private storage. Exercise live disconnect/local deletion on the dedicated profile after coordinating with M1/M2; reauthorize only if later testing needs it. Inspect source, history, release artifacts and evidence for secrets/PII. Review M2-S12.',
'Method-by-method scope and dated policy review signed by responsible human; deletion/revocation outcomes truthful.',
'Compliance/privacy acceptance with no unresolved policy or credential handling issue.')],
[
('Independent machine A and protocol compatibility','B3, NFR-06/10; handbook 44','clean clone/tag candidate; README; Java21; Docker',
'From a clean checkout on Member 1’s supported machine, use only repository instructions, install prerequisites, create an empty database and execute full local-check. Verify migrations and actual host launch/resource reads. Record Windows/Java/Docker/Python/host versions and negotiated MCP protocol. Correct undocumented assumptions such as .tools cache, absolute original paths or long socket paths. Ensure fixes are reviewed and other machines receive them. Review M3-S13.',
'No borrowed private credentials or hidden chat setup; independent report tied to exact commit.',
'First reproducibility report and updated portable setup instructions.'),
('Independent machine B and user documentation walkthrough','B3, SE-7; handbook 44–45','clean clone; README; user/MCP guides; CLI help',
'Repeat from clean state on Member 2’s machine independently. Follow auth, status, approval, repair, resolution, deletion and troubleshooting docs using fixtures wherever live consent is not required. Verify command help lists every supported operation and safe errors explain next actions. Review normalized constraints/partial results as a new user. Fix missing steps and add screenshots only if redacted and useful. Review M1-S13.',
'README-only build/test/start; actual host discovery; no unknown local prerequisite.',
'Second independent report and user-facing handover documentation.'),
('Independent machine C and Stage 4 skill evaluations','B3, TQ-7, SK-01–05; handbook 44–45','clean clone; stage-4 skill cases; Obsidian; host',
'Run independent clean-machine reproduction on Member 3’s machine. Then run all five skill positive/negative cases at the Stage 4 candidate, including live local-check and brain-query design explanation. Inspect the vault in Obsidian and demonstrate links to requirements/ADRs/tests. Review M2-S13. Reconcile machine differences and fix reproducibility or skill failures through normal review; do not replace independent reports with copied output.',
'Third machine report and fresh actual-host Stage 4 skill bundle; all required cases complete.',
'Independent reproduction and final-stage skill evidence ready for release audit.')],
[
('Audit closure and release candidate integration','A1–A11/B1–B4/C/D1/D2, all FR; handbook 44–46','audit ledger; acceptance-evidence; merged PRs; current source',
'Walk every original audit finding with its implementation, named tests, human review and live evidence. Reopen any item whose fix was only planned. Confirm all 48 package issues and missing-source requirements are represented. Integrate only reviewed fixes, rerun affected checks and cut a local candidate identifier, not the final evaluated tag. Recheck OAuth Testing expiry and schedule human reauthorization now if needed for final demo. Review M3-S14.',
'No critical/open functional/security gap; candidate commit, evidence and dependency inventory align.',
'Reviewable release candidate with an exhaustive closure matrix.'),
('Traceability and source-to-code walkthrough','SE-5, SB-1/3, B4; handbook 8, 45','traceability.csv; brain; ADRs; issues/PRs; tests',
'Replace remaining DEFERRED/TBD placeholders only with genuine completed evidence. Walk all FR/TQ/SB/SE/SK/NFR rows; verify test assertions actually support each obligation. Record a live explanation linking one requirement from research note to ADR, issue, reviewed PR, source, regression and skill. Have each human explain code authored/reviewed by another member. Fix stale docs, links and unsupported claims. Review M1-S14.',
'Final traceability validator rejects unresolved entries; actual URLs/commits inspected; comprehension record completed.',
'Complete evidence chain and human understanding, not a path-existence-only matrix.'),
('Release security, dependency and artifact review','A10, security, NFR-01/06; handbook 40, 42, 46','BOM; OSV; Gitleaks; package manifest; license; source references',
'Refresh scans at the exact candidate and review source/history/package contents. Verify actions/dependency pins and review any new advisory, including stdio-only applicability. Confirm no credentials or private evidence, client PDF distribution rights/private repository setting, accurate license terms and all runtime prerequisites. Rebuild the release and verify every checksum; ensure old staged files cannot contaminate it. Scan the extracted package independently. Review M2-S14.',
'No unresolved applicable advisory, secret finding or licensing/distribution blocker; checksums and source commit recorded.',
'Security-reviewed candidate package and signed artifact review.')],
[
('Full live rehearsal and scheduled-run verification','FR-1–5, B1/B2, TQ-5; handbook 45','demo script; scheduled live workflow; dedicated account',
'Rehearse the complete live demo at the frozen candidate without exposing personal data. Verify OAuth remains usable, quota sufficient and every FR/skill result truthful. Use a small approved real write only where needed, replay without duplicate and verify saved item order. Confirm at least one scheduled live workflow actually ran on its schedule, not only manual dispatch; repair missing runner/credential/budget issues. Record sanitized evidence and demonstrate zero-budget rejection separately with fixtures. Review M3-S15.',
'Successful rehearsal and actual scheduled-run URL/log with fixed cost; no unapproved mutation.',
'Operational demonstration ready, external prerequisites resolved before final day.'),
('Reviewer rehearsal and final documentation corrections','SE-7, SB-2, B4; handbook 45–47','README; updated handbook; demo; maintenance; all stage reviews',
'Act as evaluator: follow the exact Stage 4 scenes, ask each member to explain ranking, quota, OAuth, approval, recovery and history limitations, and note misunderstandings. Run local-check and brain-query live. Ensure the updated handbook addendum matches actual code/commands while preserving all original pages. Correct documentation and compile known limitations that are accepted scope choices, not missing obligations. Review M1-S15.',
'All demo scenes executable; original-source preservation verified; no contradictory readiness claims.',
'Final reviewed user/developer/learning/handover documents and comprehension record.'),
('Final candidate regression and go/no-go audit','All TQ, A10, handbook 44–46','candidate commit; complete evidence; release gate',
'Review M2-S15. Run clean full suite, formatting, validators, scans, all relevant skills and package probe on the exact integrated candidate. Independently audit evidence dates/commits and each acceptance gate. Check branch protections, real peer reviews and all-member note authorship. Produce an explicit go/no-go record with no fabricated approvals. Any failure gets an owner and a regression and is fixed/reverified today; if unresolved, block Day 16 release rather than downgrading the requirement.',
'All pre-release gates pass with current evidence; all three humans review the go/no-go.',
'Frozen validated candidate or an explicit no-go; no silent acceptance debt.')],
[
('Final evaluated release and immutable tag','SDLC Stage 4, C, handbook 46','main; final checks; release assets; changelog; acceptance manifest',
'After M2/M3 final reviews approve the exact candidate, verify clean main, all checks and complete final evidence. Tag the reviewed commit with the agreed final version (normally v1.0.0); do not overwrite an existing tag or tag an unreviewed fix. Publish the checksum-verified package, accurate changelog, SBOM and sanitized evidence links under the authorized repository visibility. Record commit/tag/asset hashes and provenance. Return in the review window to review M3-S16; no self-approval.',
'python scripts/release_gate.py --final passes after legitimate evidence updates; tag resolves to reviewed green commit; downloaded assets match checksums.',
'Actual final release, not just a local ZIP. Any remaining required gap blocks tagging/publishing.'),
('Final client demonstration and Stage 4 signoff','FR-1–5, SK-04/05, SB-2, B2/B4; handbook 45–46','released candidate; existing host; stage-4 evidence',
'Demonstrate the exact evaluated commit in the client: discovery/resources, all five FRs, refused unapproved commit, human approval and truthful real creation/readback/replay, full product skill and short analysis, local-check, brain-query and traceability walk. Use already-permitted sanitized recordings only if the client accepts that fallback and separate live-test evidence exists. Obtain actual client/team review decisions, record remaining accepted scope limits and make no false transcript/history claims. Review M1-S16 release metadata and checksums before publishing approval.',
'Stage 4 scenes and actual human signoff linked to final commit; no unsupported substitution of fixture/live evidence.',
'Final demonstrated acceptance and dated Stage 4 review.'),
('Independent final closure and maintenance handover','All audit IDs, SDLC final review, handbook 47','downloaded release; all gates; team/maintenance ownership',
'Independently verify the tagged release assets, checksums, docs and evidence. Review M2-S16 demonstration record, confirm all three members have genuine commits/notes/reviews and can explain the code. Ensure all mandatory issues/gates are closed with evidence and no required work is mislabeled future enhancement. Assign maintenance owners and schedule dependency/quota/policy/credential/retention reviews; document backup/restore and incident handling. Remove temporary private test artifacts through authorized local cleanup; do not silently delete remote playlists. Record final closure only after M1/M2 signoffs exist.',
'Final gate and independent artifact probe pass; open issue list contains only explicitly optional enhancements; all three human acknowledgements present.',
'Nothing from the original audit remains unresolved; otherwise report NOT COMPLETE and list the exact blocking obligation.')]
]
package_updates = {'M1-S01': 'Read the 4 November handover first. Reuse the existing Cloud setup where authorized; exclude WORKSPACE/desktop-client.json and every local vault from imports. Do not treat the friend account as automatically available to other members.', 'M1-S05': 'Cover the observed desktop-browser launch failure: verify the auth-login-only headless override and real console/browser availability with a meaningful regression or reproducible isolated check. Do not claim fixture OAuth mocks verify the production desktop launch.', 'M1-S07': 'Use the observed six/eight-second clips and weak topic matches as regression examples. Establish a documented educational-relevance/short-clip policy without imposing unstated hard constraints; record before/after ranking evidence.', 'M2-S07': 'Review the actual number-theory selection: exam-preparation material and very short clips are poor evidence of cryptographic-engineering coverage. Add representative RSA/modular arithmetic/finite-field cases and evaluate language uncertainty without pretending to inspect audio.', 'M3-S07': 'Independently evaluate the live-demo relevance weaknesses with human labels and verify the fixes generalize beyond those two queries. Retain duration/count constraints and unchanged approval binding.', 'M1-S09': 'Google setup and successful consent already occurred on the original machine. Inspect current local status and use WORKSPACE/desktop-client.json for authorized re-login if needed. Reconcile existing setup and complete missing refresh/revoke/re-login evidence on a coordinated test profile; do not needlessly replace or revoke the active friend profile.', 'M2-S09': 'Two real terminal approvals already led to server-reported creation. Reuse sanitized observations, then independently test the full grant boundary; never type the live phrase on a human’s behalf.', 'M3-S10': 'The existing release ZIP predates the browser-launcher fix and current handover. Build/test a fresh archive and verify that desktop-client.json is absent from source imports and package contents; also warn against manually zipping the outer workspace.', 'M1-S12': 'Reuse the two historical approved native-MCP creations as partial FR-5 evidence. Complete live FR-2/3/4 and missing replay/refusal assertions on the reviewed candidate; do not repeat writes without a new exact human approval. Coordinate any personal-data reads with the authorized friend.', 'M2-S12': 'Codex is already configured and native tool calls worked on 3 November. Reconnect and verify current native discovery, then demonstrate the actual video-to-playlist skill; isolated tool calls are not a completed skill evaluation. Account for the missing native catalog observed on 4 November.', 'M1-S14': 'Ensure the desktop browser fix, relevance follow-ups and sanitized live evidence are in the reviewed candidate; do not retain obsolete claims that no Google login or native host call ever occurred.', 'M2-S15': 'Reconcile older status documents with the 4 November live handover while keeping unverified composite gates pending. Verify credential location guidance, account ownership and the difference between native host calls and direct probes.'}
out=[intro]
for day,packages in enumerate(days,1):
 out.append(f'\n## Day {day:02d}\n')
 for member,(title,requirements,files,actions,checks,done) in enumerate(packages,1):
  key=f'M{member}-S{day:02d}'
  if key in package_updates:
   actions = 'Current-state update: ' + package_updates[key] + '\n\n' + actions
  reviewer=member%3+1
  peer=3 if member==1 else member-1
  deps='Day 1 bootstrap and membership coordination; do independent source reading while repository setup completes.' if day==1 else f'All required Day {day-1:02d} outputs merged/reviewed; inspect the same-day dependency references below before proceeding.'
  out.append(f'''\n### {key} — {title}

**Owner:** Member {member}. **Required human reviewer:** Member {reviewer}. **Also review today:** M{peer}-S{day:02d}. **Scope:** {requirements}.

**Review choice:** Offer Member {reviewer} Option A: review personally with an agent-prepared checklist; or Option B: delegate technical review to the agent against all three source documents, then personally inspect the changes/findings and decide. Apply the same choice when reviewing M{peer}-S{day:02d}. Agent-only findings do not close the SDLC human-review gate.

**Read/inspect:** {files}. **Dependencies:** {deps}

**Agent execution:** {actions}

**Required checks:** {checks}

**Commit/review/evidence:** Apply every item of the common execution procedure. Create/update the real `{key}` issue, work on `m{member}/d{day:02d}-<topic>`, write `docs/execution/day-{day:02d}/member-{member}.md`, update relevant traceability and brain records, and open a reviewed PR with actual test evidence. Request Member {reviewer}'s human review; separately inspect M{peer}-S{day:02d}. Preserve honest attribution and never claim an absent approval. A useful commit contains the implemented correction, test, document or executed acceptance evidence—not a cosmetic daily marker.

**Done only when:** {done} All required checks and the peer review have passed, the PR is merged and the evidence contains its real URL and SHA. If a dependent human/cloud action is missing, record the exact blocker and complete independent substeps; do not mark this package DONE.
''')
out.append(r'''
## Audit-to-closure map

| Audit finding | Primary closure packages | Independent/final checks |
|---|---|---|
| A1 credential lifecycle | M1-S05, M1-S09 | M3-S08, M3-S12 |
| A2 metadata cache | M3-S05, M1-S08 | M1-S11, M3-S15 |
| A3 OAuth tests | M1-S05 | M3-S08, M1-S11 |
| A4 official provider/MCP assertions | M1-S08, M2-S07, M2-S08 | M1-S11 |
| A5 skill evaluations | M2-S03, M2-S06, M2-S10, M2-S11, M3-S13 | every stage gate, M2-S16 |
| A6 relevance/performance | M1/M2/M3-S07 | M3-S15 |
| A7 exclusions/draft diagnostics | M2-S05, M2-S08 | M2-S09, M1-S12 |
| A8 partial counts | M2-S05, M1-S10 | M1-S11 |
| A9 retention/deletion | M3-S05, M3-S10, M3-S12 | M3-S16 |
| A10 quality gates/scans | M3-S02, M2-S06, M3-S11, M3-S14 | M3-S15, all Day 16 |
| A11 documents/contracts/scopes | M2-S01/02, all Day 4, M2-S13/15 | M3-S14 |
| B1 Google/live acceptance | setup begins Day 1; M1-S09, all Day 12 | M1-S15, M2-S16 |
| B2 actual host/live demonstration | M2-S10/12, M3-S13 | M2-S15/16 |
| B3 independent machines | M3-S01, all Day 13 | M3-S15/16 |
| B4 human review/authorship | all three every day | stage gates, M2-S14/15, all Day 16 |
| C GitHub/CI/live schedule/tag | M1-S01/02, M3-S02/09/11 | M1-S15/16, M3-S16 |
| D1 recovery | M1-S04/10 | M2-S09, M3-S10 |
| D2 pagination | M3-S05, M1-S08 | M1-S11/12 |

## Final release checklist — every box requires evidence

- [ ] FR-1 ranked URL/ID similar videos and FR-2 ranked URL/handle/ID channels work through fixture MCP and the live selected host.
- [ ] FR-3 uses likes, subscriptions and playlists with honest coverage/cold start; FR-4 exact aggregation and truthful temporal comparisons are verified.
- [ ] FR-5 natural-language and typed constraints, exact preview, local human approval, real save/readback, no duplicate replay and truthful partial/recovery behavior are verified.
- [ ] Tools, resources, prompt and five actual Agent Skills are documented, discoverable where appropriate and evaluated with positive/negative evidence at each stage.
- [ ] TQ-1–8 and prescribed security/negative cases have named tests, actual reports, isolated fixture CI, bounded scheduled live execution and regression links.
- [ ] Cache, quotas, account isolation, token lifecycle, safe deletion/retention, metadata/URL attribution and current compliance review are complete.
- [ ] SRS, architecture/UML/ER/deployment, ADRs, development plan, user/API docs, traceability and updated handbook agree with the tagged implementation.
- [ ] Brain PARA/index/log, >=10 research notes, all three real authors, distilled-note citations, significant AI session records and four reviewed stage bundles are complete.
- [ ] Protected shared repository, genuine incremental work from all members, issues, human-reviewed PRs, green checks, changelog and final tag exist.
- [ ] Independent supported-machine reproduction and actual existing-host demo are complete; no hidden author-machine prerequisites.
- [ ] Latest dependency/secret/history/package scans are reviewed, exact source/asset hashes match and client material is distributed only with permission.
- [ ] Every acceptance-evidence entry has verified evidence and genuine signoff. No BLOCKED/PENDING/DEFERRED mandatory obligation, undisclosed defect or imaginary review remains.
- [ ] All three members can explain the final code, skills and design; maintenance and incident/deletion owners are assigned.

An agent must report **NOT COMPLETE** if any required box remains unchecked. Do not promise a guaranteed calendar outcome independent of Google, GitHub permissions, reviewers and test results. The purpose of the detailed schedule is to make every remaining obligation executable and visible, not to turn required human actions into invented automated evidence.
''')
target=R.parent/'plan.md';target.write_text('\n'.join(out),encoding='utf-8')
assert len(days)==16 and all(len(d)==3 for d in days)
print(f'{target}: {len(" ".join(out).split())} words; 48 work packages')
