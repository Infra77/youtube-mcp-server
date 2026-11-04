"""Query OSV for exact CycloneDX Maven component versions; sends coordinates only.

Generate target/bom.json with CycloneDX first. Fails closed on service errors.
This is a known-advisory check, not proof that dependencies have no vulnerabilities.
"""
from pathlib import Path
import json, urllib.request, sys, datetime
R=Path(__file__).resolve().parents[1]
bom=json.loads((R/'target/bom.json').read_text(encoding='utf-8'))
components=[c for c in bom['components'] if c.get('purl','').startswith('pkg:maven/')]
queries=[{'package':{'ecosystem':'Maven','name':c['group']+':'+c['name']},'version':c['version']} for c in components]
results=[]
for offset in range(0,len(queries),100):
 batch=queries[offset:offset+100]
 request=urllib.request.Request('https://api.osv.dev/v1/querybatch',data=json.dumps({'queries':batch}).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(request,timeout=60) as response: data=json.load(response)
 if len(data['results'])!=len(batch): raise RuntimeError('Incomplete OSV response')
 for q,r in zip(batch,data['results']):
  if r.get('vulns'):results.append({'package':q['package']['name'],'version':q['version'],'advisories':[v['id'] for v in r['vulns']]})
not_affected=[]
config=(R/'src/main/resources/application.yml').read_text()
pom=(R/'pom.xml').read_text()
stdio_only='web-application-type: none' in config and 'stdio: true' in config and not any(x in pom for x in ['starter-web','server-webmvc','server-webflux'])
for finding in results:
 if stdio_only and finding['package']=='io.modelcontextprotocol.sdk:mcp-core' and 'GHSA-8jxr-pr72-r468' in finding['advisories']:
  finding['advisories'].remove('GHSA-8jxr-pr72-r468')
  not_affected.append({'id':'GHSA-8jxr-pr72-r468','reason':'Advisory requires HTTP MCP listener; shipped server is stdio-only with web application disabled. Reassess before any transport change.','source':'https://github.com/modelcontextprotocol/java-sdk/security/advisories/GHSA-8jxr-pr72-r468','humanReview':'pending'})
results=[r for r in results if r['advisories']]
report={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'service':'OSV','components':len(components),'status':'FAIL' if results else 'PASS','findings':results,'notAffected':not_affected,'scope':'exact runtime versions; explicit transport-specific applicability disposition retained, human review required'}
(R/'target/evidence').mkdir(exist_ok=True)
(R/'target/evidence/dependency-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2));sys.exit(bool(results))
