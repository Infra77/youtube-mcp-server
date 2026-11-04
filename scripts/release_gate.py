"""Evidence gate: development checks are not final client acceptance."""
from pathlib import Path
import argparse,json,sys
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');a=p.parse_args()
manifest=json.loads((R/'docs/acceptance-evidence.json').read_text())
missing=[]
for item in manifest['gates']:
 if not a.final and item['kind']=='external':continue
 if item['status']!='PASS' or not item.get('evidence'):missing.append(item['id']);continue
 for path in item['evidence']:
  if not path.startswith('https://') and not (R/path).is_file():missing.append(item['id']+': missing '+path)
print(json.dumps({'mode':'final' if a.final else 'local','status':'FAIL' if missing else 'PASS','missing':missing,'warning':'Human reviewers must verify artifact contents, commit identity and actual external run results; this script cannot authenticate signoffs.'},indent=2));sys.exit(bool(missing))
