# ContractorOS Codex Operating Model

## Purpose

This file defines how Codex may operate in the ContractorOS California repository.

GitHub code, GitHub PRs, and versioned project-control files are the source of truth. Chat memory, local scratch files, connector state, and unversioned notes are not source of truth.

## Role Boundary

Codex is a developer executor only. Codex may implement approved scoped changes, collect evidence, and prepare PRs. Codex must not self-review, act as red-team, approve its own work, merge, bypass branch protection, or start the next phase.

Red-team review remains separate. Human/write-access approval remains required before merge.

## Required Development Route

Use this route unless a later project-control PR changes it:

```text
GitHub Issue or approved phase prompt -> Developer branch -> Pull request -> Control gates -> Red-team decision -> Human/write-access approval -> Merge
```

No auto-merge is permitted. No branch-protection bypass is permitted.

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

Phase 4J-0 may create this file and the AI governance files before `AGENTS.md` exists. This exception is active only for Phase 4J-0 and does not permit future bypass, product work, auto-merge, self-review, branch-protection bypass, or merge without red-team review and human/write-access approval.
