#!/usr/bin/env python3
"""Read-only continuity evidence collector and derived startup-packet renderer."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


GENERATOR_VERSION = "1.2.0"
EVIDENCE_SCHEMA_VERSION = "1.2.0"
PACKET_SCHEMA_VERSION = "1.2.0"
FIXTURE_VERSION = "1.2.0"
ROOT = Path(__file__).resolve().parents[2]
CANONICAL_PATH = "docs/project-control/state/contractoros-state.yaml"
OUTPUT_NAMES = ("continuity-evidence.json", "RED_TEAM_STARTUP_PACKET.md")
CLASSIFICATIONS = {
    "consistent",
    "requires_live_verification",
    "stale",
    "blocked",
    "quarantined",
}
EXIT_BY_CLASSIFICATION = {
    "consistent": 0,
    "requires_live_verification": 0,
    "stale": 2,
    "quarantined": 2,
    "blocked": 3,
}
PACKET_HASH_RULE = (
    "SHA-256 over the canonical UTF-8 packet payload with LF newlines, stable headings "
    "and list ordering, no trailing whitespace, exactly one final newline, and excluding "
    "the displayed Packet Hash heading and value"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
MARKER_TEXT_LIMIT = 1_000_000
MARKER_NAMES = ("OWNER_TRIGGER_REVIEW", "RED_TEAM_DECISION")
RED_TEAM_REQUIRED_FIELDS = (
    "PR number",
    "PR head SHA",
    "Decision",
    "Reviewer role",
    "Review date",
    "Scope reviewed",
    "Conditions",
    "Forbidden-scope confirmation",
    "SHA-bound statement",
)
RED_TEAM_DECISIONS = {"APPROVED", "CHANGES_REQUESTED", "BLOCKED"}
RED_TEAM_SHA_BOUND_STATEMENT = "This decision applies only to the listed PR head SHA."
OWNER_REQUIRED_FIELDS = (
    "Owner interruption required",
    "Trigger categories",
    "Lane eligibility",
    "Human approval required",
    "Auto-merge eligible",
    "Rationale",
)
OWNER_INTERRUPTION_VALUES = {"YES", "NO"}
OWNER_TRIGGER_CATEGORIES = {
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
OWNER_LANE_VALUES = {"NOT_AUTOMATION_ELIGIBLE", "FUTURE_LOW_RISK_CANDIDATE"}
EXPECTED_REPOSITORY = "Zest-LeadGen/contractoros-california"
EXPECTED_WORKFLOW_NAME = "ContractorOS Control Gates"
EXPECTED_WORKFLOW_ID = 309083557
EXPECTED_WORKFLOW_EVENT = "pull_request"
EXPECTED_JOB_NAME = "contractoros-control-gates"
PRE_MARKER_STEPS = (
    "Checkout repository",
    "Python version",
    "Changed-file allowlist / lane check",
    "Forbidden-scope check",
    "Required control-file update check",
    "PR body / linked issue / template completeness check",
    "Owner-trigger / lane-eligibility marker check",
    "Low-risk lane classification check",
)
MARKER_STEP = "Mandatory SHA-bound red-team marker check"
POST_MARKER_STEPS = (
    "Lockfile / dependency contamination check",
    "Claim-language check",
)
REQUIRED_STEPS = PRE_MARKER_STEPS + (MARKER_STEP,) + POST_MARKER_STEPS
IGNORED_RUNNER_STEPS = {"Set up job", "Post Checkout repository", "Complete job"}
MAX_COMMAND_OUTPUT_BYTES = 2_000_000
MAX_REVIEW_RECORDS = 500
MAX_PERMISSION_CANDIDATES = 100
REVIEW_PAGE_SIZE = 100
MAX_REVIEW_PAGES = 5
REVIEW_STATES = {"APPROVED", "CHANGES_REQUESTED", "DISMISSED", "COMMENTED", "PENDING"}
DECISIVE_REVIEW_STATES = {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}
GITHUB_LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")  # scope-bound approval evidence

# Every entry is forbidden private material and causes a fail-closed rejection.
FORBIDDEN_PRIVATE_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),  # forbidden GitHub token form
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{8,}"),  # forbidden bearer token
    re.compile(r"(?i)(?:api[_-]?key|secret|password)\s*[:=]\s*\S+"),  # forbidden secret assignment
    re.compile(r"AKIA[0-9A-Z]{16}"),  # forbidden cloud credential identifier
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),  # forbidden private key
    re.compile(r"(?i)authorization\s*:\s*\S+"),  # forbidden authorization header
    re.compile(r"/(?:Users|home)/[^/\s]+/"),  # forbidden local absolute home path
    re.compile(r"(?i)private[_ -]?customer\s*[:=]\s*\S+"),  # forbidden private customer value
    re.compile(r"(?i)confidential[_ -]?(?:owner|legal|vendor|budget)\s*[:=]\s*\S+"),  # forbidden confidential value
)


class CollectorError(Exception):
    exit_code = 5


class UnsafeEvidenceError(CollectorError):
    exit_code = 4


class CommandRejectedError(CollectorError):
    exit_code = 5


class ApprovalEvidenceUnavailableError(CollectorError):
    exit_code = 3


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA_RE.fullmatch(value))


def _parse_rfc3339(value: str) -> str:
    if not RFC3339_RE.fullmatch(value or ""):
        raise CollectorError("observation timestamp must be explicit RFC3339")
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CollectorError("observation timestamp is invalid") from exc
    return value


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _reject_unsafe(value: Any) -> None:
    text = _canonical_json(value)
    for pattern in FORBIDDEN_PRIVATE_PATTERNS:
        if pattern.search(text):
            raise UnsafeEvidenceError("unsafe or private-looking evidence rejected")


def _validate_command(
    argv: list[str], allowed_permission_logins: set[str] | None = None  # scope-bound approval evidence
) -> None:
    """Reject every command shape not included in the positive read-only allowlist."""
    if not argv or argv[0] not in {"git", "gh"}:
        raise CommandRejectedError("unknown executable rejected by command allowlist")

    if argv[0] == "git":
        allowed = {
            ("git", "remote", "get-url", "origin"),
            ("git", "rev-parse", "HEAD"),
            ("git", "rev-parse", "main"),
            ("git", "rev-parse", "origin/main"),
            ("git", "rev-parse", "--show-toplevel"),
            ("git", "status", "--porcelain=v1", "--branch"),
        }
        shape = tuple(argv)
        exact_show = (
            len(argv) == 3
            and argv[1] == "show"
            and re.fullmatch(r"[0-9a-f]{40}:" + re.escape(CANONICAL_PATH), argv[2] or "")
        )
        if shape not in allowed and not exact_show:
            raise CommandRejectedError("forbidden or unknown git command rejected by command allowlist")
        return

    if len(argv) == 5 and argv[:4] == ["gh", "api", "--method", "GET"]:
        endpoint = argv[4]
        review_match = re.fullmatch(
            r"repos/Zest-LeadGen/contractoros-california/pulls/50/reviews\?per_page=100&page=([1-5])",
            endpoint,
        )
        permission_match = re.fullmatch(
            r"repos/Zest-LeadGen/contractoros-california/collaborators/([A-Za-z0-9][A-Za-z0-9-]{0,38})/permission",
            endpoint,
        )
        if review_match:
            return
        if permission_match and permission_match.group(1) in (allowed_permission_logins or set()):  # scope-bound approval evidence
            return
        raise CommandRejectedError("unbounded or unsourced GitHub API shape rejected")

    # Every other gh api shape and every GitHub mutation are forbidden.
    allowed_prefixes = {
        ("gh", "repo", "view"),
        ("gh", "issue", "view"),
        ("gh", "pr", "view"),
        ("gh", "pr", "checks"),
        ("gh", "run", "view"),
    }
    if len(argv) < 3 or tuple(argv[:3]) not in allowed_prefixes:
        raise CommandRejectedError("forbidden or unknown GitHub command rejected by command allowlist")
    if any(arg in {"--jq", "--template", "--web"} for arg in argv):
        raise CommandRejectedError("unknown GitHub output flag rejected by command allowlist")
    if tuple(argv[:3]) == ("gh", "repo", "view"):
        if len(argv) != 6 or argv.count("--repo") != 0 or argv.count("--json") != 1:
            raise CommandRejectedError("GitHub repository-read shape rejected by command allowlist")
        return
    if argv.count("--repo") != 1 or argv.count("--json") != 1:
        raise CommandRejectedError("GitHub command shape rejected by command allowlist")


def _run_read_command(
    argv: list[str],
    cwd: Path,
    timeout: int = 20,
    allowed_permission_logins: set[str] | None = None,  # scope-bound approval evidence
) -> tuple[str, dict[str, Any]]:
    _validate_command(argv, allowed_permission_logins)  # scope-bound approval evidence
    try:
        proc = subprocess.run(
            argv,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            shell=False,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CollectorError(f"required read command inaccessible: {argv[:3]}") from exc
    if len(proc.stdout.encode("utf-8")) > MAX_COMMAND_OUTPUT_BYTES:
        raise CollectorError("required read command output exceeds the bounded size limit")
    if len(proc.stderr.encode("utf-8")) > MAX_COMMAND_OUTPUT_BYTES:
        raise CollectorError("required read command error output exceeds the bounded size limit")
    result = {
        "argv": argv,
        "return_code": int(proc.returncode),
        "stdout_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
        "stderr_present": bool(proc.stderr.strip()),
    }
    if proc.returncode != 0:
        raise CollectorError(f"required read command failed: {argv[:3]}")
    return proc.stdout, result


def _json_command(
    argv: list[str],
    cwd: Path,
    commands: list[dict[str, Any]],
    allowed_permission_logins: set[str] | None = None,  # scope-bound approval evidence
) -> Any:
    output, result = _run_read_command(argv, cwd, allowed_permission_logins=allowed_permission_logins)  # scope-bound approval evidence
    commands.append(result)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise CollectorError("read command returned malformed JSON") from exc


def _extract_marker_blocks(body: str) -> dict[str, list[dict[str, Any]]]:
    text = str(body or "")
    if len(text) > MARKER_TEXT_LIMIT:
        raise CollectorError("marker evidence exceeds the bounded input limit")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    lines = text.splitlines()
    markers: dict[str, list[dict[str, Any]]] = {name: [] for name in MARKER_NAMES}
    for index, line in enumerate(lines):
        marker_name = line.strip()
        if marker_name not in markers:
            continue
        fields: dict[str, str] = {}
        duplicate_fields: list[str] = []
        for raw in lines[index + 1 :]:
            stripped = raw.strip()
            if stripped in MARKER_NAMES or stripped.startswith("#"):
                break
            if not stripped:
                continue
            match = re.match(r"^([^:]+):\s*(.*)$", stripped)
            if not match:
                continue
            field = match.group(1).strip()
            value = match.group(2).strip()
            if field in fields:
                duplicate_fields.append(field)
            else:
                fields[field] = value
        markers[marker_name].append(
            {"fields": fields, "duplicate_fields": sorted(set(duplicate_fields))}
        )
    return markers


def _parse_marker(body: str, marker_name: str) -> list[dict[str, str]]:
    """Compatibility view of the centralized bounded marker parser."""
    return [block["fields"] for block in _extract_marker_blocks(body).get(marker_name, [])]


def _multiple_marker_reason(prefix: str, blocks: list[dict[str, Any]]) -> str:
    normalized = [
        (tuple(sorted(block["fields"].items())), tuple(block["duplicate_fields"]))
        for block in blocks
    ]
    return f"{prefix}_DUPLICATE_GOVERNING_MARKERS" if len(set(normalized)) == 1 else f"{prefix}_CONFLICTING_GOVERNING_MARKERS"


def _evaluate_red_team_blocks(
    blocks: list[dict[str, Any]], pr_head: str, pr_number: int | str
) -> dict[str, Any]:
    if not blocks:
        return {"status": "missing", "bound_sha": None, "reasons": ["RT_MISSING"]}
    if len(blocks) > 1:
        reason = _multiple_marker_reason("RT", blocks)
        status = "ambiguous" if "DUPLICATE" in reason else "conflicting"
        return {"status": status, "bound_sha": None, "reasons": [reason]}

    block = blocks[0]
    marker = block["fields"]
    reasons = [f"RT_DUPLICATE_FIELD:{field}" for field in block["duplicate_fields"]]
    for field in RED_TEAM_REQUIRED_FIELDS:
        if not marker.get(field):
            reasons.append(f"RT_REQUIRED_FIELD_MISSING_OR_EMPTY:{field}")

    decision = marker.get("Decision", "")
    if decision and decision not in RED_TEAM_DECISIONS:
        reasons.append("RT_DECISION_UNSUPPORTED")
    elif decision == "BLOCKED":
        reasons.append("RT_DECISION_BLOCKED")
    elif decision == "CHANGES_REQUESTED":
        reasons.append("RT_DECISION_CHANGES_REQUESTED")

    current_pr = str(pr_number or "").strip().lstrip("#")
    marker_pr = marker.get("PR number", "").strip().lstrip("#")
    if marker_pr and not re.fullmatch(r"\d+", marker_pr):
        reasons.append("RT_PR_NUMBER_MALFORMED")
    elif marker_pr and current_pr and marker_pr != current_pr:
        reasons.append("RT_PR_NUMBER_MISMATCH")

    marker_sha = marker.get("PR head SHA", "")
    if marker_sha and not re.fullmatch(r"[0-9a-fA-F]{40}", marker_sha):
        reasons.append("RT_SHA_MALFORMED")
    elif marker_sha and pr_head and marker_sha.lower() != pr_head.lower():
        reasons.append("RT_SHA_MISMATCH")

    review_date = marker.get("Review date", "")
    if review_date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", review_date):
        reasons.append("RT_REVIEW_DATE_MALFORMED")
    if marker.get("SHA-bound statement") != RED_TEAM_SHA_BOUND_STATEMENT:
        reasons.append("RT_SHA_BOUND_STATEMENT_INVALID")

    reasons = sorted(set(reasons))
    if not reasons:
        return {"status": "valid", "bound_sha": marker_sha, "reasons": []}
    if reasons == ["RT_SHA_MISMATCH"]:
        status = "stale"
    elif any(reason in {"RT_DECISION_BLOCKED", "RT_DECISION_CHANGES_REQUESTED"} for reason in reasons):
        status = "adverse"
    else:
        status = "malformed"
    return {"status": status, "bound_sha": None, "reasons": reasons}


def _parse_categories(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _evaluate_owner_blocks(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    if not blocks:
        return {"status": "missing", "reasons": ["OWNER_MISSING"]}
    if len(blocks) > 1:
        reason = _multiple_marker_reason("OWNER", blocks)
        status = "ambiguous" if "DUPLICATE" in reason else "conflicting"
        return {"status": status, "reasons": [reason]}

    block = blocks[0]
    marker = block["fields"]
    reasons = [f"OWNER_DUPLICATE_FIELD:{field}" for field in block["duplicate_fields"]]
    for field in OWNER_REQUIRED_FIELDS:
        if not marker.get(field):
            reasons.append(f"OWNER_REQUIRED_FIELD_MISSING_OR_EMPTY:{field}")

    owner_required = marker.get("Owner interruption required", "")
    if owner_required and owner_required not in OWNER_INTERRUPTION_VALUES:
        reasons.append("OWNER_INTERRUPTION_VALUE_INVALID")

    categories = _parse_categories(marker.get("Trigger categories", ""))
    if marker.get("Trigger categories") and not categories:
        reasons.append("OWNER_CATEGORIES_EMPTY")
    if any(category not in OWNER_TRIGGER_CATEGORIES for category in categories):
        reasons.append("OWNER_CATEGORY_UNKNOWN")
    if "NONE" in categories and len(categories) > 1:
        reasons.append("OWNER_NONE_CATEGORY_CONFLICT")
    if owner_required == "YES" and categories == ["NONE"]:
        reasons.append("OWNER_INTERRUPTION_CATEGORY_CONFLICT")
    if owner_required == "NO" and categories != ["NONE"]:
        reasons.append("OWNER_INTERRUPTION_CATEGORY_CONFLICT")

    lane = marker.get("Lane eligibility", "")
    if lane and lane not in OWNER_LANE_VALUES:
        reasons.append("OWNER_LANE_VALUE_INVALID")
    if any(category != "NONE" for category in categories) and lane == "FUTURE_LOW_RISK_CANDIDATE":
        reasons.append("OWNER_CATEGORY_LANE_CONFLICT")
    if marker.get("Human approval required") and marker.get("Human approval required") != "YES":
        reasons.append("OWNER_HUMAN_APPROVAL_MUST_BE_YES")
    if marker.get("Auto-merge eligible") and marker.get("Auto-merge eligible") != "NO":
        reasons.append("OWNER_AUTO_MERGE_MUST_BE_NO")

    reasons = sorted(set(reasons))
    return {"status": "valid" if not reasons else "malformed", "reasons": reasons}


def _marker_evaluations(body: str, pr_head: str, pr_number: int | str) -> dict[str, Any]:
    blocks = _extract_marker_blocks(body)
    return {
        "owner": _evaluate_owner_blocks(blocks["OWNER_TRIGGER_REVIEW"]),
        "red_team": _evaluate_red_team_blocks(blocks["RED_TEAM_DECISION"], pr_head, pr_number),
    }


def _marker_summary(body: str, pr_head: str, pr_number: int | str = "") -> dict[str, Any]:
    evaluations = _marker_evaluations(body, pr_head, pr_number)
    owner = evaluations["owner"]
    red_team = evaluations["red_team"]
    return {
        "owner_trigger_status": "valid" if owner["status"] == "valid" else "missing_or_invalid",
        "red_team_status": (
            "valid" if red_team["status"] == "valid" else "missing" if red_team["status"] == "missing" else "stale"
        ),
        "red_team_bound_sha": red_team["bound_sha"] if red_team["status"] == "valid" else None,
    }


def _normalized_checks(raw: Any) -> list[dict[str, str]]:
    checks = []
    for item in raw if isinstance(raw, list) else []:
        checks.append(
            {
                "name": str(item.get("name") or ""),
                "state": str(item.get("state") or ""),
                "bucket": str(item.get("bucket") or ""),
                "link": str(item.get("link") or ""),
            }
        )
    return sorted(
        checks,
        key=lambda item: (item["name"], item["state"], item["bucket"], item["link"]),
    )


def _normalized_jobs(raw: Any) -> list[dict[str, Any]]:
    jobs = []
    for job in raw if isinstance(raw, list) else []:
        steps = [
            {
                "name": str(step.get("name") or ""),
                "number": int(step.get("number") or 0),
                "status": str(step.get("status") or ""),
                "conclusion": str(step.get("conclusion") or "") or None,
            }
            for step in (job.get("steps") or [])
        ]
        jobs.append(
            {
                "name": str(job.get("name") or ""),
                "status": str(job.get("status") or ""),
                "conclusion": str(job.get("conclusion") or "") or None,
                "steps": sorted(steps, key=lambda item: (item["number"], item["name"])),
            }
        )
    return sorted(jobs, key=lambda item: (item["name"], _canonical_json(item)))


def _normalized_review_record(raw: Any) -> dict[str, Any]:
    user = raw.get("user") or {} if isinstance(raw, dict) else {}
    return {
        "review_id": raw.get("id") if isinstance(raw, dict) else None,
        "reviewer_login": str(user.get("login") or ""),  # scope-bound approval evidence
        "reviewer_type": str(user.get("type") or ""),
        "state": str(raw.get("state") or "").upper() if isinstance(raw, dict) else "",
        "submitted_at": raw.get("submitted_at") if isinstance(raw, dict) else None,
        "commit_id": str(raw.get("commit_id") or "") if isinstance(raw, dict) else "",
        "author_association": str(raw.get("author_association") or "") if isinstance(raw, dict) else "",  # scope-bound approval evidence
    }


def _review_sort_key(record: dict[str, Any]) -> tuple[str, int, str]:
    return (
        str(record.get("submitted_at") or ""),
        int(record.get("review_id") or 0) if isinstance(record.get("review_id"), int) else 0,
        _canonical_json(record),
    )


def _approval_evaluation(pr: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    """Recompute qualifying approvals from normalized, public-safe evidence."""
    blocked: list[str] = []
    quarantined: list[str] = []
    status = str(review.get("evidence_status") or "")
    records = review.get("review_records")
    permissions = review.get("permission_records")
    if status not in {"complete", "truncated", "unavailable"}:
        quarantined.append("Approval evidence status is malformed")
    if status == "truncated":
        blocked.append("Review approval evidence is truncated")
    if status == "unavailable":
        blocked.append("Review or permission approval evidence is unavailable")
    if not isinstance(records, list) or not isinstance(permissions, list):
        blocked.append("Required normalized approval evidence is missing")
        records = records if isinstance(records, list) else []
        permissions = permissions if isinstance(permissions, list) else []
    if len(records) > MAX_REVIEW_RECORDS:
        blocked.append("Review approval evidence exceeds the bounded record limit")
    if len(permissions) > MAX_PERMISSION_CANDIDATES:
        blocked.append("Permission approval evidence exceeds the bounded candidate limit")

    normalized_records: list[dict[str, Any]] = []
    records_by_id: dict[int, dict[str, Any]] = {}
    duplicate_ids: set[int] = set()
    conflicting_ids: set[int] = set()
    malformed_logins: set[str] = set()  # scope-bound approval evidence
    for raw in records[:MAX_REVIEW_RECORDS]:
        if not isinstance(raw, dict):
            quarantined.append("Approval review record is malformed")
            continue
        record = {
            "review_id": raw.get("review_id"),
            "reviewer_login": str(raw.get("reviewer_login") or ""),  # scope-bound approval evidence
            "reviewer_type": str(raw.get("reviewer_type") or ""),
            "state": str(raw.get("state") or "").upper(),
            "submitted_at": raw.get("submitted_at"),
            "commit_id": str(raw.get("commit_id") or ""),
            "author_association": str(raw.get("author_association") or ""),  # scope-bound approval evidence
        }
        review_id = record["review_id"]
        login = record["reviewer_login"] or "_evidence"  # scope-bound approval evidence
        malformed = (
            not isinstance(review_id, int)
            or review_id <= 0
            or not GITHUB_LOGIN_RE.fullmatch(record["reviewer_login"])  # scope-bound approval evidence
            or record["state"] not in REVIEW_STATES
            or not _is_sha(record["commit_id"])
        )
        if malformed:
            malformed_logins.add(login)  # scope-bound approval evidence
            quarantined.append("Approval review record is malformed")
        if isinstance(review_id, int) and review_id in records_by_id:
            duplicate_ids.add(review_id)
            if records_by_id[review_id] != record:
                conflicting_ids.add(review_id)
        elif isinstance(review_id, int):
            records_by_id[review_id] = record
        normalized_records.append(record)
    if duplicate_ids:
        quarantined.append("Duplicate approval review IDs are ambiguous")
    if conflicting_ids:
        quarantined.append("Conflicting duplicate approval review records are ambiguous")
    normalized_records.sort(key=_review_sort_key)

    permission_by_login: dict[str, dict[str, str]] = {}  # scope-bound approval evidence
    permission_conflicts: set[str] = set()
    approved_source_logins = {  # scope-bound approval evidence
        record["reviewer_login"]  # scope-bound approval evidence
        for record in normalized_records
        if record["state"] == "APPROVED"
        and record["commit_id"] == pr.get("head")
        and record["reviewer_type"] == "User"
        and record["reviewer_login"] != pr.get("author_login")  # scope-bound approval evidence
        and record.get("submitted_at")
    }
    normalized_permissions: list[dict[str, str]] = []
    for raw in permissions[:MAX_PERMISSION_CANDIDATES]:
        if not isinstance(raw, dict):
            quarantined.append("Permission approval record is malformed")
            continue
        item = {
            "reviewer_login": str(raw.get("reviewer_login") or ""),  # scope-bound approval evidence
            "permission": str(raw.get("permission") or "").lower(),
            "role_name": str(raw.get("role_name") or ""),
            "account_type": str(raw.get("account_type") or ""),
        }
        login = item["reviewer_login"]  # scope-bound approval evidence
        if login not in approved_source_logins:  # scope-bound approval evidence
            quarantined.append("Permission evidence identity is not sourced from normalized review evidence")
        if login in permission_by_login and permission_by_login[login] != item:  # scope-bound approval evidence
            permission_conflicts.add(login)  # scope-bound approval evidence
        permission_by_login[login] = item  # scope-bound approval evidence
        normalized_permissions.append(item)
    if permission_conflicts:
        quarantined.append("Permission evidence is internally contradictory")
    normalized_permissions.sort(key=lambda item: (item["reviewer_login"], _canonical_json(item)))  # scope-bound approval evidence

    reasons: dict[str, list[str]] = {}

    def disqualify(login: str, reason: str) -> None:  # scope-bound approval evidence
        reasons.setdefault(login or "_evidence", []).append(reason)  # scope-bound approval evidence

    for login in malformed_logins:  # scope-bound approval evidence
        disqualify(login, "APPROVAL_REVIEW_RECORD_MALFORMED")  # scope-bound approval evidence
    for review_id in duplicate_ids:
        matching = [r for r in normalized_records if r.get("review_id") == review_id]
        for record in matching:
            disqualify(record.get("reviewer_login") or "_evidence", "APPROVAL_REVIEW_RECORD_MALFORMED")  # scope-bound approval evidence

    qualifying: list[str] = []
    reviewer_logins = sorted({r["reviewer_login"] for r in normalized_records if r["reviewer_login"]})  # scope-bound approval evidence
    for login in reviewer_logins:  # scope-bound approval evidence
        reviewer_records = [r for r in normalized_records if r["reviewer_login"] == login]  # scope-bound approval evidence
        approvals = [r for r in reviewer_records if r["state"] == "APPROVED"]
        if not approvals:
            continue
        current_decisive = [
            r
            for r in reviewer_records
            if r["commit_id"] == pr.get("head")
            and r["state"] in DECISIVE_REVIEW_STATES
            and r.get("submitted_at")
        ]
        latest = max(current_decisive, key=_review_sort_key) if current_decisive else None
        if latest is None or latest["state"] != "APPROVED":
            if any(r["commit_id"] != pr.get("head") for r in approvals):
                disqualify(login, "APPROVAL_STALE_HEAD")  # scope-bound approval evidence
            if latest and latest["state"] == "CHANGES_REQUESTED":
                disqualify(login, "APPROVAL_SUPERSEDED_BY_CHANGES_REQUESTED")  # scope-bound approval evidence
            if latest and latest["state"] == "DISMISSED":
                disqualify(login, "APPROVAL_DISMISSED")  # scope-bound approval evidence
            if any(not r.get("submitted_at") for r in approvals):
                disqualify(login, "APPROVAL_NOT_SUBMITTED")  # scope-bound approval evidence
            continue
        if latest["reviewer_type"] != "User":
            disqualify(login, "APPROVAL_BOT_ACCOUNT")  # scope-bound approval evidence
            continue
        if login == pr.get("author_login"):  # scope-bound approval evidence
            disqualify(login, "APPROVAL_PR_AUTHOR")  # scope-bound approval evidence
            continue
        permission = permission_by_login.get(login)  # scope-bound approval evidence
        if permission is None:
            blocked.append(f"Permission evidence is missing for approval candidate: {login}")
            disqualify(login, "APPROVAL_PERMISSION_EVIDENCE_MISSING")  # scope-bound approval evidence
            continue
        if permission["reviewer_login"] != login or permission["account_type"] != "User":  # scope-bound approval evidence
            quarantined.append("Permission evidence identity differs from the approval reviewer")
            disqualify(login, "APPROVAL_PERMISSION_IDENTITY_MISMATCH")  # scope-bound approval evidence
            continue
        base_permission = permission["permission"]
        if base_permission in {"write", "admin"}:
            qualifying.append(login)  # scope-bound approval evidence
        elif base_permission == "read":
            disqualify(login, "APPROVAL_PERMISSION_READ_ONLY")  # scope-bound approval evidence
        elif base_permission == "none":
            disqualify(login, "APPROVAL_PERMISSION_NONE")  # scope-bound approval evidence
        else:
            disqualify(login, "APPROVAL_PERMISSION_UNKNOWN")  # scope-bound approval evidence

    qualifying = sorted(set(qualifying))
    claimed = review.get("qualifying_approvals")
    if claimed is not None and sorted(set(claimed)) != qualifying:
        quarantined.append("Claimed qualifying approvals contradict computed approval evidence")
    if str(review.get("decision") or "").upper() == "APPROVED" and not qualifying:
        quarantined.append("Review decision claims approval without a qualifying current-head approver")
    normalized_reasons = {key: sorted(set(value)) for key, value in sorted(reasons.items())}
    result = {
        "decision": str(review.get("decision") or "") or None,
        "evidence_status": status,
        "review_records": normalized_records,
        "permission_records": normalized_permissions,
        "qualifying_approvals": qualifying,
        "disqualified_approvals": sorted(normalized_reasons),
        "disqualification_reasons": normalized_reasons,
    }
    return {
        "review": result,
        "blocked": sorted(set(blocked)),
        "quarantined": sorted(set(quarantined)),
    }


def _collect_review_evidence(
    repo_root: Path,
    commands: list[dict[str, Any]],
    pr_head: str,
    pr_author_login: str,  # scope-bound approval evidence
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    evidence_status = "complete"
    for page in range(1, MAX_REVIEW_PAGES + 1):
        raw_page = _json_command(
            [
                "gh",
                "api",
                "--method",
                "GET",
                f"repos/{EXPECTED_REPOSITORY}/pulls/50/reviews?per_page={REVIEW_PAGE_SIZE}&page={page}",
            ],
            repo_root,
            commands,
        )
        if not isinstance(raw_page, list):
            raise ApprovalEvidenceUnavailableError("review approval evidence is not a JSON array")
        if len(raw_page) > REVIEW_PAGE_SIZE:
            raise ApprovalEvidenceUnavailableError("review approval page exceeds the bounded page size")
        records.extend(_normalized_review_record(item) for item in raw_page)
        if len(records) > MAX_REVIEW_RECORDS:
            raise ApprovalEvidenceUnavailableError("review approval evidence exceeds the bounded record limit")
        if len(raw_page) < REVIEW_PAGE_SIZE:
            break
        if page == MAX_REVIEW_PAGES:
            evidence_status = "truncated"

    permission_records: list[dict[str, str]] = []
    if evidence_status == "complete":
        candidates = sorted(
            {
                record["reviewer_login"]  # scope-bound approval evidence
                for record in records
                if record["state"] == "APPROVED"
                and record["commit_id"] == pr_head
                and record.get("submitted_at")
                and record["reviewer_type"] == "User"
                and record["reviewer_login"] != pr_author_login  # scope-bound approval evidence
                and GITHUB_LOGIN_RE.fullmatch(record["reviewer_login"])  # scope-bound approval evidence
            }
        )
        if len(candidates) > MAX_PERMISSION_CANDIDATES:
            raise ApprovalEvidenceUnavailableError("permission approval candidates exceed the bounded limit")
        allowed = set(candidates)
        for login in candidates:  # scope-bound approval evidence
            try:
                permission = _json_command(
                    [
                        "gh",
                        "api",
                        "--method",
                        "GET",
                        f"repos/{EXPECTED_REPOSITORY}/collaborators/{login}/permission",  # scope-bound approval evidence
                    ],
                    repo_root,
                    commands,
                    allowed_permission_logins=allowed,  # scope-bound approval evidence
                )
            except CollectorError as exc:
                raise ApprovalEvidenceUnavailableError(
                    f"permission approval evidence is inaccessible for reviewer: {login}"  # scope-bound approval evidence
                ) from exc
            user = permission.get("user") or {} if isinstance(permission, dict) else {}
            permission_records.append(
                {
                    "reviewer_login": login,  # scope-bound approval evidence
                    "permission": str(permission.get("permission") or "") if isinstance(permission, dict) else "",
                    "role_name": str(permission.get("role_name") or "") if isinstance(permission, dict) else "",
                    "account_type": str(user.get("type") or ""),
                }
            )
    return {
        "evidence_status": evidence_status,
        "review_records": records,
        "permission_records": permission_records,
    }


def _collect_live(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve(strict=True)
    if not (repo_root / ".git").exists():
        raise CollectorError("repo root is not a Git repository")
    if not _is_sha(args.canonical_ref):
        raise CollectorError("canonical ref must be an exact 40-character lowercase SHA")
    if (
        args.repository != EXPECTED_REPOSITORY
        or args.issue_number != 49
        or args.pr_number != 50
    ):
        raise CollectorError("live approval collection is bounded to Issue #49 and PR #50")

    commands: list[dict[str, Any]] = []

    def read(argv: list[str]) -> str:
        output, result = _run_read_command(argv, repo_root)
        commands.append(result)
        return output.strip()

    remote = read(["git", "remote", "get-url", "origin"])
    local_head = read(["git", "rev-parse", "HEAD"])
    local_main = read(["git", "rev-parse", "main"])
    local_origin = read(["git", "rev-parse", "origin/main"])
    read(["git", "rev-parse", "--show-toplevel"])
    read(["git", "status", "--porcelain=v1", "--branch"])
    canonical_raw = read(["git", "show", f"{args.canonical_ref}:{CANONICAL_PATH}"])
    try:
        canonical = json.loads(canonical_raw)
    except json.JSONDecodeError as exc:
        raise CollectorError("canonical state is malformed") from exc

    repo = _json_command(
        ["gh", "repo", "view", args.repository, "--json", "nameWithOwner,defaultBranchRef"],
        repo_root,
        commands,
    )
    issue = _json_command(
        [
            "gh",
            "issue",
            "view",
            str(args.issue_number),
            "--repo",
            args.repository,
            "--json",
            "number,state,stateReason,url,closedAt,title",
        ],
        repo_root,
        commands,
    )
    pr = _json_command(
        [
            "gh",
            "pr",
            "view",
            str(args.pr_number),
            "--repo",
            args.repository,
            "--json",
            "number,state,baseRefName,headRefName,headRefOid,isDraft,mergeCommit,mergedAt,url,autoMergeRequest,reviewDecision,author,body",  # scope-bound approval evidence
        ],
        repo_root,
        commands,
    )
    raw_checks = _json_command(
        [
            "gh",
            "pr",
            "checks",
            str(args.pr_number),
            "--repo",
            args.repository,
            "--json",
            "name,state,bucket,link",
        ],
        repo_root,
        commands,
    )
    run = _json_command(
        [
            "gh",
            "run",
            "view",
            str(args.run_id),
            "--repo",
            args.repository,
            "--json",
            "databaseId,name,workflowDatabaseId,event,status,conclusion,headSha,headBranch,url,jobs",
        ],
        repo_root,
        commands,
    )

    default_ref = repo.get("defaultBranchRef") or {}
    pr_author = pr.get("author") or {}  # scope-bound approval evidence
    approval_evidence = _collect_review_evidence(
        repo_root,
        commands,
        str(pr.get("headRefOid") or ""),
        str(pr_author.get("login") or ""),  # scope-bound approval evidence
    )
    marker = _marker_summary(
        str(pr.get("body") or ""),
        str(pr.get("headRefOid") or ""),
        int(pr.get("number")),
    )
    evidence = {
        "fixture_version": FIXTURE_VERSION,
        "repository": {
            "name": str(repo.get("nameWithOwner") or args.repository),
            "default_branch": str(default_ref.get("name") or "main"),
            "remote_identifier": hashlib.sha256(remote.encode("utf-8")).hexdigest(),
        },
        "source_shas": {
            "local_head": local_head,
            "local_main": local_main,
            "local_origin_main": local_origin,
            "live_default_branch": str((default_ref.get("target") or {}).get("oid") or local_origin),
            "canonical_ref": args.canonical_ref,
        },
        "canonical_state": canonical,
        "issue": {
            "number": int(issue.get("number")),
            "state": str(issue.get("state") or "").lower(),
            "state_reason": str(issue.get("stateReason") or "").lower() or None,
            "url": str(issue.get("url") or ""),
            "closeout_state": "closed" if issue.get("closedAt") else "open",
        },
        "pr": {
            "number": int(pr.get("number")),
            "state": str(pr.get("state") or "").lower(),
            "base": str(pr.get("baseRefName") or ""),
            "head_branch": str(pr.get("headRefName") or ""),
            "head": str(pr.get("headRefOid") or ""),
            "draft": bool(pr.get("isDraft")),
            "merge_commit": (pr.get("mergeCommit") or {}).get("oid"),
            "merged_at": pr.get("mergedAt"),
            "url": str(pr.get("url") or ""),
            "author_login": str(pr_author.get("login") or ""),  # scope-bound approval evidence
            "author_type": "Bot" if pr_author.get("is_bot") else "User",  # scope-bound approval evidence
        },
        "checks": _normalized_checks(raw_checks),
        "workflow_run": {
            "id": int(run.get("databaseId")),
            "name": str(run.get("name") or ""),
            "workflow_id": int(run.get("workflowDatabaseId") or 0),
            "event": str(run.get("event") or ""),
            "status": str(run.get("status") or ""),
            "conclusion": str(run.get("conclusion") or "") or None,
            "head_sha": str(run.get("headSha") or ""),
            "head_branch": str(run.get("headBranch") or ""),
            "url": str(run.get("url") or ""),
            "jobs": _normalized_jobs(run.get("jobs")),
        },
        "markers": marker,
        "review": {
            "decision": str(pr.get("reviewDecision") or "") or None,
            **approval_evidence,
        },
        "auto_merge": {"active": bool(pr.get("autoMergeRequest"))},
        "lifecycle_claim": "active_pr" if str(pr.get("state") or "").upper() == "OPEN" else "closed_gate",
        "raw_chat_status": "no authority",
        "source_commands": commands,
    }
    evidence["review"] = _approval_evaluation(evidence["pr"], evidence["review"])["review"]
    _reject_unsafe(evidence)
    return evidence


def _load_fixture(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CollectorError("fixture input is inaccessible") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CollectorError("fixture input is malformed JSON") from exc
    if not isinstance(value, dict):
        raise CollectorError("fixture input must be an object")
    _reject_unsafe(value)
    return value


def _validate_input(data: dict[str, Any]) -> None:
    required = {
        "fixture_version",
        "repository",
        "source_shas",
        "canonical_state",
        "issue",
        "pr",
        "checks",
        "workflow_run",
        "markers",
        "review",
        "auto_merge",
        "lifecycle_claim",
        "raw_chat_status",
    }
    if set(data) - (required | {"source_commands"}):
        raise CollectorError("fixture contains unknown top-level fields")
    if not required.issubset(data):
        raise CollectorError("fixture is missing required top-level fields")
    if data.get("fixture_version") != FIXTURE_VERSION:
        raise CollectorError("fixture version is unsupported")
    if data.get("raw_chat_status") != "no authority":
        raise CollectorError("raw chat input has no authority")
    if data.get("lifecycle_claim") not in {"active_pr", "externally_approved", "merge_ready", "closed_gate"}:
        raise CollectorError("lifecycle claim is invalid")
    source = data.get("source_shas")
    if not isinstance(source, dict) or set(source) != {
        "local_head",
        "local_main",
        "local_origin_main",
        "live_default_branch",
        "canonical_ref",
    }:
        raise CollectorError("source SHA object is malformed")
    if any(value is not None and not _is_sha(value) for value in source.values()):
        raise CollectorError("source SHA is malformed")
    canonical = data.get("canonical_state")
    if not isinstance(canonical, dict):
        raise CollectorError("canonical state is malformed")
    canonical_required = {
        "schema_version",
        "snapshot_semantics",
        "current_main_sha",
        "linked_issue",
        "linked_pr",
        "lifecycle_state",
        "consistency_status",
    }
    if not canonical_required.issubset(canonical):
        raise CollectorError("canonical state is missing required fields")
    if canonical.get("snapshot_semantics") != "observed_snapshot_requires_live_verification":
        raise CollectorError("canonical snapshot semantics are invalid")
    if not _is_sha(canonical.get("current_main_sha")):
        raise CollectorError("canonical main SHA is malformed")
    if canonical.get("consistency_status") not in CLASSIFICATIONS:
        raise CollectorError("canonical consistency status is invalid")
    for key in ("repository", "issue", "pr", "workflow_run", "markers", "review", "auto_merge"):
        if not isinstance(data.get(key), dict):
            raise CollectorError(f"{key} evidence is malformed")
    if not isinstance(data.get("checks"), list):
        raise CollectorError("checks evidence is malformed")
    pr = data["pr"]
    if not GITHUB_LOGIN_RE.fullmatch(str(pr.get("author_login") or "")):  # scope-bound approval evidence
        raise CollectorError("PR author login evidence is malformed")  # scope-bound approval evidence
    if pr.get("author_type") not in {"User", "Bot"}:  # scope-bound approval evidence
        raise CollectorError("PR author account type evidence is malformed")  # scope-bound approval evidence
    review = data["review"]
    review_required = {
        "decision",
        "evidence_status",
        "review_records",
        "permission_records",
        "qualifying_approvals",
        "disqualified_approvals",
        "disqualification_reasons",
    }
    if not review_required.issubset(review):
        raise CollectorError("normalized approval evidence is missing required fields")


def _control_workflow_evaluation(data: dict[str, Any]) -> dict[str, list[str]]:
    repository = data["repository"]
    pr = data["pr"]
    checks = data["checks"]
    run = data["workflow_run"]
    markers = data["markers"]
    blocked: list[str] = []
    quarantined: list[str] = []

    identity = (
        ("repository", repository.get("name"), EXPECTED_REPOSITORY),
        ("workflow name", run.get("name"), EXPECTED_WORKFLOW_NAME),
        ("workflow ID", run.get("workflow_id"), EXPECTED_WORKFLOW_ID),
        ("workflow event", run.get("event"), EXPECTED_WORKFLOW_EVENT),
        ("workflow head SHA", run.get("head_sha"), pr.get("head")),
        ("workflow head branch", run.get("head_branch"), pr.get("head_branch")),
    )
    for label, actual, expected in identity:
        if actual in {None, "", 0}:
            blocked.append(f"Missing required workflow evidence: {label}")
        elif actual != expected:
            quarantined.append(f"Workflow provenance mismatch: {label}")

    run_id = run.get("id")
    expected_link = re.compile(
        rf"^https://github\.com/{re.escape(EXPECTED_REPOSITORY)}/actions/runs/{run_id}(?:/job/\d+)?$"
    )
    expected_checks = [check for check in checks if check.get("name") == EXPECTED_JOB_NAME]
    if not expected_checks:
        blocked.append("Missing required ContractorOS PR check")
    elif len(expected_checks) > 1:
        quarantined.append("Duplicate ContractorOS PR checks")
    elif not expected_link.fullmatch(str(expected_checks[0].get("link") or "")):
        quarantined.append("ContractorOS PR check link differs from the supplied workflow run")
    for check in checks:
        if check.get("name") == EXPECTED_JOB_NAME:
            continue
        if str(check.get("state") or "").upper() in {
            "FAILURE",
            "ERROR",
            "CANCELLED",
            "TIMED_OUT",
            "ACTION_REQUIRED",
        } or str(check.get("bucket") or "").lower() == "fail":
            quarantined.append("Unknown failed PR check contradicts the governed lifecycle")

    jobs = run.get("jobs") if isinstance(run.get("jobs"), list) else []
    expected_jobs = [job for job in jobs if job.get("name") == EXPECTED_JOB_NAME]
    if not expected_jobs:
        blocked.append("Missing expected ContractorOS workflow job")
    elif len(expected_jobs) > 1:
        quarantined.append("Duplicate expected ContractorOS workflow jobs")

    if blocked or quarantined or len(expected_jobs) != 1 or len(expected_checks) != 1:
        return {"blocked": sorted(set(blocked)), "quarantined": sorted(set(quarantined))}

    run_status = str(run.get("status") or "").lower()
    if run_status != "completed":
        blocked.append("ContractorOS workflow run is pending or in progress")
        return {"blocked": sorted(set(blocked)), "quarantined": []}

    job = expected_jobs[0]
    if str(job.get("status") or "").lower() != "completed":
        blocked.append("ContractorOS workflow job is pending or in progress")
        return {"blocked": sorted(set(blocked)), "quarantined": []}

    steps = job.get("steps") if isinstance(job.get("steps"), list) else []
    by_name: dict[str, list[dict[str, Any]]] = {}
    for step in steps:
        by_name.setdefault(str(step.get("name") or ""), []).append(step)
    for name in REQUIRED_STEPS:
        count = len(by_name.get(name, []))
        if count == 0:
            blocked.append(f"Missing required workflow step: {name}")
        elif count > 1:
            quarantined.append(f"Duplicate required workflow step: {name}")
    if blocked or quarantined:
        return {"blocked": sorted(set(blocked)), "quarantined": sorted(set(quarantined))}

    governed = [by_name[name][0] for name in REQUIRED_STEPS]
    numbers = [int(step.get("number") or 0) for step in governed]
    if any(number <= 0 for number in numbers) or numbers != sorted(numbers) or len(set(numbers)) != len(numbers):
        quarantined.append("Required workflow step order is invalid")
    if any(str(step.get("status") or "").lower() != "completed" for step in governed):
        quarantined.append("A required workflow step is not completed in a completed run")

    for job_item in jobs:
        if job_item is job:
            continue
        if str(job_item.get("status") or "").lower() != "completed" or str(
            job_item.get("conclusion") or ""
        ).lower() not in {"success", "skipped"}:
            quarantined.append("Unknown workflow job evidence contradicts the governed lifecycle")
    for step in steps:
        name = str(step.get("name") or "")
        if name in REQUIRED_STEPS or name in IGNORED_RUNNER_STEPS:
            continue
        if str(step.get("status") or "").lower() != "completed" or str(
            step.get("conclusion") or ""
        ).lower() not in {"success", "skipped"}:
            quarantined.append("Unknown workflow step evidence contradicts the governed lifecycle")

    conclusions = {
        name: str(by_name[name][0].get("conclusion") or "").lower() for name in REQUIRED_STEPS
    }
    pre = [conclusions[name] for name in PRE_MARKER_STEPS]
    marker = conclusions[MARKER_STEP]
    post = [conclusions[name] for name in POST_MARKER_STEPS]
    run_conclusion = str(run.get("conclusion") or "").lower()
    job_conclusion = str(job.get("conclusion") or "").lower()
    check_state = str(expected_checks[0].get("state") or "").upper()
    red_status = markers.get("red_team_status")

    if any(value != "success" for value in pre):
        quarantined.append("A required pre-marker workflow step did not succeed")
    if marker == "success" and red_status != "valid":
        quarantined.append("Marker step succeeded without valid exact-head marker evidence")
    if marker != "success" and red_status == "valid":
        quarantined.append("Valid exact-head marker evidence conflicts with the marker step")
    if marker != "success" and any(value == "success" for value in post):
        quarantined.append("A post-marker workflow step succeeded before the marker gate")
    if marker == "success" and any(value != "success" for value in post):
        quarantined.append("A post-marker workflow step did not succeed after the marker gate")

    missing_marker_matrix = (
        red_status == "missing"
        and pre == ["success"] * len(PRE_MARKER_STEPS)
        and marker == "failure"
        and post == ["skipped"] * len(POST_MARKER_STEPS)
        and run_conclusion == "failure"
        and job_conclusion == "failure"
        and check_state == "FAILURE"
    )
    approved_matrix = (
        red_status == "valid"
        and pre == ["success"] * len(PRE_MARKER_STEPS)
        and marker == "success"
        and post == ["success"] * len(POST_MARKER_STEPS)
        and run_conclusion == "success"
        and job_conclusion == "success"
        and check_state == "SUCCESS"
    )
    if not missing_marker_matrix and not approved_matrix:
        quarantined.append("Workflow run, job, check and required-step evidence are contradictory")

    return {"blocked": sorted(set(blocked)), "quarantined": sorted(set(quarantined))}


def _compare(
    data: dict[str, Any], approval: dict[str, Any] | None = None
) -> tuple[str, list[str], list[str], bool]:
    source = data["source_shas"]
    canonical = data["canonical_state"]
    issue = data["issue"]
    pr = data["pr"]
    run = data["workflow_run"]
    markers = data["markers"]
    review = data["review"]
    findings: list[str] = []
    blockers: list[str] = []

    required_values = {
        "local main SHA": source.get("local_main"),
        "live default-branch SHA": source.get("live_default_branch"),
        "issue number": issue.get("number"),
        "issue state": issue.get("state"),
        "PR number": pr.get("number"),
        "PR state": pr.get("state"),
        "PR head branch": pr.get("head_branch"),
        "PR head": pr.get("head"),
        "workflow run ID": run.get("id"),
        "workflow name": run.get("name"),
        "workflow ID": run.get("workflow_id"),
        "workflow event": run.get("event"),
        "workflow run head": run.get("head_sha"),
        "workflow run branch": run.get("head_branch"),
    }
    missing = [label for label, value in required_values.items() if value in {None, ""}]
    if missing:
        blockers.extend(f"Missing required evidence: {label}" for label in missing)
        return "blocked", sorted(findings), sorted(blockers), False

    canonical_issue = canonical.get("linked_issue") or {}
    canonical_pr = canonical.get("linked_pr") or {}
    if source["local_main"] != source["live_default_branch"]:
        findings.append("Local main differs from the live default branch")
    if source.get("local_origin_main") and source["local_origin_main"] != source["live_default_branch"]:
        findings.append("Local origin/main differs from the live default branch")
    if canonical["current_main_sha"] != source["live_default_branch"]:
        findings.append("Canonical main differs from the live default branch")
    if canonical_issue.get("number") != issue.get("number"):
        findings.append("Canonical linked issue differs from live issue")
    if canonical_pr and canonical_pr.get("number") != pr.get("number"):
        findings.append("Canonical linked PR differs from live PR")
    canonical_issue_state = str(canonical_issue.get("state") or "").lower()
    live_issue_state = str(issue.get("state") or "").lower()
    issue_states_agree = (
        canonical_issue_state in {"active", "open"} and live_issue_state in {"active", "open"}
    ) or (canonical_issue_state == "closed_completed" and live_issue_state == "closed")
    if not issue_states_agree:
        findings.append("Canonical issue lifecycle differs from live issue lifecycle")
    canonical_pr_state = str(canonical_pr.get("state") or "").lower()
    live_pr_state = str(pr.get("state") or "").lower()
    if canonical_pr_state and canonical_pr_state != live_pr_state:
        findings.append("Canonical PR lifecycle differs from live PR lifecycle")
    if data["lifecycle_claim"] == "closed_gate" and canonical.get("lifecycle_state") != "phase_closed_ready_for_next_phase":
        findings.append("Canonical lifecycle state differs from the closed gate")
    observed_head = canonical_pr.get("observed_head_sha") if isinstance(canonical_pr, dict) else None
    if observed_head and observed_head != pr.get("head"):
        findings.append("Canonical observed PR head moved")
        return "quarantined", sorted(findings), sorted(blockers), True
    if data["lifecycle_claim"] == "active_pr" and (
        str(pr.get("state") or "").lower() != "open"
        or str(issue.get("state") or "").lower() not in {"open", "active"}
        or pr.get("merge_commit")
    ):
        findings.append("Active-PR lifecycle evidence is contradictory")
        return "quarantined", sorted(set(findings)), sorted(blockers), True
    if findings:
        return "stale", sorted(findings), sorted(blockers), False
    if markers.get("owner_trigger_status") != "valid":
        findings.append("Owner-trigger marker evidence is missing, malformed, conflicting, or ambiguous")
        return "quarantined", sorted(findings), sorted(blockers), True
    if markers.get("red_team_status") == "stale":
        findings.append("Red-team marker evidence is stale, adverse, malformed, conflicting, or ambiguous")
        return "quarantined", sorted(findings), sorted(blockers), True
    if data["auto_merge"].get("active"):
        findings.append("Auto-merge is active despite the gate prohibition")
        return "quarantined", sorted(findings), sorted(blockers), True
    workflow = _control_workflow_evaluation(data)
    if workflow["blocked"]:
        blockers.extend(workflow["blocked"])
        return "blocked", sorted(findings), sorted(set(blockers)), False
    if workflow["quarantined"]:
        findings.extend(workflow["quarantined"])
        return "quarantined", sorted(set(findings)), sorted(blockers), True

    approval = approval or _approval_evaluation(pr, review)
    if approval["quarantined"]:
        findings.extend(approval["quarantined"])
        return "quarantined", sorted(set(findings)), sorted(blockers), True
    if approval["blocked"]:
        blockers.extend(approval["blocked"])
        return "blocked", sorted(findings), sorted(set(blockers)), False

    claim = data["lifecycle_claim"]
    pr_state = str(pr.get("state") or "").lower()
    issue_state = str(issue.get("state") or "").lower()
    approvals = review.get("qualifying_approvals") or []
    red_status = markers.get("red_team_status")

    if claim == "active_pr":
        if pr_state != "open" or issue_state not in {"open", "active"} or pr.get("merge_commit"):
            findings.append("Active-PR lifecycle evidence is contradictory")
            return "quarantined", sorted(findings), sorted(blockers), True
        if red_status == "missing":
            blockers.append("External exact-SHA red-team review is pending")
        if not approvals:
            blockers.append("Human/write-access approval is pending")
        blockers.append("Merge, main verification and linked-issue closeout are pending")
        findings.append("Active developer PR requires live verification and external review")
        return "requires_live_verification", sorted(findings), sorted(set(blockers)), False

    if claim in {"externally_approved", "merge_ready"}:
        if red_status != "valid" or not approvals:
            findings.append("Approval or merge-readiness claim lacks current required evidence")
            return "quarantined", sorted(findings), sorted(blockers), True
        return "requires_live_verification", sorted(findings), sorted(blockers), False

    closed_consistent = (
        pr_state == "merged"
        and issue_state == "closed"
        and issue.get("closeout_state") == "closed"
        and pr.get("merge_commit") == source["live_default_branch"]
        and markers.get("red_team_status") == "valid"
        and markers.get("red_team_bound_sha") == pr.get("head")
        and bool(approvals)
        and run.get("status") == "completed"
        and run.get("conclusion") == "success"
    )
    if not closed_consistent:
        findings.append("Merged or closed gate evidence is contradictory or incomplete")
        return "quarantined", sorted(findings), sorted(blockers), True
    findings.append("Merged gate, main, review, approval, run and closeout evidence agree")
    return "consistent", sorted(findings), sorted(blockers), False


def _packet_data(data: dict[str, Any], observed_at: str, classification: str, findings: list[str], blockers: list[str], quarantine: bool) -> dict[str, Any]:
    pr = data["pr"]
    next_action = (
        "External exact-SHA review must rerun this collector against the current PR head."
        if classification == "requires_live_verification"
        else "Stop and reconcile the listed evidence before any consequential action."
        if classification != "consistent"
        else "Verify the merged gate remains current before planning a later phase."
    )
    return {
        "schema_version": PACKET_SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "observed_at": observed_at,
        "repository": data["repository"]["name"],
        "canonical_schema_version": str(data["canonical_state"].get("schema_version")),
        "source_shas": data["source_shas"],
        "issue": data["issue"],
        "pr": pr,
        "checks": sorted(data["checks"], key=lambda item: _canonical_json(item)),
        "workflow_run": data["workflow_run"],
        "markers": data["markers"],
        "review": data["review"],
        "auto_merge": data["auto_merge"],
        "classification": classification,
        "quarantine": quarantine,
        "findings": findings,
        "blockers": blockers,
        "missing_evidence": [item for item in blockers if item.startswith("Missing required evidence")],
        "next_action": next_action,
        "stop_conditions": [
            "Stop if the current PR head differs from the packet evidence.",
            "Stop if required GitHub evidence is inaccessible, stale or contradictory.",
            "Stop if unsafe or private material is present.",
        ],
        "prohibited_actions": [
            "No issue, PR, review, approval, merge or closeout mutation is permitted.",
            "No repository write, release, spending, credential or policy change is permitted.",
            "No Phase 4K-9 work or Phase 4I resumption is permitted.",
        ],
        "evidence_classification": "public_safe",
        "derived_status": "no authority",
    }


def _list_lines(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] if values else ["- None observed."]


def _render_packet_payload(packet: dict[str, Any]) -> str:
    source = packet["source_shas"]
    issue = packet["issue"]
    pr = packet["pr"]
    run = packet["workflow_run"]
    markers = packet["markers"]
    review = packet["review"]
    lines = [
        "# RED_TEAM_STARTUP_PACKET",
        "",
        "## Derived Evidence Notice",
        "",
        "This packet is derived evidence, provides no authority, and must be revalidated against live sources.",
        "It provides no write authorization and cannot approve, merge, release or close an issue.",
        "",
        "## Generator",
        "",
        f"- Generator version: {packet['generator_version']}",
        f"- Packet schema version: {packet['schema_version']}",
        f"- Observation timestamp: {packet['observed_at']}",
        f"- Repository: {packet['repository']}",
        f"- Canonical schema version: {packet['canonical_schema_version']}",
        "",
        "## Source SHAs",
        "",
        f"- Local HEAD: {source.get('local_head')}",
        f"- Local main: {source.get('local_main')}",
        f"- Local origin/main: {source.get('local_origin_main')}",
        f"- Live default branch: {source.get('live_default_branch')}",
        f"- Canonical source ref: {source.get('canonical_ref')}",
        "",
        "## Lifecycle Evidence",
        "",
        f"- Issue: #{issue.get('number')} {issue.get('state')} ({issue.get('url')})",
        f"- Issue closeout: {issue.get('closeout_state')}",
        f"- PR: #{pr.get('number')} {pr.get('state')} ({pr.get('url')})",
        f"- PR base: {pr.get('base')}",
        f"- PR head branch: {pr.get('head_branch')}",
        f"- PR head: {pr.get('head')}",
        f"- PR draft: {str(bool(pr.get('draft'))).lower()}",
        f"- PR author: {pr.get('author_login')} ({pr.get('author_type')})",  # scope-bound approval evidence
        f"- Merge commit: {pr.get('merge_commit')}",
        f"- Workflow: {run.get('name')} ({run.get('workflow_id')})",
        f"- Workflow event: {run.get('event')}",
        f"- Workflow run: {run.get('id')} {run.get('status')} / {run.get('conclusion')}",
        f"- Workflow head: {run.get('head_sha')} on {run.get('head_branch')}",
        "",
        "## Review And Control Evidence",
        "",
        f"- Owner-trigger marker: {markers.get('owner_trigger_status')}",
        f"- Red-team marker: {markers.get('red_team_status')}",
        f"- Red-team bound SHA: {markers.get('red_team_bound_sha')}",
        f"- Review decision: {review.get('decision')}",
        f"- Approval evidence status: {review.get('evidence_status')}",
        f"- Normalized review records: {len(review.get('review_records') or [])}",
        f"- Permission records: {len(review.get('permission_records') or [])}",
        f"- Qualifying human approvals: {len(review.get('qualifying_approvals') or [])}",
        f"- Disqualified approval candidates: {len(review.get('disqualified_approvals') or [])}",
        f"- Auto-merge active: {str(bool(packet['auto_merge'].get('active'))).lower()}",
        "",
        "## Required Checks",
        "",
        *(
            [
                f"- {check.get('name')}: {check.get('state')} / {check.get('bucket')} ({check.get('link')})"
                for check in packet["checks"]
            ]
            or ["- None observed."]
        ),
        "",
        "## Classification",
        "",
        f"- Consistency classification: {packet['classification']}",
        f"- Quarantine: {str(packet['quarantine']).lower()}",
        "",
        "## Comparison Findings",
        "",
        *_list_lines(packet["findings"]),
        "",
        "## Blockers And Evidence Gaps",
        "",
        *_list_lines(packet["blockers"]),
        "",
        "## Single Next Required Action",
        "",
        packet["next_action"],
        "",
        "## Stop Conditions",
        "",
        *_list_lines(packet["stop_conditions"]),
        "",
        "## Prohibited Actions",
        "",
        *_list_lines(packet["prohibited_actions"]),
        "",
        "## Public Private Classification",
        "",
        f"- Evidence classification: {packet['evidence_classification']}",
        "- Unsafe or private-looking evidence provides no authority and is rejected.",
        "",
    ]
    return "\n".join(line.rstrip() for line in lines).rstrip() + "\n"


def recompute_packet_hash(markdown: str) -> str:
    stripped = re.sub(r"\n\n## Packet Hash\n\n`[0-9a-f]{64}`\n$", "\n", markdown)
    return hashlib.sha256(stripped.encode("utf-8")).hexdigest()


def _render_packet(packet: dict[str, Any]) -> tuple[str, str]:
    payload = _render_packet_payload(packet)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    rendered = payload.rstrip("\n") + f"\n\n## Packet Hash\n\n`{digest}`\n"
    return rendered, digest


def _validate_output_dir(output_dir: Path, repo_root: Path) -> Path:
    repo = repo_root.resolve(strict=True)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        resolved = output_dir.resolve(strict=True)
    except OSError as exc:
        raise UnsafeEvidenceError("prohibited output path is inaccessible") from exc
    if resolved == repo or repo in resolved.parents:
        raise UnsafeEvidenceError("prohibited output path resolves inside the repository")
    for name in OUTPUT_NAMES:
        target = resolved / name
        if target.is_symlink():
            raise UnsafeEvidenceError("prohibited output-file symlink rejected")
        if target.exists():
            try:
                target_resolved = target.resolve(strict=True)
            except OSError as exc:
                raise UnsafeEvidenceError("prohibited output target is inaccessible") from exc
            if target_resolved == repo or repo in target_resolved.parents:
                raise UnsafeEvidenceError("prohibited output target resolves inside repository")
    return resolved


def _atomic_write(path: Path, content: str) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def generate(data: dict[str, Any], observed_at: str, output_dir: Path, repo_root: Path = ROOT) -> tuple[int, dict[str, Any], str]:
    _parse_rfc3339(observed_at)
    _reject_unsafe(data)
    _validate_input(data)
    approval = _approval_evaluation(data["pr"], data["review"])
    data = dict(data)
    data["review"] = approval["review"]
    destination = _validate_output_dir(output_dir, repo_root)
    classification, findings, blockers, quarantine = _compare(data, approval)
    packet = _packet_data(data, observed_at, classification, findings, blockers, quarantine)
    markdown, packet_hash = _render_packet(packet)
    if recompute_packet_hash(markdown) != packet_hash:
        raise CollectorError("packet hash recomputation failed")
    evidence = {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "observed_at": observed_at,
        "repository": data["repository"],
        "source_shas": data["source_shas"],
        "source_commands": data.get("source_commands", []),
        "canonical_state": data["canonical_state"],
        "live_state": {
            "issue": data["issue"],
            "pr": data["pr"],
            "checks": packet["checks"],
            "workflow_run": data["workflow_run"],
            "markers": data["markers"],
            "review": data["review"],
            "auto_merge": data["auto_merge"],
        },
        "comparison_findings": findings,
        "blockers": blockers,
        "missing_evidence": packet["missing_evidence"],
        "consistency_classification": classification,
        "quarantine": quarantine,
        "public_private_classification": "public_safe",
        "packet_hash": packet_hash,
        "packet_hash_rule": PACKET_HASH_RULE,
        "startup_packet": packet,
    }
    _reject_unsafe(evidence)
    json_text = json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    _atomic_write(destination / OUTPUT_NAMES[0], json_text)
    _atomic_write(destination / OUTPUT_NAMES[1], markdown)
    return EXIT_BY_CLASSIFICATION[classification], evidence, markdown


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    fixture = sub.add_parser("fixture")
    fixture.add_argument("--fixture", required=True, type=Path)
    fixture.add_argument("--observed-at", required=True)
    fixture.add_argument("--output-dir", required=True, type=Path)
    live = sub.add_parser("live")
    live.add_argument("--repo-root", required=True)
    live.add_argument("--repository", required=True)
    live.add_argument("--issue-number", required=True, type=int)
    live.add_argument("--pr-number", required=True, type=int)
    live.add_argument("--run-id", required=True, type=int)
    live.add_argument("--canonical-ref", required=True)
    live.add_argument("--observed-at", required=True)
    live.add_argument("--output-dir", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        if args.mode == "fixture":
            data = _load_fixture(args.fixture)
            code, evidence, _ = generate(data, args.observed_at, args.output_dir, ROOT)
        else:
            data = _collect_live(args)
            code, evidence, _ = generate(data, args.observed_at, args.output_dir, Path(args.repo_root))
        print(
            json.dumps(
                {
                    "classification": evidence["consistency_classification"],
                    "exit_code": code,
                    "packet_hash": evidence["packet_hash"],
                    "output_directory": str(Path(args.output_dir).resolve()),
                },
                sort_keys=True,
            )
        )
        return code
    except CollectorError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return exc.exit_code
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: invalid or inaccessible input: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
