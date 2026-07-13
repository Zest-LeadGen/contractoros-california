# ContractorOS Codex Operating Model

## Purpose

This file defines how Codex may operate in the ContractorOS California repository.

GitHub code, GitHub PRs, and versioned project-control files are the source of truth. Chat memory, local scratch files, connector state, and unversioned notes are not source of truth.

## Prompt Convention

Every substantive ContractorOS implementation, correction, review, red-team, continuation, handoff, or automation prompt must begin with the exact ordered ten-field model, effort, speed, agent, quota, context, checkpoint, and scope profile defined in `docs/project-control/PROMPT_CONVENTION.md`.

Agents must stop if that prompt profile is missing, incomplete, empty, or out of order. Agents must not silently choose, change, or downgrade a visible model, effort, or speed selection.

Hidden model, effort, or speed metadata is not a stop condition. Agents must proceed with the available compatible session and use the exact honest-fallback values defined in `PROMPT_CONVENTION.md`; hidden values must not be guessed.

Standard speed, Medium effort, and one lead agent are the normal Plus-plan defaults. Fast, Extra High, Max, Ultra, or parallel fan-out require the bounded justification and owner approval defined in the prompt convention.

Phase 4J-0 documents this convention only and does not activate auto-merge.

## Context, Checkpoint, And Progress Discipline

Substantial work must use quota-aware atomic packets and durable checkpoints. At 60-74% context, do not expand scope; at 75-84%, finish only the smallest safe unit and prepare a new-window handoff; at 85-100%, perform handoff only. A reported 79% requires a new window before another broad workstream.

Every substantive response must use compact structured progress tables that separate current-phase gates from program capabilities. Governance progress must not inflate product, runtime, backend, build, content, business-validation, or overall-program progress. Where supported, render exactly one detailed interactive chart at the absolute bottom without exposing raw chart configuration; otherwise record that interactive charts are unsupported and retain structured tables.

## Phase Issue Requirement

Every future phase PR must link a GitHub phase issue using an accepted issue reference such as `Closes #123`, `Fixes #123`, `Resolves #123`, `Linked issue: #123`, or `Phase issue: #123`.

Agents must not treat chat-only prompts as sufficient phase intake once Phase 4J-1 is merged. Phase scope, file allowlists, forbidden scope, assumptions, risks, validation tasks, red-team requirements, and approval requirements must be durable in GitHub issue/PR evidence.

## Role Boundary

Codex is a developer executor only. Codex may implement approved scoped changes, collect evidence, and prepare PRs. Codex must not self-review, act as red-team, approve its own work, merge, bypass branch protection, or start the next phase.

Red-team review remains separate. Human/write-access approval remains required before merge.

## Red-Team SHA Binding

Future red-team decisions must use an exact `RED_TEAM_DECISION` marker in GitHub PR evidence.

The marker must include PR number, PR head SHA, decision, reviewer role, review date, scope reviewed, conditions, forbidden-scope confirmation, and the exact SHA-bound statement defined by `scripts/control/check_red_team_marker.py`.

A red-team approval applies only to the listed PR head SHA. If new commits change the PR head SHA after review, the prior approval is stale and a fresh red-team decision is required.

Phase 4J-3 wires the marker validator into the required ContractorOS control-gates workflow for pull requests. PR body edits rerun the workflow, and a marker is valid only when it matches the current PR number and current PR head SHA.

## Red-Team Operating Protocol And State Machine

Future red-team windows must follow `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`, `docs/project-control/RED_TEAM_STATE_MACHINE.md`, and `docs/project-control/HANDOFF_PLAYBOOK.md`.

GitHub is source of truth. Chat memory, sandbox state, local scratch files, connector state, and unversioned notes are not source of truth.

If evidence is missing, status is `not proven`. If evidence is insufficient for the next action, status is `blocked`.

Red-team must classify lifecycle state before giving next steps, commands, options, next-phase prompts, or implementation guidance.

Whenever red-team gives GitHub CLI or terminal commands, it must include expected success output, failure indicators, stop conditions, and the next allowed action after confirmation.

Red-team must include the project progress snapshot unless the response is only a brief acknowledgment or the owner explicitly asks for no progress section.

Do not start the next phase until the prior phase is merged, main-verified, and issue-closed. Do not resume paused phases unless explicitly authorized.

## Owner-Trigger And Lane Eligibility Evidence

Future PRs must include an exact `OWNER_TRIGGER_REVIEW` marker in GitHub PR evidence before the required ContractorOS control gate can pass.

The marker must state whether owner interruption is required, which trigger categories apply, whether the lane is future-low-risk eligible, whether human approval is required, whether auto-merge is eligible, and the rationale.

Allowed trigger categories are `NONE`, `LEGAL`, `FINANCIAL`, `PAID_SERVICE`, `PUBLIC_RELEASE`, `PRODUCTION_READINESS`, `APP_STORE_BUILD_DISTRIBUTION`, `SCOPE_EXPANSION`, `UNRESOLVED_RED_TEAM_BLOCKED`, `DEPENDENCY_SECURITY_RISK_ACCEPTANCE`, and `ARCHITECTURE_THRESHOLD`.

Any trigger category other than `NONE` requires `Lane eligibility: NOT_AUTOMATION_ELIGIBLE`.

Current required values are `Human approval required: YES` and `Auto-merge eligible: NO`.

Phase 4J-4 wires the marker validator into the required ContractorOS control-gates workflow for pull requests. This does not activate auto-merge or reduce human/write-access approval requirements.

## Required Development Route

Use this route unless a later project-control PR changes it:

```text
GitHub Issue or approved phase prompt -> Developer branch -> Pull request -> Control gates -> Red-team decision -> Human/write-access approval -> Merge
```

No current auto-merge is permitted. No branch-protection bypass is permitted.

Future auto-merge or lane-based automation must be separately approved and implemented by a later phase. Agents must not treat Phase 4J-0 as authorization to bypass owner approval.

Future owner-interruption triggers must include legal, financial, paid-service, public-release, production/readiness, app-store/build/distribution, scope expansion, unresolved red-team BLOCKED decisions, dependency/security risk acceptance, and architecture-threshold decisions.

## Tool And Connector Rules

- Do not run `/init`.
- Do not call `api_tool.list_resources`.
- Do not call broad connector discovery, broad list-resource tools, or tool-schema dump tools.
- If a direct required tool is unavailable, stop and report the limitation instead of discovering alternate tools broadly.
- Do not trust, enable, or rely on unrelated hooks.
- Do not use cockroachdb hooks.
- Do not use unrelated Claude-imported Codex project context.
- No paid API, paid service, hosted bot, hosted CI, or hosted tool may be added unless a later approved control PR permits it.

## Scope Rules

Every phase must follow its explicit file allowlist. Product work, app work, mobile work, web work, build work, dependency work, backend work, database work, release work, and content migration work require an approved phase that names those files.

No auth, payments, scoring, readiness, analytics, public MCQs, Question Bank migration, native build, Expo prebuild, EAS, Android, iOS, backend, database, or dependency scope may be added from a control/documentation phase.

## Versioned Governance Records

Every assumption, design decision, source, model run, validation task, and originality requirement that affects project work must be versioned in repo files under `docs/project-control/`.

## Bootstrap Exception

Phase 4J-0 may create this file and the AI governance files before `AGENTS.md` exists. This exception is active only for Phase 4J-0 and does not permit future bypass, product work, auto-merge, lane-based automation, self-review, branch-protection bypass, or merge without red-team review and human/write-access approval.

## Program Constitution Authority — Documentation Scope

`docs/project-control/PROGRAM_CONSTITUTION.md` is the top-level public-safe program-direction authority. It does not replace phase issues, exact file allowlists, external exact-SHA red-team review, current human/write-access approval, branch protection, merge verification, or issue closeout. `OWNER_DECISION_REGISTER.yaml`, linked ADRs, risk and assumption registers, and canonical state provide subordinate evidence. Chat-only direction is not authority.

Canonical-state files must be changed by one active pull request at a time. No more than three non-overlapping active pull requests may be considered, and no lane may assume unmerged canonical state.
