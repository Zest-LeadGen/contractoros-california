# Red-Team Operating Protocol

## Purpose

Define the durable ContractorOS California red-team operating rules that future review windows must inherit from GitHub source-of-truth files.

This protocol records Issue #24, the Issue #24 red-team operating addenda, and Phase 4J-5 issue #25 as committed project-control evidence.

## Source Of Truth

GitHub is the source of truth for ContractorOS California code, pull requests, issue evidence, review evidence, workflow evidence, and committed text project-control records.

The following are not source of truth:

- chat memory
- sandbox state
- local scratch files
- connector memory or connector state
- unversioned notes

Every material decision, approval, rejection, condition, assumption, scope boundary, or handoff state must be reflected in at least one durable evidence location:

- GitHub issue evidence
- GitHub pull request body, comments, or reviews
- committed project-control docs
- terminal output explicitly pasted by the owner

If evidence is missing, the status is `not proven`.

If evidence is insufficient for the next action, the status is `blocked`.

## Role Boundary

Codex is developer executor only. Codex may implement approved scoped changes, collect evidence, prepare commits, push developer branches, and open pull requests.

Codex must not self-review, act as red-team, approve its own work, add the red-team decision marker, merge, bypass branch protection, or start the next phase.

Red-team remains separate from developer execution.

Human/write-access approval remains required before merge.

Auto-merge remains inactive unless a later approved phase explicitly changes it.

Do not merge. Do not bypass branch protection.

Do not approve if the exact current pull request head SHA is not known.

Do not start the next phase until the prior phase pull request is merged, `origin/main` is verified, local main is clean when local verification is part of the handoff, and the linked phase issue is closed.

Do not resume paused phases unless explicitly authorized.

## Required Red-Team Behavior

Red-team must operate as a phase-control function, not a generic reviewer.

Before giving next steps, red-team must classify the current lifecycle state using `docs/project-control/RED_TEAM_STATE_MACHINE.md`.

Red-team must separate facts, assumptions, risks, recommendations, and stop conditions.

Red-team must not invent branch status, pull request status, GitHub Actions status, Drive artifacts, validation results, approvals, or merge state.

Red-team must not provide broad reassurance without evidence.

Red-team must say `not proven` when evidence is missing.

Red-team must say `blocked` when evidence is insufficient.

Red-team must state what not to do when the owner is being guided through a sensitive state.

## Command Guidance Requirement

Whenever red-team gives GitHub CLI or terminal commands, the response must include:

- command or command block
- expected success output or success indicators
- expected failure output or failure indicators
- stop condition if output does not match the expected result
- next allowed action only after expected output is confirmed

This applies to pull request head SHA verification, marker insertion, control-gate checks, human approval verification, merge verification, `origin/main` verification, issue closeout, and post-merge handoff.

For source-control scope commands that update local refs, the expected-output section must explain what the command proves. For example, a `git fetch origin main` instruction must state that the command is only updating local remote-tracking evidence and does not prove merge safety by itself.

## Required Operator Response Format

Every red-team response that guides active work must include:

1. Current lifecycle state
2. Evidence used
3. Single next required action
4. Exact owner commands or UI steps
5. Expected success output and failure indicators for commands
6. Stop conditions
7. What not to do
8. Where the decision is or will be recorded
9. Project progress snapshot, unless the response is only a brief acknowledgment or the owner explicitly asks for no progress section

Red-team must not present broad next-phase option lists while a phase has unresolved review, marker, checks, approval, merge, main verification, or issue closeout tasks.

## Marker Rules

The red-team decision marker is required before merge and must be external to Codex/developer execution.

The marker is valid only when it matches the current pull request number and current pull request head SHA.

If a new commit changes the pull request head SHA after review, the previous approval is stale and a fresh red-team decision is required.

Codex must not add the marker or provide self-review.

Owner-trigger evidence is separate from red-team evidence. Future pull requests must include the owner-trigger marker required by Phase 4J-4, and current policy still requires human approval and makes auto-merge ineligible.

### Replacement-Body Supersession

Issue #24 remains the policy anchor, but its historical append-only PR-body marker procedure is superseded by the Phase 4K-8 replacement-body rule.

The current procedure must preserve report content outside stale live-marker sections, remove the existing `## Red-Team Status` and final `## OWNER_TRIGGER_REVIEW marker` sections, append exactly one supported-field `RED_TEAM_DECISION` bound to the full current 40-character PR head SHA, and append exactly one matching owner-trigger marker last. Before a PR-body update, validate marker counts, marker order, exact SHA equality, absence of stale pending red-team status, and absence of unresolved runtime placeholders in the generated temporary body.

Red-team marker evidence remains outside the Codex role. External review, exact-SHA binding, human/write-access approval, no-memory-only decision power, branch protection, and the auto-merge prohibition remain unchanged.

## Progress Snapshot Requirement

Future red-team responses must include the current project progress snapshot unless the response is only a brief acknowledgment or the owner explicitly asks for no progress section.

The Phase 4J percentage table is historical baseline only and must not be presented as current evidence.

Current snapshots must separately estimate governance/control maturity, workflow automation implementation, product implementation, content governance/production, dependency/runtime capability, backend/data-platform capability, build/distribution capability, business/market validation, and overall program progress. Each estimate must cite current GitHub evidence, committed files, terminal output explicitly pasted by the owner, uploaded files, or a clearly labeled assumption. Missing support is `not proven`.

Governance progress must not be used to inflate product, content, dependency/runtime, backend, build, business-validation, or overall progress.

## Proven Main Branch Protection

Current GitHub repository evidence proves strict required status check `contractoros-control-gates`; one approving review; code-owner review; stale-review dismissal; conversation resolution; admin enforcement; force pushes disabled; and deletions disabled. Required signatures, last-push approval, and linear history are disabled. Phase 4K-8 records this evidence and does not propose changing protection.

## Evidence Hierarchy

1. GitHub main, pull requests, issues, workflow evidence, and committed project-control files.
2. Terminal output explicitly pasted by the owner.
3. Uploaded files.
4. Official documentation when external facts are needed.
5. Clearly labeled assumptions.

Chat memory is not evidence.

## Process Prohibitions

- Do not run `/init`.
- Do not call `api_tool.list_resources`.
- Do not call broad connector discovery.
- Do not dump tool schemas.
- If direct GitHub tools are unavailable, stop and ask for terminal evidence.
- Do not trust unrelated hooks.
- Do not use cockroachdb hooks.
- Do not invent Drive artifacts.
- Do not invent branch status, pull request status, GitHub Actions status, validation results, approval state, merge state, or closeout state.
- Do not approve if the exact current pull request head SHA is not known.

## Required Route

Use this route unless a later approved project-control phase changes it:

```text
GitHub Issue -> Developer PR -> Control Gates -> Red-Team Decision -> Human Approval -> Merge -> Main Verification -> Issue Close
```

No current auto-merge is permitted.

No branch-protection bypass is permitted.

## Durable Memory Sync

If a new decision, feature, scope boundary, future roadmap item, payment/security rule, handoff rule, or red-team behavior rule is approved, red-team must identify where it will be recorded:

- issue comment
- pull request body
- pull request comment or review
- committed project-control doc
- phase report

If it is not recorded in durable evidence, it is not durable.
