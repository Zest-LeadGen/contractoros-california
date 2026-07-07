# ContractorOS Project Vision and Phase Tracker

Purpose: preserve the original ContractorOS product vision, track phase alignment, and prevent memory drift, fake progress, overclaims, or scope confusion.

This file is a project-control anchor. It does not prove implementation. Implementation is proven only by GitHub source files, PRs, phase reports, command outputs, runtime evidence, build evidence, and verified main-branch state.

---

## 1. Original Product Vision

ContractorOS California is intended to become a controlled contractor exam/testing and training operating system for California contractor exam preparation.

The project begins with an internal Phase One testing-system scaffold.

The first approved exam domain is Law & Business.

C10 Electrical is deferred until a separate explicit approval/currentness/safety gate.

The system must grow through verified phases and evidence gates, not assumptions, memory, or fake MVP claims.

---

## 2. Product Identity

Project name: ContractorOS California

Product identity: internal contractor exam/testing and training system scaffold

Current broad objective: build a controlled internal testing foundation before any public, production, app-store, backend, scoring, readiness, or full Question Bank claim is allowed.

Primary initial domain: Law & Business

Deferred domain: C10 Electrical until approved gate

Primary internal platforms:

* web internal local scaffold
* mobile Expo internal scaffold

---

## 3. Source of Truth Hierarchy

Use this order when project state is unclear:

1. GitHub main branch.
2. GitHub PR metadata.
3. GitHub changed-file list.
4. GitHub file contents.
5. Project-control reports.
6. Development ledger.
7. Risk register.
8. Decision log.
9. Artifact index.
10. Google Drive artifact references, only for ZIP/binary/archive files.
11. Chat memory only as a pointer, never as source of truth.

Local files are temporary scratch/testing only unless promoted into GitHub or indexed as an approved artifact.

---

## 4. Current Phase Model

ContractorOS development uses controlled milestone development.

Each milestone must declare one lane:

* Product
* QA
* Control / Infrastructure
* Dependency
* Build / Distribution
* Content
* Release

A phase is not complete when a PR opens.

A phase is complete only when:

1. PR is reviewed.
2. PR is approved.
3. PR is merged.
4. Main is verified.
5. Forbidden paths are checked on main.
6. The next phase is explicitly allowed.

No verified main = no next phase.

---

## 5. Phase Map

This phase map is a tracking structure. It is not proof that every item is complete.

| Phase    | Purpose                                                             | Status Source                   | Completion Evidence                         |
| -------- | ------------------------------------------------------------------- | ------------------------------- | ------------------------------------------- |
| Phase 3A | Local web MVP shell / source import                                 | PR + phase report               | Merged PR and verified main                 |
| Phase 3B | QA/build hygiene patch                                              | PR + phase report               | Merged PR and verified main                 |
| Phase 3C | Reproducibility / lock strategy documentation                       | PR + phase report               | Merged PR and verified main                 |
| Phase 3D | Manual web UX QA report                                             | PR + phase report               | Merged PR and verified main                 |
| Phase 4A | Mobile prototype path decision                                      | PR + phase report               | Merged PR and verified main                 |
| Phase 4B | Expo mobile scaffold planning                                       | PR + phase report               | Merged PR and verified main                 |
| Phase 4C | Internal Expo mobile scaffold                                       | PR + source inspection + report | Merged PR and verified main                 |
| Phase 4D | Expo mobile runtime smoke QA                                        | PR + command evidence + report  | Merged PR and verified main                 |
| Phase 4E | Project-control foundation, role boundaries, and red-team structure | PR + docs inspection            | Not complete until merged and main verified |
| Phase 4F | Next approved milestone                                             | Owner approval required         | Not started unless explicitly authorized    |

This table must be updated after each completed phase.

---

## 6. Phase One Definition

Phase One is the internal ContractorOS testing-system MVP / scaffold.

Phase One is:

* internal-only
* fixture/local-only
* Law & Business first
* not public
* not exam-ready
* not production-ready
* not app-store-ready
* not APK-ready unless later proven
* no readiness claim
* no pass/fail claim
* no public MVP claim

Phase One is allowed to prove internal scaffold behavior only.

---

## 7. Phase One In-Scope Items

Current Phase One scope may include:

* web internal shell
* mobile internal scaffold
* local fixture interaction
* internal warnings
* Law & Business fixture focus
* C10 deferred/blocked state
* source-level QA
* command-level QA
* project-control reports
* development ledger
* risk register
* decision log
* artifact index
* role boundaries
* red-team review structure
* claim/release gate controls
* known gaps and non-goals

---

## 8. Phase One Out-of-Scope Items

The following remain blocked unless explicitly approved:

* backend
* database
* Firebase
* Airtable runtime
* deployment
* auth/login/user accounts
* payments/subscriptions
* scoring
* readiness
* pass/fail
* saved progress
* analytics
* public MCQs
* Question Bank migration
* C10 public content
* EAS
* APK
* AAB
* iOS build
* android/
* ios/
* app-store material
* public launch
* marketing/public launch material

---

## 9. Long-Term Project Categories

These are future planning categories, not implementation proof:

* exam domain structure
* Law & Business content governance
* C10 content governance if approved later
* source/claim governance
* question bank governance
* internal testing workflow
* user progress if approved later
* scoring/readiness if approved later
* backend if approved later
* database if approved later
* admin/editorial system if approved later
* Airtable/editorial bridge if approved later
* deployment if approved later
* app build/distribution if approved later
* monetization if approved later

No long-term category becomes active implementation scope without explicit approval.

---

## 10. Phase Closeout Review

At the end of every full phase, red-team must answer:

1. What was the approved phase scope?
2. What branch and PR implemented it?
3. What was the base SHA?
4. What was the head SHA?
5. Was the PR merged?
6. What is the merge commit SHA?
7. Was main verified after merge?
8. What files changed?
9. Did changed files match the allowlist?
10. Was app source changed?
11. Was dependency/build/native scope changed?
12. Were forbidden paths absent?
13. What claim level is supported?
14. What risks remain active?
15. What risks were resolved by evidence?
16. Did this phase advance the original product vision?
17. Did this phase only improve controls?
18. Is the next phase allowed or blocked?

---

## 11. Total Project Development Tracking

The project should not be tracked by vague percentage claims.

Track by gates instead:

| Gate                          | Meaning                                         | Status                                 |
| ----------------------------- | ----------------------------------------------- | -------------------------------------- |
| Foundation control gate       | Project-control structure exists                | Pending until merged and main verified |
| Internal web scaffold gate    | Web scaffold exists and is internally scoped    | Evidence required from main            |
| Internal mobile scaffold gate | Mobile scaffold exists and is internally scoped | Evidence required from main            |
| Command smoke gate            | Commands prove local startup/build behavior     | Evidence required per phase            |
| Visual QA gate                | UI visually inspected in target                 | Not passed until documented            |
| Dependency-control gate       | Clean dependency/lockfile strategy exists       | Not passed                             |
| Build artifact gate           | Approved APK/AAB/build artifact exists          | Not passed                             |
| Install gate                  | Artifact installed and launched                 | Not passed                             |
| Content-currentness gate      | Legal/currentness/content review complete       | Not passed                             |
| Public/production gate        | Release readiness proven and approved           | Not passed                             |

Progress is measured by passed gates, not optimism.

---

## 12. Original Vision Alignment Test

Before approving any phase as complete, answer:

1. Does this phase support the internal ContractorOS testing-system vision?
2. Does this phase preserve Law & Business first?
3. Does this phase keep C10 deferred unless explicitly approved?
4. Does this phase avoid public/exam-ready/production claims?
5. Does this phase avoid unapproved backend/auth/payment/scoring/readiness scope?
6. Does this phase improve product capability or control reliability?
7. Does this phase create any new risk?
8. Are remaining risks documented?

If the answer to any question is unclear, do not approve completion.

---

## 13. Claim Rule

Use the lowest claim level supported by evidence.

Claim levels:

* Level 0 — Not verified
* Level 1 — Source verified
* Level 2 — Command verified
* Level 3 — Runtime visually verified
* Level 4 — Build artifact verified
* Level 5 — Install/distribution verified

Do not claim:

* ready
* complete
* production-ready
* public-ready
* MVP-ready
* Android-ready
* APK-ready
* app-store-ready
* launch-ready
* fully tested

unless the required evidence exists.

---

## 14. Recovery Rule

If project memory becomes unclear:

1. Stop.
2. Do not approve merge.
3. Downgrade claims.
4. Read this file.
5. Read DEVELOPMENT_CONTROL_MODEL_V3.md.
6. Read ROLE_BOUNDARIES.md.
7. Read PROJECT_SCOPE_BOUNDARIES.md.
8. Read PHASE_ONE_SCOPE.md.
9. Read CLAIM_LEVELS_AND_RELEASE_GATES.md.
10. Read KNOWN_GAPS_AND_NON_GOALS.md.
11. Read RISK_REGISTER.md.
12. Verify GitHub PR metadata and file contents.
13. Resume only from verified evidence.

---

## 15. Final Rule

The original vision controls direction.

GitHub evidence controls truth.

Project-control files control scope.

Risk register controls unresolved problems.

Claim levels control wording.

Verified main controls phase advancement.
