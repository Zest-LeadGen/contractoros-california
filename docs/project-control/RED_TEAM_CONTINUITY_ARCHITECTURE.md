# Red-Team Continuity Architecture

## Purpose And Current Claim

This public-safe architecture defines continuity controls; it does not implement a collector, generator, database, agent, credential, or write-capable service.

## Layer 1 — Canonical State

`docs/project-control/state/contractoros-state.yaml` is a sanitized observed snapshot governed by its schema. It records schema version, main SHA, active gate, linked issue/PR, lifecycle state, paused and completed phases, blockers, next planning target, timestamps, evidence identifiers, public/private references, and consistency status. It is not live authority and must require live GitHub verification while PR evidence changes. It must contain no private strategy, customer data, secrets, raw legal analysis, or private AI traces.

Canonical state changes are serialized through one protected pull request at a time. A reader must compare the recorded main SHA, issue, PR, and timestamps with live GitHub evidence and must read the exact current PR head SHA from GitHub. The containing snapshot does not embed a supposedly current self-referential PR head. A mismatch is stale-state failure and requires quarantine; no downstream write may proceed.

`requires_live_verification` is a valid consistency status while an open pull request changes lifecycle or exact-SHA evidence. A snapshot must not claim `consistent` after known lifecycle evidence has changed; it may return to `consistent` only when the committed observation and required live comparison agree under the applicable gate.

## Layer 2 — Append-Only Decisions And Events

Owner decisions and architecture events are append-only. Corrections add a new event and explicit `supersedes` / `superseded_by` links. Historical records remain available for audit. No database is implemented in this gate.

## Layer 3 — Derived Startup Packet

`RED_TEAM_STARTUP_PACKET.md` is a future generated artifact derived from canonical state, versioned controls, and live read-only GitHub evidence. It is never authoritative by itself and must disclose generation time, source SHAs, stale checks, and missing evidence. This gate does not create the packet or generator.

## Layer 4 — Unsynced-Decision Inbox

The inbox schema permits `proposed`, `owner_confirmed`, `rejected`, `recorded`, `superseded`, and `blocked`. Chat-originated content is never authority automatically. Status-dependent schema rules require non-null owner confirmation for `owner_confirmed`, require both non-null owner confirmation and a non-null durable record for `recorded`, and require durable or supersession evidence for `superseded`. Failed validation or ambiguous provenance quarantines the item.

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

## Issue #49 Implementation In Review

Issue #49 and PR #50 move the read-only collector and deterministic derived startup-packet generator from architecture-only status to implementation in review. The collector uses standard-library validation, a positive read-command allowlist, canonical-versus-live comparison, fail-closed classification, external-only output, sensitive-data rejection, and deterministic hashing.

Version `1.3.0` binds the strictly resolved requested root to Git's strictly resolved top level and a valid `.git` directory or worktree control file. It normalizes only the four authorized GitHub HTTPS/SSH origin forms to `Zest-LeadGen/contractoros-california`. Generated evidence stores public-safe verification status, normalized transport and repository identity only; it never stores an absolute private root or raw credential-bearing remote. A readable contradiction is quarantined; unavailable required evidence is blocked.

Output validation is pre-mutation. The nearest existing ancestor is strictly resolved, nonexistent suffixes are projected, repository descendants and symlink redirection are rejected, and target object types are checked before directory creation. The boundary is rechecked after creation and atomic-write temporary files are cleaned on failure.

The Issue #49 implementation has no authority scope to mutate Git, GitHub, canonical state, approvals, merges, releases, budgets, credentials, policy, Phase 4K-9, or Phase 4I. A generated packet remains derived, public-safe, point-in-time evidence.

## Issue #55 Stage A Actor Contract In Review

Issue #49 is closed and PR #50 is merged at main SHA `7d00343c233e45185e6c4d77e50eb870f408c01f`. Issue #55 extends the merged collector with deterministic actor-bound interpretation, role-conflict denial, read-only repair, public-safe incident evidence, schema binding, and packet-hash integration.

The packet distinguishes descriptive program direction from one bounded next action or `NONE` for each developer, red-team, human-approver, and merge-operator role. For red-team, repository write, GitHub write, terminal mutation, implementation, human approval, merge, and issue-closeout authority scope remains none or no.

Stage A proves only the tested repository and startup-packet contract while its PR is in review. Full runtime isolation is not proven. Least-privilege credentials, write-tool removal, immutable repository access, external action-firewall enforcement, credential isolation, and mutation-escape tests remain Stage B requirements under separate future authority scope.
