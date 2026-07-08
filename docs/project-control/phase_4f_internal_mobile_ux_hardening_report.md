# Phase 4F — Internal Mobile UX Hardening / Runtime QA Refresh Report

## 1. Scope

Phase 4F is Product / QA work for the existing internal Expo mobile scaffold only.

This phase improved readability, spacing, warning visibility, track status clarity, question-card clarity, selected-answer state, disabled-submit state, feedback-after-submit clarity, and blocked-scope grouping using built-in React Native primitives only.

This phase does not prove production readiness.
This phase does not prove public readiness.
This phase does not prove exam readiness.
This phase does not prove APK/build/install readiness.
This phase does not prove legal/currentness/content completeness.

## 2. Starting Repository State

Phase 4E verified main / merge commit:

```text
f43bd0e3c43fe305e807fcf4f66d2d0076207f33
```

Phase 4F branch:

```text
phase-4f-internal-mobile-ux-hardening
```

## 3. Control Files Read

Phase 4F followed these project-control files before app edits:

```text
docs/project-control/DEVELOPMENT_CONTROL_MODEL_V3.md
docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md
docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md
docs/project-control/PHASE_ONE_SCOPE.md
docs/project-control/PROJECT_SCOPE_BOUNDARIES.md
docs/project-control/KNOWN_GAPS_AND_NON_GOALS.md
docs/project-control/CLAIM_LEVELS_AND_RELEASE_GATES.md
docs/project-control/ROLE_BOUNDARIES.md
docs/project-control/red-team/PR_REVIEW_CHECKLIST.md
```

Controls preserved:

- controlled milestone development;
- Phase One internal-only boundaries;
- Law & Business first;
- C10 deferred / blocked;
- no public, production, exam-ready, APK/build/install, or legal/currentness/content-completeness claim;
- no backend/auth/payment/scoring/readiness/persistence/analytics scope;
- claim level remains command/source verified only, not visual/device/build/install verified.

## 4. Files Changed

Files changed in Phase 4F:

```text
apps/mobile/App.js
apps/mobile/src/components/InternalBanner.js
apps/mobile/src/components/QuestionCard.js
apps/mobile/src/components/TrackStatusCard.js
docs/project-control/phase_4f_internal_mobile_ux_hardening_report.md
```

No other files were changed.

## 5. UX Changes Implemented

### Layout and grouping

`App.js` now uses `StyleSheet`, a styled `SafeAreaView`, and padded `ScrollView` content. The screen is grouped into:

- internal warning banner;
- Phase One internal tracks;
- internal fixture interaction;
- blocked scope text.

### Internal warning visibility

`InternalBanner.js` now uses a bordered warning panel, warning pills, stronger typography, and visible required warnings:

```text
ContractorOS California
INTERNAL-ONLY
FIXTURE-ONLY
NOT PUBLIC
NOT EXAM-READY
NO SCORE / NO READINESS / NO PASS-FAIL
```

### Track cards

`TrackStatusCard.js` now distinguishes active versus blocked/deferred tracks with local styles and explicit status labels:

```text
Law & Business active internal fixture track
C10 deferred / blocked
```

### Question card

`QuestionCard.js` now improves the prompt, choice spacing, selected-choice state, locked/submitted choice state, disabled submit state, and feedback panel.

### Selected answer state

Selected answer state now shows stronger styling and a visible prefix:

```text
✓ Selected —
```

### Submit and feedback behavior

Submit remains disabled until a local choice is selected. Feedback appears only after submit.

### Reset / retry

A reset button was added:

```text
Reset local fixture interaction
```

It is local React state only. It resets `selectedChoiceId` and `submitted`. It does not create scoring, readiness, pass/fail, persistence, telemetry, analytics, or remote calls.

## 6. Behavior Preserved

Confirmed preserved:

```text
select answer
submit
feedback appears only after submit
no score
no readiness
no pass/fail
no persistence
no telemetry
no remote call
```

Also preserved:

- internal-only;
- fixture-only;
- not public;
- not exam-ready;
- Law & Business active internal fixture track;
- C10 deferred / blocked;
- Internal fixture interaction;
- Blocked scope text.

## 7. Commands Run

Commands run from `apps/mobile`:

```bash
npm install
npx expo --version
npx expo start --help
CI=1 npx expo start --non-interactive
```

### npm install

Output:

```text
npm warn deprecated uuid@7.0.3: uuid@10 and below is no longer supported.  For ESM codebases, update to uuid@latest.  For CommonJS codebases, use uuid@11 (but be aware this version will likely be deprecated in 2028).

added 471 packages, and audited 472 packages in 22s

42 packages are looking for funding
  run `npm fund` for details

10 moderate severity vulnerabilities

To address issues that do not require attention, run:
  npm audit fix

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
```

### npx expo --version

Output:

```text
57.0.6
```

### npx expo start --help

Output summary:

```text
Info
  Start a local dev server for the app

Usage
  $ npx expo start <dir>

Options included Android, iOS simulator, web, dev-client, Expo Go, clear cache, max workers, production bundle mode, minify, host mode, tunnel, LAN, localhost, offline mode, HTTPS, scheme, port, private key path, and help.
```

### CI=1 npx expo start --non-interactive

Output:

```text
  --non-interactive is not supported, use $CI=1 instead
Starting project at /mnt/data/phase4f/apps/mobile
Metro is running in CI mode, reloads are disabled. Remove CI=true to enable watch mode.
Starting Metro Bundler

Waiting on http://localhost:8081

Logs for your project will appear below.
Networking has been disabled
Unable to reach well-known versions endpoint. Using local dependency map expo/bundledNativeModules.json for version validation
Dependency validation is unreliable in offline-mode
```

Result: Metro reached `http://localhost:8081`. The process was stopped by timeout because the dev server is intentionally long-running.

## 8. Dependency / Lockfile Handling

`npm install` generated `apps/mobile/package-lock.json` locally.

The generated lockfile was scanned with:

```bash
grep -R "applied-caas\|internal.api.openai.org\|sandbox\|localhost\|127.0.0.1" -n apps/mobile/package-lock.json || true
```

Internal registry hits were found. Representative hits:

```text
18: packages.applied-caas-gateway1.internal.api.openai.org ... @babel/code-frame
32: packages.applied-caas-gateway1.internal.api.openai.org ... @babel/compat-data
41: packages.applied-caas-gateway1.internal.api.openai.org ... @babel/core
```

The generated lockfile was deleted locally and was not committed.

Vulnerability count: 10 moderate severity vulnerabilities.

No dependency remediation was attempted.

No dependencies were added.

## 9. Forbidden Scope Scan

Before clean-source scan, `node_modules` and generated `apps/mobile/package-lock.json` contained many dependency/vendor hits. Those were not source implementation hits.

After deleting local `node_modules` and generated `apps/mobile/package-lock.json`, the required clean-source scan was run:

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail\|analytics" -n apps/mobile || true
```

Result:

```text
apps/mobile/src/components/QuestionCard.js:58:          <Text style={styles.noOutcome}>No score, readiness, pass/fail, persistence, telemetry, or remote call was produced.</Text>
apps/mobile/app.json:8:    "description": "Internal-only ContractorOS California Expo scaffold. Fixture-only, not public, not readiness eligible.",
apps/mobile/App.js:8:  'No score calculation',
apps/mobile/App.js:9:  'No readiness result',
apps/mobile/App.js:10:  'No pass/fail result',
apps/mobile/App.js:13:  'No auth, login, or user accounts',
apps/mobile/App.js:14:  'No payments or subscriptions',
apps/mobile/App.js:15:  'No analytics',
```

Classification:

- `QuestionCard.js` hit: allowed warning text / allowed blocked-scope text.
- `app.json` hit: allowed warning text.
- `App.js` hits: allowed warning text / allowed blocked-scope text.
- No forbidden implementation found.
- No patch required.

## 10. Explicit Exclusions

Confirmed not added:

- backend;
- database;
- Firebase;
- Airtable runtime;
- deployment;
- auth/login/user accounts;
- payments/subscriptions;
- scoring;
- readiness;
- pass/fail;
- saved progress;
- analytics;
- public MCQs;
- Question Bank migration;
- C10 public content;
- EAS;
- APK;
- AAB;
- iOS build;
- android/;
- ios/;
- eas.json;
- package-lock.json;
- ZIP binaries.

## 11. Known Limitations

This phase does not include visual/device QA.

This phase does not include APK, AAB, iOS build, install testing, or app-store testing.

This phase does not resolve the dependency-lock issue.

This phase does not resolve the 10 moderate npm vulnerabilities.

This phase does not create or validate a production content system.

This phase does not prove legal/currentness/content completeness.

## 12. Phase Result

Phase 4F is ready for red-team review as an internal mobile UX hardening and runtime smoke QA refresh PR.

Runtime smoke result: Metro reached `http://localhost:8081`.

Claim level: source verified and command verified only.

## 13. Next Phase Status

Phase 4G was not started.

PR must be reviewed before merge.

No next phase may begin until PR is merged and `main` is verified.
