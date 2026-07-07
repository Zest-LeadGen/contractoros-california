# Phase 3C — Clean Reproducibility + Dependency Lock Strategy

## Scope

Phase 3C investigated dependency reproducibility and lockfile strategy without adding product features.

## Branch

`phase-3c-reproducibility-lock-strategy`

## Repository checkout note

A direct `git clone https://github.com/Zest-LeadGen/contractoros-california.git` attempt from the sandbox failed because the sandbox could not resolve `github.com`. The GitHub branch was created from current `main` using the GitHub connector. Local command/build verification was run from a reconstructed working tree using the verified Phase 3A app source available in the sandbox.

## Commands run

From repository root:

```bash
git status
git branch --show-current
find . -maxdepth 3 -type f | sort | sed -n '1,160p'
```

From `apps/web`:

```bash
npm config get registry
npm install
npm run build
```

Lockfile scan:

```bash
grep -R "applied-caas\|internal.api.openai.org\|sandbox\|localhost\|127.0.0.1" -n package-lock.json || true
```

Forbidden implementation scan:

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail" -n apps/web/src apps/web/package.json || true
```

## Dependency decision

Dependency pinning was not performed.

The previous attempt to replace `latest` with exact versions was reverted because public npm registry verification could not be completed in the sandbox. The only exact versions observed during the install/build check came from a lockfile generated through an internal/sandbox registry path, so those versions cannot be treated as public-safe or reproducible evidence.

`apps/web/package.json` therefore remains at the previous dependency state:

```json
"dependencies": {
  "@vitejs/plugin-react": "latest",
  "vite": "latest",
  "react": "latest",
  "react-dom": "latest"
}
```

## Package-lock decision

Package-lock not committed because public-safe generation failed.

Reason:

- `npm config get registry` returned an environment error: `The registry option is protected, and can not be retrieved in this way`.
- Default `npm install` generated `package-lock.json`, but the generated lockfile contained internal registry URLs such as `packages.applied-caas-gateway1.internal.api.openai.org`.
- An explicit `npm install --registry=https://registry.npmjs.org/` attempt timed out in the sandbox.

Therefore, committing the lockfile would violate the Phase 3C rule against internal/sandbox registry URLs.

## Open dependency-lock blocker

The dependency-lock issue remains open for a future clean external environment where all of the following can be proven:

1. install uses the public npm registry;
2. resolved package versions are available from public npm;
3. generated `apps/web/package-lock.json` contains no internal, sandbox, localhost, or private registry URLs;
4. build passes from the public-safe lockfile.

## Build result

`npm install` completed with 0 vulnerabilities.

`npm run build` passed with Vite and transformed 29 modules.

## Forbidden implementation scan classification

Scan hits were classified as allowed text/data only:

- `payment`, `downpayment`, and `progress-payment`: allowed Law & Business claim text.
- `readiness`, `score`, and `pass/fail`: allowed warning/blocked-route text.
- `auth`, `backend`, and `payments`: allowed warning/exclusion text.

No actual implementation was found for fetch, XMLHttpRequest, localStorage, sessionStorage, Firebase, Airtable, Stripe, auth, payment processing, scoring, readiness, or pass/fail logic.

## Files changed in Phase 3C

- `docs/project-control/phase_3c_reproducibility_lock_strategy_report.md`

`apps/web/package.json` was inspected and temporarily tested, but final branch content was restored to the prior `latest` dependency state.

## Explicit exclusions

- No app feature changes.
- No learner-flow changes.
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
- No internal/sandbox registry URLs committed.

## Phase 3C result

Phase 3C documents the reproducibility blocker. No dependency pins and no lockfile were committed because public npm registry verification could not be completed. No product scope was expanded.
