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

SAFE_LOW_RISK_PREFIX = "docs/project-control/"
SAFE_LOW_RISK_SUFFIX = ".md"
BLOCKED_EXACT_PATHS = {
    "package.json",
    "package-lock.json",
    "eas.json",
    ".github/pull_request_template.md",
}
BLOCKED_PREFIXES = (
    ".github/workflows/",
    "scripts/control/",
    "apps/",
    "android/",
    "ios/",
    "backend/",
    "database/",
)
BLOCKED_SUFFIXES = (
    "/package.json",
    "/package-lock.json",
)


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
        return []
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


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
            return sorted(set(out))
    return []


def changed_files_local():
    out = []
    for cmd in (
        ["diff", "--name-only", "HEAD"],
        ["diff", "--name-only", "--cached"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        out.extend(git(cmd))
    return sorted(set(out))


def resolve_changed_files(payload):
    if is_pr_context(payload):
        files = changed_files_pr(payload)
        if not files:
            return None, "PR context detected but no changed files were resolved."
        return files, None
    return changed_files_local(), None


def changed_phase_reports(files):
    return [
        path
        for path in files or []
        if path.startswith("docs/project-control/phase_") and path.endswith("_report.md")
    ]


def read_file(path):
    file_path = ROOT / path
    return file_path.read_text(errors="replace") if file_path.exists() else ""


def evidence_text(payload, files, explicit_files):
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


def marker_signature(marker):
    return tuple((field, marker.get(field, "")) for field in REQUIRED_FIELDS)


def validate_marker(marker):
    failures = []
    for field in REQUIRED_FIELDS:
        if not marker.get(field):
            failures.append(f"marker field missing or empty: {field}")

    owner_required = marker.get("Owner interruption required", "")
    if owner_required and owner_required not in ALLOWED_OWNER_INTERRUPTION:
        failures.append(f"Owner interruption required value is invalid: {owner_required}")

    categories = parse_categories(marker.get("Trigger categories", ""))
    if marker.get("Trigger categories") and not categories:
        failures.append("Trigger categories must not be empty.")
    for category in categories:
        if category not in ALLOWED_TRIGGER_CATEGORIES:
            failures.append(f"trigger category is invalid: {category}")

    if "NONE" in categories and len(categories) > 1:
        failures.append("Trigger categories may use NONE only by itself.")

    if owner_required == "YES" and categories == ["NONE"]:
        failures.append("owner interruption cannot be required with Trigger categories: NONE.")

    if owner_required == "NO" and categories != ["NONE"]:
        failures.append("owner interruption cannot be declined unless Trigger categories is NONE.")

    lane_eligibility = marker.get("Lane eligibility", "")
    if lane_eligibility and lane_eligibility not in ALLOWED_LANE_ELIGIBILITY:
        failures.append(f"Lane eligibility value is invalid: {lane_eligibility}")

    if any(category != "NONE" for category in categories) and lane_eligibility == "FUTURE_LOW_RISK_CANDIDATE":
        failures.append("FUTURE_LOW_RISK_CANDIDATE cannot be used when any owner-trigger category is present.")

    if owner_required == "YES" and lane_eligibility == "FUTURE_LOW_RISK_CANDIDATE":
        failures.append("FUTURE_LOW_RISK_CANDIDATE cannot be used when owner interruption is required.")

    if marker.get("Human approval required") and marker.get("Human approval required") != "YES":
        failures.append("Human approval required must be YES under current policy.")

    if marker.get("Auto-merge eligible") and marker.get("Auto-merge eligible") != "NO":
        failures.append("Auto-merge eligible must be NO under current policy.")

    return failures


def low_risk_file_failures(files):
    if not files:
        return ["changed files are required before FUTURE_LOW_RISK_CANDIDATE can be verified."]

    failures = []
    for path in files:
        if path in BLOCKED_EXACT_PATHS or path.endswith(BLOCKED_SUFFIXES):
            failures.append(f"{path} is not allowed for FUTURE_LOW_RISK_CANDIDATE.")
            continue
        if path.startswith(BLOCKED_PREFIXES):
            failures.append(f"{path} is not allowed for FUTURE_LOW_RISK_CANDIDATE.")
            continue
        if not (path.startswith(SAFE_LOW_RISK_PREFIX) and path.endswith(SAFE_LOW_RISK_SUFFIX)):
            failures.append(f"{path} is outside the current documentation-only low-risk pattern.")
    return failures


def evaluate(text, files):
    markers = extract_markers(text)
    if not markers:
        return False, ["owner-trigger marker is missing."]

    failures = []
    for index, marker in enumerate(markers, 1):
        failures.extend(f"marker {index}: {failure}" for failure in validate_marker(marker))
    if failures:
        return False, failures

    signature = marker_signature(markers[0])
    if any(marker_signature(marker) != signature for marker in markers[1:]):
        return False, ["multiple owner-trigger markers conflict; lane eligibility evidence is ambiguous."]

    marker = markers[0]
    lane_eligibility = marker.get("Lane eligibility", "")
    if lane_eligibility == "NOT_AUTOMATION_ELIGIBLE":
        return True, []

    if lane_eligibility != "FUTURE_LOW_RISK_CANDIDATE":
        return False, [f"unsupported lane eligibility: {lane_eligibility or '(missing)'}"]

    candidate_failures = []
    if marker.get("Owner interruption required") != "NO":
        candidate_failures.append("FUTURE_LOW_RISK_CANDIDATE requires Owner interruption required: NO.")
    if parse_categories(marker.get("Trigger categories", "")) != ["NONE"]:
        candidate_failures.append("FUTURE_LOW_RISK_CANDIDATE requires Trigger categories: NONE.")
    candidate_failures.extend(low_risk_file_failures(files))
    if candidate_failures:
        return False, candidate_failures
    return True, []


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
Rationale: Phase changes lane eligibility controls and future automation policy.
"""


def run_self_test():
    safe_files = ["docs/project-control/typo_only_policy_note.md"]
    cases = [
        ("valid NOT_AUTOMATION_ELIGIBLE with owner trigger passes", marker_text(), safe_files, True),
        (
            "valid FUTURE_LOW_RISK_CANDIDATE passes",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            safe_files,
            True,
        ),
        (
            "low-risk candidate with non-NONE trigger fails",
            marker_text("YES", "ARCHITECTURE_THRESHOLD", "FUTURE_LOW_RISK_CANDIDATE"),
            safe_files,
            False,
        ),
        (
            "low-risk candidate with owner interruption YES fails",
            marker_text("YES", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            safe_files,
            False,
        ),
        (
            "low-risk candidate with auto-merge YES fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE", auto_merge="YES"),
            safe_files,
            False,
        ),
        (
            "low-risk candidate with human approval not YES fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE", human_approval="NO"),
            safe_files,
            False,
        ),
        ("missing marker fails", "", safe_files, False),
        (("malformed marker fails"), f"{MARKER}\nOwner interruption required: NO\n", safe_files, False),
        ("unknown trigger category fails", marker_text(categories="MAGIC"), safe_files, False),
        ("unsupported lane eligibility fails", marker_text(lane_eligibility="MAYBE_LOW_RISK"), safe_files, False),
        (
            "ambiguous lane eligibility fails",
            marker_text() + "\n" + marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            safe_files,
            False,
        ),
        (
            "changed file outside safe policy fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            ["README.md"],
            False,
        ),
        (
            "workflow control change marked low risk fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            [".github/workflows/control-gates.yml"],
            False,
        ),
        (
            "control script change marked low risk fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            ["scripts/control/check_low_risk_lane.py"],
            False,
        ),
        (
            "dependency package path marked low risk fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            ["package.json"],
            False,
        ),
        (
            "lockfile path marked low risk fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            ["apps/web/package-lock.json"],
            False,
        ),
        (
            "app source path marked low risk fails",
            marker_text("NO", "NONE", "FUTURE_LOW_RISK_CANDIDATE"),
            ["apps/web/src/App.tsx"],
            False,
        ),
        (
            "HTML comments and fenced examples are ignored",
            f"<!--\n{marker_text()}\n-->\n```text\n{marker_text()}\n```",
            safe_files,
            False,
        ),
    ]
    for label, text, files, should_pass in cases:
        passed, failures = evaluate(text, files)
        if passed != should_pass:
            print(f"FAIL: self-test case failed: {label}")
            for failure in failures:
                print(f"- {failure}")
            return 1
    print("PASS: low-risk lane validator self-test completed.")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", action="append", default=[])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    payload = event_payload()
    files, files_error = resolve_changed_files(payload)
    if files_error:
        print(f"FAIL: {files_error}")
        return 1

    text, text_error = evidence_text(payload, files, args.text_file)
    if text_error:
        print(f"FAIL: {text_error}")
        return 1

    passed, failures = evaluate(text, files)
    if passed:
        print("Changed files resolved:")
        for path in files:
            print(f"- {path}")
        print("PASS: low-risk lane validator completed.")
        return 0

    print("FAIL:")
    for failure in failures:
        print(f"- {failure}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
