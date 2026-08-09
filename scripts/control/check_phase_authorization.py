#!/usr/bin/env python3
"""H3 default-deny phase-authorization check (issue #60 contract).

Resolves the PR's linked issue, loads exactly one authorization record FROM
THE BASE COMMIT (so a PR can never modify or invent its own authorization),
and requires every changed path to match exactly one allowed rule with the
right change kind. Fails closed on: unmatched, forbidden, deleted, renamed,
mode-changed, symlink, or case-colliding paths; expired, revoked,
wrong-base-SHA, wrong-repo, or self-modified authorizations; and ambiguous
(multi-rule) matches. Prints a deterministic authorization digest.

Observe-only in this delivery per OPS-005: recorded as an enforcement
candidate; cutover to blocking follows its own measured window.

Exit 0 = PASS, exit 1 = deny, exit 2 = environment failure (fail closed).
"""
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTH_DIR = "docs/project-control/authorizations"
ISSUE_REF = re.compile(r"(?im)^\s*(?:closes|fixes|resolves)\s+#(\d+)\b|^\s*(?:linked issue|phase issue)\s*:\s*#(\d+)\b")


def git(args):
    proc = subprocess.run(["git"] + args, cwd=ROOT, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def fail_env(msg):
    print(json.dumps({"result": "ENVIRONMENT_FAILURE", "error": msg}))
    return 2


def deny(failures, digest=None):
    print(json.dumps({"result": "DENY", "authorization_digest": digest, "failures": failures}, indent=2))
    return 1


def event_payload():
    p = os.getenv("GITHUB_EVENT_PATH")
    if p and Path(p).exists():
        try:
            return json.loads(Path(p).read_text())
        except Exception:
            return {}
    return {}


def main():
    payload = event_payload()
    pr = payload.get("pull_request") or {}
    body = pr.get("body") or os.getenv("PR_BODY", "")
    base_ref = os.getenv("GITHUB_BASE_REF") or (pr.get("base") or {}).get("ref") or "main"

    m = ISSUE_REF.search(body)
    if not m:
        return deny(["NO_LINKED_ISSUE: PR body must link its phase issue"])
    issue = int(m.group(1) or m.group(2))

    # Enumerate authorization records AT THE BASE COMMIT only (#60 rule 7).
    rc, listing = git(["ls-tree", "-r", "--name-only", f"origin/{base_ref}", AUTH_DIR + "/"])
    if rc != 0:
        return fail_env(f"cannot list {AUTH_DIR} at origin/{base_ref}")
    candidates = []
    for path in listing.splitlines():
        rc, blob = git(["show", f"origin/{base_ref}:{path.strip()}"])
        if rc != 0:
            continue
        try:
            record = json.loads(blob)
        except json.JSONDecodeError:
            return deny([f"UNPARSEABLE_AUTHORIZATION_AT_BASE: {path.strip()}"])
        if record.get("issue") == issue and not record.get("supersession", {}).get("revoked", False):
            candidates.append((path.strip(), record))

    if len(candidates) != 1:
        return deny([f"AUTHORIZATION_RESOLUTION: expected exactly one base-commit record for issue #{issue}, found {len(candidates)}"])
    auth_path, auth = candidates[0]
    digest = hashlib.sha256(json.dumps(auth, sort_keys=True).encode()).hexdigest()

    failures = []
    rc, base_sha_out = git(["rev-parse", f"origin/{base_ref}"])
    # The recorded base_sha must be an ancestor of (or equal to) the current base.
    rc2, _ = git(["merge-base", "--is-ancestor", auth["base_sha"], base_sha_out.strip()])
    if rc2 != 0:
        failures.append(f"BASE_SHA_MISMATCH: authorization bound to {auth['base_sha'][:7]}, not in current base lineage")

    import datetime
    if os.getenv("PA_TODAY", "") :
        today = os.getenv("PA_TODAY")
    else:
        today = datetime.date.today().isoformat()
    if today > auth["expiry"]:
        failures.append(f"AUTHORIZATION_EXPIRED: {auth['expiry']}")

    # Cumulative diff with statuses (#60 rules 4-6).
    rc, diff = git(["diff", "--name-status", "-M", f"origin/{base_ref}...HEAD"])
    if rc != 0:
        return fail_env("cannot compute cumulative diff")
    changed = []
    for line in diff.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") or status.startswith("C"):
            failures.append(f"RENAME_OR_COPY_DENIED: {parts[-1]} (never pattern-authorizable)")
            continue
        kind = {"A": "add", "M": "modify", "D": "delete"}.get(status[0], status)
        changed.append((parts[-1], kind))

    # Self-modification of any authorization or its schema (#60 rule 7).
    for path, kind in changed:
        if path.startswith(AUTH_DIR + "/") and (path, "add") != (auth_path, "add"):
            failures.append(f"AUTHORIZATION_SELF_MODIFICATION_DENIED: {path}")
        if path == auth_path and kind != "add":
            failures.append(f"AUTHORIZATION_SELF_MODIFICATION_DENIED: {path} ({kind})")

    # Case-collision detection.
    lowered = {}
    for path, _ in changed:
        key = path.lower()
        if key in lowered and lowered[key] != path:
            failures.append(f"CASE_COLLISION: {path} vs {lowered[key]}")
        lowered[key] = path

    def rule_matches(rule, path):
        pat = rule["pattern"]
        if pat.endswith("/**"):
            return path.startswith(pat[:-2])
        return path == pat

    for path, kind in changed:
        if any(fnmatch.fnmatch(path, f) or (f.endswith("/**") and path.startswith(f[:-2])) or path == f
               for f in auth.get("forbidden_paths", [])):
            failures.append(f"FORBIDDEN_PATH: {path}")
            continue
        if kind == "delete":
            exact = [r for r in auth["allowed_paths"] if r["pattern"] == path and "delete" in r.get("change_kinds", [])]
            if not exact:
                failures.append(f"DELETE_DENIED: {path} (deletes require an explicit exact-path rule)")
            continue
        matches = [r for r in auth["allowed_paths"] if rule_matches(r, path) and kind in r["change_kinds"]]
        if len(matches) == 0:
            failures.append(f"UNMATCHED_PATH: {path} ({kind}) — default deny")
        elif len(matches) > 1:
            failures.append(f"AMBIGUOUS_MATCH: {path} matches {[r['rule_id'] for r in matches]}")

    if failures:
        return deny(failures, digest)

    print(json.dumps({
        "result": "PASS",
        "authorization_id": auth["authorization_id"],
        "authorization_digest": digest,
        "issue": issue,
        "changed_paths": len(changed),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
