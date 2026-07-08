#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SECTIONS = [
    "Phase",
    "Lane",
    "Scope",
    "Starting Main SHA",
    "Changed Files",
    "Commands Run",
    "Dependency / Lockfile Handling",
    "Documentation Impact",
    "Risk Register Impact",
    "Decision Log Impact",
    "Artifact Index Impact",
    "Forbidden Scope Confirmation",
    "Claim Level",
    "Known Limitations",
    "Next Phase Status",
]

OVERCLAIMS = [
    "production-ready",
    "public-ready",
    "exam-ready",
    "APK-ready",
    "app-store-ready",
    "launch-ready",
    "fully tested",
    "complete",
    "finalized",
]
DOWNGRADE_CONTEXT = [
    "not ",
    "does not prove",
    "do not claim",
    "no ",
    "without",
    "forbidden",
    "blocked",
    "not ready",
    "not complete",
    "not finalized",
    "not yet",
    "only after",
]
CLAIM_LEVEL_PATHS = (
    "apps/",
    "android/",
    "ios/",
    "backend/",
    "database/",
    "docs/project-control/",
    ".github/",
    "scripts/control/",
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


def changed_files(payload):
    if is_pr_context(payload):
        files = changed_files_pr(payload)
        if not files:
            return None
        return files
    return changed_files_local()


def changed_phase_reports(files):
    return [
        path
        for path in files or []
        if path.startswith("docs/project-control/phase_") and path.endswith("_report.md")
    ]


def read_file(path):
    file_path = ROOT / path
    return file_path.read_text(errors="replace") if file_path.exists() else ""


def contract_text(payload, files):
    if is_pr_context(payload):
        body = (payload.get("pull_request") or {}).get("body") or ""
        if not body.strip():
            return None, "FAIL: PR context detected but PR body was unavailable or empty."
        reports = changed_phase_reports(files)
        report_text = "\n\n".join(read_file(report) for report in reports)
        return body + "\n\n" + report_text, None

    env_body = os.getenv("PR_BODY", "")
    reports = changed_phase_reports(files)
    report_text = "\n\n".join(read_file(report) for report in reports)
    if env_body.strip() or report_text.strip():
        return env_body + "\n\n" + report_text, None
    return "", None


def section_content(text, section):
    heading = re.search(rf"^#+\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", text, re.I | re.M)
    if not heading:
        return None
    next_heading = re.search(r"^#+\s+", text[heading.end():], re.M)
    end = heading.end() + next_heading.start() if next_heading else len(text)
    return text[heading.end():end].strip()


def downgraded(line):
    lower = line.lower()
    return any(token in lower for token in DOWNGRADE_CONTEXT)


def claim_level_required(files):
    for path in files or []:
        if (
            path in {"eas.json", "package.json", "package-lock.json"}
            or any(path.startswith(prefix) for prefix in CLAIM_LEVEL_PATHS)
        ):
            return True
    return False


def forbidden_scope_confirmed(content):
    if not content:
        return False
    return bool(re.search(r"- \[[xX]\]", content)) or "confirmed" in content.lower()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims-only", action="store_true")
    args = parser.parse_args()

    payload = event_payload()
    files = changed_files(payload)
    failures = []
    if is_pr_context(payload) and files is None:
        failures.append("PR context detected but no changed files were resolved.")
        files = []

    text, body_error = contract_text(payload, files)
    if body_error:
        failures.append(body_error)
    if not text or not text.strip():
        failures.append("No PR body or current changed phase report text available.")
        text = ""

    if not args.claims_only:
        for section in REQUIRED_SECTIONS:
            content = section_content(text, section)
            if content is None:
                failures.append(f"Missing required PR/report section: {section}")
            elif not content.strip():
                failures.append(f"Required PR/report section has no content: {section}")

        forbidden_content = section_content(text, "Forbidden Scope Confirmation")
        if not forbidden_scope_confirmed(forbidden_content):
            failures.append("Forbidden Scope Confirmation must include checked boxes or explicit confirmation.")

    for line_number, line in enumerate(text.splitlines(), 1):
        for term in OVERCLAIMS:
            if re.search(r"\b" + re.escape(term.lower()) + r"\b", line.lower()) and not downgraded(line):
                failures.append(f"Line {line_number}: overclaim '{term}' lacks downgrade/evidence context: {line.strip()}")

    if claim_level_required(files) and section_content(text, "Claim Level") is None:
        failures.append("Claim Level section is required for app/control/workflow/script/build/dependency/content changes.")

    if failures:
        print("FAIL:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    label = "claim-language" if args.claims_only else "PR/report contract"
    print(f"Changed files resolved: {len(files or [])}")
    for path in files or []:
        print(f"- {path}")
    print(f"PASS: {label} check completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
