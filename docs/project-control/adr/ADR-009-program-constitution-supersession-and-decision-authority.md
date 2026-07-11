# ADR-009 — Program Constitution, Supersession, And Decision Control

## Status
Approved direction; documentation created in Issue #47 remains subject to review and merge.

## Related Owner Decision IDs
D25, D26.

## Context
Chat-only direction and silent document rewrites create uncertain program control.

## Decision
Use the Constitution, machine-readable decision register, linked ADRs, risk/assumption records, and explicit supersession. No chat-originated item is authoritative without owner confirmation and durable recording.

## Alternatives Considered
Chat memory as control; one mutable summary; deletion of superseded records.

## Rejected Alternatives
They weaken provenance and audit history.

## Consequences
Conflicts are harmonized or blocked visibly. Documentation direction still requires phase gates.

## Risks
Precedence ambiguity, duplicate decisions, stale state, and apparent implementation claims.

## Controls
Decision IDs, required fields, supersession links, schemas, canonical state, and protected review.

## Implementation Prerequisites
Merge and closeout of Issue #47, then the read-only continuity collector gate.

## Non-Authorized Scope
No operational capability, next phase, private plane, or source system is authorized.

## Validation Requirements
Register completeness, conflict table, schema consistency, and exact-SHA lifecycle evidence.

## Supersession Links
The Issue #47 owner amendment supersedes the narrower initial intake while preserving it as audit history.
