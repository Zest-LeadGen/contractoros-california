# AI Development Operating Model

## Purpose

Define how AI assistance may be used for ContractorOS California without weakening GitHub evidence, red-team separation, owner judgment, or protected PR governance.

## Source Of Truth

GitHub is source of truth for code, PRs, review evidence, and text project-control records.

Chat memory is not source of truth. Unversioned local notes, transient tool state, and connector memory are not source of truth.

Every assumption, design decision, source, model run, validation task, and originality requirement must be captured in versioned repo files.

## Prompt Convention

Every future implementation, review, or correction prompt must include model and effort recommendation.

Model/effort selection must follow `docs/project-control/PROMPT_CONVENTION.md`.

Missing model/effort header is a stop condition.

Phase 4J-0 documents this convention only.

## GitHub Phase Issue Intake

After Phase 4J-1, every future phase PR must link a GitHub phase issue.

The phase issue is the durable intake record for owner-approved objective, lane, file allowlist, forbidden scope, assumptions, risks, validation tasks, red-team requirements, human approval requirements, and auto-merge status.

Chat prompts may initiate discussion, but chat memory is not sufficient phase intake once the linked-issue requirement is active.

Missing linked phase issue reference is a PR control-gate failure.

## AI Role

Codex is developer executor only. Codex may prepare scoped file changes, run permitted local checks, and open PRs. Codex must not self-review, act as red-team, merge, approve its own PR, bypass branch protection, or continue into the next phase.

Red-team remains separate. Red-team decisions must become GitHub PR evidence tied to the exact PR head SHA reviewed.

The required plain-text marker begins with `RED_TEAM_DECISION` and includes PR number, PR head SHA, decision, reviewer role, review date, scope reviewed, conditions, forbidden-scope confirmation, and the statement `This decision applies only to the listed PR head SHA.`

`scripts/control/check_red_team_marker.py` validates the marker text against the current PR head SHA and fails when the marker is missing, stale, malformed, or records `CHANGES_REQUESTED` or `BLOCKED`.

Phase 4J-3 wires the marker validator into the required ContractorOS control-gates workflow for pull requests. The workflow reruns on PR body edits so red-team can add the marker after review, and any later commit changes the PR head SHA and requires a fresh marker.

Current state:

Human/write-access approval remains required before merge. No auto-merge is currently authorized.

## Automation Meaning

Current state:

95% automation means reducing relay work, paperwork, repetitive checks, and handoff friction. It does not remove owner judgment, red-team accountability, protected PR governance, or human/write-access approval for merge.

Future target:

95% automation should reduce owner monitoring and manual merge work for low-risk, mechanically verifiable lanes after required safeguards are implemented.

Future lane-based automation must be separately approved in a later phase. Phase 4J-0 does not authorize auto-merge.

Owner interruption triggers:

Owner interruption remains required for legal, financial, paid-service, public-release, production/readiness, app-store/build/distribution, scope expansion, unresolved red-team BLOCKED decisions, dependency/security risk acceptance, and architecture-threshold decisions.

## Tool Governance

The following controls apply to Codex and other AI developer executors:

- Do not run `/init`.
- Do not call `api_tool.list_resources`.
- Do not call broad connector discovery, broad list-resource calls, or tool-schema dump calls.
- If direct tools are unavailable, stop and report the limitation instead of discovering tools broadly.
- Do not trust unrelated hooks.
- Do not use cockroachdb hooks.
- Do not use unrelated Claude-imported Codex project context.
- Do not add paid API, paid services, hosted bots, hosted CI, or hosted tools in this phase.

## Bootstrap Exception

Phase 4J-0 is allowed to create `AGENTS.md` and the AI governance files before those files exist. This bootstrap exception exists because the prior developer connector implementation path failed twice before implementation by calling `api_tool.list_resources`.

The exception is active only for Phase 4J-0. It does not permit product work, dependency work, native build work, backend work, merge, auto-merge, self-review, branch-protection bypass, or future bypass.

## Stop Conditions

Stop instead of proceeding when:

- A required direct tool is unavailable.
- The requested work would touch files outside the approved allowlist.
- A hook or connector context appears unrelated to ContractorOS California.
- A command would add dependency, build, backend, database, native, release, or product scope.
- Red-team review or human/write-access approval is missing for merge.
