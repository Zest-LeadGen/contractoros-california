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
- Issue #76 requires every substantive active-project red-team response and handoff to end with an explicit next-window navigation block naming the next role, surface, action, direct GitHub targets, independently pasteable AI prompt when applicable, and exact stop conditions.
- The Issue #76 navigation block is navigation only. It creates no implementation, repository-write, review, approval, red-team-decision, merge, closeout, credential, governance-bootstrap, product, production, or next-packet authority and permits no automatic continuation.
- Repository tests may protect committed handoff templates, generated prompts, startup guidance, and project-control artifacts from silent drift, but cannot inspect or technically enforce every private ChatGPT response; live compliance remains behavioral.
- The canonical final response order is exactly: product development stage; current lifecycle table; interactive chart or compact fallback when required; exact next-window navigation block as the absolute final response element.
- The chart or compact fallback is penultimate. The navigation block is the sole absolute final response element, and nothing follows navigation.
- The chart or fallback may be omitted only under the documented compact path. Active project work still requires the explicit final navigation block.
- The navigation block remains `NAVIGATION_ONLY`, creates no authority, and authorizes no automatic continuation.
- R1 review of PR #77 at `486a55dd17b578ad2dcbee1f05debb5337e7a32c` found the initial implementation internally contradictory and returned `CHANGES_REQUESTED` through `R1-OUTPUT-ORDER-001` and `R1-STATE-002`.
- Documentation scope: Issue #76 comment `4984310758` authorizes one bounded ten-file correction; the resulting exact PR head requires a fresh independent whole-PR exact-SHA review before any later gate.
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

## Post-H0 Durable State Reconciliation Decisions — 2026-08-08

- Documentation scope: record the durable H0 closeout. Live GitHub evidence shows Issue #82 closed completed 2026-07-31T23:26:41Z, Issue #67 closed completed 2026-07-31T23:30:36Z, and PR #84 merged at main `5ce15a55fb8dcfc3c68a7631999a22c3df569659`. H0 is closed; this record creates no new authority.
- Documentation scope: record that the inert governance root bootstrap commit ("bootstrap(h1): create inert ContractorOS governance root") was pushed to `Zest-ContractorOS/contractoros-governance` on 2026-08-01T00:11:50Z, consistent with the minimal-inert-trust-root decision above. The governance repository is no longer empty. No governance-repository mutation authority is granted by this record.
- Documentation scope: record planning reservation Issue #85 (post-H10 identity, user-account, progress, and account-security sequence), opened 2026-08-01, planning-only, with no implementation, product-restart, or production authority.
- Refresh `docs/project-control/state/contractoros-state.yaml` to the live-verified snapshot of 2026-08-08. Snapshot semantics remain observed-snapshot-requires-live-verification; the file grants no authority.
- The H1-B1A-G local review packet R11 remains local evidence only. A technical command-sequence verification was performed on 2026-08-08 by a non-independent session agent under direct owner instruction; it is recorded as advisory verification, not as the independent semantic review, and grants no implementation, publication, or GitHub-mutation authority. The owner authorization decision for H1-B1A-G remains separate and open.
- The PR #9 terminal disposition (`CLOSE_AFTER_DEPENDENCY`) dependency is now satisfied by the merged and main-verified disposition report; the separate owner closure decision for PR #9 remains open and is not made by this record.

## Throughput Reform and Web CI Baseline Decisions — 2026-08-08

- Owner decision (Issue #89, owner decision record comment): adopt risk-proportional review depth (T1). Documentation-only and contained-in-repo changes within the Low-Risk Lane policy boundaries receive one review pass plus owner approval; iterative multi-round adversarial review is reserved for authority-model, validator, workflow, dependency/lockfile, and release-claim changes.
- Owner decision (Issue #89): adopt the weekly verified-increment rule (T3), effective at H1 closeout. Every calendar week must land at least one merged, main-verified increment; a week with none triggers a mandatory owner review of the blocker.
- Owner decision (Issue #89): batch H2+H3 and H4A+H4B as single milestones (T4), consistent with the controlled-milestone model.
- Owner decision (Issue #89 plus premise-correction record): complete the Phase 4K-5 blocked lockfile work and add hosted web CI (T2). Live verification showed no lockfile existed on main and apps/web dependencies were floating on "latest"; this phase pins exact versions (react 19.2.8, react-dom 19.2.8, vite 8.2.1, @vitejs/plugin-react 6.0.5), commits apps/web/package-lock.json generated against https://registry.npmjs.org/, and adds .github/workflows/web-ci.yml running registry provenance check, npm ci from the lockfile, lockfile-drift check, build, and output sanity check.
- Dependency provenance: public npm registry only; no .npmrc is committed; install scripts on the local machine are restricted by the owner's allow-scripts allowlist. This decision grants no production, release, publication, or app-store authority.

## H1-B1A-G Completion and Program Records — 2026-08-08

- Documentation scope: H1-B1A-G is implemented and merged. Stage A (child issue #92, Issue #58 linkage 5227895582, SHA-verified readbacks) and Stage B (owner activation 5227965188; atomic commit ed37038 of the 11 sealed corpus files; governance PR #1; PR-body readback SHA match; code-owner approval; owner squash merge) completed with mutation counts exactly as authorized. Verified governance main: 81b79bd8be00116af5ae745eedf064c677622491.
- Premise discipline record (documentation scope): one pre-execution premise drift (PR #90 merged before the Stage A authorization posted) was detected by preflight, stopped on, and resolved only by owner lock amendment 5227871291. Zero drift during execution.
- Owner decision (Issue #85 comment 5228047389): CRM/user-account work, including planning, waits for the H10 restart decision. Repetition of the request does not constitute authorization.
- Issue #89 closed: T2 delivered (PRs #90/#91 merged; first web-ci run on main succeeded), T1/T3/T4 policies recorded. The weekly verified-increment rule activates at H1 closeout.
- Execution-model record (documentation scope): all owner-authority acts today (merges, authorizations, activation, code-owner approval) were executed by the owner in the terminal; session-agent both-keys approvals on product-repo PRs carry disclosed non-independence per the owner-selected flow.

## H1-B1A-P Sanitation Decisions — 2026-08-08

- Owner decision H1B1-OD-007 (documentation scope, resolved by the Issue #96 phase authorization): sanitize historical report text in the current tree by token replacement (<OWNER_HOME>, <TEMP_DIRECTORY>) per SAN-001; original bytes remain accessible through prior SHAs per SAN-006; no deletion, no history rewrite.
- Owner decision H1B1-OD-008 (documentation scope, resolved by the Issue #96 phase authorization): sanitation covers main only; the three preserved non-main branches remain untouched historical evidence under SAN-003/004/005.
- Sequence-deviation record (documentation scope): gates H1_B1C and H1_B1B_G were executed before H1_B1A_P under explicit owner continuation instructions of 2026-08-08, deviating from the H1B1-GATE-001 canonical order; the deviation is owner-accepted and disclosed on Issue #96. Remaining gates resume canonical order: B1B_P, B2, B3, B4, B5.
- Exemption record: the single /Users/example synthetic fixture value in scripts/continuity/tests is classified EXEMPT in the sanitation manifest and unchanged.

## H1 Mid-Program Reconciliation Records — 2026-08-08

- Documentation scope: durable records for three gates completed after the #93 reconciliation. H1-B1C (issue #94; governance PRs #2+#3; verified enforcement run 31281051270 on main 952a383; latent B1A-G defect fixed: 11 corpus entries reconciled PROPOSED→EXISTS; zero-external-action workflow after the sha-pinning policy correctly refused tag-pinned actions). H1-B1B-G (issue #95; governance PR #4; four provider-neutral AI contracts + closed schema at main e907a76; corpus at 25 entries, corpus_version 1.2.0). H1-B1A-P (issue #96; PR #97; sanitation manifest, 10 occurrences tokenized, validator companion rule; owner resolutions OD-007/OD-008).
- Audit-provenance decision (documentation scope): the hourly independent grounding audit found the #85 CRM-gating record was collaborator-authored; owner ratification 5228512217 (Zest-LeadGen) supersedes it and ratifies the #88/#89 session records. Standing rule adopted: owner-decision records are posted from the owner account or explicitly ratified by one.
- Sequence record (documentation scope): gates completed to date — B0, B1A_G, B1A_P, B1B_G, B1C; the GATE-001 deviation (B1C and B1B_G before B1A_P) is owner-accepted per the #96 authorization; remaining gates B1B_P, B2, B3, B4, B5 proceed in canonical order, each on separate owner authorization.

## H1-B1B-P Contract Consumption Decisions — 2026-08-08

- Documentation scope: the product repository consumes the verified governance AI contracts by exact-SHA pin (e907a76f1297e3541672de2424ed2984b03cf0d1, corpus_version 1.2.0) plus per-file SHA-256 digests; contract text duplication and parallel formats are prohibited; the pin advances only by owner decision (H1B1-GATE-006).
- Owner decision H1B1-OD-011 (documentation scope, resolved by the Issue #99 phase authorization): candidate controlled-surface classes recorded (CLI wrapper, MCP service, web console); binding runtime selection deferred to the Phase 4K-9 era.
- Owner decision H1B1-OD-019 (documentation scope, resolved by the Issue #99 phase authorization): the 4K-9 consumption mechanism is the exact-SHA pin plus digest verification created in this phase, satisfying the H1B1-4K-001 pin requirement without granting 4K-9 any start authority.
- Enforcement boundary (H1B1-OUT-014, documentation scope): official output enforcement exists only through controlled surfaces; derived status blocks create no authority; CI wiring of the consumption check is deferred to H1_B4 by design.

## H1-B3 Observation Mode Decisions — 2026-08-08

- Documentation scope: observation mode is active per the governance OBSERVATION_MODE policy (governance PR #6 lineage): three B4 enforcement candidates are measured, never blocking, until the B4 intake re-measurement. The product observe-only workflow runs the contract-consumption live check under continue-on-error and records outcomes as observation evidence.
- Owner decision H1B1-OD-015 (documentation scope, resolved by the Issue #102 phase authorization): observation window = the 2026-08-08 baseline plus continuing passive observation until B4 intake; sample threshold = 30 hosted runs (baseline: 39); accepted limits = zero unremediated false-positive classes and zero known false negatives at B4 intake re-measurement.
- Measured baseline record (documentation scope): 39 hosted runs on 2026-08-08 classified — six true-positive classes (all correct blocks, all remediated by content fixes), one false-positive class (sanitation structural gap, remediated same day by the PR #97 validator companion rule), two infrastructure startup failures (remediated same day by the zero-action workflow), zero known false negatives.

## B4-Intake Re-Measurement Finding — 2026-08-09

- Observation-mode finding (documentation scope): the B4 intake re-measurement per OD-015 found a second false-positive class, FALSE_POSITIVE_PUSH_CONTEXT_CONTRACT_CHECK — the PR-contract completeness step ran on push events, where no PR body can exist, failing every main push since 2026-07-09 (28 consecutive hosted runs). Classified as a systemic false positive; per the OD-015 zero-unremediated-FP limit, B4 cutover is blocked until this remediation is merged and a main push runs green.
- Remediation (documentation scope): condition the step on pull_request events, matching the existing pattern of the marker and owner-trigger steps in the same workflow. The claims-only step already applies to reports on both events and is unchanged.

## FP Remediation R2 — Sequential Unmasking Record — 2026-08-09

- Documentation scope: the first push-context remediation (PR #104) was incomplete because GitHub Actions aborts later steps after a failure — the Claim-language step (same PR-semantics class) was masked by the completeness step on every prior push and surfaced only after the first fix merged, failing identically on main push 7e3e727. R2 conditions the Claim-language step on pull_request events, completing the class. A full step-condition audit confirms every remaining unconditioned step passed on the 7e3e727 push (push-safe by evidence, not assumption).
- OD-015 status (documentation scope): FALSE_POSITIVE_PUSH_CONTEXT_CONTRACT_CHECK remains the open class until the first green control-gates run on a main push after the R2 merge; B4 remains blocked until then.

## H1-B4 Enforcement Cutover Decisions — 2026-08-09

- Documentation scope: the contract-consumption live check becomes a blocking step in the control-gates workflow (push-safe by design: requires no PR context). The B3 observe-only workflow is retired in the same change — its purpose completed at cutover; its observation run history remains durable in the Actions log. This is a recorded supersession, not silent removal.
- Owner decision H1B1-OD-016 (documentation scope, resolved by the Issue #106 phase authorization): rollback = owner-only deletion/disable of the B4 rulesets, recorded on #58 within one cycle; break-glass = no non-owner bypass ever, owner bypass only with a durable prior record naming scope and reason; workflow-step rollback is an ordinary control-lane PR.
- Required-check attachments (documentation scope): additive rulesets on both repositories (governance "Corpus validation + full-tree scan"; product "contractoros-control-gates") are owner console/API acts executed under the same phase authorization; the attachment record lives in the governance repository (H1_ENFORCEMENT_ATTACHMENT, corpus v1.5.0).

## B2/B3 Durable Records + Audit Reconciliation — 2026-08-09

- Audit response (documentation scope): the hourly independent audit correctly found the committed snapshot stale and B2 absent from the registers; this commit reconciles both inside the B4 delivery cycle, per the audit's before-further-gate-work recommendation.
- H1-B2 durable record (documentation scope): 15-probe adversarial suite vs immutable expected oracle merged as governance PR #5 (squash) at verified governance main 7a04ec018eed1f08916f7bdfce050c5e89de5736; DEFECT_1-4 regressions covered; tampered-oracle meta-negative proven; corpus 29 entries v1.3.0; issue #101 closed with completion record.
- H1-B3 durable record (documentation scope): observation-mode policy + immutable 39-run baseline merged as governance PR #6 at ae628f4 (corpus 30 v1.4.0); observe-only workflow merged as PR #103; OD-015 resolved (authorization 5229225607); push-context FP class remediated in two audited rounds (PRs #104/#105, sequential unmasking documented) and verified by run 31289564636 — the first green control-gates main push since 2026-07-09; issue #102 closed.

## H1-B5 Closeout Decisions — 2026-08-09

- Documentation scope: the final H1 lineage review is compiled as H1_CLOSEOUT_LINEAGE.md — every gate's merge SHA, run ID, authorization comment ID, corpus version step, and cross-cutting record (independent-audit interventions, sequence deviation, defect regressions) in one reviewable table. H1_OPERATIONAL=YES is asserted only in the post-merge closeout comment on Issue #58, never in committed pre-merge text.
- Rollback proof (OD-016 control test, documentation scope): executed by owner script cycling both B4 rulesets disabled→active with enforcement-state readbacks; the durable readback transcript lands in the #108 completion record. This proves the rollback path without ever leaving enforcement down.
- Scope boundary: H1 closeout does not unfreeze product work, start H2+H3, or create any next-horizon authority; the batched H2+H3 intake requires a separate owner go decision.

## Post-H1 Reconciliation — 2026-08-09

- Audit response (documentation scope): the hourly independent audit's DRIFT-1 (snapshot recorded #58 open / B5 in flight after the owner closeout landed) is the structural self-reference lag pre-disclosed in the B5 delivery; this commit reconciles it. The audit found zero violations and zero material assumptions across the full H1 authority chain.
- R-PROV-001 progress (documentation scope): two consecutive independent audit cycles returned zero provenance findings, meeting the stated resolution condition; the risk record is marked resolved below with the standing owner-account rule remaining in force.
- Program state (documentation scope): H1_OPERATIONAL=YES per the owner record 5229552232; lifecycle is h1_operational; no active gate; H2+H3 batched intake requires a separate owner go decision.

## H2+H3 Product Enforcement Decisions — 2026-08-09

- H3 (documentation scope): PA-0001 is the first machine-readable phase authorization, describing this very milestone's allowlist and validating against the governance schema — the contract dogfoods itself. The default-deny checker resolves authorizations FROM THE PR BASE COMMIT only, so no PR can modify or invent its own authorization (#60 rule 7); deletes and renames are never pattern-authorizable.
- Bootstrap record (documentation scope): the checker denies its own introducing PR (no authorization exists at base yet) — correct default-deny behavior; the first record lands via the pre-H3 route, all later PRs resolve at base. Per OPS-005 the checker enters as a declared command with committed adversarial tests (8/8, including one real bug the suite caught pre-delivery: directory-vs-file ls-tree resolution); CI wiring requires a future authorization because PA-0001 itself forbids workflow changes.
- H2 (documentation scope): product CODEOWNERS assigns all control surfaces to the owner account per the principal matrix and waiver H2-WAIVER-001; the require_last_push_approval ruleset upgrade is an owner companion act.

- Scanner amendment (documentation scope, disclosed, #111): the forbidden-scope 'auth' term now excludes authorization/authority/author(ed) by lookahead — those words are intrinsic control-plane vocabulary since H1 — while authentication-feature terms (auth, oauth, authenticate) still match. Sanity matrix committed in the amendment's review evidence; PA-0001 rule ALLOW-010 covers the change.

## H4A+H4B Decisions — 2026-08-09

- H4A (documentation scope): the control-gates workflow is decomposed into six independent always-run jobs plus one aggregate gate job (context contractoros-control-gates preserved so the existing required check binds to the aggregate). The sequential-unmasking defect class is eliminated structurally: an expected red-team-marker failure can no longer hide any sibling evidence. PA-0002 wires the default-deny phase-authorization check as an observe-only job per OPS-005; CodeQL (javascript-typescript, python) and dependency-review workflows are added with read-only content permissions.
- Explicit H4A deferrals (documentation scope, no silent narrowing): mobile lint/typecheck/bundle validation defers to H5+H6 (mobile has no lockfile yet); web lint/typecheck/unit defer to H6 alongside the first product test suite; deterministic-generation/hash tests exist in the governance repository's own gates; secret-scanning enablement is an owner console act in the H4B key-turn.
- H4B (documentation scope): the product main ruleset gains non_fast_forward and deletion rules and required conversation resolution via the owner companion act; the aggregate-gate context remains the single required status check (path-filtered workflows such as web-ci cannot be required checks without hanging unrelated PRs — recorded as the reason). Bypass remains restricted to the owner-only OD-016 disable-with-record procedure; a live direct-push rejection test provides the #62 negative evidence.
