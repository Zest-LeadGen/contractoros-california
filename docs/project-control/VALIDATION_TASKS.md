# Validation Tasks

Purpose: record validation tasks for ContractorOS California governance and phase-control work.

## Phase 4J-0 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J0-001 | Confirm changed files remain inside the Phase 4J-0 allowlist. | `git diff --name-only origin/main...HEAD` | Only the 14 allowed files are changed. | Passed in pre-PR validation; post-commit diff must match the PR evidence. |
| VAL-4J0-002 | Run changed-file lane check. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, or product lane file is changed. | Passed in local validation. |
| VAL-4J0-003 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside explicit exclusions. | Passed in local validation. |
| VAL-4J0-004 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4J-0 report and required control updates are present. | Passed in local validation. |
| VAL-4J0-005 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections are present. | Passed in local validation. |
| VAL-4J0-006 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no lockfile is added or changed. | Passed in local validation. |
| VAL-4J0-007 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported readiness, release, or completion claim is made. | Passed in local validation. |
| VAL-4J0-008 | Confirm no `/init`, broad discovery, `api_tool.list_resources`, or cockroachdb hook use. | Model run log and command history review | Confirmed in PR evidence. | Passed in local validation. |
| VAL-4J0-009 | Confirm future Phase 4J-2 red-team SHA artifact requirement is versioned. | Review `CONTRACTOROS_DESIGN_DECISIONS.md` and `REQUIREMENTS_TRACEABILITY_MATRIX.md` | Requirement is documented, not implemented in Phase 4J-0. | Passed in local validation. |

## Task Rule

Validation task status must be updated by repo evidence, not memory.
