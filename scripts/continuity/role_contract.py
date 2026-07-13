#!/usr/bin/env python3
"""Deterministic actor-bound role contract validation for Stage A.

Invalid or conflicting input is returned as a JSON-compatible denial result.  The
CLI catches malformed JSON and filesystem errors and emits one bounded error
object without a traceback.  Stage A enforces interpretation inside this module
and generated continuity evidence; it does not remove runtime tools or credentials.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ACTORS = ("CODEX_DEVELOPER", "RED_TEAM", "HUMAN_APPROVER", "MERGE_OPERATOR")
NEXT_ACTORS = ACTORS + ("NONE",)
ROLE_STATES = ("NORMAL", "ROLE_CONFLICT", "REPAIR_REQUIRED", "READ_ONLY_ROLE_RESTORED")

LIFECYCLE_STATES = {
    "DEVELOPER_IMPLEMENTATION_IN_REVIEW",
    "EXTERNAL_EXACT_SHA_REVIEW",
    "HUMAN_APPROVAL_PENDING",
    "MERGE_PENDING",
    "MERGED_MAIN_VERIFICATION_PENDING",
    "VERIFIED_MAIN_ISSUE_CLOSEOUT_PENDING",
    "PHASE_CLOSED_READY_FOR_NEXT_PHASE",
    "BLOCKED",
    "QUARANTINED",
}
AUTHORITY_SOURCES = {  # scope
    "GITHUB_ISSUE_49",
    "GITHUB_ISSUE_55",
    "GITHUB_PULL_REQUEST",
    "OWNER_APPROVED_GITHUB_ISSUE",
    "VERSIONED_PROJECT_CONTROL",
}

ACTION_CLASSES = {
    "NONE",
    "PROMPT_AUTHORING",  # scope
    "EXACT_SHA_REVIEW",
    "REPOSITORY_MUTATION",
    "GITHUB_MUTATION",
    "TERMINAL_MUTATION",
    "IMPLEMENTATION",
    "REVIEW_SUBMISSION",
    "HUMAN_APPROVAL",
    "MERGE",
    "ISSUE_CLOSEOUT",
    "CREDENTIAL_CHANGE",
    "SPENDING",
    "DEPLOYMENT",
    "RELEASE",
}
RED_TEAM_ALLOWED_ACTION_CLASSES = {"NONE", "PROMPT_AUTHORING", "EXACT_SHA_REVIEW"}  # scope

NEXT_ACTIONS = {
    "CODEX_DEVELOPER": {"NONE", "IMPLEMENT_ISSUE_55_STAGE_A", "CORRECT_ISSUE_55_PR"},
    "RED_TEAM": {"NONE", "AUTHOR_BOUNDED_DEVELOPER_PROMPT", "REVIEW_EXACT_SHA"},  # scope
    "HUMAN_APPROVER": {"NONE", "REVIEW_FOR_HUMAN_APPROVAL"},
    "MERGE_OPERATOR": {"NONE", "MERGE_AFTER_ALL_GATES"},
}
NEXT_ACTION_FIELDS = {
    "CODEX_DEVELOPER": "DEVELOPER_NEXT_ACTION",
    "RED_TEAM": "RED_TEAM_NEXT_ACTION",
    "HUMAN_APPROVER": "HUMAN_APPROVER_NEXT_ACTION",
    "MERGE_OPERATOR": "MERGE_OPERATOR_NEXT_ACTION",
}

AUTHORITY_FIELDS = (  # scope
    "DEVELOPER_ROLE",
    "REPOSITORY_WRITE_AUTHORITY",  # scope
    "GITHUB_WRITE_AUTHORITY",  # scope
    "TERMINAL_MUTATION_AUTHORITY",  # scope
    "IMPLEMENTATION_AUTHORITY",  # scope
    "PROMPT_AUTHORING_AUTHORITY",  # scope
    "EXACT_SHA_REVIEW_AUTHORITY",  # scope
    "HUMAN_APPROVAL_AUTHORITY",  # scope
    "MERGE_AUTHORITY",  # scope
    "ISSUE_CLOSEOUT_AUTHORITY",  # scope
)
AUTHORITY_PROFILES = {  # scope
    "RED_TEAM": {
        "DEVELOPER_ROLE": "SEPARATE",
        "REPOSITORY_WRITE_AUTHORITY": "NONE",  # scope
        "GITHUB_WRITE_AUTHORITY": "NONE",  # scope
        "TERMINAL_MUTATION_AUTHORITY": "NONE",  # scope
        "IMPLEMENTATION_AUTHORITY": "NO",  # scope
        "PROMPT_AUTHORING_AUTHORITY": "YES",  # scope
        "EXACT_SHA_REVIEW_AUTHORITY": "YES",  # scope
        "HUMAN_APPROVAL_AUTHORITY": "NO",  # scope
        "MERGE_AUTHORITY": "NO",  # scope
        "ISSUE_CLOSEOUT_AUTHORITY": "NO",  # scope
    },
    "CODEX_DEVELOPER": {
        "DEVELOPER_ROLE": "SELF",
        "REPOSITORY_WRITE_AUTHORITY": "BOUNDED",  # scope
        "GITHUB_WRITE_AUTHORITY": "PR_ONLY",  # scope
        "TERMINAL_MUTATION_AUTHORITY": "BOUNDED",  # scope
        "IMPLEMENTATION_AUTHORITY": "YES",  # scope
        "PROMPT_AUTHORING_AUTHORITY": "YES",  # scope
        "EXACT_SHA_REVIEW_AUTHORITY": "NO",  # scope
        "HUMAN_APPROVAL_AUTHORITY": "NO",  # scope
        "MERGE_AUTHORITY": "NO",  # scope
        "ISSUE_CLOSEOUT_AUTHORITY": "NO",  # scope
    },
    "HUMAN_APPROVER": {
        "DEVELOPER_ROLE": "SEPARATE",
        "REPOSITORY_WRITE_AUTHORITY": "NONE",  # scope
        "GITHUB_WRITE_AUTHORITY": "APPROVAL_ONLY",  # scope
        "TERMINAL_MUTATION_AUTHORITY": "NONE",  # scope
        "IMPLEMENTATION_AUTHORITY": "NO",  # scope
        "PROMPT_AUTHORING_AUTHORITY": "NO",  # scope
        "EXACT_SHA_REVIEW_AUTHORITY": "NO",  # scope
        "HUMAN_APPROVAL_AUTHORITY": "YES",  # scope
        "MERGE_AUTHORITY": "NO",  # scope
        "ISSUE_CLOSEOUT_AUTHORITY": "NO",  # scope
    },
    "MERGE_OPERATOR": {
        "DEVELOPER_ROLE": "SEPARATE",
        "REPOSITORY_WRITE_AUTHORITY": "NONE",  # scope
        "GITHUB_WRITE_AUTHORITY": "MERGE_ONLY",  # scope
        "TERMINAL_MUTATION_AUTHORITY": "NONE",  # scope
        "IMPLEMENTATION_AUTHORITY": "NO",  # scope
        "PROMPT_AUTHORING_AUTHORITY": "NO",  # scope
        "EXACT_SHA_REVIEW_AUTHORITY": "NO",  # scope
        "HUMAN_APPROVAL_AUTHORITY": "NO",  # scope
        "MERGE_AUTHORITY": "YES",  # scope
        "ISSUE_CLOSEOUT_AUTHORITY": "NO",  # scope
    },
}

GOVERNING_KEYS = (
    "ACTOR_ROLE",
    "ROLE",
    "REPOSITORY",
    "ISSUE",
    "PULL_REQUEST",
    "BRANCH",
    "EXACT_SHA",
    "LIFECYCLE_STATE",
    "AUTHORITY_SOURCE",  # scope
    "OBSERVATION_TIMESTAMP",
    "PROGRAM_NEXT_ACTION",
    "NEXT_AUTHORIZED_ACTOR",  # scope
    "DEVELOPER_NEXT_ACTION",
    "RED_TEAM_NEXT_ACTION",
    "HUMAN_APPROVER_NEXT_ACTION",
    "MERGE_OPERATOR_NEXT_ACTION",
    "REQUESTED_ACTION_CLASS",
) + AUTHORITY_FIELDS  # scope
EXPECTED_KEYS = (
    "REPOSITORY",
    "ISSUE",
    "PULL_REQUEST",
    "BRANCH",
    "EXACT_SHA",
    "LIFECYCLE_STATE",
    "AUTHORITY_SOURCE",  # scope
    "CURRENT_TIME",
)

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BRANCH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,199}$")
PRIVATE_PATTERNS = (
    re.compile(r"/Users/", re.I),
    re.compile(r"(?:api[_-]?key|access[_-]?token|authorization\s*:|private[_-]?key)", re.I),  # scope
    re.compile(r"(?:chain[_-]?of[_-]?thought|hidden[_-]?reasoning)", re.I),
)
MAX_TEXT_LENGTH = 240
MAX_OBSERVATION_AGE_SECONDS = 3600
MAX_FUTURE_SKEW_SECONDS = 300

REASON_ORDER = (
    "INVALID_CONTRACT_TYPE",
    "DUPLICATE_GOVERNING_FIELD",
    "MISSING_GOVERNING_KEY",
    "UNKNOWN_GOVERNING_KEY",
    "INVALID_EXPECTED_CONTEXT",
    "MISSING_ACTOR_IDENTITY",
    "UNKNOWN_ACTOR_IDENTITY",
    "ROLE_IDENTITY_MISMATCH",
    "INVALID_REPOSITORY_BINDING",
    "INVALID_ISSUE_BINDING",
    "INVALID_PULL_REQUEST_BINDING",
    "INVALID_BRANCH_BINDING",
    "INVALID_EXACT_SHA_BINDING",
    "INVALID_LIFECYCLE_BINDING",
    "MISSING_AUTHORITY_SOURCE",  # scope
    "INVALID_AUTHORITY_SOURCE",  # scope
    "INVALID_OBSERVATION_TIMESTAMP",
    "STALE_OBSERVATION_TIMESTAMP",
    "FUTURE_OBSERVATION_TIMESTAMP",
    "STALE_REPOSITORY_BINDING",
    "STALE_ISSUE_BINDING",
    "STALE_PULL_REQUEST_BINDING",
    "STALE_BRANCH_BINDING",
    "STALE_EXACT_SHA_BINDING",
    "STALE_LIFECYCLE_BINDING",
    "STALE_AUTHORITY_SOURCE_BINDING",  # scope
    "INVALID_PROGRAM_NEXT_ACTION",
    "INVALID_NEXT_AUTHORIZED_ACTOR",  # scope
    "INVALID_ACTOR_NEXT_ACTION",
    "AMBIGUOUS_ACTOR_NEXT_ACTION",
    "PROGRAM_ACTION_IS_NOT_ACTOR_AUTHORITY",  # scope
    "INVALID_REQUESTED_ACTION_CLASS",
    "CONTRADICTORY_DEVELOPER_ROLE",
    "CONTRADICTORY_REPOSITORY_WRITE_AUTHORITY",  # scope
    "CONTRADICTORY_GITHUB_WRITE_AUTHORITY",  # scope
    "CONTRADICTORY_TERMINAL_MUTATION_AUTHORITY",  # scope
    "CONTRADICTORY_IMPLEMENTATION_AUTHORITY",  # scope
    "CONTRADICTORY_PROMPT_AUTHORING_AUTHORITY",  # scope
    "CONTRADICTORY_EXACT_SHA_REVIEW_AUTHORITY",  # scope
    "CONTRADICTORY_HUMAN_APPROVAL_AUTHORITY",  # scope
    "CONTRADICTORY_MERGE_AUTHORITY",  # scope
    "CONTRADICTORY_ISSUE_CLOSEOUT_AUTHORITY",  # scope
    "RED_TEAM_ACTION_NOT_AUTHORIZED",  # scope
    "UNSAFE_PRIVATE_INPUT",
)


def _reason_sort_key(reason: str) -> tuple[int, str]:
    try:
        return REASON_ORDER.index(reason), reason
    except ValueError:
        return len(REASON_ORDER), reason


def _ordered_reasons(reasons: Iterable[str]) -> list[str]:
    return sorted(set(reasons), key=_reason_sort_key)


def _parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value or len(value) > 40:
        return None
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = dt.datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(dt.timezone.utc)


def _unsafe_input(value: Any) -> bool:
    if isinstance(value, str):
        return len(value) > 1000 or any(pattern.search(value) for pattern in PRIVATE_PATTERNS)
    if isinstance(value, Mapping):
        return any(_unsafe_input(key) or _unsafe_input(item) for key, item in value.items())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) > 100 or any(_unsafe_input(item) for item in value)
    return False


def _safe_actor(value: Any) -> str:
    return value if value in ACTORS else "UNKNOWN"


def _safe_context_value(value: Any, allowed: set[str], fallback: str) -> str:
    return value if isinstance(value, str) and value in allowed else fallback


def _incident(contract: Mapping[str, Any]) -> dict[str, Any] | None:
    action = contract.get("REQUESTED_ACTION_CLASS")
    if contract.get("ACTOR_ROLE") != "RED_TEAM" or action in RED_TEAM_ALLOWED_ACTION_CLASSES:
        return None
    if action not in ACTION_CLASSES:
        action = "UNKNOWN"
    return {
        "actor": "RED_TEAM",
        "observation_timestamp": (
            contract.get("OBSERVATION_TIMESTAMP")
            if _parse_time(contract.get("OBSERVATION_TIMESTAMP"))
            else "INVALID"
        ),
        "requested_action_class": action,
        "lifecycle_state": _safe_context_value(
            contract.get("LIFECYCLE_STATE"), LIFECYCLE_STATES, "UNKNOWN"
        ),
        "authority_source": _safe_context_value(  # scope
            contract.get("AUTHORITY_SOURCE"), AUTHORITY_SOURCES, "UNKNOWN"  # scope
        ),
        "result": "DENIED",
        "denial_reasons": ["RED_TEAM_ACTION_NOT_AUTHORIZED"],  # scope
        "required_repair_state": "REPAIR_REQUIRED",
    }


def _result(
    contract: Mapping[str, Any] | None,
    reasons: Iterable[str],
    *,
    repair: bool = False,
) -> dict[str, Any]:
    contract = contract or {}
    ordered = _ordered_reasons(reasons)
    actor = _safe_actor(contract.get("ACTOR_ROLE"))
    conflict = bool(ordered)
    restored = repair and conflict and actor == "RED_TEAM"
    next_actions = {
        actor_name: contract.get(field)
        if contract.get(field) in NEXT_ACTIONS[actor_name]
        else "NONE"
        for actor_name, field in NEXT_ACTION_FIELDS.items()
    }
    effective = dict(AUTHORITY_PROFILES["RED_TEAM"]) if restored else {  # scope
        field: contract.get(field) for field in AUTHORITY_FIELDS  # scope
    }
    return {
        "schema_version": "1.0.0",
        "valid": not conflict,
        "decision": "DENY" if conflict else "ALLOW",
        "actor_role": actor,
        "role_conflict_status": "ROLE_CONFLICT" if conflict else "NORMAL",
        "role_repair_state": (
            "READ_ONLY_ROLE_RESTORED" if restored else "REPAIR_REQUIRED" if conflict else "NORMAL"
        ),
        "reasons": ordered,
        "program_next_action_is_authority": False,  # scope
        "next_authorized_actor": (  # scope
            contract.get("NEXT_AUTHORIZED_ACTOR")  # scope
            if contract.get("NEXT_AUTHORIZED_ACTOR") in NEXT_ACTORS  # scope
            else "NONE"
        ),
        "next_actions": next_actions,
        "effective_authority": effective,  # scope
        "incident": _incident(contract),
        "bounded_claim": {
            "actor_bound_role_contract": "IMPLEMENTED_IN_REVIEW",
            "full_runtime_isolation": "NOT_PROVEN",
            "stage_b_required": "YES",
        },
    }


def _shape_reasons(contract: Any, expected: Any) -> list[str]:
    reasons: list[str] = []
    if not isinstance(contract, Mapping):
        return ["INVALID_CONTRACT_TYPE"]
    keys = set(contract)
    required = set(GOVERNING_KEYS)
    if required - keys:
        reasons.append("MISSING_GOVERNING_KEY")
    if keys - required:
        reasons.append("UNKNOWN_GOVERNING_KEY")
    if not isinstance(expected, Mapping) or set(expected) != set(EXPECTED_KEYS):
        reasons.append("INVALID_EXPECTED_CONTEXT")
    return reasons


def _binding_reasons(contract: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    actor = contract.get("ACTOR_ROLE")
    if actor in {None, ""}:
        reasons.append("MISSING_ACTOR_IDENTITY")
    elif actor not in ACTORS:
        reasons.append("UNKNOWN_ACTOR_IDENTITY")
    if contract.get("ROLE") != actor:
        reasons.append("ROLE_IDENTITY_MISMATCH")

    validators = {
        "REPOSITORY": lambda value: isinstance(value, str) and bool(REPOSITORY_RE.fullmatch(value)),
        "ISSUE": lambda value: type(value) is int and value > 0,
        "PULL_REQUEST": lambda value: type(value) is int and value > 0,
        "BRANCH": lambda value: isinstance(value, str) and bool(BRANCH_RE.fullmatch(value)),
        "EXACT_SHA": lambda value: isinstance(value, str) and bool(SHA_RE.fullmatch(value)),
        "LIFECYCLE_STATE": lambda value: value in LIFECYCLE_STATES,
        "AUTHORITY_SOURCE": lambda value: value in AUTHORITY_SOURCES,  # scope
    }
    invalid_reasons = {
        "REPOSITORY": "INVALID_REPOSITORY_BINDING",
        "ISSUE": "INVALID_ISSUE_BINDING",
        "PULL_REQUEST": "INVALID_PULL_REQUEST_BINDING",
        "BRANCH": "INVALID_BRANCH_BINDING",
        "EXACT_SHA": "INVALID_EXACT_SHA_BINDING",
        "LIFECYCLE_STATE": "INVALID_LIFECYCLE_BINDING",
        "AUTHORITY_SOURCE": "INVALID_AUTHORITY_SOURCE",  # scope
    }
    stale_reasons = {
        "REPOSITORY": "STALE_REPOSITORY_BINDING",
        "ISSUE": "STALE_ISSUE_BINDING",
        "PULL_REQUEST": "STALE_PULL_REQUEST_BINDING",
        "BRANCH": "STALE_BRANCH_BINDING",
        "EXACT_SHA": "STALE_EXACT_SHA_BINDING",
        "LIFECYCLE_STATE": "STALE_LIFECYCLE_BINDING",
        "AUTHORITY_SOURCE": "STALE_AUTHORITY_SOURCE_BINDING",  # scope
    }
    if contract.get("AUTHORITY_SOURCE") in {None, ""}:  # scope
        reasons.append("MISSING_AUTHORITY_SOURCE")  # scope
    for key, validator in validators.items():
        value = contract.get(key)
        if not validator(value):
            reasons.append(invalid_reasons[key])
        elif expected.get(key) != value:
            reasons.append(stale_reasons[key])

    observed = _parse_time(contract.get("OBSERVATION_TIMESTAMP"))
    current = _parse_time(expected.get("CURRENT_TIME"))
    if observed is None:
        reasons.append("INVALID_OBSERVATION_TIMESTAMP")
    if current is None:
        reasons.append("INVALID_EXPECTED_CONTEXT")
    if observed is not None and current is not None:
        age = (current - observed).total_seconds()
        if age > MAX_OBSERVATION_AGE_SECONDS:
            reasons.append("STALE_OBSERVATION_TIMESTAMP")
        if age < -MAX_FUTURE_SKEW_SECONDS:
            reasons.append("FUTURE_OBSERVATION_TIMESTAMP")
    return reasons


def _next_action_reasons(contract: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    program = contract.get("PROGRAM_NEXT_ACTION")
    if not isinstance(program, str) or not program.strip() or len(program) > MAX_TEXT_LENGTH:
        reasons.append("INVALID_PROGRAM_NEXT_ACTION")
    authorized_actor = contract.get("NEXT_AUTHORIZED_ACTOR")  # scope
    if authorized_actor not in NEXT_ACTORS:  # scope
        reasons.append("INVALID_NEXT_AUTHORIZED_ACTOR")  # scope

    non_none: list[str] = []
    for actor, field in NEXT_ACTION_FIELDS.items():
        value = contract.get(field)
        if value not in NEXT_ACTIONS[actor]:
            reasons.append("INVALID_ACTOR_NEXT_ACTION")
        elif value != "NONE":
            non_none.append(actor)
    if authorized_actor == "NONE" and non_none:  # scope
        reasons.append("AMBIGUOUS_ACTOR_NEXT_ACTION")
    if authorized_actor in ACTORS and non_none != [authorized_actor]:  # scope
        reasons.append("AMBIGUOUS_ACTOR_NEXT_ACTION")

    # Program direction is always descriptive.  Repeating it in an actor field is
    # rejected even when the repeated text resembles a permitted action.
    if isinstance(program, str) and any(
        contract.get(field) == program and program != "NONE" for field in NEXT_ACTION_FIELDS.values()
    ):
        reasons.append("PROGRAM_ACTION_IS_NOT_ACTOR_AUTHORITY")  # scope
    action_class = contract.get("REQUESTED_ACTION_CLASS")
    if action_class not in ACTION_CLASSES:
        reasons.append("INVALID_REQUESTED_ACTION_CLASS")
    return reasons


def _authority_reasons(contract: Mapping[str, Any]) -> list[str]:  # scope
    actor = contract.get("ACTOR_ROLE")
    if actor not in AUTHORITY_PROFILES:  # scope
        return []
    reasons: list[str] = []
    for field, expected_value in AUTHORITY_PROFILES[actor].items():  # scope
        if contract.get(field) != expected_value:
            reasons.append(f"CONTRADICTORY_{field}")
    if actor == "RED_TEAM" and contract.get("REQUESTED_ACTION_CLASS") not in RED_TEAM_ALLOWED_ACTION_CLASSES:
        if contract.get("REQUESTED_ACTION_CLASS") in ACTION_CLASSES:
            reasons.append("RED_TEAM_ACTION_NOT_AUTHORIZED")  # scope
    return reasons


def validate_role_contract(
    contract: Mapping[str, Any],
    expected: Mapping[str, Any],
    *,
    repair: bool = False,
) -> dict[str, Any]:
    """Validate one exact actor contract and return a deterministic safe result."""
    shape = _shape_reasons(contract, expected)
    if not isinstance(contract, Mapping):
        return _result(None, shape, repair=repair)
    if _unsafe_input(contract) or _unsafe_input(expected):
        shape.append("UNSAFE_PRIVATE_INPUT")
    if "INVALID_EXPECTED_CONTEXT" in shape or set(contract) != set(GOVERNING_KEYS):
        return _result(contract, shape, repair=repair)
    reasons = shape
    reasons.extend(_binding_reasons(contract, expected))
    reasons.extend(_next_action_reasons(contract))
    reasons.extend(_authority_reasons(contract))  # scope
    return _result(contract, reasons, repair=repair)


def validate_role_contract_pairs(
    pairs: Sequence[Sequence[Any]],
    expected: Mapping[str, Any],
    *,
    repair: bool = False,
) -> dict[str, Any]:
    """Validate ordered pairs while detecting duplicate governing fields."""
    if not isinstance(pairs, Sequence) or isinstance(pairs, (str, bytes, bytearray)):
        return _result(None, ["INVALID_CONTRACT_TYPE"], repair=repair)
    contract: dict[str, Any] = {}
    duplicates = False
    for item in pairs:
        if not isinstance(item, Sequence) or isinstance(item, (str, bytes, bytearray)) or len(item) != 2:
            return _result(contract, ["INVALID_CONTRACT_TYPE"], repair=repair)
        key, value = item
        if not isinstance(key, str):
            return _result(contract, ["INVALID_CONTRACT_TYPE"], repair=repair)
        if key in contract:
            duplicates = True
        else:
            contract[key] = value
    result = validate_role_contract(contract, expected, repair=repair)
    if not duplicates:
        return result
    reasons = ["DUPLICATE_GOVERNING_FIELD", *result["reasons"]]
    return _result(contract, reasons, repair=repair)


def canonical_json(result: Mapping[str, Any]) -> str:
    return json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def red_team_contract(
    *,
    repository: str,
    issue: int,
    pull_request: int,
    branch: str,
    exact_sha: str,
    lifecycle_state: str,
    authority_source: str,  # scope
    observation_timestamp: str,
    program_next_action: str,
    next_authorized_actor: str,  # scope
    developer_next_action: str,
    red_team_next_action: str,
    human_approver_next_action: str,
    merge_operator_next_action: str,
    requested_action_class: str,
) -> dict[str, Any]:
    """Build the exact read-only red-team profile; validation still remains required."""
    contract: dict[str, Any] = {
        "ACTOR_ROLE": "RED_TEAM",
        "ROLE": "RED_TEAM",
        "REPOSITORY": repository,
        "ISSUE": issue,
        "PULL_REQUEST": pull_request,
        "BRANCH": branch,
        "EXACT_SHA": exact_sha,
        "LIFECYCLE_STATE": lifecycle_state,
        "AUTHORITY_SOURCE": authority_source,  # scope
        "OBSERVATION_TIMESTAMP": observation_timestamp,
        "PROGRAM_NEXT_ACTION": program_next_action,
        "NEXT_AUTHORIZED_ACTOR": next_authorized_actor,  # scope
        "DEVELOPER_NEXT_ACTION": developer_next_action,
        "RED_TEAM_NEXT_ACTION": red_team_next_action,
        "HUMAN_APPROVER_NEXT_ACTION": human_approver_next_action,
        "MERGE_OPERATOR_NEXT_ACTION": merge_operator_next_action,
        "REQUESTED_ACTION_CLASS": requested_action_class,
    }
    contract.update(AUTHORITY_PROFILES["RED_TEAM"])  # scope
    return contract


def _self_test() -> dict[str, Any]:
    now = "2026-07-13T12:00:00Z"
    contract = red_team_contract(
        repository="Zest-LeadGen/contractoros-california",
        issue=55,
        pull_request=56,
        branch="stage-a-red-team-role-isolation",
        exact_sha="a" * 40,
        lifecycle_state="EXTERNAL_EXACT_SHA_REVIEW",
        authority_source="GITHUB_ISSUE_55",  # scope
        observation_timestamp=now,
        program_next_action="External exact-SHA review is next.",
        next_authorized_actor="RED_TEAM",  # scope
        developer_next_action="NONE",
        red_team_next_action="REVIEW_EXACT_SHA",
        human_approver_next_action="NONE",
        merge_operator_next_action="NONE",
        requested_action_class="EXACT_SHA_REVIEW",
    )
    expected = {
        key: contract[key] for key in EXPECTED_KEYS if key != "CURRENT_TIME"
    }
    expected["CURRENT_TIME"] = now
    valid = validate_role_contract(contract, expected)
    conflict_contract = dict(contract, REQUESTED_ACTION_CLASS="REPOSITORY_MUTATION")
    conflict = validate_role_contract(conflict_contract, expected)
    repaired = validate_role_contract(conflict_contract, expected, repair=True)
    duplicate = validate_role_contract_pairs([*contract.items(), ("ROLE", "CODEX_DEVELOPER")], expected)
    passed = (
        valid["valid"]
        and conflict["decision"] == "DENY"
        and conflict["incident"] is not None
        and repaired["role_repair_state"] == "READ_ONLY_ROLE_RESTORED"
        and repaired["effective_authority"]["REPOSITORY_WRITE_AUTHORITY"] == "NONE"  # scope
        and "DUPLICATE_GOVERNING_FIELD" in duplicate["reasons"]
        and canonical_json(valid) == canonical_json(validate_role_contract(contract, expected))
    )
    return {"result": "PASS" if passed else "FAIL", "tests": 6}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--repair", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        if args.self_test:
            result = _self_test()
            print(json.dumps(result, sort_keys=True))
            return 0 if result["result"] == "PASS" else 1
        if args.contract is None or args.expected is None:
            raise ValueError("--contract and --expected are required outside self-test mode")
        result = validate_role_contract(_load_json(args.contract), _load_json(args.expected), repair=args.repair)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["valid"] else 5
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        print('{"decision":"DENY","error":"INVALID_INPUT","valid":false}')
        return 5


if __name__ == "__main__":
    sys.exit(main())
