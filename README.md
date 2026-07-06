# ContractorOS California

This repository begins with the Phase 3A local MVP app shell and project-control handoff artifacts.

Current verified scope:

- Law & Business first.
- C10 deferred until a separate currentness/safety gate.
- Fixture data only.
- No backend, database, Firebase, Airtable API, auth, payments, scoring, readiness, pass/fail, Question Bank migration, or deployment.

## App

The local React + Vite app shell is under:

`apps/web/`

Run locally:

```bash
cd apps/web
npm install
npm run dev
```

Build:

```bash
cd apps/web
npm run build
```

## Package lock policy

`apps/web/package-lock.json` is intentionally not committed at this checkpoint. During Phase 3B QA, `npm install` generated a lockfile containing sandbox/internal registry URLs, so it was not public-safe to commit. A future lockfile may be committed only if it is generated from a clean public npm registry install.

## Project control

Project state and handoff files are under:

- `docs/project-control/`
- `artifacts/phase-zips/`
- `artifacts/build-logs/`
- `content/claims/`

## Important warning

Phase 3A/3B is an internal development artifact only. It is not public, not readiness eligible, pending legal review, and uses fixture data only.
