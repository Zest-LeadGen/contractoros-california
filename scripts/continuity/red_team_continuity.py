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

try:
    from scripts.continuity import role_contract
except ModuleNotFoundError:  # direct script execution from scripts/continuity
    import role_contract  # type: ignore[no-redef]

GENERATOR_VERSION = "1.4.0"
EVIDENCE_SCHEMA_VERSION = "1.4.0"
PACKET_SCHEMA_VERSION = "1.4.0"
FIXTURE_VERSION = "1.4.0"
REPOSITORY_GRAPHQL_QUERY = (
    'query { repository(owner: "Zest-LeadGen", name: "contractoros-california") '
    "{ nameWithOwner defaultBranchRef { name target { oid } } } }"
)
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
FIXED_LIVE_READS = 14
MAX_LEGAL_SOURCE_COMMANDS = (
    FIXED_LIVE_READS + MAX_REVIEW_PAGES + MAX_PERMISSION_CANDIDATES
)
MAX_CHECKS = 100
MAX_WORKFLOW_JOBS = 25
MAX_WORKFLOW_STEPS = 100
MAX_SOURCE_COMMANDS = MAX_LEGAL_SOURCE_COMMANDS
MAX_COMMAND_ARGV = 32
REVIEW_STATES = {"APPROVED", "CHANGES_REQUESTED", "DISMISSED", "COMMENTED", "PENDING"}
DECISIVE_REVIEW_STATES = {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}
REVIEW_DECISIONS = {"APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"}
PERMISSION_VALUES = {"admin", "write", "read", "none", "triage"}
ACCOUNT_TYPES = {"User", "Bot"}
MAX_ROLE_NAME_LENGTH = 100
MAX_AUTHOR_ASSOCIATION_LENGTH = 100  # scope-bound approval evidence
MAX_DISQUALIFICATION_REASONS = 100
MAX_DISQUALIFICATION_REASON_LENGTH = 100
DISQUALIFICATION_REASONS = {
    "APPROVAL_REVIEW_RECORD_MALFORMED",
    "APPROVAL_STALE_HEAD",
    "APPROVAL_SUPERSEDED_BY_CHANGES_REQUESTED",
    "APPROVAL_DISMISSED",
    "APPROVAL_NOT_SUBMITTED",
    "APPROVAL_BOT_ACCOUNT",
    "APPROVAL_PR_AUTHOR",  # scope-bound approval evidence
    "APPROVAL_PERMISSION_EVIDENCE_MISSING",
    "APPROVAL_PERMISSION_IDENTITY_MISMATCH",
    "APPROVAL_PERMISSION_READ_ONLY",
    "APPROVAL_PERMISSION_NONE",
    "APPROVAL_PERMISSION_UNKNOWN",
}
EVIDENCE_WIDE_DISQUALIFICATION_REASONS = {"APPROVAL_REVIEW_RECORD_MALFORMED"}
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


class EvidenceUnavailableError(CollectorError):
    exit_code = 3


class ApprovalEvidenceUnavailableError(EvidenceUnavailableError):
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


def _is_rfc3339(value: Any) -> bool:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        return False
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _parse_rfc3339_instant(value: str) -> dt.datetime:
    if not _is_rfc3339(value):
        raise CollectorError("review submission timestamp is malformed")
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(dt.timezone.utc)


def _canonical_login(value: Any, error: type[CollectorError] = CollectorError) -> str:  # scope-bound approval evidence
    if not isinstance(value, str) or not GITHUB_LOGIN_RE.fullmatch(value):  # scope-bound approval evidence
        raise error("reviewer login evidence is malformed")  # scope-bound approval evidence
    return value.casefold()


def _normalized_worktree_status(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, str):
        raise EvidenceUnavailableError("worktree status evidence is unavailable")
    lines = raw.splitlines()
    if not lines or not lines[0].startswith("## "):
        raise EvidenceUnavailableError("worktree status branch evidence is malformed")
    entries = [line for line in lines[1:] if line]
    normalized = "\n".join([lines[0], *entries])
    return {
        "clean": not entries,
        "sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
    }


def _require_clean_unchanged_worktree(
    before: dict[str, Any],
    after: dict[str, Any] | None = None,
    before_head: str | None = None,
    after_head: str | None = None,
) -> None:
    if not before["clean"]:
        raise EvidenceUnavailableError("worktree is not clean before authoritative collection")  # scope-bound provenance evidence
    if (after is None) != (after_head is None):
        raise EvidenceUnavailableError("worktree provenance evidence is incomplete")
    if after is None:
        return
    if not after["clean"]:
        raise EvidenceUnavailableError("worktree is not clean after authoritative collection")  # scope-bound provenance evidence
    if before["sha256"] != after["sha256"]:
        raise EvidenceUnavailableError("worktree status changed during authoritative collection")  # scope-bound provenance evidence
    if not _is_sha(before_head) or not _is_sha(after_head):
        raise EvidenceUnavailableError("worktree HEAD provenance evidence is malformed")
    if before_head != after_head:
        raise EvidenceUnavailableError("worktree HEAD changed during authoritative collection")  # scope-bound provenance evidence


def _require_review_timestamp(value: Any, state: str, error: type[CollectorError]) -> None:
    if value is not None and not _is_rfc3339(value):
        raise error("review submission timestamp is malformed")
    if state in DECISIVE_REVIEW_STATES and value is None:
        raise error("decisive review submission timestamp is missing")


def _valid_conclusion(value: Any, status: Any) -> bool:
    if value is None:
        return isinstance(status, str) and status.lower() != "completed"
    return _nonempty_string(value)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _reject_unsafe(value: Any) -> None:
    text = _canonical_json(value)
    for pattern in FORBIDDEN_PRIVATE_PATTERNS:
        if pattern.search(text):
            raise UnsafeEvidenceError("unsafe or private-looking evidence rejected")


SUPPORTED_AUTHORITY_BINDINGS = {  # scope-bound
    (49, 50): "GITHUB_ISSUE_49",
    (55, 56): "GITHUB_ISSUE_55",
}


def _derive_authority_source(issue_number: Any, pr_number: Any) -> str:  # scope
    """Return the single authorized Issue/PR authority binding or fail closed in scope."""
    if type(issue_number) is not int or type(pr_number) is not int:
        raise CollectorError("authority scope context is missing or malformed")
    try:
        return SUPPORTED_AUTHORITY_BINDINGS[(issue_number, pr_number)]  # scope-bound
    except KeyError as exc:
        raise CollectorError("authority scope context is unsupported or contradictory") from exc


def _review_page_argv(page: int, pr_number: int = 50) -> tuple[str, ...]:
    return (
        "gh",
        "api",
        "--method",
        "GET",
        f"repos/{EXPECTED_REPOSITORY}/pulls/{pr_number}/reviews"
        f"?per_page={REVIEW_PAGE_SIZE}&page={page}",
    )


def _live_command_firewall(args: argparse.Namespace) -> set[tuple[str, ...]]:
    """Return the only fixed command shapes a live invocation may execute."""
    fixed_commands = {
        ("git", "status", "--porcelain=v1", "--branch", "--untracked-files=all"),
        ("git", "remote", "get-url", "origin"),
        ("git", "rev-parse", "HEAD"),
        ("git", "rev-parse", "main"),
        ("git", "rev-parse", "origin/main"),
        ("git", "rev-parse", "--show-toplevel"),
        ("git", "show", f"{args.canonical_ref}:{CANONICAL_PATH}"),
        ("gh", "api", "graphql", "-f", f"query={REPOSITORY_GRAPHQL_QUERY}"),
        ("gh", "issue", "view", str(args.issue_number), "--repo", args.repository, "--json", "number,state,stateReason,url,closedAt,title"),
        ("gh", "pr", "view", str(args.pr_number), "--repo", args.repository, "--json", "number,state,baseRefName,headRefName,headRefOid,isDraft,mergeCommit,mergedAt,url,autoMergeRequest,reviewDecision,author,body"),  # scope-bound approval evidence
        ("gh", "pr", "checks", str(args.pr_number), "--repo", args.repository, "--json", "name,state,bucket,link"),
        ("gh", "run", "view", str(args.run_id), "--repo", args.repository, "--json", "databaseId,name,workflowDatabaseId,event,status,conclusion,headSha,headBranch,url,jobs"),
    }
    return fixed_commands | {
        _review_page_argv(page, args.pr_number) for page in range(1, MAX_REVIEW_PAGES + 1)
    }


def _validate_command(
    argv: list[str],
    allowed_permission_logins: set[str] | None = None,  # scope-bound approval evidence
    allowed_commands: set[tuple[str, ...]] | None = None,
) -> None:
    """Reject every command shape not included in the positive read-only allowlist."""
    if not argv or argv[0] not in {"git", "gh"}:
        raise CommandRejectedError("unknown executable rejected by command allowlist")
    if allowed_commands is not None:
        if tuple(argv) not in allowed_commands:
            raise CommandRejectedError("command does not match this live invocation's exact allowlist")
        return

    if argv[0] == "git":
        allowed = {
            ("git", "remote", "get-url", "origin"),
            ("git", "rev-parse", "HEAD"),
            ("git", "rev-parse", "main"),
            ("git", "rev-parse", "origin/main"),
            ("git", "rev-parse", "--show-toplevel"),
            ("git", "status", "--porcelain=v1", "--branch", "--untracked-files=all"),
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
            r"repos/Zest-LeadGen/contractoros-california/pulls/(?:50|56)/reviews\?per_page=100&page=([1-5])",
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

    if argv == ["gh", "api", "graphql", "-f", f"query={REPOSITORY_GRAPHQL_QUERY}"]:
        return

    # Every other gh api shape and every GitHub mutation are forbidden.
    allowed_prefixes = {
        ("gh", "issue", "view"),
        ("gh", "pr", "view"),
        ("gh", "pr", "checks"),
        ("gh", "run", "view"),
    }
    if len(argv) < 3 or tuple(argv[:3]) not in allowed_prefixes:
        raise CommandRejectedError("forbidden or unknown GitHub command rejected by command allowlist")
    if any(arg in {"--comments", "--jq", "--log", "--template", "--watch", "--web"} for arg in argv):
        raise CommandRejectedError("unknown GitHub output flag rejected by command allowlist")
    if argv.count("--repo") != 1 or argv.count("--json") != 1:
        raise CommandRejectedError("GitHub command shape rejected by command allowlist")


def _run_read_command(
    argv: list[str],
    cwd: Path,
    timeout: int = 20,
    allowed_permission_logins: set[str] | None = None,  # scope-bound approval evidence
    allowed_commands: set[tuple[str, ...]] | None = None,
) -> tuple[str, dict[str, Any]]:
    _validate_command(argv, allowed_permission_logins, allowed_commands)  # scope-bound approval evidence
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
        raise EvidenceUnavailableError(f"required read command inaccessible: {argv[:3]}") from exc
    if len(proc.stdout.encode("utf-8")) > MAX_COMMAND_OUTPUT_BYTES:
        raise EvidenceUnavailableError("required read command output exceeds the bounded size limit")
    if len(proc.stderr.encode("utf-8")) > MAX_COMMAND_OUTPUT_BYTES:
        raise EvidenceUnavailableError("required read command error output exceeds the bounded size limit")
    result = {
        "argv": argv,
        "return_code": int(proc.returncode),
        "stdout_sha256": hashlib.sha256(proc.stdout.encode("utf-8")).hexdigest(),
        "stderr_present": bool(proc.stderr.strip()),
    }
    if proc.returncode != 0:
        raise EvidenceUnavailableError(f"required read command failed: {argv[:3]}")
    return proc.stdout, result


def _json_command(
    argv: list[str],
    cwd: Path,
    commands: list[dict[str, Any]],
    allowed_permission_logins: set[str] | None = None,  # scope-bound approval evidence
    allowed_commands: set[tuple[str, ...]] | None = None,
) -> Any:
    output, result = _run_read_command(argv, cwd, allowed_permission_logins=allowed_permission_logins, allowed_commands=allowed_commands)  # scope-bound approval evidence
    commands.append(result)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise EvidenceUnavailableError("read command returned malformed JSON") from exc


def _normalize_origin(remote: str) -> dict[str, Any]:
    """Return only public-safe normalized GitHub identity evidence."""
    value = str(remote or "").strip()
    if not value:
        raise EvidenceUnavailableError("origin remote evidence is empty")
    if re.search(r"(?i)^https?://[^/@:]+:[^/@]+@", value):
        raise UnsafeEvidenceError("origin remote contains embedded credentials")

    transport = "unsupported"
    owner_repo: str | None = None
    if re.fullmatch(r"https://github\.com/[^/?#]+/[^/?#]+(?:\.git)?", value, re.I):
        transport = "https"
        owner_repo = re.sub(r"^https://github\.com/", "", value, flags=re.I)
    elif re.fullmatch(r"git@github\.com:[^/:?#]+/[^/:?#]+\.git", value, re.I):
        transport = "ssh"
        owner_repo = re.sub(r"^git@github\.com:", "", value, flags=re.I)
    elif re.fullmatch(r"ssh://git@github\.com/[^/?#]+/[^/?#]+\.git", value, re.I):
        transport = "ssh"
        owner_repo = re.sub(r"^ssh://git@github\.com/", "", value, flags=re.I)
    if owner_repo:
        owner_repo = re.sub(r"\.git$", "", owner_repo, flags=re.I)
    verified = bool(owner_repo and owner_repo.casefold() == EXPECTED_REPOSITORY.casefold())
    return {
        "remote_name": EXPECTED_REPOSITORY if verified else "unverified",
        "remote_transport": transport,
        "remote_verified": verified,
        "remote_identifier": EXPECTED_REPOSITORY if verified else "unverified",
    }


def _git_control_present(repo_root: Path) -> bool:
    control = repo_root / ".git"
    if control.is_dir():
        return True
    if not control.is_file() or control.is_symlink():
        return False
    try:
        line = control.read_text(encoding="utf-8").strip()
        if not line.startswith("gitdir: "):
            return False
        target = Path(line[8:])
        if not target.is_absolute():
            target = repo_root / target
        return target.resolve(strict=True).is_dir()
    except (OSError, UnicodeError):
        return False


def _require_live_fields(value: Any, fields: tuple[str, ...], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(field not in value for field in fields):
        raise EvidenceUnavailableError(f"required {label} live fields are unavailable")
    return value


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
    if not isinstance(raw, list) or len(raw) > MAX_CHECKS:
        raise EvidenceUnavailableError("required pull-request check evidence is malformed or exceeds its bound")
    checks = []
    for item in raw:
        if not isinstance(item, dict):
            raise EvidenceUnavailableError("required pull-request check item is malformed")
        if any(not isinstance(item.get(key), str) for key in ("name", "state", "bucket", "link")):
            raise EvidenceUnavailableError("required pull-request check fields are malformed")
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
    if not isinstance(raw, list) or len(raw) > MAX_WORKFLOW_JOBS:
        raise EvidenceUnavailableError("required workflow job evidence is malformed or exceeds its bound")
    jobs = []
    for job in raw:
        if not isinstance(job, dict):
            raise EvidenceUnavailableError("required workflow job item is malformed")
        raw_steps = job.get("steps")
        if not isinstance(raw_steps, list) or len(raw_steps) > MAX_WORKFLOW_STEPS:
            raise EvidenceUnavailableError("required workflow step evidence is malformed or exceeds its bound")
        steps = []
        for step in raw_steps:
            if not isinstance(step, dict):
                raise EvidenceUnavailableError("required workflow step item is malformed")
            if (
                not isinstance(step.get("name"), str)
                or type(step.get("number")) is not int
                or step["number"] < 1
                or not isinstance(step.get("status"), str)
                or "conclusion" not in step
                or not _valid_conclusion(step["conclusion"], step["status"])
            ):
                raise EvidenceUnavailableError("required workflow step fields are malformed")
            steps.append(
                {
                    "name": step["name"],
                    "number": step["number"],
                    "status": step["status"],
                    "conclusion": step.get("conclusion"),
                }
            )
        if (
            not isinstance(job.get("name"), str)
            or not isinstance(job.get("status"), str)
            or "conclusion" not in job
            or not _valid_conclusion(job["conclusion"], job["status"])
        ):
            raise EvidenceUnavailableError("required workflow job fields are malformed")
        jobs.append(
            {
                "name": job["name"],
                "status": job["status"],
                "conclusion": job.get("conclusion"),
                "steps": sorted(steps, key=lambda item: (item["number"], item["name"])),
            }
        )
    return sorted(jobs, key=lambda item: (item["name"], _canonical_json(item)))


def _normalized_review_record(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ApprovalEvidenceUnavailableError("review approval evidence record is malformed")
    user = raw.get("user") or {}
    if not isinstance(user, dict):
        raise ApprovalEvidenceUnavailableError("review approval user evidence is malformed")
    state = raw.get("state")
    if not isinstance(state, str):
        raise ApprovalEvidenceUnavailableError("review approval state evidence is malformed")
    state = state.upper()
    submitted_at = raw.get("submitted_at")
    _require_review_timestamp(submitted_at, state, ApprovalEvidenceUnavailableError)
    try:
        reviewer_login = _canonical_login(user.get("login"), ApprovalEvidenceUnavailableError)  # scope-bound approval evidence
    except CollectorError as exc:
        raise ApprovalEvidenceUnavailableError("review approval login evidence is malformed") from exc  # scope-bound approval evidence
    if not _positive_integer(raw.get("id")) or user.get("type") not in ACCOUNT_TYPES:
        raise ApprovalEvidenceUnavailableError("review approval identity evidence is malformed")
    if state not in REVIEW_STATES or not _is_sha(raw.get("commit_id")):
        raise ApprovalEvidenceUnavailableError("review approval binding evidence is malformed")
    association = raw.get("author_association")  # scope-bound approval evidence
    if not isinstance(association, str) or len(association) > MAX_AUTHOR_ASSOCIATION_LENGTH:  # scope-bound approval evidence
        raise ApprovalEvidenceUnavailableError("review approval association evidence is malformed")
    return {
        "review_id": raw.get("id"),
        "reviewer_login": reviewer_login,  # scope-bound approval evidence
        "reviewer_type": user.get("type"),
        "state": state,
        "submitted_at": submitted_at,
        "commit_id": raw.get("commit_id"),
        "author_association": association,  # scope-bound approval evidence
    }


def _review_sort_key(record: dict[str, Any]) -> tuple[dt.datetime, int, str]:
    submitted_at = record.get("submitted_at")
    return (
        _parse_rfc3339_instant(submitted_at) if isinstance(submitted_at, str) else dt.datetime.min.replace(tzinfo=dt.timezone.utc),
        int(record.get("review_id") or 0) if isinstance(record.get("review_id"), int) else 0,
        _canonical_json(record),
    )


def _approval_evaluation(pr: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    """Recompute qualifying approvals from normalized, public-safe evidence."""
    blocked: list[str] = []
    quarantined: list[str] = []
    collected_keys = {"decision", "evidence_status", "review_records", "permission_records"}
    final_keys = collected_keys | {
        "qualifying_approvals", "disqualified_approvals", "disqualification_reasons",
    }
    has_claims = set(review) == final_keys
    if set(review) == collected_keys:
        _validate_collected_review_evidence(review)
    elif has_claims:
        _validate_review_evidence(review)
    else:
        raise CollectorError("collected approval evidence has an invalid contract shape")
    status = review["evidence_status"]
    records = review.get("review_records")
    permissions = review.get("permission_records")
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
            raise CollectorError("approval review record is malformed")
        record = {
            "review_id": raw["review_id"],
            "reviewer_login": _canonical_login(raw["reviewer_login"]),  # scope-bound approval evidence
            "reviewer_type": raw["reviewer_type"],
            "state": raw["state"],
            "submitted_at": raw["submitted_at"],
            "commit_id": raw["commit_id"],
            "author_association": raw["author_association"],  # scope-bound approval evidence
        }
        review_id = record["review_id"]
        login = record["reviewer_login"]  # scope-bound approval evidence
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
            raise CollectorError("permission approval record is malformed")
        item = {
            "reviewer_login": _canonical_login(raw["reviewer_login"]),  # scope-bound approval evidence
            "permission": raw["permission"],
            "role_name": raw["role_name"],
            "account_type": raw["account_type"],
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
    ambiguous_logins = {  # scope-bound approval evidence
        record["reviewer_login"] for record in normalized_records if record.get("review_id") in duplicate_ids  # scope-bound approval evidence
    }
    reviewer_logins = sorted({r["reviewer_login"] for r in normalized_records if r["reviewer_login"]})  # scope-bound approval evidence
    unresolved_changes_requested = False
    for login in reviewer_logins:  # scope-bound approval evidence
        reviewer_records = [r for r in normalized_records if r["reviewer_login"] == login]  # scope-bound approval evidence
        approvals = [r for r in reviewer_records if r["state"] == "APPROVED"]
        if login in ambiguous_logins:  # scope-bound approval evidence
            continue
        current_decisive = [
            r
            for r in reviewer_records
            if r["commit_id"] == pr.get("head")
            and r["state"] in DECISIVE_REVIEW_STATES
            and r.get("submitted_at")
        ]
        latest = max(current_decisive, key=_review_sort_key) if current_decisive else None
        if latest and latest["state"] == "CHANGES_REQUESTED":
            unresolved_changes_requested = True
            if approvals:
                disqualify(login, "APPROVAL_SUPERSEDED_BY_CHANGES_REQUESTED")  # scope-bound approval evidence
            continue
        if not approvals:
            continue
        if latest is None or latest["state"] != "APPROVED":
            if any(r["commit_id"] != pr.get("head") for r in approvals):
                disqualify(login, "APPROVAL_STALE_HEAD")  # scope-bound approval evidence
            if latest and latest["state"] == "DISMISSED":
                disqualify(login, "APPROVAL_DISMISSED")  # scope-bound approval evidence
            if any(not r.get("submitted_at") for r in approvals):
                disqualify(login, "APPROVAL_NOT_SUBMITTED")  # scope-bound approval evidence
            continue
        if latest["reviewer_type"] != "User":
            disqualify(login, "APPROVAL_BOT_ACCOUNT")  # scope-bound approval evidence
            continue
        if login == _canonical_login(pr["author_login"]):  # scope-bound approval evidence
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
    if unresolved_changes_requested:
        quarantined.append("Unresolved current-head changes requested remain adverse")
    if str(review.get("decision") or "").upper() == "APPROVED" and not qualifying:
        quarantined.append("Review decision claims approval without a qualifying current-head approver")
    if str(review.get("decision") or "").upper() == "CHANGES_REQUESTED":
        quarantined.append("Aggregate review decision is changes requested")
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
    _validate_review_evidence(result)
    if has_claims:
        claimed_qualifying = sorted(_canonical_login(login) for login in review["qualifying_approvals"])
        claimed_disqualified = sorted(_canonical_login(login) for login in review["disqualified_approvals"])
        claimed_reasons = {
            key: sorted(values)
            for key, values in sorted(_canonical_reason_map(review["disqualification_reasons"]).items())
        }
        if claimed_qualifying != result["qualifying_approvals"]:
            quarantined.append("Claimed qualifying approvals contradict computed approval evidence")
        if claimed_disqualified != result["disqualified_approvals"]:
            quarantined.append("Claimed disqualified approvals contradict computed approval evidence")
        if claimed_reasons != result["disqualification_reasons"]:
            quarantined.append("Claimed disqualification reasons contradict computed approval evidence")
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
    allowed_commands: set[tuple[str, ...]] | None = None,
    pr_number: int = 50,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    evidence_status = "complete"
    for page in range(1, MAX_REVIEW_PAGES + 1):
        review_argv = list(_review_page_argv(page, pr_number))
        raw_page = _json_command(
            review_argv,
            repo_root,
            commands,
            allowed_commands=allowed_commands,
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
        canonical_author = _canonical_login(pr_author_login, ApprovalEvidenceUnavailableError)  # scope-bound approval evidence
        candidates = sorted(
            {
                _canonical_login(record["reviewer_login"], ApprovalEvidenceUnavailableError)  # scope-bound approval evidence
                for record in records
                if record["state"] == "APPROVED"
                and record["commit_id"] == pr_head
                and record.get("submitted_at")
                and record["reviewer_type"] == "User"
                and _canonical_login(record["reviewer_login"], ApprovalEvidenceUnavailableError) != canonical_author  # scope-bound approval evidence
                and GITHUB_LOGIN_RE.fullmatch(record["reviewer_login"])  # scope-bound approval evidence
            }
        )
        if len(candidates) > MAX_PERMISSION_CANDIDATES:
            raise ApprovalEvidenceUnavailableError("permission approval candidates exceed the bounded limit")
        allowed = set(candidates)
        for login in candidates:  # scope-bound approval evidence
            permission_argv = [
                "gh", "api", "--method", "GET",
                f"repos/{EXPECTED_REPOSITORY}/collaborators/{login}/permission",  # scope-bound approval evidence
            ]
            if allowed_commands is not None:
                allowed_commands.add(tuple(permission_argv))
            try:
                permission = _json_command(
                    permission_argv,
                    repo_root,
                    commands,
                    allowed_permission_logins=allowed,  # scope-bound approval evidence
                    allowed_commands=allowed_commands,
                )
            except EvidenceUnavailableError as exc:
                raise ApprovalEvidenceUnavailableError(
                    f"permission approval evidence is inaccessible for reviewer: {login}"  # scope-bound approval evidence
                ) from exc
            response_login, permission_value, role_name, account_type = _validate_permission_response(permission, login)  # scope-bound approval evidence
            permission_records.append(
                {
                    "reviewer_login": response_login,  # scope-bound approval evidence
                    "permission": permission_value,
                    "role_name": role_name,
                    "account_type": account_type,
                }
            )
    return {
        "evidence_status": evidence_status,
        "review_records": records,
        "permission_records": permission_records,
    }


def _validate_permission_response(permission: Any, login: str) -> tuple[str, str, str, str]:  # scope-bound approval evidence
    if not isinstance(permission, dict):
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence is malformed for reviewer: {login}"  # scope-bound approval evidence
        )
    permission_value = permission.get("permission")
    if not isinstance(permission_value, str) or permission_value not in PERMISSION_VALUES:
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence is missing permission for reviewer: {login}"  # scope-bound approval evidence
        )
    if (
        "role_name" not in permission
        or not _nonempty_string(permission.get("role_name"))
        or len(permission["role_name"]) > MAX_ROLE_NAME_LENGTH
    ):
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence is missing role name for reviewer: {login}"  # scope-bound approval evidence
        )
    user = permission.get("user")
    if not isinstance(user, dict):
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence is missing user for reviewer: {login}"  # scope-bound approval evidence
        )
    account_type = user.get("type")
    if account_type not in ACCOUNT_TYPES:
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence has unsupported user type for reviewer: {login}"  # scope-bound approval evidence
        )
    try:
        response_login = _canonical_login(user.get("login"), ApprovalEvidenceUnavailableError)  # scope-bound approval evidence
        candidate_login = _canonical_login(login, ApprovalEvidenceUnavailableError)  # scope-bound approval evidence
    except CollectorError as exc:
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence has malformed response identity for reviewer: {login}"  # scope-bound approval evidence
        ) from exc
    if response_login != candidate_login:  # scope-bound approval evidence
        raise ApprovalEvidenceUnavailableError(
            f"permission approval evidence identity differs for reviewer: {login}"  # scope-bound approval evidence
        )
    return response_login, permission_value, permission["role_name"], account_type  # scope-bound approval evidence


def _validate_live_repository(repo: Any, permitted_repository: str) -> tuple[str, str, str]:
    if not isinstance(repo, dict):
        raise EvidenceUnavailableError("required repository fields are unavailable")
    name = repo.get("nameWithOwner")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name):
        raise EvidenceUnavailableError("primary live GitHub repository name is unavailable or invalid")
    default_ref = repo.get("defaultBranchRef")
    if not isinstance(default_ref, dict):
        raise EvidenceUnavailableError("primary live GitHub default branch is unavailable or invalid")
    default_name = default_ref.get("name")
    if not isinstance(default_name, str) or not default_name.strip():
        raise EvidenceUnavailableError("primary live GitHub default branch name is unavailable or invalid")
    target = default_ref.get("target")
    if not isinstance(target, dict):
        raise EvidenceUnavailableError("primary live GitHub default branch target is unavailable or invalid")
    target_oid = target.get("oid")
    if not _is_sha(target_oid):
        raise EvidenceUnavailableError("primary live GitHub default branch target OID is unavailable or invalid")
    return name, default_name, target_oid


def _validate_live_issue(issue: Any) -> None:
    if (
        not isinstance(issue, dict)
        or not _positive_integer(issue.get("number"))
        or not _nonempty_string(issue.get("state"))
        or (issue.get("stateReason") is not None and not isinstance(issue.get("stateReason"), str))
        or not _nonempty_string(issue.get("url"))
        or (issue.get("closedAt") is not None and not _is_rfc3339(issue.get("closedAt")))
    ):
        raise EvidenceUnavailableError("required live issue evidence is malformed")
    state = str(issue["state"]).upper()
    closed_at = issue.get("closedAt")
    if state == "OPEN" and closed_at is not None:
        raise EvidenceUnavailableError("open live issue has contradictory closeout timestamp")
    if state == "CLOSED" and closed_at is None:
        raise EvidenceUnavailableError("closed live issue lacks required closeout timestamp")
    if state not in {"OPEN", "CLOSED"}:
        raise EvidenceUnavailableError("live issue state is unsupported")


def _validate_live_pr(pr: Any) -> None:
    if not isinstance(pr, dict):
        raise EvidenceUnavailableError("required live pull-request evidence is malformed")
    author = pr.get("author")  # scope-bound approval evidence
    merge_commit = pr.get("mergeCommit")
    if (
        not _positive_integer(pr.get("number"))
        or any(
            not _nonempty_string(pr.get(key))
            for key in ("state", "baseRefName", "headRefName", "headRefOid", "url")
        )
        or not _is_sha(pr.get("headRefOid"))
        or type(pr.get("isDraft")) is not bool
        or not isinstance(pr.get("body"), str)
        or not isinstance(author, dict)  # scope-bound approval evidence
        or not GITHUB_LOGIN_RE.fullmatch(author.get("login") if isinstance(author.get("login"), str) else "")  # scope-bound approval evidence
        or type(author.get("is_bot")) is not bool  # scope-bound approval evidence
        or (pr.get("mergedAt") is not None and not _is_rfc3339(pr.get("mergedAt")))
        or (pr.get("reviewDecision") is not None and not isinstance(pr.get("reviewDecision"), str))
        or (pr.get("autoMergeRequest") is not None and not isinstance(pr.get("autoMergeRequest"), dict))
        or (
            merge_commit is not None
            and (
                not isinstance(merge_commit, dict)
                or not _is_sha(merge_commit.get("oid"))
            )
        )
    ):
        raise EvidenceUnavailableError("required live pull-request evidence is malformed")


def _validate_live_run(run: Any) -> None:
    if (
        not isinstance(run, dict)
        or not _positive_integer(run.get("databaseId"))
        or not _positive_integer(run.get("workflowDatabaseId"))
        or any(
            not _nonempty_string(run.get(key))
            for key in ("name", "event", "status", "headSha", "headBranch", "url")
        )
        or not _is_sha(run.get("headSha"))
        or "conclusion" not in run
        or not _valid_conclusion(run["conclusion"], run.get("status"))
    ):
        raise EvidenceUnavailableError("required live workflow-run evidence is malformed")


def _collect_live(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve(strict=True)
    if not _is_sha(args.canonical_ref):
        raise CollectorError("canonical ref must be an exact 40-character lowercase SHA")
    if args.repository != EXPECTED_REPOSITORY:
        raise CollectorError("live approval collection is bounded to the ContractorOS repository")
    authority_source = _derive_authority_source(args.issue_number, args.pr_number)  # scope-bound

    commands: list[dict[str, Any]] = []
    allowed_commands = _live_command_firewall(args)

    def read(argv: list[str]) -> str:
        output, result = _run_read_command(argv, repo_root, allowed_commands=allowed_commands)
        commands.append(result)
        return output.strip()

    before_status = _normalized_worktree_status(
        read(["git", "status", "--porcelain=v1", "--branch", "--untracked-files=all"])
    )
    _require_clean_unchanged_worktree(before_status)
    remote = read(["git", "remote", "get-url", "origin"])
    remote_identity = _normalize_origin(remote)
    local_head = read(["git", "rev-parse", "HEAD"])
    worktree_head_before = local_head
    local_main = read(["git", "rev-parse", "main"])
    local_origin = read(["git", "rev-parse", "origin/main"])
    git_top_raw = read(["git", "rev-parse", "--show-toplevel"])
    try:
        git_top = Path(git_top_raw).resolve(strict=True)
    except OSError as exc:
        raise EvidenceUnavailableError("Git top-level evidence is inaccessible") from exc
    root_verified = git_top == repo_root and _git_control_present(repo_root)
    canonical_raw = read(["git", "show", f"{args.canonical_ref}:{CANONICAL_PATH}"])
    try:
        canonical = json.loads(canonical_raw)
    except json.JSONDecodeError as exc:
        raise CollectorError("canonical state is malformed") from exc

    repo_response = _json_command(
        ["gh", "api", "graphql", "-f", f"query={REPOSITORY_GRAPHQL_QUERY}"],
        repo_root,
        commands,
        allowed_commands=allowed_commands,
    )
    if not isinstance(repo_response, dict) or not isinstance(repo_response.get("data"), dict):
        raise EvidenceUnavailableError("required repository GraphQL response is unavailable")
    repo = repo_response["data"].get("repository")
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
        allowed_commands=allowed_commands,
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
        allowed_commands=allowed_commands,
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
        allowed_commands=allowed_commands,
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
        allowed_commands=allowed_commands,
    )

    repo = _require_live_fields(repo, ("nameWithOwner", "defaultBranchRef"), "repository")
    issue = _require_live_fields(issue, ("number", "state", "stateReason", "url", "closedAt"), "issue")
    pr = _require_live_fields(
        pr,
        ("number", "state", "baseRefName", "headRefName", "headRefOid", "isDraft", "mergeCommit", "mergedAt", "autoMergeRequest", "reviewDecision", "url", "author", "body"),  # scope-bound approval evidence
        "pull-request",
    )
    run = _require_live_fields(
        run,
        ("databaseId", "name", "workflowDatabaseId", "event", "status", "conclusion", "headSha", "headBranch", "jobs", "url"),
        "workflow-run",
    )
    if not isinstance(raw_checks, list):
        raise EvidenceUnavailableError("required pull-request check fields are unavailable")

    repository_name, default_branch_name, default_branch_oid = _validate_live_repository(
        repo, args.repository
    )
    _validate_live_issue(issue)
    _validate_live_pr(pr)
    _validate_live_run(run)
    if int(issue.get("number")) != args.issue_number or int(pr.get("number")) != args.pr_number:
        raise EvidenceUnavailableError("live issue or pull-request identity contradicts the requested authority scope")
    normalized_checks = _normalized_checks(raw_checks)
    normalized_jobs = _normalized_jobs(run.get("jobs"))
    pr_author = pr.get("author") or {}  # scope-bound approval evidence
    approval_evidence = _collect_review_evidence(
        repo_root,
        commands,
        str(pr.get("headRefOid") or ""),
        str(pr_author.get("login") or ""),  # scope-bound approval evidence
        allowed_commands=allowed_commands,
        pr_number=args.pr_number,
    )
    marker = _marker_summary(
        str(pr.get("body") or ""),
        str(pr.get("headRefOid") or ""),
        int(pr.get("number")),
    )
    after_status = _normalized_worktree_status(
        read(["git", "status", "--porcelain=v1", "--branch", "--untracked-files=all"])
    )
    worktree_head_after = read(["git", "rev-parse", "HEAD"])
    _require_clean_unchanged_worktree(before_status, after_status, worktree_head_before, worktree_head_after)
    evidence = {
        "fixture_version": FIXTURE_VERSION,
        "repository": {
            "requested_name": args.repository,
            "name": repository_name,
            "default_branch": default_branch_name,
            "root_verified": root_verified,
            **remote_identity,
        },
        "source_shas": {
            "local_head": local_head,
            "local_main": local_main,
            "local_origin_main": local_origin,
            "live_default_branch": default_branch_oid,
            "canonical_ref": args.canonical_ref,
            "worktree_clean_before": before_status["clean"],
            "worktree_clean_after": after_status["clean"],
            "worktree_status_unchanged": before_status["sha256"] == after_status["sha256"],
            "worktree_status_before_sha256": before_status["sha256"],
            "worktree_status_after_sha256": after_status["sha256"],
            "worktree_head_before": worktree_head_before,
            "worktree_head_after": worktree_head_after,
            "worktree_head_unchanged": worktree_head_before == worktree_head_after,
        },
        "canonical_state": canonical,
        "issue": {
            "number": int(issue.get("number")),
            "state": str(issue.get("state") or "").lower(),
            "state_reason": str(issue.get("stateReason") or "").lower() or None,
            "url": str(issue.get("url") or ""),
            "closeout_state": "closed" if issue.get("closedAt") is not None else "open",
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
            "author_login": _canonical_login(pr_author.get("login"), EvidenceUnavailableError),  # scope-bound approval evidence
            "author_type": "Bot" if pr_author.get("is_bot") else "User",  # scope-bound approval evidence
        },
        "checks": normalized_checks,
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
            "jobs": normalized_jobs,
        },
        "markers": marker,
        "review": {
            "decision": str(pr.get("reviewDecision") or "") or None,
            **approval_evidence,
        },
        "auto_merge": {"active": pr["autoMergeRequest"] is not None},
        "raw_chat_status": "no authority",
        "source_commands": commands,
    }
    try:
        evidence["review"] = _approval_evaluation(evidence["pr"], evidence["review"])["review"]
    except CollectorError as exc:
        raise ApprovalEvidenceUnavailableError("collected live review evidence is malformed") from exc
    route = _derive_actor_route(evidence)
    evidence["lifecycle_claim"] = route["lifecycle_claim"]
    evidence["actor_contract"] = role_contract.red_team_contract(
        repository=repository_name,
        issue=int(issue.get("number")),
        pull_request=int(pr.get("number")),
        branch=str(pr.get("headRefName") or ""),
        exact_sha=str(pr.get("headRefOid") or ""),
        lifecycle_state=route["lifecycle_state"],
        authority_source=authority_source,  # scope
        observation_timestamp=args.observed_at,
        program_next_action=route["program_next_action"],
        next_authorized_actor=route["next_authorized_actor"],  # scope
        developer_next_action=route["developer_next_action"],
        red_team_next_action=route["red_team_next_action"],
        human_approver_next_action=route["human_approver_next_action"],
        merge_operator_next_action=route["merge_operator_next_action"],
        requested_action_class=route["requested_action_class"],
    )
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


def _exact_mapping(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise CollectorError(f"{label} evidence is malformed")
    return value


def _positive_integer(value: Any) -> bool:
    return type(value) is int and value > 0


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_repository_evidence(value: Any) -> None:
    keys = {
        "requested_name", "name", "default_branch", "remote_name", "remote_transport",
        "root_verified", "remote_verified", "remote_identifier",
    }
    repository = _exact_mapping(value, keys, "repository identity")
    if repository["requested_name"] != EXPECTED_REPOSITORY:
        raise CollectorError("repository argument is outside the permitted repository")
    if not isinstance(repository["name"], str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository["name"]
    ):
        raise CollectorError("repository name evidence is malformed")
    if any(
        not _nonempty_string(repository[key])
        for key in ("default_branch", "remote_name", "remote_identifier")
    ):
        raise CollectorError("repository string evidence is malformed")
    if repository["remote_transport"] not in {"https", "ssh", "unsupported"}:
        raise CollectorError("repository transport evidence is malformed")
    if type(repository["root_verified"]) is not bool or type(repository["remote_verified"]) is not bool:
        raise CollectorError("repository verification status is malformed")


def _validate_issue_evidence(value: Any) -> None:
    issue = _exact_mapping(value, {"number", "state", "state_reason", "url", "closeout_state"}, "issue")
    if not _positive_integer(issue["number"]):
        raise CollectorError("issue number evidence is malformed")
    if issue["state"] not in {"open", "active", "closed"}:
        raise CollectorError("issue state evidence is malformed")
    if issue["state_reason"] is not None and not isinstance(issue["state_reason"], str):
        raise CollectorError("issue state-reason evidence is malformed")
    if not _nonempty_string(issue["url"]):
        raise CollectorError("issue URL evidence is malformed")
    if issue["closeout_state"] not in {"open", "closed"}:
        raise CollectorError("issue closeout evidence is malformed")
    if issue["state"] in {"open", "active"} and issue["closeout_state"] != "open":
        raise CollectorError("active issue requires open closeout evidence")
    if issue["state"] == "closed" and issue["closeout_state"] != "closed":
        raise CollectorError("closed issue requires closed closeout evidence")


def _validate_pr_evidence(value: Any) -> None:
    keys = {
        "number", "state", "base", "head_branch", "head", "draft", "merge_commit",
        "merged_at", "url", "author_login", "author_type",  # scope-bound approval evidence
    }
    pr = _exact_mapping(value, keys, "pr")
    if not _positive_integer(pr["number"]):
        raise CollectorError("PR number evidence is malformed")
    if pr["state"] not in {"open", "closed", "merged"}:
        raise CollectorError("PR state evidence is malformed")
    if any(not _nonempty_string(pr[key]) for key in ("base", "head_branch", "url")):
        raise CollectorError("PR string evidence is malformed")
    if not _is_sha(pr["head"]):
        raise CollectorError("PR head evidence is malformed")
    if type(pr["draft"]) is not bool:
        raise CollectorError("PR draft evidence is malformed")
    if pr["merge_commit"] is not None and not _is_sha(pr["merge_commit"]):
        raise CollectorError("PR merge-commit evidence is malformed")
    if pr["merged_at"] is not None and not _nonempty_string(pr["merged_at"]):
        raise CollectorError("PR merged-at evidence is malformed")
    if not GITHUB_LOGIN_RE.fullmatch(pr["author_login"] if isinstance(pr["author_login"], str) else ""):  # scope-bound approval evidence
        raise CollectorError("PR author login evidence is malformed")  # scope-bound approval evidence
    if pr["author_type"] not in {"User", "Bot"}:  # scope-bound approval evidence
        raise CollectorError("PR author account type evidence is malformed")  # scope-bound approval evidence


def _validate_checks_evidence(value: Any) -> None:
    if not isinstance(value, list) or len(value) > MAX_CHECKS:
        raise CollectorError("checks evidence is malformed or exceeds its bound")
    keys = {"name", "state", "bucket", "link"}
    for item in value:
        check = _exact_mapping(item, keys, "check item")
        if any(not isinstance(check[key], str) for key in keys):
            raise CollectorError("check item field is malformed")


def _validate_workflow_evidence(value: Any) -> None:
    keys = {
        "id", "name", "workflow_id", "event", "status", "conclusion", "head_sha",
        "head_branch", "url", "jobs",
    }
    run = _exact_mapping(value, keys, "workflow-run")
    if not _positive_integer(run["id"]) or not _positive_integer(run["workflow_id"]):
        raise CollectorError("workflow-run identifier evidence is malformed")
    if any(not _nonempty_string(run[key]) for key in ("name", "event", "status", "head_branch", "url")):
        raise CollectorError("workflow-run string evidence is malformed")
    if not _valid_conclusion(run["conclusion"], run["status"]):
        raise CollectorError("workflow-run conclusion evidence is malformed")
    if run["head_sha"] is not None and not _is_sha(run["head_sha"]):
        raise CollectorError("workflow-run head evidence is malformed")
    if not isinstance(run["jobs"], list) or len(run["jobs"]) > MAX_WORKFLOW_JOBS:
        raise CollectorError("workflow jobs evidence is malformed or exceeds its bound")
    for item in run["jobs"]:
        job = _exact_mapping(item, {"name", "status", "conclusion", "steps"}, "workflow job item")
        if not _nonempty_string(job["name"]) or not _nonempty_string(job["status"]):
            raise CollectorError("workflow job field is malformed")
        if not _valid_conclusion(job["conclusion"], job["status"]):
            raise CollectorError("workflow job conclusion is malformed")
        if not isinstance(job["steps"], list) or len(job["steps"]) > MAX_WORKFLOW_STEPS:
            raise CollectorError("workflow steps evidence is malformed or exceeds its bound")
        for nested in job["steps"]:
            step = _exact_mapping(nested, {"name", "number", "status", "conclusion"}, "workflow step item")
            if not _nonempty_string(step["name"]) or not _positive_integer(step["number"]):
                raise CollectorError("workflow step identity evidence is malformed")
            if not _nonempty_string(step["status"]):
                raise CollectorError("workflow step status evidence is malformed")
            if not _valid_conclusion(step["conclusion"], step["status"]):
                raise CollectorError("workflow step conclusion evidence is malformed")


def _validate_marker_evidence(value: Any) -> None:
    markers = _exact_mapping(
        value, {"owner_trigger_status", "red_team_status", "red_team_bound_sha"}, "markers"
    )
    if markers["owner_trigger_status"] not in {"valid", "missing_or_invalid"}:
        raise CollectorError("owner-trigger marker evidence is malformed")
    if markers["red_team_status"] not in {"valid", "missing", "stale"}:
        raise CollectorError("red-team marker evidence is malformed")
    if markers["red_team_bound_sha"] is not None and not _is_sha(markers["red_team_bound_sha"]):
        raise CollectorError("red-team bound SHA evidence is malformed")


def _validate_auto_merge_evidence(value: Any) -> None:
    auto_merge = _exact_mapping(value, {"active"}, "auto-merge")
    if type(auto_merge["active"]) is not bool:
        raise CollectorError("auto-merge active evidence is malformed")


def _source_command_firewall(data: dict[str, Any]) -> set[tuple[str, ...]]:
    """Reconstruct the exact evidence-derived read-only command set."""
    if (
        data["repository"]["name"].casefold() != EXPECTED_REPOSITORY.casefold()
    ):
        raise CollectorError("source-command evidence is outside the fixed repository scope")
    _derive_authority_source(data["issue"]["number"], data["pr"]["number"])  # scope-bound
    args = argparse.Namespace(
        repository=data["repository"]["name"],
        issue_number=data["issue"]["number"],
        pr_number=data["pr"]["number"],
        run_id=data["workflow_run"]["id"],
        canonical_ref=data["source_shas"]["canonical_ref"],
    )
    allowed = _live_command_firewall(args)
    canonical_author = _canonical_login(data["pr"]["author_login"])  # scope-bound approval evidence
    permission_logins = {  # scope-bound approval evidence
        _canonical_login(record["reviewer_login"])  # scope-bound approval evidence
        for record in data["review"]["review_records"]
        if record["state"] == "APPROVED"
        and record["commit_id"] == data["pr"]["head"]
        and record.get("submitted_at")
        and record["reviewer_type"] == "User"
        and _canonical_login(record["reviewer_login"]) != canonical_author  # scope-bound approval evidence
        and GITHUB_LOGIN_RE.fullmatch(record["reviewer_login"])  # scope-bound approval evidence
    }
    allowed.update(
        (
            "gh", "api", "--method", "GET",
            f"repos/{EXPECTED_REPOSITORY}/collaborators/{login}/permission",  # scope-bound approval evidence
        )
        for login in permission_logins  # scope-bound approval evidence
    )
    return allowed


def _validate_source_commands(value: Any, data: dict[str, Any] | None = None) -> None:
    if not isinstance(value, list) or len(value) > MAX_SOURCE_COMMANDS:
        raise CollectorError("source-command evidence is malformed or exceeds its bound")
    allowed_commands = _source_command_firewall(data) if data is not None and value else None
    keys = {"argv", "return_code", "stdout_sha256", "stderr_present"}
    for item in value:
        command = _exact_mapping(item, keys, "source-command item")
        argv = command["argv"]
        if (
            not isinstance(argv, list)
            or not 2 <= len(argv) <= MAX_COMMAND_ARGV
            or any(not _nonempty_string(argument) for argument in argv)
        ):
            raise CollectorError("source-command argv evidence is malformed")
        if type(command["return_code"]) is not int or command["return_code"] != 0:
            raise CollectorError("source-command return code evidence is malformed")
        if not isinstance(command["stdout_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", command["stdout_sha256"]):
            raise CollectorError("source-command stdout hash evidence is malformed")
        if type(command["stderr_present"]) is not bool:
            raise CollectorError("source-command stderr evidence is malformed")
        if allowed_commands is not None:
            try:
                _validate_command(argv, allowed_commands=allowed_commands)
            except CommandRejectedError as exc:
                raise CollectorError("source-command evidence violates the exact read-only firewall") from exc


def _validate_collected_review_evidence(value: Any) -> None:
    review = _exact_mapping(
        value,
        {"decision", "evidence_status", "review_records", "permission_records"},
        "collected pre-evaluation approval",
    )
    if review["decision"] is not None and review["decision"] not in REVIEW_DECISIONS:
        raise CollectorError("approval decision evidence is malformed")
    if review["evidence_status"] not in {"complete", "truncated", "unavailable"}:
        raise CollectorError("approval evidence status is malformed")
    records = review["review_records"]
    permissions = review["permission_records"]
    if not isinstance(records, list) or len(records) > MAX_REVIEW_RECORDS:
        raise CollectorError("approval review evidence is malformed or exceeds its bound")
    if not isinstance(permissions, list) or len(permissions) > MAX_PERMISSION_CANDIDATES:
        raise CollectorError("permission approval evidence is malformed or exceeds its bound")
    review_keys = {
        "review_id", "reviewer_login", "reviewer_type", "state", "submitted_at", "commit_id", "author_association",  # scope-bound approval evidence
    }
    for record in records:
        item = _exact_mapping(record, review_keys, "approval review record")
        if not _positive_integer(item["review_id"]):
            raise CollectorError("approval review ID evidence is malformed")
        _canonical_login(item["reviewer_login"])  # scope-bound approval evidence
        if item["reviewer_type"] not in ACCOUNT_TYPES or item["state"] not in REVIEW_STATES:
            raise CollectorError("approval review enum evidence is malformed")
        _require_review_timestamp(item["submitted_at"], item["state"], CollectorError)
        if not _is_sha(item["commit_id"]):
            raise CollectorError("approval review commit evidence is malformed")
        if not isinstance(item["author_association"], str) or len(item["author_association"]) > MAX_AUTHOR_ASSOCIATION_LENGTH:  # scope-bound approval evidence
            raise CollectorError("approval review association evidence is malformed")
    permission_keys = {"reviewer_login", "permission", "role_name", "account_type"}  # scope-bound approval evidence
    for permission in permissions:
        item = _exact_mapping(permission, permission_keys, "permission approval record")
        _canonical_login(item["reviewer_login"])  # scope-bound approval evidence
        if item["permission"] not in PERMISSION_VALUES or item["account_type"] not in ACCOUNT_TYPES:
            raise CollectorError("permission approval enum evidence is malformed")
        if not _nonempty_string(item["role_name"]) or len(item["role_name"]) > MAX_ROLE_NAME_LENGTH:
            raise CollectorError("permission approval role evidence is malformed")


def _validate_review_evidence(value: Any) -> None:
    review = _exact_mapping(
        value,
        {
            "decision", "evidence_status", "review_records", "permission_records",
            "qualifying_approvals", "disqualified_approvals", "disqualification_reasons",
        },
        "evaluated normalized approval",
    )
    _validate_collected_review_evidence(
        {key: review[key] for key in ("decision", "evidence_status", "review_records", "permission_records")}
    )
    for field in ("qualifying_approvals", "disqualified_approvals"):
        logins = review[field]  # scope-bound approval evidence
        if not isinstance(logins, list) or len(logins) > MAX_PERMISSION_CANDIDATES:  # scope-bound approval evidence
            raise CollectorError("approval login list evidence is malformed or exceeds its bound")  # scope-bound approval evidence
        canonical = [_canonical_login(login) for login in logins]  # scope-bound approval evidence
        if len(canonical) != len(set(canonical)):
            raise CollectorError("approval login list contains duplicate identities")  # scope-bound approval evidence
    reasons = review["disqualification_reasons"]
    if not isinstance(reasons, dict) or len(reasons) > MAX_PERMISSION_CANDIDATES:
        raise CollectorError("approval disqualification reasons are malformed or exceed their bound")
    qualifying = {_canonical_login(login) for login in review["qualifying_approvals"]}  # scope-bound approval evidence
    disqualified = {_canonical_login(login) for login in review["disqualified_approvals"]}  # scope-bound approval evidence
    if qualifying & disqualified:
        raise CollectorError("approval qualifying and disqualified identities overlap")
    reason_entries = _canonical_reason_entries(reasons)
    reason_identities: set[str] = set()
    for login, canonical_login, values in reason_entries:  # scope-bound approval evidence
        if not isinstance(values, list) or not values or len(values) > MAX_DISQUALIFICATION_REASONS:
            raise CollectorError("approval disqualification reason list is malformed")
        if login == "_evidence":  # scope-bound approval evidence
            if not set(values).issubset(EVIDENCE_WIDE_DISQUALIFICATION_REASONS):
                raise CollectorError("approval evidence-wide reason is not permitted")
        else:
            if canonical_login not in disqualified:  # scope-bound approval evidence
                raise CollectorError("approval disqualification reason lacks a disqualified reviewer")
            reason_identities.add(canonical_login)  # scope-bound approval evidence
        if len(values) != len(set(values)) or any(
            not isinstance(reason, str)
            or reason not in DISQUALIFICATION_REASONS
            or len(reason) > MAX_DISQUALIFICATION_REASON_LENGTH
            for reason in values
        ):
            raise CollectorError("approval disqualification reason is malformed")
    if disqualified != reason_identities:
        raise CollectorError("every disqualified approval requires a nonempty reason list")


def _canonical_reason_entries(reasons: dict[str, Any]) -> list[tuple[str, str | None, Any]]:
    """Preserve original reason keys while rejecting canonical reviewer collisions."""
    entries: list[tuple[str, str | None, Any]] = []
    originals_by_canonical: dict[str, str] = {}
    for original, values in reasons.items():
        if original == "_evidence":
            entries.append((original, None, values))
            continue
        canonical = _canonical_login(original)  # scope-bound approval evidence
        prior = originals_by_canonical.get(canonical)
        if prior is not None:
            raise CollectorError(
                "approval disqualification reason keys collide after canonicalization"
            )
        originals_by_canonical[canonical] = original
        entries.append((original, canonical, values))
    return entries


def _canonical_reason_map(reasons: dict[str, Any]) -> dict[str, Any]:
    """Build a canonical reason map only after one-to-one validation succeeds."""
    return {
        canonical if canonical is not None else original: values
        for original, canonical, values in _canonical_reason_entries(reasons)
    }


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
        "actor_contract",
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
    if data.get("lifecycle_claim") not in {
        "active_pr",
        "externally_approved",
        "merge_ready",
        "merged_unverified",
        "verified_main_issue_open",
        "closed_gate",
        "blocked",
        "quarantined",
    }:
        raise CollectorError("lifecycle claim is invalid")
    source = data.get("source_shas")
    if not isinstance(source, dict) or set(source) != {
        "local_head",
        "local_main",
        "local_origin_main",
        "live_default_branch",
        "canonical_ref",
        "worktree_clean_before",
        "worktree_clean_after",
        "worktree_status_unchanged",
        "worktree_status_before_sha256",
        "worktree_status_after_sha256",
        "worktree_head_before",
        "worktree_head_after",
        "worktree_head_unchanged",
    }:
        raise CollectorError("source SHA object is malformed")
    if any(value is not None and not _is_sha(value) for key, value in source.items() if key in {
        "local_head", "local_main", "local_origin_main", "live_default_branch",
        "worktree_head_before", "worktree_head_after",
    }):
        raise CollectorError("source SHA is malformed")
    if not _is_sha(source["canonical_ref"]):
        raise CollectorError("canonical source ref is malformed")
    if any(type(source[key]) is not bool for key in (
        "worktree_clean_before", "worktree_clean_after", "worktree_status_unchanged", "worktree_head_unchanged",
    )):
        raise CollectorError("worktree provenance boolean evidence is malformed")
    if any(not isinstance(source[key], str) or not re.fullmatch(r"[0-9a-f]{64}", source[key]) for key in (
        "worktree_status_before_sha256", "worktree_status_after_sha256",
    )):
        raise CollectorError("worktree provenance hash evidence is malformed")
    if source["worktree_status_unchanged"] and (
        source["worktree_status_before_sha256"] != source["worktree_status_after_sha256"]
    ):
        raise CollectorError("worktree status hashes contradict unchanged evidence")
    if not (
        source["worktree_clean_before"] and source["worktree_clean_after"]
        and source["worktree_status_unchanged"] and source["worktree_head_unchanged"]
        and source["worktree_head_before"] == source["worktree_head_after"]
    ):
        raise CollectorError("worktree provenance evidence is not clean and unchanged")
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
    if not _nonempty_string(canonical.get("schema_version")):
        raise CollectorError("canonical schema version is malformed")
    if not _nonempty_string(canonical.get("lifecycle_state")):
        raise CollectorError("canonical lifecycle state is malformed")
    if not _is_sha(canonical.get("current_main_sha")):
        raise CollectorError("canonical main SHA is malformed")
    if canonical.get("consistency_status") not in CLASSIFICATIONS:
        raise CollectorError("canonical consistency status is invalid")
    linked_issue = canonical.get("linked_issue")
    if not isinstance(linked_issue, dict) or set(linked_issue) != {"number", "state"}:
        raise CollectorError("canonical linked issue is malformed")
    if type(linked_issue.get("number")) is not int or linked_issue["number"] < 1:
        raise CollectorError("canonical linked issue number is malformed")
    if linked_issue.get("state") not in {"active", "open", "closed_completed", "closed_not_planned"}:
        raise CollectorError("canonical linked issue state is invalid")
    linked_pr = canonical.get("linked_pr")
    linked_pr_required = {"number", "state", "observed_head_sha"}
    linked_pr_allowed = linked_pr_required | {"url", "head_sha_source"}
    if (
        not isinstance(linked_pr, dict)
        or not linked_pr_required.issubset(linked_pr)
        or set(linked_pr) - linked_pr_allowed
    ):
        raise CollectorError("canonical linked PR is malformed")
    if type(linked_pr.get("number")) is not int or linked_pr["number"] < 1:
        raise CollectorError("canonical linked PR number is malformed")
    if linked_pr.get("state") not in {"open", "closed", "merged"}:
        raise CollectorError("canonical linked PR state is invalid")
    if linked_pr.get("observed_head_sha") is not None and not _is_sha(linked_pr["observed_head_sha"]):
        raise CollectorError("canonical linked PR observed head SHA is malformed")
    if "url" in linked_pr and (not isinstance(linked_pr["url"], str) or not linked_pr["url"].strip()):
        raise CollectorError("canonical linked PR URL is malformed")
    if "head_sha_source" in linked_pr and linked_pr["head_sha_source"] != "live_github_required":
        raise CollectorError("canonical linked PR head SHA source is malformed")
    _validate_repository_evidence(data["repository"])
    _validate_issue_evidence(data["issue"])
    _validate_pr_evidence(data["pr"])
    _validate_checks_evidence(data["checks"])
    _validate_workflow_evidence(data["workflow_run"])
    _validate_marker_evidence(data["markers"])
    _validate_auto_merge_evidence(data["auto_merge"])
    if not isinstance(data["actor_contract"], dict) or set(data["actor_contract"]) != set(
        role_contract.GOVERNING_KEYS
    ):
        raise CollectorError("actor contract evidence is malformed")
    review = data["review"]
    if isinstance(review, dict) and set(review) == {
        "decision", "evidence_status", "review_records", "permission_records",
    }:
        _validate_collected_review_evidence(review)
    else:
        _validate_review_evidence(review)
    if "source_commands" in data:
        _validate_source_commands(data["source_commands"], data)


def _actor_expected_context(data: dict[str, Any], observed_at: str) -> dict[str, Any]:
    issue_number = data["issue"]["number"]
    authority_source = _derive_authority_source(issue_number, data["pr"]["number"])  # scope-bound
    lifecycle = {
        "active_pr": "EXTERNAL_EXACT_SHA_REVIEW",
        "externally_approved": "HUMAN_APPROVAL_PENDING",
        "merge_ready": "MERGE_PENDING",
        "merged_unverified": "MERGED_MAIN_VERIFICATION_PENDING",
        "verified_main_issue_open": "VERIFIED_MAIN_ISSUE_CLOSEOUT_PENDING",
        "closed_gate": "PHASE_CLOSED_READY_FOR_NEXT_PHASE",
        "blocked": "BLOCKED",
        "quarantined": "QUARANTINED",
    }.get(data["lifecycle_claim"], "QUARANTINED")
    return {
        "REPOSITORY": data["repository"]["name"],
        "ISSUE": issue_number,
        "PULL_REQUEST": data["pr"]["number"],
        "BRANCH": data["pr"]["head_branch"],
        "EXACT_SHA": data["pr"]["head"],
        "LIFECYCLE_STATE": lifecycle,
        "AUTHORITY_SOURCE": authority_source,  # scope
        "CURRENT_TIME": observed_at,
    }


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


def _actor_route(
    lifecycle_claim: str,
    lifecycle_state: str,
    program_next_action: str,
    *,
    next_authorized_actor: str = "NONE",  # scope-bound
    developer_next_action: str = "NONE",
    red_team_next_action: str = "NONE",
    human_approver_next_action: str = "NONE",
    merge_operator_next_action: str = "NONE",
    requested_action_class: str = "NONE",
) -> dict[str, str]:
    return {
        "lifecycle_claim": lifecycle_claim,
        "lifecycle_state": lifecycle_state,
        "program_next_action": program_next_action,
        "next_authorized_actor": next_authorized_actor,  # scope-bound
        "developer_next_action": developer_next_action,
        "red_team_next_action": red_team_next_action,
        "human_approver_next_action": human_approver_next_action,
        "merge_operator_next_action": merge_operator_next_action,
        "requested_action_class": requested_action_class,
    }


def _inactive_actor_route(lifecycle_claim: str, reason: str) -> dict[str, str]:
    lifecycle_state = "BLOCKED" if lifecycle_claim == "blocked" else "QUARANTINED"
    return _actor_route(
        lifecycle_claim,
        lifecycle_state,
        f"Stop and reconcile lifecycle evidence: {reason}",
    )


def _separate_red_team_reviewers(pr: dict[str, Any], review: dict[str, Any]) -> list[str]:
    """Return current-head non-author reviewers outside human-approver scope."""
    author = _canonical_login(pr.get("author_login"))  # scope-bound
    qualifying = {_canonical_login(login) for login in review.get("qualifying_approvals") or []}  # scope-bound
    return sorted({
        _canonical_login(record.get("reviewer_login"))  # scope-bound
        for record in review.get("review_records") or []
        if record.get("state") == "APPROVED"
        and record.get("commit_id") == pr.get("head")
        and record.get("reviewer_type") == "User"
        and record.get("submitted_at")
        and _canonical_login(record.get("reviewer_login")) != author  # scope-bound
        and _canonical_login(record.get("reviewer_login")) not in qualifying  # scope-bound
    })


def _derive_actor_route(data: dict[str, Any]) -> dict[str, str]:
    """Derive one fail-closed actor action from validated lifecycle evidence."""
    issue = data["issue"]
    pr = data["pr"]
    markers = data["markers"]
    source = data["source_shas"]
    review = data["review"]
    pr_state = str(pr.get("state") or "").lower()
    issue_state = str(issue.get("state") or "").lower()

    if data.get("auto_merge", {}).get("active"):
        return _inactive_actor_route("quarantined", "auto-merge is active")
    if pr.get("draft"):
        return _inactive_actor_route("quarantined", "the governed pull request is draft")
    if pr_state == "open" and (pr.get("merge_commit") or pr.get("merged_at")):
        return _inactive_actor_route("quarantined", "open pull request contains merge evidence")
    if pr_state == "open" and issue_state not in {"open", "active"}:
        return _inactive_actor_route("quarantined", "open pull request conflicts with issue state")

    workflow = _control_workflow_evaluation(data)
    if workflow["quarantined"]:
        return _inactive_actor_route("quarantined", workflow["quarantined"][0])
    if workflow["blocked"]:
        return _inactive_actor_route("blocked", workflow["blocked"][0])

    if pr_state == "open":
        red_status = markers.get("red_team_status")
        if red_status == "missing":
            return _actor_route(
                "active_pr",
                "EXTERNAL_EXACT_SHA_REVIEW",
                "External exact-SHA review must inspect the current PR head.",
                next_authorized_actor="RED_TEAM",  # scope-bound
                red_team_next_action="REVIEW_EXACT_SHA",
                requested_action_class="EXACT_SHA_REVIEW",
            )
        if red_status != "valid" or markers.get("red_team_bound_sha") != pr.get("head"):
            return _inactive_actor_route("quarantined", "red-team marker is stale or invalid")

        approval = _approval_evaluation(pr, review)
        normalized_review = approval["review"]
        separated_red_team = _separate_red_team_reviewers(pr, normalized_review)
        approval_quarantine = list(approval["quarantined"])
        if issue.get("number") == 55 and separated_red_team:
            approval_quarantine = [
                reason for reason in approval_quarantine
                if reason != "Review decision claims approval without a qualifying current-head approver"
            ]
        if approval_quarantine:
            return _inactive_actor_route("quarantined", approval_quarantine[0])
        if approval["blocked"]:
            return _inactive_actor_route("blocked", approval["blocked"][0])
        if issue.get("number") == 55 and not separated_red_team:
            return _inactive_actor_route(
                "quarantined", "current-head red-team reviewer separation is not proven"
            )
        if normalized_review.get("qualifying_approvals"):
            return _actor_route(
                "merge_ready",
                "MERGE_PENDING",
                "A separate merge operator may merge only after all current-head gates.",
                next_authorized_actor="MERGE_OPERATOR",  # scope-bound
                merge_operator_next_action="MERGE_AFTER_ALL_GATES",
            )
        return _actor_route(
            "externally_approved",
            "HUMAN_APPROVAL_PENDING",
            "A separate human approver must review the current exact head.",
            next_authorized_actor="HUMAN_APPROVER",  # scope-bound
            human_approver_next_action="REVIEW_FOR_HUMAN_APPROVAL",
        )

    if pr_state != "merged":
        return _inactive_actor_route("quarantined", "pull request is closed without verified merge evidence")
    if not pr.get("merged_at") or not pr.get("merge_commit"):
        return _inactive_actor_route("quarantined", "merge is claimed without complete merge evidence")
    if markers.get("red_team_status") != "valid" or markers.get("red_team_bound_sha") != pr.get("head"):
        return _inactive_actor_route("quarantined", "merged state lacks current-head red-team evidence")

    approval = _approval_evaluation(pr, review)
    if approval["quarantined"]:
        return _inactive_actor_route("quarantined", approval["quarantined"][0])
    if approval["blocked"] or not approval["review"].get("qualifying_approvals"):
        return _inactive_actor_route("blocked", "merged state lacks qualifying human approval")
    if issue.get("number") == 55 and not _separate_red_team_reviewers(pr, approval["review"]):
        return _inactive_actor_route("quarantined", "red-team and human approval separation is not proven")

    if pr.get("merge_commit") != source.get("live_default_branch"):
        return _actor_route(
            "merged_unverified",
            "MERGED_MAIN_VERIFICATION_PENDING",
            "Verify the merged commit on main; no mutation action is authorized.",
        )
    if issue_state in {"open", "active"} and issue.get("closeout_state") == "open":
        return _actor_route(
            "verified_main_issue_open",
            "VERIFIED_MAIN_ISSUE_CLOSEOUT_PENDING",
            "Verified main is proven; issue closeout remains separate and is not granted here.",
        )
    if (
        issue_state == "closed"
        and str(issue.get("state_reason") or "").lower() == "completed"
        and issue.get("closeout_state") == "closed"
    ):
        return _actor_route(
            "closed_gate",
            "PHASE_CLOSED_READY_FOR_NEXT_PHASE",
            "Verify the closed gate remains current before later-phase planning.",
        )
    return _inactive_actor_route("quarantined", "verified main and issue closeout evidence conflict")


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
        "local head SHA": source.get("local_head"),
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

    if not data["repository"].get("root_verified"):
        findings.append("Requested repository root contradicts the Git top-level identity")
    if not data["repository"].get("remote_verified"):
        findings.append("Origin remote contradicts the permitted repository identity")
    if data["repository"].get("name", "").casefold() != EXPECTED_REPOSITORY.casefold():
        findings.append("Live repository identity contradicts the permitted repository")
        findings.append("Workflow provenance mismatch: repository")
    if findings:
        return "quarantined", sorted(set(findings)), sorted(blockers), True

    claim = data["lifecycle_claim"]
    aggregate_review_decision = str(review.get("decision") or "").upper()
    if claim in {"merge_ready", "merged_unverified", "verified_main_issue_open", "closed_gate"} and aggregate_review_decision in {
        "CHANGES_REQUESTED", "REVIEW_REQUIRED",
    }:
        findings.append("Adverse aggregate review decision forbids merge-ready or closed-gate consistency")
        return "quarantined", sorted(set(findings)), sorted(blockers), True
    if claim in {"active_pr", "externally_approved", "merge_ready"}:
        active_bindings = (
            ("Local HEAD differs from the active PR head", source["local_head"], pr.get("head")),
            ("Live repository default branch is not main", data["repository"].get("default_branch"), "main"),
            ("Active PR base branch is not main", pr.get("base"), "main"),
            ("Workflow run head differs from the active PR head", run.get("head_sha"), pr.get("head")),
            ("Workflow run branch differs from the active PR branch", run.get("head_branch"), pr.get("head_branch")),
        )
        findings.extend(label for label, actual, expected in active_bindings if actual != expected)
    elif claim in {"merged_unverified", "verified_main_issue_open", "closed_gate"}:
        closed_bindings = (
            ("Closed-gate local main differs from the live default branch", source["local_main"], source["live_default_branch"]),
            ("Live repository default branch is not main", data["repository"].get("default_branch"), "main"),
            ("Closed-gate PR base branch is not the verified default branch", pr.get("base"), data["repository"].get("default_branch")),
        )
        findings.extend(label for label, actual, expected in closed_bindings if actual != expected)
        if claim in {"verified_main_issue_open", "closed_gate"}:
            verified_bindings = (
                ("Verified-main local HEAD differs from the live default branch", source["local_head"], source["live_default_branch"]),
                ("Verified-main merge commit differs from the live default branch", pr.get("merge_commit"), source["live_default_branch"]),
            )
            findings.extend(label for label, actual, expected in verified_bindings if actual != expected)
        elif pr.get("merge_commit") == source["live_default_branch"]:
            findings.append("Merged-unverified claim already has verified-main evidence")
    if findings:
        return "quarantined", sorted(set(findings)), sorted(blockers), True

    canonical_issue = canonical["linked_issue"]
    canonical_pr = canonical["linked_pr"]
    if source["local_main"] != source["live_default_branch"]:
        findings.append("Local main differs from the live default branch")
    if source.get("local_origin_main") and source["local_origin_main"] != source["live_default_branch"]:
        findings.append("Local origin/main differs from the live default branch")
    if canonical["current_main_sha"] != source["live_default_branch"]:
        findings.append("Canonical main differs from the live default branch")
    if canonical_issue.get("number") != issue.get("number"):
        findings.append("Canonical linked issue differs from live issue")
    if canonical_pr.get("number") != pr.get("number"):
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
    if claim in {"active_pr", "externally_approved", "merge_ready"}:
        if canonical["lifecycle_state"] != "developer_implementation_in_review":
            findings.append("Canonical lifecycle state differs from the active PR family")
        if canonical["consistency_status"] != "requires_live_verification":
            findings.append("Canonical consistency status differs from the active PR family")
    elif claim == "closed_gate":
        if canonical["lifecycle_state"] != "phase_closed_ready_for_next_phase":
            findings.append("Canonical lifecycle state differs from the closed gate")
        if canonical["consistency_status"] != "consistent":
            findings.append("Canonical consistency status differs from the closed gate")
    else:
        if canonical["consistency_status"] != "requires_live_verification":
            findings.append("Canonical consistency status differs from the verification lifecycle")
    observed_head = canonical_pr.get("observed_head_sha")
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
    actor_result = data["actor_contract_result"]
    if not actor_result["valid"]:
        findings.extend(f"Actor role contract denied: {reason}" for reason in actor_result["reasons"])
        return "quarantined", sorted(set(findings)), sorted(blockers), True
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

    pr_state = str(pr.get("state") or "").lower()
    issue_state = str(issue.get("state") or "").lower()
    approvals = review.get("qualifying_approvals") or []
    red_status = markers.get("red_team_status")

    active_identity = (
        pr_state == "open"
        and issue_state in {"open", "active"}
        and pr.get("base") == "main"
        and not pr.get("draft")
        and not pr.get("merge_commit")
        and not pr.get("merged_at")
    )
    if claim == "active_pr":
        if not active_identity:
            findings.append("Active-PR lifecycle evidence is contradictory")
            return "quarantined", sorted(findings), sorted(blockers), True
        if red_status == "missing":
            blockers.append("External exact-SHA red-team review is pending")
        if not approvals:
            blockers.append("Human/write-access approval is pending")
        blockers.append("Merge, main verification and linked-issue closeout are pending")
        findings.append("Active developer PR requires live verification and external review")
        return "requires_live_verification", sorted(findings), sorted(set(blockers)), False

    if claim == "externally_approved":
        if not active_identity or red_status != "valid":
            findings.append("Externally-approved claim lacks current marker or workflow evidence")
            return "quarantined", sorted(findings), sorted(blockers), True
        if not approvals:
            blockers.append("Human/write-access approval is pending")
        blockers.append("Merge, main verification and linked-issue closeout are pending")
        findings.append("External exact-SHA approval is proven; merge decision power is not")
        return "requires_live_verification", sorted(findings), sorted(set(blockers)), False

    if claim == "merge_ready":
        if not active_identity or red_status != "valid" or not approvals:
            findings.append("Merge-readiness claim lacks current required evidence")
            return "quarantined", sorted(findings), sorted(blockers), True
        blockers.append("Protected human merge, main verification and linked-issue closeout are pending")
        findings.append("Separated external review and human/write approval evidence support merge readiness")  # scope-bound lifecycle evidence
        return "requires_live_verification", sorted(findings), sorted(blockers), False

    if claim == "merged_unverified":
        merged_identity = (
            pr_state == "merged"
            and bool(pr.get("merged_at"))
            and bool(pr.get("merge_commit"))
            and pr.get("merge_commit") != source["live_default_branch"]
            and red_status == "valid"
            and bool(approvals)
        )
        if not merged_identity:
            findings.append("Merged-unverified claim lacks separated gate or merge evidence")
            return "quarantined", sorted(findings), sorted(blockers), True
        blockers.append("Main verification and linked-issue closeout are pending")
        findings.append("Merge is proven; verified main and issue closeout remain unproven")
        return "requires_live_verification", sorted(findings), sorted(blockers), False

    if claim == "verified_main_issue_open":
        verified_open_identity = (
            pr_state == "merged"
            and issue_state in {"open", "active"}
            and issue.get("closeout_state") == "open"
            and bool(pr.get("merged_at"))
            and pr.get("merge_commit") == source["live_default_branch"]
            and red_status == "valid"
            and bool(approvals)
        )
        if not verified_open_identity:
            findings.append("Verified-main/open-issue claim lacks exact merge or issue evidence")
            return "quarantined", sorted(findings), sorted(blockers), True
        blockers.append("Linked-issue closeout remains separate and pending")
        findings.append("Verified main is proven; linked issue remains open")
        return "requires_live_verification", sorted(findings), sorted(blockers), False

    closed_consistent = (
        pr_state == "merged"
        and issue_state == "closed"
        and str(issue.get("state_reason") or "").lower() == "completed"
        and issue.get("closeout_state") == "closed"
        and bool(pr.get("merged_at"))
        and pr.get("merge_commit") == source["live_default_branch"]
        and pr.get("base") == data["repository"].get("default_branch")
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
    actor = data["actor_contract"]
    next_actor = actor.get("NEXT_AUTHORIZED_ACTOR")  # scope-bound
    lifecycle_state = actor.get("LIFECYCLE_STATE")
    if classification not in {"requires_live_verification", "consistent"}:
        next_action = "Stop and reconcile the listed evidence before any consequential action."
    elif next_actor == "RED_TEAM":
        next_action = "External exact-SHA review must rerun this collector against the current PR head."
    elif next_actor == "HUMAN_APPROVER":
        next_action = "A separate human approver must review the current exact head."
    elif next_actor == "MERGE_OPERATOR":
        next_action = "A separate merge operator may merge only after all current-head gates."
    elif lifecycle_state == "MERGED_MAIN_VERIFICATION_PENDING":
        next_action = "Verify the merged commit on main; no mutation action is authorized."
    elif lifecycle_state == "VERIFIED_MAIN_ISSUE_CLOSEOUT_PENDING":
        next_action = "Issue closeout remains separate and is not granted by this packet."
    else:
        next_action = "Verify the merged gate remains current before planning a later phase."
    return {
        "schema_version": PACKET_SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "observed_at": observed_at,
        "repository": data["repository"],
        "canonical_schema_version": str(data["canonical_state"].get("schema_version")),
        "source_shas": data["source_shas"],
        "issue": data["issue"],
        "pr": pr,
        "checks": sorted(data["checks"], key=lambda item: _canonical_json(item)),
        "workflow_run": data["workflow_run"],
        "markers": data["markers"],
        "review": data["review"],
        "auto_merge": data["auto_merge"],
        "actor_contract": data["actor_contract"],
        "actor_contract_result": data["actor_contract_result"],
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
    actor = packet["actor_contract"]
    actor_result = packet["actor_contract_result"]
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
        f"- Repository: {packet['repository']['name']}",
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
        "## Actor-Bound Role Contract",
        "",
        f"- Active actor: {actor.get('ACTOR_ROLE')}",
        f"- Actor-role declaration: ROLE={actor.get('ROLE')}",
        f"- Repository binding: {actor.get('REPOSITORY')}",
        f"- Issue binding: #{actor.get('ISSUE')}",
        f"- Pull-request binding: #{actor.get('PULL_REQUEST')}",
        f"- Branch binding: {actor.get('BRANCH')}",
        f"- Exact-SHA binding: {actor.get('EXACT_SHA')}",
        f"- Lifecycle binding: {actor.get('LIFECYCLE_STATE')}",
        f"- Authority source scope: {actor.get('AUTHORITY_SOURCE')}",
        f"- Observation timestamp: {actor.get('OBSERVATION_TIMESTAMP')}",
        f"- Program next action: {actor.get('PROGRAM_NEXT_ACTION')}",
        f"- Next authorized actor scope: {actor.get('NEXT_AUTHORIZED_ACTOR')}",
        f"- Developer next action: {actor.get('DEVELOPER_NEXT_ACTION')}",
        f"- Red-team next action: {actor.get('RED_TEAM_NEXT_ACTION')}",
        f"- Human-approver next action: {actor.get('HUMAN_APPROVER_NEXT_ACTION')}",
        f"- Merge-operator next action: {actor.get('MERGE_OPERATOR_NEXT_ACTION')}",
        f"- Role-conflict status: {actor_result.get('role_conflict_status')}",
        f"- Role-repair state: {actor_result.get('role_repair_state')}",
        f"- Requested action decision: {actor_result.get('decision')}",
        f"- Denied incident summary: {json.dumps(actor_result.get('incident'), sort_keys=True, separators=(',', ':')) if actor_result.get('incident') else 'NONE'}",
        "- Program direction is descriptive and is not actor authority scope.",
        "- Stage A claim: ACTOR_BOUND_ROLE_CONTRACT=IMPLEMENTED_IN_REVIEW",
        "- Full runtime isolation: NOT_PROVEN",
        "- Stage B required: YES",
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
    candidate = Path(os.path.abspath(output_dir))
    if candidate.is_symlink():
        raise UnsafeEvidenceError("prohibited symlink output directory rejected")

    ancestor = candidate
    suffix: list[str] = []
    while not ancestor.exists() and not ancestor.is_symlink():
        suffix.insert(0, ancestor.name)
        parent = ancestor.parent
        if parent == ancestor:
            raise UnsafeEvidenceError("prohibited output path has no existing ancestor")
        ancestor = parent
    try:
        resolved_ancestor = ancestor.resolve(strict=True)
    except OSError as exc:
        raise UnsafeEvidenceError("prohibited output path is inaccessible") from exc
    prospective = resolved_ancestor.joinpath(*suffix)
    if prospective == repo or repo in prospective.parents:
        raise UnsafeEvidenceError("prohibited output path resolves inside the repository")
    if ancestor.is_symlink() and (resolved_ancestor == repo or repo in resolved_ancestor.parents):
        raise UnsafeEvidenceError("prohibited output symlink ancestor resolves inside repository")

    if candidate.exists() and not candidate.is_dir():
        raise UnsafeEvidenceError("prohibited output destination is not a directory")
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise UnsafeEvidenceError("prohibited output path is inaccessible") from exc
    if resolved == repo or repo in resolved.parents:
        raise UnsafeEvidenceError("prohibited output path resolves inside the repository")
    for name in OUTPUT_NAMES:
        target = resolved / name
        if target.is_symlink():
            raise UnsafeEvidenceError("prohibited output-file symlink rejected")
        if target.exists():
            if not target.is_file():
                raise UnsafeEvidenceError("prohibited output target is not a regular file")
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
    actor_result = role_contract.validate_role_contract(
        data["actor_contract"], _actor_expected_context(data, observed_at)
    )
    approval = _approval_evaluation(data["pr"], data["review"])
    data = dict(data)
    data["review"] = approval["review"]
    data["actor_contract_result"] = actor_result
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
        "actor_contract": data["actor_contract"],
        "actor_contract_result": data["actor_contract_result"],
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
