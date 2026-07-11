# ADR-002 — AI Decision Power, Development, And Write Boundaries

## Status
Approved program direction; current protected lifecycle remains controlling.

## Related Owner Decision IDs
D3, D4, D5.

## Context
AI can prepare changes efficiently but self-review or unrestricted writes collapse separation of duties.

## Decision
Use Levels A–D. Permit scoped developer branches, commits, and PRs under approved gates. Keep external review, approval, merge, release, budgets, credentials, and policy changes separate and protected.

## Alternatives Considered
Unrestricted agent; read-only AI; single identity for all roles.

## Rejected Alternatives
Unrestricted and single-identity models create unacceptable control risk; read-only-only prevents bounded developer execution already permitted.

## Consequences
Capability grants must be explicit and role-specific.

## Risks
Privilege creep, prompt injection, stale approvals, and hidden uncertainty.

## Controls
Least privilege, strict schemas, traces, exact-SHA review, kill switches, and human gates.

## Implementation Prerequisites
Dedicated tool-security and identity gate.

## Non-Authorized Scope
No agent, credential, identity, approval, merge, or production action is implemented.

## Validation Requirements
Negative capability tests and role-separation evidence.

## Supersession Links
Extends existing developer-executor and red-team protocols without superseding them.
