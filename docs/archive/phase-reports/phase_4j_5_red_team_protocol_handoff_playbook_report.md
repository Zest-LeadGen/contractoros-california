# Phase 4J-5 Red-Team Operating Protocol + Handoff Playbook Report

## Linked Phase Issue

Phase issue: #25

## Phase

Phase 4J-5 — Red-Team Operating Protocol + Handoff Playbook

## Lane

Control / Infrastructure

## Phase Issue

#25

## Linked Phase Issue URL

https://github.com/Zest-LeadGen/contractoros-california/issues/25

## Source Anchors

- Issue #25: Phase 4J-5 durable phase intake.
- Issue #24: red-team handoff and memory reconciliation anchor.
- Issue #24 Red-Team Operating Protocol Addendum: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4923968200
- Issue #24 CLI Expected Output Requirement: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4924223781
- Issue #24 Progress Snapshot Requirement: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4924313115
- Issue #24 Operator State Machine Addendum: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4924596374

## Starting Main SHA

b01cd5829621c20f6bd837a9d570553a6a408573

## Scope

This phase converts Issue #24 protocol material and Issue #25 phase requirements into committed project-control documentation.

Scope is limited to control/infrastructure documentation and governance registers.

## Changed Files

- `AGENTS.md`
- `docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md`
- `docs/project-control/ARTIFACT_INDEX.md`
- `docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/HANDOFF_PLAYBOOK.md`
- `docs/project-control/MODEL_RUN_LOG.md`
- `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
- `docs/project-control/RED_TEAM_STATE_MACHINE.md`
- `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/SOURCE_REGISTER.md`
- `docs/project-control/VALIDATION_TASKS.md`
- `docs/project-control/phase_4j_5_red_team_protocol_handoff_playbook_report.md`

## Commands Run

Pre-edit checks:

- `git rev-parse origin/main` — passed; returned `b01cd5829621c20f6bd837a9d570553a6a408573`.
- `git status --short --branch` — passed; clean `main` before edits.
- `git switch -c phase-4j-5-red-team-protocol-handoff-playbook` — passed.

Source evidence reads:

- `gh api repos/Zest-LeadGen/contractoros-california/issues/24/comments --jq ...` — passed; returned the exact Issue #24 addenda named by the phase prompt.
- `gh api repos/Zest-LeadGen/contractoros-california/issues/25 --jq ...` — passed; returned the Phase 4J-5 issue body.
- `gh api repos/Zest-LeadGen/contractoros-california/issues/24 --jq ...` — passed; returned the Issue #24 handoff anchor body.

Local validation commands required for this phase:

- `python3 scripts/control/check_changed_files.py` — passed.
- `python3 scripts/control/check_forbidden_scope.py` — initially failed on progress-snapshot category lines that lacked explicit claim downgrade wording; passed after adding claim downgrade wording while preserving baseline values.
- `python3 scripts/control/check_required_control_updates.py` — passed.
- `python3 scripts/control/check_pr_contract.py` — passed.
- `python3 scripts/control/check_owner_trigger_review.py` — passed.
- `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` — passed.
- `python3 scripts/control/check_pr_contract.py --claims-only` — passed.
- `git diff --check` — passed.

No npm, Expo, EAS, Android, iOS, native build, backend, database, dependency install, deployment, or lockfile generation command was run.

## Dependency / Lockfile Handling

No dependency files or lockfiles are changed.

No dependency install command was run.

## Documentation Impact

`RED_TEAM_OPERATING_PROTOCOL.md` now records durable red-team source-of-truth, evidence, role-boundary, command-guidance, progress-snapshot, marker, and process-prohibition rules.

`RED_TEAM_STATE_MACHINE.md` now records the lifecycle states, required evidence, allowed next actions, stop conditions, forbidden actions, stale SHA handling, failed-check handling, missing-human-approval handling, merged-but-not-main-verified handling, and ready-for-next-phase handling.

`HANDOFF_PLAYBOOK.md` now records the future red-team startup sequence, evidence checks, command-block expectations, handoff summary template, progress snapshot template, closeout sequence, and prohibited handoff behavior.

`AGENTS.md` and `AI_DEVELOPMENT_OPERATING_MODEL.md` now point future agents to the durable protocol docs.

## Protocol Content Mapping

The committed protocol docs preserve:

- GitHub as source of truth.
- Chat memory, sandbox state, local scratch files, connector state, and unversioned notes as not source of truth.
- Durable evidence requirements for decisions, approvals, rejections, conditions, assumptions, scope boundaries, and handoff states.
- `not proven` status for missing evidence.
- `blocked` status for insufficient evidence.
- Lifecycle state classification before next steps.
- CLI expected-output, failure-indicator, stop-condition, and next-action requirements.
- Progress snapshot requirement and Phase 4J-4 baseline.
- Codex developer-executor-only role boundary.
- Separate red-team review and human/write-access approval requirements.
- Auto-merge inactive status.
- No merge and no branch-protection bypass.
- No approval when the exact current PR head SHA is unknown.
- No next-phase start until prior phase post-merge verification and issue closeout.
- No paused-phase resume without explicit authorization.

## Progress Snapshot Baseline

Current baseline after Phase 4J-4:

| Area | Governance estimate |
|---|---|
| Governance/control automation | 85-90% |
| Protected PR review safety | 90-95% |
| Owner-trigger / lane automation | 60-70% after Phase 4J-4 merge; auto-merge remains inactive |
| Actual product development | 15-25% |
| Content governance / question system | 10-20% |
| Backend / Firebase / auth / cloud | 0%; claim: no implemented scope |
| Build/distribution readiness | 0-10%; claim: no distribution scope |
| Overall full project | 30-40% |

These percentages are governance estimates. They are not product-readiness, exam-readiness, public-launch, pass/fail, production, build, backend, Firebase, auth, cloud, or distribution claims.

## Validation Evidence

Local validation evidence after the progress-snapshot claim wording correction:

- `python3 scripts/control/check_changed_files.py`
- `python3 scripts/control/check_forbidden_scope.py`
- `python3 scripts/control/check_required_control_updates.py`
- `python3 scripts/control/check_pr_contract.py`
- `python3 scripts/control/check_owner_trigger_review.py`
- `python3 scripts/control/check_forbidden_scope.py --lockfiles-only`
- `python3 scripts/control/check_pr_contract.py --claims-only`
- `git diff --check`

All listed local validation commands passed.

Initial validation note:

- `python3 scripts/control/check_forbidden_scope.py` initially failed because the progress snapshot category lines for backend/cloud and build/distribution percentages did not include explicit claim downgrade wording on the same lines. The lines now include claim downgrade wording and the scan passes.

Expected PR behavior after the pull request opens:

- Owner-trigger evidence should pass.
- The required ContractorOS Control Gates should remain blocked until external red-team adds a valid SHA-bound red-team decision marker for the exact current PR head SHA.
- If the PR passes before external red-team evidence is added, mandatory red-team enforcement may be broken and work must stop for investigation.

## Risk Register Impact

`RISK_REGISTER.md` records risks for red-team lifecycle state drift, chat-memory reliance, handoff gaps, stale PR head SHA approval, and non-durable approvals or conditions.

## Design Decision Impact

`CONTRACTOROS_DESIGN_DECISIONS.md` records durable red-team operating protocol and lifecycle state classification decisions.

## Decision Log Impact

`DECISION_LOG.md` records the red-team protocol, state classification, command-output requirement, progress snapshot requirement, and governance-estimate claim downgrade rule.

## Requirements Traceability Impact

`REQUIREMENTS_TRACEABILITY_MATRIX.md` records Phase 4J-5 traceability for protocol conversion, source-of-truth rules, evidence durability, state classification, command-output requirements, progress snapshot requirements, role separation, auto-merge status, state-machine coverage, handoff startup, and scope containment.

## Validation Task Impact

`VALIDATION_TASKS.md` records Phase 4J-5 validation tasks.

## Source Register Impact

`SOURCE_REGISTER.md` records Issue #24, Issue #25, all named Issue #24 addenda, and the verified starting main SHA as Phase 4J-5 sources.

## Artifact Index Impact

`ARTIFACT_INDEX.md` records that Phase 4J-5 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.

No Google Drive artifact is created by this phase.

## Owner Trigger / Lane Eligibility Evidence

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Phase 4J-5 converts red-team operating protocol, handoff behavior, and lifecycle state-machine rules into committed governance controls that affect future review behavior.

## Interaction with Red-Team Decision Enforcement

Codex did not add the red-team decision marker.

External red-team review remains required.

The Phase 4J-5 PR should remain blocked by the mandatory SHA-bound red-team marker check until external red-team adds a valid marker for the exact current PR head SHA.

## Red-Team Status

Pending external red-team review.

Codex did not self-review and did not add the red-team decision marker.

## Human Approval Status

Pending human/write-access approval after external red-team review.

## Auto-Merge Status

Auto-merge remains inactive.

This phase does not activate auto-merge.

## Forbidden Scope Confirmation

- [x] No backend
- [x] No database
- [x] No Firebase
- [x] No Airtable runtime
- [x] No deployment
- [x] No auth/login/user accounts
- [x] No payments/subscriptions
- [x] No scoring
- [x] No readiness
- [x] No pass/fail
- [x] No saved progress
- [x] No analytics
- [x] No public MCQs
- [x] No Question Bank migration
- [x] No C10 public content
- [x] No C46 public content
- [x] No C39 public content
- [x] No EAS
- [x] No APK/AAB/iOS build
- [x] No eas.json
- [x] No android/
- [x] No ios/
- [x] No package or lockfile changes
- [x] No ZIP binaries

Forbidden scope confirmation: confirmed control/infrastructure-only documentation changes.

## Claim Level

Source verified and local-script verified for Phase 4J-5 control files only after validation passes.

No product, release, build, distribution, backend, database, dependency, mobile, web, scoring, readiness, pass/fail, public-content, or launch claim is made.

## Known Limitations

This phase improves red-team continuity and handoff behavior only.

It does not implement product features, activate auto-merge, reduce human approval requirements, resume Phase 4I, or start Phase 4J-6.

GitHub Actions evidence remains pending until the PR opens.

## Next Phase Status

Phase 4J-6 is not started.

Phase 4I remains paused.

Product implementation remains blocked until an explicit approved phase authorizes it.
