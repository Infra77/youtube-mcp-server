"""Local supplemental source scanner. Does not substitute for hosted secret scanning."""
from pathlib import Path
import re,sys,json
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'google_api_key':re.compile(r'AIza[0-9A-Za-z_-]{35}'),
 'oauth_access_token':re.compile(r'ya29\.[0-9A-Za-z_-]{20,}'),
 'private_key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'oauth_refresh_literal':re.compile(r'"refresh_token"\s*:\s*"(?!synthetic|fake|test)[^"]{20,}"'),
}
EXCLUDE={'.tools','.local','.git','target','source-text','release','__pycache__'}
def scan(root):
    findings=[]
    for p in root.rglob('*'):
        if not p.is_file() or any(x in EXCLUDE for x in p.relative_to(root).parts) or p.suffix not in {'.java','.py','.ps1','.md','.json','.yml','.yaml','.xml','.properties','.sql'}: continue
        for kind,pattern in PATTERNS.items():
            if pattern.search(p.read_text(encoding='utf-8',errors='ignore')):findings.append({'file':str(p.relative_to(root)),'kind':kind})
    return findings
def selftest():
    import tempfile
    with tempfile.TemporaryDirectory(dir=ROOT/'target') as folder:
        p=Path(folder)/'secret.json';p.write_text('AIza'+'A'*35)
        assert scan(Path(folder))
        p.write_text('{"token":"synthetic-fixture"}')
        assert not scan(Path(folder))
if __name__=='__main__':
    (ROOT/'target').mkdir(exist_ok=True);selftest();findings=scan(ROOT)
    print(json.dumps({'status':'FAIL' if findings else 'PASS','selfTest':'PASS','findings':findings,'scope':'source files only; excludes local credentials, dependency cache, build output and supplied source text'},indent=2));sys.exit(bool(findings))
