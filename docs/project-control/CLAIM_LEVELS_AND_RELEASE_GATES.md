# Claim Levels and Release Gates

Permanent claim and release control for ContractorOS California.

## Claim Levels

- Level 0 — Not verified
- Level 1 — Source verified
- Level 2 — Command verified
- Level 3 — Runtime visually verified
- Level 4 — Build artifact verified
- Level 5 — Install/distribution verified

## Forbidden Overclaims Unless Evidence Supports Them

- ready
- complete
- production-ready
- public-ready
- MVP-ready
- Android-ready
- APK-ready
- app-store-ready
- launch-ready
- fully tested

## Release Gates

- Internal scaffold gate: requires source and report evidence.
- Runtime smoke gate: requires command output evidence.
- Visual QA gate: requires observed UI evidence.
- Dependency-control gate: requires dependency and lockfile evidence.
- Build artifact gate: requires artifact evidence.
- Install test gate: requires installation evidence.
- Public/production gate: requires all prior gates plus owner approval.

## Claim Rule

Use the lowest claim level supported by evidence. Tests prove only what they directly test.
