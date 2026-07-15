# ContractorOS Decision Log

Purpose: record durable architectural and process decisions.

## Active Decisions

- GitHub is source of truth for code, PRs, review evidence, and text project-control records.
- Chat memory is not source of truth.
- Codex is developer executor only.
- Red-team remains separate from developer execution.
- Human/write-access approval remains required before merge.
- No auto-merge is permitted.
- No branch-protection bypass is permitted.
- No paid API, paid services, hosted bots, hosted CI, or hosted tools may be added in Phase 4J-0.
- No unrelated Claude-imported Codex project context may be used as ContractorOS evidence.
- No unrelated hooks may be trusted; cockroachdb hooks must not be used.
- No broad connector discovery, broad list-resource calls, or tool-schema dump calls are permitted.
- If direct tools are unavailable, the developer executor must stop instead of discovering tools broadly.
- Future Phase 4J-2 must make red-team decisions GitHub artifacts tied to the exact PR head SHA.
- 95% automation means reducing relay, paperwork, repetitive checks, and handoff, not removing owner judgment.
- Assumptions, design decisions, sources, model runs, validation tasks, and originality requirements must be versioned in repo files.
- The developer connector implementation path is currently blocked after repeated api_tool.list_resources violations.
- Bootstrap Codex use for Phase 4J-0 is allowed only because this phase creates AGENTS.md and the AI governance files.
- GitHub is source of truth for code and text project-control records.
- Historical archive assumption: Google Drive was named for archive artifacts. This is superseded by the Issue #58 recovery decision: the GitHub artifact index is authoritative, external archive bytes are non-authoritative, and no archive provider or location is durably selected.
- Local files are temporary scratch/testing only.
- Controlled Milestone Development Model v3 is active.
- Clean public provenance is required before committing lock records.
- Distribution and product-scope expansion require explicit approval.
- DEVELOPMENT_CONTROL_MODEL_V3.md is the fallback development-control anchor.
- PROJECT_FOUNDATION.md is the living project foundation.
- PROJECT_VISION_AND_PHASE_TRACKER.md preserves original long-term vision and phase tracking.
- PROJECT_IMPLEMENTATION_ROADMAP.md preserves long-term implementation architecture without authorizing current scope expansion.
- Future modules remain roadmap categories until explicit approval.
- PHASE_ONE_SCOPE.md controls Phase One scope.
- CLAIM_LEVELS_AND_RELEASE_GATES.md controls claim wording and release claims.
- KNOWN_GAPS_AND_NON_GOALS.md must be checked before readiness, MVP, or public claims.
- Red-team execution files live under docs/project-control/red-team/.
- Red-team files are reviewer/control files.
- Role separation inside this repo is process-based; private review notes require separate access control.
- Product / QA PRs may include exactly one current `docs/project-control/phase_*_report.md` companion report without converting the declared lane to Control / Infrastructure.
- Report-only `docs/project-control/**` PRs remain Control / Infrastructure.
- Non-report `docs/project-control/**` changes remain Control / Infrastructure.
- Maintained route is GitHub Issue → Developer PR → Control Gates → Red-Team Decision → Human Approval → Merge.
- The maintained route reduces owner copy/paste and manual supervision while preserving protected PR governance, red-team accountability, and human approval for major decisions.
- The maintained route does not authorize automated merge, automated approval, direct-to-main work, branch-protection bypass, or scope expansion.
- Red-team decisions must use a `RED_TEAM_DECISION` marker tied to the exact PR head SHA reviewed.
- A red-team approval is stale after any later commit changes the PR head SHA.
- The ContractorOS control-gates workflow requires the SHA-bound red-team marker on pull requests after Phase 4J-3.
- PR body edits rerun the control-gates workflow so a red-team marker can be added after review without using elevated pull request permissions.
- Future PRs must include a machine-checkable `OWNER_TRIGGER_REVIEW` marker before the required pull request control gate can pass after Phase 4J-4.
- Owner-trigger categories other than `NONE` make a PR `NOT_AUTOMATION_ELIGIBLE`.
- Human approval remains required and auto-merge remains ineligible for all PRs after Phase 4J-4 unless a later approved control phase changes policy.
- Future red-team windows must follow committed red-team protocol files and must not rely on chat memory, sandbox state, local scratch files, connector state, or unversioned notes as source of truth.
- Red-team must classify lifecycle state before giving next steps, commands, options, next-phase prompts, or implementation guidance.
- Red-team command guidance must include expected success output, failure indicators, stop conditions, and the next allowed action after confirmation.
- Future red-team responses must include the project progress snapshot unless the response is only a brief acknowledgment or the owner explicitly asks for no progress section.
- The Phase 4J-4 progress snapshot baseline is a governance estimate only and does not make product-readiness, exam-readiness, public-launch, pass/fail, production, build, backend, Firebase, auth, cloud, or distribution claims.
- Phase 4K-0 is a control/planning re-entry gate only and does not authorize product implementation.
- The durable no-memory-only owner directive from Issue #24 applies to Phase 4K-0 and future ContractorOS work: if a material approval, decision, scope, condition, closeout, protocol update, or operating rule is not recorded in GitHub/project-control evidence, it is not durable.
- Exactly one next implementation phase is recommended after Phase 4K-0: Phase 4K-1 - Internal Scaffold Product / QA Hardening.
- Phase 4K-1 must be created as a later GitHub phase issue before implementation and must not begin inside Phase 4K-0.
- Phase 4I remains paused and is not authorized for resumption unless a later durable GitHub issue records future authorization.
- Phase 4K-3 creates `docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` as the canonical product/development current-state register.
- Roadmap, tracker, ledger, decision, risk, validation, traceability, source, artifact, and phase-report records are subordinate to `PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md` for current product/development state after Phase 4K-3.
- Issue #34 dependency/lockfile baseline decision work is closed not planned and must not be treated as active or implemented.
- Dependency/lockfile decision work is deferred until a later durable GitHub issue records scope, allowlist, forbidden scope, validation tasks, red-team requirement, and human approval requirement.
- The Issue #35 requested semantic owner-trigger category `PRODUCT_SOURCE_OF_TRUTH` is not supported by the current machine-checkable owner-trigger validator category list; Phase 4K-3 uses supported category `ARCHITECTURE_THRESHOLD` for machine validation and records the unsupported semantic category as missing control-script support.
- Phase 4K-4 uses Issue #37 as the durable dependency/lockfile governance decision intake and does not resurrect closed/not-planned Issue #34.
- Phase 4K-4 recommends exactly one next controlled phase: deterministic web dependency/lockfile baseline implementation for `apps/web`.
- Mobile dependency/lockfile baseline implementation remains a later separate candidate after web baseline evidence, because combining web and mobile dependency mutation would increase first-baseline blast radius.
- Runtime smoke QA, browser QA, emulator/device QA, install QA, and build/distribution work remain blocked until a deterministic dependency/lockfile baseline is implemented and verified in a later approved phase.
- Package-manager migration, vendored/preloaded dependency directories, and containerized runtime QA are not selected as the immediate next phase because current repo evidence does not prove they are safer or more auditable than deterministic lockfile creation.
- Phase 4K-5 uses Issue #39 as the durable web dependency/lockfile baseline implementation intake, but it is blocked before mutation because required node/npm tooling is unavailable.
- Phase 4K-5 must not install Node/npm, bootstrap npm, use Corepack, substitute pnpm/yarn/bun, use bundled Node without npm for lockfile generation, create lockfiles, edit package manifests, create npmrc files, create dependency directories, run runtime QA, or run builds.
- Issue #39 is closed/completed and PR #40 merged Phase 4K-5 blocked-before-mutation evidence at `e531c4d8bc1904c231be1f43114f16f652c4ec52` without implementing the dependency baseline.
- The owner-approved immediate path is redirected from the toolchain availability / npm bootstrap governance gate to workflow automation policy and sequencing through approximately Phase 4K-12.
- The toolchain/npm bootstrap path remains valid but is deferred, not rejected, and no dependency-resolution retry is authorized by Phase 4K-6.
- Approximately 95% workflow automation is a measurable process target for reducing repetitive relay, issue preparation, Codex handoff, evidence collection, marker coordination, check monitoring, merge verification, issue closeout, and progress updates; it does not grant approval power to remove owner judgment or protected review.
- Current manual relay is estimated at approximately 8-14 owner/collaborator actions per phase.
- Future target ranges are approximately 0-2 owner actions for low-risk documentation/control phases, 2-4 for routine low-risk source-safe patches, and 5-9 owner/human actions for dependency/security/toolchain phases unless later durable policy reduces them.
- Legal, financial, paid-service, public-release, production, app-store/build/distribution, backend or auth security, dependency/security risk acceptance, architecture-threshold, scope-expansion, and high-risk product decisions remain owner/human controlled.
- Any owner-trigger category other than `NONE` is not automation eligible and must interrupt future automation.
- Codex remains developer executor only; external red-team separation, exact PR-head SHA binding, branch protection, and current human approval requirements remain in force.
- Auto-merge remains inactive and prohibited. Any future eligibility requires a separate durable issue, policy approval, implementation, validation, dry-run evidence, required checks, and proof that owner-triggered work cannot enter the lane.
- Phase 4K-7 merged through PR #44, Issue #43 is closed/completed, and the merge/current starting SHA for Phase 4K-8 is `8d443310cf006b82966163f8e486d1f52d8d4e6c`.
- Phase 4K-7 permits `FUTURE_LOW_RISK_CANDIDATE` only when owner interruption is `NO`, trigger categories are exactly `NONE`, human approval remains `YES`, auto-merge remains `NO`, and changed files stay inside the current documentation-only low-risk pattern.
- Phase 4K-7 treats workflow/control enforcement changes, control scripts, dependency/package/lockfile paths, app source, product claims, and owner-triggered categories as not low-risk candidates.
- Historical decision: Phase 4K-8 was active through Issue #45 to document a copy-safe command pack and operator runbook for the protected lifecycle without implementing automation; it is now closed/merged.
- Phase 4K-8 records that safe PR-body marker assembly places `RED_TEAM_DECISION` before the final live `OWNER_TRIGGER_REVIEW` marker and does not put live markers in comments or fenced code.
- Phase 4K-8 supersedes the historical Issue #24 append-only marker procedure with replacement-body assembly that removes stale red-team status and existing owner-marker sections before adding exactly one current-SHA decision and one final owner marker.
- Main branch protection is proven by GitHub repository evidence: strict `contractoros-control-gates`, one approving review, code-owner review, stale-review dismissal, conversation resolution, and admin enforcement are required; force pushes and deletions are disabled; signatures, last-push approval, and linear history are not enabled.
- In the current workflow order, changed-file, forbidden-scope, required-control-update, PR-contract, owner-trigger, and low-risk-lane checks precede the mandatory red-team marker. While that marker is missing, later GitHub lockfile-only and claim-language steps are skipped, so their equivalent local checks remain mandatory.
- Phase 4K-8 preserves manual merge, external red-team, human approval, exact PR-head SHA binding, auto-merge prohibition, and no hidden or chat-only approvals.
- Phase 4K-9 through Phase 4K-12 remain future planning targets. Each must have its own future durable GitHub issue and cannot start inside Phase 4K-8.

## Review Condition

Update decisions through project-control PRs or explicitly approved control milestones.

## Pre-4K-9 Program Constitution Decisions

- Issue #47 owner amendment `4949071184` approves D1–D26 as program direction, not implemented capability.
- The Program Constitution has top-level public-safe direction precedence while phase-specific issues and protected lifecycle gates remain mandatory.
- Canonical public-safe state, append-only decisions, derived startup packets, an unsynced-decision inbox, and a future private plane form the five-layer continuity direction.
- The 95% objective applies only to eligible routine steps; high-impact decisions retain protected human control.
- Zero spend is the default before revenue; only a separately owner-approved bounded paid pilot may be considered.
- Provider policy is evidence-driven and provider-agnostic. UI labels are not official taxonomy without current official evidence.
- Phase 4K-9 remains not started. The read-only continuity collector/startup-packet gate must come first.

## Issue #49 Implementation Decision

- Implement the continuity collector as a Python standard-library-only CLI with fixture and live modes.
- Require an explicit positive command allowlist, argument arrays, `shell=False`, finite timeouts, and bounded parsed evidence.
- Write exactly two derived outputs only to an explicit directory outside the repository.
- Treat every generated packet as derived evidence with no authority by itself.
- Fail closed with `consistent`, `requires_live_verification`, `stale`, `blocked`, or `quarantined` classification and the documented exit contract.
- Do not update canonical state automatically and grant no write, review, approval, merge, release, spending, credential, or policy decision power.

## H1 Recovery Decisions

- Documentation scope: Issue #58 comment `4975617497` is the active H1 recovery authority; Issue #49 is closed and PR #50 merged at `7d00343c233e45185e6c4d77e50eb870f408c01f`.
- Preserve the long-term product direction while freezing product work, blocking production, pausing Phase 4K-9 and downstream progression, and keeping Phase 4I paused.
- Preserve owner decision authority, red-team Lead Engineer/Architect and independent audit duties, Codex developer-executor-only duties, and fresh exact-SHA independent final review as separate roles; this documentation grants no role expansion.
- Reject the complete-first-governance-commit alternative. A future first governance commit must be a minimal inert trust root and requires a separate exact owner authorization.
- Adopt the Epistemic Integrity and Non-Fabrication Standard; no perfect non-hallucination guarantee is claimed.
- Preserve historical evidence, explicitly supersede contradictions, correct stale current state, and prohibit broad deletion in the first reconciliation.
- Make the GitHub artifact index authoritative for identity, accepted hash, classification, status, retention, review, supersession, and storage reference. External archive bytes are non-authoritative and no provider or location is yet selected.
- Withdraw Packet 1E and reject Control Plane Seed v0 and prior local H1 candidates as project authority. Local outputs remain evidence or donor material only; local implementation authority is not authorized.
- Require hook execution by default. Hook bypass is prohibited unless a later exact owner authorization names the command and scope; prior blanket bypass language is superseded.
- Follow recovery order R4 reconciliation, R5 fresh review, R6 owner merge decision, and R7 verified-main durable closeout. No automatic next packet or H1 bootstrap is authorized.
