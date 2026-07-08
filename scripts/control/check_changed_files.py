#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DANGEROUS_EXACT = {
    "apps/mobile/package-lock.json": "Dependency",
    "apps/web/package-lock.json": "Dependency",
    "package-lock.json": "Dependency",
    "eas.json": "Build / Distribution",
}
DANGEROUS_PREFIX = {
    "android/": "Build / Distribution",
    "ios/": "Build / Distribution",
    "backend/": "Backend",
    "database/": "Backend",
}

CATEGORY_PREFIXES = [
    ("apps/mobile/", "app/mobile"),
    ("apps/web/", "app/web"),
    ("docs/project-control/", "docs/project-control"),
    (".github/", "workflow/control"),
    ("scripts/control/", "workflow/control"),
    ("android/", "build/native"),
    ("ios/", "build/native"),
    ("backend/", "backend/database"),
    ("database/", "backend/database"),
]

LANE_APPROVALS = {
    "Dependency": ("Lane: Dependency", "approved dependency lane"),
    "Build / Distribution": ("Lane: Build / Distribution", "approved build/distribution lane"),
    "Backend": ("Lane: Backend", "approved backend lane"),
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
        return []
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def changed_files():
    base = os.getenv("GITHUB_BASE_REF")
    before = os.getenv("GITHUB_EVENT_BEFORE") or os.getenv("BEFORE_SHA")
    candidates = []
    if base:
        candidates.append(["diff", "--name-only", f"origin/{base}...HEAD"])
    if before and before.strip("0"):
        candidates.append(["diff", "--name-only", f"{before}...HEAD"])
    candidates.extend(
        [
            ["diff", "--name-only", "HEAD"],
            ["diff", "--name-only", "--cached"],
            ["ls-files", "--others", "--exclude-standard"],
        ]
    )
    for args in candidates:
        out = git(args)
        if out:
            return sorted(set(out))
    return []


def category(path):
    if path in {"package.json", "package-lock.json"} or path.endswith("/package.json") or path.endswith("/package-lock.json"):
        return "dependency/package"
    if path == "eas.json":
        return "build/native"
    for prefix, label in CATEGORY_PREFIXES:
        if path.startswith(prefix):
            return label
    return "unknown"


def dangerous_lane(path):
    if path in DANGEROUS_EXACT:
        return DANGEROUS_EXACT[path]
    for prefix, lane in DANGEROUS_PREFIX.items():
        if path.startswith(prefix):
            return lane
    return None


def current_phase_reports(files):
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


def approval_text(files):
    parts = [read_pr_body()]
    for report in current_phase_reports(files):
        parts.append(read_file(report))
    return "\n".join(parts)


def has_approval(text, lane):
    exact_lane, approved_lane = LANE_APPROVALS[lane]
    normalized = text.lower()
    precise_lane_present = exact_lane.lower() in normalized
    explicit_approval_present = (
        "explicit owner approval" in normalized
        or approved_lane.lower() in normalized
    )
    return precise_lane_present and explicit_approval_present


def main():
    files = changed_files()
    print("Changed files:")
    for path in files:
        print(f"- {path} [{category(path)}]")

    text = approval_text(files)
    failures = []
    for path in files:
        lane = dangerous_lane(path)
        if lane and not has_approval(text, lane):
            failures.append(
                f"{path} requires exact lane '{lane}' plus explicit owner approval or approved lane phrase"
            )

    if failures:
        print("FAIL: dangerous path approval check failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: changed-file allowlist / lane check completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
