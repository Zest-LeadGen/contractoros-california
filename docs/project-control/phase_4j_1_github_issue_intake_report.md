# Phase 4J-1 — GitHub Issue Intake + Linked Phase Issue Requirement Report

## Phase

Phase 4J-1 — GitHub Issue Intake + Linked Phase Issue Requirement

## Lane

Control / Infrastructure

## Starting Main SHA

```text
0f04efa564c4f28bd351881c00f72d41f540c319
```

## Scope

This phase moves future phase initiation out of chat-only prompts and into durable GitHub Issues.

Every future phase PR must link to a GitHub phase issue so scope, owner approvals, assumptions, risks, and red-team requirements are versioned and reviewable.

This phase does not touch app/product/dependency/build/backend/mobile/web files, does not activate auto-merge, does not bypass branch protection, does not merge, does not start Phase 4J-2, and does not resume Phase 4I.

## Linked Phase Issue

The Phase 4J-1 issue must be created before opening the PR.

Owner should create the issue using the issue body provided in the final handoff, then the PR body must use one accepted issue reference format such as `Phase issue: #123`.

## Changed Files

```text
.github/ISSUE_TEMPLATE/phase_issue.yml
.github/pull_request_template.md
.github/workflows/control-gates.yml
scripts/control/check_pr_contract.py
AGENTS.md
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/RISK_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/DEVELOPMENT_LEDGER.md
docs/project-control/phase_4j_1_github_issue_intake_report.md
```

## Commands Run

```text
git switch -c phase-4j-1-github-issue-intake
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --check
git add .github scripts/control docs/project-control AGENTS.md
git commit -m "Add Phase 4J-1 GitHub issue intake controls"
```

## Dependency / Lockfile Handling

No dependencies were added or changed.

No package files were changed.

No package-lock file was created or committed.

No npm install was run.

## Issue Template Impact

Phase 4J-1 adds `.github/ISSUE_TEMPLATE/phase_issue.yml`.

The issue template captures phase name, lane, owner-approved objective, explicit file allowlist, explicit forbidden scope, required evidence, assumptions, risks, validation tasks, red-team review requirement, human approval requirement, auto-merge prohibition/future-only status, and legal/financial/paid-service/release/security triggers.

## PR Template Impact

`.github/pull_request_template.md` now requires linked phase issue number, phase name, lane, scope summary, changed files, commands run, forbidden scope confirmation, validation evidence, red-team status, human approval status, auto-merge status, and next phase status.

Accepted issue reference formats are:

```text
Closes #123
Fixes #123
Resolves #123
Linked issue: #123
Phase issue: #123
```

## PR Template / CODEOWNERS Implemented

`.github/pull_request_template.md` was updated to require linked phase issue and review/approval evidence.

CODEOWNERS was reviewed and not changed in this phase.

## Control-Gate Impact

`scripts/control/check_pr_contract.py` now fails in PR context when the PR body lacks an accepted linked issue reference.

The existing workflow step that runs `check_pr_contract.py` remains in place and is renamed to describe linked-issue enforcement.

No existing control gate was removed or weakened.

## Workflow Validation

Local validation runs the same control scripts used by the ContractorOS control-gates workflow.

GitHub Actions workflow validation is pending until the branch is pushed and the PR is opened with a linked phase issue.

If the workflow fails, Phase 4J-1 must stop for patching before review or merge.

## Security Hardening

No workflow permission expansion was made.

No `pull_request_target` trigger was added.

No secrets, deployment, package install, Expo, EAS, native build, third-party action, auto-merge, approval bypass, or branch-protection bypass was added.

## Documentation Impact

Governance files updated:

```text
AGENTS.md
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/RISK_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/DEVELOPMENT_LEDGER.md
```

## Validation Evidence

Local validation commands for this phase:

```text
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --check
```

Reviewed control records with no update required:

```text
docs/project-control/DECISION_LOG.md: reviewed, no update required
docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required
```

## Risk Register Impact

`docs/project-control/RISK_REGISTER.md` records the risk that future phase work may lack a linked GitHub phase issue.

## Decision Log Impact

`docs/project-control/DECISION_LOG.md: reviewed, no update required`

## Design Decision Impact

`docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md` adds CDR-4J-020 — GitHub phase issue required for future PRs.

## Artifact Index Impact

`docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required`

Phase 4J-1 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.

## Red-Team Status

Red-team review is required before merge and has not yet occurred.

## Human Approval Status

Human/write-access approval is required before merge and has not yet occurred.

## Auto-Merge Status

Auto-merge is not active and is not authorized by Phase 4J-1.

## Requirements Traceability Impact

`docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md` records Phase 4J-1 linked-issue and issue-intake requirements.

## Validation Task Impact

`docs/project-control/VALIDATION_TASKS.md` records Phase 4J-1 validation tasks for issue template presence, PR template issue reference, linked-issue control-gate behavior, and PR issue linkage.

## Forbidden Scope Confirmation

- [x] No app source changes
- [x] No product behavior changes
- [x] No dependency changes
- [x] No package or lockfile changes
- [x] No npm install
- [x] No Expo, EAS, Android, iOS, native build, backend, or database commands
- [x] No backend/
- [x] No database/
- [x] No mobile/web product files
- [x] No auth/login/user account implementation
- [x] No payment implementation
- [x] No scoring, readiness, pass/fail, saved progress, or analytics implementation
- [x] No auto-merge activation
- [x] No branch-protection bypass
- [x] No merge
- [x] No Phase 4J-2 start
- [x] No Phase 4I resume
- [x] No `/init`
- [x] No `api_tool.list_resources`
- [x] No broad connector discovery
- [x] No tool-schema dump

## Claim Level

Source verified and local-script verified for Phase 4J-1 control files only after local validation passes.

This phase does not prove production readiness, public readiness, runtime behavior, build behavior, install behavior, release behavior, legal currentness, or content sufficiency.

## Known Limitations

The Phase 4J-1 GitHub issue must be created before opening the PR so the PR body can link a durable issue reference.

The linked-issue control gate verifies issue reference text in the PR body; it does not verify the issue contents through the GitHub API.

Workflow status is available only after the branch is pushed and the PR is opened.

## Next Phase Status

Phase 4J-2 is not started.

Phase 4I is not resumed.

Do not merge until GitHub Actions passes, red-team review is complete, required approval is present, and post-merge main verification is planned.
