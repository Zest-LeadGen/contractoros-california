# Control Gate Automation Plan

## Purpose

Describe the lightweight GitHub Actions control-gate system introduced in Phase 4G and the maintained workflow route for controlled ContractorOS development.

## Workflow Design

Workflow: `.github/workflows/control-gates.yml`

Workflow name: `ContractorOS Control Gates`

Required status check name: `contractoros-control-gates`

The workflow runs on pull requests and pushes to `main`.

## Maintained Route

The maintained route is:

```text
GitHub Issue → Developer PR → Control Gates → Red-Team Decision → Human Approval → Merge
```

The objective is to reduce owner copy/paste and manual supervision while preserving:

- protected PR governance;
- red-team accountability;
- evidence-bearing reports;
- explicit human approval for major decisions;
- branch protection;
- no direct-to-main development;
- no automated approval;
- no automated merge.

## Scripts

The workflow runs standard-library Python scripts only:

```text
scripts/control/check_changed_files.py
scripts/control/check_forbidden_scope.py
scripts/control/check_required_control_updates.py
scripts/control/check_pr_contract.py
```

## Gates

1. Changed-file allowlist / lane check.
2. Forbidden-scope check.
3. Required control-file update check.
4. PR body/template completeness check.
5. Lockfile / dependency contamination check.
6. Claim-language check.

## Companion Phase Report Handling

A Product / QA PR may include exactly one current phase report at `docs/project-control/phase_*_report.md`.

That report is documentation for the Product / QA PR and does not change the declared PR lane to Control / Infrastructure.

The report must still satisfy current required sections and exact no-update-required markers.

Report-only project-control PRs remain Control / Infrastructure.

Non-report project-control changes remain Control / Infrastructure.

## Security Hardening

The workflow uses read-only permissions:

```text
contents: read
pull-requests: read
```

It does not use `pull_request_target`, secrets, deployment, npm install, Expo, EAS, build commands, Google Drive, or third-party actions except `actions/checkout`.

`actions/checkout@v4` is the only action dependency. Pinning to a full SHA is preferred later; current control text documents this limitation.

## Branch Protection Setup

Repository owner/admin must configure GitHub branch protection or rulesets so the contractoros-control-gates check is required before merge.

Approval and CODEOWNERS requirements must remain GitHub-enforced, not script-invented.

## Known Limitations

Branch protection required-check enforcement cannot be finished solely by adding files to the repository. Owner/admin UI configuration is required after the workflow exists and has run.

The static checks are lightweight and do not replace human red-team review.

The YAML matrix parser intentionally supports a small subset to avoid external dependencies.

The workflow cannot prove production, public, build, install, legal/currentness, or content readiness by itself.

## Future Hardening

Future phases may add SHA-pinned checkout, stricter lane allowlists, stronger PR parsing, branch protection evidence, artifact retention, and CODEOWNERS review enforcement.

## Source of Truth

GitHub remains source of truth for code, control text, PR metadata, workflow evidence, and status checks.

Google Drive is archive/reference only and is not used by this workflow.
