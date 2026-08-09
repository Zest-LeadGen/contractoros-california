# Phase 4A — Mobile Prototype Path Decision

## Scope

Phase 4A is a strategy/report-only decision checkpoint. It evaluates the safest and fastest path toward an internal sideloadable prototype without starting mobile implementation.

No mobile code, Expo scaffold, React Native files, Capacitor files, Android project files, iOS project files, backend, database, Firebase, Airtable runtime, deployment, auth, payments, scoring, readiness, pass/fail logic, new MCQs, Question Bank migration, C10 public content, dependency-lock change, package-lock, or ZIP binary was added.

## Current verified repository state

- Phase 3A source import merged into `main`.
- Phase 3B QA/hygiene patch merged into `main`.
- Phase 3C reproducibility blocker report merged into `main`.
- Phase 3D manual web UX QA report merged into `main`.
- Latest verified Phase 3D merge commit: `e3fcb6174e6bc78ec05751807a334d87cb94554e`.
- Current app is an internal React/Vite fixture shell only.
- `apps/web/package-lock.json` remains absent.
- `apps/web/package.json` still uses `latest` dependencies.
- Dependency-lock/public npm reproducibility remains an open blocker for a future clean external environment.

## 1. Current App State

Confirmed current app state:

- Current runnable shell is a React/Vite web app under `apps/web`.
- It is fixture-only.
- Law & Business is the first usable internal fixture track.
- C10 is deferred/blocked.
- No backend exists.
- No database exists.
- No Firebase exists.
- No Airtable API runtime exists.
- No auth exists.
- No payments/subscriptions exist.
- No scoring, readiness, or pass/fail logic exists.
- No mobile app code exists yet.
- No Android or iOS project files exist yet.

## Official references reviewed

- Expo development builds documentation states that a development build is a debug build including `expo-dev-client`, and that development builds are the production-grade development environment rather than Expo Go-only playground usage: https://docs.expo.dev/develop/development-builds/introduction/
- Expo EAS Build documentation states EAS Build creates app binaries for Expo and React Native projects, supports Android and iOS builds, and can share internal distribution builds with a URL: https://docs.expo.dev/build/introduction/
- Capacitor documentation describes Capacitor as a cross-platform native runtime for web apps and says it can be dropped into an existing modern JavaScript project: https://capacitorjs.com/docs
- Google Play Console documentation says internal testing can distribute an app to up to 100 testers and recommends internal testing for initial QA checks: https://support.google.com/googleplay/android-developer/answer/9845334
- Apple TestFlight documentation says TestFlight can distribute beta builds to internal and external testers through App Store Connect, with up to 100 internal testers and up to 10,000 external testers: https://developer.apple.com/testflight/

## 2. Mobile Prototype Options

### Option A — Expo / React Native

#### Feasibility

Feasible, but not in Phase 4A. The current web shell is not React Native, so a real Expo path requires a separate app package, likely `apps/mobile`, plus a shared data/module strategy for fixture records and governance metadata.

#### Required repo structure

Recommended future structure:

```text
apps/
  web/
    # existing React/Vite internal fixture shell
  mobile/
    # future Expo / React Native app
packages/
  fixture-data/
    # optional future shared fixture data extraction
  ui-policy/
    # optional future shared labels, warnings, route gates
```

For the first mobile scaffold, avoid overbuilding packages unless reuse becomes painful. The minimum safer structure is:

```text
apps/mobile/
```

with explicit imports or copied fixture JSON from the existing app only after red-team approves Phase 4B implementation.

#### Fixture-data reuse strategy

The first mobile prototype should reuse the same fixture posture and governance boundaries, but it should not automatically migrate the full current web source into mobile. Safer strategy:

1. Identify the minimal fixture data needed for mobile smoke testing.
2. Extract or duplicate only internal fixture-safe records.
3. Preserve internal-only labels and blocked states.
4. Do not introduce public MCQs.
5. Do not create scoring/readiness/pass-fail logic.
6. Do not add a backend.

#### Android internal testing path

Expo/EAS is strongest for the internal Android prototype path because EAS Build can produce installable Android binaries and supports internal distribution workflows. Google Play internal testing is also available later and supports up to 100 testers for initial QA, but a Play Console path is not required for a first internal sideloadable APK decision.

#### iOS path

iOS is inherently more constrained than Android. Expo/EAS can produce iOS builds, but device testing normally requires Apple developer account/provisioning/TestFlight/ad hoc decisions. Apple TestFlight is the proper later beta route, but it requires App Store Connect workflow and, for external testers, beta app review. This should be planned, not rushed.

#### Effort level

Medium. More work than a WebView wrapper, but cleaner for long-term app quality. Expected first implementation tasks:

- create `apps/mobile` Expo app;
- reproduce internal-only shell screens natively;
- port minimal fixture data;
- add hard blocked-route screen states;
- build Android development/internal artifact;
- keep iOS planning documented but not required for the first Android smoke test.

#### Risks

- Dependency-lock/public npm reproducibility remains unresolved.
- React Native UI will need separate implementation, not direct copy/paste from the Vite DOM app.
- Content governance warnings must be preserved exactly.
- App-source duplication risk if shared data strategy is not controlled.
- Expo/EAS introduces account/build-service decisions later.

#### Recommendation status

Recommended path.

Reason: Expo / React Native is the better real prototype architecture for a mobile-first exam prep product. It avoids locking the product into a WebView shell, gives a cleaner route to native mobile UX, and has a better path to Android internal testing and later iOS/TestFlight workflows.

### Option B — Capacitor / WebView Wrapper

#### Feasibility

Feasible and likely faster than Expo in the short term because the existing app is already a React/Vite web app. Capacitor is designed for web-first projects and can wrap an existing modern JavaScript app into native containers.

#### Speed

Fastest path to something installable if the only goal is to put the current web shell on a phone quickly.

#### Risks

- It carries the current web shell architecture into mobile rather than creating a true mobile UX.
- It may encourage premature reliance on DOM/web behavior.
- It can mask future native UX issues until later.
- It may make the app feel like a wrapped website rather than a serious exam-prep mobile app.
- It does not solve dependency-lock/public npm reproducibility.

#### Dependency on current web shell

High. This path depends directly on the current Vite shell. That shell is intentionally internal, fixture-only, and not public-ready.

#### Limitations

Capacitor is useful when the web app is already mature. ContractorOS California is not there yet. The current shell is a governance/fixture prototype, not a polished mobile-ready web product.

#### Recommendation status

Rejected for the primary internal mobile prototype path.

Reason: Capacitor is a legitimate shortcut, but it would optimize for immediate wrapping rather than correct mobile architecture. It is acceptable only as a future demo shortcut if speed is more important than mobile product quality.

### Option C — Stay Web-Only Longer

#### Benefits

- Lowest technical risk.
- Keeps QA simple.
- Avoids mobile dependency/tooling complexity.
- Allows more governance, source, and fixture clarity before mobile UI work.
- Avoids duplication between web and mobile while the app model is still changing.

#### Risks

- Delays real mobile interaction learning.
- Delays Android sideload/internal testing feedback.
- May overfit UX decisions to desktop/web rather than mobile exam-prep use.
- Does not move toward the stated mobile prototype objective.

#### When this is right

Stay web-only longer if the next goal is content governance, Airtable schema, source review, or public-readiness policy. It is not the best choice if the next goal is an internal sideloadable mobile prototype.

#### Current web QA needs

Phase 3D found no current internal app-source blocker. More web QA is useful but not required before planning mobile.

#### Recommendation status

Not recommended as the main path if the goal is mobile prototype progress. Acceptable only if red-team decides dependency-lock must be resolved before any new app package is added.

### Option D — Defer Mobile Until Dependency-Lock Is Resolved

#### Dependency-lock risk

The repo still lacks a public-safe `apps/web/package-lock.json`, and dependencies remain set to `latest`. That is not production-safe. It also weakens reproducibility for any build path.

#### Why it matters

Without a clean public lockfile, builds may drift over time. A future clean external environment must prove public npm resolution and commit a lockfile without internal/sandbox registry URLs.

#### Does it block internal mobile prototyping?

No, not completely. It should block production/public release readiness and any claim of clean reproducibility. It should not block a report-approved internal Expo scaffold if Phase 4B explicitly avoids production claims, avoids publishing, avoids app stores, and documents dependency state honestly.

#### Recommendation status

Do not fully defer mobile. Keep the dependency-lock blocker active, but proceed to scaffold planning before implementation.

## 3. Recommendation

Recommended path:

```text
Proceed with Expo / React Native for the internal sideloadable prototype path.
```

Rationale:

1. ContractorOS California is intended to become a serious exam-prep mobile product, not merely a wrapped web page.
2. Expo / React Native gives the cleanest mobile architecture among the compared options.
3. Expo development builds and EAS Build provide a practical path to real installable internal builds.
4. Android internal prototype work is achievable before iOS/TestFlight decisions are fully finalized.
5. The current React/Vite shell should remain the internal web fixture/governance reference, not become the long-term mobile runtime.
6. Capacitor is faster, but weaker architecturally for this product.
7. Staying web-only longer is safest but does not advance the approved mobile prototype objective.
8. The dependency-lock issue remains a blocker for production-grade reproducibility, not for controlled mobile scaffold planning.

## 4. Proposed Next Phase

Recommended next phase:

```text
Phase 4B — Expo Mobile Scaffold Planning
```

Do not implement the mobile scaffold yet in Phase 4A.

Phase 4B should produce a concrete implementation plan for:

- exact `apps/mobile` repo structure;
- Expo app package boundaries;
- fixture data reuse strategy;
- Android-first internal prototype path;
- iOS/TestFlight planning assumptions;
- build commands;
- red-team gate criteria;
- dependency-lock risk handling;
- no backend/auth/payments/scoring/readiness/pass-fail scope.

After red-team approves that plan, a later implementation phase can create the Expo scaffold.

## 5. Prototype Readiness Estimate

```text
Current Android sideloadable prototype readiness: 15%
After Phase 4B scaffold readiness: 45%
Production/public MVP readiness: 5%
```

### Current Android sideloadable prototype readiness: 15%

Reason: the project has a working internal React/Vite fixture shell and clear governance boundaries, but no mobile app package, no Expo config, no Android build profile, no native project/build artifact, and unresolved dependency-lock reproducibility.

### After Phase 4B scaffold readiness: 45%

Assumption: Phase 4B is planning only or creates a clearly approved minimal scaffold in a later implementation phase. If Phase 4B only plans, readiness rises mainly through reduced ambiguity. If red-team later authorizes implementation, readiness can move faster. A scaffold alone still would not equal a tested sideloadable APK.

### Production/public MVP readiness: 5%

Reason: the current product is internal-only, fixture-only, not public, not readiness eligible, pending legal/currentness review, has no public MCQ bank, no backend, no auth, no payments, no scoring/readiness/pass-fail logic, no app-store compliance package, and unresolved dependency-lock reproducibility.

## 6. Boundaries

Confirmed forbidden/not done in Phase 4A:

- No Phase 4B implementation.
- No mobile implementation.
- No Expo scaffold.
- No React Native files.
- No Capacitor files.
- No Android project files.
- No iOS project files.
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
- No package-lock committed.
- No internal/sandbox registry URLs committed.

## Phase 4A result

Phase 4A is report-only. The decision is to prefer Expo / React Native for the internal sideloadable mobile prototype path, with Phase 4B limited to Expo Mobile Scaffold Planning unless explicitly approved otherwise. Capacitor is kept as a fallback shortcut, not the preferred architecture. Dependency-lock remains an open blocker for production-grade reproducibility but does not fully block controlled internal mobile scaffold planning.