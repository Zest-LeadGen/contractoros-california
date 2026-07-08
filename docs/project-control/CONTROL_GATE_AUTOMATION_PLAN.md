# Control Gate Automation Plan

## Purpose

Describe the lightweight GitHub Actions control-gate system introduced in Phase 4G.

## Workflow Design

Workflow: `.github/workflows/control-gates.yml`

Workflow name: `ContractorOS Control Gates`

Required status check name: `contractoros-control-gates`

The workflow runs on pull requests and pushes to `main`.

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

## Security Hardening

The workflow uses read-only permissions:

```text
contents: read
pull-requests: read
```

It does not use `pull_request_target`, secrets, deployment, npm install, Expo, EAS, build commands, Google Drive, or third-party actions except `actions/checkout`.

`actions/checkout@v4` is the only action dependency. Pinning to a full SHA is preferred later; Phase 4G uses a stable version and documents this limitation.

## Branch Protection Setup After Workflow Lands

After Phase 4G is merged and the workflow has run at least once, repository owner must configure GitHub branch protection or rulesets so the contractoros-control-gates check is required before merge.

## Known Limitations

Branch protection required-check enforcement cannot be completed solely by adding files to the repository. Owner/admin UI configuration is required after the workflow exists and has run.

The static checks are lightweight and do not replace human red-team review.

The YAML matrix parser intentionally supports a small subset to avoid external dependencies.

The workflow syntax is source-inspected in Phase 4G. Full enforcement is proven only after the workflow runs in GitHub.

## Future Hardening

Future phases may add SHA-pinned checkout, stricter lane allowlists, stronger PR parsing, branch protection evidence, artifact retention, and CODEOWNERS review enforcement.

## Source of Truth

GitHub remains source of truth for code, control text, PR metadata, workflow evidence, and status checks.

Google Drive is archive/reference only and is not used by this workflow.
