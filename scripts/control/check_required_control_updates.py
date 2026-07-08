#!/usr/bin/env python3
import re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; MATRIX=ROOT/'docs/project-control/control-file-update-matrix.yml'
def git_changed():
    out=[]
    for cmd in (['git','diff','--name-only','HEAD'],['git','diff','--name-only','--cached'],['git','ls-files','--others','--exclude-standard']):
        p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode==0: out += [x for x in p.stdout.splitlines() if x]
    return sorted(set(out))
def parse(txt):
    rules=[]; cur=None; key=None
    for raw in txt.splitlines():
        s=raw.strip()
        if not s or s.startswith('#') or s=='rules:': continue
        if s.startswith('- pattern:'):
            if cur: rules.append(cur)
            cur={'pattern':s.split(':',1)[1].strip().strip('"')}; key=None; continue
        if cur is None: continue
        if re.match(r'^[A-Za-z_]+:',s):
            k,v=s.split(':',1); k=k.strip(); v=v.strip()
            if v: cur[k]=v.strip('"'); key=None
            else: cur[k]=[]; key=k
        elif s.startswith('- ') and key: cur.setdefault(key,[]).append(s[2:].strip().strip('"'))
    if cur: rules.append(cur)
    return rules
def match(pat,path): return path.startswith(pat[:-3]) if pat.endswith('/**') else path==pat
def hassec(text,sec): return re.search(rf'^#+\s+(?:\d+\.\s*)?{re.escape(sec)}\s*$',text,re.I|re.M)
def main():
    if not MATRIX.exists(): print('FAIL: matrix missing'); return 1
    changed=git_changed(); rules=parse(MATRIX.read_text()); reports=list((ROOT/'docs/project-control').glob('phase_*_report.md'))
    body='\n'.join(p.read_text(errors='replace') for p in reports); low=body.lower(); fail=[]
    if not reports: fail.append('No phase report found.')
    if not hassec(body,'Documentation Impact'): fail.append("No phase report contains 'Documentation Impact'.")
    matched=[]
    for f in changed:
        for r in rules:
            if match(str(r.get('pattern','')),f): matched.append(r); break
    for r in matched:
        for sec in r.get('required_report_sections',[]) or []:
            if not hassec(body,str(sec)): fail.append(f'Missing section for {r.get("pattern")}: {sec}')
        for req in r.get('required_control_updates',[]) or []:
            marker=f'{str(req).lower()}: reviewed, no update required'
            backtick=f'`{str(req).lower()}`: reviewed, no update required'
            if str(req) not in changed and marker not in low and backtick not in low: fail.append(f'{req} not changed and no reviewed/no-update-required declaration found')
    print('Changed files considered by matrix:'); [print('-',x) for x in changed]
    print(f'Matrix rules parsed: {len(rules)}'); print(f'Matched rules: {len(matched)}')
    if fail: print('FAIL:'); print('\n'.join(f'- {x}' for x in fail)); return 1
    print('PASS: required control update check completed.'); return 0
if __name__=='__main__': sys.exit(main())
