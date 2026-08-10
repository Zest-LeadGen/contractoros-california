# ContractorOS California

Single-human, AI-operated development program for a California contractor exam-preparation product. The repository is public for transparency and auditability; product feature work is frozen until the owner-gated H10 decision, and current activity is the H0–H10 structural-hardening program (see `docs/project-control/`).

Current verified scope:

- Law & Business first.
- C10 deferred until a separate currentness/safety gate.
- Fixture data only.
- No backend, database, Firebase, Airtable API, auth, payments, scoring, readiness, pass/fail, Question Bank migration, or deployment.

## Apps

Two deliberate JavaScript scaffolds with pinned toolchains (Node version per `.nvmrc`, exact dependency pins, committed lockfiles — see `docs/TOOLCHAIN.md`):

- `apps/web/` — React + Vite web learner
- `apps/mobile/` — Expo mobile scaffold

Run locally (deterministic install from the committed lockfile):

```bash
cd apps/web
npm ci
npm run dev
```

Build:

```bash
cd apps/web
npm run build
```

## Package lock policy

Lockfiles ARE committed for both apps (`apps/web/package-lock.json`, `apps/mobile/package-lock.json`), generated from the clean public npm registry, digest-bound in CI, and installed with `npm ci`. (The earlier policy of not committing a lockfile was superseded by the H6 toolchain baseline, 2026-08-10.)

## Governance and contributing

- Security policy: [SECURITY.md](SECURITY.md) · Contributions: [CONTRIBUTING.md](CONTRIBUTING.md)
- Canonical constitution: `docs/project-control/PROGRAM_CONSTITUTION.md`
- Structural-hardening roadmap: GitHub issue #79 (H0–H10)
- Project state and records: `docs/project-control/` · phase evidence: `artifacts/`, `content/claims/`

## Important warning

The app scaffolds are internal development artifacts only: not public releases, not readiness eligible, pending legal review, fixture data only.
