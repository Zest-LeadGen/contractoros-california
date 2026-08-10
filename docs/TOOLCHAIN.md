# ContractorOS Toolchain (H6-A baseline)

Authority: issue #118 comment 5235003178 (H6 owner authorization); PA-0011. Established 2026-08-10.

## Pinned tooling

| Tool | Pin | Where enforced |
| --- | --- | --- |
| Node.js | v22.23.2 (22 LTS "Jod" line) | `.nvmrc` (exact); `engines` ">=22.11.0 <23" in each app package.json (lands with the H6-A.2 dependency-pin PR) |
| npm | 10.9.8 (ships with Node v22.23.2) | `engines` ">=10.9.0" |
| Registry | https://registry.npmjs.org/ only | lockfile provenance scan (`check_forbidden_scope.py --lockfiles-only`); web-ci registry check |

Node 24/26 and npm 11+ are not supported targets yet; `engines` fails installs outside the 22 line when `engine-strict` is set, and CI (H6-B) installs from `.nvmrc`.

## Package boundaries

- **No root manifest, deliberately.** `apps/web` and `apps/mobile` are isolated packages with independent public-registry lockfiles: Expo/Metro resolve `node_modules` per-app, and npm-workspace hoisting is opted out of until monorepo tooling is separately evaluated and authorized. (A root orchestration manifest was drafted in H6-A and deferred: under the control-file update matrix a root `package.json` is Dependency-lane, and it carries no value until the H6-B CI jobs exist to call it. Revisit with H6-B.)
- `apps/web` — Vite + React. Pinned exact: react 19.2.8, react-dom 19.2.8, vite 8.2.1, @vitejs/plugin-react 6.0.5. Lockfile committed since PR #90; CI = contractoros-web-ci (npm ci, registry check, drift check, build). Engines pin lands with H6-A.2.
- `apps/mobile` — Expo prototype. Baseline pins per Expo SDK 57's own compatibility manifest (`expo/bundledNativeModules.json`): expo 57.0.11, react 19.2.3, react-native 0.86.2 — the `latest` declarations are removed and the lockfile lands with the H6-A.2 dependency-pin PR (Product / QA + Dependency lane); CI wiring lands in H6-B.

## Deterministic install

From a clean checkout with pinned tooling:

```
npm ci --no-audit --no-fund --prefix apps/web      # from apps/web/package-lock.json
npm ci --no-audit --no-fund --prefix apps/mobile   # from apps/mobile/package-lock.json
```

`npm ci` only (never bare `npm install`) in CI and clean environments; it installs exactly the lockfile or fails.

Known limitation (verified by deliberate test): `npm ci` does NOT reject a `"latest"` dist-tag reintroduced into a manifest — it installs whatever the lockfile pins. Manifest pinning is therefore enforced by review plus a dedicated manifest pin scan landing with the H6-B CI gate (reject dist-tags and version ranges in app `dependencies`/`devDependencies`).

## Dependency update policy

- Updates are deliberate, never "because newest" (issue #64 forbidden scope). A dependency change requires: the phase authorization covering the manifest+lockfile paths, regeneration of the lockfile via a clean `npm install --package-lock-only`, a byte-identical second resolution from a fresh directory, the provenance/contamination scan, and a green build.
- Mobile versions follow the Expo SDK compatibility manifest — react/react-native are only moved together with the `expo` pin.
- Rollback = revert the manifest+lockfile commit (both files always change together).
- Vulnerability response: advisories evaluated against the pinned set at phase boundaries; an out-of-band security bump follows the same regeneration+evidence procedure under its own authorization.
- License review: lockfile-derived inventory recorded in `docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md`; current baseline is permissive/weak-copyleft only (MIT/ISC/Apache-2.0/BSD/MPL-2.0/BlueOak; dual-licensed packages taken under their permissive option). Adding a strong-copyleft dependency requires an explicit owner decision.

## Test layers (ownership ledger, per issue #64 item 7)

| Layer | Status |
| --- | --- |
| Unit / component / integration (web) | H6-B (CI wiring) |
| Accessibility, visual | tracked, blocked until product surface stabilizes |
| End-to-end, device/emulator | tracked, blocked (no release scope; issue #64 forbidden scope) |
| Build validation (web) | ACTIVE (contractoros-web-ci) |
| Mobile static/bundle validation | H6-B |
| Release layers | blocked until a release phase exists |

Toolchain evidence is recorded separately from product-readiness claims (issue #64 item 9); nothing here claims product readiness.
