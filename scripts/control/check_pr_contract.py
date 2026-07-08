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


def read_body():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and Path(event_path).exists():
        try:
            payload = json.loads(Path(event_path).read_text())
            return (payload.get("pull_request") or {}).get("body") or ""
        except Exception:
            pass
    env_body = os.getenv("PR_BODY", "")
    if env_body.strip():
        return env_body
    parts = []
    template = ROOT / ".github/pull_request_template.md"
    if template.exists():
        parts.append(template.read_text(errors="replace"))
    parts.extend(
        report.read_text(errors="replace")
        for report in sorted((ROOT / "docs/project-control").glob("phase_*_report.md"))
    )
    return "\n\n".join(parts)


def changed_files():
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


def has_section(text, section):
    return re.search(rf"^#+\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", text, re.I | re.M)


def downgraded(line):
    lower = line.lower()
    return any(token in lower for token in DOWNGRADE_CONTEXT)


def claim_level_required(files):
    for path in files:
        if (
            path in {"eas.json", "package.json", "package-lock.json"}
            or any(path.startswith(prefix) for prefix in CLAIM_LEVEL_PATHS)
        ):
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims-only", action="store_true")
    args = parser.parse_args()

    text = read_body()
    failures = []
    if not text.strip():
        failures.append("No PR body or phase report text available.")

    if not args.claims_only:
        for section in REQUIRED_SECTIONS:
            if not has_section(text, section):
                failures.append(f"Missing required PR/report section: {section}")

    for line_number, line in enumerate(text.splitlines(), 1):
        for term in OVERCLAIMS:
            if re.search(r"\b" + re.escape(term.lower()) + r"\b", line.lower()) and not downgraded(line):
                failures.append(
                    f"Line {line_number}: overclaim '{term}' lacks downgrade/evidence context: {line.strip()}"
                )

    if claim_level_required(changed_files()) and not has_section(text, "Claim Level"):
        failures.append("Claim Level section is required for app/control/workflow/script/build/dependency/content changes.")

    if failures:
        print("FAIL:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    label = "claim-language" if args.claims_only else "PR/report contract"
    print(f"PASS: {label} check completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
