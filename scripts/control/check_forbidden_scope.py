#!/usr/bin/env python3
import argparse, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TERMS=['firebase','airtable','stripe','payment','auth','login','user account','score','readiness','pass/fail','analytics','localStorage','sessionStorage','fetch','XMLHttpRequest']
ALLOW=['no ','blocked','not included','not authorized','does not','forbidden','explicit exclusion','explicitly not','without','do not','future','roadmap','warning','blocked-scope','scope','risk','known gap','non-goal','claim','documentation','read-only permissions','not added','terms=','fetch-depth']
SKIP={'.git','node_modules','.expo','dist','build','coverage','__pycache__'}
SUF={'.js','.jsx','.ts','.tsx','.json','.md','.yml','.yaml','.py','.txt'}
def tracked():
    names=[]
    for cmd in (['git','ls-files'],['git','ls-files','--others','--exclude-standard']):
        p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode==0: names += [x for x in p.stdout.splitlines() if x]
    return [ROOT/x for x in sorted(set(names))]
def textfile(p): return p.suffix in SUF or p.name=='CODEOWNERS'
def lockfiles():
    pats=['applied-caas','internal.api.openai.org','sandbox','localhost','127.0.0.1']; fail=[]
    for p in [ROOT/'package-lock.json',ROOT/'apps/mobile/package-lock.json',ROOT/'apps/web/package-lock.json']:
        if not p.exists(): print(f'PASS: lockfile absent: {p.relative_to(ROOT)}'); continue
        for i,l in enumerate(p.read_text(errors='replace').splitlines(),1):
            if any(x in l for x in pats): fail.append(f'{p.relative_to(ROOT)}:{i}: {l[:160]}')
    if fail: print('FAIL: lockfile contamination detected'); print('\n'.join(fail)); return 1
    print('PASS: lockfile contamination check completed.'); return 0
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--lockfiles-only',action='store_true'); a=ap.parse_args()
    if a.lockfiles_only: return lockfiles()
    rg=re.compile('|'.join(re.escape(t) for t in TERMS),re.I); findings=[]; fail=[]
    for p in tracked():
        if any(part in SKIP for part in p.parts) or not textfile(p): continue
        rel=p.relative_to(ROOT).as_posix()
        for i,l in enumerate(p.read_text(errors='replace').splitlines(),1):
            if rg.search(l):
                if any(x in l.lower() for x in ALLOW): findings.append(f'allowed warning/blocked-scope text: {rel}:{i}: {l.strip()[:160]}')
                else: fail.append(f'forbidden implementation-looking hit: {rel}:{i}: {l.strip()[:160]}')
    print('Forbidden-scope findings:')
    for x in findings[:160]: print('-',x)
    if fail: print('FAIL:'); print('\n'.join(f'- {x}' for x in fail)); return 1
    print('PASS: no forbidden implementation-looking hits found.'); return lockfiles()
if __name__=='__main__': sys.exit(main())
