# ContractorOS Workflow Automation Target State

## Purpose

Define the measurable workflow/process automation target for ContractorOS California while preserving protected GitHub governance, external review separation, and owner judgment.

## 95% Workflow Automation Definition

Approximately 95% workflow automation means that repeatable phase-administration steps can be performed by future approved automation with durable GitHub evidence, deterministic checks, and explicit stop conditions. It is a process target, not a claim that 95% of product engineering or judgment can be automated.

The target may reduce repeated owner relay for issue preparation, Codex handoff preparation, PR evidence collection, marker drafting assistance, check monitoring, merge verification, issue closeout, and project-control progress updates.

The target does not remove owner judgment, external red-team review where required, human approval where required, branch protection, exact PR-head SHA binding, or evidence-based claim limits.

## What Automation May Handle

After future implementation and validation, automation may handle:

- drafting phase issues and Codex handoff prompts from versioned templates;
- checking declared file allowlists and forbidden scope;
- collecting PR metadata and changed-file evidence;
- drafting owner-trigger and red-team marker text for an approved human or external reviewer to evaluate and add;
- monitoring required checks and reporting exact failures;
- verifying merge metadata and main-branch state after an approved merge;
- drafting issue closeout and project-control register updates;
- stopping and escalating when evidence is missing, stale, ambiguous, or outside policy.

## What Humans Must Still Handle

Owner or qualified human judgment remains required for legal, financial, paid-service, public-release, production, app-store/build/distribution, dependency/security risk acceptance, architecture-threshold, scope-expansion, backend or identity/security, and high-risk product decisions.

External red-team review remains separate wherever policy requires it. A human with write access remains responsible for approvals and merge power unless a later durable policy explicitly changes a narrowly defined eligible lane after implementation evidence.

## Current Manual-Relay Baseline

The current governance route requires approximately 8-14 owner/collaborator actions per phase across intake, prompt relay, developer handoff, evidence transfer, marker coordination, check monitoring, approval, merge verification, issue closeout, and progress updates.

## Target Manual-Action Reduction

| Phase category | Target after future approved automation | Retained human boundary |
|---|---:|---|
| Low-risk documentation/control phases | Approximately 0-2 owner actions | Exception handling and any required approval remain human controlled. |
| Routine low-risk source-safe patches | Approximately 2-4 owner actions | Scope confirmation, review, and approval remain policy controlled. |
| Dependency/security/toolchain phases | Approximately 5-9 owner/human actions | Risk acceptance and toolchain decisions remain human controlled unless later durable policy reduces them. |
| Legal, financial, public-release, production, app-store/build/distribution, backend or identity/security, and high-risk product phases | No autonomous reduction of required approval | Owner/human approval remains required. |

These are target ranges for manual relay reduction, not guarantees and not approval to activate automation. Phase 4K-7 completed through Issue #43 and merged PR #44 at `8d443310cf006b82966163f8e486d1f52d8d4e6c`; Phase 4K-8 is historical and completed through closed Issue #45 and merged PR #46.

## Source-of-Truth Requirements

GitHub main, phase issues, PR metadata and evidence, required checks, and committed project-control files remain source of truth. Chat memory, local scratch, assistant memory, connector state, and unversioned notes cannot establish approval or lifecycle state.

Future automation must read current GitHub evidence, bind actions to exact identifiers and SHAs, write durable evidence through approved routes, and stop when source-of-truth records conflict.

## Red-Team Separation Requirements

Codex must not act as external red-team, approve its own work, or add the final red-team decision marker. Future automation may prepare evidence and draft review material, but an external red-team reviewer must independently evaluate the exact current PR head SHA and add any required decision marker.

Any commit after a red-team decision makes the prior SHA-bound decision stale. Automation must stop until a new external review covers the new head SHA.

## Codex Executor Boundary

Codex remains developer executor only. It may implement approved scoped work, run authorized validation, collect evidence, create a branch and PR when requested, and report status. It must not self-review, approve, merge, bypass branch protection, silently expand scope, or start a later phase.

## Human Approval Boundary

Current human/write-access approval remains required for every PR. Any future reduction must be separately approved in durable policy, restricted to a validated low-risk lane, and implemented with required checks and stop conditions.

Owner-trigger categories always interrupt automation under current policy. Human judgment remains mandatory when a trigger applies or evidence is ambiguous.

## Auto-Merge Boundary

Auto-merge is inactive and prohibited. Phase 4K-6 defines future eligibility questions only.

Any future auto-merge proposal requires its own durable issue, external red-team review, human approval, validated lane classification, branch-protection compatibility, required checks, stale-SHA protection, rollback and audit evidence, and proof that owner-trigger categories cannot enter the lane.

## Phase 4K-7 Validator Boundary

Phase 4K-7 may add deterministic lane classification to the control-gates workflow. That validator does not draft issues, operate Codex, add review markers, approve, merge, close issues, or activate low-risk automation.

Current low-risk candidate validation is documentation-only and fail-closed. Workflow/control enforcement changes, control scripts, app source, package manifests, lockfiles, dependency/toolchain paths, backend or identity-system scope, public-release, production, app-store/build/distribution, legal, financial, paid-service, architecture-threshold, scope-expansion, and ambiguous evidence remain outside the low-risk candidate lane.

## Phase 4K-8 Command-Pack Boundary

Phase 4K-8 may document copy-safe commands, operator responsibilities, marker assembly constraints, red-team handoff evidence, manual merge checks, main verification, and issue closeout evidence. It does not execute those lifecycle actions for future phases or activate automation.

The command pack is an operator reference. It preserves manual merge, external red-team, human approval, exact SHA binding, auto-merge prohibition, and no hidden approvals.

## Phase 4K-11 / 4K-12 Readiness Criteria (Blocked Until Evidence)

Phase 4K-11 may begin only from its own future durable issue after Phases 4K-7 through 4K-10 are separately implemented, reviewed, merged, and main-verified. Its dry run must demonstrate deterministic lane classification, marker/check behavior, stop conditions, audit evidence, and no branch-protection bypass.

Phase 4K-12 may evaluate the 95% workflow automation target only after dry-run evidence measures manual actions by phase category, false-positive and false-negative classifications, stale-SHA handling, escalation quality, closeout accuracy, and retained human/red-team controls.

Neither phase is started or approved by this document.

## Non-Goals

Historical Phase 4K-8 documents operator controls only. It does not implement bots, issue-intake automation, Codex-handoff automation, merge automation, issue-closeout automation, repo-backed red-team memory, auto-merge, dependency tooling, package changes, runtime QA, builds, product features, backend or identity-system implementation, public content, or release claims. Phase 4K-9 and downstream progression are paused, Phase 4I remains paused, and the toolchain/npm path remains deferred rather than rejected.

## Program Constitution Reconciliation

The 95% target means eligible routine workflow steps, not protected high-impact decisions. Exact-SHA external review, human/write-access approval, branch protection, manual protected merge, and issue closeout remain retained boundaries. Issue #49 and PR #50 are closed/merged historical collector evidence; no workflow automation is operational. Issue #58 recovery authorizes only project-control reconciliation and no H1 bootstrap or product work.
