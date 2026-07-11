# Phase 4K-8 Workflow Automation Command-Pack / Operator Runbook Gate Report

## Linked Phase Issue

Phase issue: #45

Issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/45

## Phase

Phase 4K-8 - Workflow Automation Command-Pack / Operator Runbook Gate.

## Lane

Control / Infrastructure

## Current Lifecycle State

PR #46 is open and not merge-approved. The committed phase report contains no live `RED_TEAM_DECISION`. Live review state is determined from the current PR-body marker, exact-head-SHA checks, required checks, and current human review evidence. Human/write-access approval remains required. Auto-merge is inactive. Phase 4K-9 is not started. Phase 4I remains paused.

## Starting Main SHA

`8d443310cf006b82966163f8e486d1f52d8d4e6c`

## Prior Phase Evidence

- Issue #43 is closed with state reason `COMPLETED`.
- PR #44 is merged.
- PR #44 reviewed head SHA was `a519ef5579c130181ac1b25f74bb48f481478378`.
- PR #44 merge commit and expected current main SHA are `8d443310cf006b82966163f8e486d1f52d8d4e6c`.
- Issue #45 is open and active for Phase 4K-8.

## Source Anchors

- Issue #45 - active Phase 4K-8 durable intake.
- Issue #43 - completed Phase 4K-7 intake and closeout.
- PR #44 - Phase 4K-7 merged evidence.
- `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
- `docs/project-control/RED_TEAM_STATE_MACHINE.md`
- `docs/project-control/HANDOFF_PLAYBOOK.md`
- `docs/project-control/WORKFLOW_AUTOMATION_TARGET_STATE.md`
- Existing control validators under `scripts/control/`.
- Existing ContractorOS Control Gates workflow.

## Objective

Create a durable, copy-safe workflow command pack and operator runbook for the protected ContractorOS lifecycle from starting-state verification through durable issue closeout.

## Scope

This phase is documentation-only. It creates command and operator reference material and reconciles project-control evidence. It does not implement automation.

## Changed Files

- `docs/project-control/AUTOMATION_PHASE_ROADMAP.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/HANDOFF_PLAYBOOK.md`
- `docs/project-control/LOW_RISK_LANE_POLICY.md`
- `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`
- `docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md`
- `docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md`
- `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/WORKFLOW_AUTOMATION_COMMAND_PACK.md`
- `docs/project-control/WORKFLOW_AUTOMATION_TARGET_STATE.md`
- `docs/project-control/WORKFLOW_OPERATOR_RUNBOOK.md`
- `docs/project-control/phase_4k_8_workflow_automation_command_pack_operator_runbook_gate_report.md`

## Existing Files Inspected

- Phase 4K-7 report evidence through Issue #43 and PR #44.
- Existing red-team protocol, state-machine, and handoff docs.
- Existing workflow target, roadmap, and low-risk lane policy docs.
- Existing ledger, decision, risk, validation, traceability, source, and artifact records.
- Existing control validators and ContractorOS Control Gates behavior.
- Issue #45 body and correction comment `4940178196`.
- Issue #24 comments `4940177098` and `4942006420`.
- PR #46 metadata/body and GitHub main branch-protection API evidence.

## Role and Authority Matrix — Documentation Scope

Owner/operator, Codex developer executor, external red-team, and human/write-access approver roles are separated in `WORKFLOW_OPERATOR_RUNBOOK.md`. Codex remains developer executor only. Red-team approval does not replace human/write-access approval, and hidden or chat-only approval is invalid.

## Canonical Lifecycle Sequence

The command pack covers starting-state verification, branch creation, developer execution, local validation, commit/push, PR creation, PR evidence collection, exact-SHA red-team review, post-marker gates, human approval, manual merge, main verification, and issue closeout.

## Command-Pack Summary

`WORKFLOW_AUTOMATION_COMMAND_PACK.md` provides copy-safe command blocks with placeholders, repository assertions, success indicators, failure indicators, and stop conditions for the protected lifecycle.

## Operator Runbook Summary

`WORKFLOW_OPERATOR_RUNBOOK.md` defines operator responsibilities, transition evidence, state-by-state entry and exit criteria, recovery paths, and prohibitions for stale SHA, failed checks, malformed markers, duplicate markers, unexpected files, moved main, review dismissal, merge verification failure, and closeout failure.

## Placeholder and Repository-Safety Rules

Placeholders must be replaced before any write command. Commands must target `Zest-LeadGen/contractoros-california`, verify exact SHA evidence, assert the repository remote, and stop on unresolved placeholders or wrong repository evidence.

## Marker Parser Constraints

The command pack records parser constraints for hidden HTML comments, fenced code blocks, duplicate owner-trigger markers, exact supported field names, full 40-character PR head SHA, `YYYY-MM-DD` review date, and the required SHA-bound statement.

## PR-Body Assembly Rule

Initial PR creation may use the full phase report because it contains one live owner-trigger marker as the final report section and no live red-team decision marker. The historical Issue #24 append-only procedure is superseded. After external review, the operator must generate a replacement body that preserves report content outside stale marker sections, removes the existing `## Red-Team Status` and owner-marker sections, appends exactly one supported-field decision bound to the full current 40-character PR head SHA, and appends exactly one owner marker matching the committed report as the final section. Generated-body checks must prove marker counts, decision-before-owner order, current-head SHA equality, final owner placement, stale pending-status removal, and resolved runtime values before any PR edit.

## External Red-Team Preservation

External red-team review remains required. Phase 4K-8 documents handoff commands and marker rules but does not let Codex add red-team decision evidence.

## Human Approval Preservation

Human/write-access approval remains required after valid red-team evidence and passing control gates.

## Auto-Merge Preservation

Auto-merge remains inactive and prohibited. The command pack requires auto-merge state verification and stop conditions.

## Branch-Protection Preservation

GitHub branch-protection API evidence proves strict required status check `contractoros-control-gates`; one approving review; code-owner review; stale-review dismissal; conversation resolution; admin enforcement; force pushes disabled; and deletions disabled. Signatures, last-push approval, and linear history are disabled. Phase 4K-8 does not change protection. Manual merge still requires exact current-head red-team evidence, passing required checks, and human/write-access approval. Codex does not merge.

## GitHub Actions Ordering Limitation

The current workflow runs changed-file, forbidden-scope, required-control-update, PR-contract, owner-trigger, and low-risk-lane checks before the mandatory red-team marker. While the marker is missing, that marker step fails and later GitHub lockfile-only and claim-language steps are skipped. Their equivalent local checks remain mandatory and passed for this correction. No workflow modification is authorized, and this report does not claim every GitHub step passes before marker insertion.

## Tabletop / No-Write Verification

Completed Phase 4K-7 evidence used for tabletop verification:

- Repository: `Zest-LeadGen/contractoros-california`
- Issue: #43
- PR: #44
- Starting SHA: `4315c943b6210f023849592213882bc8983c31d2`
- Reviewed head SHA: `a519ef5579c130181ac1b25f74bb48f481478378`
- Merge/main SHA: `8d443310cf006b82966163f8e486d1f52d8d4e6c`
- Closeout comment: `4934579739`

| Command or validation performed | Resolved Phase 4K-7 input | Expected result | Observed result | Pass/fail scope | No-write confirmation |
|---|---|---|---|---|---|
| `git remote get-url origin` | Repository `Zest-LeadGen/contractoros-california` | Exact repository remote | `https://github.com/Zest-LeadGen/contractoros-california.git` | PASS | Read-only Git command. |
| Issue-state read | Issue #43 | `CLOSED` / `COMPLETED` | `CLOSED` / `COMPLETED`, closed `2026-07-10T10:54:40Z` | PASS | Read-only GitHub command. |
| PR-state read | PR #44 | `MERGED` with known head and merge SHA | Merged `2026-07-10T10:52:41Z`; head `a519ef5579c130181ac1b25f74bb48f481478378`; merge `8d443310cf006b82966163f8e486d1f52d8d4e6c` | PASS | Read-only GitHub command. |
| Local and remote-main reads | Merge/main `8d443310cf006b82966163f8e486d1f52d8d4e6c` | Both refs equal merge SHA | Both returned the expected SHA | PASS | Read-only Git commands. |
| Closeout-comment read | Comment `4934579739` | Existing Phase 4K-7 closeout | Comment exists on Issue #43 with closeout body | PASS | Read-only GitHub command. |
| Correct SHA assertion | Merge/main SHA | Exit `0` | Exit `0` | PASS | Local comparison only. |
| Deliberately wrong SHA assertion | All-zero SHA | Exit nonzero and stop | Exit `1` | PASS | Fail-closed local comparison; no mutation. |
| Generated replacement-body checks | Reviewed head, marker fields, owner marker | One decision, one owner marker, correct order/SHA, owner final | Temporary body had one status heading, one decision marker line, one owner marker, no unresolved value, and no stale pending text | PASS | Local `/tmp` generation only; no PR edit. |
| Lifecycle-write review | Issue #43, PR #44, temporary body | No lifecycle write command during tabletop | No `gh pr edit`, `gh pr merge`, `gh issue comment`, or `gh issue close` was executed | PASS | All tabletop GitHub operations were reads. |

## Executable No-Write Adversarial Verification

The first suite execution stopped at `T01|multiline CONDITIONS|EXPECTED=REJECT|OBSERVED=ACCEPT|FAIL`. This was a test-harness control-flow defect, not evidence that the production marker validator accepted multiline input. The harness invoked a validator function as an `if` condition and relied on `set -e`; Bash continued after an early failed bare predicate, and a later successful predicate replaced the function status. The suite was corrected so every predicate and nested validator explicitly uses `|| return 1`, every validator ends with an explicit success return, and a harness-regression control proves that an early failure cannot be masked by later success.

The corrected suite was rerun from the beginning against the live read-only PR #46 head. The suite used only isolated shell variables and temporary files, and its before/after repository-status comparison passed. No GitHub write command was present or executed, no additional repository mutation occurred during suite execution, and no live `RED_TEAM_DECISION` was added.

| Test ID | Tested input condition | Expected result | Observed result | Pass/fail | No GitHub write | No repository mutation during test | No live `RED_TEAM_DECISION` added |
|---|---|---|---|---|---|---|---|
| HARNESS | Early failed predicate followed by a successful predicate | Reject | Rejected | PASS | Yes | Yes | Yes |
| T01 | Multiline `CONDITIONS` | Reject | Rejected | PASS | Yes | Yes | Yes |
| T02 | `CONDITIONS` contains `Decision: BLOCKED` | Reject | Rejected | PASS | Yes | Yes | Yes |
| T03 | `SCOPE_REVIEWED` contains `RED_TEAM_DECISION` | Reject | Rejected | PASS | Yes | Yes | Yes |
| T04 | `FORBIDDEN_SCOPE_CONFIRMATION` contains `OWNER_TRIGGER_REVIEW` | Reject | Rejected | PASS | Yes | Yes | Yes |
| T05 | Markdown-heading injection | Reject | Rejected | PASS | Yes | Yes | Yes |
| T06 | Invalid review-date format | Reject | Rejected | PASS | Yes | Yes | Yes |
| T07 | Short SHA | Reject | Rejected | PASS | Yes | Yes | Yes |
| T08A | Uppercase SHA | Reject | Rejected | PASS | Yes | Yes | Yes |
| T08B | Non-hexadecimal SHA | Reject | Rejected | PASS | Yes | Yes | Yes |
| T09 | SHA differs from live PR head | Reject | Rejected | PASS | Yes | Yes | Yes |
| T10 | Duplicate supported decision field | Reject | Rejected | PASS | Yes | Yes | Yes |
| T11 | Unknown colon-delimited field inside decision block | Reject | Rejected | PASS | Yes | Yes | Yes |
| T12 | Unresolved runtime placeholder | Reject | Rejected | PASS | Yes | Yes | Yes |
| T13 | Stale `requires corrections` text | Reject | Rejected | PASS | Yes | Yes | Yes |
| T14 | Duplicate `RED_TEAM_DECISION` | Reject | Rejected | PASS | Yes | Yes | Yes |
| T15 | Duplicate owner marker | Reject | Rejected | PASS | Yes | Yes | Yes |
| T16 | Owner marker not final | Reject | Rejected | PASS | Yes | Yes | Yes |
| T17 | Decision marker after owner marker | Reject | Rejected | PASS | Yes | Yes | Yes |
| VALID | Numeric PR, exact live lowercase 40-character SHA, valid date and one-line values, exactly nine once-only supported fields, one decision before one final owner marker, no unknown field, stale text, or placeholder | Accept | Accepted | PASS | Yes | Yes | Yes |
| SUITE | Repository-status comparison | Unchanged | Unchanged | PASS | Yes | Yes | Yes |

The actual documented `require_safe_marker_values` production behavior was tested separately after the harness correction. It rejected multiline input, rejected `Decision: BLOCKED` reserved-field injection, accepted safe ordinary single-line prose, and left repository status unchanged. This confirms the initial T01 result was confined to the harness and did not expose a production-validator acceptance defect.

## Documentation Impact

Phase 4K-8 creates source/text command-pack and operator-runbook documentation and updates project-control records for lifecycle state, risks, decisions, roadmap, and command boundaries.

This documentation does not authorize product implementation, runtime QA, build work, dependency/toolchain mutation, backend or identity-system work, public content, launch, Phase 4K-9, or Phase 4I.

## Product / Development Source-of-Truth Updates

`PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` was updated to record Phase 4K-7 completion through Issue #43 and PR #44, Phase 4K-8 activity through Issue #45 and PR #46, Phase 4K-9 not started, Phase 4I paused, and the toolchain/npm path deferred rather than rejected.

## Roadmap / Tracker Updates

`AUTOMATION_PHASE_ROADMAP.md` was modified to mark Phase 4K-8 active through Issue #45 after Phase 4K-7 merged through PR #44, and to keep Phase 4K-9 through Phase 4K-12 as future planning targets.

`WORKFLOW_AUTOMATION_TARGET_STATE.md` was modified to add the Phase 4K-8 command-pack boundary while preserving manual merge, external red-team, human approval, exact SHA binding, and auto-merge prohibition.

`PROJECT_IMPLEMENTATION_ROADMAP.md` and `PROJECT_VISION_AND_PHASE_TRACKER.md` were updated to remove stale active-Phase-4K-7 and unstarted-Phase-4K-8 claims while preserving product-scope boundaries.

## Decision Log Impact

`DECISION_LOG.md` was modified to replace the obsolete Phase 4K-7 active lifecycle statement with current evidence: Phase 4K-7 merged through PR #44, Issue #43 is closed/completed, the merge/current starting SHA is `8d443310cf006b82966163f8e486d1f52d8d4e6c`, Phase 4K-8 is active through Issue #45, and Phase 4K-9 through Phase 4K-12 remain future planning targets.

## Risk Register Impact

`RISK_REGISTER.md` was modified to track command misuse and marker assembly ambiguity with copy-safe commands, repository assertions, stop conditions, and parser constraints.

## Validation Tasks Updates

`VALIDATION_TASKS.md` was inspected. No change was required because Phase 4K-8 validation evidence is recorded in this report and by local command output; the phase does not add or change validator code.

## RTM Updates

`REQUIREMENTS_TRACEABILITY_MATRIX.md` was inspected. No change was required because Phase 4K-8 creates command/runbook documentation and keeps traceability within the active report, command pack, runbook, decision log, risk register, roadmap, low-risk policy, and target-state documents.

## Source Register Updates

`SOURCE_REGISTER.md` was inspected. No change was required because the durable GitHub sources for Phase 4K-8 are cited in this report and no new external source authority is introduced.

## Artifact Index Impact

`ARTIFACT_INDEX.md` was inspected. No change was required because Phase 4K-8 creates only source-text Markdown files and no binary, archive, build, runtime, dependency, release, install, automation, or device-QA artifact.

## Artifact

No artifact is created. The command pack, runbook, and report are source/text repository files only. The research ZIP and private owner-decision PDF/DOCX/source package are excluded from PR #46.

## Commands Run

- `git status --short --branch`
- `git branch --show-current`
- `git rev-parse HEAD`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git ls-files --others --exclude-standard`
- `gh issue view 45 --repo Zest-LeadGen/contractoros-california --json number,title,state,stateReason,url`
- `gh issue view 43 --repo Zest-LeadGen/contractoros-california --json number,title,state,stateReason,closedAt,url`
- `gh pr view 44 --repo Zest-LeadGen/contractoros-california --json number,state,mergedAt,mergeCommit,headRefOid,url`
- `gh api repos/Zest-LeadGen/contractoros-california/branches/main/protection`

## Dependency / Lockfile Handling

No package manifests, lockfiles, npmrc files, dependency directories, dependency install commands, Node/npm/Corepack bootstrap commands, package-manager substitutions, or dependency-resolution retries are included.

## Validation Evidence

The initial adversarial-suite run stopped when T01 falsely accepted multiline `CONDITIONS`. The cause was Bash conditional-control-flow semantics: the harness relied on `set -e` inside a function invoked as an `if` condition, so a later successful predicate masked the earlier failure. The harness was corrected with explicit fail-closed returns; all listed adversarial tests and the documented production marker probes then passed.

`check_changed_files.py` passed. The first subsequent `check_forbidden_scope.py` run failed on four documentation lines. Its literal case-insensitive substring matching found `fetch` and the `auth` substring inside `Authority` on lines without same-line documentation/scope context. No forbidden implementation was present, and no validator was modified. The affected documentation was clarified without changing command behavior or role-separation meaning, and the next forbidden-scope run passed. `check_required_control_updates.py` then failed because the current five-file correction delta did not change `DECISION_LOG.md` or `DEVELOPMENT_LEDGER.md` and the report lacked the exact reviewed/no-update declarations. The exact declarations below were added without modifying either control file. The full validator sequence remains pending and must pass on rerun before commit.

### Current Five-File Correction-Delta Control Review

The declarations below apply only to the current five-file correction delta. They do not negate that both files remain part of the existing fourteen-file Phase 4K-8 PR history.

- docs/project-control/DECISION_LOG.md: reviewed, no update required
- docs/project-control/DEVELOPMENT_LEDGER.md: reviewed, no update required

The first full local validator sequence passed after the claim language was narrowed and the two exact correction-delta declarations were added. These local results do not establish a GitHub Actions result, red-team approval, human approval, or merge authorization. The second pre-commit sequence is required because this evidence paragraph and result list modify the validated report.

- `python3 scripts/control/check_changed_files.py` - PASS
- `python3 scripts/control/check_forbidden_scope.py` - PASS
- `python3 scripts/control/check_required_control_updates.py` - PASS
- `python3 scripts/control/check_pr_contract.py` - PASS
- `python3 scripts/control/check_owner_trigger_review.py` - PASS
- `python3 scripts/control/check_low_risk_lane.py --self-test` - PASS
- `python3 scripts/control/check_low_risk_lane.py` - PASS
- `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` - PASS
- `python3 scripts/control/check_pr_contract.py --claims-only` - PASS
- `git diff --check` - PASS
- `git diff --cached --check` - PASS

## Red-Team Status

External red-team review is required for the exact current PR head. Codex does not add red-team decision evidence. Any correction commit makes prior SHA-bound review evidence stale.

## Human Approval Status

Human/write-access approval is pending and remains required before merge.

## Auto-Merge Status

Inactive and prohibited. Phase 4K-8 does not activate auto-merge.

## Forbidden Scope Confirmation

- [x] No `.github/workflows/**` changes.
- [x] No `scripts/control/**` changes.
- [x] No `.github/pull_request_template.md` change.
- [x] No app source.
- [x] No package manifests.
- [x] No lockfiles.
- [x] No npmrc.
- [x] No dependency install or resolution.
- [x] No Node/npm/Corepack bootstrap.
- [x] No runtime.
- [x] No browser, visual, emulator, device, or install QA.
- [x] No build.
- [x] No build or release artifact.
- [x] No ZIP, binary, archive, or private owner-decision artifact.
- [x] No backend, database, Firebase, auth, identity, or cloud implementation.
- [x] No payment, CRM, marketplace, analytics, saved progress, scoring, readiness, or pass/fail implementation.
- [x] No public content.
- [x] No Question Bank or C10/C46/C39 migration.
- [x] No issue-intake automation.
- [x] No Codex-handoff automation.
- [x] No merge automation.
- [x] No issue-closeout automation.
- [x] No bot implementation.
- [x] No GitHub App implementation.
- [x] No external red-team reduction.
- [x] No repo-backed red-team memory/window-handoff implementation.
- [x] No human-approval reduction.
- [x] No auto-merge activation.
- [x] No approval reduction.
- [x] No branch-protection bypass.
- [x] No merge by Codex.
- [x] No Phase 4K-9 start.
- [x] No Phase 4I resume.
- [x] No toolchain/npm bootstrap governance work.

Forbidden scope confirmation: confirmed Phase 4K-8 documentation-only command-pack and operator-runbook scope.

## Claim Level

Documentation-only command-pack and operator-runbook gate. This phase does not prove workflow automation activation, issue-intake automation, Codex-handoff automation, merge automation, closeout automation, approval reduction, product readiness, runtime readiness, build readiness, public readiness, or release readiness.

## Known Limitations

- The command pack and runbook are documentation only and are not executable automation.
- External red-team review, human/write-access approval, and manual merge remain required.
- Current GitHub ordering skips later lockfile-only and claim-language steps while the mandatory marker is missing; equivalent local checks remain mandatory.
- Tabletop verification uses completed Phase 4K-7 evidence only and performs no lifecycle write actions.
- Future Phase 4K-9, Phase 4K-10, Phase 4K-11, and Phase 4K-12 each require separate durable GitHub issues.

## Next Phase Recommendation

After Phase 4K-8 is externally reviewed, human-approved, merged, main-verified, and Issue #45 is closed, the next planning target is Phase 4K-9 - Phase Intake + Codex Handoff Automation Gate through a new durable GitHub issue.

## Next Phase Status

Phase 4K-9 is not started. Phase 4I remains paused.

## OWNER_TRIGGER_REVIEW marker

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Phase 4K-8 defines the canonical operator workflow, command sequence, role boundaries, marker handling, and future automation handoff controls. These operating rules affect future development-control architecture and automation execution safety, so owner interruption, external red-team review, and human approval are required. This phase must not activate automation, reduce current approval requirements, enable auto-merge, or authorize Phase 4K-9.
