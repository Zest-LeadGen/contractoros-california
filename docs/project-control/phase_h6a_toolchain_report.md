# H6-A Toolchain Baseline Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #64)

## Phase

H6-A.1 — reproducible toolchain, control half: pinned Node/npm, toolchain documentation and policy, dependency-selection evidence, scanner lockfile exemption, PA-0011. (H6-A.2 delivers the app manifests and lockfiles.)

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under owner H6 authorization (issue #118 comment 5235003178, owner-authored 2026-08-10T01:42:17Z; PA-0011, introduced via bootstrap, closing PA-0010). AUTOMATIC_CONTINUATION=NO.

## Scope

H6-A.1 — the Control / Infrastructure half of the toolchain baseline (H6-A.2, a separate Product / QA + Dependency-lane PR, delivers the app manifests and lockfiles; lane purity in the control-file update matrix forbids mixing them in one PR):

1. Node/npm pinned: `.nvmrc` v22.23.2 (22 LTS latest, read live from nodejs.org dist index); docs/TOOLCHAIN.md documents pins, package boundaries (deliberate no-workspace / no-root-manifest decision recorded), deterministic per-app `npm ci --prefix` install, update/rollback/vulnerability/license policy, and the test-layer ownership ledger.
2. Version selection for H6-A.2, verified dual-source: expo 57.0.11 (npm dist-tag latest), react 19.2.3 + react-native 0.86.2 (`npx expo install` AND expo's own bundledNativeModules.json agree). Evidence recorded separately from product claims in docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md: byte-identical two-directory lockfile re-resolution, clean `npm ci` (mobile 463 pkgs, web 20 pkgs + green vite build), sha256 digests binding the H6-A.2 artifacts in advance, license inventory (permissive/weak-copyleft only), five deliberate failure tests.
3. check_forbidden_scope.py: committed-lockfile paths exempted from implementation-term scanning (package names like whatwg-fetch legitimately contain term literals; lockfiles remain governed by the dedicated --lockfiles-only contamination/provenance scan, which still runs on those exact paths). Same disclosed-exemption pattern as H5-B's docs/archive and scripts/control exemptions.
4. PA-0011 (bootstrap, closing PA-0010) pre-authorizes both halves: this PR's paths and H6-A.2's exact manifest/lockfile/companion-report paths.

## Starting Main SHA

93777cc (post-H5-D reconciliation merge of PR #126).

## Changed Files

- .nvmrc (new), docs/TOOLCHAIN.md (new)
- scripts/control/check_forbidden_scope.py (lockfile term-scan exemption)
- docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md (new)
- docs/project-control/authorizations/PA-0011.json (new), PA-0010.json (supersession closure only)
- docs/project-control/phase_h6a_toolchain_report.md (this report), DECISION_LOG.md, DEVELOPMENT_LEDGER.md

H6-A.2 (separate follow-up PR, pre-authorized by PA-0011): apps/mobile/package.json + package-lock.json (new), apps/web/package.json + package-lock.json (engines sync), companion report.

## Commands Run

- Live version selection: nodejs.org dist index; npm view expo dist-tags.latest; npx expo install; bundledNativeModules.json cross-check
- Determinism: two-directory byte-identical `npm install --package-lock-only`; clean `npm ci` both apps; web `vite build` green
- Five deliberate failure tests (one produced a real finding — see Known Limitations)
- Six control validators against the real PR body pre-push; adversarial + continuity suites; armed checker self-test (bootstrap, closes PA-0010)

## Dependency / Lockfile Handling

No dependency or lockfile file changes in THIS PR. The dependency work (mobile latest→exact pins + new lockfile, PINNED_CHANGE; web engines metadata + 4-line lockfile sync) lands in H6-A.2 under Lane: Product / QA with the Dependency-lane approval phrases, pre-authorized by PA-0011 and pre-bound by the sha256 digests in the evidence file.

## Documentation Impact

docs/TOOLCHAIN.md is the new single source of truth for toolchain pins and package boundaries; evidence file records toolchain proof independently from product-readiness claims (issue #64 item 9).

## Validation Evidence

See docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md (digests, proofs, license inventory, failure-test transcript summary). Armed phase-authorization gate validates this PR in bootstrap mode (closed_records=[PA-0010]).

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required (the npm-ci/latest gap is tracked as an H6-B work item in TOOLCHAIN.md and the evidence file, becoming a register entry only if H6-B does not land it).

## Decision Log Impact

Adds the H6-A entry: version-selection provenance, no-workspace decision, and the npm-ci/latest finding.

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required.

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — toolchain documentation, evidence, authorization records, and one disclosed scanner exemption (check_forbidden_scope.py, walk-through required per R-STRESS-002) only; no app files in this PR; no backend/auth/database/deployment/release/app-store work; no dependency selected "because newest" (the H6-A.2 pins are the Expo SDK 57 compatibility set, the deliberate supported baseline); no workflows, policy, or state snapshot touched.

## Claim Level

Toolchain baseline only. A clean checkout with pinned tooling installs deterministically from committed public-safe lockfiles (proven). No product-readiness claim; product capability remains prototype. CI wiring (mobile static validation, lint/typecheck/test layers, manifest pin scan) is H6-B.

## Known Limitations

- REAL FINDING from deliberate failure testing: `npm ci` does NOT reject a `"latest"` dist-tag reintroduced into a manifest (it installs whatever the lockfile pins). Manifest pinning is currently enforced by review; a dedicated manifest pin scan is a named H6-B deliverable.
- Lane purity forced the two-PR split: H6-A.2 (apps manifests + lockfiles) can only be opened after this PR merges, because the armed checker resolves its base-mode authorization (PA-0011) from the base commit. Two sequential owner key-turns for H6-A are the honest cost of the armed wall plus lane purity.
- A root orchestration manifest was drafted and deferred to H6-B (Dependency lane; no value before CI jobs exist). The deliberate no-workspace decision stands and is recorded in TOOLCHAIN.md.
- The web-ci workflow still pins node-version "22" inline; aligning it to `.nvmrc` (node-version-file) is H6-B (workflow paths are outside PA-0011 by design).
- Mobile validation is dependency-level (install determinism, peer compatibility); bundle/static validation requires the H6-B CI job.
- Local resolution ran on node 26/npm 12 (resolution host); consumption environments are held to the Node 22 pin via .nvmrc/engines, and engines are advisory without engine-strict — CI enforcement lands in H6-B.

## Next Phase Status

Next: H6-B — product CI (mobile static/bundle validation, lint/format/typecheck/unit/coverage wiring, manifest pin scan, node-version-file alignment) + control hardening (R-STRESS-002: run checkers from main; flag control-file PRs). Same H6 authorization (5235003178); new PA record per PR. AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Toolchain baseline pins, new lockfile, and dependency policy; owner review required.
