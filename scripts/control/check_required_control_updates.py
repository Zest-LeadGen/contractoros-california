#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/project-control/control-file-update-matrix.yml"


def git_changed():
    out = []
    for cmd in (
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            out.extend([line for line in proc.stdout.splitlines() if line])
    return sorted(set(out))


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


def changed_phase_reports(files):
    return [
        path
        for path in files
        if path.startswith("docs/project-control/phase_") and path.endswith("_report.md")
    ]


def read_pr_body():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and Path(event_path).exists():
        try:
            payload = json.loads(Path(event_path).read_text())
            return (payload.get("pull_request") or {}).get("body") or ""
        except Exception:
            pass
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
    normalized = text.lower()
    exact_lane = f"lane: {lane}".lower()
    return exact_lane in normalized and (
        "explicit owner approval" in normalized
        or f"approved {lane.lower()} lane" in normalized
        or (lane == "Build / Distribution" and "approved build/distribution lane" in normalized)
    )


def lane_compatible(rule_lane, declared_lane):
    if not rule_lane:
        return True
    return rule_lane.lower() == declared_lane.lower()


def main():
    if not MATRIX.exists():
        print("FAIL: matrix missing")
        return 1

    files = git_changed()
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
        fail.append(
            f"Expected exactly one changed current phase report, found {len(reports)}: {reports}"
        )
    if not report_required and len(reports) > 1:
        fail.append(f"Expected at most one changed phase report, found {len(reports)}: {reports}")

    current_report_text = read_file(reports[0]) if reports else ""
    pr_body = read_pr_body()
    validation_text = pr_body + "\n\n" + current_report_text
    declared_lane = lane_from_text(validation_text)

    required_sections = set()
    required_updates = set()
    for _, rule in matched:
        required_sections.update(rule.get("required_report_sections", []) or [])
        required_updates.update(rule.get("required_control_updates", []) or [])
        rule_lane = str(rule.get("lane", "")).strip()
        if rule_lane and declared_lane and not lane_compatible(rule_lane, declared_lane):
            fail.append(f"Lane mismatch: changed path category requires '{rule_lane}' but PR/report declares '{declared_lane}'")
        if rule.get("blocked_without_approval") and not approval_present(validation_text, rule_lane):
            fail.append(f"Blocked category '{rule.get('pattern')}' requires {rule_lane} and explicit owner approval")

    if report_required and not current_report_text:
        fail.append("Current phase report text is missing.")

    if report_required and not has_section(validation_text, "Documentation Impact"):
        fail.append("Current PR/report is missing Documentation Impact section.")

    for section in sorted(required_sections):
        if not has_section(validation_text, str(section)):
            fail.append(f"Missing required current PR/report section: {section}")

    for req in sorted(required_updates):
        marker = f"{req}: reviewed, no update required"
        changed = req in files
        if not changed and marker not in validation_text:
            fail.append(f"{req} not changed and missing exact current report declaration: {marker}")

    print("Changed files considered by matrix:")
    for path in files:
        print(f"- {path}")
    print(f"Matrix rules parsed: {len(rules)}")
    print(f"Matched rules: {len(matched)}")
    if reports:
        print(f"Current phase report: {reports[0]}")
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
