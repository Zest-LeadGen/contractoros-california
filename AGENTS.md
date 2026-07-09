# ContractorOS Codex Operating Model

## Purpose

This file defines how Codex may operate in the ContractorOS California repository.

GitHub code, GitHub PRs, and versioned project-control files are the source of truth. Chat memory, local scratch files, connector state, and unversioned notes are not source of truth.

## Prompt Convention

Every future ContractorOS prompt must include the model/effort header defined in `docs/project-control/PROMPT_CONVENTION.md`.

Agents must stop if the model/effort header is missing.

Agents must not silently choose model/effort for ContractorOS work.

Phase 4J-0 documents this convention only and does not activate auto-merge.

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

Phase 4J-2 creates the marker format and validator. Mandatory enforcement may be activated by Phase 4J-3 or a later approved control phase after bootstrap review.

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
