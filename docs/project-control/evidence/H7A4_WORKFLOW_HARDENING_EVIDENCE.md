# H7A-4 Workflow Hardening Evidence — 2026-08-10 <!-- documentation scope -->

Phase issue: #137 (parent #65). Standing authorization: issue-137-comment-5238006617; owner "Go" for H7A-4 recorded in-session after RECON-2 merged and main verified (PR #148 merged 21:14:09Z, main ff2400e, #144 closed) — resumption basis is on-platform and objective (the H7A-4 block condition is satisfied); the in-session instruction concurred but is not load-bearing (R-PROV-001). This PR under PA-0025 (bootstrap closing PA-0023). Scope per owner word: the four existing workflows + the tracked bytecode removal; the routed apps/web/README.md fix was NOT included (owner chose plain "go").

## 1. SHA pin resolution (captured live 2026-08-10T21:25:23Z)

| Action | Tag | Resolution | Commit SHA |
| --- | --- | --- | --- |
| actions/checkout | v4 | lightweight tag → commit | 11d5960a326750d5838078e36cf38b85af677262 |
| actions/setup-node | v4 | lightweight tag → commit | 49933ea5288caeca8642d1e84afbd3f7d6820020 |
| github/codeql-action (init + analyze) | v3 | ANNOTATED tag c3400c2f → dereferenced | c4dd10e44af883a891fe31ced449bcb4a6728b9b |

The annotated-tag dereference matters: pinning the tag object SHA instead of the commit SHA would not resolve (the Opus round-1 review of PR #143 verified the same dereference discipline on the dependency-review pin).

## 2. Before/after ref inventory

Before (H7A-1 baseline + H7A-3): 15 tag-pinned refs across the four pre-existing workflows (checkout ×11, setup-node ×2, codeql-action ×2) + 1 SHA-pinned ref (dependency-review.yml, born pinned in H7A-3). After this PR: **16 of 16 `uses:` refs across all five workflows are full-commit-SHA pinned; zero tag pins remain** (`grep -rn "@v[0-9]" .github/workflows/` returns nothing).

## 3. Hardening matrix (per workflow; no job/step logic changed)

| Workflow | SHA pins | timeout-minutes | concurrency group | persist-credentials: false |
| --- | --- | --- | --- | --- |
| codeql.yml | 3 refs | 30 (analyze) | codeql-* , cancel-in-progress | on its 1 checkout |
| web-ci.yml | 2 refs | 15 | web-ci-* , cancel-in-progress | on its 1 checkout |
| mobile-ci.yml | 2 refs | 15 | mobile-ci-* , cancel-in-progress | on its 1 checkout |
| control-gates.yml | 8 refs | 10 (all 9 jobs) | control-gates-* , cancel-in-progress | on all 8 checkouts |
| dependency-review.yml (H7A-3, unchanged) | 1 ref | 10 | present | N/A (no checkout) |

control-gates.yml caution honored: only mechanical hardening — pins, timeouts, concurrency, credential flags; every job, step, command, needs-list, and aggregate rule is byte-unchanged (the T2 self-modification threat class is why this file is normally PA-forbidden; PA-0025 allowlists it for exactly this mechanical scope under the standing H7A authorization, and the R-STRESS-002 from-main wall copy plus the Opus exact-head review are the checks on this PR itself). All four edited workflows parse-validated locally (js-yaml) before push.

## 4. Tracked bytecode removal

`scripts/control/__pycache__/check_forbidden_scope.cpython-314.pyc` DELETED — committed compiled bytecode of a control checker, tracked in violation of `.gitignore`'s `__pycache__/`/`*.pyc` rules (found by the H7A-3 private-data scan's skipped-binary classification; routed here). The wall supports deletions only via an explicit exact-path rule with change_kind "delete"; PA-0025 carries exactly that rule. No other scripts/** path is touched.

## 5. Concurrency-cancellation disclosure

`cancel-in-progress: true` means a superseded run (new push or PR-body edit) is cancelled rather than completed; required contexts always re-evaluate on the latest run, so no gate weakens. On main pushes, groups are per-ref so successive merges queue/cancel within main only. Recorded, not silent.
