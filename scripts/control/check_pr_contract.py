#!/usr/bin/env python3
import argparse, json, os, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REQ=['Phase','Lane','Scope','Changed Files','Commands Run','Dependency / Lockfile Handling','Documentation Impact','Forbidden Scope Confirmation','Known Limitations','Next Phase Status']
CLAIMS=['production-ready','public-ready','exam-ready','APK-ready','app-store-ready','launch-ready','fully tested','complete','finalized']
DOWN=['not ','does not prove','do not claim','no ','without','forbidden','blocked','not ready','not complete','not finalized']
def body():
    ep=os.getenv('GITHUB_EVENT_PATH')
    if ep and Path(ep).exists():
        try: return (json.loads(Path(ep).read_text()).get('pull_request') or {}).get('body') or ''
        except Exception: pass
    txt=os.getenv('PR_BODY','')
    if txt.strip(): return txt
    return (ROOT/'.github/pull_request_template.md').read_text(errors='replace')+'\n\n'+'\n\n'.join(p.read_text(errors='replace') for p in sorted((ROOT/'docs/project-control').glob('phase_*_report.md')))
def changed():
    out=[]
    for cmd in (['git','diff','--name-only','HEAD'],['git','diff','--name-only','--cached'],['git','ls-files','--others','--exclude-standard']):
        p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode==0: out += [x for x in p.stdout.splitlines() if x]
    return sorted(set(out))
def hassec(t,s): return re.search(rf'^#+\s+(?:\d+\.\s*)?{re.escape(s)}\s*$',t,re.I|re.M)
def downgraded(line):
    l=line.lower(); return any(x in l for x in DOWN)
def appchg(files): return any(x.startswith(('apps/','android/','ios/','backend/','database/')) or x in {'eas.json','package.json','package-lock.json'} or x.endswith('/package.json') or x.endswith('/package-lock.json') for x in files)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--claims-only',action='store_true'); a=ap.parse_args(); t=body(); fail=[]
    if not t.strip(): fail.append('No PR body or phase report text available.')
    if not a.claims_only:
        for s in REQ:
            if not hassec(t,s): fail.append(f'Missing required PR/report section: {s}')
    for i,line in enumerate(t.splitlines(),1):
        for c in CLAIMS:
            if re.search(r'\b'+re.escape(c.lower())+r'\b', line.lower()) and not downgraded(line): fail.append(f'Line {i}: overclaim {c} lacks downgrade/evidence context: {line.strip()}')
    if appchg(changed()) and 'claim level' not in t.lower(): fail.append('App/source/build/content change detected but claim level wording is missing.')
    if fail: print('FAIL:'); print('\n'.join(f'- {x}' for x in fail)); return 1
    print('PASS: '+('claim-language' if a.claims_only else 'PR/report contract')+' check completed.'); return 0
if __name__=='__main__': sys.exit(main())
