# H6-A.2 Dependency Pins Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #64)

## Phase

H6-A.2 — reproducible toolchain, dependency half: pinned app manifests and public-registry lockfiles. Companion to the merged H6-A.1 control half (PR #127).

## Lane

Product / QA

Lane: Product / QA — explicit owner approval (issue #118 comment 5235003178, H6 owner authorization).

Lane: Dependency — approved dependency lane under explicit owner approval (issue #118 comment 5235003178, H6 owner authorization; PA-0011 pre-authorizes these exact paths).

## Authority <!-- documentation scope -->

Under owner H6 authorization (issue #118 comment 5235003178; PA-0011, live at base since PR #127 — this PR runs the armed checker in base mode, its first base-mode exercise). AUTOMATIC_CONTINUATION=NO.

## Scope

The four app files pre-authorized and digest-bound by H6-A.1: apps/mobile/package.json (the three `latest` declarations replaced with the Expo SDK 57 compatibility set — expo 57.0.11, react 19.2.3, react-native 0.86.2 — plus engines pin), apps/mobile/package-lock.json (new; sha256 89bc1562f91b341e0a528249a28c29dd1fda6223ca51c88a87fb2e20494c834c, byte-equal to the evidence-bound baseline), apps/web/package.json (engines pin only), apps/web/package-lock.json (root-entry engines sync only, 4-line diff; sha256 4741f1e5437f060898f7f3ac61bb0d6d56e6cc856c5d43b2938479bf575b71be, digest-match to evidence). No source code changes.

## Starting Main SHA

0b27369 (H6-A.1 merge of PR #127).

## Changed Files

- apps/mobile/package.json (pins + engines), apps/mobile/package-lock.json (new)
- apps/web/package.json (engines), apps/web/package-lock.json (engines sync)
- docs/project-control/phase_h6a_dependency_pins_report.md (this companion report)

## Commands Run

- Digest verification against docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md (both lockfiles byte-match the pre-bound sha256 values)
- Determinism/provenance proofs recorded in that evidence file (byte-identical re-resolution, clean npm ci mobile 463 pkgs / web 20 pkgs + green vite build, 100% registry.npmjs.org, contamination scans clean)
- Six control validators against the real PR body pre-push; armed checker base-mode self-test vs PA-0011

## Dependency / Lockfile Handling

dependency classification: PINNED_CHANGE. Mobile latest→exact (Expo SDK 57 set, dual-source verified in H6-A.1 evidence); new mobile lockfile; web engines metadata only, no web dependency changes. Both lockfiles pass the dedicated --lockfiles-only contamination/provenance scan; term-scan exemption for lockfile paths landed in H6-A.1 with owner walk-through.

## Documentation Impact

None beyond this companion report — docs/TOOLCHAIN.md (merged in H6-A.1) already documents this baseline.

## Validation Evidence

docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md (merged, H6-A.1) is the evidence of record; this PR's artifacts byte-match its digests. Armed phase-authorization gate validates this PR in base mode under PA-0011.

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required (H6-A.1 recorded the npm-ci/latest finding routing).

## Decision Log Impact

docs/project-control/DECISION_LOG.md: reviewed, no update required (the H6-A.1 entry records the split and both halves; ledger and decision log updates for docs/project-control are Control-lane and landed there).

docs/project-control/DEVELOPMENT_LEDGER.md: reviewed, no update required (the H6-A.1 ledger block covers both halves of H6-A, including this PR's scope).

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required (explicit owner approval per the dependency-lane rule).

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — dependency manifests and lockfiles only; no source code, no backend/auth/database/deployment/release/app-store work; no dependency moved "because newest" (Expo SDK 57 compatibility set is the deliberate supported baseline); no control files beyond this companion report.

## Claim Level

Dependency pinning only. Deterministic install from committed public-safe lockfiles is proven at the toolchain level; no product-readiness claim — product capability remains prototype.

## Known Limitations

- npm ci does not reject reintroduced `latest` dist-tags (H6-A.1 real finding); pin scan is a named H6-B deliverable — until then manifest pinning is review-enforced.
- Mobile CI (install + static/bundle validation in CI) lands in H6-B; this PR proves the artifacts locally against the recorded evidence only.

## Next Phase Status

Next: H6-B — product CI (mobile job, lint/typecheck/test wiring, manifest pin scan, node-version-file alignment, root-manifest decision) + R-STRESS-002 control hardening. Same H6 authorization; new PA record per PR. AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Dependency pins and new lockfile under explicit owner approval; owner review required.
