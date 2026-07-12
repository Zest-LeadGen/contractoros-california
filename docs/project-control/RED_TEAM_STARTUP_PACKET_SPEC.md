# Red-Team Startup Packet Specification

## Status And Decision Boundary

This specification governs the Issue #49 implementation in review. A generated `RED_TEAM_STARTUP_PACKET.md` is derived, non-authoritative, point-in-time evidence. It grants no write, approval, review, merge, release, spending, credential, policy, Phase 4K-9, or Phase 4I decision power.

The packet supplements versioned public-safe state with live read-only evidence. It does not replace GitHub, exact-SHA external review, human/write-access approval, branch protection, merge verification, or issue closeout.

## Inputs And Provenance

Fixture mode consumes a bounded JSON fixture plus an explicit observation timestamp. Live mode consumes an explicit repository root, repository identity, issue number, pull request number, workflow-run ID, exact canonical Git ref, observation timestamp, and external output directory.

Live provenance includes bounded local Git metadata; canonical state read from the exact ref; issue, pull request, checks, workflow run and step evidence; owner-trigger and red-team marker status; normalized pull-request reviews; calculated repository-permission evidence for sourced candidates; deterministic qualifying and disqualified approvals; auto-merge state; comparison findings; blockers; and gaps. Raw credentials, headers, environment contents, review bodies, unrelated comment bodies, and unrestricted command output are not persisted.

The version `1.2.0` evidence contract requires PR author identity and account type; approval evidence status; normalized review and permission records; qualifying and disqualified reviewer lists; stable disqualification reasons; PR head branch; check link; workflow identity; event; run head branch; bounded jobs; and numbered step status/conclusion evidence. The generator and both generated schemas use `1.2.0`; every fixture uses `fixture_version: 1.2.0`. This is scope-bound approval evidence only.

## Read-Only Command Security

Every subprocess uses an argument array, `shell=False`, a finite timeout, size-bounded captured standard output and error, and a normalized return code. A positive allowlist admits only the exact Git reads and narrowly shaped GitHub CLI reads documented in `scripts/continuity/README.md`.

Unrestricted shells are forbidden. The only permitted REST calls are sequential review pages 1 through 5 for PR #50 and calculated permission reads for logins originating in normalized exact-head review evidence. Both routes use GET. Review pages use 100 records, stop on the first short page, and block when page 5 is full. Review and permission-candidate counts are bounded. Every other `gh api` shape, Git remote-ref, branch, index, worktree, remote mutation, and GitHub issue, pull-request, review, approval, merge or closeout mutation is forbidden. Unknown executables, subcommands, flags, and command shapes are rejected.

## Qualifying Human Approval

Review records are sorted deterministically by submission timestamp and numeric review ID. Per reviewer, the latest submitted current-head decisive state among `APPROVED`, `CHANGES_REQUESTED`, and `DISMISSED` governs. A later comment is non-decisive. Duplicate review IDs, contradictory duplicates, malformed exact-commit binding, permission identity mismatch, stale-as-current representation, bot/author qualification, or a coarse approved decision without a computed qualifying approver is quarantined.

Qualification requires a submitted `APPROVED` record bound to the exact current PR head, a non-empty reviewer login, reviewer account type `User`, separation from the PR author, permission evidence for the same repository and login, and calculated base permission `write` or `admin`. Maintain access qualifies through GitHub's base-permission mapping to `write`; triage maps to `read` and does not qualify. Author association, login text, an earlier head, bot identity, pending/dismissed/superseded state, read/none/unknown permission, or inaccessible evidence does not qualify.

The collector persists only bounded public-safe review identity/state/binding fields and bounded permission identity/role fields. Missing or inaccessible review or permission evidence is blocked. A full fifth review page is truncated and blocked. External exact-SHA red-team evidence and qualifying human approval remain separate categories; neither substitutes for the other.

## Canonical And Live Comparison

Canonical state is a sanitized observed snapshot with no live decision power. The collector compares canonical main, linked issue, linked pull request, observed head when present, lifecycle state, and consistency status with local and live evidence.

Supported classifications are exactly:

- `consistent`
- `requires_live_verification`
- `stale`
- `blocked`
- `quarantined`

For an active developer pull request, absent external red-team evidence and absent human approval are expected pending blockers. A valid active snapshot may return `requires_live_verification` and exit `0`, but it cannot permit merge or downstream writes.

For a pull request claiming external approval or merge eligibility, a missing or stale marker is quarantined, a marker bound to another SHA is quarantined, missing required human approval is blocked or quarantined, and active auto-merge is quarantined.

For a merged/closed gate, merge SHA, main evidence, required control evidence, exact-SHA review, human approval, workflow evidence, and linked-issue closeout must agree. Contradiction is quarantined; inaccessible required evidence is blocked.

## Workflow And Required-Check Binding

The trusted run must belong to repository `Zest-LeadGen/contractoros-california`, workflow `ContractorOS Control Gates` with database ID `309083557`, event `pull_request`, the exact current PR head SHA and branch, and exactly one `contractoros-control-gates` job. Exactly one same-named PR check must link to the supplied run ID. Matching SHA alone is insufficient.

The expected job must contain exactly one ordered occurrence of each governed workflow step. A valid pre-review run is completed/failure with every pre-marker step successful, the marker step failed while marker evidence is missing, both post-marker steps skipped, and the linked check failed. A valid post-review run requires a valid exact-head marker and success for every governed step, job, run, and linked check. Missing required jobs or steps are blocked. Identity mismatches, duplicate jobs or steps, invalid ordering, pre-marker failures, premature post-marker success, unexplained run failures, and check contradictions are quarantined. Pending or in-progress runs remain blocked and cannot support external approval, merge readiness, or completed-gate status.

## Exit Contract

- Exit `0`: `consistent` or valid `requires_live_verification` packet generated.
- Exit `2`: `stale` or `quarantined` evidence.
- Exit `3`: required evidence missing or inaccessible, classified `blocked`.
- Exit `4`: unsafe/private evidence or prohibited output path.
- Exit `5`: invalid arguments, malformed input, malformed canonical state, or schema failure.

No stale, blocked, quarantined, or unsafe result returns exit `0`.

## Deterministic Rendering And Hashing

The normalization rule is UTF-8, LF newlines, stable headings, stable list order, stable JSON key order, no trailing whitespace, and exactly one final newline.

`packet_hash` is SHA-256 over the canonical rendered packet payload excluding the displayed `Packet Hash` heading and value. The displayed hash is appended after hashing. The evidence JSON records the rule, and tests independently remove the displayed hash section and recompute the digest.

Fixture runs with identical inputs, timestamp, and arguments must produce byte-for-byte identical JSON evidence, Markdown packet, ordered evidence lists, and packet hash. Changing material fixture evidence changes the packet hash.

## Output Boundary

The caller must supply an output directory outside the repository. The collector resolves paths and rejects the repository root, repository descendants, a directory symlink resolving into the repository, and an output-file symlink. It writes exactly `continuity-evidence.json` and `RED_TEAM_STARTUP_PACKET.md` using safe atomic replacement within the approved external directory.

The caller's absolute home path must not enter generated evidence. A live generated packet or evidence manifest must not be committed.

## Sensitive-Data Controls

Private-looking or unsafe material fails closed. Forbidden categories include GitHub token forms, bearer values, API-key or secret assignments, cloud credential identifiers, passwords, private keys, authorization headers, local absolute home paths, private customer information, and confidential owner, legal, vendor, or budget material.

The collector avoids gathering data that would require broad redaction. Sanitization cannot convert unsafe material into decision power. Only an approved public-safe opaque identifier or hash may represent a governed private source.

## Packet Content

The rendered packet contains generator and schema versions, observation timestamp, repository identity, source SHAs, canonical schema version, issue and pull-request lifecycle evidence, exact pull-request head, workflow evidence, marker status and binding, human approval state, auto-merge state, classification, quarantine flag, comparison findings, blockers, gaps, the single next action, stop conditions, prohibited actions, evidence classification, a derived notice that grants no authority, and packet hash.

The packet contains no write permission. It must be revalidated against live evidence before consequential action.

## Schemas And Runtime Validation

`docs/project-control/state/red-team-continuity-evidence.schema.json` and `docs/project-control/state/red-team-startup-packet.schema.json` use Draft 2020-12, required properties, bounded enums, SHA patterns, date-time and URI formats, typed arrays, unique items where applicable, and nested `additionalProperties: false`.

No third-party schema validator is added. Standard-library runtime validation checks the bounded fixture and canonical-state contract before classification or output.
