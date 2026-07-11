# Red-Team Continuity Architecture

## Purpose And Current Claim

This public-safe architecture defines continuity controls; it does not implement a collector, generator, database, agent, credential, or write-capable service.

## Layer 1 — Canonical State

`docs/project-control/state/contractoros-state.yaml` is the sanitized canonical state snapshot governed by its schema. It records schema version, main SHA, active gate, linked issue/PR, lifecycle state, paused and completed phases, blockers, next planning target, timestamps, evidence identifiers, public/private references, and consistency status. It must contain no private strategy, customer data, secrets, raw legal analysis, or private AI traces.

Canonical state changes are serialized through one protected pull request at a time. A reader must compare the recorded main SHA, issue, PR, and timestamps with live GitHub evidence. A mismatch is stale-state failure and requires quarantine; no downstream write may proceed.

## Layer 2 — Append-Only Decisions And Events

Owner decisions and architecture events are append-only. Corrections add a new event and explicit `supersedes` / `superseded_by` links. Historical records remain available for audit. No database is implemented in this gate.

## Layer 3 — Derived Startup Packet

`RED_TEAM_STARTUP_PACKET.md` is a future generated artifact derived from canonical state, versioned controls, and live read-only GitHub evidence. It is never authoritative by itself and must disclose generation time, source SHAs, stale checks, and missing evidence. This gate does not create the packet or generator.

## Layer 4 — Unsynced-Decision Inbox

The inbox schema permits `proposed`, `owner_confirmed`, `rejected`, `recorded`, `superseded`, and `blocked`. Chat-originated content is never authority automatically. Owner confirmation plus durable GitHub or committed recording is required before `recorded`. Failed validation or ambiguous provenance quarantines the item.

## Layer 5 — Private Control Plane

The public repository stores sanitized references only. A future private governance repository may hold confidential strategy, legal-review material, traces, incidents, and sensitive handoffs. Future private artifact storage may hold proprietary packages and originals. Cross-plane references require opaque IDs or hashes, provenance, classification, retention, access-control, sanitization, and incident procedures. No private repository or storage is created here.

## Failure, Rollback, And Quarantine

- Schema failure, moved SHA, conflicting lifecycle evidence, missing owner confirmation, or inaccessible authoritative evidence sets consistency to `blocked` or `quarantined`.
- Rollback restores the last committed public-safe state through a new reviewed commit; history is not erased.
- Exact-SHA review is mandatory. A new commit makes prior approval stale.
- A quarantined packet or inbox item does not authorize implementation, approval, merge, release, spending, credentials, or policy changes.

## Issue #24 Continuity

Issue #24 remains audit history. Its source-of-truth, role-separation, lifecycle-classification, command-evidence, progress-snapshot, and no-memory-only rules remain controlling where incorporated into committed protocol. Its early Phase 4J lifecycle snapshot and append-only marker example are historical; Phase 4K-8 replacement-body rules supersede that marker procedure. Event-sourced continuity will supersede manual relay only after a later implementation gate proves read-only collection and deterministic packet generation.

## Required Next Gate

After Issue #47 is merged, main-verified, and closed, the next gate is exactly: **Read-Only Red-Team Continuity Evidence Collector / Startup Packet Gate**. It precedes ordinary Phase 4K-9 and begins with read-only evidence access only. It has no write, approval, merge, release, budget, credential-management, or policy-amendment authority.
