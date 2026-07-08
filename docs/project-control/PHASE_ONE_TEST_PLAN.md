# Phase One Test Plan

Purpose: define how internal Phase One will be tested. Tests prove only what they directly test.

## Test Categories

- source inspection
- dependency/install check
- Metro/runtime smoke check
- web local build check
- mobile runtime smoke check
- future visual/device QA
- future Android build gate if approved
- forbidden-scope scan
- lockfile contamination scan
- claim-level review
- risk-register review

## Source Inspection

Verify internal warnings, Law & Business fixture path, C10 deferred state, fixture interaction, and blocked-scope text in source files.

## Dependency / Install Check

Run approved install/version/help commands only in an approved phase. Document package-lock generation, scans, vulnerability counts, and remediation decisions.

## Runtime Smoke Checks

Metro/runtime smoke checks verify only that the internal scaffold starts in the tested environment. They do not prove visual QA, install readiness, store readiness, or production readiness.

## Future Visual / Device QA

Visual/device QA must separately document device/emulator/browser target, observed UI, and limitations.

## Future Android Build Gate If Approved

Android build work requires explicit approval. No APK/AAB/native-folder work is included by this test plan.

## Forbidden-Scope Scan

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail\|analytics" -n apps || true
```

Classify hits as allowed warning/blocked-scope text or forbidden implementation.

## Lockfile Contamination Scan

```bash
grep -R "applied-caas\|internal.api.openai.org\|sandbox\|localhost\|127.0.0.1" -n apps/mobile/package-lock.json || true
```

If any hit appears, do not commit the lockfile.

## Claim-Level Review

Map every readiness or release claim to the claim-level system before reporting it.

## Risk-Register Review

Confirm current risks are active or resolved by evidence before milestone acceptance.
