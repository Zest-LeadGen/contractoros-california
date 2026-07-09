#!/usr/bin/env python3
import argparse
import json
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
    'pull-requests: read',
    'production_readiness',
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


def event_payload():
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if event_path and Path(event_path).exists():
        try:
            return json.loads(Path(event_path).read_text())
        except Exception:
            return {}
    return {}


def is_pr_context(payload):
    return bool(os.getenv('GITHUB_BASE_REF')) or os.getenv('GITHUB_EVENT_NAME') == 'pull_request' or 'pull_request' in payload


def is_push_context(payload):
    return os.getenv('GITHUB_EVENT_NAME') == 'push' or ('before' in payload and 'after' in payload)


def changed_files_pr(payload):
    base_ref = os.getenv('GITHUB_BASE_REF') or (payload.get('pull_request') or {}).get('base', {}).get('ref')
    candidates = []
    if base_ref:
        candidates.append(['diff', '--name-only', f'origin/{base_ref}...HEAD'])
        candidates.append(['diff', '--name-only', f'{base_ref}...HEAD'])
    for args in candidates:
        out = git(args)
        if out:
            return sorted(set(out))
    return []


def changed_files_push(payload):
    before = os.getenv('GITHUB_EVENT_BEFORE') or payload.get('before')
    after = os.getenv('GITHUB_SHA') or payload.get('after') or 'HEAD'
    if before and after and str(before).strip('0'):
        out = git(['diff', '--name-only', f'{before}...{after}'])
        if out:
            return sorted(set(out))
    out = git(['diff', '--name-only', 'HEAD~1...HEAD'])
    return sorted(set(out)) if out else []


def changed_files_local():
    out = []
    for cmd in (
        ['diff', '--name-only', 'HEAD'],
        ['diff', '--name-only', '--cached'],
        ['ls-files', '--others', '--exclude-standard'],
    ):
        out.extend(git(cmd))
    return sorted(set(out))


def all_tracked_files():
    names = []
    for cmd in (['ls-files'], ['ls-files', '--others', '--exclude-standard']):
        names.extend(git(cmd))
    return sorted(set(names))


def resolve_scan_files(manual_all_files=False):
    payload = event_payload()
    if manual_all_files:
        files = all_tracked_files()
        return files, 'manual-all-files'
    if is_pr_context(payload):
        files = changed_files_pr(payload)
        if not files:
            print('FAIL: PR context detected but no changed files were resolved.')
            return None, 'pull_request'
        return files, 'pull_request'
    if is_push_context(payload):
        files = changed_files_push(payload)
        return files, 'push'
    return changed_files_local(), 'local-changes'


def textfile(path):
    return path.suffix in SUF or path.name == 'CODEOWNERS'


def self_reference_literal(rel, line):
    stripped = line.strip()
    return rel == 'scripts/control/check_forbidden_scope.py' and (
        stripped.startswith("'") or stripped.startswith('"')
    )


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
    parser.add_argument('--all-files', action='store_true', help='manual full-repo scan mode; not default CI behavior')
    args = parser.parse_args()
    if args.lockfiles_only:
        return lockfiles()

    rel_files, mode = resolve_scan_files(manual_all_files=args.all_files)
    if rel_files is None:
        return 1

    print(f'Forbidden-scope scan mode: {mode}')
    print('Changed files scanned:')
    if rel_files:
        for rel in rel_files:
            print(f'- {rel}')
    else:
        print('- none')

    rg = re.compile('|'.join(re.escape(term) for term in TERMS), re.I)
    findings = []
    fail = []
    for rel in rel_files:
        path = ROOT / rel
        if not path.exists():
            continue
        if any(part in SKIP for part in path.parts) or not textfile(path):
            continue
        for line_number, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
            if self_reference_literal(rel, line):
                continue
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
    print('PASS: no forbidden implementation-looking hits found in scanned files.')
    return lockfiles()


if __name__ == '__main__':
    sys.exit(main())
