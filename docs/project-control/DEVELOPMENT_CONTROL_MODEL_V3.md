# ContractorOS Development Control Model v3

Permanent fallback operating model for ContractorOS California development.

Core controls: controlled milestone development, triple manual red-team verification, automated gates where practical, strict supply-chain controls, claim-level discipline, risk-register discipline, and verified `main` before the next phase.

## 1. Core Operating Principle

No project claim may exceed the evidence in GitHub, project-control files, reports, and approved scope.

## 2. Roles

Developer prepares scoped PRs. Red-team verifies evidence and negative scope. Owner authorizes merge and phase advancement. Control lane maintains ledger, risks, decisions, artifacts, and claim gates.

## 3. Development Model

Branch from verified `main`, change only approved files, open PR, red-team, merge only after explicit approval, verify `main`, then advance.

## 4. Lane Classification

Every phase declares a lane: product, QA, control/infrastructure, dependency, build/distribution, content, or release.

## 5. Mandatory Triple Micro-Check

1. GitHub truth check.
2. Source/report inspection.
3. Negative-scope/repo-pollution check.

## 6. Macro Review

Major milestones also require architecture, claim-level, risk-register, dependency, and phase-sequencing review.

## 7. Claim-Level System

Level 0 — Not verified. Level 1 — Source verified. Level 2 — Command verified. Level 3 — Runtime visually verified. Level 4 — Build artifact verified. Level 5 — Install/distribution verified.

## 8. Developer Evidence Contract

Each PR states branch, base SHA, head SHA, changed files, commands run, outputs or limits, forbidden-scope result, and next allowed step.

## 9. File Allowlist Rule

A phase may change only its approved files. Extra files are blockers unless explicitly approved.

## 10. Dependency and Supply-Chain Policy

No contaminated lockfile may be committed. No package-lock may be committed unless clean public provenance is proven. Dependency additions require explicit approval.

## 11. Runtime, Build, and Distribution Policy

No EAS, APK, AAB, iOS build, native folders, or app-store material without explicit approval.

## 12. Report Quality Standard

Reports must cover scope, starting state, files changed, commands, dependency handling, forbidden-scope scan, exclusions, known issues, and result.

## 13. Forbidden-Scope Scan

App phases must scan for backend, storage, auth, payment, scoring, readiness, pass/fail, persistence, analytics, and similar expansion terms.

## 14. Patch Rules

Patch only the verified blocker or approved control expansion. Do not bundle unrelated work.

## 15. Merge Rules

Do not merge without explicit owner approval after red-team. Merge commit is preferred unless otherwise approved.

## 16. Phase Advancement Rules

No next phase begins until the prior PR is merged and `main` is verified.

## 17. Risk Register

Risks stay active until evidence proves resolution.

## 18. Automated Gates Policy

Automated gates should be added where practical, but manual red-team remains required until automation is verified.

## 19. Recovery Protocol

If project participants drift, overclaim, or lose alignment:

1. Stop and downgrade claims.
2. Re-identify source of truth.
3. Rebuild current state from GitHub, files, reports, and approved scope.
4. Run triple-check:
   - GitHub truth check
   - Source/report inspection
   - Negative-scope/repo-pollution check
5. For major milestones, also run:
   - Macro architecture review
   - Claim-level review
   - Risk-register review
6. Resume only from verified evidence.

## 20. Self-Audit Questions

What evidence supports this claim? Did the branch start from verified `main`? Are changed files allowed? Did forbidden scope appear? Are known gaps documented? Is the next step authorized?

## 21. Final Enforcement Rule

No evidence = no claim.
No clean file proof = no merge.
No verified main = no next phase.
No explicit approval = no scope expansion.

## Red-Team Execution Files

Red-team execution files live under `docs/project-control/red-team/`.

These files operationalize the triple-check, claim-downgrade, main-verification, and recovery process.

They do not define product scope and do not authorize developer implementation work.
