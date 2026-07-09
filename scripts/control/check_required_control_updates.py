#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/project-control/control-file-update-matrix.yml"

APPROVAL_PHRASES = {
    "Dependency": "approved dependency lane",
    "Build / Distribution": "approved build/distribution lane",
    "Backend": "approved backend lane",
}
CONTROL_LANE = "Control / Infrastructure"
PHASE_REPORT_PREFIX = "docs/project-control/phase_"
PHASE_REPORT_SUFFIX = "_report.md"


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


def is_push_context(payload):
    return os.getenv("GITHUB_EVENT_NAME") == "push" or ("before" in payload and "after" in payload)


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


def changed_files_push(payload):
    before = os.getenv("GITHUB_EVENT_BEFORE") or payload.get("before")
    after = os.getenv("GITHUB_SHA") or payload.get("after") or "HEAD"
    if before and after and str(before).strip("0"):
        out = git(["diff", "--name-only", f"{before}...{after}"])
        if out:
            return sorted(set(out))
    return sorted(set(git(["diff", "--name-only", "HEAD~1...HEAD"])))


def changed_files_local():
    out = []
    for cmd in (
        ["diff", "--name-only", "HEAD"],
        ["diff", "--name-only", "--cached"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        out.extend(git(cmd))
    return sorted(set(out))


def resolve_changed_files():
    payload = event_payload()
    if is_pr_context(payload):
        files = changed_files_pr(payload)
        if not files:
            print("FAIL: PR context detected but no changed files were resolved.")
            return None, "pull_request"
        return files, "pull_request"
    if is_push_context(payload):
        return changed_files_push(payload), "push"
    return changed_files_local(), "local-changes"


def parse_bool(value):
    return str(value).strip().lower() == "true"


def parse_matrix(text):
    rules = []
    current = None
    list_key = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped == "rules:":
            continue
        if stripped.startswith("- pattern:"):
            if current:
                rules.append(current)
            current = {"pattern": stripped.split(":", 1)[1].strip().strip('"')}
            list_key = None
            continue
        if current is None:
            continue
        if re.match(r"^[A-Za-z_]+:", stripped):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                value = value.strip('"')
                current[key] = parse_bool(value) if value.lower() in {"true", "false"} else value
                list_key = None
            else:
                current[key] = []
                list_key = key
        elif stripped.startswith("- ") and list_key:
            current.setdefault(list_key, []).append(stripped[2:].strip().strip('"'))
    if current:
        rules.append(current)
    return rules


def matches(pattern, path):
    return path.startswith(pattern[:-3]) if pattern.endswith("/**") else path == pattern


def is_phase_report(path):
    return path.startswith(PHASE_REPORT_PREFIX) and path.endswith(PHASE_REPORT_SUFFIX)


def changed_phase_reports(files):
    return [path for path in files if is_phase_report(path)]


def read_pr_body():
    payload = event_payload()
    if "pull_request" in payload:
        return (payload.get("pull_request") or {}).get("body") or ""
    return os.getenv("PR_BODY", "")


def read_file(path):
    file_path = ROOT / path
    return file_path.read_text(errors="replace") if file_path.exists() else ""


def has_section(text, section):
    return re.search(rf"^#+\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", text, re.I | re.M)


def lane_from_text(text):
    match = re.search(r"^#+\s+Lane\s*\n+\s*([^\n]+)", text, re.I | re.M)
    if match:
        return match.group(1).strip()
    match = re.search(r"^Lane:\s*(.+)$", text, re.I | re.M)
    if match:
        return match.group(1).strip()
    return ""


def approval_present(text, lane):
    if not lane:
        return False
    normalized = text.lower()
    precise_lane_present = f"lane: {lane}".lower() in normalized
    approval_phrase = APPROVAL_PHRASES.get(lane, f"approved {lane.lower()} lane")
    explicit_approval_present = (
        "explicit owner approval" in normalized
        or approval_phrase.lower() in normalized
    )
    return precise_lane_present and explicit_approval_present


def lane_compatible(rule_lane, declared_lane):
    if not rule_lane:
        return True
    if not declared_lane:
        return False
    return rule_lane.lower() == declared_lane.lower()


def companion_report_path(path, non_report_matches, declared_lane):
    if not is_phase_report(path):
        return False
    if not non_report_matches:
        return False
    return bool(declared_lane) and declared_lane.lower() != CONTROL_LANE.lower()


def effective_matches(matched, declared_lane):
    non_report_matches = [(path, rule) for path, rule in matched if not is_phase_report(path)]
    for path, rule in matched:
        if companion_report_path(path, non_report_matches, declared_lane):
            yield path, rule, True
        else:
            yield path, rule, False


def main():
    if not MATRIX.exists():
        print("FAIL: matrix missing")
        return 1

    files, context = resolve_changed_files()
    if files is None:
        return 1

    rules = parse_matrix(MATRIX.read_text())
    matched = []
    for path in files:
        for rule in rules:
            if matches(str(rule.get("pattern", "")), path):
                matched.append((path, rule))
                break

    report_required = any(bool(rule.get("required_phase_report")) for _, rule in matched)
    reports = changed_phase_reports(files)
    fail = []

    if report_required and len(reports) != 1:
        fail.append(f"Expected exactly one changed current phase report, found {len(reports)}: {reports}")
    if not report_required and len(reports) > 1:
        fail.append(f"Expected at most one changed phase report, found {len(reports)}: {reports}")

    current_report_text = read_file(reports[0]) if reports else ""
    pr_body = read_pr_body()
    validation_text = pr_body + "\n\n" + current_report_text
    declared_lane = lane_from_text(validation_text)

    required_sections = set()
    required_updates = set()
    companion_reports = []
    for path, rule, is_companion in effective_matches(matched, declared_lane):
        if is_companion:
            companion_reports.append(path)
            continue
        required_sections.update(rule.get("required_report_sections", []) or [])
        required_updates.update(rule.get("required_control_updates", []) or [])
        rule_lane = str(rule.get("lane", "")).strip()
        if rule_lane and not lane_compatible(rule_lane, declared_lane):
            fail.append(f"Lane mismatch: changed path category requires '{rule_lane}' but PR/report declares '{declared_lane or '(missing)'}'")
        if rule.get("blocked_without_approval") and not approval_present(validation_text, rule_lane):
            fail.append(f"Blocked category '{rule.get('pattern')}' requires Lane: {rule_lane} and explicit owner approval")

    if report_required and not current_report_text:
        fail.append("Current phase report text is missing.")

    if report_required and not has_section(validation_text, "Documentation Impact"):
        fail.append("Current PR/report is missing Documentation Impact section.")

    for section in sorted(required_sections):
        if not has_section(validation_text, str(section)):
            fail.append(f"Missing required current PR/report section: {section}")

    for req in sorted(required_updates):
        marker = f"{req}: reviewed, no update required"
        if req not in files and marker not in current_report_text:
            fail.append(f"{req} not changed and missing exact current report declaration: {marker}")

    print(f"Changed-file context: {context}")
    print("Changed files considered by matrix:")
    for path in files:
        print(f"- {path}")
    print(f"Matrix rules parsed: {len(rules)}")
    print(f"Matched rules: {len(matched)}")
    if reports:
        print(f"Current phase report: {reports[0]}")
    if companion_reports:
        print("Companion phase reports treated as documentation for declared lane:")
        for path in companion_reports:
            print(f"- {path}")
    print(f"Declared lane: {declared_lane or '(missing)'}")

    if fail:
        print("FAIL:")
        for item in fail:
            print(f"- {item}")
        return 1

    print("PASS: required control update check completed against current PR/report only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
