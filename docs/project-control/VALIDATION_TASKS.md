# Validation Tasks

Purpose: record validation tasks for ContractorOS California governance and phase-control work.

## Historical Phase 4J-0 Tasks

The status cells in this section preserve the original Phase 4J-0 checkpoint. PR #15 correction, push, body-update, workflow, review, approval, merge, and verification statements are historical execution state and are not current H1 lifecycle claims.

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

## H0 Durable Finding Validation Contracts

`VALIDATION_GROUP_ID=VAL-H8-AI-001` identifies the cross-gate AI permission and drift contracts. Unless a row explicitly names an existing script, these are documented manual contracts; automation is not claimed. H1-B1A-G remains responsible for future machine-readable schema enforcement.

| Task ID | Contract | Method | Expected result | Current status |
|---|---|---|---|---|
| `VAL-H0-FIND-001` | Required finding fields | Parse every finding record against the 24-field register schema. | Every record has one nonempty value for each required field. | Documented manual contract; not automated. |
| `VAL-H0-FIND-002` | Unique finding IDs | Enumerate `FINDING_ID` values and reject duplicates or reuse. | Seven unique accepted H0 IDs; any duplicate blocks. | Documented manual contract; not automated. |
| `VAL-H0-FIND-003` | Allowed lifecycle values | Compare `CURRENT_STATUS` with the exact register lifecycle enum. | Unknown or misspelled values block. | Documented manual contract; not automated. |
| `VAL-H0-SUPER-001` | Exact supersession edges | For each superseded record, require replacement ID, exact owner authority, conflict/premise, preserved evidence, and dependency revalidation. | Silence, chronology, UI change, PR creation, developer claim, or docs-only edit cannot supersede. | Documented manual contract; not automated. |
| `VAL-H0-DELETE-001` | No silent deletion | Diff register IDs and versions against the prior protected main. | Removed finding without exact preserved supersession evidence blocks. | Documented manual contract; not automated. |
| `VAL-H0-RESOLVE-001` | Resolution evidence | Verify issue, PR, reviewed head, tests, independent result, human approval, protected merge, current main, closeout, and fresh live evidence where applicable. | Missing applicable evidence prevents `COMPLETED_AND_VERIFIED`. | Documented manual contract; not automated. |
| `VAL-H0-STALE-001` | Stale evidence detection | Compare observation date, expiry, registered retest triggers, and live GitHub. | Triggered or expired evidence becomes `EVIDENCE_STALE_REVERIFICATION_REQUIRED`. | Documented manual contract; not automated. |
| `VAL-H0-DEFER-001` | Valid deferral extension contract | Find every record with `CURRENT_STATUS=VALIDLY_DEFERRED`; require all seven extension fields; reject empty, placeholder, circular, or unresolvable values; require a responsible gate, revisit trigger, expiry or maximum review date, preservation evidence, and explicit prohibited interim actions; fail when Issue #79 requirements are not satisfied. | `INVALID_OR_INCOMPLETE_DEFERRAL=BLOCK` | Documented manual contract; not automated. |
| `VAL-H0-STARTUP-001` | Startup-packet finding coverage | Verify all seven startup fields and all affected IDs against the exact register ref/main SHA. | Omitted, stale, conflicting, or unauthorized finding evidence blocks the affected gate within documentation scope. | Documented manual contract; collector automation not implemented for this schema. |
| `VAL-H0-HANDOFF-001` | Handoff finding coverage | Verify all seven handoff fields and exact IDs/classifications. | No affected finding silently disappears between windows. | Documented manual contract; not automated. |
| `VAL-H8-AI-001` | App-permission drift review | Re-read connector scope, repositories, permission grants, principals, provider roles, and organization policy. | Drift is recorded as a changed or new finding before H8 action. | Manual; required on registered triggers. |
| `VAL-H8-AI-002` | Repository-transfer revalidation | Compare pre-transfer and post-transfer app installations, access scope, permissions, principals, and organization policy. | Any unreviewed difference blocks H8 closeout and H9 assurance. | Manual; transfer is not authorized by this packet. |
| `VAL-H8-AI-003` | H8 revocation and least-privilege tests | Test selected-repository restriction, separate developer/reviewer principals, revocation, denied unauthorized repositories, and audit attribution. | All owner-approved least-privilege and revocation cases pass with independent evidence. | Not started; H8 implementation not authorized. |
| `VAL-H8-AI-004` | AI and OAuth permission detail evidence capture | For `CLAUDE`, `COPILOT_CHAT_APP`, `COPILOT_SWE_AGENT`, and `GITHUB_DESKTOP_OAUTH`, capture exact application name, application type, exact permissions or OAuth scopes, repository or organization access where applicable, observation timestamp, evidence source, and reviewer classification; infer nothing from application presence alone. | `MISSING_PERMISSION_DETAILS_BLOCK_H8_IMPLEMENTATION` | Not started; live evidence is required before H8 implementation or any permission change. |
| `VAL-H7A-SEC-001` | H7A security-setting revalidation | Live-read each named security setting and prove operative dependencies such as CodeQL before relying on downstream features. | Dated values and operative/inoperative status are explicit; discrepancies block. | Not started; H7A implementation not authorized. |
| `VAL-H7A-SUPPLY-001` | Full-SHA action reference | Inspect workflow at exact head and verify each governed third-party action reference against the approved full commit SHA. | Mutable tags fail the H7A contract. | Not started; workflow change not authorized. |
| `VAL-H9-FIND-001` | Permission drift and finding-closure assurance | Re-run all finding freshness, resolution, permission, security, supply-chain, and supersession contracts against current main and live GitHub. | No known unresolved blocking finding is represented as closed; residual risks have exact owner acceptance and expiry. | Not started; H9 assurance not authorized. |

```text
VALIDATION_ID=VAL-H8-AI-004
TITLE=AI_AND_OAUTH_PERMISSION_DETAIL_EVIDENCE_CAPTURE # documentation scope
VALIDATION_ID=VAL-H0-DEFER-001
TITLE=VALID_DEFERRAL_EXTENSION_CONTRACT
```

`VAL-H8-AI-003` is reserved only for future revocation and least-privilege implementation testing. Issue #79 controls deferral requirements; the findings register records compliance and does not replace the master roadmap.

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
| VAL-PRE4K9-006 | Verify pre-marker PR behavior. | GitHub Actions after PR creation and after every correction head. | Pre-marker checks pass; mandatory exact-SHA marker fails; later checks may skip. | Initial run `29172467406` observed: steps before the marker passed, marker failed as expected, and later steps skipped. A fresh run is required for the correction head. |

## Historical Issue #49 Validation Tasks

The status cells in this section preserve successive Issue #49 / PR #50 implementation checkpoints. Any pending commit, push, exact-head workflow, collector, review, approval, merge, or closeout statement is `HISTORICAL_LIFECYCLE_STATE`; Issue #49 is closed and PR #50 is merged at `7d00343c233e45185e6c4d77e50eb870f408c01f`.

| Task ID | Task | Command or check | Expected result | Status |
|---|---|---|---|---|
| VAL-I49-001 | Run the standard-library unit suite. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/continuity/tests -p 'test_*.py'` | All fixture, security, determinism and lifecycle tests pass. | 30 tests passed in the final pre-implementation-commit sequence. |
| VAL-I49-002 | Prove deterministic JSON and Markdown. | Two identical fixture runs and byte comparisons. | Both comparisons match byte for byte. | Pending final validation sequence. |
| VAL-I49-003 | Verify exit contract fixtures. | Run consistent, active, stale, moved-head, missing, unsafe and malformed cases. | Exit `0`, `0`, `2`, `2`, `3`, `4`, and `5`. | Covered by unit suite; explicit CLI capture pending. |
| VAL-I49-004 | Verify command and shell security. | Unit command rejection and subprocess mock tests. | Unknown/write-capable shapes fail; subprocess uses argument array and `shell=False`. | Passed in unit suite. |
| VAL-I49-005 | Verify output boundary. | Repository path, directory symlink, file symlink and exact file-count tests. | Escape attempts return unsafe failure; safe output contains exactly two files. | Passed in unit suite. |
| VAL-I49-006 | Verify private-data boundary. | Unsafe fixture and absolute-home-path tests. | Unsafe/private-looking evidence returns exit `4` or is rejected before output. | Passed in unit suite. |
| VAL-I49-007 | Run starting-main stale baseline. | Live Issue #47, PR #48, run `29176103821`, canonical ref `01b90ab8b12416101b4be067794bf543a3488779`. | Exit `2`; stale canonical main, issue, PR and lifecycle differences are visible; status unchanged. | Passed with exit `2`, all four stale findings, packet hash `a0d86fd3e7ac279435fef3ac6c364cfd123a2b7c068ba38f62733389754978c1`, and unchanged status. |
| VAL-I49-008 | Validate active PR live evidence. | Live Issue #49, PR #50, current run and exact implementation ref. | Exit `0`, `requires_live_verification`, missing external review and human approval pending, auto-merge inactive. | Passed for implementation head `ee0ffc7c17072543cf818849252a8c07d2019538`, run `29177537570`, exit `0`, packet hash `4dcf61157d2ca1a6c2b4deb90666c67110aa1802f283ebeb93d6f7d7aca4f3f8`, and unchanged status. Final-head rerun required. |
| VAL-I49-009 | Validate both JSON schemas and runtime structure. | JSON parse plus unit malformed-object tests. | Schemas parse and malformed structures return exit `5`. | Schema parse and unit structure tests passed; final rerun required. |
| VAL-I49-010 | Run all current control validators. | Required Issue #49 local control sequence. | Every local validator passes; external review marker remains absent. | Full pre-implementation-commit sequence passed. Final evidence-only changes require a narrow rerun before the reconciliation commit. |
| VAL-I49-011 | Validate ten-field prompt profile and hidden-metadata fallbacks. | Continuity unit suite governance-profile tests. | Exact fields are ordered and non-empty; hidden model, effort, and speed are not fabricated or treated as a stop. | Passed in 45-test governance-hardening suite. |
| VAL-I49-012 | Validate proportional routing and Plus defaults. | Continuity unit suite routing tests. | Medium, Standard, and one lead are defaults; Fast needs justification; Ultra is not default. | Passed in 45-test governance-hardening suite. |
| VAL-I49-013 | Validate quota packets and context rotation. | Continuity unit suite context tests. | Atomic packet fields exist; 79% requires a new window; 85% is handoff-only. | Passed in 45-test governance-hardening suite. |
| VAL-I49-014 | Validate compact structured progress. | Continuity unit suite progress tests. | Required phase and program rows exist; paragraph compression is prohibited; capability categories remain separate. | Passed in 45-test governance-hardening suite. |
| VAL-I49-015 | Validate interactive-chart contract. | Continuity unit suite chart tests. | Exactly one actual chart is last where supported; raw chart configuration is prohibited; unsupported surfaces retain compact tables. | Passed in 45-test governance-hardening suite. |
| VAL-I49-016 | Verify forbidden changed paths remain untouched. | Existing changed-file, forbidden-scope, lockfile, and diff checks. | No workflow, `scripts/control/**`, manifest, lockfile, application, runtime, or private path changes. | Passed in final governance-hardening control sequence. |
| VAL-I49-017 | Validate red-team prompt-profile inheritance. | Continuity unit suite protocol tests. | Six generated-prompt classes require the exact ordered non-empty profile, visible-selector preservation, hidden fallbacks, defaults, atomic packets, context rotation, and final attestations. | Passed in 55-test G1.1 suite. |
| VAL-I49-018 | Validate dated official-source reconciliation. | Prompt/source-register unit tests plus official-page review. | Review date and three official URLs are present; stable policy and dated guidance are separate; time-sensitive facts require revalidation. | Passed in 55-test G1.1 suite and official-page review. |
| VAL-I49-019 | Validate historical-source supersession. | Source-register unit test. | GPT-5.5-only guidance is retained as historical and marked superseded for current policy. | Passed in 55-test G1.1 suite. |
| VAL-I49-020 | Validate chart capability wording. | Red-team-protocol unit tests. | Interactive chart is actual and last; hover/tooltips are conditional; expand/drill-down is conditional; hover does not imply expandability; Markdown fallback and raw-config prohibition remain. | Passed in 55-test G1.1 suite. |
| VAL-I49-021 | Validate prior-head workflow evidence. | Report unit test and `gh run view 29203963944`. | Head, completed/failure status, pre-marker passes, marker absence/failure, skipped post-marker checks, and no decision power are exact. | Passed in 55-test G1.1 suite and live run inspection. |
| VAL-I49-022 | Run focused C1A marker semantics. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.continuity.tests.test_red_team_continuity.MarkerSemanticsTests` | Exact red-team and owner-trigger semantics, fail-closed ambiguity and ignored examples pass. | Passed: 32 tests. |
| VAL-I49-023 | Run the complete continuity suite after C1A. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/continuity/tests -p 'test_*.py'` | Collector, determinism, security, governance and marker semantics pass without fixture changes. | Passed: 87 tests. |
| VAL-I49-024 | Run all existing local controls without validator edits. | Required Issue #49 eleven-command sequence. | Five-file C1A allowlist passes; no workflow, control-script, fixture, schema, manifest, lockfile or product/runtime change. | Passed in final C1A local-control sequence. |
| VAL-I49-025 | Run focused C1B workflow-provenance behavior tests. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.continuity.tests.test_red_team_continuity.WorkflowProvenanceTests` | Identity, link, job, step, pending and contradiction classifications pass. | Passed: 28 tests. |
| VAL-I49-026 | Run the complete continuity suite after the `1.1.0` migration. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/continuity/tests -p 'test_*.py'` | All prior 87 tests and 28 C1B tests pass. | Passed: 115 tests. |
| VAL-I49-027 | Validate deterministic `1.1.0` fixture output and both schemas. | Two fixture generations, byte comparisons, and `python3 -m json.tool` for each schema. | Both generated files are byte-identical and both schemas parse. | Passed; JSON and Markdown match byte for byte, both schemas parse, consistent-fixture packet hash `556ef5a137869e896ad25a4da3cf2e10065aa3f1674ea0da282efa7477ba55b9`. |
| VAL-I49-028 | Run the migrated live collector against the exact reviewed C1A head and run. | Issue #49, PR #50, run `29205653852`, canonical ref `0801bd6497a3e16fa0565c7ac13a6a455da962f9`. | Exit `0`; `requires_live_verification`; exact workflow/check binding; pre-marker success, marker failure for missing evidence, post-marker skipped; consequential action blocked pending review. | Passed at `2026-07-12T19:30:00Z`; packet hash `49614f0f6afd703fd05efca4f45bcc056a6a5f407020e589c9e3c5330ea34af1`; repository status unchanged apart from authorized C1B edits. |
| VAL-I49-029 | Run all current local controls without workflow or validator edits. | Required Issue #49 eleven-command sequence. | Sixteen-path C1B allowlist passes; no workflow, control-script, manifest, lockfile or product/runtime change. | Passed in final C1B local-control sequence. |
| VAL-I49-030 | Run the 30 focused C2 approval-evidence behavior tests and complete continuity suite. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.continuity.tests.test_red_team_continuity.ApprovalEvidenceTests` and full discovery. | All C2 tests and all retained 115 tests pass. | Passed: 30 focused tests and 145 total tests. |
| VAL-I49-031 | Validate bounded REST command shapes and reviewer-state reduction. | C2 scope tests cover API rejection, pagination, sourced-login, exact-head, latest-decisive-state, author/bot and permission evidence. | Only fixed GET routes qualify; all adversarial classifications match the C2 contract. | Passed in the focused C2 class and live command evidence. |
| VAL-I49-032 | Validate deterministic `1.2.0` output and both schemas. | Two identical fixture generations, byte comparisons, independent packet-hash recomputation, and `python3 -m json.tool` for each schema. | Both generated files are byte-identical, packet hash matches, and both schemas parse. | Passed after scanner-safe fixture reconciliation; hash `04a815d64dd69f551ed0a60a3ed3fd3113270cee381565f65324d79532e67e5e`. |
| VAL-I49-033 | Run C2 live collector against exact starting head and run. | Issue #49, PR #50, run `29206726405`, canonical ref `eb655a245466220970fde97070f6d40c426d0051`, explicit timestamp and external output directory. | Exit `0`; `requires_live_verification`; complete review evidence; zero qualifying approvals; human approval pending; repository unchanged except C2 edits. | Passed at `2026-07-12T20:20:27Z`; packet hash `12892194f2b57e4a731779cd52988e3282756fb4f34f235ebcd1536af76ba7b5`. |
| VAL-I49-034 | Run the complete current local-control sequence for C2. | Eleven required validator and diff commands from the C2 prompt. | All controls pass without workflow or validator modification. | Passed in the final C2 local-control sequence. |
| VAL-I49-035 | Reproduce the pull-request-context forbidden-scope scan after the first C2 run failed before the marker. | `GITHUB_BASE_REF=main GITHUB_EVENT_NAME=pull_request python3 scripts/control/check_forbidden_scope.py` | Required approval-identity fields are explicitly scope-labeled; the full branch diff passes without validator modification. | Passed after scanner-safe correction; the first C2-head run `29207739830` is retained as failed evidence, not described as an expected marker failure. |
| VAL-I49-036 | Run focused C3 trust-boundary, lifecycle and reporting tests and the retained suite. | C3 test class plus full discovery. | All 51 new C3 cases and all prior 145 tests pass. | Passed: 51 focused C3 tests and 196 total tests. |
| VAL-I49-037 | Validate deterministic `1.3.0` output, independent hash and both schemas. | Two fixed-time consistent-fixture generations, byte comparisons, hash recomputation and both `json.tool` parses. | JSON/Markdown match, hash matches and schemas parse. | Passed; packet hash `ca5f2da6a3c2531c9f4a4985edd45a0de1d6e9b44841d21fbbee5a1b9fc0aa1b`. |
| VAL-I49-038 | Prove prohibited output rejection is pre-mutation. | Unique nested repository candidate, exit capture, absence and status comparison. | Exit `4`; candidate root absent; no output/temp files; status unchanged. | Passed. |
| VAL-I49-039 | Run live C3 collector against exact C2 head and run. | Issue #49, PR #50, run `29207994481`, canonical ref `053ac81a63dc44f448bfbf2ae58166eed8d927a3`, fixed timestamp and external output. | Exit `0`; pending classification; root/remote verified; marker missing; zero approvals; auto-merge inactive. | Passed at `2026-07-12T21:15:00Z`; packet hash `bd4bd6079922c85d4b81eaeafc38781f1bcae88c165195073114525ba4e04078`. |
| VAL-I49-040 | Validate permanent reporting layout from amendments `4952599609` and `4952612646`. | Seven focused C3 protocol tests. | Within reporting scope, Product stage and lifecycle are retained; separate readiness section is prohibited; three series and combined bottom fallback are required; nothing follows. | Passed. |
| VAL-I49-041 | Run the complete local and pull-request-context control sequences for C3. | Required validator and diff commands without workflow/control edits. | All controls pass and changed paths remain within the C3 allowlist. | Passed: all eleven local controls and all three PR-context reproductions. |
| VAL-I49-042 | Run the 22 focused C3.1 fail-closed tests and complete continuity suite. | C3 class plus full discovery. | All 22 new cases and all prior 196 tests pass. | Passed: 73 focused C3 tests and 218 total tests. |
| VAL-I49-043 | Validate deterministic `1.3.1` output, independent hash and both schemas. | Two fixed-time consistent-fixture generations, byte comparisons, hash recomputation and both `json.tool` parses. | JSON/Markdown match, independent hash matches and schemas parse. | Passed; consistent-fixture packet hash `c84d8905a14c998f085adb2fc3c9f3b3555e039e94056de7afe9d5b985418f76`. |
| VAL-I49-044 | Run the live C3.1 collector against Issue #49, PR #50, run `29209108826` and canonical ref `4b92dae569f07bbb4eedd117e9666e5bb340b9c4`. | Unique external output and explicit observation timestamp. | Exit `0`; `requires_live_verification`; authoritative repository fields complete; no fallback; root/remote verified; marker missing; zero approvals; auto-merge inactive. | Passed at `2026-07-12T21:44:03Z`; packet hash `278816f9f995ac665a700ac647ed7b6ee5caca9ad2c77917247b4026ab53aa31`. |
| VAL-I49-045 | Run the eleven local controls and three pull-request-context reproductions for C3.1. | Required validators and diff commands without workflow/control edits. | All controls pass and changed paths remain inside the authorized C3.1 set. | Passed in the final post-reconciliation rerun. |
| VAL-I49-046 | Inspect the new-head workflow. | Exact-head Actions run and governed step matrix. | Every pre-marker control passes; marker step fails only because the exact-head marker is absent; post-marker checks skip; overall conclusion is failure. | Pending after push. |
| VAL-I49-047 | Run the 30 focused C3.2 structural-classification tests and complete continuity suite. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.continuity.tests.test_red_team_continuity.FinalStructuralValidationCorrectionTests` and full discovery. | All 30 new cases and all prior 218 tests pass. | Passed: 30 focused C3.2 tests and 248 total tests. |
| VAL-I49-048 | Validate deterministic `1.3.2` output, independent hash and both schemas. | Two fixed-time consistent-fixture generations, byte comparisons, hash recomputation and both `json.tool` parses. | JSON/Markdown match, independent hash matches and schemas parse. | Passed; both outputs are byte-identical, schemas parse, and independent hash matches `87ec5d64a0c2ffba24e83aad47b29ae1d5c36c902f52e5f0cf652a46b6e34905`. |
| VAL-I49-049 | Prove unavailable-versus-contradictory live repository classification. | Direct live-structure behavior tests plus an offline valid-different repository fixture. | Missing/malformed identity returns exit `3`; valid different identity reaches comparison, quarantines and returns exit `2` without fallback. | Passed; unit tests preserve exit `3` for missing/malformed identity, and offline `Other/repository` evidence returned exit `2`, `quarantined=true`, with both repository-identity findings. |
| VAL-I49-050 | Run the live C3.2 collector against Issue #49, PR #50, run `29210362551` and canonical ref `29883ec704e16a9cc158b860603c0e7093260fc8`. | Unique external output and explicit observation timestamp. | Exit `0`; `requires_live_verification`; repository/root/remote complete; marker missing; zero approvals; auto-merge inactive. | Passed with exit `0`, `requires_live_verification`, verified root/remote, missing marker, zero qualifying approvals, pending human approval, inactive auto-merge and packet hash `0fe9d76fbece29cc439785e8f34b7a6548dac12cf18d7141cfb31398df4fe8a3`. |
| VAL-I49-051 | Run all eleven local controls and three pull-request-context reproductions for C3.2. | Required validators and diff commands without workflow/control edits. | All controls pass and changed paths remain inside the authorized C3.2 set. | Passed after validator-safe scope labels and claim wording; all eleven local controls and the forbidden-scope, required-update and PR-contract pull-request reproductions pass without workflow/control edits. |
| VAL-I49-052 | Inspect the exact C3.2 new-head workflow. | Exact-head Actions run and governed step matrix. | Every pre-marker control passes; marker fails only because the exact-head marker is absent; post-marker checks skip; overall conclusion is failure. | Pending after push. |
| VAL-I49-053 | Run focused C3.3 authority-binding tests and complete continuity suite. | C3.3 class plus full discovery. | Source binding, nullable live fields, timestamp validation and canonical reconciliation pass without regression. | Passed locally: 19 C3.3 tests and 267 total tests. |
| VAL-I49-054 | Validate deterministic `1.3.3` output and both schemas. | Two fixed-time fixture generations, byte comparisons, independent hash recomputation and `json.tool` parses. | Outputs match byte-for-byte, hash matches and schemas parse. | Passed; both outputs are byte-identical, schemas parse, and independent hash matches `bab6c5137aadc344f23cb0651794d9b02414b9a4ea331f445b7571e32a7137b6`. |
| VAL-I49-055 | Run C3.3 live collector against the recovered exact head and required workflow. | Issue #49, PR #50, run `29211199001`, canonical ref `09243095e3224db872f8c0b843ba19716abdec8b`, explicit timestamp and unique external output. | Exit `0`; `requires_live_verification`; scope-bound authority bindings agree; marker missing; zero approvals; inactive auto-merge. | Passed at `2026-07-12T23:00:00Z`; exit `0`, `requires_live_verification`, zero qualifying approvals, inactive auto-merge and packet hash `a88e787144f16dbdca306ff8cab8d801299cbd521cbfcb4ee28c8b7877b5e00f`. |
| VAL-I49-056 | Run all local and pull-request-context controls for C3.3. | Eleven local controls, three PR-context reproductions and both diff checks without workflow/control edits. | All pass with only authorized files changed. | Passed; all eleven local controls, all three live-body PR-context reproductions and both diff checks pass without workflow or control-script edits. |
| VAL-I49-057 | Inspect the exact C3.3 new-head workflow. | Exact-head Actions run and governed step matrix. | Pre-marker controls pass; marker failure is the only failure; post-marker checks skip. | Pending commit and push. |
| VAL-I49-058 | Run focused C3.4 scope-bound identity, worktree, structure, ordering, `closedAt`, and closed-gate base tests. | C3.4 class plus existing continuity tests. | Each malformed fixture exits `5`; malformed authoritative live input exits `3`; mismatched identity and dirty/changed worktree cannot qualify. | Passed locally: 13 focused C3.4 tests within 280 total tests. |
| VAL-I49-059 | Validate coherent `1.3.4` fixture, evidence and packet contracts. | Two fixed-time fixture generations, byte comparison, hash recomputation and both schema parses. | Outputs and hashes match byte-for-byte; both schemas parse. | Passed: byte-identical output, matching independent hash `13e2927970f1b6176b33549ebe765c834355eb355b8e97c9283d4218a38e65f7`, and both schemas parse. |
| VAL-I49-060 | Run C3.4 scope-bound controls and exact-head live collector after commit/push. | Authorized local controls, PR-context checks, exact-new-head Actions run and outside-repository live output. | Only permitted paths change; pre-marker controls pass; marker remains absent; live collection proves clean unchanged worktree. | Pending commit and push. |
| VAL-I49-061 | Validate staged four-field live review collection and seven-field evaluation. | C3.5 focused class. | Zero approvals and valid current-head approvals reduce successfully; malformed live evidence blocks `3`, malformed fixture evidence returns `5`, and contradictions fail closed. | Passed locally in focused C3.5 validation. |
| VAL-I49-062 | Validate explicit all-untracked worktree and stable HEAD provenance. | C3.5 focused class. | Old status shape is rejected; tracked, staged, untracked, changed hash, or moving HEAD cannot qualify. | Passed locally in focused C3.5 validation. |
| VAL-I49-063 | Validate review claim consistency and issue `closedAt` lifecycle pairing. | C3.5 focused class. | Overlap/unmatched reasons/unsupported `_evidence` fail closed; open/null and closed valid RFC3339 pairs succeed; contradictions block or return `5` by source. | Passed locally in focused C3.5 validation. |
| VAL-I49-064 | Validate coherent C3.5 `1.3.5` fixture, evidence, and packet contracts. | Two fixed-time consistent-fixture generations, byte comparisons, independent hash recomputation, and both schema parses. | Evidence JSON and packet Markdown are byte-identical; packet hashes agree; schemas parse. | Passed; packet hash `f1aa0c3bfe76d8d063579a5019f748bff1514fa6bdda94ea47ed660763415989`. |
| VAL-I49-065 | Run C3.5 local and pull-request-context controls. | Required controls, three PR-context reproductions, and both diff checks without workflow/control edits. | Only 17 authorized paths change; all controls pass. | Passed locally; exact-new-head workflow and live collection remain pending after commit and push. |
| VAL-I49-066 | Validate exact C3.6 command firewall and mocked live command acceptance. | C3.6 focused command tests and mocked live collection. | Required commands are accepted only in exact current-invocation shapes; repository/issue/PR/run/flag/field mutations reject with exit `5`. | Passed locally in the C3.6 focused class. |
| VAL-I49-067 | Validate C3.6 canonical reason-map collision and schema contracts. | C3.6 focused collision and standard-library schema-contract tests. | Case-only collisions fail at exit `5`; `_evidence` permits only the evidence-wide reason; reviewer-specific reasons remain permitted. | Passed locally in the C3.6 focused class. |
| VAL-I49-068 | Validate C3.6 source-command bounds and deterministic output. | C3.6 bound tests, two fixed-time generations, byte comparisons, independent hash recomputation, and schema parses. | 119 legal source commands are accepted; 120 rejects; evidence/packet and hashes agree deterministically. | Passed locally; both outputs are byte-identical, both schemas parse, and independent hash matches `8755f33d6416160ad16af824ead9e53d3a3a183f8f823f4546721ce7c7ea75d0`. |
| VAL-I49-069 | Run C3.6 scope-bound local and PR-context controls. | Required controls, three PR-context reproductions, diff checks, exact-head workflow, and outside-repository live collector. | Only authorized paths change; marker remains absent; expected pre-marker workflow matrix and live classification hold. | Passed locally: all required controls, both diff checks, and all three PR-context reproductions pass; exact-new-head workflow and live collection remain pending delivery. |
| VAL-I49-070 | Validate C3.7 reviewer-wide adverse-state reduction. | Focused approval-evidence tests. | Every reviewer is reduced by UTC instant; unresolved current-head changes requested remain adverse through comments and other approvals, clear only on later approval/dismissal, and stale-head records remain nonblocking evidence. | Passed within 68 focused C3.7 plus C3.6 regression tests. |
| VAL-I49-071 | Validate C3.7 semantic source-command claims. | Focused source-command tests. | Exact live-generated histories and sourced permission reads pass; mutations, wrong identities/refs/pages/fields, unsourced permission reads, argument changes and nonzero results return exit `5` without output or traceback. | Passed within 68 focused C3.7 plus C3.6 regression tests. |
| VAL-I49-072 | Validate coherent `1.3.7` fixture, evidence and packet contracts. | Two fixed-time generations, byte comparison, independent hash recomputation and both schema parses. | Outputs and hashes match byte-for-byte; both schemas parse. | Passed; both outputs are byte-identical, schemas parse, and independent hash matches `40667c04edb9bce8d4c3aae4efae2f3f9c8d782261707db4359171ea540be4d8`. |
| VAL-I49-073 | Run the complete C3.7 continuity suite and required local/PR-context controls. | Full discovery, eleven local controls, three PR-context reproductions and both diff checks. | All tests and controls pass with only the 17 permitted paths changed. | Passed: 329 total tests, all eleven local controls, all three PR-context reproductions and both diff checks pass. |
| VAL-I49-074 | Inspect and collect exact-new-head C3.7 evidence. | Push one normal commit, inspect the exact-head workflow, run the collector outside the repository and reconcile PR #50. | Expected absent-marker matrix; exit `0`; `requires_live_verification`; clean unchanged worktree; PR body bound to C3.7 exact head and live packet hash. | Pending commit and push. |
| VAL-I49-075 | Validate C3.8 review ordering, canonical provenance and return-code equivalence. | Focused C3.8 direct-generation, CLI and schema-contract class. | Every malformed review case returns exit `5` without traceback/output before firewall construction; exact canonical refs and zero return codes alone pass. | Passed: 7 focused tests covering direct/CLI matrices and both schemas. |
| VAL-I49-076 | Validate the complete `1.3.8` continuity contract and determinism. | Full discovery, two fixed-time generations, byte comparisons, independent hash recomputation, both schema parses, semantic assertions and exit matrix. | All tests pass; outputs and hashes match; current schemas bind exact canonical ref and return code zero. | Passed: 336 tests; byte-identical evidence and packet; independent hash `733034ae5d75ad54065da906d11f01ac6e461df09b81623357b00833dc3ff266`; both schemas parse; fixture exits `0/0/2/2/3/4/5`. |
| VAL-I49-077 | Run C3.8 local and pull-request-context controls. | Eleven local controls, three Issue #49 PR-context reproductions and both diff checks. | All controls pass with only the 17 authorized paths changed and no workflow/control-script edit. | Passed after validator-safe scope labeling: all eleven local controls, all three PR-context reproductions and both diff checks pass; cumulative PR file count remains 32. |
| VAL-I49-078 | Inspect and collect exact-new-head C3.8 evidence. | Push one normal commit, inspect the exact-head workflow, run the collector outside the repository and reconcile PR #50. | Expected absent-marker matrix; exit `0`; `requires_live_verification`; exact canonical ref; zero command returns; clean unchanged worktree; PR body bound to C3.8 exact head and live packet hash. | Pending commit and push. |

## H1 Project-Control Reconciliation — Historical Initial R4 Validation Tasks

| ID | Task | Method | Expected result | Status |
|---|---|---|---|---|
| VAL-H1-R3-001 | Verify attached contract identity. | SHA-256 and UTF-8 byte count. | `52df643dbd5fcce2b1d8b018730c8762b60900a806bf97f5a2c9c2b5946e4726`; 27736 bytes. | Passed before mutation. |
| VAL-H1-R3-002 | Verify exact repository/base/worktree. | Read-only scope: repository root, origin, branch, local HEAD, fetched `origin/main`, live remote main, and status. | Product repository; exact approved base; clean worktree. | Passed before branch creation. |
| VAL-H1-R3-003 | Verify corrected authentication. | Read-only scope: active GitHub login, repository push permission, and live remote-main SHA. | `Zest-LeadGen`; push `true`; exact approved base; pass. | Passed before branch creation. |
| VAL-H1-R3-004 | Verify recovery authority. | Read-only scope: direct Issue #58/comment reads and exact body hashing. | Issue open; comment `4975617497` exact hash; approval comment contains exact contract hash. | Passed before branch creation. |
| VAL-H1-R3-005 | Verify prior gate closeout. | Direct Issue #49 and PR #50 reads. | Issue closed; PR merged at `7d00343c233e45185e6c4d77e50eb870f408c01f`. | Passed before branch creation. |
| VAL-H1-R3-006 | Verify PR #56 conflict-cleared state. | Direct PR, branch, reaction, comment, and Issue #55/#53 reads. | Closed unmerged; exact head; branch preserved; disposition comment exists; zero reactions; both issues open. | Passed before branch creation. |
| VAL-H1-R3-007 | Verify target governance repository. | Direct repository, branch, and commit reads. | Public, size zero, zero branches, empty Git history response. | Passed before branch creation. |
| VAL-H1-R3-008 | Verify no serialized-state PR overlap. | List open PRs and inspect every changed-file set. | Sole open PR #9 has no overlap with the 31-path reconciliation allowlist. | Passed before branch creation. |
| VAL-H1-R3-009 | Verify existing allowlist. | Exact 27-path existence check. | All 27 existing records present. | Passed before branch creation. |
| VAL-H1-R3-010 | Verify exact changed-file set. | Contract allowlist diff assertion. | No unexpected path; all four required new files present; 31 changed files. | Passed before staging. |
| VAL-H1-R3-011 | Verify canonical state. | JSON parse and exact targeted assertions. | Main, Issue #58, null PR, completed Issue #49/PR #50, consistency status, and evidence identifiers match contract. | Passed before staging. |
| VAL-H1-R3-012 | Verify decision register. | `python3 -m json.tool`. | JSON-compatible YAML parses and record count equals decision count. | Passed with 32 declared and actual decisions. |
| VAL-H1-R3-013 | Run existing control suite. | Every contract-listed control, continuity test, parse, and diff command. | Every local and pre-marker control passes without validator or workflow edits. | Passed before staging; 336 continuity tests passed. |
| VAL-H1-R3-014 | Verify manual claim boundaries. | Targeted searches and file review. | No stale current Issue #49/PR #50 claim, product-direction change, local-artifact promotion, H1 acceptance, invented storage, perfect-truth claim, deletion, or forbidden path. | `INITIAL_R4_STALE_STATE_SEARCH=PASSED_WITH_LATER_MISSED_DEFECTS`; R5 later found incomplete current-state reconciliation in `R5-STATE-001`. |
| VAL-H1-R3-015 | Verify staged and committed state. | Historical initial R4 checkpoint: cached diff checks; one commit; parent/base; post-commit diff; clean status. | Exact original 31-path PR diff, no deletion/rename/move, one initial implementation commit above the approved base, clean handoff worktree. | Passed for initial R4 implementation commit `6a567366ed992ddb0f8b28ca28a43d874f53bc70`; its parent was the approved base and the initial handoff worktree was clean. |
| VAL-H1-R3-016 | Verify remote branch and PR. | Historical initial R4 checkpoint: GitHub account-identity and push-permission verification, one push, one PR, remote-head equality, PR files/commits/checks. | Initial remote head and PR metadata agree; pre-marker checks pass; missing exact-SHA red-team marker is the only expected gate failure. | Passed for the initial branch, PR #75, and workflow run `29385059008`: steps 4–9 passed, the missing-marker gate failed as expected, and later checks skipped. Resulting correction-head evidence must be retrieved live. |

## H1 R5 Whole-PR Stale-State Correction Validation

```text
INITIAL_R4_STALE_STATE_SEARCH=PASSED_WITH_LATER_MISSED_DEFECTS
R5_DECISION=CHANGES_REQUESTED
R5_FINDING=R5-STATE-001
R5_REVIEWED_HEAD=572f25898d61a39d762f83bd0a17e9b40b0c5d1b
R5_FINDING_CLASS=INCOMPLETE_CURRENT_STATE_RECONCILIATION
CURRENT_CORRECTION=OWNER_AUTHORIZED_BOUNDED_ELEVEN_FILE_CORRECTION # documentation scope
FRESH_EXACT_SHA_REVIEW_AFTER_CORRECTION=REQUIRED
```

| ID | Task | Method | Expected result | Status |
|---|---|---|---|---|
| VAL-H1-R5-001 | Verify documentation-scope correction authorization identity and controls. | Discover the unique Issue #58 comment containing the exact authorization ID; hash the raw UTF-8 body; verify author, controls, exact eleven-file allowlist, subject, one-commit/one-push limits, and absence of later contradiction. | Comment `4978245466`; SHA-256 `5486cd21cac3bc457e25d42f9c885dfa29e8f557788e9e1cfadc9f3c66aadbd2`; 4103 bytes; exact controls pass. | Passed before mutation. |
| VAL-H1-R5-002 | Inspect the complete whole-PR stale-state surface before correction. | Review complete current contents and base-to-head diff for all 31 PR paths; search all required lifecycle terms in context. | No required correction outside the authorized eleven paths; historical evidence remains explicit. | Passed before mutation; no twelfth-file conflict found. |
| VAL-H1-R5-003 | Verify the correction changed exactly eleven existing paths. | Compare working-tree paths to the exact correction allowlist; inspect status and name-status. | Exact eleven-file match; zero new, deleted, renamed, or moved files. | Passed: exact eleven existing modified paths; zero additions, deletions, renames, or moves. |
| VAL-H1-R5-004 | Re-run deterministic whole-PR stale-state assertions. | Reinspect all 31 paths after correction; evaluate each required entity in its complete heading, row, paragraph, or record context. | Zero current-active claims for Issue #47, Issue #45, PR #46, Phase 4K-8, Issue #49, PR #50, or PR #15; history preserved; Issue #58/PR #75 recovery and all stop boundaries remain explicit. | Passed: every required legacy lifecycle reference is explicitly historical or a non-authorizing technical-risk record; Issue #58/PR #75 and all stop boundaries remain current. |
| VAL-H1-R5-005 | Run focused and complete local validation. | Required seven focused commands plus the full continuity/control/parse/diff sequence from the owner packet. | All non-tolerated commands pass; continuity count is 336. | Passed before staging: all focused and complete commands passed; continuity count is 336. |
| VAL-H1-R5-006 | Bind later acceptance to the resulting exact head. | One normal commit, one non-force push, exact-new-head workflow inspection, and fresh independent whole-PR review. | Pre-marker checks pass; marker fails only because absent; later steps skip; fresh exact-SHA review remains required. | Developer delivery pending; no marker, approval, merge, closeout, or H1 bootstrap authorized. |

## H1 Issue #76 Next-Window Handoff Contract Validation

The initial Developer validation and R1 correction evidence below are historical. R2 reviewed the R1 correction head and required this separately authorized six-file, event-invariant lifecycle correction (documentation scope).

```text
INITIAL_DEVELOPER_DELIVERY=COMPLETED_AT_486a55dd17b578ad2dcbee1f05debb5337e7a32c
R1_RESULT=CHANGES_REQUESTED
R1_FINDING_1=R1-OUTPUT-ORDER-001
R1_FINDING_2=R1-STATE-002
R1_CORRECTION_HEAD=5ac454ae2ce2c12dd144ab688dfdb02f5202cb92
R2_REVIEWED_HEAD=5ac454ae2ce2c12dd144ab688dfdb02f5202cb92
R2_RESULT=CHANGES_REQUESTED
R2_FINDING_1=R2-STATE-001
R2_FINDING_2=R2-TEST-001
R2_CORRECTION_AUTHORITY_COMMENT=4984934461 # documentation scope
R2_CORRECTION_IMPLEMENTATION=THIS_COMMIT
CURRENT_PR_HEAD=LIVE_GITHUB_REQUIRED
REMOTE_DELIVERY_STATE=LIVE_GITHUB_REQUIRED
PR_BODY_REPLACEMENT_STATE=LIVE_GITHUB_REQUIRED
EXACT_HEAD_WORKFLOW_STATE=LIVE_GITHUB_REQUIRED
CURRENT_RED_TEAM_REVIEW_STATE=LIVE_GITHUB_REQUIRED
NEXT_GATE=FRESH_INDEPENDENT_WHOLE_PR_REVIEW_AFTER_LIVE_VERIFICATION
```

| ID | Task | Method | Expected result | Status |
|---|---|---|---|---|
| VAL-H1-76-001 | Verify historical initial authorized starting state. | Documentation-scope fetch of `main`; compare local, origin, and fetched live SHA; inspect worktree, issues, target branch, and existing PRs. | All main refs equal `98aa418aca568eca0c98cedb017488c711bb50ed`; clean worktree; Issues #76 and #58 open; the initial delivery branch and PR had not yet been created. | Passed before the historical initial implementation mutation. |
| VAL-H1-76-002 | Prove the ordered Codex prompt profile remains unchanged. | Existing and new governance tests plus exact field-order/count assertions. | Ten ordered prompt-profile fields remain in their prior order. | Passed in focused and complete continuity validation. |
| VAL-H1-76-003 | Prove the explicit navigation contract remains in governing documents. | Focused static tests over the red-team protocol, prompt convention, handoff playbook, and startup-packet specification. | Ten field labels, role/surface enums, no-window sentinels, direct-link rule, navigation-only boundary, and private-chat limitation are present. | Passed in focused and complete continuity validation. |
| VAL-H1-76-004 | Run the focused continuity module. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.continuity.tests.test_red_team_continuity` | All continuity tests pass without bytecode writes. | Passed: 342 tests. |
| VAL-H1-76-005 | Run complete continuity discovery. | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/continuity/tests -p 'test_*.py'` | All continuity tests pass without regression. | Passed: 342 tests. |
| VAL-H1-76-006 | Run all required local control checks. | Nine named control/diff commands from Issue #76. | Every control passes without workflow or validator changes. | Passed: all nine commands returned zero. |
| VAL-H1-76-007 | Verify exact bounded file and claim surface. | Name-status, allowlist, field counts, sentinel searches, and private-chat overclaim review. | Eleven authorized paths only; one new report; zero deletion, rename, workflow, product, runtime, schema, or fixture changes. | Passed: 10 modified paths, one new report, and zero forbidden paths or positive private-chat enforcement overclaims. |
| VAL-H1-76-008 | Bind the initial delivery to the exact PR head. | Historical initial commit, push, non-draft PR, exact live metadata, and workflow inspection. | Initial delivery is bound to `486a55dd17b578ad2dcbee1f05debb5337e7a32c`; R1 findings govern subsequent correction work. | Initial Developer delivery completed at `486a55dd17b578ad2dcbee1f05debb5337e7a32c`; R1 returned `CHANGES_REQUESTED`. |
| VAL-H1-76-009 | Validate canonical final response ordering. | Run the four named deterministic Issue #76 ordering/current-state tests directly and within full continuity discovery. | Product stage, lifecycle table, chart/fallback when required, and navigation appear in that semantic order; navigation is the sole absolute final response element. | Passed: four named focused tests and both 344-test continuity runs; fresh independent exact-SHA verification pending. |
| VAL-H1-76-010 | Prove conflicting chart-final language is absent. | Search the three governing files for every prohibited chart-final phrase and run the semantic regression test. | Zero conflicting chart-final instructions remain. | Passed: conflicting chart-final language count is zero; fresh independent exact-SHA verification pending. |
| VAL-H1-76-011 | Preserve historical R1 validation evidence. | Keep initial-delivery and R1 results distinct from R2 current-state assertions. | Historical initial and R1 facts remain explicit without asserting mutable post-R2 GitHub state. | Historical evidence retained. |
| VAL-H1-76-012 | Verify event-invariant lifecycle fields across the five active project-control records. | Static regression tests require every current record to distinguish R2 implementation from mutable GitHub state. | All five records contain the required `THIS_COMMIT`, `LIVE_GITHUB_REQUIRED`, and next-gate fields. | This commit. |
| VAL-H1-76-013 | Reject stale post-correction instructions. | Static regression tests search active/current Issue #76 sections case-insensitively for delivery, commit, push, body-replacement, and workflow instructions represented as repository facts. | No active record directs recreation of a mutable GitHub action; historical evidence remains separately classified. | This commit. |
| VAL-H1-76-014 | Verify exact six-file R2 correction scope. | Compare working-tree and staged name-status to the R2 allowlist. | Exactly six existing files changed; zero new files, deletions, renames, navigation-governing-file, workflow, validator, runtime/schema/fixture, or product/production changes. | This commit. |
| VAL-H1-76-015 | Preserve navigation-order governing documents. | Inspect the cumulative PR and correction diff. | No R2 modification to `RED_TEAM_OPERATING_PROTOCOL.md`, `PROMPT_CONVENTION.md`, `HANDOFF_PLAYBOOK.md`, or `RED_TEAM_STARTUP_PACKET_SPEC.md`. | This commit. |
| VAL-H1-76-016 | Verify one controlled PR-body replacement only through live evidence. | Retrieve live PR body after correction delivery; validate a body-only proposal and its hashes before the single authorized update (documentation scope). | Mutable body state is `LIVE_GITHUB_REQUIRED`; one replacement is accepted only after live verification. | Live GitHub required. |
| VAL-H1-76-017 | Verify the exact-head workflow only through live evidence. | Retrieve live workflow, review, and issue evidence for the live PR head after body verification. | Mutable workflow and review states are `LIVE_GITHUB_REQUIRED`; a fresh whole-PR review follows live verification. | Live GitHub required. |

## H0 Terminal-Disposition Validation

| Validation ID | Task | Method | Acceptance | Status |
|---|---|---|---|---|
| VAL-H0-TD-001 | Verify exact owner decision and starting state; documentation scope. | Live Issue #70 comments; identity/permission read; fetch; four-way SHA comparison; clean-tree check | Exact comment `5017555554`, owner identity, write permission, exact repo, clean tree, and all main views at `564fe30cd0e7e11896ef01ef4117940e1d42c2a3` | Passed before mutation. |
| VAL-H0-TD-002 | Verify the open-work matrix. | Strict JSON parse and ID/count checks | 28 records, zero duplicate IDs, every required field nonempty, only Issue #79 dispositions | Passed: 28 records, zero duplicates, required fields present, and disposition enum accepted. |
| VAL-H0-TD-003 | Verify the branch matrix. | Strict JSON parse, name/count checks, capture/live tip comparison, and branch-class assertions | 39 records, zero duplicate names, all live tips match capture, three unique-commit branches separated, deletion permission none | Passed: 39 records, zero duplicates, tips matched, special branches separated, deletion permission none. |
| VAL-H0-TD-004 | Verify evidence checksum and privacy. | SHA-256 check; JSON parse; email, local-path, secret-value, and raw-payload scans | Source checksum match; derived JSON parses; zero prohibited matches | Initial implementation passed; R1 final rerun required after all correction content and hashes are finalized. |
| VAL-H0-TD-005 | Run the required local control suite. | Nine commands named by Issue #70 comment `5017555554` | Every command returns zero without editing controls | Initial implementation passed locally; R1 full suite must rerun from the beginning after correction finalization. |
| VAL-H0-TD-006 | Verify exact changed paths and canonical hashes; documentation scope. | Correction/cumulative diff checks, canonical recomputation, raw SHA-256 | Exactly nine correction paths, ten cumulative paths, deterministic manifest/report canonical hashes, and raw hashes for handoff | R1 correction implementation in progress until live delivery. |
| VAL-H0-TD-007 | Verify initial post-PR live state. | PR readback, exact head SHA, changed-file listing, review and checks readback | PR #83 at initial head, one commit, exact ten paths, no approval/merge/close/delete action; hosted result represented honestly | Historically completed: initial head `887c88b4f3ad82dde3e5b6901636601612785920`, workflow run `29869266686`, R1 `CHANGES_REQUESTED`. |
| VAL-H0-TD-R1-001 | Validate all six R1 correction groups. | Exact-field assertions across the nine allowed files and cumulative diff | `R1-STATE-001`, `R1-FINDING-LIFECYCLE-001`, `R1-DISPOSITION-LINK-001`, `R1-DELTA-001`, `R1-HASH-001`, and `R1-VALIDATION-001` all pass | Passed locally: exact scope, counts, links, deltas, lifecycle fields, canonical/raw hash computation, stale-state rejection, and privacy assertions; live delivery remains pending. |
| VAL-H0-TD-R1-002 | Bind acceptance to the corrected exact head. | One normal push, exact-head workflow inspection, one PR-body replacement, live readback, and fresh independent whole-PR review | Pre-marker controls pass; marker is the expected failure; later checks skip; fresh exact-head review remains required | Live GitHub required after correction delivery; developer adds no decision, approval, merge, or closeout. |

```text
INITIAL_WORKFLOW_RUN=29869266686
INITIAL_CHANGED_FILE_ALLOWLIST=PASS
INITIAL_FORBIDDEN_SCOPE=PASS
INITIAL_REQUIRED_CONTROL_UPDATES=PASS
INITIAL_PR_CONTRACT=PASS
INITIAL_OWNER_TRIGGER=PASS
INITIAL_LOW_RISK_LANE=PASS
INITIAL_RED_TEAM_MARKER=EXPECTED_FAILURE
INITIAL_LOCKFILE_CHECK=SKIPPED
INITIAL_CLAIM_LANGUAGE_CHECK=SKIPPED
R1_REVIEW=RT_PR83_R1_CHANGES_REQUESTED
CORRECTION_AUTHORITY_COMMENT=5041407565 # documentation scope
CORRECTION_IMPLEMENTATION=IN_PROGRESS_UNTIL_LIVE_DELIVERY
CURRENT_PR_HEAD=LIVE_GITHUB_REQUIRED
CURRENT_HOSTED_WORKFLOW=LIVE_GITHUB_REQUIRED
NEXT_GATE=FRESH_INDEPENDENT_WHOLE_PR_EXACT_HEAD_REVIEW_AFTER_CORRECTION_DELIVERY
HUMAN_APPROVAL_ELIGIBLE=NO
MERGE_ELIGIBLE=NO
H0_MAY_CLOSE=NO
H1_IMPLEMENTATION_AUTHORIZED=NO # documentation scope
```
