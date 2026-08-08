# T2-B Web CI Workflow Gate Report

## Linked Phase Issue

Phase issue: #89

Parent issue: #79

## Phase

T2-B — Hosted Web CI Workflow and Durable Reform Records (second half of owner decision T2 on Issue #89; depends on the merged T2-A lockfile baseline)

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Owner decision record and premise correction on Issue #89 (2026-08-08) authorize this bounded phase: add the hosted web CI workflow and land the durable T1-T4 reform records. The dependency baseline itself was delivered by the merged T2-A PR. This phase grants no production, release, publication, app-store, backend, database, or content authority and does not unfreeze general product development.

## Scope

Add one hosted workflow that proves install-from-lockfile and build on every web-touching PR and main push, and land the durable decision-log, risk-register, and ledger records for the T1-T4 reform. No apps/, mobile, root, backend, or governance-repository path is changed in this PR.

## Starting Main SHA

`9c3481cfc657269cebda58fe35df27c10ce6f9b9`

## Changed Files

- `.github/workflows/web-ci.yml` (new)
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/phase_t2b_web_ci_workflow_report.md` (new)

No other path is changed.

## Commands Run

- Read-only scope: local dry-proof of the exact CI command path (`npm ci` from the T2-A lockfile followed by `npm run build`) succeeded on the developer machine; evidence is recorded in the merged T2-A companion report.
- Control validators and continuity tests — results in `## Validation Results`.

## Dependency / Lockfile Handling

No dependency or lockfile path is changed in this PR. The workflow consumes the lockfile committed by the merged T2-A PR; no install, package-manager, or dependency-resolution command runs in this delivery.

## Documentation Impact

The decision log records the four owner-approved reform decisions (T1 risk-proportional review, T2 this baseline, T3 weekly verified increment at H1 closeout, T4 horizon batching) and the dependency-provenance decision. The risk register supersedes the floating-dependency exposure with R-T2-DEP-001. The ledger carries the chronological entry. The 4K-5 gate report remains unchanged as the historical record of the blocked attempt.

## Workflow Validation

`web-ci.yml` triggers on pull requests and main pushes touching `apps/web/**` or itself; permissions are read-only (`contents: read`); Node 22 with npm cache keyed to the lockfile. Steps: registry provenance check (public registry, no local `.npmrc`), `npm ci` from lockfile only, lockfile drift check (`git diff --exit-code` on package files), `npm run build`, and build-output sanity check (`dist/index.html` plus hashed JS asset). The workflow adds no secrets, tokens, deploy targets, or write permissions. Hosted execution proof is `LIVE_GITHUB_REQUIRED` until the first run on this PR.

## Security Hardening

The workflow's permission surface is minimized: `permissions: contents: read` at the workflow level; no secret, token, credential, deploy target, environment, or write permission of any kind; no third-party action beyond `actions/checkout@v4` and `actions/setup-node@v4`; triggers are path-scoped so unrelated PRs never execute it; the registry-provenance step fails the run if a non-public registry or a local `.npmrc` appears; the lockfile-drift step fails the run if install mutates the committed package files.

## Validation Evidence

- Local clean-room proof: `npm ci` from the committed lockfile followed by `npm run build` succeeded with byte-stable dependency tree (exact versions above).
- Workflow YAML reviewed for: read-only permissions, no secret usage, path-scoped triggers, lockfile-only install.
- All control validators and the continuity suite run locally; results recorded below.

## Validation Results

- Continuity test discovery: passed, 344 tests.
- All control validators: passed locally in replicated PR context.
- `git diff --check`: passed.
- Hosted `contractoros-control-gates` and `contractoros-web-ci` outcomes are `LIVE_GITHUB_REQUIRED` and cannot be asserted from repository text.

## Risk Register Impact

Adds `R-T2-DEP-001` (floating "latest" dependencies superseded), mitigated by pins + lockfile + CI drift gate; residual until the workflow passes on main after merge.

## Decision Log Impact

Adds the Throughput Reform and Web CI Baseline Decisions section: T1, T2 (with premise correction), T3, T4, and dependency provenance.

## Artifact Index Impact

No artifact index update is required. Build outputs (`dist/`) are gitignored and not published; no binary, archive, release, hosted, or external artifact is created by this phase.

`docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required`

## Red-Team Status

No review of this PR has occurred yet. The developer did not self-review and did not add a `RED_TEAM_DECISION` marker. Per the owner-selected both-keys flow, an owner-directed verification review with disclosed non-independence will follow delivery; the marker will be added to the PR body only after that verification pass at the exact head SHA.

## Human Approval Status

Human/write-access approval is not granted by this report and remains required before merge.

## Auto-Merge Status

Auto-merge is inactive and ineligible. No automatic continuation is authorized.

## Forbidden Scope Confirmation

- [x] No product source (JS/JSX/CSS), mobile, content, backend, or database mutation.
- [x] No deployment, release, production, publication, or app-store mutation.
- [x] No branch-protection, control-validator, credential, secret, or governance-repository mutation.
- [x] No auth, payments, scoring, readiness, analytics, or public-content scope.
- [x] No review, approval, merge, issue closeout, or next-phase start within this delivery.

Forbidden scope confirmation: confirmed for this bounded dependency-baseline and CI phase.

## Claim Level

Local install/build proof and lockfile baseline only. This does not prove hosted CI success (pending first run), cross-platform reproducibility beyond the lockfile contract, product correctness, production capability, or release readiness.

## Known Limitations

The hosted workflow has never executed before this PR; its first run is the proof. Exact-version pins do not pin transitive advisories; audit posture is a future H7A concern. The build proves compilation, not behavior — no test suite exists for apps/web yet (candidate for a follow-up phase).

## Remaining Gates

1. Hosted control-gates and web-ci runs on this PR head.
2. Owner-directed verification review at the exact head SHA (both-keys flow, disclosed non-independence).
3. Human/write-access approval and protected merge.
4. Verify `main` and confirm web-ci passes on the main push.
5. Record closeout on Issue #89 (T2 executed; T1/T3/T4 records landed).

## Next Phase Status

No next phase is authorized by this report. `NEXT_GATE=HOSTED_CI_PROOF_THEN_OWNER_DIRECTED_REVIEW`.

## Owner Trigger / Lane Eligibility Evidence

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: DEPENDENCY_SECURITY_RISK_ACCEPTANCE
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: First committed dependency tree and first hosted product workflow; owner review of the exact pinned versions and workflow permissions is required before merge.
