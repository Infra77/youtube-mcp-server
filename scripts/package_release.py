"""Build a local review distribution from explicit credential-free paths."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
release=ROOT/'release/educational-video-curator-mcp-0.1.0-local'
if release.exists():
    assert release.resolve().parent == (ROOT/'release').resolve(), 'Unsafe staging path'
    shutil.rmtree(release)
release.mkdir(parents=True,exist_ok=True)
report=json.loads((ROOT/'target/evidence/local-check.json').read_text(encoding='utf-8-sig'))
assert report['overall']=='PASS','Packaging requires successful local-check'
roots=['src','scripts','tests','infra','docs','brain','.agents','evals','.mvn']
files=['pom.xml','mvnw','mvnw.cmd','.gitignore','.gitattributes','.gitleaks.toml','.gitleaksignore','README.md','CHANGELOG.md','AGENTS.md','LICENSE','target/curator.jar']
omitted={'__pycache__','source-text','.local','.tools','.git','workspace.json','workspace-mobile.json'}
for folder in roots:
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and not any(s in omitted for s in p.relative_to(ROOT).parts): files.append(p.relative_to(ROOT).as_posix())
for relative in sorted(set(files)):
    source=ROOT/relative;destination=release/relative
    assert source.is_file(),relative
    destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
quick='''# Local review package 0.1.0

Requires JDK 21, Docker Desktop and Python 3 for checks. Set JAVA_HOME to your installed JDK 21.
The source tree and prebuilt target/curator.jar are included; no Google/DB credentials are included.
From this directory run scripts/start-db.ps1, then configure an MCP host to run
scripts/start-mcp.ps1 -Mode fixture. To rebuild and test, run scripts/build.ps1 and local-check.ps1.
Read README.md and docs/acceptance-status.md. Live Google setup and final human/GitHub gates
remain pending. Do not present fixture results as a real YouTube account.
'''
(release/'README-QUICKSTART.md').write_text(quick,encoding='utf-8')
entries=[]
for p in sorted(release.rglob('*')):
    if not p.is_file() or p.name=='SHA256SUMS.txt':continue
    relative=p.relative_to(release).as_posix()
    assert not any(s in omitted for s in p.relative_to(release).parts),relative
    entries.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+relative)
(release/'SHA256SUMS.txt').write_text('\n'.join(entries)+'\n',encoding='utf-8')
archive=Path(str(release)+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(release.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(release.parent))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'package':str(archive),'files':len(entries)+1,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
