# H6-A Toolchain Evidence — 2026-08-10

Recorded independently from product-readiness claims (issue #64 item 9). All commands run locally on macOS with node v26.5.0 / npm 12.0.1 against https://registry.npmjs.org/ (resolution host); CI consumption uses the pinned Node 22 line.

Delivery shape: H6-A lands as two PRs under lane purity — H6-A.1 (Control / Infrastructure: this evidence, TOOLCHAIN.md, .nvmrc, PA-0011, scanner lockfile exemption) and H6-A.2 (Product / QA + Dependency lane: the app manifests and lockfiles this evidence describes). The lockfile digests below bind the H6-A.2 artifacts in advance; verify at H6-A.2 review.

## Version selection provenance

- Node 22 LTS latest at selection time: v22.23.2 ("Jod", ships npm 10.9.8) — read live from https://nodejs.org/dist/index.json.
- Expo latest at selection time: 57.0.11 — `npm view expo dist-tags.latest`.
- react 19.2.3 / react-native 0.86.2 — resolved by `npx expo install react react-native` AND independently confirmed against `expo@57.0.11`'s own `bundledNativeModules.json` (both sources agree).

## Determinism proofs

- Byte-identical lockfile re-resolution: `npm install --package-lock-only` from the final `apps/mobile/package.json` in two separate fresh directories produced byte-identical package-lock.json files (diff clean). An earlier incrementally-grown lockfile (multi-step install history) differed in tree shape and was DISCARDED in favor of the clean single-shot resolution — recorded so the baseline's provenance is unambiguous.
- Clean install: `npm ci --no-audit --no-fund` from the committed mobile lockfile: 463 packages, exit 0. Web lockfile: `npm ci` 20 packages, exit 0, followed by a green `vite build` producing dist/index.html.
- Lockfile drift: `npm ci` modifies neither manifest nor lockfile (web-ci drift check remains the enforcing gate).

## Registry provenance & contamination

- apps/mobile/package-lock.json: 473 `resolved` URLs, 100% https://registry.npmjs.org/, zero hits for the contamination token set (applied-caas, internal.api.openai.org, sandbox, localhost, 127.0.0.1).
- apps/web/package-lock.json: pre-existing baseline (PR #90/#91 era) unchanged except the root `engines` entry; same scans clean via `check_forbidden_scope.py --lockfiles-only`.

## Lockfile digests (sha256)

```text
apps/mobile/package-lock.json  89bc1562f91b341e0a528249a28c29dd1fda6223ca51c88a87fb2e20494c834c
apps/web/package-lock.json     4741f1e5437f060898f7f3ac61bb0d6d56e6cc856c5d43b2938479bf575b71be
```

## License inventory (lockfile-derived, count by declared license)

```text
apps/mobile (481 packages): MIT 404, ISC 29, MPL-2.0 12, Apache-2.0 11, BSD-3-Clause 7,
  BlueOak-1.0.0 6, BSD-2-Clause 3, (MIT OR CC0-1.0) 2, Unlicense 2, Python-2.0 1,
  CC-BY-4.0 1, (MIT OR Apache-2.0) 1, 0BSD 1, (BSD-3-Clause OR GPL-2.0) 1 [taken as BSD-3-Clause]
apps/web (33 packages): MIT 28, MPL-2.0 12*, Apache-2.0 1, ISC 1, BSD-3-Clause 1
```

*Web MPL-2.0 count reflects per-entry lockfile records. No strong-copyleft-only dependency exists in either tree.

## EOL / unsupported check

Node 22 is the active LTS line (support horizon beyond this baseline); Expo SDK 57 is the current stable SDK at selection time. No dependency in either manifest is EOL-flagged at its pinned version.

## Deliberate failure tests (issue #64)

Executed in scratch copies (results recorded as observed, including the one that did NOT fail):
- lockfile drift: hand-edited lockfile version field → `npm ci` exit 1 (sync refusal). FAILED AS DESIGNED.
- unpinned latest: `"expo": "latest"` reintroduced against the committed lockfile → **`npm ci` exit 0 — it does NOT catch dist-tag declarations** (a tag spec is treated as satisfiable by whatever the lockfile pins). GAP FOUND: `npm ci` alone cannot enforce pinned manifests; a dedicated manifest pin scan (reject dist-tags and ranges in dependencies) is required and is tracked to the H6-B CI gate (control-script/workflow changes are outside PA-0011's paths by design).
- registry contamination: injected `localhost` resolved URL → `check_forbidden_scope.py --lockfiles-only` exit 1, "FAIL: lockfile contamination detected". FAILED AS DESIGNED.
- missing scripts: `npm run <undeclared-script>` in the pinned mobile package → exit 1. FAILED AS DESIGNED. (Originally exercised via a draft root orchestration manifest; that manifest was deferred to H6-B under lane purity — see the decision log — and the test re-run package-locally.)
- incompatible peers: react 18.3.1 pinned against react-native 0.86.2 → `npm install` exit 1, ERESOLVE. FAILED AS DESIGNED.
