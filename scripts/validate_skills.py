"""Strict YAML and per-skill behavioral-case validation; does not claim agent execution."""
from pathlib import Path
import json,re,sys
try: import yaml
except ImportError: raise SystemExit('Install pinned tooling: python -m pip install -r scripts/requirements-quality.txt')
R=Path(__file__).resolve().parents[1];errors=[]
for p in sorted((R/'.agents/skills').glob('*/SKILL.md')):
 text=p.read_text(encoding='utf-8');parts=text.split('---',2)
 try:
  assert len(parts)==3 and not parts[0].strip();meta=yaml.safe_load(parts[1]);name=meta['name'];assert name==p.parent.name and re.fullmatch('[a-z0-9]+(-[a-z0-9]+)*',name)
  assert isinstance(meta['description'],str) and 1<=len(meta['description'])<=1024
  cases=json.loads((R/'evals'/name/'cases.json').read_text())['cases']
  assert len(cases)>=2 and any(c['kind']=='negative' for c in cases) and any(c['kind']=='positive' for c in cases)
  for c in cases: assert all(c.get(k) for k in ['name','input','expected','forbidden','evidence'])
 except Exception as e:errors.append(f'{p.parent.name}: invalid YAML/name or incomplete behavioral cases ({type(e).__name__})')
print(json.dumps({'status':'FAIL' if errors else 'PASS','errors':errors,'scope':'schema and cases only; actual host runs required separately'},indent=2));sys.exit(bool(errors))
