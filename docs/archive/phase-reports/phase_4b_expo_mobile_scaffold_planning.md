# Phase 4B — Expo Mobile Scaffold Planning

## Scope

Phase 4B is a planning/report phase only. It creates a concrete implementation plan for a future Expo / React Native mobile scaffold without adding mobile code or changing app source.

No `apps/mobile`, Expo config, React Native files, Capacitor files, Android files, iOS files, backend, database, Firebase, Airtable runtime, deployment, auth, payments, scoring, readiness, pass/fail logic, public launch pages, marketing pages, app-store materials, new MCQs, Question Bank migration, C10 public content, ZIP binaries, dependency-lock changes, package-lock, or internal/sandbox registry URLs were added.

## 1. Current Repository State

Confirmed current repository state:

- `apps/web` exists and is the current React/Vite internal fixture shell.
- No `apps/mobile` directory exists.
- No Expo scaffold exists.
- No Android native project exists.
- No iOS native project exists.
- `apps/web/package-lock.json` remains absent.
- Dependency-lock/public npm reproducibility remains open.
- Current source remains fixture-only.
- Law & Business remains first internal fixture track.
- C10 remains deferred/blocked.
- No backend, database, Firebase, Airtable API runtime, auth, payments, scoring, readiness, or pass/fail logic exists.

## 2. Official Expo References Reviewed

Official Expo documentation reviewed for this planning phase:

1. Expo development builds: https://docs.expo.dev/develop/development-builds/introduction/
   - Expo defines a development build as a debug build that includes `expo-dev-client`.
   - Expo distinguishes Expo Go as a playground with a fixed set of native libraries, while development builds are the fuller environment for production-grade Expo apps.

2. EAS Build introduction: https://docs.expo.dev/build/introduction/
   - EAS Build is a hosted service for creating app binaries for Expo and React Native projects.
   - EAS Build supports Android and iOS builds, build profiles in `eas.json`, and internal distribution build sharing.

3. Create an Expo project: https://docs.expo.dev/get-started/create-a-project/
   - Expo identifies itself as a React Native framework for Android and iOS app development.
   - Expo recommends starting with a default project created by `create-expo-app`.

4. EAS Build setup: https://docs.expo.dev/build/setup/
   - EAS Build requires a React Native Android or iOS project and an Expo account.
   - Expo documents EAS CLI setup and `eas build:configure` for build configuration.
   - Expo points to installable Android APK and iOS simulator resources for non-store testing.

5. EAS internal distribution: https://docs.expo.dev/build/internal-distribution/
   - Internal distribution with EAS Build provides shareable URLs for builds.
   - Setting `distribution: internal` affects Android by generating APK behavior suitable for direct installation and affects iOS through ad hoc or enterprise provisioning.

6. Expo Android APK builds: https://docs.expo.dev/build-reference/apk/
   - Expo documents that EAS Build defaults Android builds to AAB for Google Play distribution.
   - Expo documents that AAB files cannot be directly installed on a device and that APK files are needed for direct installation on Android devices or emulators.

## 3. Proposed Future Repo Structure

Recommended future target structure:

```text
apps/
  web/
    # existing React/Vite internal fixture shell
  mobile/
    # future Expo / React Native internal prototype app
```

Do not create this structure in Phase 4B.

### Shared packages evaluation

Possible later structure:

```text
packages/
  fixture-data/
  ui-policy/
```

Recommendation: do not create shared packages in the first implementation unless absolutely necessary. Keep Phase 4C minimal. Shared packages should wait until duplication becomes a practical maintenance problem.

Reason:

- The current fixture/data shape is still internal and unstable.
- Shared package setup adds monorepo complexity before there is a real mobile app.
- The first scaffold only needs enough internal fixture data to prove the native shell path.
- Shared packages can be introduced later after the mobile shell validates the screen model.

## 4. Future Phase 4C Scaffold File Plan

If Phase 4C is later approved as implementation, the expected minimum file additions are:

```text
apps/mobile/package.json
apps/mobile/app.json
apps/mobile/App.js
apps/mobile/src/
apps/mobile/src/screens/
apps/mobile/src/components/
apps/mobile/src/data/
apps/mobile/assets/
```

Optional future TypeScript variant if explicitly approved later:

```text
apps/mobile/App.tsx
apps/mobile/tsconfig.json
```

### App config decision

Start with:

```text
apps/mobile/app.json
```

Use `app.config.js` only if dynamic configuration becomes necessary. Avoid dynamic config in the first scaffold.

### EAS config decision

Do not create `eas.json` in the first minimal scaffold unless Phase 4C explicitly includes EAS build-profile planning and red-team approval.

Recommended split:

- Phase 4C: create minimal Expo app scaffold and local Expo development path only.
- Phase 4D: add EAS Android internal build planning/config if public-safe dependency install and Expo account assumptions are verified.

Reason: `eas.json` is build-distribution configuration. Adding it too early can blur the line between mobile scaffold and build/distribution work.

## 5. Dependency Strategy

### Should `apps/mobile/package-lock.json` be committed in the future?

Yes, eventually, but only if generated in a clean public npm environment and scanned clean.

### Lockfile rule

Do not commit any lockfile containing:

```text
applied-caas
internal.api.openai.org
sandbox
localhost
127.0.0.1
private registry URLs
```

### How to avoid internal/sandbox registry URLs

Future implementation must either:

1. run dependency installation in a verified clean external/public npm environment; or
2. run installation with a verified public registry configuration and prove the resulting lockfile contains only public-safe registry URLs.

### Does mobile dependency installation need a clean public npm environment?

Yes, for any committed lockfile. The current sandbox has already produced contaminated lockfiles for `apps/web`, so Phase 4C must not trust sandbox-generated lockfiles.

### Should Phase 4C proceed if public npm verification is unavailable?

Phase 4C may proceed only as a minimal scaffold if it does not commit a contaminated lockfile and documents the dependency risk. However, a future build/distribution phase should not claim reproducibility until a clean lockfile is generated and verified.

### Anti-contamination checks

Before committing any future mobile lockfile, run:

```bash
grep -R "applied-caas\|internal.api.openai.org\|sandbox\|localhost\|127.0.0.1" -n apps/mobile/package-lock.json || true
```

If any hit appears, do not commit the lockfile.

## 6. Fixture Data Strategy

### Option A — copied minimal fixture records into `apps/mobile`

Recommended for the first scaffold.

Pros:

- Smallest controlled surface.
- Avoids importing from web-specific modules.
- Preserves mobile scaffold isolation.
- Keeps Phase 4C easy to red-team.

Cons:

- Creates short-term duplication.
- Requires later cleanup if data grows.

### Option B — import from `apps/web/src/data`

Not recommended for first scaffold.

Pros:

- Avoids duplication.

Cons:

- Couples mobile to the web app source tree.
- Risks pulling web-specific assumptions into React Native.
- Makes future mobile packaging harder.

### Option C — extract shared fixture package later

Recommended later, not now.

Pros:

- Long-term maintainability.
- Cleaner cross-platform source of truth.

Cons:

- Adds monorepo/package complexity.
- Premature before mobile screens exist.

### Fixture recommendation

For first mobile scaffold, use the smallest controlled fixture subset in `apps/mobile/src/data/`, preserve all internal-only labels, and do not migrate the full Question Bank.

Do not create public MCQs. Do not create C10 public content. Do not add scoring, readiness, or pass/fail logic.

## 7. Minimum Mobile UX Scope for First Implementation

Minimum internal mobile shell for Phase 4C if later approved:

- internal-only banner;
- Law & Business fixture track visible;
- C10 deferred/blocked state;
- one simple internal fixture question flow;
- answer selection;
- submit-before-feedback behavior;
- no score;
- no readiness;
- no pass/fail;
- blocked route/status screen;
- source/governance warning text;
- local-only issue-report mock or explicitly deferred issue-report panel.

Hard exclusions for first mobile shell:

- no auth;
- no payments;
- no backend;
- no database;
- no Firebase;
- no Airtable API runtime;
- no scoring;
- no readiness;
- no pass/fail;
- no public content;
- no new MCQs;
- no C10 public content.

## 8. Android-First Test Path

### Expo Go vs development build

Expo Go may be useful for quick early UI development only if all used libraries are compatible with Expo Go. However, official Expo docs describe Expo Go as a playground with fixed native libraries, while development builds are the fuller environment for production-grade Expo apps.

Recommendation: use Expo Go only as a convenience during initial scaffold smoke checks. Treat an Expo development build as the real internal prototype path.

### Local dev server vs installable build

- Local dev server: useful for rapid development and UI iteration.
- Installable Android build: required for sideloadable prototype confidence.

### APK vs AAB

- AAB is Google Play oriented and not directly installable on Android devices.
- APK is required for direct installation on Android device/emulator.

### Is EAS Build needed for the first installable artifact?

Likely yes for the fastest controlled APK path, unless a local native build path is explicitly approved and verified. EAS Build can create Android binaries and supports internal distribution. However, Phase 4B does not create a build.

### Is Google Play internal testing required?

No. Google Play internal testing is optional later. The first Android internal prototype can use an APK sideload/development build path before Play Console testing.

## 9. iOS Planning Assumptions

iOS should come after Android for this project.

Assumptions:

- iOS device testing requires Apple Developer account/provisioning decisions if moving beyond simulator-only checks.
- EAS internal distribution for iOS uses ad hoc or enterprise provisioning.
- TestFlight is a later beta distribution path, not required for the first Android internal prototype.
- No iOS build should be attempted in Phase 4B.
- No iOS files should be created in Phase 4B.

## 10. Phase 4C Recommendation

Recommended next phase:

```text
Phase 4C — Expo Internal Mobile Scaffold
```

This recommendation is conditional. Phase 4C should be approved only if red-team accepts these constraints:

- create `apps/mobile` only;
- no backend;
- no database;
- no Firebase;
- no Airtable runtime;
- no auth;
- no payments;
- no scoring/readiness/pass-fail;
- no new MCQs;
- no C10 public content;
- no Expo/EAS build artifact yet unless separately authorized;
- no contaminated lockfile;
- no Android/iOS native folders unless generated by an explicitly approved command and verified.

If dependency/public npm verification is still unavailable, Phase 4C may still create a minimal scaffold but must not commit any contaminated lockfile and must document the blocker.

## 11. Readiness Estimate

```text
Current Android sideloadable prototype readiness: 15%
After Phase 4B planning readiness: 30%
After Phase 4C scaffold readiness: 55%
Production/public MVP readiness: 5%
```

### Current Android sideloadable prototype readiness: 15%

The project has a working internal web fixture shell and governance documentation, but no mobile package, no Expo app, no Android build profile, no native install artifact, and unresolved dependency-lock risk.

### After Phase 4B planning readiness: 30%

This plan removes ambiguity around repo structure, scaffold files, mobile UX scope, fixture reuse, Android-first testing, iOS assumptions, and dependency-lock risk. It does not create a mobile app.

### After Phase 4C scaffold readiness: 55%

Assuming Phase 4C creates only a minimal Expo app shell with internal-only fixture UX and no forbidden runtime scope, the project would have a real mobile package but still no verified sideloadable APK unless a later build phase creates one.

### Production/public MVP readiness: 5%

The product remains internal-only, fixture-only, not public, not readiness eligible, pending legal/currentness review, without public MCQ bank, backend, auth, payments, scoring/readiness/pass-fail, app-store compliance package, or clean dependency-lock reproducibility.

## 12. Explicit Boundaries

Confirmed not done in Phase 4B:

- No Phase 4C implementation.
- No mobile scaffold.
- No Expo app files.
- No React Native files.
- No Capacitor files.
- No Android files.
- No iOS files.
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
- No ZIP binaries.
- No dependency-lock changes.
- No package-lock committed.
- No internal/sandbox registry URLs committed.

## Red-team gates for future Phase 4C

Before Phase 4C can be merged, red-team should verify:

- only intended `apps/mobile` scaffold files were added;
- no backend/database/Firebase/Airtable runtime exists;
- no scoring/readiness/pass-fail logic exists;
- no public MCQs or C10 public content exists;
- no Android/iOS native folders were added unless explicitly authorized;
- no `eas.json` unless explicitly authorized;
- no contaminated lockfile;
- internal-only warnings are visible in the mobile shell;
- Law & Business fixture track is clearly internal;
- C10 is clearly deferred/blocked;
- issue-report UI is local/mock only or deferred;
- no app-store or production/public readiness claim is introduced.

## Phase 4B result

Phase 4B is report-only. The recommended next implementation phase is `Phase 4C — Expo Internal Mobile Scaffold`, constrained to a minimal Expo app package under `apps/mobile` and preserving all internal-only, fixture-only, no-backend/no-scoring/no-public-content boundaries.