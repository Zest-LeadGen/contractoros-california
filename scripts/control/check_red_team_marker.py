#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MARKER = "RED_TEAM_DECISION"
REQUIRED_FIELDS = [
    "PR number",
    "PR head SHA",
    "Decision",
    "Reviewer role",
    "Review date",
    "Scope reviewed",
    "Conditions",
    "Forbidden-scope confirmation",
    "SHA-bound statement",
]
ALLOWED_DECISIONS = {"APPROVED", "CHANGES_REQUESTED", "BLOCKED"}
SHA_BOUND_STATEMENT = "This decision applies only to the listed PR head SHA."


def git(args):
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        return ""
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def event_payload():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and Path(event_path).exists():
        try:
            return json.loads(Path(event_path).read_text())
        except Exception:
            return {}
    return {}


def is_pr_context(payload):
    return bool(os.getenv("GITHUB_BASE_REF")) or os.getenv("GITHUB_EVENT_NAME") == "pull_request" or "pull_request" in payload


def changed_files_pr(payload):
    base_ref = os.getenv("GITHUB_BASE_REF") or (payload.get("pull_request") or {}).get("base", {}).get("ref")
    candidates = []
    if base_ref:
        candidates.append(["diff", "--name-only", f"origin/{base_ref}...HEAD"])
        candidates.append(["diff", "--name-only", f"{base_ref}...HEAD"])
    for args in candidates:
        out = git(args)
        if out:
            return sorted(set(line.strip() for line in out.splitlines() if line.strip()))
    return []


def changed_files_local():
    out = []
    for cmd in (
        ["diff", "--name-only", "HEAD"],
        ["diff", "--name-only", "--cached"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        result = git(cmd)
        out.extend(line.strip() for line in result.splitlines() if line.strip())
    return sorted(set(out))


def changed_phase_reports(files):
    return [
        path
        for path in files or []
        if path.startswith("docs/project-control/phase_") and path.endswith("_report.md")
    ]


def read_file(path):
    file_path = ROOT / path
    return file_path.read_text(errors="replace") if file_path.exists() else ""


def contract_text(payload, files, explicit_files):
    parts = []
    if explicit_files:
        for path in explicit_files:
            parts.append(Path(path).read_text(errors="replace"))
        return "\n\n".join(parts), None

    if "pull_request" in payload:
        parts.append((payload.get("pull_request") or {}).get("body") or "")
    else:
        parts.append(os.getenv("PR_BODY", ""))

    for report in changed_phase_reports(files):
        parts.append(read_file(report))

    text = "\n\n".join(parts)
    if is_pr_context(payload) and not text.strip():
        return "", "PR context detected but PR body/report text was unavailable or empty."
    return text, None


def current_head_sha(payload, override):
    if override:
        return override
    pr = payload.get("pull_request") or {}
    return (
        (pr.get("head") or {}).get("sha")
        or os.getenv("PR_HEAD_SHA")
        or os.getenv("GITHUB_HEAD_SHA")
        or os.getenv("GITHUB_SHA")
        or git(["rev-parse", "HEAD"])
    )


def current_pr_number(payload, override):
    if override:
        return override
    pr = payload.get("pull_request") or {}
    return str(pr.get("number") or os.getenv("PR_NUMBER") or "").strip()


def normalize_pr_number(value):
    return str(value or "").strip().lstrip("#")


def remove_ignored_blocks(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"```.*?```", "", text, flags=re.S)


def extract_markers(text):
    markers = []
    lines = remove_ignored_blocks(text).splitlines()
    for index, line in enumerate(lines):
        if line.strip() != MARKER:
            continue
        fields = {}
        for raw in lines[index + 1:]:
            stripped = raw.strip()
            if stripped == MARKER:
                break
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"^([^:]+):\s*(.*)$", stripped)
            if match:
                fields[match.group(1).strip()] = match.group(2).strip()
        markers.append(fields)
    return markers


def validate_marker(marker, head_sha, pr_number):
    failures = []
    for field in REQUIRED_FIELDS:
        if not marker.get(field):
            failures.append(f"red-team marker field missing or empty: {field}")

    decision = marker.get("Decision", "")
    if decision and decision not in ALLOWED_DECISIONS:
        failures.append(f"red-team marker decision is invalid: {decision}")

    marker_sha = marker.get("PR head SHA", "")
    if marker_sha and not re.fullmatch(r"[0-9a-fA-F]{40}", marker_sha):
        failures.append("red-team marker PR head SHA must be a 40-character git SHA.")

    if marker.get("Review date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", marker["Review date"]):
        failures.append("red-team marker review date must use YYYY-MM-DD.")

    if marker.get("SHA-bound statement") != SHA_BOUND_STATEMENT:
        failures.append(f"red-team marker SHA-bound statement must equal: {SHA_BOUND_STATEMENT}")

    if decision in {"CHANGES_REQUESTED", "BLOCKED"}:
        failures.append(f"red-team marker decision is not merge-eligible: {decision}")

    return failures


def marker_matches_current(marker, head_sha, pr_number):
    marker_sha = marker.get("PR head SHA", "")
    marker_pr = normalize_pr_number(marker.get("PR number", ""))
    current_pr = normalize_pr_number(pr_number)
    if not head_sha or marker_sha.lower() != head_sha.lower():
        return False
    if current_pr and marker_pr != current_pr:
        return False
    return True


def evaluate_markers(markers, head_sha, pr_number):
    failures = []
    approved_matches = []
    for index, marker in enumerate(markers, 1):
        decision = marker.get("Decision", "")
        marker_failures = validate_marker(marker, head_sha, pr_number)
        if marker_failures:
            failures.extend(f"marker {index}: {failure}" for failure in marker_failures)
        if decision == "APPROVED" and not marker_failures and marker_matches_current(marker, head_sha, pr_number):
            approved_matches.append(marker)

    if failures:
        return False, failures
    if approved_matches:
        return True, []
    return False, ["no APPROVED red-team marker matches the current PR number and PR head SHA."]


def marker_text(decision="APPROVED", sha=None, pr_number="#123"):
    marker_sha = sha or "0123456789abcdef0123456789abcdef01234567"
    return f"""
{MARKER}
PR number: {pr_number}
PR head SHA: {marker_sha}
Decision: {decision}
Reviewer role: Red-team reviewer
Review date: 2026-07-09
Scope reviewed: Phase scope and changed files reviewed.
Conditions: None.
Forbidden-scope confirmation: Confirmed no forbidden scope in reviewed diff.
SHA-bound statement: {SHA_BOUND_STATEMENT}
"""


def run_self_test():
    good_sha = "0123456789abcdef0123456789abcdef01234567"
    stale_sha = "fedcba9876543210fedcba9876543210fedcba98"
    cases = [
        ("approved-only marker passes", marker_text(), True),
        ("BLOCKED-only marker fails", marker_text("BLOCKED"), False),
        ("CHANGES_REQUESTED-only marker fails", marker_text("CHANGES_REQUESTED"), False),
        ("APPROVED plus BLOCKED fails", marker_text() + marker_text("BLOCKED"), False),
        ("APPROVED plus CHANGES_REQUESTED fails", marker_text() + marker_text("CHANGES_REQUESTED"), False),
        ("APPROVED with stale SHA fails", marker_text(sha=stale_sha), False),
        ("template fenced-code examples are ignored", f"```text\n{marker_text()}\n```", False),
    ]
    for label, text, should_pass in cases:
        markers = extract_markers(text)
        passed, failures = evaluate_markers(markers, good_sha, "123") if markers else (False, ["red-team marker is missing."])
        if passed != should_pass:
            print(f"FAIL: self-test case failed: {label}")
            if failures:
                for failure in failures:
                    print(f"- {failure}")
            return 1
    if extract_markers(""):
        print("FAIL: self-test empty text unexpectedly produced a marker.")
        return 1
    print("PASS: red-team marker parser self-test completed.")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", action="append", default=[])
    parser.add_argument("--head-sha")
    parser.add_argument("--pr-number")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    payload = event_payload()
    files = changed_files_pr(payload) if is_pr_context(payload) else changed_files_local()
    text, error = contract_text(payload, files, args.text_file)
    if error:
        print(f"FAIL: {error}")
        return 1

    markers = extract_markers(text)
    if not markers:
        print("FAIL: red-team marker is missing.")
        return 1

    head_sha = current_head_sha(payload, args.head_sha)
    pr_number = current_pr_number(payload, args.pr_number)

    passed, failures = evaluate_markers(markers, head_sha, pr_number)
    if passed:
        print(f"PASS: red-team marker check completed for SHA {head_sha}.")
        return 0

    print("FAIL:")
    for failure in failures:
        print(f"- {failure}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
