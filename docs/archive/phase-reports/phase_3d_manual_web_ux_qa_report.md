# Phase 3D — Manual Internal Web UX QA Report

## Scope

Phase 3D performed a manual internal web UX QA review of the current React/Vite fixture shell. This phase did not change app source, app behavior, product scope, dependencies, or runtime architecture.

## Branch

`phase-3d-manual-web-ux-qa`

## Repository state reviewed

- Phase 3A source import merged into `main`.
- Phase 3B QA/hygiene patch merged into `main`.
- Phase 3C reproducibility blocker report merged into `main`.
- Latest verified Phase 3C merge commit: `574c2026ca3e5d1972846018cd83bcaccbef9f76`.
- `apps/web/package-lock.json` remains absent from `main`.
- `apps/web/package.json` uses `latest` dependencies.
- Dependency-lock/public npm reproducibility remains open for a future clean external environment.

## Local run / inspection note

`npm install` and `npm run build` passed from `apps/web`. A Vite dev server also started locally and served the app HTML shell. Chromium/Playwright browser navigation to localhost and file URLs was blocked by the sandbox environment with `net::ERR_BLOCKED_BY_ADMINISTRATOR`; this was treated as an environment limitation, not an app failure. Because of that limitation, this UX QA used:

1. successful Vite build output;
2. successful local Vite server startup and HTML shell retrieval;
3. source-level walkthrough of React components and fixture data;
4. static verification of blocked routes, warning labels, source panels, issue-report mock, and governance dashboard logic.

No app source changes were made.

## Build evidence

Command run from `apps/web`:

```bash
npm install
npm run build
```

`npm install` output:

```text
added 19 packages, and audited 20 packages in 4s

8 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

`npm run build` output:

```text
> contractoros-phase-3a-local-mvp-app-shell@0.1.0 build
> vite build

vite v8.1.3 building client environment for production...
transforming...
✓ 29 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.44 kB │ gzip:  0.31 kB
dist/assets/index-90nBcqBQ.css    4.43 kB │ gzip:  1.61 kB
dist/assets/index-DukPz6SY.js   250.22 kB │ gzip: 69.98 kB

✓ built in 525ms
```

## Package-lock handling

`npm install` generated a local `package-lock.json`, but it contained internal/sandbox registry URLs such as `packages.applied-caas-gateway1.internal.api.openai.org`. The generated lockfile was not committed.

Internal/sandbox URL scan command:

```bash
grep -R "applied-caas\|internal.api.openai.org\|sandbox\|localhost\|127.0.0.1" -n package-lock.json || true
```

Result: internal/sandbox registry URLs were present in the generated local lockfile. Therefore `apps/web/package-lock.json` remains intentionally excluded.

## Forbidden implementation scan

Command:

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail" -n apps/web/src apps/web/package.json || true
```

Classification:

- `readiness`, `score`, and `pass/fail` hits in `BlockedRoute.jsx`, `Layout.jsx`, `QuestionPlayer.jsx`, and `App.jsx` are allowed warning/blocked-route text.
- `payment`, `downpayment`, `progress-payment`, `stop payment notice`, and `payment-bond` hits in `internalFixtureItems.js` and `claimEligibilityMatrix.js` are allowed Law & Business payment/downpayment claim text.
- No implementation was found for `fetch`, `XMLHttpRequest`, `localStorage`, `sessionStorage`, Firebase, Airtable runtime, Stripe, auth, payment processing, scoring, readiness calculation, or pass/fail logic.

## Manual UX QA results

| Area | Pass / Fail / Needs Patch | Evidence / Notes |
| --- | --- | --- |
| App startup | Pass with environment limitation | Build passed; Vite dev server started; HTML shell was served. Browser automation was blocked by sandbox admin policy, not by app code. |
| Law & Business fixture-only state | Pass | `TrackSelect.jsx` makes Law & Business the selectable internal fixture track. `Layout.jsx` states fixture data only, Law & Business first, and C10 deferred. |
| C10 deferred / blocked state | Pass | `TrackSelect.jsx` renders C10 Electrical as disabled/locked. `App.jsx` defines `c10Public` blocked route. No C10 public MCQ path found. |
| Question flow | Pass | `QuestionPlayer.jsx` renders fixture questions/choices, allows answer selection before submit, hides correct answer/explanation until submit, then shows item-level fixture feedback only. No score, readiness, pass/fail, or performance recommendation logic exists. |
| Source / claim panel | Pass | `SourcePanel.jsx` displays source/claim metadata and states the panel does not imply legal approval, public approval, CSLB affiliation, PSI affiliation, or Question Bank approval. |
| Issue report panel | Pass | `IssueReportPanel.jsx` is labeled mock/local in-memory only and says nothing is saved, synced, or submitted. |
| Claim governance dashboard | Pass | `ClaimGovernanceDashboard.jsx` states claims are internal source claims, not MCQs, not public content, and not Question Bank records. It shows risk/status counts and legal/currentness governance fields. |
| Blocked routes | Pass | `BlockedRoute.jsx` clearly lists blocked readiness scoring, pass/fail logic, public launch, C10 public content, backend/database, and Question Bank migration. |
| Forbidden implementation scan | Pass | Scan hits were allowed warning text or Law & Business payment/downpayment claim text only. No forbidden implementation was found. |
| Build | Pass | `npm install` completed with 0 vulnerabilities and `npm run build` completed successfully. Generated local lockfile was excluded because it contained internal/sandbox registry URLs. |

## Findings

### Critical blockers

- None found in the current app source/build for the internal fixture shell.

### High issues

- No high source/app blocker found.
- Environment limitation: sandbox browser automation could not load localhost/file URLs due Chromium admin policy. This limits visual click-through evidence in this phase, but the app build and source-level UX walkthrough were completed.

### Medium issues

- Dependency-lock/public npm reproducibility remains unresolved from Phase 3C. This is already documented and remains outside Phase 3D scope.

### Low issues

- Phase labels in some UI strings still say Phase 3A. This is acceptable for the internal fixture shell because the app source was not advanced beyond the Phase 3A shell; no source change was made.

### No-action observations

- Internal-only posture is visible in `InternalBanner`, `Layout`, question feedback, source panel, issue-report mock, claim governance, and blocked routes.
- C10 remains deferred and blocked.
- No backend/database/API/runtime service appears in source.
- No public-use or readiness eligibility claim was found in the reviewed app source.

## Files changed in Phase 3D

- `docs/project-control/phase_3d_manual_web_ux_qa_report.md`

No app source file was changed.

## Explicit exclusions

- No Phase 4 work.
- No mobile app work.
- No Expo.
- No React Native.
- No Capacitor.
- No backend.
- No database.
- No Firebase.
- No Airtable API runtime.
- No deployment.
- No auth.
- No payments.
- No subscriptions.
- No scoring.
- No readiness logic.
- No pass/fail logic.
- No public launch pages.
- No marketing pages.
- No app-store materials.
- No new MCQs.
- No public MCQs.
- No Question Bank migration.
- No C10 public content.
- No ZIP binaries committed to GitHub.
- No dependency-lock changes.
- No `apps/web/package-lock.json` committed.

## Phase 3D result

Phase 3D produced a report-only QA PR. The internal React/Vite fixture shell passed build and source-level manual UX QA within the sandbox limitations. No app source changes were made and no product scope was expanded.
