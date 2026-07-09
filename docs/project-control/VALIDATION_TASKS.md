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
