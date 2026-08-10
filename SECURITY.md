# Security Policy

## Supported Versions

ContractorOS California is pre-release. There are no packaged or distributed releases, and no deployed service exists (product work is frozen until the owner-gated H10 decision). Security fixes land on the `main` branch only.

| Version | Supported |
| --- | --- |
| `main` (latest) | Yes |
| Anything else | No |

## Reporting a Vulnerability

Please use **GitHub private vulnerability reporting**: on this repository, open the **Security** tab and choose **Report a vulnerability**. This keeps details private while the report is triaged.

If the private reporting form is not available to you, open a regular issue titled "security contact requested" **without any vulnerability details**, and the owner will arrange a private channel.

Please do not disclose vulnerability details in public issues, pull requests, discussions, or commit messages before a fix is merged and coordinated disclosure is agreed.

## Response Process

- Acknowledgement target: within 7 days of a private report.
- Triage, severity assessment, and disposition follow `docs/project-control/INCIDENT_RESPONSE_AND_VULNERABILITY_TRIAGE_POLICY.md`.
- Fixes are delivered through the repository's gated route: authorized scoped pull request, required status checks, code-owner review, and owner-only merge. No fix is merged silently.
- Findings that are accepted rather than fixed require an owner-approved, dated, expiring risk acceptance recorded in `docs/project-control/RISK_REGISTER.md`; silent suppression is not permitted.

## Disclosure Policy

Coordinated disclosure: details are published after a fix (or an owner-approved acceptance with mitigation guidance) is on `main`. Reporters are credited unless they prefer otherwise.

## Scope

In scope: this repository's source, control scripts, GitHub Actions workflows, dependency manifests and lockfiles, and repository configuration. Out of scope: third-party platforms themselves (GitHub, npm registry) except as this repository configures them.

## Security Contacts

- Repository owner: @Zest-LeadGen (GitHub)

## Current Baseline Disclosure

The repository's security baseline is documented honestly in `docs/project-control/evidence/H7A1_SECURITY_POSTURE_INVENTORY.md`, including gaps that are still open and settings whose state is recorded as NOT_PROVEN rather than assumed. This policy does not claim any control that the inventory does not prove.
