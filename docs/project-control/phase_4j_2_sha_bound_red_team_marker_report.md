# Phase 4J-2 — SHA-Bound Red-Team Decision Marker Report

## Phase

Phase 4J-2 — SHA-Bound Red-Team Decision Marker

## Lane

Control / Infrastructure

## Phase Issue

Phase issue: #18

Issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/18

## Starting Main SHA

```text
a3d8e88f11200b01b0f1ef54960d1a39938b78db
```

## Scope

This phase defines a machine-checkable red-team decision marker and adds local validation support for matching a red-team decision to the exact PR head SHA reviewed.

This phase does not touch app/product/dependency/build/backend/mobile/web files, does not activate auto-merge, does not bypass branch protection, does not merge, does not start Phase 4J-3, and does not resume Phase 4I.

## Linked Phase Issue

Phase issue: #18

The PR body must include this exact accepted reference:

```text
Phase issue: #18
```

## Changed Files

```text
.github/pull_request_template.md
scripts/control/check_red_team_marker.py
AGENTS.md
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/RISK_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/DEVELOPMENT_LEDGER.md
docs/project-control/DECISION_LOG.md
docs/project-control/phase_4j_2_sha_bound_red_team_marker_report.md
```

## Commands Run

```text
git switch -c phase-4j-2-sha-bound-red-team-marker
python3 scripts/control/check_red_team_marker.py --self-test
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --check
git add .github scripts/control docs/project-control AGENTS.md
git commit -m "Add Phase 4J-2 SHA-bound red-team marker controls"
git push -u origin phase-4j-2-sha-bound-red-team-marker
gh pr create --base main --head phase-4j-2-sha-bound-red-team-marker --title "Phase 4J-2 SHA-bound red-team decision marker" --body-file docs/project-control/phase_4j_2_sha_bound_red_team_marker_report.md
```

## Dependency / Lockfile Handling

No dependencies were added or changed.

No package files were changed.

No package-lock file was created or committed.

No npm install was run.

## Red-Team Marker Format

Accepted marker:

```text
RED_TEAM_DECISION
PR number: #123
PR head SHA: 0123456789abcdef0123456789abcdef01234567
Decision: APPROVED
Reviewer role: Red-team reviewer
Review date: YYYY-MM-DD
Scope reviewed: Phase scope and changed files reviewed.
Conditions: None.
Forbidden-scope confirmation: Confirmed no forbidden scope in reviewed diff.
SHA-bound statement: This decision applies only to the listed PR head SHA.
```

Accepted decisions are `APPROVED`, `CHANGES_REQUESTED`, and `BLOCKED`.

## SHA-Binding Rule

The `PR head SHA` field must match the current PR head SHA.

A red-team approval is valid only for the exact SHA listed in the marker. Any later commit changes the PR head SHA and requires a fresh red-team decision.

## Enforcement Behavior

`scripts/control/check_red_team_marker.py` supports PR-body or report validation. It reads GitHub pull request event text when available, falls back to `PR_BODY`, and also reads changed phase reports in local/report contexts.

The validator ignores HTML comments and fenced code examples so template/report examples are not treated as real red-team decisions. The actual marker must be plain text.

Minimum behavior:

- If no marker exists, the script reports that the red-team marker is missing.
- If a marker exists but the PR head SHA does not match, the script fails.
- If the marker decision is `CHANGES_REQUESTED` or `BLOCKED`, the script fails.
- If the marker decision is `APPROVED` and the SHA matches, the red-team marker check passes.

## Bootstrap Limitation

Phase 4J-2 creates the marker format and validator, but mandatory workflow enforcement is documented as a future activation step.

The limitation exists because this phase cannot require a SHA-bound red-team marker before the marker format and validator are reviewed and merged. Phase 4J-3 or a later approved control phase may activate mandatory workflow enforcement after bootstrap review.

## PR Template Impact

`.github/pull_request_template.md` now includes a red-team decision evidence section with the exact marker format and a warning that the marker SHA must match the current PR head SHA.

## PR Template / CODEOWNERS Implemented

`.github/pull_request_template.md` was updated to include SHA-bound red-team decision evidence.

CODEOWNERS was reviewed and not changed in this phase.

## Control-Gate Impact

This phase adds `scripts/control/check_red_team_marker.py`.

The existing mandatory workflow gates are not weakened or removed.

Mandatory red-team marker enforcement is not active in this phase and is recorded as a bootstrap/future activation step.

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
docs/project-control/DECISION_LOG.md
```

## Validation Evidence

Local validation commands for this phase:

```text
python3 scripts/control/check_red_team_marker.py --self-test
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
docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required
```

## Risk Register Impact

`docs/project-control/RISK_REGISTER.md` records the stale red-team approval risk after new PR commits.

## Decision Log Impact

`docs/project-control/DECISION_LOG.md` records SHA-bound red-team approval and future activation status.

## Design Decision Impact

`docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md` adds CDR-4J-021 — Red-team decisions must be bound to exact PR head SHA.

## Artifact Index Impact

`docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required`

Phase 4J-2 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.

## Requirements Traceability Impact

`docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md` records Phase 4J-2 SHA-bound red-team marker requirements.

## Validation Task Impact

`docs/project-control/VALIDATION_TASKS.md` records Phase 4J-2 validation tasks for the marker validator, existing local control checks, whitespace validation, and bootstrap status.

## Workflow Validation

No workflow file was changed in this phase.

GitHub Actions workflow validation is pending until the branch is pushed and the PR is opened with `Phase issue: #18`.

## Security Hardening

No workflow permission expansion was made.

No `pull_request_target` trigger was added.

No secrets, deployment, package install, Expo, EAS, native build, third-party action, auto-merge, approval bypass, or branch-protection bypass was added.

## Red-Team Status

Red-team review is required before merge and has not yet occurred.

Phase 4J-2 does not self-review and does not approve its own PR.

## Human Approval Status

Human/write-access approval is required before merge and has not yet occurred.

## Auto-Merge Status

Auto-merge is not active and is not authorized by Phase 4J-2.

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
- [x] No Phase 4J-3 start
- [x] No Phase 4I resume
- [x] No `/init`
- [x] No `api_tool.list_resources`
- [x] No broad connector discovery
- [x] No tool-schema dump

## Claim Level

Source verified and local-script verified for Phase 4J-2 control files only after local validation passes.

This phase does not prove production readiness, public readiness, runtime behavior, build behavior, install behavior, release behavior, legal currentness, or content sufficiency.

## Known Limitations

Mandatory red-team marker enforcement is not active in the workflow during Phase 4J-2.

The validator checks marker structure, decision, PR number when available, review date format, exact SHA-bound statement, and current PR head SHA match. It does not verify reviewer identity through the GitHub API.

Workflow status is available only after the branch is pushed and the PR is opened.

## Next Phase Status

Phase 4J-3 is not started.

Phase 4I is not resumed.

Do not merge until GitHub Actions passes, red-team review is complete, required approval is present, and post-merge main verification is planned.
