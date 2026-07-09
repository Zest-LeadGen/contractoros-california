#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MARKER = "OWNER_TRIGGER_REVIEW"
REQUIRED_FIELDS = [
    "Owner interruption required",
    "Trigger categories",
    "Lane eligibility",
    "Human approval required",
    "Auto-merge eligible",
    "Rationale",
]
ALLOWED_OWNER_INTERRUPTION = {"YES", "NO"}
ALLOWED_TRIGGER_CATEGORIES = {
    "NONE",
    "LEGAL",
    "FINANCIAL",
    "PAID_SERVICE",
    "PUBLIC_RELEASE",
    "PRODUCTION_READINESS",
    "APP_STORE_BUILD_DISTRIBUTION",
    "SCOPE_EXPANSION",
    "UNRESOLVED_RED_TEAM_BLOCKED",
    "DEPENDENCY_SECURITY_RISK_ACCEPTANCE",
    "ARCHITECTURE_THRESHOLD",
}
ALLOWED_LANE_ELIGIBILITY = {
    "NOT_AUTOMATION_ELIGIBLE",
    "FUTURE_LOW_RISK_CANDIDATE",
}


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


def review_text(payload, files, explicit_files):
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


def parse_categories(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def validate_marker(marker):
    failures = []
    for field in REQUIRED_FIELDS:
        if not marker.get(field):
            failures.append(f"owner-trigger marker field missing or empty: {field}")

    owner_required = marker.get("Owner interruption required", "")
    if owner_required and owner_required not in ALLOWED_OWNER_INTERRUPTION:
        failures.append(f"owner-trigger marker Owner interruption required value is invalid: {owner_required}")

    categories = parse_categories(marker.get("Trigger categories", ""))
    if marker.get("Trigger categories") and not categories:
        failures.append("owner-trigger marker Trigger categories must not be empty.")
    unknown_categories = [category for category in categories if category not in ALLOWED_TRIGGER_CATEGORIES]
    for category in unknown_categories:
        failures.append(f"owner-trigger marker trigger category is invalid: {category}")

    if "NONE" in categories and len(categories) > 1:
        failures.append("owner-trigger marker Trigger categories may use NONE only by itself.")

    if owner_required == "YES" and categories == ["NONE"]:
        failures.append("owner-trigger marker cannot require owner interruption with Trigger categories: NONE.")

    if owner_required == "NO" and categories != ["NONE"]:
        failures.append("owner-trigger marker cannot decline owner interruption unless Trigger categories is NONE.")

    lane_eligibility = marker.get("Lane eligibility", "")
    if lane_eligibility and lane_eligibility not in ALLOWED_LANE_ELIGIBILITY:
        failures.append(f"owner-trigger marker Lane eligibility value is invalid: {lane_eligibility}")

    triggered = any(category != "NONE" for category in categories)
    if triggered and lane_eligibility == "FUTURE_LOW_RISK_CANDIDATE":
        failures.append("owner-trigger marker cannot use FUTURE_LOW_RISK_CANDIDATE when trigger categories are present.")

    if marker.get("Human approval required") and marker.get("Human approval required") != "YES":
        failures.append("owner-trigger marker Human approval required must be YES.")

    if marker.get("Auto-merge eligible") and marker.get("Auto-merge eligible") != "NO":
        failures.append("owner-trigger marker Auto-merge eligible must be NO.")

    return failures


def evaluate_markers(markers):
    failures = []
    valid_markers = []
    for index, marker in enumerate(markers, 1):
        marker_failures = validate_marker(marker)
        if marker_failures:
            failures.extend(f"marker {index}: {failure}" for failure in marker_failures)
        else:
            valid_markers.append(marker)

    if failures:
        return False, failures
    if valid_markers:
        return True, []
    return False, ["owner-trigger marker is missing."]


def marker_text(
    owner_required="YES",
    categories="ARCHITECTURE_THRESHOLD",
    lane_eligibility="NOT_AUTOMATION_ELIGIBLE",
    human_approval="YES",
    auto_merge="NO",
):
    return f"""
{MARKER}
Owner interruption required: {owner_required}
Trigger categories: {categories}
Lane eligibility: {lane_eligibility}
Human approval required: {human_approval}
Auto-merge eligible: {auto_merge}
Rationale: Phase changes owner-trigger/lane eligibility controls and future automation policy.
"""


def run_self_test():
    cases = [
        ("valid triggered marker passes", marker_text(), True),
        ("valid no-trigger marker passes", marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"), True),
        ("missing marker fails", "", False),
        ("unknown trigger category fails", marker_text(categories="MAGIC"), False),
        ("YES with NONE fails", marker_text(categories="NONE"), False),
        ("NO with non-NONE fails", marker_text("NO", "LEGAL"), False),
        (
            "triggered PR marked FUTURE_LOW_RISK_CANDIDATE fails",
            marker_text(lane_eligibility="FUTURE_LOW_RISK_CANDIDATE"),
            False,
        ),
        ("Human approval required NO fails", marker_text(human_approval="NO"), False),
        ("Auto-merge eligible YES fails", marker_text(auto_merge="YES"), False),
        ("HTML comments and fenced examples are ignored", f"<!--\n{marker_text()}\n-->\n```text\n{marker_text()}\n```", False),
    ]
    for label, text, should_pass in cases:
        markers = extract_markers(text)
        passed, failures = evaluate_markers(markers)
        if passed != should_pass:
            print(f"FAIL: self-test case failed: {label}")
            if failures:
                for failure in failures:
                    print(f"- {failure}")
            return 1
    print("PASS: owner-trigger marker parser self-test completed.")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", action="append", default=[])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    payload = event_payload()
    files = changed_files_pr(payload) if is_pr_context(payload) else changed_files_local()
    text, error = review_text(payload, files, args.text_file)
    if error:
        print(f"FAIL: {error}")
        return 1

    markers = extract_markers(text)
    passed, failures = evaluate_markers(markers)
    if passed:
        print("PASS: owner-trigger marker check completed.")
        return 0

    print("FAIL:")
    for failure in failures:
        print(f"- {failure}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
