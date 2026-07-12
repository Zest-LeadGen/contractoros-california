# ContractorOS Automation Phase Roadmap

## Purpose

Record the owner-approved redirect toward workflow automation, the planning sequence through Phase 4K-12, dependencies between gates, and the deferred toolchain path. This roadmap does not start later phases.

## Current State

Phase 4K-5 ended as blocked-before-mutation dependency/toolchain evidence. Issue #39 is closed/completed and PR #40 merged at `e531c4d8bc1904c231be1f43114f16f652c4ec52` without implementing the dependency baseline.

Phase 4K-6 is merged through PR #42. Phase 4K-7 completed through Issue #43 and merged PR #44; its reviewed head was `a519ef5579c130181ac1b25f74bb48f481478378`, and its merge/current-main SHA is `8d443310cf006b82966163f8e486d1f52d8d4e6c`. Phase 4K-8 is active through Issue #45 and PR #46. Phase 4K-9 is not started, Phase 4I remains paused, and auto-merge remains inactive.

## Owner-Approved Redirect

The immediate path is redirected from the previously recommended toolchain availability / npm bootstrap governance gate to a workflow-automation policy and implementation sequence. The toolchain path remains valid but deferred, not rejected.

The strategic goal is approximately 95% workflow/process automation while retaining owner judgment, external red-team separation, branch protection, required human approval under current policy, and exact SHA-bound evidence.

## Phase 4K-6 Policy Gate

Status: Merged through PR #42 at `4315c943b6210f023849592213882bc8983c31d2`.

Outcome: version the target state, low-risk lane policy, owner-trigger boundaries, retained human/red-team controls, measurable manual-action targets, stop conditions, and the planning sequence through Phase 4K-12.

No automation implementation, workflow mutation, control-script mutation, toolchain work, or later-phase work is authorized.

## Phase 4K-7 Low-Risk Lane Validator / Control-Gate Implementation Gate

Status: Merged through PR #44 at `8d443310cf006b82966163f8e486d1f52d8d4e6c`.

Planned outcome: implement and test deterministic low-risk candidate classification, owner-trigger consistency, fail-closed behavior, and control-gate integration without changing approval policy or activating auto-merge.

Dependency: Phase 4K-6 merged, main verified, Issue #41 closed, and Issue #43 approved as the durable implementation intake.

## Phase 4K-8 Workflow Automation Command-Pack / Operator Runbook Gate

Status: Active through Issue #45 and PR #46.

Planned outcome: define an approved operator command pack and runbook for repetitive evidence collection, check monitoring, marker assembly, merge verification, issue closeout, and stop-condition reporting.

Dependency: Phase 4K-7 merged, main-verified, Issue #43 closed, and validated lane/control behavior.

## Phase 4K-9 Phase Intake + Codex Handoff Automation Gate

Status: Planning target only; not started and requires its own future durable GitHub issue.

Planned outcome: automate durable issue preparation and Codex handoff drafting from governed templates while preserving owner-trigger interruption and executor-only boundaries.

Dependency: Phase 4K-8 merged, main-verified, Issue #45 closed, approved command pack, source-of-truth controls, and deterministic issue/prompt validation.

## Phase 4K-10 Post-Marker Checks, Merge Verification, and Issue Closeout Automation Gate

Status: Planning target only; not started and requires its own future durable GitHub issue.

Planned outcome: automate post-marker check monitoring, exact-SHA verification, post-merge main verification, issue closeout drafting, and progress-register update drafting. Automation must stop before unapproved merge or closeout.

Dependency: Phase 4K-9 evidence plus retained red-team and human approval controls.

## Phase 4K-11 Low-Risk Automation Dry-Run Gate

Status: Planning target only; not started and requires its own future durable GitHub issue.

Planned outcome: run a non-autonomous low-risk lane trial, measure manual actions, classification accuracy, stop-condition behavior, stale-SHA handling, audit evidence, and rollback quality.

Dependency: Phases 4K-7 through 4K-10 separately reviewed, merged, and main-verified.

## Phase 4K-12 95% Workflow Automation Readiness Decision Gate (Blocked Until Evidence)

Status: Planning target only; not started and requires its own future durable GitHub issue.

Planned outcome: decide whether evidence supports approximately 95% workflow automation for defined phase categories, what owner/human actions remain, and whether any narrow policy change should be proposed. This is a decision gate, not automatic approval.

Dependency: Phase 4K-11 dry-run evidence and external review of metrics, exceptions, and retained controls.

## Deferred Toolchain Path

The toolchain availability / npm bootstrap governance decision path is deferred while the automation sequence is documented and pursued. It is not rejected.

Any later return requires a durable issue, explicit dependency/toolchain scope, registry and package-manager policy, risk acceptance, external red-team review, human approval, and no assumption that Phase 4K-6 authorizes dependency work.

## Risks

- Low-risk lane misclassification could admit owner-triggered work.
- Automation could be mistaken for authority to approve, merge, close issues, or expand scope.
- Stale PR-head SHA evidence could be reused after a commit.
- Source-of-truth conflicts could produce incorrect lifecycle or closeout actions.
- Manual-action reduction could be optimized at the expense of review quality.
- Later implementation could outpace durable issues, tests, or rollback evidence.

## Stop Conditions

Stop the sequence when a prerequisite phase is not merged/main-verified/closed, a future phase lacks its own durable issue, required evidence conflicts, classification is uncertain, protected checks fail, owner-trigger or external review requirements are unmet, or the work would bypass branch protection or activate auto-merge without separately approved policy.

## Claim Limits

Phase 4K-8 may prove command-pack and operator-runbook documentation only after local validation, external review, and merge. It does not prove low-risk automation activation, reduced manual action in practice, runtime behavior, toolchain availability, dependency baseline, build status, product status, or release status.

## Pre-4K-9 Program Constitution Gate

Phase 4K-8 is completed through merged PR #46 and closed/completed Issue #45 at main `b99fc7d1fe0882380fc53041be42bb0aad35c02e`. Issue #47 is the active documentation gate for the Program Constitution, D1–D26 decision reconciliation, red-team continuity architecture, public/private policy, and current-state records. Phase 4K-9 remains not started and Phase 4I remains paused.

After Issue #47 is merged, main-verified, and closed, the next gate is the **Read-Only Red-Team Continuity Evidence Collector / Startup Packet Gate**. It must precede Phase 4K-9 and begin with read-only evidence access only.

## Issue #49 Read-Only Continuity Gate

Issue #47 is closed/completed and PR #48 is merged at `01b90ab8b12416101b4be067794bf543a3488779`. Issue #49 is active through PR #50 for the read-only continuity collector and deterministic derived startup packet implementation in review.

Phase 4K-9 is not started. Phase 4I remains paused. This gate must pass external exact-SHA review, human approval, protected merge, main verification and Issue #49 closeout before Phase 4K-9 may be evaluated.
