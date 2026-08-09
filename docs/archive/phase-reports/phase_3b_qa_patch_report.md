# Phase 3B — Repository-Controlled App QA + Fix Patch

## Scope

Phase 3B performed a controlled QA/fix pass on the Phase 3A React/Vite app shell source now stored in GitHub.

This phase did not expand product scope.

## Branch

`phase-3b-qa-fix-patch`

## Build commands run

```bash
cd apps/web
npm install
npm run build
```

## Build result

`npm install` completed successfully and reported 0 vulnerabilities.

`npm run build` completed successfully with Vite.

## Package-lock decision

`npm install` generated a local `package-lock.json`, but the generated lockfile contained sandbox/internal registry URLs such as:

`packages.applied-caas-gateway1.internal.api.openai.org`

Because that lockfile was not public-safe, it was not committed to GitHub.

## Forbidden implementation scan

Command run:

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail" -n apps/web/src apps/web/package.json || true
```

Findings were warning text, fixture content, and claim text only. No runtime implementation of backend, fetch, XMLHttpRequest, localStorage, sessionStorage, Firebase, Airtable, Stripe, auth, payment, scoring, readiness, or pass/fail logic was added.

## QA fixes applied

1. `.gitignore` now ignores `dist/` in addition to `dist/.vite/`.
2. Root `README.md` now documents why `apps/web/package-lock.json` is intentionally absent at this checkpoint.
3. This QA report was added under `docs/project-control/`.

## QA findings left unchanged

- The app remains fixture-only.
- The learner flow remains internal-only.
- The claim governance dashboard remains local fixture-only.
- C10 remains deferred.
- Blocked routes remain informational only.
- No persistence, API, backend, database, scoring, readiness, or pass/fail logic exists.

## Explicit exclusions

- No backend.
- No database.
- No Firebase.
- No Airtable API.
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

## Phase 3B result

Build passed. Forbidden implementation scan produced no prohibited implementation hits. Patch is limited to repository hygiene, README accuracy, and QA reporting.
