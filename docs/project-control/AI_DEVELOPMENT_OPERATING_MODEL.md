# AI Development Operating Model

## Purpose

Define how AI assistance may be used for ContractorOS California without weakening GitHub evidence, red-team separation, owner judgment, or protected PR governance.

## Source Of Truth

GitHub is source of truth for code, PRs, review evidence, and text project-control records.

Chat memory is not source of truth. Unversioned local notes, transient tool state, and connector memory are not source of truth.

Every assumption, design decision, source, model run, validation task, and originality requirement must be captured in versioned repo files.

## AI Role

Codex is developer executor only. Codex may prepare scoped file changes, run permitted local checks, and open PRs. Codex must not self-review, act as red-team, merge, approve its own PR, bypass branch protection, or continue into the next phase.

Red-team remains separate. Future red-team decisions must become GitHub artifacts tied to the exact PR head SHA, beginning with the future Phase 4J-2 control path.

Human/write-access approval remains required before merge. No auto-merge is permitted.

## Automation Meaning

95% automation means reducing relay work, paperwork, repetitive checks, and handoff friction. It does not remove owner judgment, red-team accountability, protected PR governance, or human/write-access approval for merge.

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
