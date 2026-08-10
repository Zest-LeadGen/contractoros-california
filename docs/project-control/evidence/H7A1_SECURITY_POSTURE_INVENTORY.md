# H7A-1 Security Posture Inventory — 2026-08-10 <!-- documentation scope -->

Phase issue: #137 (parent #65). Authorization: issue-137-comment-5238006617 (PA-0019).
All reads below are live GitHub/API/tree reads by the developer executor (danidon-wq) with captured timestamps per R-STRESS-005. Reads at `2026-08-10T08:56:39Z` (API) and `2026-08-10T08:57Z–08:59Z` (tree at main 3310052bd2af774cd124edc41f723c64facb4c10). This document changes no control; it records observed state, disclosed limitations, and the reconciliation #137 requires.

## 1. Repository security configuration snapshot

| Control | Observed state | Evidence basis |
| --- | --- | --- |
| Repository visibility | PUBLIC | `gh api repos/Zest-LeadGen/contractoros-california` `.private=false` |
| Dependency graph | ENABLED | SBOM readable: `dependency-graph/sbom` returned SPDX-2.3 |
| Dependabot / vulnerability alerts | ENABLED (alerts readable) | `dependabot/alerts?state=open` returned 3 alerts (§4) |
| CodeQL code scanning | ACTIVE on default branch | latest analyses 2026-08-10T08:09:37/38Z at commit 3310052 |
| Secret scanning alert feed | NOT_PROVEN — endpoint 404 for executor | `secret-scanning/alerts` HTTP 404; see limitation L-1 |
| Push protection | NOT_PROVEN | admin-only setting; see limitation L-1 |
| `security_and_analysis` settings block | NOT_PROVEN — null for executor | admin-scope required; see limitation L-1 |
| `vulnerability-alerts` toggle endpoint | NOT_PROVEN directly (404) | admin-only endpoint; alert feed readability (above) proves alerts function |
| SECURITY.md | ABSENT | tree read at 3310052 |
| CONTRIBUTING.md | ABSENT | tree read at 3310052 |
| LICENSE | ABSENT — owner decision open in #71 | tree read at 3310052 |
| Dependabot config (`.github/dependabot.yml`) | ABSENT | tree read at 3310052 |
| Dependency-review workflow | ABSENT (history in §5) | tree read at 3310052 |
| CODEOWNERS | PRESENT (`.github/CODEOWNERS`) | tree read at 3310052 |

**Limitation L-1 (disclosed, not guessed):** the executor token (danidon-wq, push:true admin:false) cannot read admin-only security settings (`security_and_analysis`, `vulnerability-alerts` toggle, `secret-scanning/alerts`). These rows are NOT_PROVEN, not absent. Closing L-1 requires either a one-time owner read (key-turn command supplied with the H7A-2+ plan) or acceptance of the executor-visible evidence bounds.

## 2. GitHub Actions workflow audit (tree at 3310052)

Four workflows: `codeql.yml`, `control-gates.yml`, `web-ci.yml`, `mobile-ci.yml`.

| Property | Observed | Assessment |
| --- | --- | --- |
| Top-level `permissions` | All four declare `contents: read`; codeql adds `security-events: write` | MINIMAL — matches #65 requirement; `security-events: write` is required for SARIF upload |
| `pull_request_target` usage | NONE | No misuse surface present |
| Action pinning | 15 `uses:` references, ALL tag-pinned (`actions/checkout@v4` ×11, `actions/setup-node@v4` ×2, `github/codeql-action/init@v3`, `analyze@v3`) | GAP — zero full-SHA pins; H7A-4 scope |
| `timeout-minutes` | NONE in any workflow | GAP — H7A-4 scope |
| `concurrency` groups | NONE in any workflow | GAP — H7A-4 scope |
| `persist-credentials: false` | NOT SET on any checkout | GAP — H7A-4 scope |

## 3. Action-pin inventory (exact, for the H7A-4 pinning PR)

```text
actions/checkout@v4        — 11 occurrences (control-gates ×8, codeql ×1, web-ci ×1, mobile-ci ×1)
actions/setup-node@v4      — 2 occurrences (web-ci, mobile-ci)
github/codeql-action/init@v3     — 1 occurrence (codeql)
github/codeql-action/analyze@v3  — 1 occurrence (codeql)
```

Exact per-line locations are grep-reproducible: `grep -n "uses:" .github/workflows/*.yml` at 3310052. SHA resolution happens in H7A-4 at execution time against live tags — resolving them now would be stale by then (verify-number-freshness rule).

## 4. R-DEP-SEC-001 phase-boundary revisit (due at this boundary; executed)

Read at 2026-08-10T08:56:39Z: `dependabot/alerts?state=open` → **unchanged** from the H6-closeout revisit (2026-08-10T07:51Z): high|image-size, high|image-size, medium|uuid — same three alerts, same packages. Owner acceptance (Q2, dated revisit at each phase boundary) **stands**. Next revisit: next phase boundary (H7A closeout or H7B intake, whichever first).

## 5. Claim-vs-observed reconciliation (required by #137)

Two #118 H6-B plan items are recorded in the intake as planned; observed state at 3310052 shows neither landed. Neither appears in the H6 closeout's delivered list — so this is plan-vs-delivery drift disclosed at the next boundary, not a falsified record:

1. **Dependency-review workflow "re-add":** added in H4A (50c4d50), removed as premature (c78dcfe, "drop premature dependency-review"), never re-added. Now explicit H7A-3 scope.
2. **Pin GitHub Actions to commit SHAs:** not present in any workflow at 3310052 (§2). Now explicit H7A-4 scope.

## 6. Red-team findings classification (AGENTS.md pre-implementation requirement)

- **RT-H0-SEC-001** (ACCEPTED_FOR_ROADMAP): H7A is the roadmap phase addressing it. This inventory documents the baseline it will be measured against. Status untouched — resolution requires the register's supersession contract and owner authority, not this document.
- **RT-H0-SUPPLY-001** (ACCEPTED_FOR_ROADMAP): same treatment; supply-chain scope lands in H7A-3/H7A-4.
- No other register finding is affected by a read-only inventory. No finding is inferred resolved.

## 7. Threat-model cross-reference

The twelve #65 threat classes are assessed against this baseline in `docs/project-control/THREAT_MODEL_H7A.md` (same PR).
