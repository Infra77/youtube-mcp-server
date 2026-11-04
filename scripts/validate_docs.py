"""Validate actual local links, required note metadata, skills and traceability paths."""
from pathlib import Path
import re, json, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
notes=list((ROOT/'brain').rglob('*.md'))
titles={}
for p in notes: titles.setdefault(p.stem,[]).append(p)
for title,paths in titles.items():
    if len(paths)>1: errors.append(f'Duplicate note basename: {title}')
for p in notes:
    text=p.read_text(encoding='utf-8')
    if 'type: research' in text:
        for field in ['type','status','author','reviewed','requirements','source_urls']:
            if not re.search(r'^'+field+r':\s*\S',text,re.M): errors.append(f'{p.name}: missing {field}')
    for target in re.findall(r'\[\[([^\]|#]+)',text):
        if target not in titles: errors.append(f'{p.name}: broken wikilink {target}')
for name in ['inbox','projects','areas','resources','archive']:
    if not (ROOT/'brain'/name).is_dir(): errors.append(f'Missing PARA directory: {name}')
for p in [ROOT/'brain/index.md',ROOT/'brain/log.md',ROOT/'AGENTS.md']:
    if not p.exists(): errors.append(f'Missing {p.name}')
for name in ['brain-ingest','brain-refine','brain-query','local-check','video-to-playlist']:
    p=ROOT/'.agents/skills'/name/'SKILL.md'
    if not p.exists(): errors.append(f'Missing skill {name}');continue
    text=p.read_text(encoding='utf-8')
    if not text.startswith('---\n') or f'name: {name}\n' not in text or not re.search(r'^description: .+',text,re.M):errors.append(f'Invalid skill metadata: {name}')
    citations=re.findall(r'\[\[([^\]|#]+)',text)
    if not citations: errors.append(f'Skill lacks research citation: {name}')
    for title in citations:
        if title not in titles or 'status: distilled' not in titles[title][0].read_text(encoding='utf-8'):errors.append(f'Invalid distilled citation: {name}/{title}')
    cases=ROOT/'evals'/name/'cases.json'
    try:
        data=json.loads(cases.read_text());assert len(data['cases'])>=2
    except Exception: errors.append(f'Invalid evaluation cases: {name}')
for p in (ROOT/'docs/adr').glob('*.md'):
    citations=re.findall(r'\[\[([^\]|#]+)',p.read_text(encoding='utf-8'))
    if not citations or any(t not in titles for t in citations):errors.append(f'ADR missing valid citation: {p.name}')
for p in [*notes,*list((ROOT/'docs').rglob('*.md'))]:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#') and not (p.parent/target.split('#')[0]).exists():errors.append(f'{p.name}: broken relative link {target}')
print(json.dumps({'status':'FAIL' if errors else 'PASS','notes':len(notes),'researchNotes':sum('type: research' in p.read_text(encoding='utf-8') for p in notes),'skills':5,'errors':errors},indent=2))
sys.exit(bool(errors))
