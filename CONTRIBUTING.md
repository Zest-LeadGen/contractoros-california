# Contributing to ContractorOS California

## Program model — read this first

This repository is operated as a **single-human, AI-executed program**: one owner (@Zest-LeadGen) holds all merge and decision authority, and development is performed by governed AI executor sessions under a recorded authorization chain. It is public for transparency and auditability, not as an open-contribution project.

**External pull requests and code contributions are not accepted at this time.** There is no license or contributor agreement in place (see issue #71 for the open decision), so contribution ownership terms are undefined; any unsolicited PR will be closed without merge. If you want to propose something, open an issue describing it — the owner may then authorize scoped work through the program's own process.

Security reports are the exception: they are welcome and handled per [SECURITY.md](SECURITY.md).

## How changes actually land (the required route)

Every change follows this route, with no bypass:

```text
GitHub issue (scoped, owner-authorized) -> developer branch -> pull request ->
required status checks (control gates, product CI, CodeQL) ->
SHA-bound red-team review -> code-owner review -> owner-only merge
```

- Each PR is bound to a phase authorization record (`docs/project-control/authorizations/`) that enumerates the exact paths it may touch; the `phase-authorization` check denies anything outside that allowlist, default-deny.
- Required checks must be green; the aggregate `contractoros-control-gates` context and both product CI contexts are enforced by ruleset on `main`.
- Review approvals are bound to the exact PR head SHA; new commits invalidate prior review.

## Secure development requirements

These apply to all authorized work, human or AI:

1. **No secrets anywhere** — not in code, config, issues, PR bodies, commit messages, workflow logs, or evidence files. If a credential is exposed, follow `docs/project-control/INCIDENT_RESPONSE_AND_VULNERABILITY_TRIAGE_POLICY.md` immediately.
2. **Dependencies are exact-pinned** with committed lockfiles; installs use `npm ci`; lockfile changes require the dependency lane and owner approval. Do not add, upgrade, or remove a dependency outside an authorized dependency-lane PR.
3. **Workflow changes are control-surface changes**: no new GitHub Actions workflow or workflow edit outside an authorized phase; never introduce `pull_request_target` without a recorded threat review; keep top-level `permissions` minimal.
4. **Evidence integrity**: claims in reports must be grounded in live reads with captured timestamps; missing evidence is recorded NOT_PROVEN, never assumed.
5. **Tests must pass**: lint and unit/coverage layers run in both product CI contexts and are required; changes that touch tested surfaces must keep them green and extend them where scope demands.
6. **Scope discipline**: touch only the paths your authorization enumerates; product/app/dependency/build/backend/content scope requires a phase that names those files.

## Questions

Open an issue. The owner triages everything through the program's recorded process.
