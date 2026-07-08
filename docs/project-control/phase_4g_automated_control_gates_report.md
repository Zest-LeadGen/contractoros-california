# Phase 4G — Automated Control Gates and Documentation Maintenance Protocol Report

## 1. Scope

Phase 4G is a Control / Infrastructure phase only.

It adds lightweight automated control-gate infrastructure, static Python scripts, a machine-readable control-file update matrix, human-readable documentation maintenance protocol, control-gate automation plan, PR template, CODEOWNERS file, and this report.

This is not a product feature phase. This is not a mobile UX phase. This is not a backend, dependency, build, APK, EAS, deployment, content, scoring, or release phase.

## 2. Starting Repository State

Phase 4F verified main / merge commit:

```text
96d1146f35f23e0e6c12302bdd857ab02ba0abe2
```

## 3. Files Added

Exactly these files were added:

```text
.github/workflows/control-gates.yml
.github/CODEOWNERS
.github/pull_request_template.md
scripts/control/check_changed_files.py
scripts/control/check_required_control_updates.py
scripts/control/check_forbidden_scope.py
scripts/control/check_pr_contract.py
docs/project-control/CONTROL_FILE_UPDATE_MATRIX.md
docs/project-control/control-file-update-matrix.yml
docs/project-control/DOCUMENTATION_MAINTENANCE_PROTOCOL.md
docs/project-control/CONTROL_GATE_AUTOMATION_PLAN.md
docs/project-control/phase_4g_automated_control_gates_report.md
```

## 4. Automation Implemented

The GitHub Actions workflow `ContractorOS Control Gates` implements the `contractoros-control-gates` job on pull requests and pushes to `main`.

## 5. Control Gates Implemented

1. Changed-file allowlist / lane check.
2. Forbidden-scope check.
3. Required control-file update check.
4. PR body/template completeness check.
5. Lockfile / dependency contamination check.
6. Claim-language check.

The gates fail closed when their scripts detect violations.

## 6. Matrix Rules Implemented

The machine-readable matrix covers apps/mobile, apps/web, docs/project-control, package files, mobile package files, GitHub workflow/control files, CODEOWNERS, PR template, Android, iOS, EAS, backend, and database categories.

Each category defines lane, required phase report, required control updates, required report sections, blocked-without-approval behavior, and forbidden claims.

## 7. PR Template / CODEOWNERS Implemented

The PR template requires phase, lane, scope, starting main SHA, changed files, commands, dependency/lockfile handling, documentation impact, risk/decision/artifact impacts, forbidden scope, claim level, known limitations, and next phase status.

CODEOWNERS assigns project-control, GitHub config, control scripts, app paths, package files, EAS, Android, and iOS paths to `@Zest-LeadGen`.

## 8. Commands Run

Initial commands:

```bash
python3 --version
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
```

Targeted red-team patch validation commands rerun:

```bash
python3 --version
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
```

Final meaningful outputs:

```text
Python 3.13.5
check_changed_files.py: PASS — changed-file allowlist / lane check completed.
check_forbidden_scope.py: PASS — no forbidden implementation-looking hits found; package-lock.json, apps/mobile/package-lock.json, and apps/web/package-lock.json absent.
check_required_control_updates.py: PASS — required control update check completed against current PR/report only.
check_pr_contract.py: PASS — PR/report contract check completed.
check_forbidden_scope.py --lockfiles-only: PASS — lockfile contamination check completed; all checked lockfiles absent.
check_pr_contract.py --claims-only: PASS — claim-language check completed.
```

Validation context: local rerun used the live PR body and `GITHUB_BASE_REF=main` to mirror pull-request event context for changed-file detection.

## 9. Workflow Validation

Workflow validation was source-inspected and locally supported by executing the same static Python scripts that the workflow invokes.

The workflow itself was not executed in GitHub before the PR was opened. Full workflow enforcement is not proven until the workflow exists on GitHub and runs on a pull request or push.

## 10. Security Hardening

Confirmed: no `pull_request_target`, no secrets, read-only permissions, no deployment, no npm install, no Expo, no EAS, no build commands, no Google Drive, and no third-party actions except `actions/checkout`.

`actions/checkout@v4` is the only action dependency. Pinning to a full SHA is preferred later; Phase 4G documents this limitation.

## 11. Explicit Exclusions

Confirmed not added or changed: app source, mobile source, web source, package files, lockfiles, EAS, Android, iOS, backend, database, Firebase, Airtable runtime, deployment, auth/login/user accounts, payments/subscriptions, scoring/readiness/pass-fail, saved progress/analytics, public MCQs, Question Bank migration, C10 public content, APK/AAB/iOS build, ZIP binaries, or Google Drive artifacts.

## 12. Known Limitations

Branch protection required-check enforcement cannot be completed solely by adding files to the repository. Owner/admin UI configuration is required after the workflow exists and has run.

The scripts are lightweight static checks and do not replace red-team review.

The matrix parser intentionally supports a conservative YAML subset without PyYAML.

The workflow syntax was source-inspected, not executed in GitHub before PR open.

## 13. Required Owner Action

After Phase 4G is merged and the workflow has run at least once, repository owner must configure GitHub branch protection or rulesets so the contractoros-control-gates check is required before merge.

## 14. Phase Result

Phase 4G remains in red-team patch state as a Control / Infrastructure PR. It is not merged.

Claim level: source verified and local static-command verified only. GitHub Actions execution is separately verified only if a workflow run appears for the patched head SHA.

## 15. Next Phase Status

Phase 4H was not started. PR must be reviewed before merge. No next phase may begin until PR is merged and `main` is verified.

## Patch Note — Red-Team Targeted Corrections

Red-team found three issues before merge:

- weakened lane-signal issue in `scripts/control/check_changed_files.py`;
- stale-report issue in `scripts/control/check_required_control_updates.py`;
- PR-contract section mismatch in `scripts/control/check_pr_contract.py`.

Exact files patched:

```text
scripts/control/check_changed_files.py
scripts/control/check_required_control_updates.py
scripts/control/check_pr_contract.py
docs/project-control/phase_4g_automated_control_gates_report.md
```

Patch results:

- `check_changed_files.py` no longer treats standard checklist text such as explicit exclusions or forbidden-scope confirmation as approval for dangerous paths.
- `check_changed_files.py` requires exact lane plus explicit owner approval or the approved-lane phrase for dependency, build/distribution, and backend dangerous paths.
- `check_changed_files.py` fails closed for package lockfiles, `eas.json`, Android, iOS, backend, and database dangerous paths unless precise lane approval is present.
- `check_required_control_updates.py` validates only the current PR body and the changed current phase report.
- `check_required_control_updates.py` detects the current phase report from the changed-file list and requires exactly one current phase report when the matrix requires a report.
- `check_required_control_updates.py` enforces lane compatibility, blocked-without-approval rules, required report sections, and exact reviewed/no-update-required declarations.
- `check_required_control_updates.py` now requires exact reviewed/no-update-required markers inside the current phase report itself; old phase reports and PR-body-only markers do not satisfy missing control-file updates.
- `check_required_control_updates.py` and `check_pr_contract.py` now derive changed files from the PR/base diff when `GITHUB_BASE_REF` is available, rather than relying only on a dirty working tree.
- `check_pr_contract.py` enforces the full PR template contract section list and requires claim-level wording for app, control, workflow, script, build, dependency, backend, and database changes.

## Documentation Impact

docs/project-control/DEVELOPMENT_LEDGER.md: reviewed, no update required
docs/project-control/RISK_REGISTER.md: reviewed, no update required
docs/project-control/DECISION_LOG.md: reviewed, no update required
docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required

## Decision Log Impact

docs/project-control/DECISION_LOG.md: reviewed, no update required

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required
