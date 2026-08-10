# H7A-3 Automated Scanning Evidence — 2026-08-10 <!-- documentation scope -->

Phase issue: #137 (parent #65). Authorization: standing H7A phase authorization issue-137-comment-5238006617; this PR under PA-0023 (bootstrap closing PA-0020). All reads captured at second precision per R-STRESS-005.

## 1. Dependabot configuration

`.github/dependabot.yml` added: npm ecosystem for `/apps/web` and `/apps/mobile`, github-actions ecosystem for `/`, weekly schedule, open-pull-requests-limit 2 per ecosystem. Governance posture recorded in the file itself: Dependabot PRs are ADVISORY SIGNALS — they cannot pass the default-deny wall (no PA record) and cannot merge (owner-only); real dependency changes ride authorized dependency-lane PRs under the H6 exact-pin + lockfile-digest baseline.

**Function evidence:** Dependabot alerts were already live pre-config (three open alerts, readable feed — H7A-1 inventory §4; R-DEP-SEC-001). Version-update function evidence (first Dependabot-authored PR or a zero-update log entry) is PENDING the first scheduled run after merge — recorded as pending, not claimed. To be captured at the next phase boundary alongside the R-DEP-SEC-001 revisit.

## 2. Dependency-review workflow (re-add)

`.github/workflows/dependency-review.yml` added: `actions/dependency-review-action` pinned to full commit SHA `a1d282b36b6f3519aa1f3fc636f609c47dddb294` (release v5.0.0, tag resolved live 2026-08-10), `fail-on-severity: high`, minimal `permissions: contents: read`, `timeout-minutes: 10`, concurrency group, and NO checkout step (the action reads the dependency diff via the API and needs no repository contents; Opus 5 round 1 caught an unnecessary tag-pinned checkout in the draft — removed, so the file's sole ref is SHA-pinned). Scoped claim: hardening of the four existing workflows is H7A-4. History: originally added in H4A (50c4d50), dropped as premature (c78dcfe) before the Dependency Graph existed; the graph is verified enabled (H7A-1 inventory: SBOM readable), so the precondition now holds. This workflow runs on every PR; it is not yet a required ruleset context (owner ruleset act, considered at H7A-5 closeout).

## 3. Secret scanning and push protection (L-1 closure path)

Prior state: NOT_PROVEN behind admin-only endpoints (H7A-1 limitation L-1). Owner setting authorization staged per the PVR precedent; owner-run enable + read-back records the verified state here:

- Authorization comment: PENDING_OWNER_POST at PR-open time (this line is updated with the comment id and read-back values when the owner key-turn executes; if it executes before merge, the verified state replaces this pending marker in a head-updating commit).

## 4. Private-data / credential-pattern scan (executed)

Method: one-time evidence scan over the 258 tracked files at base 1f67dc9 (`git ls-files`; 257 text-scanned, 1 binary skipped — classified below) with nine pattern classes: private-key blocks, AWS access keys, GitHub token formats (ghp/gho/ghu/ghs/ghr/github_pat), Slack tokens, Google API keys, JWT triplets, credentials-in-URL, generic secret assignments, personal-email addresses. Scan executed 2026-08-10T19:04:50Z from the PR worktree. The five files this PR adds were not in that base scan; Opus 5 round 1 independently re-scanned the full 263-file HEAD tree with a 13-class superset and found no additional hit.

Skipped binary, classified (Opus 5 round-1 finding, not silently skipped): `scripts/control/__pycache__/check_forbidden_scope.cpython-314.pyc` — committed compiled bytecode of the forbidden-scope checker, tracked despite the `.gitignore` `__pycache__/`/`*.pyc` rules; pre-existing at origin/main; `scripts/**` is PA-0023-forbidden so removal is routed to H7A-4 (workflow/control hardening lane).

Result: **1 raw hit, 0 real findings.**

| Hit | Classification |
| --- | --- |
| `scripts/continuity/tests/test_red_team_continuity.py:2011` — `https://user:secret@github.com/...` | BENIGN TEST FIXTURE: the negative test `test_embedded_remote_credentials_are_rejected` proves the continuity collector raises `UnsafeEvidenceError` on embedded remote credentials. Synthetic value; the control working as designed. |

No private keys, tokens, API keys, JWTs, personal emails, or secret assignments in the tracked tree. The scan script itself is not committed (one-time evidence run; method fully recorded above; a recurring CI scan is H7A-4/H7B scope where workflow/control-script changes are in lane).

## 5. Delta from H7A-1 baseline

| #65 control | H7A-1 state | After this PR |
| --- | --- | --- |
| Dependabot config | ABSENT | PRESENT (advisory-signal posture) |
| Dependency-review workflow | ABSENT (dropped c78dcfe) | PRESENT, SHA-pinned, hardened |
| Secret scanning / push protection | NOT_PROVEN (L-1) | Owner key-turn staged; state recorded on execution |
| Private-data scan | Not executed | Executed clean (1 benign fixture classified) |
| SHA pinning (all workflows) | 0 of 15 refs | New workflow born pinned; remaining refs are H7A-4 |
