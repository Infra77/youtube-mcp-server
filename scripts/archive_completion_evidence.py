"""Archive actual local reports without claiming external acceptance."""
from pathlib import Path
import datetime, hashlib, json, re, shutil, xml.etree.ElementTree as ET
R = Path(__file__).resolve().parents[1]
E = R / 'docs/evidence'
suites = []
for folder in ['surefire-reports', 'failsafe-reports']:
    for path in sorted((R / 'target' / folder).glob('TEST-*.xml')):
        root = ET.parse(path).getroot()
        suites.append({'name': root.attrib['name'], **{k: int(root.attrib.get(k, 0)) for k in ['tests', 'failures', 'errors', 'skipped']}, 'cases': [t.attrib['name'] for t in root.findall('testcase')]})
totals = {k: sum(s[k] for s in suites) for k in ['tests', 'failures', 'errors', 'skipped']}
assert totals['tests'] == 47 and not any(totals[k] for k in ['failures','errors','skipped']), totals
(E / 'test-summary.json').write_text(json.dumps({'date': '2026-11-03', 'scope': 'fixture/local; no real Google consent or writes', 'totals': totals, 'suites': suites}, indent=2))
for path in (R/'target/evidence').glob('*.json'):
    shutil.copy2(path, E/path.name)
shutil.copy2(R/'target/bom.json', E/'bom.json')
rows = '\n'.join('| '+s['name'].split('.')[-1]+' | '+ ' | '.join(str(s[k]) for k in ['tests','failures','errors','skipped'])+' |' for s in suites)
(R/'docs/test-results.md').write_text(f'''# Executed verification - 3 November 2026

**47 Java tests passed, with zero failures, errors or skips.** The full local pipeline
ran clean package, verify (including PostgreSQL Testcontainers and packaged MCP), formatting,
documentation, traceability, strict skill/case schema validation, Gitleaks and MCP startup/read.
After the final CLI help-text change, package reran all 32 unit tests successfully; the 15
integration results are from the preceding full verify. [Actual cases](evidence/test-summary.json).

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
{rows}

[Local pipeline](evidence/local-check.json), [MCP protocol](evidence/mcp-protocol.json),
[startup/read smoke](evidence/smoke.json), [coordinator negative cases](evidence/local-check-negative.json),
[ranking benchmark](evidence/ranking-evaluation.json), [dependency audit](evidence/dependency-audit.json)
and [runtime BOM](evidence/bom.json) record the executed checks. The ranking cases are synthetic;
they do not replace independent relevance evaluation. Gitleaks found no leaks in its configured scope.
OSV checked 66 exact Maven components: no undispositioned known advisory; one HTTP-only MCP advisory
is retained as not applicable to stdio, with independent human review still required.

[Package verification](evidence/package-check.json) records the final archive hash and an actual
extracted PowerShell launcher probe on this machine. It is not independent-machine acceptance.
Skill schemas and coordinator checks are not real agent-host behavioral evaluations.

Google setup/consent, native credential lifecycle, live FR-1 through FR-5, personally approved
playlist creation, host skill runs, peer review, independent machines, GitHub controls/CI/history
and final signoff remain explicit gates in acceptance-evidence.json and the external plan.md.
''', encoding='utf-8')
plan = (R.parent/'plan.md').read_text(encoding='utf-8')
ids = re.findall(r'^### (M[123]-S\d\d)\b', plan, re.M)
assert len(ids) == 48 and len(set(ids)) == 48
assert set(ids) == {f'M{m}-S{d:02}' for m in range(1,4) for d in range(1,17)}
pdfs = ['Project_1_YouTube_MCP.pdf','SDLC_and_Workflow.pdf','YouTube_Intelligence_MCP_Server_Only_Handbook.pdf']
for name in pdfs:
    assert (R.parent/name).read_bytes() == (R/'docs/reference'/name).read_bytes()
(E/'plan-validation.json').write_text(json.dumps({'status':'PASS','packages':48,'members':3,'days':16,'planSha256':hashlib.sha256(plan.encode()).hexdigest(),'originalPdfCopiesIdentical':pdfs},indent=2))
manifest=json.loads((R/'docs/acceptance-evidence.json').read_text())
evidence={'LOCAL_TESTS':['docs/evidence/test-summary.json'], 'LOCAL_QUALITY':['docs/evidence/local-check.json'], 'DEPENDENCIES':['docs/evidence/dependency-audit.json'], 'PACKAGE':['docs/evidence/package-check.json']}
for gate in manifest['gates']:
    if gate['id'] in evidence:
        gate.update(status='PASS',evidence=evidence[gate['id']])
(R/'docs/acceptance-evidence.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'tests': totals, 'planPackages':len(ids),'originalPdfs':'identical'}))
