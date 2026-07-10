# Phase 4K-8 Workflow Automation Command-Pack / Operator Runbook Gate Report

## Linked Phase Issue

Phase issue: #45

Issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/45

## Phase

Phase 4K-8 - Workflow Automation Command-Pack / Operator Runbook Gate.

## Lane

Control / Infrastructure

## Current Lifecycle State

Developer execution in progress. The phase is not merge-approved, and Phase 4K-9 is not started.

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
- `docs/project-control/LOW_RISK_LANE_POLICY.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/WORKFLOW_AUTOMATION_TARGET_STATE.md`
- `docs/project-control/WORKFLOW_AUTOMATION_COMMAND_PACK.md`
- `docs/project-control/WORKFLOW_OPERATOR_RUNBOOK.md`
- `docs/project-control/phase_4k_8_workflow_automation_command_pack_operator_runbook_gate_report.md`

## Existing Files Inspected

- Phase 4K-7 report evidence through Issue #43 and PR #44.
- Existing red-team protocol, state-machine, and handoff docs.
- Existing workflow target, roadmap, and low-risk lane policy docs.
- Existing ledger, decision, risk, validation, traceability, source, and artifact records.
- Existing control validators and ContractorOS Control Gates behavior.

## Role And Permission Matrix

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

Initial PR creation may use the full phase report because it contains one live owner-trigger marker as the final report section and no live red-team decision marker. After external review, the operator must copy report content only up to the owner-trigger heading, append exactly one live red-team decision, append exactly one live owner-trigger marker matching the committed report marker, and ensure no later `Rationale:` or colon-delimited evidence appears after the final owner marker.

## External Red-Team Preservation

External red-team review remains required. Phase 4K-8 documents handoff commands and marker rules but does not let Codex add red-team decision evidence.

## Human Approval Preservation

Human/write-access approval remains required after valid red-team evidence and passing control gates.

## Auto-Merge Preservation

Auto-merge remains inactive and prohibited. The command pack requires auto-merge state verification and stop conditions.

## Branch-Protection Preservation

Manual merge remains protected by required checks, exact current head SHA, external red-team evidence, and human approval. Codex does not merge.

## Tabletop / No-Write Verification

Completed Phase 4K-7 evidence resolves placeholders unambiguously:

- Issue #43
- PR #44
- Starting SHA `4315c943b6210f023849592213882bc8983c31d2`
- Reviewed head SHA `a519ef5579c130181ac1b25f74bb48f481478378`
- Merge/main SHA `8d443310cf006b82966163f8e486d1f52d8d4e6c`
- Closeout comment `4934579739`

The tabletop verifies that commands target the correct repository, exact SHA checks fail closed, marker assembly avoids duplicate-rationale conflicts, manual merge verification requires the reviewed SHA, and closeout verification identifies Issue #43 as `CLOSED` / `COMPLETED`.

No lifecycle write command is executed during tabletop verification. Only this Phase 4K-8 documentation work is changed.

## Documentation Impact

Phase 4K-8 creates source/text command-pack and operator-runbook documentation and updates project-control records for lifecycle state, risks, decisions, roadmap, and command boundaries.

This documentation does not authorize product implementation, runtime QA, build work, dependency/toolchain mutation, backend or identity-system work, public content, launch, Phase 4K-9, or Phase 4I.

## Product / Development Source-of-Truth Updates

`PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` was inspected. No change was required because the existing product-development authority remains blocked for product, runtime, build, dependency, and Phase 4I scope, and Phase 4K-8 adds only workflow command documentation.

## Roadmap / Tracker Updates

`AUTOMATION_PHASE_ROADMAP.md` was modified to mark Phase 4K-8 active through Issue #45 after Phase 4K-7 merged through PR #44, and to keep Phase 4K-9 through Phase 4K-12 as future planning targets.

`WORKFLOW_AUTOMATION_TARGET_STATE.md` was modified to add the Phase 4K-8 command-pack boundary while preserving manual merge, external red-team, human approval, exact SHA binding, and auto-merge prohibition.

`PROJECT_IMPLEMENTATION_ROADMAP.md` and `PROJECT_VISION_AND_PHASE_TRACKER.md` were inspected. No change was required for this nine-file correction because Phase 4K-8 does not change product implementation sequencing or active product scope.

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

No artifact is created. The new command pack, runbook, and report are source/text repository files only.

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

## Dependency / Lockfile Handling

No package manifests, lockfiles, npmrc files, dependency directories, dependency install commands, Node/npm/Corepack bootstrap commands, package-manager substitutions, or dependency-resolution retries are included.

## Validation Evidence

Local validations passed before commit:

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

External red-team review is pending. Codex does not add red-team decision evidence.

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
- [x] No backend, database, Firebase, auth, identity, or cloud implementation.
- [x] No payment, CRM, marketplace, analytics, saved progress, scoring, readiness, or pass/fail implementation.
- [x] No public content.
- [x] No Question Bank or C10/C46/C39 migration.
- [x] No issue-intake automation.
- [x] No Codex-handoff automation.
- [x] No merge automation.
- [x] No issue-closeout automation.
- [x] No bot implementation.
- [x] No auto-merge activation.
- [x] No approval reduction.
- [x] No branch-protection bypass.
- [x] No merge by Codex.
- [x] No Phase 4K-9 start.
- [x] No Phase 4I resume.

Forbidden scope confirmation: confirmed Phase 4K-8 documentation-only command-pack and operator-runbook scope.

## Claim Level

Documentation-only command-pack and operator-runbook gate. This phase does not prove workflow automation activation, issue-intake automation, Codex-handoff automation, merge automation, closeout automation, approval reduction, product readiness, runtime readiness, build readiness, public readiness, or release readiness.

## Known Limitations

- The command pack and runbook are documentation only and are not executable automation.
- External red-team review, human/write-access approval, and manual merge remain required.
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
