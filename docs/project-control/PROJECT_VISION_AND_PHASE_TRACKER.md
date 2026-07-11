# ContractorOS Project Vision and Phase Tracker

Purpose: preserve the original ContractorOS product vision, track phase alignment, and prevent memory drift, fake progress, overclaims, or scope confusion.

This file is a project-control anchor. It does not prove implementation. Implementation is proven only by GitHub source files, PRs, phase reports, command outputs, runtime evidence, build evidence, and verified main-branch state.

Current product/development source-of-truth is owned by `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`. This tracker preserves vision and phase history and is subordinate to that canonical register for current product/development state.

---

## 1. Original Product Vision

ContractorOS California / California TradeOS is intended to become one modular role-based California contractor, trade, and solar operating-system app.

The long-term product vision is one fixed app shell with role-based modules, role-based downloadable content packs, role-based UI configuration, source-governed updates, and versioned publishing.

The first controlled implementation lane is the internal Phase One testing scaffold.

The first controlled content domain is Law & Business.

C10, C46, and C39 are part of the broader CSLB exam-prep vision, but they are not current public/production content scope until separate content/currentness gates are approved.

Future role/module categories may include:

- CSLB exam prep: Law & Business, C10, C46, C39
- solar incentive and financing copilot
- California contractor code and utility watch
- homeowner / home energy analysis tools
- government contracting radar
- future solar EPC proposal / readiness tools
- admin/editorial command center
- AI source-watch and content-update pipeline

These future categories are roadmap categories only.
They are not current implementation scope.
They do not authorize backend, Firebase, auth, scoring, readiness, public content, APK, EAS, deployment, production claims, or public release work.

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

## 4K Current State

Phase 4K current source-of-truth is `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md`.

Phase 4K-0 was a control/planning re-entry gate after Phase 4J-5.

Phase 4K-1 was implemented through Issue #29 and PR #30.

Phase 4K-2 was implemented through Issue #32 and PR #33 as runtime smoke-QA feasibility documentation; runtime launch remained blocked.

Issue #34 dependency/lockfile baseline decision work was closed not planned before implementation and is not active scope.

Phase 4K-3 created the canonical product/development register.

Phase 4K-4 documented the dependency/lockfile governance decision. It recommended a later controlled deterministic web lockfile baseline implementation phase, but did not implement that dependency baseline.

Phase 4K-5 is historical blocked-before-mutation dependency/toolchain evidence. Issue #39 is closed/completed and PR #40 merged at `e531c4d8bc1904c231be1f43114f16f652c4ec52` without implementing the dependency baseline.

Phase 4K-6 is historical after PR #42 merged at `4315c943b6210f023849592213882bc8983c31d2`. It records the owner-approved redirect toward approximately 95% workflow/process automation and does not implement automation.

Phase 4K-7 completed through Issue #43 and merged PR #44. Its reviewed head was `a519ef5579c130181ac1b25f74bb48f481478378`, and its merge/current-main SHA is `8d443310cf006b82966163f8e486d1f52d8d4e6c`. Phase 4K-8 is active through Issue #45 and PR #46. Phase 4K-9 through Phase 4K-12 remain planning targets and are not started. The toolchain availability / npm bootstrap governance path is deferred, not rejected.

Phase 4I remains paused and is not authorized for resumption unless a later durable GitHub issue records future authorization.

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
| Phase 4F | Next approved milestone                                             | Owner approval required         | Not started and not authorized unless a future durable issue says so |
| Phase 4J-5 | Red-team operating protocol, state machine, and handoff playbook | PR + project-control docs | Merged at `98cf25ff91e9bd3b852669af32bc2951e958494a` |
| Phase 4K-0 | Product development re-entry scope gate | Issue #27 + project-control docs | Historical control/planning phase |
| Phase 4K-1 | Internal scaffold Product / QA hardening phase | Issue #29 + PR #30 | Merged at `07226b7ebed4661a425aab72799d307df1c296ac` |
| Phase 4K-2 | Internal runtime smoke QA feasibility gate | Issue #32 + PR #33 | Merged at `4bb9fedb5648ea1b7185667948256276ad04d3b9`; runtime launch blocked |
| Issue #34 | Dependency / lockfile baseline decision gate | Issue #34 | Closed not planned before implementation |
| Phase 4K-3 | Product / development source-of-truth reconciliation gate | Issue #35 + PR #36 | Merged at `196a48545285afdf8f5d5bc3f948395a5f289a4d`; created canonical product/development register |
| Phase 4K-4 | Dependency / lockfile governance decision gate | Issue #37 + PR #38 | Merged at `61f5354ea55f7de9d0e88fd82031bacd94a9bf60`; historical decision documentation only |
| Phase 4K-5 | Web dependency / lockfile baseline implementation gate | Issue #39 + PR #40 | Merged at `e531c4d8bc1904c231be1f43114f16f652c4ec52`; blocked-before-mutation evidence and no dependency baseline implementation |
| Phase 4K-6 | Owner-trigger / low-risk lane automation policy gate | Issue #41 + PR #42 | Merged at `4315c943b6210f023849592213882bc8983c31d2`; policy/documentation phase only |
| Phase 4K-7 | Low-risk lane validator / control-gate implementation gate | Issue #43 + PR #44 | Completed; reviewed head `a519ef5579c130181ac1b25f74bb48f481478378`, merged at `8d443310cf006b82966163f8e486d1f52d8d4e6c` |
| Phase 4K-8 | Workflow automation command-pack / operator runbook gate | Issue #45 + PR #46 | Active documentation-only gate; no automation activation or approval reduction |
| Phase 4K-9 through 4K-12 | Intake, closeout, dry-run, and decision planning sequence | Future durable issues required | Planning targets only; not started or authorized by Phase 4K-8 |

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
* no Firebase
* no Airtable runtime
* deployment
* no auth/login/user accounts
* no payments/subscriptions
* scoring
* no readiness
* no pass/fail
* saved progress
* no analytics
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
* future scoring/readiness if approved later
* backend if approved later
* database if approved later
* admin/editorial system if approved later
* future Airtable/editorial bridge if approved later
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
| Dependency-control gate       | Clean dependency/lockfile strategy exists       | Decision in Phase 4K-4; implementation not passed |
| Build artifact gate           | Approved APK/AAB/build artifact exists          | Not passed                             |
| Install gate                  | Artifact installed and launched                 | Not passed                             |
| Content-currentness gate      | Legal/currentness/content review complete       | Not passed                             |
| Public/production gate        | no release readiness proven or approved         | Not passed                             |
| Source-of-truth reconciliation gate | Product/development current-state register exists | Passed by PR #36 merge at `196a48545285afdf8f5d5bc3f948395a5f289a4d` |
| Workflow automation policy gate | Target state, low-risk lane, owner-trigger boundaries, and roadmap are versioned | Phase 4K-7 validator merged through PR #44; Phase 4K-8 documentation gate is active through Issue #45 and PR #46 |

Progress is measured by passed gates, not optimism.

---

## 12. Original Vision Alignment Test

Before approving any phase as complete, answer:

1. Does this phase preserve the long-term one-app modular ContractorOS / California TradeOS vision?
2. Does this phase stay inside the current approved phase scope?
3. Does this phase support the internal ContractorOS testing-system vision?
4. Does this phase preserve Law & Business first?
5. Does this phase keep C10 deferred unless explicitly approved?
6. Does this phase avoid public/exam-ready/production claims?
7. Does this phase avoid unapproved backend/auth/payment/scoring/readiness scope?
8. Does this phase improve product capability or control reliability?
9. Does this phase create any new risk?
10. Are remaining risks documented?

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

`PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` controls current product/development source-of-truth.
