# Phase 4J-3 — Mandatory Red-Team Marker Enforcement Report

## Phase

Phase 4J-3 — Mandatory Red-Team Marker Enforcement

## Lane

Control / Infrastructure

## Phase Issue

Phase issue: #20

Issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/20

## Linked Phase Issue

Phase issue: #20

The PR body must include this exact accepted reference:

```text
Phase issue: #20
```

## Starting Main SHA

```text
cfe01c7e381b3d2c0f26f0dba187d0a030368219
```

## Scope

This phase activates mandatory GitHub Actions enforcement for the SHA-bound `RED_TEAM_DECISION` marker created in Phase 4J-2.

This phase changes only allowed control files. It does not touch app/product/dependency/build/backend/mobile/web files, does not activate auto-merge, does not bypass branch protection, does not merge, does not start Phase 4J-4, and does not resume Phase 4I.

## Changed Files

```text
.github/workflows/control-gates.yml
.github/pull_request_template.md
AGENTS.md
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/RISK_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/DECISION_LOG.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/DEVELOPMENT_LEDGER.md
docs/project-control/ARTIFACT_INDEX.md
docs/project-control/phase_4j_3_mandatory_red_team_marker_enforcement_report.md
```

## Commands Run

```text
git branch --show-current
git rev-parse HEAD
git remote -v
gh --version
blocked command: gh auth status
git switch -c phase-4j-3-mandatory-red-team-marker-enforcement
python3 scripts/control/check_red_team_marker.py --self-test
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --check
git add .github scripts/control docs/project-control AGENTS.md
git commit -m "Activate mandatory red-team marker enforcement"
git push -u origin phase-4j-3-mandatory-red-team-marker-enforcement
gh pr create --base main --head phase-4j-3-mandatory-red-team-marker-enforcement --title "Phase 4J-3 mandatory red-team marker enforcement" --body-file docs/project-control/phase_4j_3_mandatory_red_team_marker_enforcement_report.md
gh pr view 21 --json url,state,headRefOid,mergeStateStatus,reviewDecision,statusCheckRollup
```

`gh auth status` was blocked by an invalid stored GitHub CLI token before local edits. Git push and `gh pr create` later succeeded. The first `gh pr view` attempt failed with an API connection error, then passed after approved network access.

## Dependency / Lockfile Handling

No dependencies were added or changed.

No package files were changed.

No package-lock file was created or committed.

No npm install was run.

## Workflow Enforcement Behavior

`.github/workflows/control-gates.yml` now runs `python3 scripts/control/check_red_team_marker.py` during `pull_request` control-gates runs.

Expected enforcement lifecycle:

- A PR opens without a plain-text `RED_TEAM_DECISION` marker and the mandatory marker step fails.
- Red-team reviews the exact current PR head SHA.
- The PR body is edited to include the plain-text marker for the exact current PR head SHA.
- The workflow reruns and can pass when all marker fields are valid and the marker SHA matches.
- If a later commit changes the PR head SHA, the prior marker is stale and the marker step fails again.

## PR Body Edit/Rerun Behavior

The workflow uses explicit `pull_request` event types:

```text
opened
reopened
synchronize
edited
```

The `edited` event is the minimum safe addition needed for PR body edits to rerun the marker check after red-team evidence is pasted into the PR body.

No `pull_request_target` trigger was added.

No elevated permissions were added.

## SHA-Binding Enforcement

The validator reads the GitHub pull request event payload through `GITHUB_EVENT_PATH`.

The validator compares the marker `PR head SHA` to the current pull request head SHA from the event payload. It also compares the marker PR number when the current PR number is available.

The validator ignores HTML comments and fenced code blocks, so examples in the PR template are not accepted as review evidence.

## Bootstrap Handling For Phase 4J-3 Itself

Phase 4J-3 uses the new mandatory marker process for its own PR.

The Phase 4J-3 PR is expected to fail the marker step until red-team reviews the exact current PR head SHA and adds the required plain-text marker to the PR body. This is not a bypass; it is the intended enforcement flow.

If this branch receives a new commit after red-team approval, the prior marker becomes stale and a fresh red-team marker is required.

## PR Template Impact

`.github/pull_request_template.md` now states that the `RED_TEAM_DECISION` marker must be pasted as plain text outside HTML comments and outside fenced code blocks.

The template states that the marker must match the current PR head SHA and that new commits after the marker require a fresh marker.

## PR Template / CODEOWNERS Implemented

`.github/pull_request_template.md` was updated to document mandatory plain-text marker placement.

CODEOWNERS was reviewed and not changed in this phase.

## Control-Gate Impact

The required ContractorOS control-gates workflow now includes a mandatory SHA-bound red-team marker step for pull requests.

Existing workflow checks were kept in place.

Pushes to `main` still run the existing control checks without requiring a PR body, because the red-team marker is PR evidence.

## Documentation Impact

Governance files updated:

```text
AGENTS.md
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/RISK_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/DECISION_LOG.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/DEVELOPMENT_LEDGER.md
docs/project-control/ARTIFACT_INDEX.md
```

## Risk Register Impact

`docs/project-control/RISK_REGISTER.md` updates the stale red-team approval risk to reflect Phase 4J-3 pull request workflow enforcement.

## Design Decision Impact

`docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md` adds CDR-4J-022 — Red-team marker enforcement is mandatory in protected control gates.

## Decision Log Impact

`docs/project-control/DECISION_LOG.md` records mandatory pull request workflow enforcement and PR body edit rerun behavior.

## Artifact Index Impact

`docs/project-control/ARTIFACT_INDEX.md` records that Phase 4J-3 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.

## Requirements Traceability Impact

`docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md` records Phase 4J-3 requirements for mandatory marker enforcement, PR body edit reruns, stale marker behavior, plain-text marker placement, and forbidden-scope exclusion.

## Validation Task Impact

`docs/project-control/VALIDATION_TASKS.md` records Phase 4J-3 local validation tasks and post-PR GitHub Actions evidence tasks.

## Workflow Validation

Local workflow validation is limited to static review and the local control scripts listed in this report.

GitHub Actions has run on PR #21 and is expected to fail until red-team adds a valid plain-text `RED_TEAM_DECISION` marker for the current PR head SHA and the workflow reruns.

## Validation Evidence

Local validation commands for this phase:

```text
PASS: python3 scripts/control/check_red_team_marker.py --self-test
PASS: python3 scripts/control/check_changed_files.py
PASS: python3 scripts/control/check_forbidden_scope.py
PASS: python3 scripts/control/check_required_control_updates.py
PASS: python3 scripts/control/check_pr_contract.py
PASS: python3 scripts/control/check_forbidden_scope.py --lockfiles-only
PASS: python3 scripts/control/check_pr_contract.py --claims-only
PASS: git diff --check
```

Reviewed control records with no update required:

```text
docs/project-control/DECISION_LOG.md: reviewed, no update required
docs/project-control/RISK_REGISTER.md: reviewed, no update required
scripts/control/check_red_team_marker.py: reviewed, no update required
```

## Security Hardening

No `pull_request_target` trigger was added.

No workflow permission expansion was added.

No secrets, deployment, package install, Expo, EAS, native build, third-party action, auto-merge, approval bypass, or branch-protection bypass was added.

## Red-Team Status

Red-team review is required before merge and has not yet occurred.

Phase 4J-3 does not self-review and does not approve its own PR.

## Human Approval Status

Human/write-access approval is required before merge and has not yet occurred.

## Auto-Merge Status

Auto-merge is not active and is not authorized by Phase 4J-3.

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
- [x] No Phase 4J-4 start
- [x] No Phase 4I resume
- [x] No `/init`
- [x] No `api_tool.list_resources`
- [x] No broad connector discovery
- [x] No tool-schema dump

## Claim Level

Source verified and local-script verified for Phase 4J-3 control files only after local validation passes.

This phase does not prove production readiness, public readiness, runtime behavior, build behavior, install behavior, release behavior, legal currentness, or content sufficiency.

## Known Limitations

The validator checks marker structure, decision, PR number when available, review date format, exact SHA-bound statement, and current PR head SHA match. It does not verify reviewer identity through the GitHub API.

Initial workflow status after PR creation: queued on PR #21 before the publish-evidence correction commit.

The PR body was updated to the corrected report before red-team marker review.

## Next Phase Status

Phase 4J-4 is not started.

Phase 4I is not resumed.

Do not merge until GitHub Actions passes, red-team review is recorded for the exact current PR head SHA, required human/write-access approval is present, and post-merge main verification is planned.
