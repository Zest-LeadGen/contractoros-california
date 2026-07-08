#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TERMS = [
    'firebase',
    'airtable',
    'stripe',
    'payment',
    'auth',
    'login',
    'user account',
    'score',
    'readiness',
    'pass/fail',
    'analytics',
    'localStorage',
    'sessionStorage',
    'fetch',
    'XMLHttpRequest',
]
ALLOW = [
    'no ',
    'blocked',
    'not included',
    'not authorized',
    'does not',
    'forbidden',
    'explicit exclusion',
    'explicitly not',
    'without',
    'do not',
    'future',
    'roadmap',
    'warning',
    'blocked-scope',
    'scope',
    'risk',
    'known gap',
    'non-goal',
    'claim',
    'documentation',
    'read-only permissions',
    'not added',
    'terms=',
    'fetch-depth',
]
SKIP = {'.git', 'node_modules', '.expo', 'dist', 'build', 'coverage', '__pycache__'}
SUF = {'.js', '.jsx', '.ts', '.tsx', '.json', '.md', '.yml', '.yaml', '.py', '.txt'}
LOCKFILES = [
    'package-lock.json',
    'apps/mobile/package-lock.json',
    'apps/web/package-lock.json',
]


def git(args):
    try:
        proc = subprocess.run(
            ['git'] + args,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        return []
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def changed_files():
    base = os.getenv('GITHUB_BASE_REF')
    before = os.getenv('GITHUB_EVENT_BEFORE') or os.getenv('BEFORE_SHA')
    candidates = []
    if base:
        candidates.append(['diff', '--name-only', f'origin/{base}...HEAD'])
        candidates.append(['diff', '--name-only', f'{base}...HEAD'])
    if before and before.strip('0'):
        candidates.append(['diff', '--name-only', f'{before}...HEAD'])
    candidates.extend(
        [
            ['diff', '--name-only', 'HEAD'],
            ['diff', '--name-only', '--cached'],
            ['ls-files', '--others', '--exclude-standard'],
        ]
    )
    for args in candidates:
        out = git(args)
        if out:
            return sorted(set(out))
    return []


def tracked_changed_paths():
    files = changed_files()
    if files:
        return [ROOT / path for path in files if (ROOT / path).exists()]
    names = []
    for cmd in (['ls-files'], ['ls-files', '--others', '--exclude-standard']):
        names.extend(git(cmd))
    return [ROOT / name for name in sorted(set(names))]


def textfile(path):
    return path.suffix in SUF or path.name == 'CODEOWNERS'


def lockfiles():
    pats = ['applied-caas', 'internal.api.openai.org', 'sandbox', 'localhost', '127.0.0.1']
    fail = []
    for rel in LOCKFILES:
        path = ROOT / rel
        if not path.exists():
            print(f'PASS: lockfile absent: {rel}')
            continue
        for line_number, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
            if any(token in line for token in pats):
                fail.append(f'{rel}:{line_number}: {line[:160]}')
    if fail:
        print('FAIL: lockfile contamination detected')
        print('\n'.join(fail))
        return 1
    print('PASS: lockfile contamination check completed.')
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lockfiles-only', action='store_true')
    args = parser.parse_args()
    if args.lockfiles_only:
        return lockfiles()

    rg = re.compile('|'.join(re.escape(term) for term in TERMS), re.I)
    findings = []
    fail = []
    for path in tracked_changed_paths():
        if any(part in SKIP for part in path.parts) or not textfile(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
            if rg.search(line):
                if any(token in line.lower() for token in ALLOW):
                    findings.append(f'allowed warning/blocked-scope text: {rel}:{line_number}: {line.strip()[:160]}')
                else:
                    fail.append(f'forbidden implementation-looking hit: {rel}:{line_number}: {line.strip()[:160]}')

    print('Forbidden-scope findings:')
    for finding in findings[:160]:
        print('-', finding)
    if fail:
        print('FAIL:')
        print('\n'.join(f'- {item}' for item in fail))
        return 1
    print('PASS: no forbidden implementation-looking hits found in changed files.')
    return lockfiles()


if __name__ == '__main__':
    sys.exit(main())
