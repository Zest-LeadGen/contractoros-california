# Product / Development Source of Truth

## Register Purpose

This register is the canonical product/development source-of-truth record for ContractorOS California after Phase 4K-3 and is updated by Phase 4K-6 for the owner-approved workflow-automation redirect.

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

Current implemented state is limited to repository source and project-control evidence on main at Phase 4K-6 starting SHA `e531c4d8bc1904c231be1f43114f16f652c4ec52`.

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
- Phase 4K-4 recommends a later controlled deterministic web dependency/lockfile baseline implementation phase as the safest next dependency-governance step.
- Mobile dependency/lockfile baseline implementation remains a later separate candidate after web baseline evidence, because the mobile Expo dependency surface is larger and should not be combined with the first baseline mutation phase.
- Phase 4K-4 does not implement that baseline and does not create or change package manifests, lockfiles, dependency directories, runtime QA, or build artifacts.
- Phase 4K-5 attempted the web dependency/lockfile baseline gate through Issue #39 but is blocked before mutation because required node/npm tooling is unavailable.
- Phase 4K-5 does not implement the web dependency/lockfile baseline and does not create or change package manifests, lockfiles, `.npmrc` files, dependency directories, runtime QA, or build artifacts.
- Issue #39 is closed/completed and PR #40 merged at `e531c4d8bc1904c231be1f43114f16f652c4ec52`; the merge records blocked-before-mutation evidence and no dependency baseline implementation.
- The toolchain availability / npm bootstrap governance path remains valid but is deferred, not rejected, while the workflow-automation path is documented and sequenced.

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
- Phase 4K-6 defines approximately 95% workflow automation as a measurable process target that preserves owner judgment, external red-team separation, branch protection, SHA-bound evidence, and current human approval requirements.
- Phase 4K-6 defines low-risk candidate policy, owner-trigger interruption, fail-closed stop conditions, and planning targets through Phase 4K-12.
- Phase 4K-7 implements the first fail-closed low-risk lane validator and pull-request control-gate integration without activating workflow automation.

Development-model items not proven by durable evidence:

- Any implemented low-risk automation lane or measured reduction in manual owner actions.
- Any auto-merge implementation.
- Any replacement for external red-team review.
- Any durable product/platform decision that exists only in chat memory.

## Active Phase State

Current active phase: Phase 4K-7 - Low-Risk Lane Validator / Control-Gate Implementation Gate.

Active issue: Issue #43.

Starting main SHA: `4315c943b6210f023849592213882bc8983c31d2`.

Prior phase state:

- Issue #32 / Phase 4K-2 is closed/completed.
- PR #33 merged at `4bb9fedb5648ea1b7185667948256276ad04d3b9`.
- Issue #34 is closed/not planned and dependency/lockfile decision work is not active.
- Issue #35 / Phase 4K-3 is closed/completed.
- PR #36 merged at `196a48545285afdf8f5d5bc3f948395a5f289a4d`.
- Issue #37 / Phase 4K-4 is closed/completed.
- PR #38 / Phase 4K-4 merged at `61f5354ea55f7de9d0e88fd82031bacd94a9bf60`.
- Issue #39 / Phase 4K-5 is closed/completed.
- PR #40 / Phase 4K-5 merged at `e531c4d8bc1904c231be1f43114f16f652c4ec52`.
- Issue #41 / Phase 4K-6 is closed/completed.
- PR #42 / Phase 4K-6 merged at `4315c943b6210f023849592213882bc8983c31d2`.
- Issue #43 / Phase 4K-7 is open/active.

## Phase Sequence and Dependency Rules

Phase sequence rules:

- Do not start the next phase until the prior phase is merged, main is verified, and the phase issue is closed.
- Do not resume Phase 4I unless a later durable GitHub issue explicitly authorizes it.
- Do not start dependency/lockfile baseline implementation from Issue #34 because Issue #34 is closed/not planned.
- Do not start dependency/lockfile baseline implementation inside Phase 4K-4 because Phase 4K-4 is decision documentation only.
- Treat Phase 4K-5 as historical blocked-before-mutation evidence; no dependency baseline was implemented.
- The owner-approved immediate path is Phase 4K-7 low-risk lane validator implementation before later automation-command phases.
- Phase 4K-8 through Phase 4K-12 are planning targets only and each requires its own future durable GitHub issue after the prior phase is merged, main-verified, and closed.
- Do not retry dependency resolution, package mutation, lockfile creation, npmrc creation, dependency-directory creation, runtime QA, or build work from Phase 4K-7.
- Do not start Phase 4K-8 inside Phase 4K-7.

Dependency rules:

- Runtime smoke QA remains blocked until a later approved phase supplies a safe dependency baseline path.
- Any package or lockfile mutation requires a Dependency lane or other explicitly approved future phase.
- Any build/distribution work requires a Build / Distribution lane or other explicitly approved future phase.
- Any decision to install, bootstrap, substitute, or rely on a package manager requires a later durable issue, red-team review, and human/write-access approval.

## Deferred Phase Candidates

Deferred candidates are not active scope:

- deterministic dependency baseline implementation;
- toolchain availability / npm bootstrap governance decision;
- Phase 4K-7 low-risk lane validator / control-gate implementation;
- Phase 4K-8 workflow automation command-pack / operator runbook;
- Phase 4K-9 phase intake and Codex handoff automation;
- Phase 4K-10 post-marker checks, merge verification, and issue closeout automation;
- Phase 4K-11 low-risk automation dry run;
- Phase 4K-12 95% workflow automation decision gate, blocked until evidence;
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
- Phase 4K-7 start;
- auto-merge activation.

## Evidence Anchors

- Issue #24 - Red-Team Handoff + Memory Reconciliation Gate.
- Issue #29 - Phase 4K-1 Internal Scaffold Product / QA Hardening.
- Issue #32 - Phase 4K-2 Internal Runtime Smoke QA Feasibility Gate.
- Issue #34 - Dependency / Lockfile Baseline Decision Gate, closed not planned.
- Issue #35 - Phase 4K-3 Product / Development Source-of-Truth Reconciliation Gate.
- Issue #37 - Phase 4K-4 Dependency / Lockfile Governance Decision Gate.
- Issue #39 - Phase 4K-5 Web Dependency / Lockfile Baseline Implementation Gate.
- Issue #41 - Phase 4K-6 Owner-Trigger / Low-Risk Lane Automation Policy Gate.
- PR #30 - Phase 4K-1 merged at `07226b7ebed4661a425aab72799d307df1c296ac`.
- PR #33 - Phase 4K-2 merged at `4bb9fedb5648ea1b7185667948256276ad04d3b9`.
- PR #36 - Phase 4K-3 merged at `196a48545285afdf8f5d5bc3f948395a5f289a4d`.
- PR #38 - Phase 4K-4 merged at `61f5354ea55f7de9d0e88fd82031bacd94a9bf60`.
- PR #40 - Phase 4K-5 merged at `e531c4d8bc1904c231be1f43114f16f652c4ec52`.
- `docs/project-control/phase_4k_1_internal_scaffold_product_qa_hardening_report.md`.
- `docs/project-control/phase_4k_2_internal_runtime_smoke_qa_feasibility_gate_report.md`.
- `docs/project-control/WORKFLOW_AUTOMATION_TARGET_STATE.md`.
- `docs/project-control/LOW_RISK_LANE_POLICY.md`.
- `docs/project-control/AUTOMATION_PHASE_ROADMAP.md`.
- Current source under `apps/web/**` and `apps/mobile/**`.
- Current package manifests under `apps/web/package.json` and `apps/mobile/package.json`.

## Conflict Resolution Notes

Resolved by this register:

- Older roadmap/tracker text that labels Phase 4K-0 as the current re-entry gate is historical and subordinate to this register.
- Older tracker text that says Phase 4K-1 is not started is historical and superseded by PR #30 / Issue #29 evidence.
- Phase 4K-2 is not a runtime pass; it is blocked feasibility evidence from PR #33 / Issue #32.
- Issue #34 dependency/lockfile baseline decision work is closed/not planned and is not active Phase 4K-3 scope.
- Phase 4K-4 uses Issue #37 as the active durable dependency/lockfile governance decision intake and does not resurrect Issue #34.
- Phase 4K-4 recommends a split deterministic baseline path, starting with web dependency/lockfile baseline implementation in a later controlled phase. Runtime QA remains blocked until the relevant baseline is implemented and verified.
- Phase 4K-5 used Issue #39 as its durable web baseline implementation intake and stopped before mutation because node/npm tooling was unavailable. No baseline was implemented.
- Phase 4K-5 is historical after Issue #39 closed/completed and PR #40 merged at the Phase 4K-6 starting main SHA.
- Phase 4K-6 records the owner-approved redirect toward approximately 95% workflow/process automation before the toolchain/npm bootstrap path resumes.
- Phase 4K-7 implements the first validator/control-gate step in the automation sequence, but no low-risk automation lane, approval reduction, or auto-merge is activated by Phase 4K-7.
- Long-term platform architecture categories are roadmap candidates only unless backed by later durable GitHub/project-control evidence.
- The Issue #35 requested owner-trigger semantic category `PRODUCT_SOURCE_OF_TRUTH` is not supported by the current owner-trigger validator category list. Until a later control phase updates the validator, Phase 4K-3 records the source-of-truth concern under supported category `ARCHITECTURE_THRESHOLD` and documents the unsupported semantic category as missing control-script support.

## Open Questions / Missing Durable Evidence

- Whether the owner wants `PRODUCT_SOURCE_OF_TRUTH` added to the machine-checkable owner-trigger category list in a future control phase.
- Which backend/provider architecture, if any, should be selected in a later approved architecture phase.
- Which content-currentness process should govern public Law & Business and future C10/C46/C39 content.
- Which package-manager/toolchain details the later deterministic baseline implementation phase should approve.
- Which future low-risk documentation patterns can be classified deterministically beyond the initial Phase 4K-7 documentation-only pattern.
- What measured dry-run evidence would support the Phase 4K-12 workflow automation decision gate.
- Which runtime QA path should be used after dependency governance is implemented and verified.
- Which build/distribution route, if any, should be used after runtime and install gates are approved.

## Validation Tasks

Current validation tasks for Phase 4K-7:

- verify starting main SHA `4315c943b6210f023849592213882bc8983c31d2`;
- verify Issue #43 open, Issue #41 closed/completed, and PR #42 merged;
- verify changed files stay inside the Issue #43 implementation and project-control allowlist;
- run changed-file, forbidden-scope, required-control-update, PR-contract, owner-trigger, low-risk lane self-test, low-risk lane local evidence, lockfile-only, claims-only, and whitespace checks;
- verify no app source, package, lockfile, dependency/toolchain mutation, dependency directory, runtime launch, build, artifact, backend or identity-system implementation, public content, automation activation, Phase 4I, Phase 4K-8, merge, or auto-merge scope is added.

## Maintenance Rule

Future project-control updates must update this register when they change product/development source-of-truth.

Roadmap and tracker files may summarize or link to this register, but they must not reintroduce competing current-state claims.

Historical records should be preserved as evidence, not rewritten into false current-state claims.
