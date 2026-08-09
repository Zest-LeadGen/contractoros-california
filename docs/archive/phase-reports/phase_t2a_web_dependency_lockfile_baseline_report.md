# T2-A Web Dependency Lockfile Baseline Gate Report

## Linked Phase Issue

Phase issue: #89

Parent issue: #79

## Phase

T2-A — Web Dependency Pinning and Lockfile Baseline (first half of owner decision T2 on Issue #89; completes the Phase 4K-5 blocked work)

## Lane

Product / QA

Lane: Product / QA

Lane: Dependency

This delivery carries the approved dependency lane under explicit owner approval recorded on Issue #89 (owner decision T2 plus the premise-correction record of 2026-08-08). The dependency-lane files are `apps/web/package.json` and `apps/web/package-lock.json` only.

## Authority <!-- documentation scope -->

Owner decision T2 on Issue #89 with its premise-correction record. This phase grants no production, release, publication, app-store, backend, database, or content scope and does not unfreeze general product development. The companion CI workflow lands separately in the T2-B Control / Infrastructure PR to keep this PR lane-clean.

## Scope

Replace the four floating "latest" dependency specifiers in `apps/web/package.json` with exact pins and commit the generated `apps/web/package-lock.json`. No JS/JSX/CSS source file, mobile file, root file, workflow, or control-doc file is changed in this PR.

## Starting Main SHA

`9c3481cfc657269cebda58fe35df27c10ce6f9b9`

## Changed Files

- `apps/web/package.json`
- `apps/web/package-lock.json` (new)
- `docs/project-control/phase_t2a_web_dependency_lockfile_baseline_report.md` (new companion report)

No other path is changed.

## Commands Run

- Read-only scope: `npm view <pkg> version` against the public registry for the four dependencies.
- `npm install --no-audit --no-fund` in `apps/web` — generated the lockfile (19 packages).
- `rm -rf node_modules dist && npm ci --no-audit --no-fund` — clean reproduction from the lockfile only (20 packages, 292ms).
- `npm run build` — vite build succeeded on both the install path and the ci path; 29 modules transformed; `dist/index.html` plus hashed assets produced.
- `npm ls --depth=0` — exact tree: react 19.2.8, react-dom 19.2.8, vite 8.2.1, @vitejs/plugin-react 6.0.5.

## Dependency / Lockfile Handling

Floating `"latest"` specifiers are replaced with exact pins. Runtime dependencies (react, react-dom) are separated from build tooling (vite, @vitejs/plugin-react) in `devDependencies`. The lockfile was generated against `https://registry.npmjs.org/` with no committed `.npmrc`; local install scripts were constrained by the owner's machine-level allow-scripts allowlist. `node_modules/` and `dist/` remain gitignored and uncommitted. Future dependency changes remain Dependency-lane gated with this lockfile as the drift baseline.

## Documentation Impact

This companion report is the documentation for the dependency baseline. The durable decision-log, risk-register, and ledger records for the T2 program land in the T2-B Control / Infrastructure PR to keep this PR lane-clean:

`docs/project-control/RISK_REGISTER.md: reviewed, no update required`

`docs/project-control/DEVELOPMENT_LEDGER.md: reviewed, no update required`

`docs/project-control/DECISION_LOG.md: reviewed, no update required`

## Validation Evidence

- Clean-room reproduction: `npm ci` from the committed lockfile alone, followed by a successful `vite build`, on the developer machine.
- Exact dependency tree verified with `npm ls --depth=0`.
- Registry provenance: public npm registry; no lockfile entry resolves outside `registry.npmjs.org`.

## Validation Results

- `npm ci`: 20 packages, no missing peer or engine errors.
- `npm run build`: succeeded, 29 modules, output sanity confirmed (`dist/index.html`, hashed JS and CSS assets).
- Hosted control-gate outcomes for this PR are `LIVE_GITHUB_REQUIRED` and cannot be asserted from repository text.

## Risk Register Impact

The floating-dependency risk record (R-T2-DEP-001) lands in the T2-B control PR together with the other durable records; this PR contains the mitigation itself (pins plus lockfile).

## Decision Log Impact

The T1–T4 owner decisions and the dependency-provenance decision are recorded in the T2-B control PR. This companion report documents the product-lane delivery only.

## Artifact Index Impact

No artifact index update is required. Build outputs remain gitignored; no binary, archive, release, hosted, or external artifact is created.

`docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required`

## Red-Team Status

No review of this PR has occurred yet. The developer did not self-review and did not add a `RED_TEAM_DECISION` marker. Per the owner-selected both-keys flow, an owner-directed verification review with disclosed non-independence will follow delivery at the exact head SHA.

## Human Approval Status

Human/write-access approval is not granted by this report and remains required before merge.

## Auto-Merge Status

Auto-merge is inactive and ineligible. No automatic continuation is authorized.

## Forbidden Scope Confirmation

- [x] No product source (JS/JSX/CSS), mobile, content, backend, or database mutation.
- [x] No workflow, control-validator, credential, secret, or governance-repository mutation in this PR.
- [x] No deployment, release, production, publication, or app-store mutation.
- [x] No additional dependency beyond pinning the four already-declared packages.
- [x] No review, approval, merge, issue closeout, or next-phase start within this delivery.

Forbidden scope confirmation: confirmed for this bounded dependency-baseline delivery.

## Claim Level

Local install and build proof with a committed lockfile baseline only. This does not prove hosted CI success (T2-B pending), product correctness, cross-platform behavior, production capability, or release readiness.

## Known Limitations

Exact pins do not freeze transitive security advisories; audit posture is a future H7A concern. The build proves compilation, not behavior; no test suite exists for apps/web yet. The hosted CI that enforces this baseline on every PR is delivered in T2-B and is not active until that PR merges.

## Remaining Gates

1. Hosted control-gates run on this PR head.
2. Owner-directed verification review at the exact head SHA (both-keys flow, disclosed non-independence).
3. Human/write-access approval and protected merge.
4. Verify `main`.
5. Deliver T2-B (CI workflow plus durable control records), which activates enforcement.

## Next Phase Status

T2-B (Control / Infrastructure: web-ci workflow plus decision-log, risk-register, and ledger records) follows after this PR merges. No other phase is authorized. `NEXT_GATE=HOSTED_GATES_THEN_OWNER_DIRECTED_REVIEW`.

## Owner Trigger / Lane Eligibility Evidence

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: DEPENDENCY_SECURITY_RISK_ACCEPTANCE
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: First committed dependency tree for the product; owner review of the exact pinned versions is required before merge.
