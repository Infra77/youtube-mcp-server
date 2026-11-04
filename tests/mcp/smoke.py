"""Small bounded protocol smoke probe. Full E2E uses the maintained Java MCP SDK."""
import json, os, queue, subprocess, threading, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def smoke(command=None):
    jdk=next((ROOT/'.tools').glob('jdk-21*'),None)
    java=str(jdk/'bin/java.exe') if jdk else str(Path(os.environ['JAVA_HOME'])/'bin'/('java.exe' if os.name=='nt' else 'java'))
    env=dict(os.environ, CURATOR_MODE='fixture')
    if not env.get('DB_PASSWORD'):
        env['DB_PASSWORD']=(ROOT/'.local/db-password').read_text().strip()
    events=queue.Queue()
    stderr=[]
    launch=command or [java,'-Djdk.net.unixdomain.tmpdir='+os.environ.get('CURATOR_SOCKET_DIR',str(ROOT/'target')),'-jar',str(ROOT/'target/curator.jar'),'mcp']
    process=subprocess.Popen(launch,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',env=env,cwd=ROOT)
    def stdout():
        for line in process.stdout: events.put(line)
    def diagnostics():
        for line in process.stderr: stderr.append(line)
    threading.Thread(target=stdout,daemon=True).start();threading.Thread(target=diagnostics,daemon=True).start()
    def send(data): process.stdin.write(json.dumps(data)+'\n');process.stdin.flush()
    def request(i,method,params):
        send({'jsonrpc':'2.0','id':i,'method':method,'params':params})
        until=time.monotonic()+45
        while time.monotonic()<until:
            line=events.get(timeout=max(.1,until-time.monotonic()))
            result=json.loads(line)  # any non-protocol stdout is a failing test
            if result.get('id')==i:
                if 'error' in result: raise AssertionError(result['error'])
                return result['result']
        raise TimeoutError(method)
    try:
        init=request(1,'initialize',{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'local-check-smoke','version':'1.0'}})
        send({'jsonrpc':'2.0','method':'notifications/initialized'})
        tools=request(2,'tools/list',{})
        assert 'get_quota_status' in [t['name'] for t in tools['tools']]
        resources=request(3,'resources/list',{})
        assert len(resources['resources'])==5
        result=request(4,'tools/call',{'name':'get_quota_status','arguments':{}})
        assert not result.get('isError'), result
        data=json.loads(result['content'][0]['text'])
        assert data['status']=='ok' and data['fixture'] is True
        return {'status':'PASS','startServer':'PASS','initialize':'PASS','readOnlyTool':'PASS','protocolVersion':init['protocolVersion'],'tools':[t['name'] for t in tools['tools']],'resources':len(resources['resources']),'fixture':True}
    except Exception:
        safe=''.join(stderr).replace(env.get('DB_PASSWORD','unavailable'),'<redacted>')
        (ROOT/'target/smoke-stderr.txt').write_text(safe,encoding='utf-8')
        raise
    finally:
        process.stdin.close()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.terminate();process.wait(timeout=5)
if __name__=='__main__':
    result=smoke(); (ROOT/'target/evidence').mkdir(parents=True,exist_ok=True)
    (ROOT/'target/evidence/smoke.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
