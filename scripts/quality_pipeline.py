"""Local-check coordinator with deterministic failure-reporting tests."""
from pathlib import Path
import datetime,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def maven(*goals):
 script=str(R/'scripts/build.ps1').replace("'","''")
 args=','.join("'"+g+"'" for g in goals)
 return ['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-Command',f"& '{script}' -Goals @({args})"]
steps=[('build',maven('clean','package','-DskipTests')),
 ('tests',maven('verify')),
 ('formatting',maven('spotless:check')),
 ('documentation',[sys.executable,'scripts/validate_docs.py']),
 ('traceability',[sys.executable,'scripts/validate_traceability.py']),
 ('packagePrivacy',[sys.executable,'tests/test_package_privacy.py']),
 ('skillSchema',[sys.executable,'scripts/validate_skills.py']),
 ('secretScan',[str(R/'.tools/gitleaks/gitleaks.exe'),'dir','.', '--config','.gitleaks.toml','--redact','--no-banner','--report-format','json','--report-path','target/evidence/gitleaks.json']),
 ('startServerAndReadOnlyTool',[sys.executable,'tests/mcp/smoke.py'])]
def pipeline(run,items=steps):
 report={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'fixture','overall':'FAIL',**{name:'NOT_RUN' for name,_ in items}}
 for name,cmd in items:
  try:code=run(cmd)
  except (OSError,subprocess.TimeoutExpired):code=1
  report[name]='PASS' if code==0 else 'FAIL'
  if code:return report
 report['overall']='PASS';report['startServer']='PASS';report['readOnlyTool']='PASS'
 return report
def selftest():
 for failure in range(len(steps)):
  counter=[0]
  def run(cmd):
   n=counter[0];counter[0]+=1;return 1 if n==failure else 0
  result=pipeline(run);assert result['overall']=='FAIL';assert result[steps[failure][0]]=='FAIL';assert counter[0]==failure+1
 def timeout(cmd):raise subprocess.TimeoutExpired(cmd,1)
 assert pipeline(timeout)['overall']=='FAIL'
 assert pipeline(lambda cmd:0)['overall']=='PASS'
 return {'status':'PASS','cases':len(steps)+2,'scope':'coordinator failure, missing command/timeout propagation; real host skill evaluations remain separate'}
if __name__=='__main__':
 (R/'target/evidence').mkdir(parents=True,exist_ok=True)
 if '--self-test' in sys.argv:
  result=selftest();name='local-check-negative.json'
 else:
  result=pipeline(lambda cmd:subprocess.run(cmd,cwd=R,timeout=1200).returncode);name='local-check.json'
 (R/'target/evidence').mkdir(parents=True,exist_ok=True)
 (R/'target/evidence'/name).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(result.get('overall',result.get('status'))!='PASS')
