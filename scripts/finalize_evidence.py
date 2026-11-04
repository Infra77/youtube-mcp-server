"""Archive sanitized executed evidence and finish handbook step notes."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from record_step import record
DATE='2026-11-01'
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
reports=[]
for folder in ['surefire-reports','failsafe-reports']:
    for p in sorted((ROOT/'target'/folder).glob('TEST-*.xml')):
        suite=ET.parse(p).getroot()
        reports.append({'suite':suite.attrib['name'],'tests':int(suite.attrib['tests']),'failures':int(suite.attrib['failures']),'errors':int(suite.attrib['errors']),'skipped':int(suite.attrib['skipped']),'testCases':[c.attrib['name'] for c in suite.findall('testcase')]})
assert reports and not any(r['failures'] or r['errors'] or r['skipped'] for r in reports),'Acceptance tests did not all pass'
local=json.loads((ROOT/'target/evidence/local-check.json').read_text(encoding='utf-8-sig'))
assert local['overall']=='PASS','local-check has not passed'
evidence=ROOT/'docs/evidence';evidence.mkdir(exist_ok=True)
for name in ['mcp-protocol.json','local-check.json','smoke.json','skill-evaluations.json']:
    shutil.copy2(ROOT/'target/evidence'/name,evidence/name)
write('docs/evidence/test-summary.json',json.dumps({'reportedDate':DATE,'suites':reports,'totalTests':sum(r['tests'] for r in reports),'liveGoogleUsed':False},indent=2))
total=sum(r['tests'] for r in reports)
table='\n'.join(f"| {r['suite'].rsplit('.',1)[-1]} | {r['tests']} | {r['failures']} | {r['errors']} | {r['skipped']} |" for r in reports)
write('docs/test-results.md',f'''# Executed verification — {DATE}

**{total} Java tests passed; zero failures, errors or skips.** These are fixture/local tests, not live
Google acceptance. Counts are extracted from the current Surefire/Failsafe XML; sanitized case names
are archived in [test summary](evidence/test-summary.json).

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
{table}

Executed command: scripts/local-check.ps1, following formatting with spotless:apply. It packaged the
JAR, ran verify, checked formatting, validated documentation, scanned selected source secret forms,
started the packaged stdio server and invoked get_quota_status. [Local-check report](evidence/local-check.json)
records each status. [Smoke report](evidence/smoke.json) records real protocol negotiation/discovery.

The maintained Java MCP SDK test discovers ten tools, five resources and one prompt, then exercises
FR-1..FR-5 including unapproved commit rejection, test-only local grant, fixture creation/readback and
idempotent replay. [Protocol evidence](evidence/mcp-protocol.json) contains only fictional data.
Real PostgreSQL Testcontainers tests cover migrations, locking, exact approval, expiry, cross-account
rejection, partial/ambiguous writes, quota contention, settlement and deletion.

The supplemental source scanner has a positive/negative self-test. It is not an audited vulnerability
scan. Skill evidence is separated in [skill evaluations](skill-evaluations.md). Original failed runs
remain under ignored .local logs; final reports do not conceal the defects described in defects.md.

Live OAuth/browser consent, actual token lifecycle, actual YouTube write, evaluator-host demonstration,
independent machine reproduction and human review remain pending. GitHub was deferred by the user.
''')
skills=json.loads((evidence/'skill-evaluations.json').read_text())
assert all(r['status']=='PASS' for r in skills['results']),'A workflow evaluation is incomplete'
skilltable='\n'.join('| '+r['skill']+' | '+r['case']+' | '+r['status']+' |' for r in skills['results'])
write('docs/skill-evaluations.md',f'''# Skill workflow evaluations — {DATE}

Evaluator: Codex authoring agent, with deterministic artifact/protocol checks. These are not an
independent agent benchmark and do not prove that a particular AI host automatically imports skills.
No live Google account or real approval was used. [Machine-readable results](evidence/skill-evaluations.json).

| Skill | Case | Outcome |
|---|---|---|
{skilltable}

brain-ingest was applied to an actual synthetic undated input; the resulting note explicitly retains
unknown author/date. Missing-source handling produced an explanation and no invented research note.
brain-refine moved the note while preserving bytes/basename, retained a contradictory synthetic claim
for review, and validated the vault. A deliberately broken link caused the isolated validator to fail.
brain-query answers were authored after reading the actual quota/stdout/OAuth notes; an unsupported
viewing-history question was explicitly declined. Those two answers are author-reviewed outcomes,
not assertions that a string-matching test measures language-model reasoning.

video-to-playlist checks use the real MCP transcript for workflow order, missing-grant rejection and
truthful fixture outcomes. PostgreSQL tests separately assert no writes and replay safety. The positive
grant is a test administrator simulation; interactive live human consent remains a separate gate.
local-check ran the real build/test/start/read workflow. An actual earlier failing build is retained as
negative evidence; the final successful report is separate. Further independent skill/host evaluation
is required at human stage submission. No historical stage submission or PR review was invented.
''')
steps={
38:('System tests through real MCP','Verified locally',
'''Implemented McpProtocolIT with the maintained Java MCP SDK, not direct service-only calls. The harness launches target/curator.jar as a child, supplies a disposable PostgreSQL database and explicit fixture mode, initializes protocol state, discovers tools/resources/prompts and reads a knowledge resource. It then invokes every functional requirement through tools/call. The test reads structured JSON, checks metadata provenance and nonempty rankings, exercises period comparisons and saves a constrained draft. An unapproved commit returns APPROVAL_REQUIRED. A test-only administrator simulation creates a real database grant for the fictional account; the following commit returns CREATED and readback verifies ordered items. Repeating the call returns the same playlist ID. The fixture URL remains empty, preventing a fictional success from being presented as an actual YouTube playlist. Invalid text, malformed IDs and unavailable videos are also exercised. The harness closes the child and archives a sanitized protocol trace.''',
'src/test/java/org/example/videocurator/McpProtocolIT.java; docs/evidence/mcp-protocol.json'),
39:('Negative tests and regression record','Verified locally',
'''Preserved actual failures and their fixes in docs/defects.md. Input tests reject deceptive hosts, duplicate ID parameters, absent schemes and unsupported channel aliases without touching quota/provider. Duration and text parsing reject zero, fractions, ambiguity and arithmetic overflow. WireMock exercises private/deleted video absence, missing metadata, malformed JSON, upstream quota, missing channel, expired authorization, permissions and rate limiting without live API calls. Database tests reject wrong account, altered digest, wrong typed phrase, expired grant and duplicate writers. Ambiguous create and partial item failure persist safe states and cannot blindly replay. The language regression enforces complete requested region tags and excludes malformed upstream language metadata. Partial date ranges now reject before reading personal data. Each negative category is a distinct executable assertion, not a prose checklist.''',
'src/test/java/org/example/videocurator; docs/defects.md'),
40:('Complete local quality gates','Verified locally; GitHub deferred',
'''Implemented and executed local-check.ps1 as the local quality-gate sequence. It packages an executable JAR, runs unit/provider/database/protocol tests, checks Java formatting, validates brain/skill/document links, runs a supplemental credential-pattern scanner with a deliberate synthetic positive/negative self-test, starts the actual packaged server and invokes a read-only tool. Failures stop the workflow and the finally block writes a FAIL report rather than substituting success. Traceability validation checks all 41 requirement rows and real artifact/test/skill/note paths. The scanner covers selected recognizable secret formats; it is explicitly not advertised as a full dependency vulnerability assessment. Hosted PR checks and a scheduled live workflow were not created because the user asked to skip GitHub. Their translation plan is documented for later authorization.''',
'scripts/local-check.ps1; scripts/validate_docs.py; scripts/validate_traceability.py; scripts/scan_secrets.py; docs/ci-local.md'),
41:('Five skill evaluations and Stage 3 review','Authored workflow evaluations recorded',
'''Read each canonical SKILL.md and applied its procedure to concrete isolated artifacts or the actual execution evidence. The ingestion exercise preserved unknown source metadata and refused a nonexistent source. Refinement moved a note without changing provenance, kept contradictory material for review, and proved the validator rejects a deliberately broken wikilink. Query outputs cite actual read notes and decline unsupported watch-history inference. Product-workflow evidence checks the real MCP call sequence, approval rejection and honest synthetic results; the positive grant is explicitly test-only. local-check evidence comes from its actual run. The evaluation report distinguishes deterministic checks and author-reviewed answers from independent agent/host testing. Stage retrospectives identify what worked, observed defects, changes and the remaining human/live gates. No earlier stage submission or peer approval is fabricated.''',
'scripts/evaluate_workflows.py; docs/skill-evaluations.md; docs/evidence/skill-evaluations.json; brain/projects/Video Intelligence MCP/Stage 3 Review.md'),
42:('Packaging and launch','Local release candidate packaged',
'''Prepared a credential-free local distribution containing the executable JAR, source/build files, launch/admin/database scripts, Compose definition, user/API/setup documentation, skills, PARA notes and sanitized evidence. Packaging uses an explicit allowlist and excludes .local, dependency/JDK caches, personal credentials and raw build reports. SHA256SUMS.txt records each delivered file. The package is versioned 0.1.0-local rather than falsely presenting a final evaluated v1.0 release. Launchers derive paths from their own location, use JAVA_HOME on another machine and keep stdout clean in MCP mode. The source tree also remains available so the user can inspect and rebuild every implementation decision. A package probe uses only fixture mode and the configured local database; it is not claimed to be a second person's clean machine.''',
'scripts/package_release.py; release; target/curator.jar; scripts/start-mcp.ps1; scripts/admin.ps1'),
43:('Google Cloud and compliance gate','Pending user setup',
'''The user explicitly confirmed that Google Cloud/YouTube Desktop OAuth is not set up. Therefore no live Google credential was requested in chat, no real consent was simulated and no real playlist was written. Auth code, scope rationale, local encrypted storage, status/logout/delete-data operations and a detailed setup guide are implemented. The guide instructs the user to enable the official API in one project, configure consent/test users, create Desktop credentials outside the repository, check channel availability/actual quota, and authorize through Google's browser flow. Minimum operational scope and metadata limitations are documented. A final compliance review and actual lifecycle test remain pending real account setup; code inspection and synthetic fixtures cannot prove these external conditions.''',
'docs/google-cloud-setup.md; docs/security-threat-model.md; docs/acceptance-status.md; oauth/WindowsTokenVault.java (under src/main/java/org/example/videocurator)'),
44:('Reproduction and final verification checklist','Local reproduction verified; independent machine pending',
'''Executed the published local commands against this workstation and built a transportable package with explicit prerequisites. The project-local Java archive was verified; other machines can use installed JDK 21 through JAVA_HOME. The Maven wrapper and dependency pins are included. Testcontainers migrates fresh databases, and the protocol test launches the actual packaged JAR with credentials only for fictional test infrastructure. The standalone smoke probe checks clean protocol stdout and a read-only result against the local server. Documentation and source scans inspect the delivered artifact paths. The user's second machine, editor/client configuration and real OAuth environment were not available, so the independent-clean-machine and specific-client portions remain honestly pending. This distinction prevents local reproducibility from being inflated into team acceptance.''',
'docs/setup-windows.md; docs/test-results.md; docs/evidence/local-check.json; docs/acceptance-status.md'),
45:('Stage 4 demonstration','Fixture rehearsal verified; live demo pending',
'''Wrote an ordered demonstration script that shows capability discovery, limitations, FR-1 video ranking, FR-2 channel ranking, FR-3 sampled recommendations, FR-4 truthful temporal analysis and FR-5 proposal/approval/commit. The maintained-client test records the fixture sequence and explicit approval rejection; the manual script tells the human how to review and approve an exact proposal in their own terminal. It also explains short playlist analysis, replay behavior, the product skill and a requirement walk from brain note to ADR, implementation and test. No custom UI was introduced. A live evaluator-host demonstration with a real Google account remains pending. All fixture IDs, account events and playlist outputs are explicitly fictional, and the result never substitutes a fake URL for a successful remote creation.''',
'docs/demo-script.md; docs/evidence/mcp-protocol.json; docs/brain-query-evidence.md'),
46:('Release candidate and handover','Local handover ready; final signoff deferred',
'''Created README, changelog, API/user/setup guides, traceability, executed test results, known limitations, maintenance instructions and a release-candidate archive with checksums. Updated the handbook by prepending a clearly labeled three-page implementation addendum to an updated copy, retaining all 53 original pages unchanged and leaving the original PDF untouched. The addendum records local-only GitHub deferral, exact dependency choices, Windows socket fix, bounded optimizer improvement, quota configuration and conservative write recovery. A local release candidate is deliberately distinct from a final evaluated release. No Git tag, remote release, license grant on the client's material, human signoff or production readiness was fabricated. The owner can review the complete local artifacts and finish the external gates later.''',
'README.md; CHANGELOG.md; docs/traceability.csv; docs/YouTube_Intelligence_MCP_Handbook_Updated.pdf; release'),
47:('Maintenance and extension criteria','Documented and handed over',
'''Documented routine build/test/format/link checks, dependency/API policy review, quota reconciliation, explicit local data cleanup, token reauthorization and conservative interrupted-write handling. The local database volume is persistent; deleting it is not a troubleshooting shortcut. Backups and OAuth material are private and excluded from the release. Expired uncommitted proposals can be removed with cleanup; profile data can be removed through an interactive command. Remote playlists are not silently deleted. Future work must be justified by requirements and measurements: fuller pagination, global optimization, additional OS vaults or an authenticated remote MCP design. The project does not add a website, Redis, Kafka or Kubernetes merely to enlarge the stack. Significant new defects should receive a regression and corresponding note/ADR amendment.''',
'docs/maintenance.md; docs/acceptance-status.md; AGENTS.md')}
for n,(title,status,actions,files) in steps.items():
    record(n,title,status,actions,files,
      f'Final local acceptance has {total} executed Java tests with zero failures/errors/skips. local-check reports PASS for the actual build/test/start/read sequence. Sanitized evidence lives in docs/evidence; exact test names are in test-summary.json. Each step above distinguishes direct executed evidence from a document, code path or external gate.',
      'All five functional services, the MCP interface, official/fixture providers, database invariants, local CLI, tests, skills and SDLC documentation exist. The deliverable is a local review candidate. Google Cloud/live authorization/real YouTube writes, independent machine/client acceptance, human review and deferred GitHub work are not complete.',
      'No live Google data or credentials were used. The original client documents remain unchanged. Human review and external acceptance must be completed before claiming final client signoff.')
    note=ROOT.parent/'notes'/f'step {n}.md'
    note.write_text(note.read_text().replace('Date: 2026-10-31','Date: '+DATE),encoding='utf-8')
for n in range(19,38):
    note=ROOT.parent/'notes'/f'step {n}.md'
    with note.open('a',encoding='utf-8') as f:
        f.write(f'\n## Final verification update — {DATE}\n\nThe complete local-check now passes: {total} Java tests, zero failures/errors/skips, real PostgreSQL integration and packaged MCP calls. See ../youtube-intelligence-mcp/docs/test-results.md and its evidence links. This supersedes the earlier in-progress verification wording, while retaining the history of how the step was implemented. Live Google and human review remain pending.\n')
        if n==31:f.write('\nThe original plain-greedy limitation was subsequently improved through ADR-0009: a bounded one-for-two swap fixes the demonstrated 20 vs 11+11 minute case. The final regression is selectorDeterministicAndRepairsGreedyUnderfill. Explicit regional language requests now require the full declared tag; malformed language metadata is excluded.\n')
notes_index='# Handbook step notes\n\nNumbering follows explicit handbook Steps 0–47; chapter 22 is Step 0. Source files and code are in ../youtube-intelligence-mcp. Date of final local handover: '+DATE+'.\n\n| Step | Note | Status |\n|---|---|---|\n'
for n in range(48):
    status=steps[n][2-1] if n in steps else ('GitHub deferred' if n in (2,5) else 'Local artifact implemented; see detailed evidence')
    notes_index+=f'| {n} | [step {n}.md](step%20{n}.md) | {status} |\n'
(ROOT.parent/'notes/index.md').write_text(notes_index,encoding='utf-8')
run=subprocess.run([sys.executable,str(ROOT/'scripts/validate_traceability.py')],capture_output=True,text=True,cwd=ROOT)
assert run.returncode==0,run.stdout+run.stderr
write('docs/evidence/traceability-validation.json',run.stdout)
for script,name in [('validate_docs.py','documentation-validation.json'),('scan_secrets.py','source-scan.json')]:
    run=subprocess.run([sys.executable,str(ROOT/'scripts'/script)],capture_output=True,text=True,cwd=ROOT)
    assert run.returncode==0,run.stdout+run.stderr
    write('docs/evidence/'+name,run.stdout)
print(f'Archived {total} passing Java tests; wrote handover reports and notes 38–47.')
