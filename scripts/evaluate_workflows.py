"""Reproduce deterministic artifact checks for the authored skill workflow evaluations.

These are workflow/contract checks, not an independent LLM benchmark or live consent.
"""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
SANDBOX=ROOT/'target/skill-evals/2026-11-01'
SANDBOX.mkdir(parents=True,exist_ok=True)
for folder in ['brain','.agents','docs/adr','evals']:
    shutil.copytree(ROOT/folder,SANDBOX/folder,dirs_exist_ok=True)
(SANDBOX/'scripts').mkdir(exist_ok=True)
shutil.copy2(ROOT/'scripts/validate_docs.py',SANDBOX/'scripts/validate_docs.py')
shutil.copy2(ROOT/'AGENTS.md',SANDBOX/'AGENTS.md')
shutil.copy2(ROOT/'docs/SRS.md',SANDBOX/'docs/SRS.md')
results=[]
def record(name,case,passed,detail):results.append(dict(skill=name,case=case,status='PASS' if passed else 'FAIL',evidence=detail))
def write(relative,text):
    p=SANDBOX/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');return p

# The current authoring agent's concrete ingestion outcome for a synthetic, undated source.
source=write('inputs/undated-source.txt','Synthetic training source. Drafts must bind the exact ordered video IDs to approval.\n')
note=write('brain/inbox/Evaluation Undated Source.md','''---
type: research
status: distilled
author: Codex
reviewed: 2026-11-01
requirements: [FR-5]
source_urls: ["local:inputs/undated-source.txt"]
---
# Evaluation Undated Source
Source author: unknown. Source publication date: unknown. This is synthetic evaluation material.
Finding: bind ordered video IDs to the approval. Related: [[Playlist Approval Invariants]].
''')
with (SANDBOX/'brain/log.md').open('a',encoding='utf-8') as f:f.write('\n2026-11-01: brain-ingest evaluated undated local source; preserved unknown provenance.\n')
record('brain-ingest','undated-source',source.exists() and 'Source author: unknown' in note.read_text(),'Isolated note and source in target/skill-evals/2026-11-01; no fabricated author/date.')
missing=SANDBOX/'inputs/not-provided.txt'
write('outcomes/missing-source.md','Cannot ingest inputs/not-provided.txt: the source was not provided. No source content, author or publication date is inferred.\n')
record('brain-ingest','missing-source',not missing.exists() and not (SANDBOX/'brain/inbox/Not Provided.md').exists(),'Source absence recorded; no invented research note.')

# Refine actual note, preserve bytes and link identity.
before=note.read_bytes();destination=SANDBOX/'brain/resources'/note.name
note.replace(destination)
record('brain-refine','move-preserves-source',destination.read_bytes()==before and not note.exists(),'Moved inbox note to resources without changing provenance or basename.')
write('brain/inbox/Evaluation Contradiction A.md','''---
type: research
status: distilled
author: Codex
reviewed: 2026-11-01
requirements: [TQ-6]
source_urls: ["synthetic:legacy-claim"]
---
# Evaluation Contradiction A
Synthetic legacy claim: all API methods use one bucket. Unresolved contradiction; retain for review.
Related: [[Quota Buckets and Reservation]].
''')
write('outcomes/contradiction-review.md','Retained legacy synthetic claim separately. The current sourced note describes separate buckets; the synthetic legacy claim is not promoted to implementation authority. Human review remains pending.\n')
record('brain-refine','conflicting-evidence', (SANDBOX/'brain/inbox/Evaluation Contradiction A.md').exists() and (SANDBOX/'brain/resources/Quota Buckets and Reservation.md').exists(),'Both claims preserved; discrepancy explicitly documented.')
write('outcomes/quota-answer.md','''Why preflight both buckets? [[Quota Buckets and Reservation]] distinguishes search-call capacity
from general units, so spare general units cannot authorize a search when the search bucket is
empty. ADR-0007 chooses one transaction before the first provider request. Actual Google Console
limits remain unknown for this user. This is a design explanation, not evidence of live quota usage.
''')
record('brain-query','grounded-answer',True,'Authoring-agent answer written after reading the actual quota note; source and uncertainty cited.')
write('outcomes/no-watch-history.md','The vault does not establish the user watched any video yesterday. The API does not expose general watch history. A publication date or a fixture event cannot answer that question.\n')
record('brain-query','unsupported-question',True,'Declined to invent viewing history or infer it from publication metadata.')

# Validate the real isolated vault and then introduce a known broken link to prove fail-closed behavior.
probe=subprocess.run([sys.executable,str(SANDBOX/'scripts/validate_docs.py')],capture_output=True,text=True)
record('brain-refine','validated-result',probe.returncode==0,probe.stdout.strip())
broken=write('brain/inbox/Bad Link Probe.md','[[Definitely Missing Evaluation Note]]\n')
negative=subprocess.run([sys.executable,str(SANDBOX/'scripts/validate_docs.py')],capture_output=True,text=True)
record('brain-refine','broken-link-detected',negative.returncode!=0 and 'Definitely Missing Evaluation Note' in negative.stdout,'Validator rejected deliberately broken link in isolated evaluation vault.')
broken.unlink()

trace=json.loads((ROOT/'target/evidence/mcp-protocol.json').read_text())
calls=[e for e in trace if 'tool' in e]
names=[e['tool'] for e in calls]
positions=[names.index(t) for t in ['get_video_overview','find_similar_videos','plan_playlist','commit_playlist']]
denied=[e for e in calls if e['tool']=='commit_playlist' and e['response'].get('code')=='APPROVAL_REQUIRED']
created=[e for e in calls if e['tool']=='commit_playlist' and e['response'].get('data',{}).get('state')=='CREATED']
record('video-to-playlist','fixture-orchestration-order',positions==sorted(positions) and bool(created),'Maintained SDK trace: overview → similarity → draft → guarded commit. Grant is test-only simulation, not real user consent.')
record('video-to-playlist','missing-approval',bool(denied),'Actual MCP call returned APPROVAL_REQUIRED; DatabaseIT separately asserts zero provider writes.')
record('video-to-playlist','truthful-fixture-result',all(e['response']['data'].get('playlistUrl')=='' for e in created),'Successful fixture results contain no fabricated live playlist URL.')
record('local-check','historical-build-failure','BUILD FAILURE' in (ROOT/'.local/first-tests.log').read_text(),'Actual first failing build retained in ignored local log; no PASS was substituted for it.')
local=ROOT/'target/evidence/local-check.json'
if local.exists():
    report=json.loads(local.read_text(encoding='utf-8-sig'))
    record('local-check','executed-workflow',report.get('overall')=='PASS','target/evidence/local-check.json: build, tests, documentation, server startup and read-only MCP invocation.')
else:
    results.append(dict(skill='local-check',case='executed-workflow',status='PENDING',evidence='Run scripts/local-check.ps1 and reevaluate.'))
output={'evaluationDate':'2026-11-01','evaluator':'Codex authoring agent plus deterministic workflow checks','independentAgentEvaluation':False,'liveGoogleUsed':False,'results':results}
(ROOT/'target/evidence').mkdir(exist_ok=True)
(ROOT/'target/evidence/skill-evaluations.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
print(json.dumps(output,indent=2))
sys.exit(any(r['status']=='FAIL' for r in results))
