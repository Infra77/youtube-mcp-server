"""Verify package hashes and probe the actual PowerShell launcher from an isolated extraction."""
from pathlib import Path
import hashlib,zipfile,json,os,importlib.util
from package_policy import verify_archive_members
ROOT=Path(__file__).resolve().parents[1]
archive=ROOT/'release/educational-video-curator-mcp-0.1.0-local.zip'
destination=ROOT/'target/release-probe'
destination.mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as z:
    verify_archive_members(z)
    for member in z.namelist():
        resolved=(destination/member).resolve()
        assert resolved.is_relative_to(destination.resolve()),'Unsafe archive member'
    z.extractall(destination)
package=destination/'educational-video-curator-mcp-0.1.0-local'
count=0
for line in (package/'SHA256SUMS.txt').read_text().splitlines():
    checksum,name=line.split('  ',1)
    assert hashlib.sha256((package/name).read_bytes()).hexdigest()==checksum,name
    count+=1
spec=importlib.util.spec_from_file_location('package_smoke',package/'tests/mcp/smoke.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
os.environ['JAVA_HOME']=str(next((ROOT/'.tools').glob('jdk-21*')))
os.environ['DB_PASSWORD']=(ROOT/'.local/db-password').read_text().strip()
os.environ['CURATOR_SOCKET_DIR']=str(ROOT/'target')
result=module.smoke(['powershell.exe','-NoProfile','-File',str(package/'scripts/start-mcp.ps1'),'-Mode','fixture'])
report={'status':'PASS','checkedFiles':count,'archiveSha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'credentialFilesIncluded':False,'launchMethod':'actual packaged PowerShell script','fixture':True,'independentMachine':False,'protocol':result}
(ROOT/'docs/evidence/package-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
