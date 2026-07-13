# Red-Team Startup Packet Specification

## Status And Decision Boundary

This specification governs the Issue #49 implementation in review. A generated `RED_TEAM_STARTUP_PACKET.md` is derived, non-authoritative, point-in-time evidence. It grants no write, approval, review, merge, release, spending, credential, policy, Phase 4K-9, or Phase 4I decision power.

The packet supplements versioned public-safe state with live read-only evidence. It does not replace GitHub, exact-SHA external review, human/write-access approval, branch protection, merge verification, or issue closeout.

## Inputs And Provenance

Fixture mode consumes a bounded JSON fixture plus an explicit observation timestamp. Live mode consumes an explicit repository root, repository identity, issue number, pull request number, workflow-run ID, exact canonical Git ref, observation timestamp, and external output directory.

Live provenance includes bounded local Git metadata; canonical state read from the exact ref; issue, pull request, checks, workflow run and step evidence; owner-trigger and red-team marker status; normalized pull-request reviews; calculated repository-permission evidence for sourced candidates; deterministic qualifying and disqualified approvals; auto-merge state; comparison findings; blockers; and gaps. Raw credentials, headers, environment contents, review bodies, unrelated comment bodies, and unrestricted command output are not persisted.

The version `1.3.8` scope-bound evidence contract binds active-family classification to collected local HEAD equals PR head, repository default branch and PR base equal `main`, and run SHA/branch equals the PR. It captures normalized public-safe worktree hashes before and after authoritative reads; both must be clean and equal. Closed-gate classification also requires PR base equal to the verified default branch and binds collected local HEAD, local main, and merge commit to verified live main without conflating that post-merge SHA with the pre-merge PR head. Nullable authoritative PR keys are presence-bound; only a null auto-merge request is inactive, and a non-null Issue `closedAt` must be RFC3339. Completed live runs, jobs, and steps require a nonempty conclusion. Decisive review timestamps must be valid RFC3339 and non-null before selection. Canonical schema version and lifecycle state are nonempty strings, canonical lifecycle/consistency values are compared against the active or closed family, and the canonical source ref is a required exact lowercase 40-character SHA. The generator and both generated schemas use `1.3.8`; every current fixture uses `fixture_version: 1.3.8`. Absolute repository paths and raw remote URLs are never persisted.

## Read-Only Command Security

Every subprocess uses an argument array, `shell=False`, a finite timeout, size-bounded captured standard output and error, and a normalized return code. A positive allowlist admits only the exact Git reads, one fixed repository GraphQL query, and narrowly shaped GitHub CLI reads documented in `scripts/continuity/README.md`.

Unrestricted shells are forbidden. For each live invocation, the firewall accepts only exact ordered command vectors bound to the fixed repository, Issue #49, PR #50, the supplied workflow-run ID, and fixed JSON fields; `gh repo view` is unused and forbidden. The only permitted GraphQL call is the fixed repository identity/default-branch query; it accepts no mutation or caller-supplied fields. The only permitted REST calls are sequential review pages 1 through 5 for PR #50 and calculated permission reads for logins originating in normalized exact-head review evidence. Both REST routes use GET. Review pages use 100 records, stop on the first short page, and block when page 5 is full. The source-command evidence bound is derived as 14 fixed reads plus five review pages plus 100 permission candidates, or 119 total; one above that fails closed. Every other `gh api` shape, Git remote-ref, branch, index, worktree, remote mutation, and GitHub issue, pull-request, review, approval, merge or closeout mutation is forbidden. Unknown executables, subcommands, flags, and command shapes are rejected.

## Qualifying Human Approval

Review records are sorted deterministically by parsed UTC submission instant, numeric review ID, then stable record content. Per reviewer, the latest submitted current-head decisive state among `APPROVED`, `CHANGES_REQUESTED`, and `DISMISSED` governs. A later comment is non-decisive. Duplicate review IDs, contradictory duplicates, malformed exact-commit binding, permission identity mismatch, stale-as-current representation, bot/author qualification, or a coarse approved decision without a computed qualifying approver is quarantined.

Qualification requires a submitted `APPROVED` record bound to the exact current PR head, a non-empty reviewer login, reviewer account type `User`, separation from the PR author, permission evidence for the same repository and login, and calculated base permission `write` or `admin`. Maintain access qualifies through GitHub's base-permission mapping to `write`; triage maps to `read` and does not qualify. Author association, login text, an earlier head, bot identity, pending/dismissed/superseded state, read/none/unknown permission, or inaccessible evidence does not qualify.

The collector persists only bounded public-safe review identity/state/binding fields, permission identity/role fields, and deterministic worktree hashes/booleans. Before normalization, each permission response must be an object with an allowed calculated permission, a bounded nonempty role name, and a valid supported user whose canonical case-folded login exactly matches the requested candidate. Missing, inaccessible, mismatched, or malformed review or permission evidence is blocked with exit `3`; command-shape rejection remains exit `5` and unsafe evidence remains exit `4`. A full fifth review page is truncated and blocked. External exact-SHA red-team evidence and qualifying human approval remain separate categories; neither substitutes for the other.

## Canonical And Live Comparison

Canonical state is a sanitized observed snapshot with no live decision power. Before comparison, the collector requires a bounded linked-issue object with a positive integer number and supported state, plus a bounded linked-PR object with a positive integer number, supported state, and null or exact lowercase observed head SHA. Documented optional linked-PR fields retain their canonical types; unsupported nested properties or types are invalid input and return exit `5` without a traceback. The collector then compares canonical main, linked issue, linked pull request identity, observed head when present, lifecycle state, and consistency status with local and live evidence.

Supported classifications are exactly:

- `consistent`
- `requires_live_verification`
- `stale`
- `blocked`
- `quarantined`

For an active developer pull request, absent external red-team evidence and absent human approval are expected pending blockers. A valid active snapshot may return `requires_live_verification` and exit `0`, but it cannot permit merge or downstream writes.

An active PR requires an open issue, open non-draft PR based on `main`, no merge commit or merge timestamp, inactive auto-merge, exact provenance, and a valid owner-trigger marker. It permits either the expected missing-marker workflow failure or a valid current-head marker with a fully successful workflow.

`externally_approved` additionally requires the valid exact-current-head red-team marker and fully successful workflow. Human/write approval is not required to prove external approval; when absent, it remains pending and merge readiness is not claimed. `merge_ready` additionally requires at least one qualifying exact-current-head human/write approval while the PR remains open, non-draft, unmerged, and auto-merge inactive. The collector grants no merge power.

For a merged/closed gate, `merged_at`, merge SHA equal to verified live main, required control evidence, exact-SHA review bound to the pre-merge PR head, human approval, successful head-bound workflow evidence, Issue state `closed` with reason `completed`, canonical linkage, and closeout state must agree. Contradiction is quarantined; inaccessible required evidence is blocked.

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

The caller must supply an output directory outside the repository. Before creation, the collector resolves the nearest existing ancestor, projects nonexistent suffixes, and rejects the repository root, prospective repository descendants, symlink redirection into the repository, an output-directory symlink, output-file symlinks, and non-regular targets. It creates only a passing external directory, strictly resolves and rechecks it, then writes exactly `continuity-evidence.json` and `RED_TEAM_STARTUP_PACKET.md` through atomic replacement with cleanup.

The caller's absolute home path must not enter generated evidence. A live generated packet or evidence manifest must not be committed.

## Sensitive-Data Controls

Private-looking or unsafe material fails closed. Forbidden categories include GitHub token forms, bearer values, API-key or secret assignments, cloud credential identifiers, passwords, private keys, authorization headers, local absolute home paths, private customer information, and confidential owner, legal, vendor, or budget material.

The collector avoids gathering data that would require broad redaction. Sanitization cannot convert unsafe material into decision power. Only an approved public-safe opaque identifier or hash may represent a governed private source.

## Packet Content

The rendered packet contains generator and schema versions, observation timestamp, repository identity, source SHAs, canonical schema version, issue and pull-request lifecycle evidence, exact pull-request head, workflow evidence, marker status and binding, human approval state, auto-merge state, classification, quarantine flag, comparison findings, blockers, gaps, the single next action, stop conditions, prohibited actions, evidence classification, a derived notice that grants no authority, and packet hash.

The packet contains no write permission. It must be revalidated against live evidence before consequential action.

## Schemas And Runtime Validation

`docs/project-control/state/red-team-continuity-evidence.schema.json` and `docs/project-control/state/red-team-startup-packet.schema.json` use Draft 2020-12, required properties, bounded enums, SHA patterns, date-time and URI formats, typed arrays, unique items where applicable, and nested `additionalProperties: false`.

No third-party schema validator is added. Standard-library runtime validation checks exact allowed keys, documented types, supported values and bounded counts for repository, issue, pull request, checks, workflow run, jobs, steps, markers, auto-merge and optional source-command evidence before classification, rendering or output. Malformed fixture/evidence structures return exit `5` without a traceback; malformed authoritative live responses return unavailable-evidence exit `3`.

## C3.6 correction contract

The `1.3.6` contract stages exact four-field collected review evidence before deriving the exact seven-field normalized review. Fixture claims are compared with recomputation; original reason-map keys must map one-to-one to canonical reviewer identities before structural validation, comparison, rendering, or map construction. Case-only or other canonical collisions return fixture exit `5`; malformed authoritative live evidence blocks with exit `3`. `_evidence` is a separate schema property and accepts only `APPROVAL_REVIEW_RECORD_MALFORMED`; reviewer keys accept the complete supported reviewer-specific reason enum. The sole accepted status command includes explicit `--untracked-files=all`; clean equal status hashes and equal exact `HEAD` values are required before and after authoritative reads. Live `OPEN` requires null `closedAt`; live `CLOSED` requires a valid non-null timestamp, with matching normalized open/closed closeout state.

## C3.7 Adverse Review And Source-Command Semantics

The `1.3.7` evaluator reduces the latest submitted exact-current-head decisive state for every reviewer, including reviewers with no approval record. Current-head `CHANGES_REQUESTED` remains adverse through later comments and through another reviewer's qualifying approval; the same reviewer's later current-head approval or dismissal clears it. Historical-head change requests remain deterministic normalized evidence without becoming current-head blockers. Aggregate `CHANGES_REQUESTED` is adverse, and neither `CHANGES_REQUESTED` nor `REVIEW_REQUIRED` may support merge-ready or closed-gate consistency.

Nonempty source-command claims are semantically validated against the exact evidence-derived live firewall. Repository, issue, pull request, run, canonical ref, JSON-field ordering, review page, page size, method, endpoint, flag set, and dynamically sourced permission identity must match exactly, and every recorded return code must be zero. Prohibited or unrelated commands, pages outside 1–5, unsourced permission reads, argument reordering, extra flags, and failed command results return malformed-input exit `5` before classification or output. Empty synthetic source-command lists remain valid.

## C3.8 Validation Ordering And Provenance Contract

The `1.3.8` evaluator validates the complete collected four-field or evaluated seven-field review object before semantic source-command validation can read any review record. Wrong review types, missing keys, malformed lists or records, invalid login/timestamp/commit/permission evidence, and malformed derived claims return fixture exit `5` without traceback or output; malformed authoritative live evidence remains unavailable-evidence exit `3`.

Every fixture and live output requires `source_shas.canonical_ref` as a non-null exact lowercase 40-character SHA. Both source-SHA schemas use a dedicated non-null SHA definition for this field without changing nullable SHA fields such as `merge_commit`. Packet rendering always includes the validated exact canonical source ref, and the firewall cannot construct a canonical `git show` command until this provenance passes validation.

Command-result runtime and evidence-schema contracts both permit only a successful result. Runtime requires an integer equal to zero, and the generated-evidence schema fixes `return_code` to `const: 0`; nonzero, negative, string, boolean, float, and null runtime values fail closed.
