# ADR-003 — Red-Team Continuity And Public/Private Control Plane

## Status
Approved architecture direction; collector and private planes are not implemented.

## Related Owner Decision IDs
D6, D7, D15, D25.

## Context
Manual handoff and public-only evidence cannot safely hold complete continuity state.

## Decision
Use five layers: sanitized canonical state, append-only events, derived startup packet, controlled unsynced inbox, and separated private planes.

## Alternatives Considered
Chat memory, a manually maintained canonical packet, public storage of all evidence, or deletion of old handoffs.

## Rejected Alternatives
They lose provenance, expose sensitive material, or erase audit history.

## Consequences
Cross-plane references use opaque IDs or hashes; canonical state is serialized.

## Risks
State drift, private-data leakage, orphan references, and false derived evidence.

## Controls
Schema checks, stale detection, quarantine, sanitization, retention, access review, and exact-SHA binding.

## Implementation Prerequisites
Read-only collector gate, private-plane design review, and incident process.

## Non-Authorized Scope
No generator, private repository, storage, database, or write service is created.

## Validation Requirements
Deterministic packet, stale-state, provenance, and leak tests.

## Supersession Links
Future event-sourced continuity will supersede manual relay; Issue #24 remains audit history.
