#!/usr/bin/env python3
"""H6-B.1 manifest pin check (issue #64; closes the npm-ci/latest gap).

Deliberate failure testing in H6-A proved `npm ci` does NOT reject a
dist-tag (e.g. "latest") reintroduced into a manifest — it installs
whatever the lockfile pins. This gate enforces what npm cannot: every
dependency declaration in the governed manifests must be an EXACT semver
version. Dist-tags ("latest", "next", ...), ranges (^ ~ > < = x *), OR
bars, and URL/git/file specifiers are all rejected.

Scope: dependencies and devDependencies of the governed manifests that
exist in the tree. Absent manifests are skipped (the repo has no root
manifest by recorded decision). optionalDependencies/peerDependencies are
scanned too when present — apps declare none today, and a future one must
still be exact.

Exit 0 = PASS, exit 1 = violations found, exit 2 = environment failure.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MANIFESTS = [
    "package.json",
    "apps/web/package.json",
    "apps/mobile/package.json",
]

SECTIONS = ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies")

# Exact semver only: MAJOR.MINOR.PATCH with optional pre-release/build suffix.
EXACT = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def main():
    failures = []
    scanned = 0
    for rel in MANIFESTS:
        path = ROOT / rel
        if not path.exists():
            print(f"SKIP: {rel} absent (no root manifest by recorded decision)")
            continue
        try:
            manifest = json.loads(path.read_text())
        except json.JSONDecodeError as err:
            print(f"FAIL:\n- {rel}: unparseable JSON ({err})")
            return 1
        for section in SECTIONS:
            for name, spec in (manifest.get(section) or {}).items():
                scanned += 1
                if not isinstance(spec, str) or not EXACT.fullmatch(spec.strip()):
                    failures.append(f"{rel}: {section}.{name} = {spec!r} is not an exact version")

    if failures:
        print("FAIL: unpinned dependency declarations found (exact semver required).")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS: manifest pin check completed ({scanned} declarations, all exact).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
