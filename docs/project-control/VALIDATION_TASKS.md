# Validation Tasks

Purpose: record validation tasks for ContractorOS California governance and phase-control work.

## Phase 4J-0 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J0-001 | Confirm changed files remain inside the Phase 4J-0 allowlist. | `git diff --name-only origin/main...HEAD` | Only the 14 allowed files are changed. | Passed in pre-PR validation; post-commit diff must match the PR evidence. |
| VAL-4J0-002 | Run changed-file lane check. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, or product lane file is changed. | Passed in local validation. |
| VAL-4J0-003 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside explicit exclusions. | Passed in local validation. |
| VAL-4J0-004 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4J-0 report and required control updates are present. | Passed in local validation. |
| VAL-4J0-005 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections are present. | Passed in local validation. |
| VAL-4J0-006 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no lockfile is added or changed. | Passed in local validation. |
| VAL-4J0-007 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported readiness, release, or completion claim is made. | Passed in local validation. |
| VAL-4J0-008 | Confirm no `/init`, broad discovery, `api_tool.list_resources`, or cockroachdb hook use. | Model run log and command history review | Confirmed in PR evidence. | Passed in local validation. |
| VAL-4J0-009 | Confirm future Phase 4J-2 red-team SHA artifact requirement is versioned. | Review `CONTRACTOROS_DESIGN_DECISIONS.md` and `REQUIREMENTS_TRACEABILITY_MATRIX.md` | Requirement is documented, not implemented in Phase 4J-0. | Passed in local validation. |
| VAL-4J0-010 | Verify local GitHub authentication before push. | `git push --no-verify -u origin phase-4j-0-codex-operating-model` only after credentials are available | Push can authenticate without interactive username failure. | Mitigated by owner GitHub CLI authentication for documentation PR setup. |
| VAL-4J0-011 | Verify branch exists on GitHub after push. | GitHub branch view or direct GitHub branch check | `phase-4j-0-codex-operating-model` exists on GitHub at the expected head SHA. | Passed for initial PR branch; verify again after correction push. |
| VAL-4J0-012 | Verify PR exists. | GitHub PR view or direct PR check | PR exists into `main` with the required title and body. | Passed; PR #15 exists. |
| VAL-4J0-013 | Verify GitHub Actions workflow passes. | GitHub Actions status on the PR head SHA | Required workflow checks pass for the pushed branch. | Pending after correction push. |
| VAL-4J0-014 | Verify PR evidence matches local report. | Compare PR body with `docs/project-control/phase_4j_0_codex_operating_model_report.md` | PR body does not imply push or PR creation succeeded before it did. | Pending until PR #15 body is updated with the corrected report. |
| VAL-4J0-015 | Verify post-merge main state after approval/merge. | GitHub main SHA/file verification | Main contains the approved Phase 4J-0 governance docs after merge. | Pending until red-team review, approval, and merge. |
| VAL-4J0-016 | Verify future prompts include model/effort header. | Prompt review against `docs/project-control/PROMPT_CONVENTION.md` | Prompt begins with the required model/effort header. | Active after Phase 4J-0 merge. |
| VAL-4J0-017 | Verify `PROMPT_CONVENTION.md` exists and is referenced by `AGENTS.md`. | File review | `docs/project-control/PROMPT_CONVENTION.md` exists and `AGENTS.md` points to it. | Passed in local documentation review. |
| VAL-4J0-018 | Verify xhigh/Extra High caveat is documented. | File review | `PROMPT_CONVENTION.md`, `SOURCE_REGISTER.md`, and `ASSUMPTION_REGISTER.md` avoid claiming official UI mapping. | Passed in local documentation review. |
| VAL-4J0-019 | Verify prompt convention does not activate auto-merge or product scope. | File review and forbidden-scope scan | Convention is documentation/control only and does not authorize auto-merge or product scope. | Passed in local validation. |

## Task Rule

Validation task status must be updated by repo evidence, not memory.

## Phase 4K-7 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4K7-001 | Verify starting main after Phase 4K-6. | `git rev-parse HEAD` before implementation edits | Returns `4315c943b6210f023849592213882bc8983c31d2`. | Passed before implementation edits. |
| VAL-4K7-002 | Verify active Phase 4K-7 intake. | Direct GitHub read of Issue #43 | Issue #43 is open/active. | Passed with direct GitHub evidence. |
| VAL-4K7-003 | Verify prior Phase 4K-6 lifecycle. | Direct GitHub reads of Issue #41 and PR #42 | Issue #41 is closed/completed and PR #42 merged at the starting main SHA. | Passed with direct GitHub evidence. |
| VAL-4K7-004 | Verify changed files stay inside the Phase 4K-7 allowlist. | `python3 scripts/control/check_changed_files.py` | Pass; no app, package, lockfile, dependency, build, backend, database, native, mobile, or web source file is changed. | Pending local validation. |
| VAL-4K7-005 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; restricted terms appear only in policy, risk, future, blocked, documentation, or explicit no-scope context. | Pending local validation. |
| VAL-4K7-006 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; current report and required project-control updates are present. | Pending local validation. |
| VAL-4K7-007 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required sections and `Phase issue: #43` reference are present. | Pending local validation. |
| VAL-4K7-008 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass with `ARCHITECTURE_THRESHOLD`, owner interruption, human approval, and no auto-merge eligibility. | Pending local validation. |
| VAL-4K7-009 | Run low-risk lane validator self-test. | `python3 scripts/control/check_low_risk_lane.py --self-test` | Pass; valid and invalid lane fixtures behave as expected. | Pending local validation. |
| VAL-4K7-010 | Run low-risk lane validator against current evidence. | `python3 scripts/control/check_low_risk_lane.py` | Pass; current Phase 4K-7 report declares `NOT_AUTOMATION_ELIGIBLE` and preserves current approval boundaries. | Pending local validation. |
| VAL-4K7-011 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile change is present. | Pending local validation. |
| VAL-4K7-012 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported automation, product, build, public, or release claim is made. | Pending local validation. |
| VAL-4K7-013 | Verify whitespace safety. | `git diff --check` and `git diff --cached --check` | Pass; no whitespace errors. | Pending local validation. |
| VAL-4K7-014 | Verify no app, package, lockfile, runtime, build, dependency, product, backend, or identity-system scope. | Changed-file review and validation output | Only control script, workflow, and allowed project-control files are changed. | Pending local validation. |
| VAL-4K7-015 | Verify approval boundaries. | Report, validator, and workflow review | Human approval and external red-team remain required; auto-merge remains inactive. | Pending local validation. |
| VAL-4K7-016 | Verify expected PR behavior. | GitHub Actions after PR opens | Owner-trigger and low-risk lane evidence pass; mandatory SHA-bound external red-team marker check fails until external review evidence matches the exact current PR head SHA. | Pending PR creation. |

## Phase 4K-6 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4K6-001 | Verify starting main after Phase 4K-5. | `git rev-parse HEAD` before documentation edits | Returns `e531c4d8bc1904c231be1f43114f16f652c4ec52`. | Passed before documentation edits. |
| VAL-4K6-002 | Verify Issue #39 and PR #40 historical state. | Direct GitHub reads | Issue #39 is closed/completed and PR #40 is merged at the starting main SHA. | Passed with direct GitHub evidence. |
| VAL-4K6-003 | Verify active Phase 4K-6 intake. | Direct GitHub read of Issue #41 | Issue #41 is open/active. | Passed with direct GitHub evidence. |
| VAL-4K6-004 | Verify changed files match the Phase 4K-6 allowlist. | `python3 scripts/control/check_changed_files.py` | Pass; only the 14 allowed project-control files are changed. | Pending local validation. |
| VAL-4K6-005 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; all restricted terms appear only in policy, risk, future, blocked, documentation, or explicit no-scope context. | Pending local validation. |
| VAL-4K6-006 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; report and required project-control updates are present. | Pending local validation. |
| VAL-4K6-007 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required sections and `Phase issue: #41` reference are present. | Pending local validation. |
| VAL-4K6-008 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass with `ARCHITECTURE_THRESHOLD`, owner interruption, human approval, and no auto-merge eligibility. | Pending local validation. |
| VAL-4K6-009 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile change is present. | Pending local validation. |
| VAL-4K6-010 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported implementation, product, build, public, or release claim is made. | Pending local validation. |
| VAL-4K6-011 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Pending local validation. |
| VAL-4K6-012 | Verify no package, lockfile, npmrc, or dependency-directory scope. | Changed-file review and lockfile scanner | No dependency/toolchain mutation is present; path remains deferred. | Pending local validation. |
| VAL-4K6-013 | Verify no app, runtime, build, workflow, control-script, or automation implementation scope. | Changed-file and command review | Only allowed policy/project-control documentation is changed. | Pending local validation. |
| VAL-4K6-014 | Verify no Phase 4K-7 or Phase 4I work. | Report and changed-file review | Phase 4K-7 remains a planning target only and Phase 4I remains paused. | Pending local validation. |
| VAL-4K6-015 | Verify current approval boundaries. | Policy/report review | External red-team and human approval remain required; auto-merge remains inactive. | Pending local validation. |
| VAL-4K6-016 | Verify expected PR behavior. | GitHub Actions after PR opens | Owner-trigger evidence passes; mandatory SHA-bound external red-team marker check fails until external review evidence matches the exact current PR head SHA. | Pending PR creation. |

## Phase 4K-5 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4K5-001 | Verify starting main after Phase 4K-4. | `git rev-parse HEAD` before documentation edits | Returns `61f5354ea55f7de9d0e88fd82031bacd94a9bf60`; stop if main has moved unexpectedly. | Passed before documentation edits. |
| VAL-4K5-002 | Verify Issue #39 is open. | Direct GitHub API read of Issue #39 | Issue #39 state is `open`. | Passed with direct GitHub issue evidence. |
| VAL-4K5-003 | Verify Issue #37 is closed/completed. | Direct GitHub API read of Issue #37 | Issue #37 state is `closed` with state reason `completed`. | Passed with direct GitHub issue evidence. |
| VAL-4K5-004 | Verify Issue #34 is closed/not planned and not active. | Direct GitHub API read of Issue #34 | Issue #34 state is `closed` with state reason `not_planned`. | Passed with direct GitHub issue evidence. |
| VAL-4K5-005 | Record node/npm tooling blocker evidence. | `npm --version`, `node --version`, escalated `npm --version`, escalated `node --version`, bundled Node version check, bundled bin listing | npm and node are unavailable on PATH; bundled Node exists; bundled npm does not exist at the bundled Node path. | Passed; blocker recorded in Phase 4K-5 report. |
| VAL-4K5-006 | Verify changed files match the Issue #39 blocked-correction allowlist. | Changed-file review | Only allowed `docs/project-control/**` records are changed. | Passed in local validation. |
| VAL-4K5-007 | Run changed-file lane check. | `python3 scripts/control/check_changed_files.py` | Pass; no app, package, lockfile, dependency, build, backend, database, native, mobile, or web source file is changed. | Passed in local validation. |
| VAL-4K5-008 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside blocked, deferred, future, risk, claim, or documentation context. | Passed in local validation. |
| VAL-4K5-009 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; current report and required control updates are present. | Passed in local validation. |
| VAL-4K5-010 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #39` reference are present. | Passed in local validation. |
| VAL-4K5-011 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass; Phase 4K-5 report contains the required `OWNER_TRIGGER_REVIEW` marker. | Passed in local validation. |
| VAL-4K5-012 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile changes are present. | Passed in local validation. |
| VAL-4K5-013 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported dependency baseline, runtime QA, release, production, backend, Firebase, auth, cloud, build, distribution, app-store, public-launch, readiness, scoring, pass/fail, CRM, marketplace, or payment implementation claim is made. | Passed in local validation. |
| VAL-4K5-014 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4K5-015 | Verify no package, lockfile, npmrc, dependency directory, runtime, build, artifact, backend, cloud, auth, scoring, readiness, pass/fail, analytics, saved-progress, public-content, payment, CRM, marketplace, Phase 4I, Phase 4K-6, merge, or auto-merge scope was added. | Changed-file review, package/lockfile/dependency-directory scan, and phase report commands section | No forbidden scope appears in changed files or commands. | Passed in local validation. |
| VAL-4K5-016 | Verify expected PR behavior. | GitHub Actions after PR opens | Owner-trigger evidence should pass; mandatory SHA-bound red-team marker check should fail until external red-team adds a valid marker for the exact current PR head SHA. | Pending PR creation. |

## Phase 4K-4 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4K4-001 | Verify starting main after Phase 4K-3. | `git rev-parse HEAD` before branch creation | Returns `196a48545285afdf8f5d5bc3f948395a5f289a4d`; stop if main has moved unexpectedly. | Passed before branch work. |
| VAL-4K4-002 | Verify Issue #35 is closed/completed. | Direct GitHub API read of Issue #35 | Issue #35 state is `closed` with state reason `completed`. | Passed with direct GitHub issue evidence. |
| VAL-4K4-003 | Verify Issue #34 is closed/not planned. | Direct GitHub API read of Issue #34 | Issue #34 state is `closed` with state reason `not_planned`. | Passed with direct GitHub issue evidence. |
| VAL-4K4-004 | Verify Issue #37 is open. | Direct GitHub API read of Issue #37 | Issue #37 state is `open`. | Passed with direct GitHub issue evidence. |
| VAL-4K4-005 | Inspect Phase 4K-2 blocker evidence. | File review of `phase_4k_2_internal_runtime_smoke_qa_feasibility_gate_report.md` and Issue #32 | Runtime smoke QA was blocked by missing dependency directories, missing lockfiles, missing safe no-install runtime path, and no dependency install authority. | Passed in local documentation review. |
| VAL-4K4-006 | Inspect current dependency and lockfile state. | `rg --files` and package manifest reads | Only `apps/web/package.json` and `apps/mobile/package.json` appear among package/lockfile/dependency-directory paths; no lockfile or dependency directory appears. | Passed in local inspection. |
| VAL-4K4-007 | Verify changed files match the Issue #37 allowlist. | Changed-file review | Only allowed `docs/project-control/**` files listed by Issue #37 are changed. | Passed in local validation. |
| VAL-4K4-008 | Run changed-file lane check. | `python3 scripts/control/check_changed_files.py` | Pass; no app, package, lockfile, dependency, build, backend, database, native, mobile, or web source file is changed. | Passed in local validation. |
| VAL-4K4-009 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside blocked, deferred, future, risk, claim, or documentation context. | Passed in local validation. |
| VAL-4K4-010 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; current report and required control updates are present. | Passed in local validation. |
| VAL-4K4-011 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #37` reference are present. | Passed in local validation. |
| VAL-4K4-012 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass; Phase 4K-4 report contains the required `OWNER_TRIGGER_REVIEW` marker. | Passed in local validation. |
| VAL-4K4-013 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile changes are present. | Passed in local validation. |
| VAL-4K4-014 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported dependency baseline, runtime QA, release, production, backend, Firebase, auth, cloud, build, distribution, app-store, public-launch, readiness, scoring, pass/fail, CRM, marketplace, or payment implementation claim is made. | Passed in local validation. |
| VAL-4K4-015 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4K4-016 | Verify no package, lockfile, dependency directory, runtime, build, artifact, backend, cloud, auth, scoring, readiness, pass/fail, analytics, saved-progress, public-content, payment, CRM, marketplace, Phase 4I, Phase 4K-5, merge, or auto-merge scope was added. | Changed-file review, package/lockfile scan, and phase report commands section | No forbidden scope appears in changed files or commands. | Passed in local validation. |
| VAL-4K4-017 | Verify expected PR behavior. | GitHub Actions after PR opens | Owner-trigger evidence should pass; mandatory SHA-bound red-team marker check should fail until external red-team adds a valid marker for the exact current PR head SHA. | Pending PR creation. |

## Phase 4K-3 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4K3-001 | Verify starting main after Phase 4K-2. | Documentation source sync command `git fetch origin main` and `git rev-parse origin/main` | Returns `4bb9fedb5648ea1b7185667948256276ad04d3b9`; stop if main has moved unexpectedly. | Passed before branch work. |
| VAL-4K3-002 | Verify Issue #32 is closed/completed. | Direct GitHub API read of Issue #32 | Issue #32 state is `closed` with state reason `completed`. | Passed with direct GitHub issue evidence. |
| VAL-4K3-003 | Verify Issue #34 is closed/not planned. | Direct GitHub API read of Issue #34 | Issue #34 state is `closed` with state reason `not_planned`. | Passed with direct GitHub issue evidence. |
| VAL-4K3-004 | Verify Issue #35 is open. | Direct GitHub API read of Issue #35 | Issue #35 state is `open`. | Passed with direct GitHub issue evidence. |
| VAL-4K3-005 | Inventory project-control overlaps. | File review of allowed project-control records | Stale 4K-0/4K-1 current-state text, missing canonical source-of-truth owner, Issue #34 supersession, and owner-trigger category gap are identified. | Passed in local documentation review. |
| VAL-4K3-006 | Verify changed files match the Issue #35 allowlist. | Changed-file review | Only allowed `docs/project-control/**` files listed by Issue #35 are changed. | Passed in local validation. |
| VAL-4K3-007 | Run changed-file lane check. | `python3 scripts/control/check_changed_files.py` | Pass; no app, package, lockfile, dependency, build, backend, database, native, mobile, or web source file is changed. | Passed in local validation. |
| VAL-4K3-008 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass after wording confirms forbidden terms are blocked, deferred, future, or documentation-only. | Passed in local validation. |
| VAL-4K3-009 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; current report and required control updates are present. | Passed in local validation. |
| VAL-4K3-010 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #35` reference are present. | Passed in local validation. |
| VAL-4K3-011 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass with current supported category `ARCHITECTURE_THRESHOLD`; unsupported Issue #35 semantic category `PRODUCT_SOURCE_OF_TRUTH` remains documented as a control-script gap. | Passed in local validation. |
| VAL-4K3-012 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile changes are present. | Passed in local validation. |
| VAL-4K3-013 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported product, dependency baseline, runtime QA, release, production, backend, Firebase, auth, cloud, build, distribution, app-store, public-launch, readiness, scoring, pass/fail, CRM, marketplace, or payment implementation claim is made. | Passed in local validation. |
| VAL-4K3-014 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4K3-015 | Verify no app/package/lockfile/runtime/build/artifact scope was added. | Changed-file review, package/lockfile scan, and phase report commands section | No app source, package, lockfile, dependency install, runtime launch, build, artifact, backend, cloud, auth, scoring, readiness, pass/fail, analytics, saved-progress, public-content, payment, CRM, marketplace, Phase 4I, Phase 4K-4, merge, or auto-merge scope is added. | Passed in local validation. |
| VAL-4K3-016 | Verify expected PR behavior. | GitHub Actions after PR opens | Owner-trigger evidence should pass; mandatory SHA-bound red-team marker check should fail until external red-team adds a valid marker for the exact current PR head SHA. | Pending PR creation. |

## Phase 4K-0 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4K0-001 | Verify starting main after Phase 4J-5. | Documentation source sync command `git fetch origin main` and `git rev-parse origin/main` | Returns `98cf25ff91e9bd3b852669af32bc2951e958494a`; stop if main has moved unexpectedly. | Passed before branch creation. |
| VAL-4K0-002 | Verify Phase 4J-5 protocol docs exist on main. | File review of `RED_TEAM_OPERATING_PROTOCOL.md`, `RED_TEAM_STATE_MACHINE.md`, and `HANDOFF_PLAYBOOK.md` | Required protocol docs exist in committed project-control records. | Passed in local documentation review. |
| VAL-4K0-003 | Verify Issue #24 no-memory-only directive is recorded. | Direct GitHub API read of Issue #24 comment `4928479219` | Comment records that non-durable approvals, decisions, agreed scope, authorizations, rejections, conditions, closeouts, protocol updates, and future operating rules are not durable. | Passed with direct GitHub issue-comment evidence. |
| VAL-4K0-004 | Inventory committed project evidence. | `git ls-tree -r --name-only HEAD` and project-control file review | Inventory identifies product/app, content, backend/Firebase/auth/cloud, build/distribution, known gaps, risks, roadmap, and phase tracker status from committed files only. | Passed in local evidence review. |
| VAL-4K0-005 | Verify changed files are limited to the allowlist. | Changed-file review | Only `docs/project-control/**` files changed. | Passed in local validation. |
| VAL-4K0-006 | Run changed-file lane check. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, product, app, mobile, or web lane file is changed. | Passed in local validation. |
| VAL-4K0-007 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside blocked/future/claim/control context. | Passed in local validation after wording updates. |
| VAL-4K0-008 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4K-0 report and required control updates are present. | Passed in local validation. |
| VAL-4K0-009 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #27` reference are present. | Passed in local validation. |
| VAL-4K0-010 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass; Phase 4K-0 report contains the required `OWNER_TRIGGER_REVIEW` marker. | Passed in local validation. |
| VAL-4K0-011 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile changes are present and no contaminated lockfile is introduced. | Passed in local validation. |
| VAL-4K0-012 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported product, release, production, backend, Firebase, auth, cloud, build, distribution, app-store, public-launch, readiness, scoring, pass/fail, CRM, marketplace, or payment implementation claim is made. | Passed in local validation. |
| VAL-4K0-013 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4K0-014 | Verify no package or lockfile files changed. | Changed-file review and lockfile scanner | No package or lockfile paths appear. | Passed in local validation. |
| VAL-4K0-015 | Verify no forbidden product/app/backend/database/Firebase/auth/cloud/deployment/payment/CRM/marketplace files changed. | Changed-file review and forbidden-scope scan | Only allowed project-control files are changed. | Passed in local validation. |
| VAL-4K0-016 | Verify no forbidden commands were run. | Phase report commands section and model run log | No npm, Expo, EAS, Android, iOS, native build, backend, Firebase, database, auth, deployment, dependency, payment, CRM, or marketplace commands were run. | Passed in local documentation review. |
| VAL-4K0-017 | Verify no artifact output was created. | Artifact index and changed-file review | No artifact, ZIP, binary, build output, Drive artifact, hosted artifact, release artifact, or archive artifact is created. | Passed in local validation. |
| VAL-4K0-018 | Verify expected PR behavior. | GitHub Actions after PR opens | Owner-trigger evidence should pass; mandatory SHA-bound red-team marker check should fail until external red-team adds a valid marker for the exact current PR head SHA. | Pending PR creation. |

## Phase 4J-1 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J1-001 | Verify phase issue template exists. | File review of `.github/ISSUE_TEMPLATE/phase_issue.yml` | Template captures required phase intake fields. | Pending local validation. |
| VAL-4J1-002 | Verify PR template requires linked issue evidence. | File review of `.github/pull_request_template.md` | Template requires linked phase issue and phase evidence sections. | Pending local validation. |
| VAL-4J1-003 | Verify PR contract enforces issue reference in PR context. | `scripts/control/check_pr_contract.py` review and GitHub Actions after PR open | PR body without accepted issue reference fails. | Pending workflow validation after PR opens. |
| VAL-4J1-004 | Verify existing local control checks pass. | Phase 4J-1 validation command set | Local checks pass before commit. | Pending local validation. |
| VAL-4J1-005 | Verify Phase 4J-1 PR links a GitHub phase issue. | PR body review | PR body includes `Phase issue: #16`. | Issue #16 exists; PR body must include `Phase issue: #16`; workflow validation remains pending until PR opens. |
| VAL-4J1-006 | Verify no auto-merge or product scope is activated. | Forbidden-scope scan and file review | Control-only files changed; auto-merge remains inactive. | Pending local validation. |

## Phase 4J-2 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J2-001 | Verify red-team marker validator self-test. | `python3 scripts/control/check_red_team_marker.py --self-test` | Pass; approved fixture passes and blocked fixture fails internally. | Passed in local validation. |
| VAL-4J2-002 | Verify changed files remain inside the Phase 4J-2 allowlist. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, or product lane file is changed. | Passed in local validation. |
| VAL-4J2-003 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside explicit exclusions. | Passed in local validation. |
| VAL-4J2-004 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4J-2 report and required control updates are present. | Passed in local validation. |
| VAL-4J2-005 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and Phase issue reference are present. | Passed in local validation. |
| VAL-4J2-006 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no lockfile is added or changed. | Passed in local validation. |
| VAL-4J2-007 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported readiness, release, or completion claim is made. | Passed in local validation. |
| VAL-4J2-008 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4J2-009 | Verify bootstrap status. | Report and workflow review | Marker validator exists, but mandatory enforcement is documented for Phase 4J-3 or later activation. | Passed in local documentation review. |

## Phase 4J-3 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J3-001 | Verify red-team marker validator self-test. | `python3 scripts/control/check_red_team_marker.py --self-test` | Pass; approved marker fixture passes, blocked markers fail, and fenced-code examples are ignored. | Passed in local validation. |
| VAL-4J3-002 | Verify changed files remain inside the Phase 4J-3 allowlist. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, product, app, mobile, or web lane file is changed. | Passed in local validation. |
| VAL-4J3-003 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside explicit exclusions. | Passed in local validation. |
| VAL-4J3-004 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4J-3 report and required control updates are present. | Passed in local validation. |
| VAL-4J3-005 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #20` reference are present. | Passed in local validation. |
| VAL-4J3-006 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no lockfile is added or changed. | Passed in local validation. |
| VAL-4J3-007 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported readiness, release, or completion claim is made. | Passed in local validation. |
| VAL-4J3-008 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4J3-009 | Verify PR-body edit rerun behavior. | GitHub Actions after PR body edit with a red-team marker | The `pull_request` `edited` event reruns the control-gates workflow. | Pending GitHub Actions evidence after PR opens. |
| VAL-4J3-010 | Verify stale marker behavior. | Add or compare a marker whose SHA differs from current PR head SHA | The mandatory marker step fails until the marker matches the current PR head SHA. | Pending GitHub Actions evidence after PR opens. |

## Phase 4J-4 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J4-001 | Verify owner-trigger marker validator self-test. | `python3 scripts/control/check_owner_trigger_review.py --self-test` | Pass; valid triggered and no-trigger markers pass; missing, unknown, inconsistent, auto-merge, human-approval, and ignored-example cases fail internally. | Passed in local validation. |
| VAL-4J4-002 | Verify changed files remain inside the Phase 4J-4 allowlist. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, product, app, mobile, or web lane file is changed. | Passed in local validation. |
| VAL-4J4-003 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside explicit exclusions. | Passed in local validation after adding `PRODUCTION_READINESS` as controlled governance enum text. |
| VAL-4J4-004 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4J-4 report and required control updates are present. | Passed in local validation after adding the exact `Artifact Index Impact` report section. |
| VAL-4J4-005 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #22` reference are present. | Passed in local validation after adding the exact `Validation Evidence` report section. |
| VAL-4J4-006 | Run local owner-trigger marker check against changed reports. | `python3 scripts/control/check_owner_trigger_review.py` | Pass; Phase 4J-4 report contains a valid `OWNER_TRIGGER_REVIEW` marker. | Passed in local validation. |
| VAL-4J4-007 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no lockfile is added or changed. | Passed in local validation. |
| VAL-4J4-008 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported readiness, release, or completion claim is made. | Passed in local validation. |
| VAL-4J4-009 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4J4-010 | Verify PR control-gate interaction with red-team enforcement. | GitHub Actions after PR opens and PR body contains `OWNER_TRIGGER_REVIEW` evidence | Owner-trigger check can pass; mandatory red-team marker check is expected to fail until red-team adds a SHA-bound `RED_TEAM_DECISION` marker. | Observed on PR #23: control-gates failed at `Mandatory SHA-bound red-team marker check` with `FAIL: red-team marker is missing.` Any later commit reruns the workflow and still requires red-team evidence. |

## Phase 4J-5 Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-4J5-001 | Verify starting main. | `git rev-parse origin/main` | Returns `b01cd5829621c20f6bd837a9d570553a6a408573` before branch creation. | Passed before branch creation. |
| VAL-4J5-002 | Verify clean starting worktree. | `git status --short --branch` | Clean `main` or clean phase branch before edits. | Passed before branch creation. |
| VAL-4J5-003 | Verify changed files remain inside the Phase 4J-5 allowlist. | `python3 scripts/control/check_changed_files.py` | Pass; no dependency, build, backend, database, native, product, app, mobile, or web lane file is changed. | Passed in local validation before staging. |
| VAL-4J5-004 | Run forbidden-scope scan. | `python3 scripts/control/check_forbidden_scope.py` | Pass; no implementation-looking forbidden terms outside explicit exclusions or controlled governance text. | Passed in local validation after adding claim downgrade wording to progress-snapshot lines. |
| VAL-4J5-005 | Run required control update check. | `python3 scripts/control/check_required_control_updates.py` | Pass; Phase 4J-5 report and required register updates are present. | Passed in local validation. |
| VAL-4J5-006 | Run PR/report contract check. | `python3 scripts/control/check_pr_contract.py` | Pass; required report sections and `Phase issue: #25` reference are present. | Passed in local validation. |
| VAL-4J5-007 | Run owner-trigger marker check. | `python3 scripts/control/check_owner_trigger_review.py` | Pass; Phase 4J-5 report contains the required `OWNER_TRIGGER_REVIEW` marker. | Passed in local validation. |
| VAL-4J5-008 | Run lockfile contamination check. | `python3 scripts/control/check_forbidden_scope.py --lockfiles-only` | Pass; no package or lockfile changes are present. | Passed in local validation. |
| VAL-4J5-009 | Run claim-language check. | `python3 scripts/control/check_pr_contract.py --claims-only` | Pass; no unsupported readiness, release, production, public launch, build, backend, scoring, or pass/fail claim is made. | Passed in local validation. |
| VAL-4J5-010 | Verify whitespace safety. | `git diff --check` | Pass; no whitespace errors. | Passed in local validation. |
| VAL-4J5-011 | Verify Issue #24 protocol content is reflected in committed docs. | File review of `RED_TEAM_OPERATING_PROTOCOL.md`, `RED_TEAM_STATE_MACHINE.md`, and `HANDOFF_PLAYBOOK.md` | Source-of-truth, CLI expected-output, progress snapshot, and operator state-machine requirements are represented. | Passed in local documentation review. |
| VAL-4J5-012 | Verify no package or lockfile files changed. | `git diff --name-only origin/main...HEAD` and lockfile scanner | No package or lockfile paths appear. | Passed in local validation before staging. |
| VAL-4J5-013 | Verify no product/app/backend/database/Firebase/auth/cloud/deployment/payment/CRM/marketplace files changed. | Changed-file review and forbidden-scope scan | Only allowed control documentation files are changed. | Passed in local validation before staging. |
| VAL-4J5-014 | Verify no npm, Expo, EAS, Android, iOS, native build, backend, Firebase, database, auth, deployment, or dependency commands were run. | Phase report commands section and model run log | Commands are limited to git, direct GitHub reads, local text edits, and local control validation. | Passed in local documentation review. |
| VAL-4J5-015 | Verify GitHub Actions after PR opens. | PR control-gates workflow | Owner-trigger check should pass and mandatory red-team marker check should fail until external red-team adds a valid SHA-bound marker. | Pending PR creation. |
| VAL-4J5-016 | Verify no auto-merge activation and no next-phase start. | PR/report review | Auto-merge remains inactive; Phase 4J-6 is not started; Phase 4I remains paused. | Pending PR creation. |

## Pre-4K-9 Validation Tasks

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-PRE4K9-001 | Validate D1–D26 register. | Temporary standard-library Python JSON/YAML-subset check. | Exactly D1–D26, all required fields, option A, D1/D11 conditions, no operational overclaim. | Passed locally. |
| VAL-PRE4K9-002 | Validate canonical state and schemas. | Temporary standard-library Python structural checks. | Verified lifecycle values and valid JSON-compatible YAML. | Passed locally. |
| VAL-PRE4K9-003 | Validate ADR index. | Temporary standard-library Python and file review. | Nine existing ADRs; every ADR links owner decisions and required sections. | Passed locally. |
| VAL-PRE4K9-004 | Scan public-safe files. | Git path and secret-pattern review. | No private artifact, credential, secret, raw PDF, DOCX, or ZIP. | Passed locally. |
| VAL-PRE4K9-005 | Run existing controls. | Required eleven-command control sequence. | All local controls pass before commit. | First and final full sequences passed. |
| VAL-PRE4K9-006 | Verify pre-marker PR behavior. | GitHub Actions after PR creation. | Pre-marker checks pass; mandatory exact-SHA marker fails; later checks may skip. | Pending PR creation. |
