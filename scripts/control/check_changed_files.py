#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXACT={'apps/mobile/package-lock.json','apps/web/package-lock.json','package-lock.json','eas.json'}
PREFIX=('backend/','database/','android/','ios/')
def git(args):
    try:
        p=subprocess.run(['git']+args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except FileNotFoundError:
        return []
    return [x.strip() for x in p.stdout.splitlines() if p.returncode==0 and x.strip()]
def changed():
    base=os.getenv('GITHUB_BASE_REF')
    before=os.getenv('GITHUB_EVENT_BEFORE') or os.getenv('BEFORE_SHA')
    candidates=[]
    if base: candidates.append(['diff','--name-only',f'origin/{base}...HEAD'])
    if before and before.strip('0'): candidates.append(['diff','--name-only',f'{before}...HEAD'])
    candidates += [['diff','--name-only','HEAD'],['diff','--name-only','--cached'],['ls-files','--others','--exclude-standard']]
    for args in candidates:
        out=git(args)
        if out: return sorted(set(out))
    return []
def cat(p):
    if p.startswith('apps/mobile/'): return 'app/mobile'
    if p.startswith('apps/web/'): return 'app/web'
    if p.startswith('docs/project-control/'): return 'docs/project-control'
    if p.startswith('.github/') or p.startswith('scripts/control/'): return 'workflow/control'
    if p in {'package.json','package-lock.json'} or p.endswith('/package.json') or p.endswith('/package-lock.json'): return 'dependency/package'
    if p.startswith(('android/','ios/')) or p=='eas.json': return 'build/native'
    if p.startswith(('backend/','database/')): return 'backend/database'
    return 'unknown'
def body():
    ep=os.getenv('GITHUB_EVENT_PATH')
    if ep and Path(ep).exists():
        try: return (json.loads(Path(ep).read_text()).get('pull_request') or {}).get('body') or ''
        except Exception: pass
    return os.getenv('PR_BODY','')+'\n'+"\n".join(f.read_text(errors='replace') for f in (ROOT/'docs/project-control').glob('phase_*_report.md'))
def main():
    files=changed(); print('Changed files:')
    for f in files: print(f'- {f} [{cat(f)}]')
    text=body().lower(); ok_lane=any(x in text for x in ['control / infrastructure','build / distribution','dependency','explicitly approved','explicit exclusions','forbidden scope confirmation'])
    bad=[f for f in files if (f in EXACT or any(f.startswith(x) for x in PREFIX)) and not ok_lane]
    if bad:
        print('FAIL: forbidden path without allowed lane/report signal:'); print('\n'.join(bad)); return 1
    print('PASS: changed-file lane check completed.'); return 0
if __name__=='__main__': sys.exit(main())
