#!/usr/bin/env python3
"""Default-deny phase-authorization check (H3 #60 contract, H5-D #118 extensions).

Resolves the PR's linked issue and validates every changed path against
exactly one governing authorization record. Two resolution modes:

BASE mode (H3 behavior): exactly one live (non-revoked) record for the issue
exists at the base commit; the PR may not touch the authorization directory
at all.

BOOTSTRAP mode (H5-D): the PR introduces exactly one new record for its
linked issue. Conditions, all mandatory:
- the record's filename matches its authorization_id and it is not revoked;
- its evidence_id is an on-platform owner comment reference for the linked
  issue (issue-<N>-comment-<id>);
- its repository field matches the repository the check runs in;
- every live base record for the issue is closed in the same PR by a
  content-verified supersession edit — the only permitted delta is
  supersession.revoked false->true plus revocation_evidence null->string
  naming the new record — and each closed ID is listed in the new record's
  supersedes array;
- the new record's own addition and each closure edit must themselves match
  exact-path allowed rules in the new record (self-consistent scope).
Trust root for bootstrap: CODEOWNERS owner review on docs/project-control/**
plus owner-only merge authority; the checker enforces machine-verifiable
shape, the owner review supplies the authorization judgment.

RELOCATE (H5-D): a content-identical rename (git R100) is authorizable only
by a rule carrying change_kind "relocate" with pattern == exact old path and
"to" == exact new path. Renames with content drift (R<100), copies, and
pattern-based renames remain denied. Authorization records are never
deletable or relocatable.

Everything else fails closed as before: unmatched, forbidden, deleted,
mode-changed, symlink, or case-colliding paths; expired, revoked,
wrong-base-SHA, or self-modified authorizations; ambiguous (multi-rule)
matches. Prints a deterministic authorization digest.

ARMED as of H5-D per owner decision on issue #118 (comment 5233703034,
PATH_WALL_DECISION=ARM_NOW); the OPS-005 observe-only window has ended.

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
PA_DIR = "docs/project-control/authorizations"
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


def load_record(ref, path):
    rc, blob = git(["show", f"{ref}:{path}"])
    if rc != 0:
        return None, f"unreadable at {ref}"
    try:
        return json.loads(blob), None
    except json.JSONDecodeError:
        return None, f"unparseable at {ref}"


def is_live(record, issue):
    return (record.get("issue") == issue
            and not record.get("supersession", {}).get("revoked", False))


def main():
    payload = event_payload()
    pr = payload.get("pull_request") or {}
    body = pr.get("body") or os.getenv("PR_BODY", "")
    base_ref = os.getenv("GITHUB_BASE_REF") or (pr.get("base") or {}).get("ref") or "main"
    base = f"origin/{base_ref}"

    m = ISSUE_REF.search(body)
    if not m:
        return deny(["NO_LINKED_ISSUE: PR body must link its phase issue"])
    issue = int(m.group(1) or m.group(2))

    # Cumulative diff with statuses (#60 rules 4-6). -M keeps renames visible
    # so they can be exactly authorized (H5-D) or denied.
    rc, diff = git(["diff", "--name-status", "-M", f"{base}...HEAD"])
    if rc != 0:
        return fail_env("cannot compute cumulative diff")
    changed = []       # (path, kind) with kind in add/modify/delete or raw status
    relocations = []   # (old_path, new_path, similarity_score)
    structural = []
    for line in diff.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("C"):
            structural.append(f"COPY_DENIED: {parts[-1]} (copies are never authorizable)")
            continue
        if status.startswith("R"):
            try:
                score = int(status[1:])
            except ValueError:
                score = 0
            relocations.append((parts[1], parts[2], score))
            continue
        kind = {"A": "add", "M": "modify", "D": "delete"}.get(status[0], status)
        changed.append((parts[-1], kind))

    # Enumerate authorization records AT THE BASE COMMIT (#60 rule 7).
    rc, listing = git(["ls-tree", "-r", "--name-only", base, PA_DIR + "/"])
    if rc != 0:
        return fail_env(f"cannot list {PA_DIR} at {base}")
    base_records = {}
    for path in [p.strip() for p in listing.splitlines() if p.strip()]:
        record, err = load_record(base, path)
        if record is None:
            return deny([f"UNPARSEABLE_AUTHORIZATION_AT_BASE: {path} ({err})"])
        base_records[path] = record
    base_live = [(p, r) for p, r in sorted(base_records.items()) if is_live(r, issue)]

    # Partition authorization-directory changes.
    pa_adds = [p for p, k in changed if p.startswith(PA_DIR + "/") and k == "add"]
    pa_mods = [p for p, k in changed if p.startswith(PA_DIR + "/") and k == "modify"]
    pa_dels = [p for p, k in changed if p.startswith(PA_DIR + "/") and k == "delete"]
    pa_other = [p for p, k in changed if p.startswith(PA_DIR + "/")
                and k not in ("add", "modify", "delete")]
    pa_reloc = [(o, n) for o, n, _ in relocations
                if o.startswith(PA_DIR + "/") or n.startswith(PA_DIR + "/")]

    # Records the PR itself introduces for the linked issue (bootstrap candidates).
    added_for_issue = []
    for p in sorted(pa_adds):
        record, err = load_record("HEAD", p)
        if record is None:
            return deny([f"UNPARSEABLE_AUTHORIZATION_IN_PR: {p} ({err})"])
        if record.get("issue") == issue:
            added_for_issue.append((p, record))

    failures = list(structural)
    verified_closures = set()

    if len(added_for_issue) > 1:
        return deny([f"BOOTSTRAP_MULTIPLE_RECORDS: PR adds {len(added_for_issue)} records for issue #{issue}; exactly one is allowed"])

    bootstrap = len(added_for_issue) == 1
    if bootstrap:
        permit_path, permit = added_for_issue[0]
        if Path(permit_path).name != f"{permit.get('authorization_id')}.json":
            return deny([f"BOOTSTRAP_FILENAME_MISMATCH: {permit_path} vs authorization_id {permit.get('authorization_id')!r}"])
        if permit.get("supersession", {}).get("revoked", False):
            return deny([f"BOOTSTRAP_RECORD_REVOKED: {permit_path} introduced already revoked"])
        if not re.fullmatch(rf"issue-{issue}-comment-[0-9]+", str(permit.get("evidence_id", ""))):
            return deny([f"BOOTSTRAP_EVIDENCE_FORMAT: evidence_id must be issue-{issue}-comment-<id>, got {permit.get('evidence_id')!r}"])
        env_repo = os.getenv("GITHUB_REPOSITORY")
        if env_repo and permit.get("repository") != env_repo:
            return deny([f"BOOTSTRAP_REPOSITORY_MISMATCH: record bound to {permit.get('repository')!r}, running in {env_repo!r}"])

        supersedes = set(permit.get("supersession", {}).get("supersedes", []))
        # Every live base record for the issue must be closed in this PR.
        for bp, br in base_live:
            bid = br.get("authorization_id")
            if bp not in pa_mods:
                failures.append(f"BOOTSTRAP_CLOSURE_REQUIRED: live base record {bid} ({bp}) must be revoked in the same PR")
                continue
            if bid not in supersedes:
                failures.append(f"SUPERSEDES_MISSING: {bid} closed by this PR but absent from {permit['authorization_id']}.supersession.supersedes")
        # Every modified record must be a verified supersession closure.
        for mp in sorted(pa_mods):
            base_rec = base_records.get(mp)
            if base_rec is None:
                failures.append(f"CLOSURE_TARGET_MISSING_AT_BASE: {mp}")
                continue
            if base_rec.get("issue") != issue:
                failures.append(f"CLOSURE_WRONG_ISSUE: {mp} authorizes issue #{base_rec.get('issue')}, not #{issue}")
                continue
            if base_rec.get("supersession", {}).get("revoked", False):
                failures.append(f"CLOSURE_ALREADY_REVOKED: {mp}")
                continue
            head_rec, err = load_record("HEAD", mp)
            if head_rec is None:
                failures.append(f"UNPARSEABLE_AUTHORIZATION_IN_PR: {mp} ({err})")
                continue
            evidence = head_rec.get("supersession", {}).get("revocation_evidence")
            expected = json.loads(json.dumps(base_rec))
            expected["supersession"]["revoked"] = True
            expected["supersession"]["revocation_evidence"] = evidence
            if not isinstance(evidence, str) or permit["authorization_id"] not in evidence:
                failures.append(f"CLOSURE_EVIDENCE_INVALID: {mp} revocation_evidence must be a string naming {permit['authorization_id']}")
            elif head_rec != expected:
                failures.append(f"CLOSURE_CONTENT_MISMATCH: {mp} changes more than supersession.revoked + revocation_evidence")
            else:
                verified_closures.add(mp)
    else:
        if len(base_live) != 1:
            return deny([f"AUTHORIZATION_RESOLUTION: expected exactly one live base-commit record for issue #{issue}, found {len(base_live)} (and no bootstrap record added)"])
        permit_path, permit = base_live[0]

    digest = hashlib.sha256(json.dumps(permit, sort_keys=True).encode()).hexdigest()

    rc, base_sha_out = git(["rev-parse", base])
    # The recorded base_sha must be an ancestor of (or equal to) the current base.
    rc2, _ = git(["merge-base", "--is-ancestor", permit["base_sha"], base_sha_out.strip()])
    if rc2 != 0:
        failures.append(f"BASE_SHA_MISMATCH: authorization bound to {permit['base_sha'][:7]}, not in current base lineage")

    import datetime
    today = os.getenv("PA_TODAY", "") or datetime.date.today().isoformat()
    if today > permit["expiry"]:
        failures.append(f"AUTHORIZATION_EXPIRED: {permit['expiry']}")

    # Authorization directory integrity (#60 rule 7, H5-D bootstrap carve-outs).
    for p in pa_dels:
        failures.append(f"AUTHORIZATION_DELETE_DENIED: {p} (records are never deletable)")
    for o, n in pa_reloc:
        failures.append(f"AUTHORIZATION_RELOCATE_DENIED: {o} -> {n} (records are never relocatable)")
    for p in pa_other:
        failures.append(f"AUTHORIZATION_SELF_MODIFICATION_DENIED: {p} (unsupported change type)")
    for p in pa_adds:
        if not (bootstrap and p == permit_path):
            failures.append(f"AUTHORIZATION_SELF_MODIFICATION_DENIED: {p} (add)")
    if not bootstrap:
        for p in pa_mods:
            failures.append(f"AUTHORIZATION_SELF_MODIFICATION_DENIED: {p} (modify)")

    # Case-collision detection across every touched path, including rename endpoints.
    lowered = {}
    for path in [p for p, _ in changed] + [x for o, n, _ in relocations for x in (o, n)]:
        key = path.lower()
        if key in lowered and lowered[key] != path:
            failures.append(f"CASE_COLLISION: {path} vs {lowered[key]}")
        lowered[key] = path

    def forbidden(path):
        return any(fnmatch.fnmatch(path, f) or (f.endswith("/**") and path.startswith(f[:-2])) or path == f
                   for f in permit.get("forbidden_paths", []))

    def rule_matches(rule, path):
        pat = rule["pattern"]
        if pat.endswith("/**"):
            return path.startswith(pat[:-2])
        return path == pat

    # Relocations: exact old path -> exact new path, content-identical only.
    for old, new, score in relocations:
        if old.startswith(PA_DIR + "/") or new.startswith(PA_DIR + "/"):
            continue  # already denied above
        if score != 100:
            failures.append(f"RELOCATE_CONTENT_DRIFT_DENIED: {old} -> {new} (R{score}; relocations must be content-identical)")
            continue
        if forbidden(old) or forbidden(new):
            failures.append(f"FORBIDDEN_PATH: {old} -> {new}")
            continue
        matches = [r for r in permit["allowed_paths"]
                   if "relocate" in r.get("change_kinds", [])
                   and r["pattern"] == old and r.get("to") == new]
        if len(matches) == 0:
            failures.append(f"RELOCATE_DENIED: {old} -> {new} (requires an exact-path relocate rule with matching 'to')")
        elif len(matches) > 1:
            failures.append(f"AMBIGUOUS_MATCH: {old} -> {new} matches {[r['rule_id'] for r in matches]}")

    for path, kind in changed:
        if forbidden(path):
            failures.append(f"FORBIDDEN_PATH: {path}")
            continue
        if kind == "delete":
            exact = [r for r in permit["allowed_paths"] if r["pattern"] == path and "delete" in r.get("change_kinds", [])]
            if not exact:
                failures.append(f"DELETE_DENIED: {path} (deletes require an explicit exact-path rule)")
            continue
        matches = [r for r in permit["allowed_paths"] if rule_matches(r, path) and kind in r["change_kinds"]]
        if len(matches) == 0:
            failures.append(f"UNMATCHED_PATH: {path} ({kind}) — default deny")
        elif len(matches) > 1:
            failures.append(f"AMBIGUOUS_MATCH: {path} matches {[r['rule_id'] for r in matches]}")

    if failures:
        return deny(failures, digest)

    print(json.dumps({
        "result": "PASS",
        "mode": "bootstrap" if bootstrap else "base",
        "authorization_id": permit["authorization_id"],
        "authorization_digest": digest,
        "issue": issue,
        "changed_paths": len(changed) + len(relocations),
        "closed_records": sorted(base_records[p]["authorization_id"] for p in verified_closures),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
