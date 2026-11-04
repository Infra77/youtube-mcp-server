from pathlib import Path
import csv,sys,json,re
ROOT=Path(__file__).resolve().parents[1]
required={*(f'FR-{i}' for i in range(1,6)),*(f'TQ-{i}' for i in range(1,9)),*(f'SB-{i}' for i in range(1,7)),*(f'SE-{i}' for i in range(1,8)),*(f'SK-{i:02}' for i in range(1,6)),*(f'NFR-{i:02}' for i in range(1,11))}
errors=[]
with (ROOT/'docs/traceability.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
if required-{r['requirement'] for r in rows}: errors.append('Missing requirements: '+str(sorted(required-{r['requirement'] for r in rows})))
for row in rows:
    if row['pr']!='DEFERRED' and not re.fullmatch(r'https://github\.com/[^/]+/[^/]+/pull/\d+',row['pr']):errors.append('Invalid PR reference: '+row['requirement'])
    if '--final' in sys.argv and (row['pr']=='DEFERRED' or any(s in row['status'].lower() for s in ['pending','deferred','separate'])):errors.append('Unresolved final requirement: '+row['requirement'])
    for key in ['artifact','test']:
        for target in filter(None,row[key].split(';')):
            if target=='PENDING':continue
            if not (ROOT/target.split('#')[0]).is_file():errors.append(f"{row['requirement']} missing {key}: {target}")
    if not (ROOT/'.agents/skills'/row['skill']/'SKILL.md').is_file():errors.append('Missing skill '+row['skill'])
    if not (ROOT/'brain/resources'/f"{row['brain_note']}.md").is_file():errors.append('Missing brain note '+row['brain_note'])
print(json.dumps({'status':'FAIL' if errors else 'PASS','requirements':len(required),'rows':len(rows),'errors':errors,'note':'Validates trace links, not completion of explicitly pending live/human/GitHub gates.'},indent=2))
sys.exit(bool(errors))
