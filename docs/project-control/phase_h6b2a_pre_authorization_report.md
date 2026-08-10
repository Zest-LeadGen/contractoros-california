# H6-B.2a Pre-Authorization Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #64)

## Phase

H6-B.2a — authorization record and design decisions for the H6-B.2 test layers (Product / QA half follows in base mode).

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under owner H6 authorization (issue #118 comment 5235003178; PA-0017 via bootstrap, closing PA-0016). AUTOMATIC_CONTINUATION=NO.

## Scope

PA-0017 pre-authorizes H6-B.2's exact paths (H6-A lane-purity pattern): app manifests + lockfiles (lint devDependencies), flat eslint configs, node:test unit suites on the data modules, evidence file, companion report. Design decisions recorded in DECISION_LOG: zero-dependency unit+coverage layer via Node 22's built-in test runner; exactly three exact-pinned lint packages per app (eslint 10.8.1, @eslint/js 10.0.1, globals 17.9.0 — resolved live, engines verified against the .nvmrc pin); type checking recorded N/A-by-design for the JavaScript scaffolds; React lint rulesets and component/DOM tooling tracked, not silently omitted; CI step enforcement deferred to the H6 closeout PR so steps never precede the scripts they run.

## Starting Main SHA

a0993e3 (post-H6-B.1 reconciliation merge of PR #133).

## Changed Files

- docs/project-control/authorizations/PA-0017.json (new; bootstrap), PA-0016.json (supersession closure only)
- docs/project-control/phase_h6b2a_pre_authorization_report.md (this report)
- docs/project-control/DECISION_LOG.md, docs/project-control/DEVELOPMENT_LEDGER.md

## Commands Run

- Live version resolution (npm view) for the three lint packages; eslint 10 engines check vs the Node pin
- Six control validators + pin gate against the real PR body pre-push; armed checker self-test (bootstrap, closes PA-0016)

## Dependency / Lockfile Handling

None in THIS PR. H6-B.2 (pre-authorized here) adds the three lint packages per app as exact-pinned devDependencies with regenerated lockfiles, determinism proofs, and license records — classification NEW_DEPENDENCY, carried on PA-0017.

## Documentation Impact

Control records only.

## Validation Evidence

Armed checker (both wall jobs) validates this PR in CI; validators green vs real body.

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required.

## Decision Log Impact

Adds the H6-B.2 design-decision entry (zero-dep unit layer, lint dep set, typecheck N/A, CI-steps-last sequencing).

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required.

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — authorization records and control documentation only; no app files, scripts, workflows, state snapshot, or governance mutation in this PR (app source directories are explicitly forbidden_paths in PA-0017 — the test-layer PR may add configs and tests but never touch src/).

## Claim Level

Authorization record and design decisions only; no test layer exists until H6-B.2 merges.

## Known Limitations

Two sequential key-turns for H6-B.2 (this record, then the Product / QA half) — the armed wall reads authorization from the base commit, so pre-authorization must merge first.

## Next Phase Status

Next: H6-B.2 (Product / QA test layers, base mode under PA-0017), then the H6 closeout control PR (CI step enforcement + closeout records). AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Authorization-record bootstrap defining the test-layer scope; owner review required.
