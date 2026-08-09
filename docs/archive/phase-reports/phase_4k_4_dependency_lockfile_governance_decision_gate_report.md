# Phase 4K-4 Dependency / Lockfile Governance Decision Gate Report

## Linked Phase Issue

Phase issue: #37

Issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/37

## Phase

Phase 4K-4 - Dependency / Lockfile Governance Decision Gate

## Lane

Control / Infrastructure

Issue #37 functional lane: Dependency / Architecture / QA.

Control-gate lane note: the changed files are under `docs/project-control/**`; the current control matrix classifies those changes as Control / Infrastructure.

## Current Lifecycle State

WAITING_FOR_CODEX_RESPONSE at intake.

After this developer response and PR creation, the next expected lifecycle state is PR_OPEN_MARKER_MISSING until external red-team review adds a valid SHA-bound `RED_TEAM_DECISION` marker for the exact current PR head SHA.

## Starting Main SHA

`196a48545285afdf8f5d5bc3f948395a5f289a4d`

Local `HEAD` was verified at this SHA before branch creation.

## Source Anchors

- Issue #24 - Red-Team Handoff + Memory Reconciliation Gate.
- Issue #32 - Phase 4K-2 Internal Runtime Smoke QA Feasibility Gate.
- Issue #34 - Dependency / Lockfile Baseline Decision Gate, closed not planned before implementation.
- Issue #35 - Phase 4K-3 Product / Development Source-of-Truth Reconciliation Gate.
- Issue #37 - Phase 4K-4 Dependency / Lockfile Governance Decision Gate.
- PR #33 - Phase 4K-2 merged at `4bb9fedb5648ea1b7185667948256276ad04d3b9`.
- PR #36 - Phase 4K-3 merged at `196a48545285afdf8f5d5bc3f948395a5f289a4d`.
- `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`.
- `docs/project-control/phase_4k_2_internal_runtime_smoke_qa_feasibility_gate_report.md`.
- Existing package manifests under `apps/web/package.json` and `apps/mobile/package.json`.

## Scope

In scope:

- Dependency/lockfile governance decision documentation.
- Inspection of existing package manifests, package/lockfile state, Phase 4K-2 blocker evidence, Phase 4K-3 source-of-truth evidence, and allowed project-control records.
- Recommendation of exactly one next controlled phase.
- Project-control record updates listed by Issue #37.

Out of scope:

- No app source edits.
- No package manifest edits.
- No package lockfile, pnpm lockfile, yarn lockfile, bun lockfile, shrinkwrap, or other lockfile creation.
- No dependency installation, upgrade, removal, package-manager migration, dependency directory creation, runtime launch, browser QA, emulator/device QA, install QA, build artifact, Expo/EAS/native build, APK/AAB/iOS build, app-store material, deployment, backend/database/Firebase/auth/cloud implementation, payment/subscription, CRM, marketplace, analytics, saved progress, scoring, readiness, pass/fail, public content, Question Bank migration, C10/C46/C39 public content, ZIP/binary/archive/Drive artifact, Phase 4I resume, Phase 4K-5 start, branch-protection bypass, merge by Codex, or auto-merge activation.

## Changed Files

Changed files:

- `docs/project-control/phase_4k_4_dependency_lockfile_governance_decision_gate_report.md`
- `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`
- `docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md`
- `docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/VALIDATION_TASKS.md`
- `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `docs/project-control/SOURCE_REGISTER.md`
- `docs/project-control/ARTIFACT_INDEX.md`

## Commands Run

Commands run before and during this phase:

```text
git status -sb
git branch --show-current
git rev-parse HEAD
git remote -v
gh api repos/Zest-LeadGen/contractoros-california/issues/35
gh api repos/Zest-LeadGen/contractoros-california/issues/34
gh api repos/Zest-LeadGen/contractoros-california/issues/37
git switch -c phase-4k-4-dependency-lockfile-governance-decision-gate
rg --files docs/project-control
rg --files
sed reads of allowed project-control files
sed reads of apps/web/package.json and apps/mobile/package.json
rg --files apps/web apps/mobile
gh api repos/Zest-LeadGen/contractoros-california/issues/32
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_owner_trigger_review.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --check
```

Validation command results are listed in `Validation Evidence`.

## Existing Files Inspected

- `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`
- `docs/project-control/phase_4k_2_internal_runtime_smoke_qa_feasibility_gate_report.md`
- `docs/project-control/phase_4k_3_product_development_source_of_truth_reconciliation_report.md`
- `docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md`
- `docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/VALIDATION_TASKS.md`
- `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `docs/project-control/SOURCE_REGISTER.md`
- `docs/project-control/ARTIFACT_INDEX.md`
- `docs/project-control/control-file-update-matrix.yml`
- `scripts/control/check_owner_trigger_review.py`
- `apps/web/package.json`
- `apps/mobile/package.json`
- App source file list under `apps/web/**` and `apps/mobile/**` for package/app boundary inspection only.

GitHub issue evidence inspected:

- Issue #32: closed with state reason `completed`.
- Issue #34: closed with state reason `not_planned`.
- Issue #35: closed with state reason `completed`.
- Issue #37: open.

## Current Dependency / Lockfile State

Current state found by package/lockfile scan and manifest inspection:

- `apps/web/package.json` exists.
- `apps/web/package.json` defines `dev`, `build`, and `preview` scripts using Vite.
- `apps/web/package.json` uses `latest` ranges for `@vitejs/plugin-react`, `vite`, `react`, and `react-dom`.
- `apps/mobile/package.json` exists.
- `apps/mobile/package.json` defines `start` as `expo start`.
- `apps/mobile/package.json` uses `latest` ranges for `expo`, `react`, and `react-native`.
- No root `package.json` was found.
- No `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or `npm-shrinkwrap.json` was found.
- No committed dependency directory was found.

No package, lockfile, dependency directory, dependency install, runtime launch, or build command was created or run in this phase.

## Dependency / Lockfile Handling

No dependency was installed, upgraded, removed, or resolved in this phase.

No package manifest was edited.

No lockfile was created or changed.

No dependency directory was created or committed.

Phase 4K-4 recommends a future web-only deterministic dependency/lockfile baseline implementation phase, but it does not implement that baseline.

## Phase 4K-2 Runtime Blocker Evidence

Phase 4K-2 found runtime smoke QA blocked before runtime launch.

Web blocker evidence:

- `apps/web/package.json` requires Vite/React dependencies.
- No `apps/web/node_modules` directory was present.
- No web lockfile was present.
- No safe no-install runtime launch path was proven.
- Bundled package-manager probing attempted registry dependency resolution and was stopped before dependency installation could finish.

Mobile blocker evidence:

- `apps/mobile/package.json` requires Expo/React/React Native dependencies.
- No `apps/mobile/node_modules` directory was present.
- No mobile lockfile was present.
- No safe no-install Expo/Metro launch path was proven.
- Bundled package-manager probing attempted registry dependency resolution and was stopped before dependency installation could finish.

Result: runtime smoke QA, browser QA, emulator/device QA, install QA, build/distribution work, and readiness claims remain blocked until a safe dependency baseline path is approved, implemented, and verified.

## Phase 4K-3 Source-of-Truth Evidence

Phase 4K-3 created `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` as the canonical product/development current-state register.

That register records:

- `apps/web/package.json` and `apps/mobile/package.json` exist and use `latest` dependency ranges.
- No root package manager entrypoint is present.
- No committed package lockfile exists for web or mobile.
- No committed dependency directory exists for web or mobile.
- Runtime smoke QA remains blocked until a later approved phase supplies a safe dependency baseline path.
- Issue #34 is closed/not planned and must not be treated as active.
- Future dependency/lockfile work needs a durable GitHub issue after source-of-truth reconciliation.

Phase 4K-4 uses Issue #37 as that durable issue. It does not resurrect Issue #34.

## Decision Options Evaluated

Evaluated options:

- Option A: Do nothing; keep runtime QA blocked.
- Option B: Add deterministic lockfiles in a later controlled dependency-baseline implementation phase.
- Option C: Split web and mobile dependency baselines into separate future implementation phases.
- Option D: Use containerized/toolchain-pinned runtime QA in a later controlled phase.
- Option E: Vendor/preload dependency directories externally without package/lockfile governance.
- Option F: Package-manager migration or standardization in a later controlled phase.

## Option A Assessment

Option A would avoid immediate dependency risk, but it preserves the Phase 4K-2 blocker.

Benefit:

- Lowest immediate mutation risk.

Risks:

- Runtime smoke QA remains blocked.
- Browser, emulator/device, install, build, and release gates remain blocked.
- The repository keeps `latest` dependency ranges without deterministic resolution evidence.

Assessment: rejected as the recommended next phase because it does not reduce the known blocker.

## Option B Assessment

Option B would create deterministic lockfiles in a later controlled dependency-baseline implementation phase.

Benefit:

- Directly addresses the missing lockfile blocker.
- Creates reviewable supply-chain evidence.
- Enables later no-surprise runtime QA attempts if the baseline passes provenance and contamination checks.

Risks:

- Package resolution can expose dependency/security findings.
- Lockfiles can be contaminated by non-public registry references if the environment is not controlled.
- Combining web and mobile baselines in one phase may be broader than necessary.

Assessment: accepted in principle, but refined by Option C so the next phase is split and begins with web only.

## Option C Assessment

Option C splits web and mobile dependency baselines into separate future implementation phases.

Benefit:

- Narrows the first package/lockfile mutation surface.
- Web has a smaller dependency set than mobile Expo/React Native.
- Reduces blast radius if registry/provenance or contamination checks fail.
- Leaves mobile baseline for a later phase after web baseline evidence is reviewed.

Risks:

- Mobile runtime QA remains blocked after a web-only baseline.
- Additional phase overhead is required.

Assessment: selected. The recommended next controlled phase is a deterministic web dependency/lockfile baseline implementation phase.

## Option D Assessment

Option D would use containerized/toolchain-pinned runtime QA in a later controlled phase.

Benefit:

- Could improve repeatability once a baseline exists.

Risks:

- Does not itself solve the missing dependency/lockfile evidence.
- Adds toolchain/container governance before dependency provenance is controlled.
- Could hide package-resolution problems behind a runtime environment layer.

Assessment: rejected as the immediate next phase. It may be reconsidered after deterministic dependency baseline evidence exists.

## Option E Assessment

Option E would vendor or preload dependency directories externally without package/lockfile governance.

Benefit:

- Might avoid package resolution during runtime QA.

Risks:

- Poor auditability compared with committed lockfiles.
- Difficult provenance review.
- High risk of stale, unreviewed, or environment-specific dependency state.
- Does not create a clear source-governed package baseline.

Assessment: rejected. Current evidence does not prove this is safer or more auditable than lockfiles.

## Option F Assessment

Option F would migrate or standardize package managers in a later controlled phase.

Benefit:

- Could create one future package-manager policy.

Risks:

- Migration is a separate architecture/dependency decision.
- Current evidence does not prove migration is safer than creating deterministic lockfiles for the existing manifests.
- Migration would increase scope before the baseline blocker is reduced.

Assessment: rejected as the immediate next phase. It may be reconsidered only if a later issue proves migration is safer than deterministic lockfile creation.

## Recommended Next Controlled Phase

Recommended exactly one next controlled phase:

Phase 4K-5 - Web Dependency / Lockfile Baseline Implementation Gate.

Recommended objective:

Create and verify a deterministic dependency/lockfile baseline for `apps/web` only, under an approved Dependency lane issue, without launching runtime QA or changing mobile dependencies.

## Rationale

The web app has the smaller dependency surface and uses a standard Vite/React manifest. A web-only deterministic baseline is the narrowest useful package/lockfile mutation step that can reduce the Phase 4K-2 blocker while preserving auditability.

This recommendation follows Option C with Option B's deterministic lockfile principle:

- split web and mobile baselines;
- start with web only;
- require explicit package/lockfile allowlists;
- require registry/provenance checks;
- require contamination checks;
- stop before runtime QA, build, or release claims.

## Risk Level

Risk level: Medium.

Reason:

The recommended next phase would intentionally allow package and lockfile mutation for `apps/web`, which can affect reproducibility and supply-chain evidence. The risk is bounded by limiting the first baseline to web only, requiring provenance/contamination checks, and stopping before runtime QA or build work.

## Proposed Next-Phase Allowlist

Likely allowlist for the recommended future Phase 4K-5:

- `apps/web/package.json`
- `apps/web/package-lock.json`
- `docs/project-control/phase_4k_5_web_dependency_lockfile_baseline_report.md`
- `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/VALIDATION_TASKS.md`
- `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `docs/project-control/SOURCE_REGISTER.md`
- `docs/project-control/ARTIFACT_INDEX.md`

The future issue may add a package-manager config file only if it is explicitly justified and allowed.

## Proposed Next-Phase Forbidden Scope

Recommended forbidden scope for the next phase:

- No mobile package, lockfile, or Expo changes.
- No app source edits unless the future issue explicitly proves they are required for dependency baseline generation.
- No runtime launch.
- No browser QA.
- No emulator/device QA.
- No install QA.
- No build artifact.
- No deployment.
- No backend/database/Firebase/auth/cloud implementation.
- No payment/subscription, CRM, marketplace, analytics, saved progress, scoring, readiness, pass/fail, public content, Question Bank migration, or C10/C46/C39 public content.
- No Phase 4I resume.
- No phase after Phase 4K-5 start.
- No auto-merge activation.
- No merge by Codex.

## Proposed Next-Phase Validation Tasks

Recommended validation tasks for the next phase:

- Verify starting main SHA after Phase 4K-4 merge and main verification.
- Verify Issue #37 is closed/completed.
- Verify the new Phase 4K-5 issue is open and explicitly permits web dependency/lockfile baseline implementation.
- Verify changed files match the future issue allowlist.
- Verify only `apps/web` package/lockfile files are changed among app package surfaces.
- Generate a deterministic web lockfile using the approved package manager and public registry configuration only.
- Verify lockfile registry/provenance references are public and expected.
- Run `python3 scripts/control/check_changed_files.py`.
- Run `python3 scripts/control/check_forbidden_scope.py`.
- Run `python3 scripts/control/check_required_control_updates.py`.
- Run `python3 scripts/control/check_pr_contract.py`.
- Run `python3 scripts/control/check_owner_trigger_review.py`.
- Run `python3 scripts/control/check_forbidden_scope.py --lockfiles-only`.
- Run `python3 scripts/control/check_pr_contract.py --claims-only`.
- Run `git diff --check`.
- Verify no dependency directory is committed.
- Verify no runtime, browser QA, build, backend, cloud, auth, scoring, readiness, pass/fail, analytics, saved-progress, public-content, payment, CRM, marketplace, Phase 4I, later phase, merge, or auto-merge scope was added.

## Explicit Stop Conditions

Stop the recommended future phase if any of the following occurs:

- Starting main SHA does not match the future issue.
- Future issue does not explicitly allow package/lockfile mutation.
- Package manager attempts to use a non-public or unexpected registry.
- Generated lockfile contains internal, sandbox, localhost, non-public, or machine-specific references.
- Dependency resolution changes files outside the future allowlist.
- Dependency install creates a dependency directory that cannot be removed before commit.
- New security findings require owner/security risk acceptance.
- App source changes appear necessary.
- Runtime launch, browser QA, build, backend, cloud, auth, scoring, readiness, pass/fail, analytics, saved-progress, public-content, payment, CRM, marketplace, Phase 4I, later phase, merge, or auto-merge scope is requested.
- Local validation fails and the fix is outside the approved future scope.

## Rejected Options and Why

- Option A is rejected because it keeps runtime QA blocked and does not reduce dependency uncertainty.
- Option B as a combined web+mobile phase is rejected because it is broader than necessary for the first dependency mutation.
- Option D is rejected for the immediate next phase because containerized runtime QA does not replace dependency/lockfile provenance.
- Option E is rejected because vendored/preloaded dependency directories are less auditable than lockfiles.
- Option F is rejected for the immediate next phase because package-manager migration is a separate decision and current evidence does not prove it is safer.

## Product / Development Source-of-Truth Updates

`docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` now records Phase 4K-4 as the active phase and records the recommendation for a later web-only deterministic dependency/lockfile baseline implementation phase.

## Documentation Impact

Phase 4K-4 changes only source/text project-control documentation. It updates the canonical register, roadmap/tracker, ledger, decision log, risk register, validation tasks, traceability matrix, source register, artifact index, and this phase report.

## Roadmap / Tracker Updates

`docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md` and `docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md` now record Phase 4K-4 as active and Phase 4K-3 as merged through PR #36.

## Decision Log Updates

`docs/project-control/DECISION_LOG.md` records that Phase 4K-4 uses Issue #37, does not resurrect Issue #34, and recommends a later web-only deterministic dependency/lockfile baseline implementation phase.

## Decision Log Impact

Decision log impact is limited to dependency/lockfile governance decision documentation. No implementation permission is granted by the decision-log update.

## Risk Register Updates

`docs/project-control/RISK_REGISTER.md` records that the dependency baseline is still not implemented, updates the Issue #34 supersession risk, and updates dependency/latest/lockfile contamination risks with Phase 4K-4 evidence.

## Risk Register Impact

Risk register impact is limited to documenting that dependency baseline risk remains active until a later approved implementation phase creates and verifies deterministic lockfile evidence.

## Validation Tasks Updates

`docs/project-control/VALIDATION_TASKS.md` adds Phase 4K-4 validation tasks.

## RTM Updates

`docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md` adds Phase 4K-4 traceability rows.

## Source Register Updates

`docs/project-control/SOURCE_REGISTER.md` adds Phase 4K-4 source rows for Issues #32, #34, #35, #37, starting main, the canonical register, Phase 4K-2 blocker report, package manifests, and app boundary inspection.

## Artifact Index Updates

`docs/project-control/ARTIFACT_INDEX.md` records that Phase 4K-4 creates no artifact, ZIP, binary, build output, lockfile artifact, dependency archive, Drive artifact, hosted artifact, release artifact, install artifact, runtime visual artifact, device QA artifact, or archive artifact.

## Artifact Index Impact

No new artifact is indexed. Phase 4K-4 creates source/text governance records only.

## Forbidden Scope Confirmation

- [x] No app source edits
- [x] No package manifest edits
- [x] No package lockfile, pnpm lockfile, yarn lockfile, bun lockfile, shrinkwrap, or other lockfile creation
- [x] No dependency installation
- [x] No dependency upgrade
- [x] No dependency removal
- [x] No package-manager migration
- [x] No dependency directory creation
- [x] No runtime launch
- [x] No browser QA
- [x] No emulator/device QA
- [x] No install QA
- [x] No build artifact
- [x] No Expo/EAS/native build
- [x] No APK/AAB/iOS build
- [x] No app-store material
- [x] No deployment
- [x] No backend/database/Firebase/auth/cloud implementation
- [x] No payment/subscription
- [x] No CRM
- [x] No marketplace
- [x] No analytics
- [x] No saved progress
- [x] No scoring
- [x] No readiness
- [x] No pass/fail
- [x] No public content
- [x] No Question Bank migration
- [x] No C10/C46/C39 public content
- [x] No ZIP/binary/archive/Drive artifact
- [x] No Phase 4I resume
- [x] No Phase 4K-5 start
- [x] No branch-protection bypass
- [x] No merge by Codex
- [x] No auto-merge activation

## Validation Evidence

Validation command results:

```text
PASS: python3 scripts/control/check_changed_files.py
PASS: python3 scripts/control/check_forbidden_scope.py
PASS: python3 scripts/control/check_required_control_updates.py
PASS: python3 scripts/control/check_pr_contract.py
PASS: python3 scripts/control/check_owner_trigger_review.py
PASS: python3 scripts/control/check_forbidden_scope.py --lockfiles-only
PASS: python3 scripts/control/check_pr_contract.py --claims-only
PASS: git diff --check
```

Pre-edit and inspection evidence:

- Local `HEAD` before branch creation: `196a48545285afdf8f5d5bc3f948395a5f289a4d`.
- Issue #35: closed/completed.
- Issue #34: closed/not planned.
- Issue #37: open.
- Issue #32: closed/completed.
- Package/lockfile scan found `apps/web/package.json` and `apps/mobile/package.json` only.

## OWNER_TRIGGER_REVIEW marker

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD, DEPENDENCY_SECURITY_RISK_ACCEPTANCE
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Phase 4K-4 makes the dependency/lockfile governance decision that controls whether future runtime QA can proceed safely. Dependency governance can affect reproducibility, supply-chain risk, package mutation, runtime QA, build eligibility, and future security posture, so owner interruption, external red-team review, and human approval are required.

## Red-Team Status

External red-team review is required before merge.

Codex does not self-review and does not add the `RED_TEAM_DECISION` marker.

The PR is expected to fail the mandatory SHA-bound red-team marker check until external red-team adds a valid marker for the exact current PR head SHA.

## Human Approval Status

Human/write-access approval is required before merge after red-team approval and successful post-marker ContractorOS Control Gates.

Human approval has not been granted by this report.

## Auto-Merge Status

Auto-merge is inactive and prohibited.

No auto-merge activation is included in this phase.

## Claim Level

Dependency/lockfile governance decision documentation only.

No dependency baseline is implemented in this phase. No runtime QA, visual QA, device QA, install QA, build readiness, APK readiness, public readiness, production readiness, scoring, pass/fail, backend, Firebase, auth, cloud, content-currentness, public content, payment, CRM, marketplace, or release claim is made.

## Known Limitations

- This phase recommends the next dependency-governance implementation path but does not prove that dependency resolution will succeed.
- This phase does not generate or inspect a new lockfile.
- This phase does not prove web runtime behavior, mobile runtime behavior, browser QA, emulator/device QA, install QA, build behavior, release behavior, or public/content currentness.
- GitHub Actions status is available only after the branch is pushed and the PR is opened.

## Next Phase Status

Recommended next controlled phase: Phase 4K-5 - Web Dependency / Lockfile Baseline Implementation Gate.

Phase 4K-5 is not started.

Phase 4I remains paused.

Do not start the next phase until Phase 4K-4 is merged, main is verified, Issue #37 is closed, and a later durable GitHub issue permits the next scope.
