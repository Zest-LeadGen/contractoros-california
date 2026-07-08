# Forbidden Scope Scan Playbook

Purpose: standard negative-scope scans and forbidden path checks.

## App Scan

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail\|analytics" -n apps || true
```

## Mobile Scan

```bash
grep -R "fetch\|XMLHttpRequest\|localStorage\|sessionStorage\|firebase\|airtable\|stripe\|payment\|auth\|score\|readiness\|pass/fail\|analytics" -n apps/mobile || true
```

## Lockfile Contamination Scan

```bash
grep -R "applied-caas\|internal.api.openai.org\|sandbox\|localhost\|127.0.0.1" -n apps/mobile/package-lock.json || true
```

## Forbidden Paths And Scope Terms

```text
apps/mobile/package-lock.json
apps/web/package-lock.json
eas.json
android/
ios/
backend
database
Firebase
Airtable runtime
deployment config
auth/login/user accounts
payments/subscriptions
scoring/readiness/pass-fail
saved progress/analytics
public MCQs
Question Bank migration
C10 public content
ZIP binaries
```

## Classification

- allowed warning text
- allowed documentation reference
- forbidden implementation
- requires patch
