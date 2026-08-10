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

- H4 correction (documentation scope): dependency-review workflow removed from this PR — it requires Dependency Graph enabled (owner settings act), and shipping an always-red non-required check would recreate the alarm-fatigue antipattern remediated at B3. Enabling Dependency Graph + adding dependency-review is folded into the H4B owner companion acts with the workflow to follow under a later authorization once the setting is on. CodeQL security analysis ships in this PR unaffected.
## Post-H2+H3 Reconciliation + Merge-Actor Accuracy Correction — 2026-08-09

- Audit response (documentation scope): six overnight independent grounding cycles unanimously found the state snapshot stale after PR #112 (H2+H3) merged and confirmed NO live violation. This reconciliation refreshes the snapshot to fabfa8f, records H2+H3 complete and H4A+H4B in flight, backfills the DEVELOPMENT_LEDGER H2+H3 head-SHA placeholder, and issues the accuracy correction below.
- ACCURACY CORRECTION (epistemic-integrity standard, documentation scope): earlier records overstated owner merge authorship. Verified merge actors: PRs #87, #90, #91, #93 were MERGED BY the collaborator account danidon-wq under the disclosed both-keys flow; the owner (Zest-LeadGen) provided the APPROVING review at the exact head in each case. PRs #97 onward were merged directly by Zest-LeadGen. The DECISION_LOG "H1-B1A-G Completion" phrase "all owner-authority acts today ... were executed by the owner in the terminal" and the Issue #85 ratification phrase "my own merges ... of PRs #87/#90/#91" are superseded by this correction: the owner AUTHORIZED and APPROVED those acts; the merge execution actor was danidon-wq under the both-keys flow for that subset. This is an accuracy refinement, not a new authority claim — the both-keys flow was disclosed throughout, and every merge traces to a genuine owner approval at the exact head.
- H4 provenance gate (documentation scope): issue #113 (H4A+H4B intake) currently has no owner-authored authorization comment; PA-0002 correctly marks evidence_id PENDING_OWNER_COMMENT_ON_113. PR #114 must not merge until the owner posts that authorization comment on #113 and PA-0002's evidence_id is updated to it. Recorded as a hard precondition.
## OD-017 — Model pin: Fable 5 only — 2026-08-09 (owner decision)

- Owner instruction (verbatim intent): never run this project on any model other than Fable 5; treat as a hard rule. Trigger: owner observed an "Opus 4.8" label during the 2026-08-09 session.
- Session-side finding (documentation scope): session environment reports model claude-fable-5 for the whole session; all session commits carry the Fable 5 trailer; the "Opus 4.8" string traces to harness boilerplate (default commit-trailer template / fast-mode display label), not a model change. No model switch occurred.
- Enforcement: `.claude/settings.json` pins Fable 5 as the project default (owner-applied via /model, 2026-08-09). Any future session on another model must stop and surface it to the owner before doing project work.

## H4A+H4B Completion — 2026-08-09

- H4A: PR #114 merged BY the owner (Zest-LeadGen) at 2026-08-09T18:10:36Z after owner review approval; authorization = owner comment 5232806979 on issue #113 (PA-0002 evidence). Merge actor stated precisely per R-RECON-001.
- H4B: owner-executed hardening script (terminal, owner account): ruleset 20598456 upgraded to deletion + non_fast_forward + required_status_checks + pull_request with required_review_thread_resolution=true and bypass_actors empty; secret scanning + push protection enabled; dependency alerts (Dependency Graph) enabled; direct-push rejection probe REJECTED with GH013 (proof pasted into session by owner).
- Verification split (documentation scope): ruleset state independently re-read from the collaborator account and matched; security-settings fields are admin-only reads, so their evidence is the owner's pasted script output (primary source), not a collaborator read.
- Main-push CI after merge: ContractorOS Control Gates run on 598c2e3 completed success — decomposed aggregate green in push context.
- Deferrals per the authorization: mobile/web lint+unit -> H5/H6; dependency-review workflow -> next control intake now that Dependency Graph is on.

## Post-Stress Reconciliation + Corrections — 2026-08-09

- Trigger: owner-commissioned full-tree adversarial stress test (7 subagents, 95 probes, 78 findings; artifact 7dcf3ead). Owner approved the "Mine" dispositions and the disclose-and-track disposition for owner-lane structural items.
- ACCURACY CORRECTION (epistemic-integrity standard): OD-017's claim that ".claude/settings.json pins Fable 5 as the project default (owner-applied via /model)" is CORRECTED — the pin is user-global (~/.claude/settings.json), uncommitted, and binds nothing on other machines/clones. The Fable-5-only rule (OD-017) stands unchanged; only the record of its mechanism is corrected. See also the published project report Edition 4 correction (merge counts: 24 total at grounding / 20 owner-executed / 4 both-keys collaborator-merged — the flagship stat previously repeated the R-RECON-001 overstatement).
- PA-0001 evidence_id backfilled from placeholder PENDING_OWNER_COMMENT_ON_111 to issue-111-comment-5230073633 (owner comment verified live; matching the PA-0002 standard).
- state.yaml advanced to lifecycle_state h4_operational (H4 closed_completed via #113/#116), resolving the h4_operational-vs-h4_delivered label contradiction the stress test flagged.
- OWNER_DECISION_REGISTER.yaml: OD-series divergence recorded via an operational_decision_records cross-reference (register holds program-direction D1-D32; OD-series live in DECISION_LOG).
- Dangerous stale rescue scripts (run-h2-h3-keyturn.sh, run-b5-rollback-proof.sh, run-h1-final.sh, run-h4b-hardening.sh, + others) moved to ~/Documents/ContractorOS-Support/ContractorOS-Rescue-20260808/superseded/ with exec bit removed (local tree; not in this repo).
- KNOWN GAP recorded (owner decision, not a defect to auto-fix): R-STRESS-001 — path-scope automated enforcement is observe-only; arming it is an owner decision folded into H5. R-STRESS-002/003 disclose CI self-referentiality, marker self-attestation, and one-keyring separation, tracked to H5/H6/H9.

## H5-A Intake + PA-0003 — 2026-08-09

- H5+H6 batched phase authorized by owner "go" (2026-08-09), to be recorded on-platform via the owner authorization comment on issue #118 (PA-0003 evidence_id, currently PENDING_OWNER_COMMENT_ON_118).
- H5-A deliverable: read-only governance-document inventory & classification (134 files in docs/project-control; 51 historical phase reports; ~40 competing "current" records). No file moves in H5-A.
- Owner decision recorded for execution as the first act after PA-0003 lands: ARM the path-scope wall (make check_phase_authorization blocking). Arming is a SEPARATE PR after PA-0003 is on base, because an armed checker self-denies the PR that introduces its own authorization (same bootstrap as PA-0001/PA-0002).
- Operating-mode change (owner, 2026-08-09): batch to ONE owner key-turn per phase — developer executor prepares all PRs and gates; owner approves/merges + posts authorizations in a single combined command per phase.

## H5-B.1 — Source of Truth Map + PA-0003 Backfill — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034). PA-0003 evidence_id backfilled to that comment; PA-0004 issued for H5-B paths.
- Added a Single Source of Truth Map to AUTHORITY_AND_SUPERSESSION_INDEX.md fixing canonical artifacts for unambiguous concerns (status→state.yaml+live artifact, risk→RISK_REGISTER, findings→RED_TEAM_FINDINGS_REGISTER, decisions→DECISION_LOG+ADRs, history→DEVELOPMENT_LEDGER, authorizations→PA-*).
- Deferred (not guessed): the single canonical ROADMAP and CONSTITUTION require an explicit owner choice (H5-B.2). No roadmap/constitution superseded here.
- Sequencing recorded: archive move of 51 phase reports and arming the path wall both depend on a control-script hardening PR (exempt docs/archive/ from forbidden-scope; PA-bootstrap so an armed wall does not deadlock future PA introduction; fix R-STRESS-004). That PR is delivered separately for deliberate owner review of the sensitive checker surface.


## H5-B Control-Script Hardening — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0005). This PR edits the enforcement checkers themselves — presented for deliberate owner review (R-STRESS-002: CI is self-referential, so owner review is the primary control for checker changes).
- check_forbidden_scope.py: exempt docs/archive/ and scripts/control/ from term-scanning. Reason: the archive holds immutable historical reports (legacy language = audit evidence), and control code contains the scanned term literals by design. Both remain governed by CODEOWNERS + control-script tests.
- check_pr_contract.py: R-STRESS-004 fix — an overclaim is downgraded only when a negation PRECEDES the term (forward qualifiers still count anywhere). Closes the "complete with no open blockers" bypass; verified on 8 in-line cases; adversarial + continuity suites still pass.
- Explicitly NOT in this PR: arming the path wall and the archive file move (separate follow-ups). check_phase_authorization.py and check_changed_files.py are untouched (PA-0005 forbids them).


## H5 State Reconciliation — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0006). Refreshes state.yaml current_main_sha to fd09cbb and lifecycle to h5_in_progress after H5-A (#119), H5-B.1 (#120), and H5-B control-hardening (#121) merged. Separate PR because state.yaml is forbidden in the delivery PAs (the disclosed, established reconciliation pattern). Closes the hourly audit's open DRIFT finding on the snapshot SHA; the PA-0003 evidence backfill it also flagged was already landed in #120.


## H5-C Archive Move — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0007). Moved 52 completed-phase reports (3 kept in place as live continuity-test fixtures) + H0/H1 closeout lineage + incidents + sanitation manifests into docs/archive/ (git mv; history preserved). Enabled by the H5-B docs/archive scanner exemption.
- Disclosed limitation: report renames/deletes are not pattern-authorizable (schema: add/modify only), so they ran under observe-only phase-authorization. An exact-path deletion-authorization mechanism is therefore a prerequisite before the path wall can be armed — recorded for the arming PR.


## Post-H5-C Reconciliation + Local Tree Consolidation — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0008). Refreshes state.yaml to 0f87c1a after PR #123 (H5-C archive move) merged, closing the hourly audit's DRIFT finding, and corrects the active_gate text that still listed the archive move as remaining.
- Local tree consolidation (owner request, outside this repo): eight scattered ~/Documents/ContractorOS-* entries consolidated to ONE support parent, ~/Documents/ContractorOS-Support/, holding the active Rescue key-turn folder, the Archive (now including packets R1-R11 and superseded evidence), and the backup tarball. The canonical session directory is unchanged and unambiguous: ~/Documents/GitHub/contractoros-california (companion policy root: ~/Documents/GitHub/contractoros-governance). Path references in this log updated accordingly.
- Verified at reconciliation time: both local repos clean, zero dirty files, HEAD identical to origin/main; zero stale local branches; zero open PRs; 15 open issues after closing 12 completed/superseded ones.

## H5-D Authorization Bootstrap + Exact-Path Relocation + Wall Arming — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0009, introduced by this PR via the bootstrap mechanism it delivers). The comment's PATH_WALL_DECISION=ARM_NOW is the arming authority; scope trace disclosed: the comment's gate list names H5-A..H5-C and this final piece is the "arm the path wall" first-deliverable item plus its two recorded prerequisites (state snapshot: "PA-bootstrap + exact-path deletion authorization, then arming the path wall"). AUTOMATIC_CONTINUATION=NO — owner approval of this PR is the continuation consent.
- DEFECT FOUND during pre-arming verification (would have broken the wall on day one): all six H5 authorization records (PA-0003..PA-0008) were simultaneously live for issue #118; the checker's exactly-one resolution rule computed DENY found=6 for any #118 PR. Observe mode discarded this every time. Fix: single-live-record invariant — PA-0009 supersedes and revokes all six via content-verified closure edits (only supersession.revoked and revocation_evidence may change; verified byte-equal otherwise).
- check_phase_authorization.py extensions (owner walk-through in the PR body/report): (1) BOOTSTRAP — a PR may introduce exactly one record for its linked issue; filename must match authorization_id; evidence_id must be on-platform (issue-N-comment-id); repository binding checked; every live base record for the issue must be closed in the same PR and listed in supersedes; the record must self-authorize its own addition and each closure via exact-path rules. (2) RELOCATE — content-identical renames (R100) authorizable only by exact-path relocate rules (pattern -> to); R<100, copies, and pattern renames remain denied; authorization records are never deletable or relocatable. (3) ARMED — phase-authorization job added to aggregate needs, continue-on-error removed; OPS-005 observe window ended.
- Trust model disclosed: bootstrap moves the wall from pre-authorized-on-main to authorized-in-same-PR; the authorization judgment rests on CODEOWNERS owner review + owner-only merge (same trust root as checker self-edits, R-STRESS-002); running checkers from main remains an H6-B hardening item.
- Companion governance PR (Zest-ContractorOS/contractoros-governance): phase-authorization schema 1.1.0 — change_kinds enum gains "delete" and "relocate" (fixes a live contradiction: the checker and PA-0007's disclosed limitation both assumed delete rules the 1.0.0 enum forbade), optional exact-path "to" field for relocate rules, schema_version widened to enum ["1.0.0","1.1.0"]. PA-0009 itself uses only add/modify and remains 1.0.0-conformant.
- Out of scope, recorded not guessed: PA-0001 (#111) and PA-0002 (#113) remain live but bind closed issues; they do not collide with any open issue's resolution and expire 2026-08-16; closing them is deferred to the next reconciliation. Adversarial test suite extended 8 -> 25 cases; full continuity suite green.

## Post-H5-D Reconciliation — 2026-08-09

- Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0010, the second live exercise of the H5-D bootstrap mechanism — it closes PA-0009 per the single-live-record invariant).
- Owner key-turns verified live: PR #125 approved and merged by Zest-LeadGen 2026-08-10T01:31:59Z (product main 32735ea — path-scope wall ARMED); governance PR #9 approved and squash-merged by Zest-LeadGen 2026-08-10T01:32:04Z (governance main 56eaef9 — phase-authorization schema 1.1.0). First main-push run under the armed workflow: green (push-skip semantics proven live).
- Snapshot refreshed to 32735ea; lifecycle h5_delivered_pending_closeout; the observe-only wall blocker is removed as resolved; H6-awaits-own-authorization blocker retained.
- Disclosed, not worked around: PA-0001 (#111) and PA-0002 (#113) remain live for closed issues. The armed checker's CLOSURE_WRONG_ISSUE rule (by design) prevents a #118-linked PR from revoking other issues' records; they expire 2026-08-16 and no PR will link those closed issues again, so no resolution collision is possible.

## H6-A.1 Toolchain Baseline (control half) — 2026-08-10

- Under owner H6 authorization (issue #118 comment 5235003178, owner-authored 2026-08-10T01:42:17Z; PA-0011 via bootstrap, closing PA-0010). First H6 deliverable.
- LANE-PURITY SPLIT, discovered by running the validators against the real combined diff: the control-file update matrix requires apps/** changes under Lane: Product / QA while PA records and control docs are Control / Infrastructure, and a root package.json is Dependency-lane — one combined PR cannot declare a compatible lane. H6-A therefore lands as H6-A.1 (this PR, control half) then H6-A.2 (apps manifests + lockfiles, Product / QA + Dependency approval phrases per the PR #90 precedent), opened only after H6-A.1 merges because the armed checker resolves base-mode authorization from the base commit. PA-0011 pre-authorizes both halves by exact path.
- Version selection, verified not guessed: Node v22.23.2 (22 LTS latest, live nodejs.org dist index; npm 10.9.8 ships with it); expo 57.0.11 (npm dist-tag latest); react 19.2.3 + react-native 0.86.2 (npx expo install AND expo's bundledNativeModules.json — both sources agree). The apps/mobile `latest` eliminations ship in H6-A.2.
- Deliberate decisions, recorded: NO npm workspace (Expo/Metro per-app resolution; hoisting deferred until monorepo tooling is separately evaluated and authorized; each app keeps an isolated public-registry lockfile) and NO root orchestration manifest yet (drafted, then deferred to H6-B — Dependency lane, and no value before CI jobs exist to call it).
- check_forbidden_scope.py: committed-lockfile paths exempted from implementation-term scanning (package names like whatwg-fetch/fetch-nodeshim contain term literals; lockfiles remain fully governed by the dedicated --lockfiles-only contamination/provenance scan on the same exact paths). Third instance of the H5-B disclosed-exemption pattern.
- Determinism proven (evidence file): byte-identical lockfile re-resolution across two fresh directories; clean npm ci (mobile 463 packages, web 20 + green vite build); provenance 100% registry.npmjs.org; contamination scans clean; sha256 digests bind the H6-A.2 artifacts in advance; license inventory permissive/weak-copyleft only.
- REAL FINDING from deliberate failure tests (recorded as observed): npm ci does NOT reject a "latest" dist-tag reintroduced against a committed lockfile. Manifest pinning therefore needs a dedicated pin scan — named H6-B deliverable alongside mobile static validation, lint/typecheck/test wiring, node-version-file alignment, root-manifest decision, and R-STRESS-002 (checkers from main). The other four failure tests failed as designed (lockfile drift, registry contamination, missing script, incompatible peers).

## Post-H6-A Reconciliation — 2026-08-10

- Under owner H6 authorization (issue #118 comment 5235003178; PA-0012 via bootstrap, closing PA-0011).
- Owner key-turns verified live: PR #127 (H6-A.1 control half) merged 2026-08-10T02:15:02Z; PR #128 (H6-A.2 dependency half) merged 02:21:01Z — product main 396d4a3. H6-A delivered in full across the lane-purity split. web-ci green with the committed engines pins on both the PR and the main push; the armed checker's first base-mode validation (PA-0011, PR #128) succeeded.
- Snapshot refreshed to 396d4a3; lifecycle h6_in_progress; the npm-ci/latest manifest-pin gap recorded as a blocker-level disclosure (review-enforced until the H6-B pin scan lands).
- POST-OPEN ADDITION (same reconciliation, disclosed): pushing this PR surfaced GitHub's first Dependabot report on the new mobile lockfile — 3 alerts (image-size 2xHIGH with NO published patch; uuid MEDIUM patched only via transitive override). Recorded as R-DEP-SEC-001 in RISK_REGISTER with exposure assessment and both disposition options; OWNER DECISION REQUIRED (DEPENDENCY_SECURITY_RISK_ACCEPTANCE) — nothing is accepted or bumped by this PR. PA-0012 amended in-PR (bootstrap record, pre-merge) to add the RISK_REGISTER path and the trigger category.

## Stress-Run-3 Corrections + Owner Decision Questionnaire — 2026-08-10

- Under owner H6 authorization (issue #118 comment 5235003178; PA-0013 via bootstrap, closing PA-0012; schema 1.1.0 record — first use of an exact-path delete rule, for the committed .pyc). Stress-run-3 report: artifact 7dcf3ead (run3 label): 7 agents, 157 probes, 85 findings, 0 critical / 2 high, ZERO provenance violations.
- OWNER DECISION QUESTIONNAIRE (2026-08-10, all 13 answered; recorded verbatim by outcome): Q1 merge #129 now (done 03:30:34Z, main 1f493f6). Q2 R-DEP-SEC-001 ACCEPTED with dated revisit at each phase boundary (also in the #129 approval text; register updated). Q3 amkb80 credential LOGGED OUT (executed by owner 2026-08-10, verified absent from keyring — closes the stress run's first HIGH; keyring back to the two H2-WAIVER-001-disclosed accounts). Q4 one batched corrections PR (this PR). Q5 project-report Edition 5 after #129 (in flight). Q6 local tidy now (done: governance pulled + merged worktree/branch removed; 10 stale/probe branches deleted). Q7 CODEOWNERS consolidation as a dedicated PR immediately after this one (second HIGH). Q8 overclaim-gate FORWARD_QUALIFIERS fix -> H6-B. Q9 required-check wiring (web-ci/CodeQL/mobile) -> H6-B. Q10 OWNER OVERRIDE: hourly auditor repinned to claude-opus-5 (owner: a weaker model auditing Fable 5 work is backwards; Opus 5 is the SOLE permitted non-Fable model under OD-017, scoped to read-only cloud audit only) + prompt refreshed to the PA-chain era incl. an independent github_verified_at plausibility check (routine trig_01TUwRyGHvf5J9w71gxDv2zb updated 03:23Z). Q11 machine-speed key-turn bursts held as documented residual under H2-WAIVER-001 (structural fix remains H9). Q12 PA-0001/PA-0002 expire naturally 2026-08-16. Q13 H6-B GO once Part-1 items executed (they now are).
- R-STRESS-005 (new, systemic): the authorized spot-check of all 22 snapshot revisions found EIGHT with github_verified_at AFTER their own commit time — fabricated verification claims, confined to the 2026-08-08/09 sessions (July-era snapshots wrote genuine second-precision values). Underlying facts were all independently re-verified as true; the fabrication is the WHEN, not the WHAT. Rule now in snapshot_semantics (second-precision, captured at the actual gh read); Opus 5 auditor independently checks it hourly; history disclosed, not rewritten. This snapshot's timestamp (03:32:21Z) is the captured read time.
- Evidence-of-record corrections (verify-number-freshness): mobile resolved URLs 473->481; npm ci count 463->471; web license line "33 packages"->43 lockfile entries (npm ci installs 20). Corrections made IN the living evidence file with dated annotations; the two merged phase reports carrying the stale numbers are left unedited as historical records, corrected here.
- Stress-test workflow script committed to scripts/control/stress/contractoros-st.workflow.js (the skill's referenced path; current-era targets). Committed .pyc removed from the control-test tree; __pycache__/ gitignored.

## CODEOWNERS Consolidation + Report-Navigation Hard Rule — 2026-08-10

- Under owner H6 authorization (issue #118 comment 5235003178; PA-0014 via bootstrap, closing PA-0013; owner questionnaire Q7 authorized this as a dedicated immediate PR). Closes stress-run-3's second HIGH: GitHub gives .github/CODEOWNERS precedence, and that file had no catch-all, so the root file's `*` rule was dead — scripts/continuity/**, docs/ outside project-control, docs/archive/**, and any new top-level path had NO code owner and require_code_owner_review did not bind there. Fix: catch-all added to .github/CODEOWNERS (with the root file's /scripts/continuity/ entry absorbed and /docs/project-control/authorizations/ made explicit); the shadowed root CODEOWNERS deleted via PA-0014's exact-path delete rule. Effective ownership is now: every path -> owner review required.
- OWNER HARD RULE recorded (2026-08-10, applies to this and all future sessions): every report/response ends with an explicit NEXT block — who acts, the exact action (pasteable command for owner acts), and the stop condition. This re-activates the Issue #76 navigation-block discipline already in this log; the operator had let it lapse mid-session and the owner corrected it.

## H6-B.1 Control Hardening — 2026-08-10

- Under owner H6 authorization (issue #118 comment 5235003178; PA-0015 via bootstrap, closing PA-0014; owner questionnaire Q8/Q9/Q13 routed this scope here). This PR edits enforcement checkers and CI gates — presented for deliberate owner walk-through (R-STRESS-002 discipline).
- check_pr_contract.py: stress-run-3 overclaim regression fixed — "forbidden" and "blocked" removed from FORWARD_QUALIFIERS (they are negations, not forward qualifiers; they now downgrade only when PRECEDING a claim term, via DOWNGRADE_CONTEXT). Verified five-way: the two bypass phrasings now flag; preceding negation and true forward qualifiers still downgrade; the original R-STRESS-004 case still flags.
- check_manifest_pins.py (NEW) + 11-case adversarial suite: every dependency declaration in the governed manifests must be EXACT semver — dist-tags, ranges, wildcards, OR bars, URL/git/file specifiers all rejected. Closes the disclosed npm-ci/latest gap (H6-A real finding) with a machine gate; wired into the required policy-validators job. Live scan at delivery: 7 declarations, all exact.
- phase-authorization-from-main (NEW aggregate-required job): the path wall ALSO runs from the base branch's copy of check_phase_authorization.py, so a PR that neuters the checker in its own tree still faces main's version. Scope disclosed: protects the wall itself; other validators remain PR-tree, backstopped by total CODEOWNERS coverage (#131). This is the R-STRESS-002 structural mitigation scheduled for H6-B.
- web-ci + new mobile-ci: setup-node now reads .nvmrc (node-version-file) — single source for the Node pin. contractoros-mobile-ci (NEW, advisory until the owner's required-check ruleset act): registry provenance, npm ci from the committed lockfile, drift check, expo config static validation, entry-module resolution — all steps verified locally against the committed manifest before delivery.
- Root-manifest decision closed (deferred from H6-A): NO root package.json — per-app npm ci --prefix suffices, TOOLCHAIN.md documents it, and the matrix's Dependency-lane treatment of a root manifest adds ceremony without value while no orchestration consumer exists. Revisit only if a monorepo tool is separately authorized.
- Remaining H6-B after this PR: owner ruleset act (wire contractoros-web-ci + contractoros-mobile-ci as required checks) and H6-B.2 (Product / QA lane: lint/format/typecheck/unit-test layers in the apps).
