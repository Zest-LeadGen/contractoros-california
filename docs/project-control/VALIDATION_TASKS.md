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
| VAL-4J0-010 | Verify local GitHub authentication before push. | `git push --no-verify -u origin phase-4j-0-codex-operating-model` only after credentials are available | Push can authenticate without interactive username failure. | Mitigated by owner GitHub CLI authentication for documentation PR setup. |
| VAL-4J0-011 | Verify branch exists on GitHub after push. | GitHub branch view or direct GitHub branch check | `phase-4j-0-codex-operating-model` exists on GitHub at the expected head SHA. | Passed for initial PR branch; verify again after correction push. |
| VAL-4J0-012 | Verify PR exists. | GitHub PR view or direct PR check | PR exists into `main` with the required title and body. | Passed; PR #15 exists. |
| VAL-4J0-013 | Verify GitHub Actions workflow passes. | GitHub Actions status on the PR head SHA | Required workflow checks pass for the pushed branch. | Pending after correction push. |
| VAL-4J0-014 | Verify PR evidence matches local report. | Compare PR body with `docs/project-control/phase_4j_0_codex_operating_model_report.md` | PR body does not imply push or PR creation succeeded before it did. | Pending until PR #15 body is updated with the corrected report. |
| VAL-4J0-015 | Verify post-merge main state after approval/merge. | GitHub main SHA/file verification | Main contains the approved Phase 4J-0 governance docs after merge. | Pending until red-team review, approval, and merge. |
| VAL-4J0-016 | Verify future prompts include model/effort header. | Prompt review against `docs/project-control/PROMPT_CONVENTION.md` | Prompt begins with the required model/effort header. | Active after Phase 4J-0 merge. |
| VAL-4J0-017 | Verify `PROMPT_CONVENTION.md` exists and is referenced by `AGENTS.md`. | File review | `docs/project-control/PROMPT_CONVENTION.md` exists and `AGENTS.md` points to it. | Passed in local documentation review. |
| VAL-4J0-018 | Verify xhigh/Extra High caveat is documented. | File review | `PROMPT_CONVENTION.md`, `SOURCE_REGISTER.md`, and `ASSUMPTION_REGISTER.md` avoid claiming official UI mapping. | Passed in local documentation review. |
| VAL-4J0-019 | Verify prompt convention does not activate auto-merge or product scope. | File review and forbidden-scope scan | Convention is documentation/control only and does not authorize auto-merge or product scope. | Passed in local validation. |

## Task Rule

Validation task status must be updated by repo evidence, not memory.

## Phase 4J-1 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J1-001 | Verify phase issue template exists. | File review of `.github/ISSUE_TEMPLATE/phase_issue.yml` | Template captures required phase intake fields. | Pending local validation. |
| VAL-4J1-002 | Verify PR template requires linked issue evidence. | File review of `.github/pull_request_template.md` | Template requires linked phase issue and phase evidence sections. | Pending local validation. |
| VAL-4J1-003 | Verify PR contract enforces issue reference in PR context. | `scripts/control/check_pr_contract.py` review and GitHub Actions after PR open | PR body without accepted issue reference fails. | Pending workflow validation after PR open. |
| VAL-4J1-004 | Verify existing local control checks pass. | Phase 4J-1 validation command set | Local checks pass before commit. | Pending local validation. |
| VAL-4J1-005 | Verify Phase 4J-1 PR links a GitHub phase issue. | PR body review | PR body includes accepted issue reference. | Blocked until owner creates the Phase 4J-1 issue. |
| VAL-4J1-006 | Verify no auto-merge or product scope is activated. | Forbidden-scope scan and file review | Control-only files changed; auto-merge remains inactive. | Pending local validation. |
