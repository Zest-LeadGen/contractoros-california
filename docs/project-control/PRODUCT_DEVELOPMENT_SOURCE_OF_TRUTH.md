# Product / Development Source of Truth

## Register Purpose

This register is the canonical product/development source-of-truth record for ContractorOS California after Phase 4K-3.

It reconciles the roadmap, phase tracker, development ledger, decision log, risk register, validation tasks, requirements traceability matrix, source register, artifact index, and phase reports into one current project-control anchor.

Historical phase reports remain evidence for their own phases. They do not override this register for current product/development state.

## Source-of-Truth Rule

GitHub main, GitHub issues, GitHub PR evidence, and committed project-control files are source of truth.

Chat memory, sandbox state, assistant memory, connector state, local scratch files, and unversioned notes are not source of truth.

If an approval, scope change, platform decision, development-model decision, future operating rule, or closeout is not recorded in GitHub/project-control evidence, it is not durable and must be treated as not proven.

## Product Vision

ContractorOS California / California TradeOS is intended to become one modular, role-based California contractor, trade, and solar operating-system app.

The long-term vision remains one fixed app shell with role-based modules, governed content packs, role-based UI configuration, source-governed updates, and versioned publishing after explicit future approvals.

Current product direction starts with an internal Phase One testing-system scaffold.

Law & Business remains the first controlled domain.

C10, C46, and C39 remain future/deferred roadmap domains until separate durable GitHub issues and content-currentness/safety gates approve them.

## Current Implemented State

Current implemented state is limited to repository source and project-control evidence on main at Phase 4K-3 intake SHA `4bb9fedb5648ea1b7185667948256276ad04d3b9`.

Implemented source-level surfaces:

- internal web scaffold under `apps/web/src/**`;
- internal mobile Expo scaffold under `apps/mobile/**`;
- fixture/local Law & Business learner flow;
- internal-only warning and blocked-scope copy;
- C10 deferred/blocked source state;
- web claim-governance fixture view;
- mobile local fixture interaction with local feedback display;
- project-control gate scripts and reports.

Current command/runtime evidence:

- Phase 4K-2 classified runtime smoke QA as blocked before runtime launch under no-install/no-mutation constraints.
- No current Phase 4K-3 runtime launch is performed.

Current dependency state:

- `apps/web/package.json` exists and uses `latest` dependency ranges.
- `apps/mobile/package.json` exists and uses `latest` dependency ranges.
- No root package manager entrypoint is present.
- No committed package lockfile exists for web or mobile.
- No committed dependency directory exists for web or mobile.

## Current Non-Implemented / Blocked Scope

The following remain blocked or not implemented:

- public MCQs;
- Question Bank migration;
- public C10/C46/C39 content;
- legal/currentness/content-currentness approval;
- backend;
- database;
- no Firebase implementation;
- no auth/login/user accounts;
- cloud service implementation;
- scoring;
- no readiness;
- no pass/fail;
- saved progress;
- no analytics;
- no payment/subscription;
- CRM;
- marketplace;
- deployment;
- runtime visual QA;
- browser QA;
- emulator/device QA;
- install QA;
- dependency/lockfile baseline implementation;
- Expo/EAS/native build;
- APK/AAB/iOS build;
- app-store material;
- release artifact;
- public launch;
- no production readiness.

## Platform Architecture Decisions

Durable platform decisions supported by current evidence:

- One fixed app shell is the long-term direction.
- Future modules should be added through controlled modules, governed content packs, UI configuration, source registries, and approved backend services only after explicit future approval.
- No backend, Firebase, auth, cloud, deployment, analytics, payment, CRM, marketplace, or build/distribution platform is currently approved for implementation.

Platform items not proven by durable evidence:

- Any specific hosted backend provider selection.
- Any final database selection.
- No final auth provider selection.
- Any final deployment provider selection.
- No final analytics provider selection.
- Any final app-store/distribution route.

## Development Model Decisions

Durable development-model decisions supported by current evidence:

- GitHub Issue -> Developer branch -> Pull request -> Control gates -> External red-team decision -> Human/write-access approval -> Merge is the maintained route.
- Codex is developer executor only.
- Codex must not self-review, approve, merge, bypass branch protection, or add `RED_TEAM_DECISION` markers.
- Every phase must link a durable GitHub phase issue.
- Every phase must declare scope, allowlist, forbidden scope, validation evidence, red-team requirement, human approval status, auto-merge status, and next-phase status.
- Auto-merge remains inactive.
- Human approval remains required.

Development-model items not proven by durable evidence:

- Any future low-risk automation lane that reduces human approval.
- Any auto-merge implementation.
- Any replacement for external red-team review.
- Any durable product/platform decision that exists only in chat memory.

## Active Phase State

Current active phase: Phase 4K-3 - Product / Development Source-of-Truth Reconciliation Gate.

Active issue: Issue #35.

Starting main SHA: `4bb9fedb5648ea1b7185667948256276ad04d3b9`.

Prior phase state:

- Issue #32 / Phase 4K-2 is closed/completed.
- PR #33 merged at `4bb9fedb5648ea1b7185667948256276ad04d3b9`.
- Issue #34 is closed/not planned and dependency/lockfile decision work is not active.

## Phase Sequence and Dependency Rules

Phase sequence rules:

- Do not start the next phase until the prior phase is merged, main is verified, and the phase issue is closed.
- Do not resume Phase 4I unless a later durable GitHub issue explicitly authorizes it.
- Do not start dependency/lockfile baseline implementation from Issue #34 because Issue #34 is closed/not planned.
- Do not start Phase 4K-4 inside Phase 4K-3.
- Future dependency/lockfile baseline decision or implementation work needs a new durable GitHub issue after this reconciliation phase.

Dependency rules:

- Runtime smoke QA remains blocked until a later approved phase supplies a safe dependency baseline path.
- Any package or lockfile mutation requires a Dependency lane or other explicitly approved future phase.
- Any build/distribution work requires a Build / Distribution lane or other explicitly approved future phase.

## Deferred Phase Candidates

Deferred candidates are not active scope:

- dependency/lockfile governance decision after source-of-truth reconciliation;
- deterministic dependency baseline implementation;
- web runtime smoke QA after dependency baseline;
- mobile runtime smoke QA after dependency baseline;
- visual QA;
- device/emulator QA;
- install QA;
- content governance;
- C10/C46/C39 content-currentness gates;
- backend/security architecture decision;
- build/distribution planning;
- future public/release readiness gates.

## Explicit Non-Authorized Scope

This register does not authorize:

- app source edits;
- package or lockfile changes;
- dependency installation;
- runtime launch;
- browser QA;
- emulator/device QA;
- install QA;
- build artifacts;
- Expo/EAS/native build;
- APK/AAB/iOS build;
- app-store material;
- deployment;
- no backend/database/Firebase/auth/cloud implementation;
- no payment/subscription;
- CRM;
- marketplace;
- no analytics;
- saved progress;
- scoring;
- no readiness;
- no pass/fail;
- public content;
- Question Bank migration;
- C10/C46/C39 public content;
- ZIP/binary/archive/Drive artifact;
- Phase 4I resume;
- Phase 4K-4 start;
- auto-merge activation.

## Evidence Anchors

- Issue #24 - Red-Team Handoff + Memory Reconciliation Gate.
- Issue #29 - Phase 4K-1 Internal Scaffold Product / QA Hardening.
- Issue #32 - Phase 4K-2 Internal Runtime Smoke QA Feasibility Gate.
- Issue #34 - Dependency / Lockfile Baseline Decision Gate, closed not planned.
- Issue #35 - Phase 4K-3 Product / Development Source-of-Truth Reconciliation Gate.
- PR #30 - Phase 4K-1 merged at `07226b7ebed4661a425aab72799d307df1c296ac`.
- PR #33 - Phase 4K-2 merged at `4bb9fedb5648ea1b7185667948256276ad04d3b9`.
- `docs/project-control/phase_4k_1_internal_scaffold_product_qa_hardening_report.md`.
- `docs/project-control/phase_4k_2_internal_runtime_smoke_qa_feasibility_gate_report.md`.
- Current source under `apps/web/**` and `apps/mobile/**`.
- Current package manifests under `apps/web/package.json` and `apps/mobile/package.json`.

## Conflict Resolution Notes

Resolved by this register:

- Older roadmap/tracker text that labels Phase 4K-0 as the current re-entry gate is historical and subordinate to this register.
- Older tracker text that says Phase 4K-1 is not started is historical and superseded by PR #30 / Issue #29 evidence.
- Phase 4K-2 is not a runtime pass; it is blocked feasibility evidence from PR #33 / Issue #32.
- Issue #34 dependency/lockfile baseline decision work is closed/not planned and is not active Phase 4K-3 scope.
- Long-term platform architecture categories are roadmap candidates only unless backed by later durable GitHub/project-control evidence.
- The Issue #35 requested owner-trigger semantic category `PRODUCT_SOURCE_OF_TRUTH` is not supported by the current owner-trigger validator category list. Until a later control phase updates the validator, Phase 4K-3 records the source-of-truth concern under supported category `ARCHITECTURE_THRESHOLD` and documents the unsupported semantic category as missing control-script support.

## Open Questions / Missing Durable Evidence

- Which dependency/lockfile governance path should replace the closed/not-planned Issue #34 path?
- Whether the owner wants `PRODUCT_SOURCE_OF_TRUTH` added to the machine-checkable owner-trigger category list in a future control phase.
- Which backend/provider architecture, if any, should be selected in a later approved architecture phase.
- Which content-currentness process should govern public Law & Business and future C10/C46/C39 content.
- Which runtime QA path should be used after dependency governance is approved.
- Which build/distribution route, if any, should be used after runtime and install gates are approved.

## Validation Tasks

Current validation tasks for Phase 4K-3:

- verify starting main SHA;
- verify Issue #32 closed/completed;
- verify Issue #34 closed/not planned;
- verify Issue #35 open;
- verify changed files match the Issue #35 allowlist;
- run changed-file, forbidden-scope, required-control-update, PR-contract, owner-trigger, lockfile-only, claims-only, and whitespace checks;
- verify no app source, package, lockfile, dependency, runtime, build, artifact, backend, cloud, auth, scoring, readiness, pass/fail, analytics, saved-progress, public-content, payment, CRM, marketplace, Phase 4I, Phase 4K-4, merge, or auto-merge scope was added.

## Maintenance Rule

Future project-control updates must update this register when they change product/development source-of-truth.

Roadmap and tracker files may summarize or link to this register, but they must not reintroduce competing current-state claims.

Historical records should be preserved as evidence, not rewritten into false current-state claims.
