"""Maintain handover documents and source-to-evidence mapping, without claiming live signoff."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
def write(p,text):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
write('README.md','''# Educational Video Curator MCP

Java 21 headless MCP server implementing video/channel similarity, personalized recommendations,
honest engagement analysis and human-approved playlist creation through the official YouTube API.
No custom frontend. Existing MCP hosts provide conversation.

**Status:** local release candidate 0.1.0. Fixture/provider/PostgreSQL/MCP verification is available;
Google Cloud setup, live OAuth/YouTube acceptance, human review and deferred GitHub evidence are
not claimed complete. See [test results](docs/test-results.md) and [acceptance status](docs/acceptance-status.md).

## Run locally on Windows

Start Docker Desktop, install JDK 21 and Python 3, then open PowerShell in this directory:

```powershell
.\\scripts\\start-db.ps1
.\\scripts\\build.ps1
.\\scripts\\local-check.ps1
```

This workspace already contains a project-local verified JDK and Maven cache. Other machines use
JAVA_HOME. Build output is target/curator.jar. Ordinary tests use fictional data and disposable
PostgreSQL containers, never live Google. The persistent local database listens on 127.0.0.1:55432.

Configure your host to launch scripts/start-mcp.ps1 with `-Mode fixture`. Rehearsal inputs:
`FIXTURE0001`, `@ExampleMath`. Fixture results are explicitly labeled and never provide fake live URLs.
For live use, follow [Google setup](docs/google-cloud-setup.md) yourself; never send credentials to chat.

## Read and inspect

- [Windows setup](docs/setup-windows.md), [MCP user guide](docs/user-guide-mcp-client.md), [tool API](docs/mcp-api.md)
- [SRS](docs/SRS.md), [architecture](docs/architecture.md), [decisions](docs/adr/0001.md), [threat model](docs/security-threat-model.md)
- [Traceability](docs/traceability.csv), [testing](docs/test-plan.md), [defects](docs/defects.md), [versions](docs/versions.md)
- [Second brain](brain/index.md): open brain/ in Obsidian; canonical skills are .agents/skills/
- [Handbook amendments](docs/handbook-amendments.md), [demo](docs/demo-script.md), [maintenance](docs/maintenance.md)
- Detailed learning notes live **outside** this project in ../notes/step 0.md through step 47.md.

Every YouTube write requires the user to review the immutable proposal and type its full fingerprint
in the separate local approval CLI. commit_playlist only accepts the saved draft ID. Partial and
ambiguous writes are journaled and require review; they are never blindly retried.
''')
write('CHANGELOG.md','''# Changelog

## 0.1.0 — local release candidate, 2026-11-01

- Ten MCP tools, five resources and one safe workflow prompt.
- Official/fixture provider boundaries, metadata TF-IDF ranking and bounded personal analysis.
- Natural-language grammar and deterministic hard-constraint planner with one-for-two swap.
- PostgreSQL drafts, exact-digest approval, write journal and two-bucket quota reservations.
- Windows PKCE/DPAPI authorization CLI, human approval, cleanup and account data deletion.
- Unit, WireMock, real PostgreSQL and packaged MCP tests; external detailed step notes and PARA vault.
- Fixed malformed URL handling, Windows selector temp path, missing JSON mapper and partial-period input.

Not a final evaluated v1.0 release: live Google acceptance, peer signoff and GitHub stages are pending.
No release tag, remote repository or hosted CI run was fabricated.
''')
write('docs/acceptance-status.md','''# Acceptance status — 2026-11-01

## Verified locally

Implemented FR-1 through FR-5, tools/resources/prompt, PostgreSQL/Flyway state, exact human grant
logic and quota preflight. Automated fixture protocol evidence exercises all FRs through the packaged
server. Check the executed results in test-results.md, not merely the existence of source files.
The product remains a headless local Java server.

## Required external evidence still pending

1. Google Cloud project/API/desktop OAuth client and dedicated test account. User confirmed not set up.
2. Interactive Google consent, real token refresh/revocation and real approved playlist creation.
3. A live demonstration in the evaluator's chosen existing AI client. Java SDK and smoke probes are
   real MCP clients, but do not prove that particular host's configuration or skill import.
4. Human code/design review and second contributor comprehension/authorship.
5. GitHub repo, Issues, PRs, protection, hosted/scheduled workflows and release tag, deferred by user.
6. Independent clean-machine reproduction and dependency vulnerability/compliance review before
   public or production use. A packaged local probe is not a second person's machine.

No remote service was deployed and no real playlist was created. Ordinary checks require no Google
credentials. Tests are synthetic, and live operations never run as a side effect of packaging.

## Deliberate limitations

Windows-only protected live credential vault; fixture core can run on Java21 elsewhere. One local
account per process. One bounded page per personal source with explicit truncation. Natural-language
grammar is intentionally limited; unsupported phrasing asks for clarification. Language means declared
audio metadata, not verified speech. Selection is a bounded heuristic, not a global optimum. Partial
or ambiguous remote writes require manual review, with no automatic repair command. Quota ledger
cannot see other clients' Google usage; operators must verify actual Console budgets.
''')
write('docs/demo-script.md','''# Local rehearsal and live demonstration

1. Run local-check and inspect its JSON result. Explain that this is a stdio Java MCP service.
2. In an existing MCP client discover ten tools, five resources and one workflow prompt.
3. Read limitations; call get_video_overview(FIXTURE0001), then find_similar_videos with limit=4.
4. Call find_similar_channels(@ExampleMath,3), recommend_for_me(3), and analyze_my_engagement
   comparing 2026-01-01/2026-02-01 to 2026-02-01/2026-03-01. Explain coverage and timestamp meaning.
5. Plan a 1800-second English Fourier playlist with maxVideoSeconds=1200 and maxVideos=3.
6. Commit without approval and show APPROVAL_REQUIRED. Display the full saved draft.
7. The human runs admin.ps1 -Mode fixture approve UUID in a terminal and types the digest.
8. Commit through the host; show CREATED with fixture=true and no real playlist URL. Repeat to
   demonstrate no duplicate write. Explain that the test-only grant simulation is not real consent.
9. Walk through video-to-playlist skill and brief output analysis, then use brain-query to explain
   quota reservation from its note, ADR-0007, QuotaService and DatabaseIT test.
10. For the actual live gate, first complete google-cloud-setup.md and switch to live mode. Use small
    approved constraints and check remaining quota before any operation. Record only nonprivate evidence.

The scripted SDK test performs the fixture sequence automatically. It does not impersonate human
consent to a live account, nor substitute for a human evaluator reviewing the real CLI preview.
''')
write('docs/maintenance.md','''# Maintenance and operator recovery

Run local-check after source/dependency changes. Keep notes, traceability and regression cases current.
Review Spring AI/MCP compatibility, Google endpoint/scope/quota rules and dependency advisories before
upgrading. Re-run packaged protocol discovery after SDK updates. Do not expose this server over HTTP
without a new authorization/user-isolation architecture and ADR.

Use cleanup regularly to delete expired uncommitted drafts. Use delete-data when finished with a
profile; it deletes local proposals/grants/journals, not remote playlists or Google account activity.
Retain only necessary local evidence; this prototype has explicit operator-driven cleanup, not a
background retention service. Review current YouTube retention rules before use beyond coursework.

If a write is PARTIAL/NEEDS_MANUAL_REVIEW or remains CREATING after a crash, inspect its journal
and the account directly. Do not edit approvals or rerun inserts to force completion. Confirm which
remote resources exist, resolve them manually, and obtain a fresh approval for any new proposal.
Abandoned quota reservations are conservatively retained for their quota day; they do not consume
the next Pacific day's ledger. No automatic reset claims actual Google Console usage.

PostgreSQL backup: use pg_dump locally, protect the backup as private user data and exclude it from
source/evidence bundles. Never delete the Compose volume as a troubleshooting shortcut. OAuth
credentials are bound to Windows CurrentUser and require reauthorization on another OS/user.

Future additions need a measured requirement: global optimizer, public metadata cache, richer
pagination, remote authenticated MCP, or additional secure OS vaults. No Redis/Kafka/Kubernetes/UI
is needed for this local assignment.
''')
write('LICENSE','''No public redistribution license has been selected by the project owner.
The generated project is delivered locally for the user's client assignment. This file does not
grant rights to the supplied client documents. Third-party libraries retain their respective licenses;
inspect their bundled notices and Maven metadata before redistributing a compiled package.
''')
write('docs/ci-local.md','''# Local quality gates; GitHub deferred

The user explicitly requested no GitHub work. No .github workflow, PR, branch protection or hosted
run is claimed. scripts/local-check.ps1 is the executed local equivalent: package, tests, formatting,
documentation links, supplemental source secret scan, actual server startup and read-only MCP call.
validate_traceability.py checks source/test/skill/note paths and explicit deferred statuses.

The secret scanner detects selected common credential forms and tests itself with an ephemeral
synthetic key. It is supplemental and not a replacement for an audited hosted scanner or security review.
The full Maven suite uses WireMock, fictional provider data and disposable PostgreSQL only.

When GitHub is authorized, translate these commands into restricted-permission PR workflows, require
human review, add audited secret/dependency scanning, and archive sanitized reports. A separate
scheduled live workflow must use a dedicated account and an explicit fixed quota gate; it must stay
disabled until credentials and review exist. Live tests must never become a PR merge prerequisite.
''')
tests='src/test/java/org/example/videocurator/'
rows=[]
def add(req,step,artifact,test,skill,note,status='local-verified; live/human acceptance separate'):
    rows.append(dict(requirement=req,issue=f'L-{step:02}',pr='DEFERRED',artifact=artifact,test=test,skill=skill,brain_note=note,status=status))
for i,step,note in [(1,26,'TF-IDF and Cosine Similarity'),(2,27,'Related Endpoints Do Not Exist'),(3,28,'YouTube Endpoint Matrix'),(4,29,'Analytics Data Semantics'),(5,32,'Playlist Approval Invariants')]:
    add(f'FR-{i}',step,'src/main/java/org/example/videocurator/application/CuratorService.java',tests+'McpProtocolIT.java','video-to-playlist',note)
for i,step,test,note in [(1,36,'domain/DomainTest.java','TF-IDF and Cosine Similarity'),(2,37,'DatabaseIT.java','Postgres Crash Recovery'),(3,38,'McpProtocolIT.java','MCP Stdio Semantics'),(4,39,'ProviderTest.java','YouTube Endpoint Matrix'),(5,40,'ProviderTest.java','CI Fixture Isolation'),(6,23,'DatabaseIT.java','Quota Buckets and Reservation'),(7,41,'PENDING','Obsidian Knowledge Structure'),(8,39,'domain/DomainTest.java','CI Fixture Isolation')]:
    add(f'TQ-{i}',step,'docs/test-plan.md',tests+test if test!='PENDING' else 'docs/skill-evaluations.md','local-check',note,'local evidence; scheduled live workflow deferred' if i==5 else 'see executed report; no hosted CI claim')
for i,artifact in enumerate(['brain/index.md','brain/projects/Video Intelligence MCP/Stage 4 Review.md','docs/adr/0001.md','AGENTS.md','docs/acceptance-status.md','docs/acceptance-status.md'],1):
    add(f'SB-{i}',3,artifact,'scripts/validate_docs.py','brain-refine','Obsidian Knowledge Structure','DEFERRED human/GitHub evidence' if i>=5 else 'local artifacts validated')
for i,artifact in enumerate(['docs/SRS.md','docs/architecture.md','docs/adr/0001.md','docs/development-plan.md','docs/traceability.csv','src/main/java/org/example/videocurator/provider/YouTubeProvider.java','docs/mcp-api.md'],1):
    add(f'SE-{i}',7 if i==1 else 10,artifact,'scripts/validate_traceability.py','brain-query','Codex Project Boundaries','local artifacts; human review pending')
for i,name in enumerate(['brain-ingest','brain-refine','brain-query','local-check','video-to-playlist'],1):
    add(f'SK-{i:02}',35,f'.agents/skills/{name}/SKILL.md','docs/skill-evaluations.md',name,'Obsidian Knowledge Structure','see authored workflow evaluation; independent host evaluation pending')
for i,note,test in [(1,'Google OAuth Desktop PKCE','SemanticsTest.java'),(2,'TF-IDF and Cosine Similarity','domain/DomainTest.java'),(3,'TF-IDF and Cosine Similarity','McpProtocolIT.java'),(4,'Quota Buckets and Reservation','DatabaseIT.java'),(5,'Playlist Approval Invariants','DatabaseIT.java'),(6,'CI Fixture Isolation','McpProtocolIT.java'),(7,'Google OAuth Desktop PKCE','DatabaseIT.java'),(8,'YouTube Endpoint Matrix','ProviderTest.java'),(9,'Quota Buckets and Reservation','ServiceTest.java'),(10,'MCP Stdio Semantics','McpProtocolIT.java')]:
    add(f'NFR-{i:02}',36,'docs/SRS.md',tests+test,'local-check',note,'local evidence; live/manual aspects pending as applicable')
with (ROOT/'docs/traceability.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
for stage,topic in [(1,'requirements and research'),(2,'architecture and design'),(3,'implementation and fixture verification'),(4,'local handover and pending live review')]:
    write(f'brain/projects/Video Intelligence MCP/Stage {stage} Review.md',f'''# Stage {stage} Review

Date: 2026-11-01. Author: Codex. Human reviewer: pending. GitHub PR: deferred by user.
Scope: {topic}. This is a retrospective local review record, not a fabricated prior stage submission.

## What worked
Client identifiers and four stages were preserved. Source extraction retained page markers. The
project stayed headless and used official provider boundaries. Notes and ADRs cite distilled sources.
Automated reports separately show unit, provider, real database and packaged protocol evidence.

## What failed and changed
Malformed URL null handling, Windows socket-path compatibility and missing headless JSON mapper
were found by actual tests and fixed. The planner's greedy underfill case justified a bounded swap.
These are recorded with regressions in docs/defects.md and ADR-0009.

## Remaining gate and next action
Human review, a second contributor/machine, live Google authorization and a real approved playlist
remain pending. GitHub controls/history and scheduled live CI are explicitly deferred, not passed.
Follow the setup/demo checklist; do not present synthetic results as a user's YouTube account.

Related: [[Project Map]], [[CI Fixture Isolation]], [[Codex Project Boundaries]].
''')
with (ROOT/'brain/index.md').open('a',encoding='utf-8') as f:f.write('\n## Stage reviews\n'+''.join(f'- [[Stage {i} Review]]\n' for i in range(1,5)))
print('Prepared local handover docs and 41-requirement traceability matrix.')
