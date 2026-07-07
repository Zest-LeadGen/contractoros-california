# ContractorOS Risk Register

Purpose: track active risks until evidence proves they are resolved.

Template:

```text
Risk:
Status:
Evidence:
Owner:
Resolution condition:
Last reviewed:
```

## Active Risks

Existing active risks remain in prior versions of this register and project-control reports, including latest dependencies, lockfile provenance, local contaminated lockfiles, npm vulnerabilities, visual/device QA, APK/build/install gaps, CI automation, content system gaps, release-gate gaps, and public/production overclaim risk.

### red-team files are visible in the same repo and could be misread as developer scope

```text
Risk: red-team files are visible in the same repo and could be misread as developer scope.
Status: Active / Controlled
Evidence: Red-team files are committed for auditability in GitHub.
Owner: ContractorOS development lead / red-team gate
Resolution condition: ROLE_BOUNDARIES.md and red-team README clearly mark them as reviewer/control files; developer must not treat them as implementation scope.
Last reviewed: 2026-07-07
```
