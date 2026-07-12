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
