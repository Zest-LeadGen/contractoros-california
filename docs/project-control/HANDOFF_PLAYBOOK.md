# ContractorOS Handoff Playbook

## Purpose

Give future ContractorOS California red-team windows a durable startup sequence so review behavior does not depend on chat memory.

## Startup Sequence

At the start of a red-team window:

1. Read the active phase issue.
2. Read Issue #24 as the handoff/protocol anchor.
3. Read the Issue #24 protocol addenda:
   - Red-Team Operating Protocol Addendum
   - CLI Expected Output Requirement
   - Progress Snapshot Requirement
   - Red-Team Operator State Machine Addendum
   - Consolidated owner direction, while treating it as future program direction that does not expand the active phase
4. Read the committed project-control protocol files:
   - `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
   - `docs/project-control/RED_TEAM_STATE_MACHINE.md`
   - `docs/project-control/HANDOFF_PLAYBOOK.md`
   - `AGENTS.md`
   - `docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md`
5. Verify the current lifecycle state before giving next steps.
6. Verify the current active issue.
7. Verify PR status if a PR exists.
8. Verify the latest PR head SHA if a PR exists.
9. Verify control-gate state.
10. Verify red-team marker state.
11. Verify owner-trigger marker state.
12. Verify human approval state.
13. Verify merge, main, and issue-closeout state before allowing next-phase planning.

Before any red-team next step, validate the actor-bound scope from `RED_TEAM_ROLE_CONTRACT.md`: active actor, `ROLE`, repository, issue, pull request, branch, exact SHA, lifecycle state, authority source, observation timestamp, descriptive program action, next authorized actor, and one bounded next action or `NONE` for every lifecycle role. Program direction creates no actor authority scope.

For red-team, repository write, GitHub write, terminal mutation, implementation, human approval, merge, and issue-closeout power must remain none or no. A contradiction enters `ROLE_CONFLICT` and `REPAIR_REQUIRED`; repair may restore only `READ_ONLY_ROLE_RESTORED`. Any attempted mutation remains denied and recorded in bounded public-safe incident evidence.

Never rely on chat memory as source of truth.

## Current Marker Handoff Rule

Issue #24 remains the policy anchor, but its historical append-only marker procedure is superseded. Current handoffs must use the Phase 4K-8 replacement-body rule: preserve report content outside stale red-team and owner-marker sections, remove those existing sections, append exactly one current-SHA `RED_TEAM_DECISION`, and append exactly one matching `OWNER_TRIGGER_REVIEW` section last. Validate counts, ordering, the full current 40-character head SHA, stale pending-status removal, and resolved runtime values before any PR-body update.

This rule does not let Codex add red-team evidence. External exact-SHA review and human/write-access approval remain separate, auto-merge remains prohibited, and no memory-only authority is valid.

## Required Evidence Checks

Use GitHub and repo evidence to answer:

- What is the active phase issue?
- What branch and PR are in scope?
- What is the base branch and starting main SHA?
- What is the current PR head SHA?
- Which files changed?
- Are changed files inside the explicit allowlist?
- Which validation commands ran, and what did they output?
- Did the owner-trigger marker pass validation?
- Is the red-team marker missing, stale, malformed, or valid for the current head SHA?
- What is the latest GitHub Actions status for the current head SHA?
- Is human/write-access approval present?
- Is the PR merged?
- Is `origin/main` verified after merge?
- Is the linked issue closed with closeout evidence?

If any answer cannot be proven, label it `not proven`.

If a missing answer blocks the next action, label the state `blocked`.

## Command Blocks

When giving terminal or GitHub CLI commands, include:

- the exact command or command block
- expected success output or success indicators
- failure indicators
- stop condition
- next allowed action after confirmation

For source-control scope commands that include remote ref updates, state that the command updates local evidence and must be followed by SHA verification.

## Handoff Summary Template

Use this structure when handing a phase to another red-team window:

```text
Current lifecycle state:
Evidence used:
Active phase issue:
Pull request:
Branch:
Starting main SHA:
Current PR head SHA:
Changed files:
Control-gate state:
Owner-trigger evidence:
Red-team marker state:
Human approval state:
Merge/main state:
Linked issue state:
Single next required action:
Stop conditions:
What not to do:
Where this state is recorded:
Progress snapshot:
Actor role and authority scope:
Program next action:
Next authorized actor scope:
Developer next action:
Red-team next action:
Human-approver next action:
Merge-operator next action:
Role-conflict status:
Role-repair state:
Denied incident summary:
```

## Progress Snapshot Template

The old Phase 4J percentages are historical baseline only. Do not carry them forward as current estimates.

Unless the owner explicitly asks for no progress section or the response is only a brief acknowledgment, give a current evidence-based estimate for each distinct area:

- governance and control maturity;
- workflow automation implementation;
- product implementation;
- content governance and content production;
- dependency and runtime capability;
- backend and data-platform capability;
- build and distribution capability;
- business and market validation;
- overall program progress.

For every estimate, cite the current GitHub, committed-file, terminal, uploaded-file, or clearly labeled assumption evidence that supports it. Mark an area `not proven` when evidence is unavailable. Do not blend governance progress into product, content, runtime, backend, build, business-validation, or overall progress.

## Closeout Sequence

A current phase reaches `PHASE_CLOSED_READY_FOR_NEXT_PHASE` only after all of these are proven:

- PR merged.
- Main verified after merge.
- Local main clean when local verification is part of the handoff.
- Linked phase issue closed with closeout evidence.
- Closeout summarized.

Only then may red-team prepare next-phase issue guidance or implementation prompts.

## Prohibited Handoff Behavior

- Do not ask the owner to choose next-phase options before current phase closeout.
- Do not resume Phase 4I unless explicitly authorized.
- Do not start Phase 4K-9 until Phase 4K-8 is merged, main-verified, and Issue #45 is closed.
- Do not treat chat memory, sandbox state, connector state, or local scratch files as durable evidence.
- Do not invent Google Drive artifacts, branch state, PR state, GitHub Actions state, validation results, approvals, merge state, or issue state.
- Do not merge, approve, self-review, bypass branch protection, or activate auto-merge.

## Future Generated Startup Packet

After Issue #47 closeout, a dedicated read-only gate may implement a deterministic `RED_TEAM_STARTUP_PACKET.md` generator from canonical state and live GitHub reads. The packet is derived, never authoritative by itself, and must disclose source SHAs, timestamps, stale checks, and missing evidence. Until that gate passes, use this playbook and live evidence; do not manually maintain a packet and call it canonical.

## Issue #49 Collector Handoff Procedure

Issue #49 implements the collector in review. After the gate is merged, main-verified and closed, a future red-team window may create an external temporary directory and invoke:

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/continuity/red_team_continuity.py live \
  --repo-root <verified-repository-root> \
  --repository Zest-LeadGen/contractoros-california \
  --issue-number <active-issue> \
  --pr-number <active-pull-request> \
  --run-id <current-control-run> \
  --canonical-ref <exact-current-ref> \
  --observed-at <explicit-rfc3339-time> \
  --output-dir <external-temporary-directory>
```

Expected safe active-PR output is exit `0` with `requires_live_verification`, a packet bound to the current head, pending external review and human approval disclosed, auto-merge inactive, and no merge permission. Exit `2`, `3`, `4`, or `5` is a stop condition. The operator must compare the live head and run evidence again before any next action. Generated output remains external and derived; it has no authority by itself.

## Quota-Aware Atomic Packet Handoff

Every substantial packet declares primary objective, permitted files/functions, model, reasoning effort, speed, agent count, focused validation, checkpoint, stop conditions, and next packet. One lead agent, Medium effort, and Standard speed are the normal Plus defaults; hidden session values use the honest fallback attestations in `PROMPT_CONVENTION.md`.

Before quota or context exhaustion, preserve a truthful checkpoint containing issue and PR, branch, local and remote head SHAs, staged/unstaged/untracked paths, completed packet, tests and exact results, remaining blockers, next packet, and prohibited actions. Do not create a commit merely to hide partial or failing work.

Context thresholds control handoff behavior:

- 0-59%: normal bounded work.
- 60-74%: no scope expansion; prepare the checkpoint.
- 75-84%: finish only the smallest safe unit, validate, and prepare a new-window handoff.
- 85-100%: handoff-only; no new implementation.

A reported 79% requires a new Codex window before another broad implementation packet. If percentage is unavailable, record that fact and use visible compaction warnings or context-loss symptoms without inventing a value.

The final handoff records `ACTUAL_CODEX_MODEL`, `ACTUAL_REASONING_EFFORT`, `SPEED_MODE`, `AGENT_STRATEGY`, context-window state, lifecycle evidence, validation, changed files, and the single next packet. It also follows the compact tables, percentage-integrity, and chart rules in `RED_TEAM_OPERATING_PROTOCOL.md`.
