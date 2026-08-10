# H6-B.2 Test-Layer Evidence — 2026-08-10

Recorded independently from product-readiness claims (issue #64 item 9). Local host: macOS, node v26.5.0 / npm 12.0.1 (resolution + proof host); consumption pinned to the Node 22 line via .nvmrc/engines. Authorized by PA-0017 (owner comment 5235003178); design decisions pre-recorded in DECISION_LOG before delivery.

## Dependency additions (lint layer only — unit/coverage layers add ZERO packages)

Exactly three exact-pinned devDependencies per app, resolved live at selection time: eslint 10.8.1 (dist-tag latest), @eslint/js 10.0.1, globals 17.9.0. eslint engines `^20.19.0 || ^22.13.0 || >=24` verified compatible with the .nvmrc pin v22.23.2. `jiti` peer is unused (no TypeScript config) and npm resolved cleanly without it.

## Determinism proofs

- Byte-identical lockfile re-resolution: `npm install --package-lock-only` from each final manifest in two independent fresh directories — byte-identical both apps (sha256 equality asserted programmatically before staging).
- Clean install from the committed lockfiles: web "added 91 packages" exit 0; mobile "added 520 packages" exit 0.
- Registry provenance and contamination: web 114 resolved URLs, mobile 530 — 100% https://registry.npmjs.org/ both; zero hits for the contamination token set, both.

## Lockfile digests (sha256)

```text
apps/web/package-lock.json     ac295ea22117d2cd9530badda4b74795fe4203b8c4abf19ca2efabbf96be7f46
apps/mobile/package-lock.json  92dd08d3c45e6bf7f6e98b6aa67cf29a7ed9ca657957ae9001093966b7d17069
```

## Layer proofs (all run locally against the committed trees)

- LINT: `npm run lint` exit 0 both apps (eslint recommended + JSX parse; PascalCase exemption documented in each config — core ESLint cannot see JSX usage without the React plugin, which is a tracked enhancement).
- UNIT: web 6/6 pass (claim-matrix uniqueness/official-source/risk-enum/non-public invariants; fixture-item choice/answer/source invariants); mobile 3/3 pass (track-id uniqueness; C10-blocked invariant; internal-question shape). Runner: node:test — zero test dependencies.
- COVERAGE: `node --test --experimental-test-coverage` reports 100% lines/branches/functions on the imported data modules, both apps. HONEST SCOPE: under the node runner, coverage measures only imported modules — the JSX component layer is NOT imported and therefore not measured (0%, untested); component/DOM tooling is a tracked enhancement, not a silent omission. No inflated repo-wide percentage is claimed.
- TYPE CHECKING: N/A-by-design — both apps are deliberate JavaScript scaffolds (recorded decision; a TS adoption would be its own authorized change).
- Mobile `"type": "module"` addition proven safe before delivery: `expo config --type public` exit 0, entry `require.resolve('./App.js')` OK, `node --test` ESM imports OK.

## License inventory (lockfile-derived, count by declared license)

```text
apps/web (114 entries): MIT 75, Apache-2.0 13, MPL-2.0 12, BSD-2-Clause 6, ISC 5, BSD-3-Clause 2, BlueOak-1.0.0 1
apps/mobile (530 entries): MIT 432, ISC 31, Apache-2.0 23, MPL-2.0 12, BSD-2-Clause 9, BSD-3-Clause 8,
  BlueOak-1.0.0 6, (MIT OR CC0-1.0) 2, Unlicense 2, Python-2.0 1, CC-BY-4.0 1, (MIT OR Apache-2.0) 1,
  0BSD 1, (BSD-3-Clause OR GPL-2.0) 1 [taken as BSD-3-Clause]
```

No strong-copyleft-only dependency in either tree.

## Dependabot note

The lockfile regeneration re-resolved transitives within pinned ranges; the three R-DEP-SEC-001 alerts (image-size 2x HIGH no-patch, uuid MEDIUM) remain applicable under the owner's accepted-with-revisit disposition — next revisit at H6-B closeout as scheduled.
