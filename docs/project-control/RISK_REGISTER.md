# ContractorOS Risk Register

Purpose: track active risks until evidence proves they are resolved.

Template:

```text
Risk:
Status:
Evidence:
Owner:
Resolution condition:
Last reviewed:
```

## H1 Recovery Risks

| Risk ID | Risk | Current control | Status |
|---|---|---|---|
| R-H1-P0-01 | Circular trust: a candidate policy or first commit defines the oracle that accepts itself. | Minimal inert first commit, external trusted evidence, protected later PR, fresh independent review. | P0 active; unresolved. |
| R-H1-02 | Local authority drift advances prompts or packets beyond durable GitHub closeout. | Issue #58 authority, no local authority, ordered R4-R7 closeout, no automatic continuation. | Active. |
| R-H1-03 | Developer and red-team roles collapse into self-review. | Codex executor-only role, separate red-team architecture/audit, fresh exact-SHA review, human approval. | Active. |
| R-H1-04 | Candidate-owned oracle accepts candidate-controlled policy or test evidence. | External trusted file oracle requirement and prohibition on executing candidate policy code. | P0 active; unresolved. |
| R-H1-05 | Duplicate YAML or JSON keys create ambiguous accepted policy. | Strict parsing strategy and duplicate-key rejection remain required H1 engineering decisions. | Active; unresolved. |
| R-H1-06 | Stale canonical current state competes with live GitHub evidence. | Reconciled snapshot, explicit supersession, live reverification, fail-closed contradiction handling. | Active. |
| R-H1-07 | Mutable third-party Action provenance changes reviewed behavior. | Full-SHA action pins and immutable reusable-workflow provenance remain required. | Active; unresolved. |
| R-H1-08 | Policy and runtime resource limits diverge. | Policy-bound runtime-limit engineering decision and negative tests remain required. | Active; unresolved. |
| R-H1-09 | Broad connector/resource discovery violates scope or exposes unrelated context. | Direct-tool-only rule, incident evidence, regression checks, and fail-closed stop. | Active. |

Nine unresolved H1 engineering decisions remain: `P0_02` exact current product PR-head mechanism; `P0_03` trusted default-branch/main binding; `P1_01` immutable reusable-workflow provenance; `P1_03` strict YAML/schema strategy; `P1_04` deterministic evaluation time; `P1_05` GitHub-applicable ruleset payload; `RT_P0_04` external trusted file oracle; `RT_P1_06` policy-bound runtime limits; and `RT_P2_07` duplicate JSON-key rejection. No local H1 candidate is accepted.

## Historical Issue #49 Continuity Collector Risks

Issue #49 is closed and PR #50 merged at `7d00343c233e45185e6c4d77e50eb870f408c01f`. Any row wording below that says “implementation review” records the historical review state; it is superseded by merged status. Remaining technical limitations stay active only as operational risks and grant no current-phase authority.

| Risk ID | Risk | Control | Validation task | Status |
|---|---|---|---|---|
| R-I49-01 | Stale-state false negative | Compare canonical, local and live main plus issue/PR lifecycle evidence; fail closed. | Stale-main and starting-main baseline runs. | Controlled in implementation review. |
| R-I49-02 | Command allowlist bypass | Positive executable, subcommand, flag and shape validation. | Unknown executable/subcommand and prohibited Git/GitHub command tests. | Controlled in implementation review. |
| R-I49-03 | Shell execution | Argument arrays with `shell=False` and finite timeout. | Mocked subprocess call inspection. | Controlled in implementation review. |
| R-I49-04 | Output path or symlink escape | Resolve the nearest existing ancestor and prospective suffix before creation; recheck after creation and before atomic writes. | Nonexistent/nested repository descendants, output/ancestor/target symlinks, non-regular targets, valid external creation and cleanup tests. | Controlled in C3 implementation review. |
| R-I49-05 | Secret or private evidence leakage | Avoid broad collection and reject private-looking patterns. | Unsafe fixture and absolute-home-path tests. | Controlled in implementation review. |
| R-I49-06 | Moved-head approval reuse | Compare observed and marker-bound SHA with current PR head; quarantine mismatch. | Moved-head and stale-marker tests. | Controlled in implementation review. |
| R-I49-07 | Misleading derived packet authority | Derived notice, prohibited-action section and no write permission. | Packet-content and raw-chat rejection tests. | Controlled in implementation review. |
| R-I49-08 | Inaccessible required live evidence | Executable, timeout, nonzero, output-bound, malformed-live-JSON and missing-field failures use `EvidenceUnavailableError` and exit `3`; no safe classification is inferred. | C3 inaccessible-evidence exit tests. | Controlled in C3 implementation review. |
| R-I49-09 | Deterministic-output drift | Stable ordering, normalized line endings and explicit packet-hash rule. | Identical-run comparison, expected packet and hash recomputation. | Controlled in implementation review. |
| R-I49-10 | Contradictory lifecycle or active auto-merge | Quarantine protected-boundary contradictions. | Contradictory lifecycle and auto-merge tests. | Controlled in implementation review. |
| R-I49-11 | Hidden metadata fabrication, quota/context loss, or governance-progress inflation | Exact honest fallbacks, proportional routing, atomic packets, context bands, compact structured tables, capability separation, and chart-output prohibitions. | Governance profile, routing, context, progress, chart, and non-inflation tests. | Controlled in governance-hardening review; exact-SHA external review pending. |
| R-I49-12 | Wrong local root or contradictory origin accepted as the requested repository | Strict root/top-level/control-file binding and four-form normalized GitHub origin verification; persist no raw path or URL. | C3 repository identity and private-path exclusion tests plus live collector. | Controlled in C3 implementation review. |
| R-I49-13 | Lifecycle categories collapse external review, human approval, merge and closeout into a false readiness claim | Separate active, externally approved, merge-ready and closed-gate matrices; contradictions quarantine and inaccessible evidence blocks. | C3 lifecycle matrix tests. | Controlled in C3 implementation review. |
| R-I49-14 | Operational readiness inherits documentation or governance progress | Permanent three-series chart contract and explicit non-inheritance rule; blocked capabilities stay zero or not proven. | C3 reporting-layout tests. | Controlled in C3 governance reconciliation review. |
| R-I49-15 | Missing authoritative GitHub repository/default-branch values are represented by local or requested fallback evidence | Require exact live repository identity, default-branch object/name/target and lowercase target SHA before evidence construction; permit no substitution. | Eight C3.1 authoritative-live-field tests plus live collector. | Controlled in C3.1 implementation review. |
| R-I49-16 | Permission read rejection or unsafe evidence is misclassified as unavailable, or malformed permission data creates an empty normalized record | Catch only unavailable-evidence exceptions and structurally validate the response before normalization. | Six C3.1 exception-boundary and permission-response tests. | Controlled in C3.1 implementation review. |
| R-I49-17 | Malformed nested canonical state escapes the documented CLI exit contract or loses linked-PR identity | Validate bounded linked objects, required identity, supported state and exact observed-head SHA before comparison. | Eight C3.1 canonical and CLI tests. | Controlled in C3.1 implementation review. |

## Active Risks

### low-risk lane misclassification

```text
Risk: low-risk lane misclassification
Status: Active / Phase 4K-7 validator merged; dry-run evidence not yet available
Evidence: Phase 4K-7 added a fail-closed validator and self-test coverage for marker consistency and changed-file classification, but no dry-run evidence or approval-policy reduction exists.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Later dry-run evidence proves false-positive and false-negative behavior before any approval or merge policy is reduced.
Last reviewed: 2026-07-10
```

### low-risk validator workflow drift

```text
Risk: low-risk validator workflow drift
Status: Active / controlled by protected control-gates workflow and external review
Evidence: Phase 4K-7 completed through Issue #43 and merged PR #44 after adding the required pull-request validator step. Its reviewed head was `a519ef5579c130181ac1b25f74bb48f481478378`, and its merge/current-main SHA is `8d443310cf006b82966163f8e486d1f52d8d4e6c`. A future workflow edit could weaken ordering, skip PR context, or treat missing evidence as a low-risk pass.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Workflow changes remain protected by required control-gate review, validator self-tests, external red-team review, human approval, and fail-closed behavior for missing or ambiguous evidence.
Last reviewed: 2026-07-10
```

### workflow command misuse

```text
Risk: workflow command misuse
Status: Active / controlled by Phase 4K-8 command-pack stop conditions
Evidence: Copy/paste lifecycle commands can affect branch, PR, marker, merge, and issue-closeout evidence if placeholders, repository identity, or SHA values are wrong. A dirty worktree or branch synchronization before exact local/origin starting-SHA proof can also mutate or misclassify the starting state.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future operator use follows the command pack, proves a clean worktree before synchronization, fetches without pulling, verifies exact local and `origin/main` starting SHAs before branch creation, and stops on unresolved placeholders, ref mismatch, or unexpected output.
Last reviewed: 2026-07-10
```

### marker assembly ambiguity

```text
Risk: marker assembly ambiguity
Status: Active / controlled by Phase 4K-8 PR-body assembly rule
Evidence: Phase 4K-7 exposed that live marker ordering and duplicate fields can affect parser behavior. Multiline review values or embedded reserved marker/field text can inject contradictory decisions while superficial marker counts still pass. Active Phase 4K-8 through Issue #45 and PR #46 supersedes the historical append-only procedure with replacement-body assembly and generated-body validation.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future PR evidence keeps templates fenced or commented; rejects empty, multiline, placeholder, marker-token, heading, and reserved-field values; validates supported formats and exactly one of every decision field; rejects unknown fields; rechecks the live PR head immediately before body replacement; and leaves exactly one owner marker final.
Last reviewed: 2026-07-10
```

### pre-marker workflow ordering visibility

```text
Risk: pre-marker workflow ordering visibility
Status: Active / documented limitation; no workflow change authorized in Phase 4K-8
Evidence: Changed-file, forbidden-scope, required-control-update, PR-contract, owner-trigger, and low-risk-lane checks run before the mandatory red-team marker. While the marker is missing, later GitHub lockfile-only and claim-language steps are skipped even though their local equivalents remain mandatory. Main protection is proven with strict `contractoros-control-gates`, required review controls, conversation resolution, and admin enforcement.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Operators report the ordering accurately, run the equivalent local checks, and do not claim every GitHub step passed before marker insertion. Any workflow reordering requires a separate authorized phase.
Last reviewed: 2026-07-10
```

### automation approval overreach

```text
Risk: automation approval overreach
Status: Active / controlled by Phase 4K-6 executor, red-team, human approval, and auto-merge boundaries
Evidence: The owner-approved 95% workflow automation target could be misread as approval power for Codex or future automation to self-review, approve, merge, bypass branch protection, expand scope, or close work without verified evidence.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future implementation preserves Codex executor-only status, external red-team separation, current human approval policy, protected required checks, durable evidence, and fail-closed stop conditions.
Last reviewed: 2026-07-09
```

### canonical continuity state drift or leakage

```text
Risk: public canonical state becomes stale or exposes private evidence
Status: Active / architecture documented; collector not implemented
Evidence: Issue #47 defines schema validation, exact-SHA comparison, sanitization, quarantine, opaque private references, and serialized canonical-state changes.
Owner: ContractorOS owner / future continuity gate
Resolution condition: read-only collector gate proves stale detection, deterministic derived packets, leak controls, and rollback without write authority.
Last reviewed: 2026-07-11
```

### program targets mistaken for guarantees

```text
Risk: twenty-four-month, fourteen-day, or ninety-five-percent targets are treated as unconditional commitments
Status: Active / controlled by Constitution wording and later evidence gates
Evidence: Risk documentation for D1, D2, D13, and D14 distinguishes targets from readiness, release, or completion proof.
Owner: ContractorOS owner / program governance
Resolution condition: milestone and automation claims use measured evidence, explicit denominators, prerequisites, and retained human gates.
Last reviewed: 2026-07-11
```

### paid pilot bypasses zero-spend policy

```text
Risk: a pilot activates spend without explicit bounded owner approval
Status: Active / blocked by policy
Evidence: D21 requires a named objective, ceiling, duration, data class, exit criteria, and hard shutdown threshold; no automatic recharge or uncapped fallback.
Owner: ContractorOS owner
Resolution condition: a separate paid-pilot gate records approval and measured need before any purchase or activation.
Last reviewed: 2026-07-11
```

### automated SHA and closeout drift

```text
Risk: automated SHA and closeout drift
Status: Active / policy defined; implementation not started
Evidence: Future check monitoring, merge verification, issue closeout, and progress updates could use stale PR-head evidence or close an issue before the exact merge and main state are verified.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future automation binds review evidence to the exact current PR head SHA, verifies merge metadata and main state, and stops when issue, PR, check, or branch evidence conflicts.
Last reviewed: 2026-07-09
```

### premature approval or auto-merge policy reduction

```text
Risk: premature approval or auto-merge policy reduction
Status: Active / auto-merge prohibited
Evidence: Phase 4K-6 defines future eligibility questions but does not implement automation or reduce external red-team and human approval requirements.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Any future policy change has a separate durable issue, external red-team review, human approval, implementation evidence, protected checks, dry-run evidence, rollback controls, and proof that owner-triggered work cannot enter the lane.
Last reviewed: 2026-07-09
```

### manual-action target measurement error

```text
Risk: manual-action target measurement error
Status: Active / target ranges are not yet measured in a dry run
Evidence: Phase 4K-6 records an 8-14 action baseline and future category targets, but no automation implementation or measured Phase 4K-11 sample exists.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Phase 4K-11, if separately approved later, measures action counts, exception rates, classification errors, review quality, and closeout accuracy before Phase 4K-12 evaluates the target.
Last reviewed: 2026-07-09
```

### product development source-of-truth drift

```text
Risk: product development source-of-truth drift
Status: Active / controlled by PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md after Phase 4K-3
Evidence: Roadmap, phase tracker, ledger, and phase reports contained overlapping current-state and future-phase statements after Phase 4K-1 and Phase 4K-2 completed.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future project-control updates keep PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md current and mark older roadmap/tracker statements as historical or subordinate instead of competing current-state authority.
Last reviewed: 2026-07-09
```

### unsupported owner-trigger semantic category

```text
Risk: unsupported owner-trigger semantic category
Status: Active / controlled by documented validator limitation
Evidence: Issue #35 requests PRODUCT_SOURCE_OF_TRUTH in the OWNER_TRIGGER_REVIEW marker, but scripts/control/check_owner_trigger_review.py does not include that category in its allowed category list.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: A later approved control phase either adds PRODUCT_SOURCE_OF_TRUTH to the validator and governance docs or records a different durable category policy.
Last reviewed: 2026-07-09
```

### dependency baseline issue superseded before implementation

```text
Risk: dependency baseline issue superseded before implementation
Status: Active / controlled by Issue #34 not-planned closeout, Phase 4K-3 source-of-truth reconciliation, and Phase 4K-4 Issue #37 decision intake
Evidence: Issue #34 was created for dependency/lockfile baseline decision work but closed as not planned before implementation because roadmap/platform/development-model reconciliation was required first. Phase 4K-4 uses Issue #37 as the active dependency/lockfile governance decision intake.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Any future dependency/lockfile baseline implementation starts only from a new durable GitHub issue after Phase 4K-4 is merged, main is verified, and Issue #37 is closed.
Last reviewed: 2026-07-09
```

### dependency baseline not yet implemented after governance decision

```text
Risk: dependency baseline not yet implemented after governance decision
Status: Active / Phase 4K-5 blocked before mutation
Evidence: Phase 4K-4 recommends a later deterministic dependency/lockfile baseline implementation phase. Phase 4K-5 attempts the web baseline gate through Issue #39 but is blocked before mutation because required node/npm tooling is unavailable. No package manifest, lockfile, npmrc file, dependency directory, runtime QA, or build artifact is created or changed.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: A later approved toolchain availability / npm bootstrap governance phase resolves the toolchain path, proves public npm registry configuration before mutation, and only then allows a later dependency-baseline implementation retry.
Last reviewed: 2026-07-09
```

### dependency toolchain unavailable

```text
Risk: dependency toolchain unavailable
Status: Active / blocks Phase 4K-5 dependency mutation
Evidence: Phase 4K-5 command evidence shows `npm --version` and escalated `npm --version` both report `zsh:1: command not found: npm`; `node --version` and escalated `node --version` both report `zsh:1: command not found: node`; bundled Node exists at version `v24.14.0`, but bundled npm does not exist at the bundled Node path.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: A later durable toolchain availability / npm bootstrap governance issue decides and verifies the approved Node/npm path, public npm registry proof, stop conditions, and package-manager substitution policy before dependency resolution is retried.
Last reviewed: 2026-07-09
```

### product re-entry scope expansion

```text
Risk: product re-entry scope expansion
Status: Active / controlled by Phase 4K-0 recommendation boundaries
Evidence: Issue #27 requires Phase 4K-0 to recommend exactly one next implementation phase while prohibiting product changes inside Phase 4K-0.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Phase 4K-1 starts only from a later GitHub phase issue with explicit allowed files, forbidden scope, validation tasks, red-team requirement, human approval requirement, auto-merge status, and stop conditions.
Last reviewed: 2026-07-09
```

### non-durable product direction after governance hardening

```text
Risk: non-durable product direction after governance hardening
Status: Active / controlled by Issue #24 no-memory-only directive and Phase 4K-0 project-control records
Evidence: Issue #24 No Memory-Only Owner Decisions addendum requires owner approvals, decisions, agreed scope, authorizations, rejections, conditions, closeouts, protocol updates, and future operating rules to be recorded in relevant GitHub/project-control evidence before they are durable.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future product direction is recorded in GitHub issues, PR bodies/comments/reviews, committed project-control files, phase reports, decision/source/risk/validation records, or artifact index entries when applicable.
Last reviewed: 2026-07-09
```

### red-team lifecycle state drift

```text
Risk: red-team lifecycle state drift
Status: Active / controlled by Phase 4J-5 protocol after merge
Evidence: Issue #24 Operator State Machine Addendum records that prior handoff behavior did not fully preserve operator sequencing across review windows.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Future red-team windows classify lifecycle state from RED_TEAM_STATE_MACHINE.md before giving next steps and record the state in GitHub evidence.
Last reviewed: 2026-07-09
```

### chat memory treated as project truth

```text
Risk: chat memory treated as project truth
Status: Active / controlled by Phase 4J-5 protocol after merge
Evidence: Issue #24 Red-Team Operating Protocol Addendum states that chat memory, sandbox state, local scratch files, connector state, and unversioned notes are not source of truth.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Material decisions, approvals, rejections, assumptions, scope boundaries, and handoff states are recorded in GitHub issue evidence, PR evidence, committed project-control docs, GitHub PR comments/reviews, or owner-pasted terminal output.
Last reviewed: 2026-07-09
```

### red-team handoff gap before closeout

```text
Risk: red-team handoff gap before closeout
Status: Active / controlled by Phase 4J-5 handoff playbook after merge
Evidence: Issue #24 Operator State Machine Addendum identifies premature option lists before merge, main verification, and issue closeout as incorrect behavior.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: HANDOFF_PLAYBOOK.md startup and closeout sequence is followed before next-phase planning.
Last reviewed: 2026-07-09
```

### stale PR head SHA approval

```text
Risk: stale PR head SHA approval
Status: Active / controlled by SHA-bound marker and Phase 4J-5 state machine
Evidence: Phase 4J-3 requires the red-team marker to match the current PR head SHA; Issue #24 prohibits approval when the exact current PR head SHA is unknown.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Red-team verifies current PR head SHA before approval, and any later commit requires a fresh red-team decision for the new SHA.
Last reviewed: 2026-07-09
```

### non-durable approvals or conditions

```text
Risk: non-durable approvals or conditions
Status: Active / controlled by Phase 4J-5 protocol after merge
Evidence: Issue #24 requires every material approval, rejection, condition, assumption, scope boundary, and handoff state to be reflected in durable GitHub evidence or owner-pasted terminal output.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Red-team records where each material decision is or will be stored before treating it as durable.
Last reviewed: 2026-07-09
```

### future phase work without linked GitHub phase issue

```text
Risk: future phase work without linked GitHub phase issue
Status: Active / controlled by Phase 4J-1 after merge
Evidence: Phase initiation previously could occur through chat-only prompts; Phase 4J-1 adds issue template, PR template requirement, and PR contract enforcement.
Owner: ContractorOS project owner / development lead / red-team gate
Resolution condition: Phase 4J-1 is merged and future phase PRs link GitHub phase issues before review.
Last reviewed: 2026-07-08
```

### local commit not yet in GitHub source of truth

```text
Risk: local commit not yet in GitHub source of truth
Status: Mitigated for initial branch/PR creation; final resolution pending
Evidence: Owner installed/authenticated GitHub CLI for documentation PR setup, pushed branch, and opened PR #15. The correction commit still must be pushed, PR body updated, checks run, red-team review completed, approval obtained, merge completed, and main verified.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Branch pushed to GitHub, PR opened, GitHub Actions run, red-team review completed, human/write-access approval or approved automation lane rule satisfied, and main verified after merge.
Last reviewed: 2026-07-08
```

### Premature auto-merge before owner-trigger controls

```text
Risk: Premature auto-merge before owner-trigger controls
Status: Active / future control target
Evidence: Phase 4J-0 documents future lane-based automation only as a policy target; current owner approval remains required and auto-merge is not active.
Owner: ContractorOS project owner / development lead / red-team gate
Resolution condition: A future approved phase implements SHA-bound red-team markers, required checks, owner-trigger detection, and explicit lane eligibility before any auto-merge path is activated.
Last reviewed: 2026-07-08
```

### Prompt model/effort omitted from future work

```text
Risk: Prompt model/effort omitted from future work
Status: Active / controlled by prompt convention after merge
Evidence: Owner approved adding model/effort selection to every future prompt.
Owner: ContractorOS project owner / development lead / red-team gate
Resolution condition: PROMPT_CONVENTION.md is merged and future prompts follow it.
Last reviewed: 2026-07-08
```

### Codex bootstrap before AGENTS.md

```text
Risk: Codex bootstrap before AGENTS.md
Status: Active / Controlled by Phase 4J-0 constraints
Evidence: Phase 4J-0 creates AGENTS.md and AI governance files before AGENTS.md exists on the starting main SHA.
Owner: ContractorOS development lead / red-team gate / project owner
Resolution condition: Phase 4J-0 PR is reviewed by red-team, approved by human/write-access reviewer, merged without scope expansion, and main is verified.
Last reviewed: 2026-07-08
```

### developer connector path blocked after prohibited list-resource calls

```text
Risk: developer connector path blocked after prohibited list-resource calls
Status: Active / Controlled by bootstrap path
Evidence: Phase 4J-0 prompt records that the prior developer connector implementation path failed twice before implementation by calling api_tool.list_resources.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Future developer connector path is redesigned or explicitly cleared without broad discovery, list-resource, or tool-schema dump calls.
Last reviewed: 2026-07-08
```

### broad connector discovery recurrence

```text
Risk: broad connector discovery recurrence
Status: Active / Controlled by AGENTS.md and AI operating model
Evidence: Phase 4J-0 records a stop rule for missing direct tools and prohibits broad connector discovery, broad list-resource calls, and tool-schema dumps.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Future AI developer runs comply with AGENTS.md and record model runs in repo evidence.
Last reviewed: 2026-07-08
```

### automation misread as owner-judgment replacement

```text
Risk: automation misread as owner-judgment replacement
Status: Active / Controlled by Phase 4J-0 governance docs
Evidence: Phase 4J-0 defines 95% automation as reducing relay, paperwork, repetitive checks, and handoff while preserving owner judgment, red-team review, and human/write-access approval.
Owner: ContractorOS project owner / development lead / red-team gate
Resolution condition: Future automation phases preserve protected PR governance and do not add auto-merge or branch-protection bypass.
Last reviewed: 2026-07-08
```

### control gate lane mismatch for companion phase reports

```text
Risk: control gate lane mismatch for companion phase reports
Status: Active / Hotfix in review
Evidence: Product / QA changes require a current phase report, but docs/project-control/** was treated as Control / Infrastructure, causing valid Product / QA + phase report PRs to risk lane mismatch.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Phase 4I-A hotfix is reviewed, control-gate workflow passes, PR is approved, and main is verified after merge.
Last reviewed: 2026-07-08
```

### owner manual supervision burden

```text
Risk: owner manual supervision burden
Status: Active / Controlled by route documentation
Evidence: Project routing has required repeated owner copy/paste and manual supervision to move between developer work, red-team review, and protected merge.
Owner: ContractorOS owner / development lead / red-team gate
Resolution condition: GitHub Issue → Developer PR → Control Gates → Red-Team Decision → Human Approval → Merge route is adopted and verified without weakening branch protection.
Last reviewed: 2026-07-08
```

### dependencies use latest

```text
Risk: dependencies use latest
Status: Active
Evidence: apps/web/package.json uses latest for Vite, React, and React DOM. apps/mobile/package.json uses latest for expo, react, and react-native. Phase 4K-5 is blocked before mutation by unavailable node/npm tooling and does not implement dependency pinning or lockfile baseline work.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Dependencies are pinned or otherwise controlled under an approved reproducibility plan.
Last reviewed: 2026-07-09
```

### no clean public npm lockfile

```text
Risk: no clean public npm lockfile
Status: Active
Evidence: Phase reports and Phase 4K-5 inspection document no committed clean public npm lockfile for apps/web or apps/mobile. Phase 4K-5 creates no lockfile because npm is unavailable.
Owner: ContractorOS development lead / red-team gate
Resolution condition: A clean public npm lockfile is generated and verified before commit.
Last reviewed: 2026-07-09
```

### contaminated lockfiles generated locally

```text
Risk: contaminated lockfiles generated locally
Status: Active
Evidence: Prior local npm installs produced lockfiles with non-public registry references. Phase 4K-4 keeps contamination checks as a required stop condition for the recommended future baseline phase.
Owner: ContractorOS development lead / red-team gate
Resolution condition: No non-public registry reference appears in any committed lockfile.
Last reviewed: 2026-07-09
```

### 10 moderate npm vulnerabilities reported during mobile npm install

```text
Risk: 10 moderate npm vulnerabilities reported during mobile npm install
Status: Active
Evidence: Phase 4C and Phase 4D reports document npm audit output.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Dedicated dependency triage phase resolves or accepts the risk with evidence.
Last reviewed: 2026-07-07
```

### visual/device QA not yet complete

```text
Risk: visual/device QA not yet complete
Status: Active
Evidence: Runtime QA reached Metro locally but did not visually inspect a device or emulator.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved visual QA is completed and documented.
Last reviewed: 2026-07-07
```

### no APK build yet

```text
Risk: no APK build yet
Status: Active
Evidence: Prior phase reports explicitly exclude APK creation.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved Android build phase creates and verifies an APK.
Last reviewed: 2026-07-07
```

### no install test yet

```text
Risk: no install test yet
Status: Active
Evidence: No Android install test has been completed.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved install test is completed and documented.
Last reviewed: 2026-07-07
```

### CI automation not yet implemented

```text
Risk: CI automation not yet implemented
Status: Mitigated / monitor branch-protection behavior
Evidence: Phase 4G introduced control-gates workflow; Phase 4H verified workflow run on a protected PR; branch-protection behavior still depends on repository settings.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Required checks and review protections remain enforced on main and are observed across multiple PRs.
Last reviewed: 2026-07-08
```

### no full content system

```text
Risk: no full content system
Status: Active
Evidence: Current mobile app uses a minimal internal fixture placeholder only.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved content system architecture and implementation are completed.
Last reviewed: 2026-07-07
```

### no production/public MVP claim allowed

```text
Risk: no production/public MVP claim allowed
Status: Active
Evidence: Current work is internal-only and fixture-only.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Production/public MVP readiness claim remains blocked until explicit owner approval after required gates.
Last reviewed: 2026-07-07
```

### foundation scope file newly added but must remain living document

```text
Risk: foundation scope file newly added but must remain living document
Status: Active
Evidence: PROJECT_FOUNDATION.md is a control document, not implementation proof.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Foundation file remains updated as project evidence changes.
Last reviewed: 2026-07-07
```

### Phase One acceptance not yet achieved

```text
Risk: Phase One acceptance not yet achieved
Status: Active
Evidence: Acceptance criteria now exist, but evidence for all levels has not been completed.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Required acceptance levels are verified and documented.
Last reviewed: 2026-07-07
```

### release gates not yet passed

```text
Risk: release gates not yet passed
Status: Active
Evidence: Claim/release gates are defined but not completed.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Relevant gates are passed with evidence.
Last reviewed: 2026-07-07
```

### full project scope beyond Phase One remains future/controlled, not implemented

```text
Risk: full project scope beyond Phase One remains future/controlled, not implemented
Status: Active
Evidence: PROJECT_FOUNDATION.md lists long-term categories as not necessarily implemented.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Each future scope area is separately approved, implemented, and verified.
Last reviewed: 2026-07-07
```

### red-team files are visible in the same repo and could be misread as developer scope

```text
Risk: red-team files are visible in the same repo and could be misread as developer scope.
Status: Active / Controlled
Evidence: Red-team files are committed for auditability in GitHub.
Owner: ContractorOS development lead / red-team gate
Resolution condition: ROLE_BOUNDARIES.md and red-team README clearly mark them as reviewer/control files; developer must not treat them as implementation scope.
Last reviewed: 2026-07-07
```

### stale red-team approval after new PR commits

```text
Risk: stale red-team approval after new PR commits
Status: Active / controlled by Phase 4J-3 pull request workflow enforcement after merge
Evidence: Phase 4J-3 wires `scripts/control/check_red_team_marker.py` into the required pull request control-gates workflow and reruns the workflow on PR body edits. Without the matching current PR head SHA, the marker step fails.
Owner: ContractorOS development lead / red-team gate
Resolution condition: SHA-bound red-team marker validation remains required in protected PR control gates, and post-PR Actions evidence confirms stale markers fail.
Last reviewed: 2026-07-09
```

### owner-triggered work misclassified as low-risk automation

```text
Risk: owner-triggered work misclassified as low-risk automation
Status: Active / controlled by Phase 4J-4 pull request workflow enforcement after merge
Evidence: Phase 4J-4 defines the `OWNER_TRIGGER_REVIEW` marker and validates owner interruption status, trigger categories, lane eligibility, human approval, and auto-merge eligibility in pull request control gates.
Owner: ContractorOS development lead / red-team gate / human approver
Resolution condition: Owner-trigger marker validation remains required in protected PR control gates, and future automation phases refuse to treat legal, financial, paid-service, public-release, production/readiness, app-store/build/distribution, scope expansion, unresolved red-team BLOCKED, dependency/security risk acceptance, or architecture-threshold PRs as future-low-risk candidates.
Last reviewed: 2026-07-09
```

### malformed nested continuity evidence bypasses the documented exit contract

```text
Risk: Malformed nested continuity evidence reaches comparison, rendering, or output code and raises an unbounded runtime error instead of a deterministic fail-closed result.
Status: Active / controlled in C3.2 developer review
Evidence: The 1.3.2 collector validates exact repository, issue, PR, check, workflow-run, job, step, marker, auto-merge, and optional source-command shapes with bounded list sizes before use. Behavior and CLI tests cover wrong types, missing fields, unknown properties, invalid identifiers, exit 5, and absence of tracebacks.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: The C3.2 exact head passes the full suite, deterministic/schema checks, all local and PR-context controls, live collection, contradictory-repository classification, and a fresh external whole-PR exact-SHA review.
Last reviewed: 2026-07-12
```

### C3.5 staged evidence, provenance, and lifecycle binding

```text
Risk: A four-field live review structure, implicit untracked-file status, moving worktree head, contradictory approval claims, or inconsistent issue closeout timestamp could appear authoritative without fail-closed reduction.
Status: Active / controlled in C3.5 developer validation
Evidence: Collected and evaluated review contracts are distinct; all-untracked status hashes and exact heads are paired before/after collection; final claims are recomputed and compared; `closedAt` and normalized closeout state are lifecycle-bound.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: C3.5 exact head passes focused and complete tests, deterministic/schema checks, all controls, live collection, new-head workflow inspection and fresh whole-PR exact-SHA review.
Last reviewed: 2026-07-12
```

### C3.6 command, reason-map, schema, and accounting equivalence

```text
Risk: A broad GitHub command, canonical reviewer-key collision, schema/runtime reason mismatch, or understated source-command bound could make malformed or expanded evidence appear authoritative.
Status: Active / controlled in C3.6 developer validation
Evidence: The collector accepts only current-invocation exact command vectors, preserves original reason keys until one-to-one canonical validation succeeds, separates `_evidence` from reviewer-key reason schemas, and derives the 119-command limit from named bounds.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: C3.6 exact head passes focused and complete tests, determinism and schema-contract checks, all controls, live collection, new-head workflow inspection, and fresh whole-PR exact-SHA review.

### C3.7 adverse-review or source-command semantic false positive

Risk: A qualifying approval can mask another reviewer's unresolved exact-current-head change request, or structurally valid command metadata can claim prohibited, unrelated, mismatched, unsourced, or unsuccessful reads and still appear authoritative.
Status: Active / controlled in C3.7 developer validation
Evidence: Reviewer-wide latest-decisive reduction makes unresolved current-head changes requested adverse without storing review bodies; claim-sensitive aggregate checks forbid merge-ready and closed-gate success. Nonempty source-command histories are checked against the exact evidence-derived live firewall and require zero return codes.
Validation: Approval-plus-adverse, no-prior-approval, comment/approval/dismissal, stale-head, aggregate-decision, merge-ready, closed-gate, private-content, mutation, identity, page, permission-source, argument-order, return-code and no-output tests.
Resolution condition: C3.7 exact head passes focused and complete tests, deterministic/schema checks, all local and PR-context controls, exact-head workflow inspection, outside-repository live collection, PR reconciliation, and fresh whole-PR exact-SHA review.
Last reviewed: 2026-07-12
```

### C3.8 pre-validation dereference or provenance/schema mismatch

```text
Risk: Malformed review evidence can be dereferenced by semantic command validation before structural validation, canonical source provenance can be absent, or a nonzero command result can satisfy the evidence schema despite runtime rejection.
Status: Active / controlled in C3.8 developer validation
Evidence: Review validation now precedes semantic firewall derivation; canonical_ref uses a dedicated required exact-SHA contract in runtime and both schemas; command results require runtime integer zero and schema const zero.
Validation: Direct-generation and CLI malformed-review matrices, null/missing/abbreviated/uppercase/malformed canonical refs, active/closed output generation, firewall non-construction, return-code type/value cases, and standard-library schema assertions.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: C3.8 exact head passes focused and complete tests, determinism and schema checks, all local and PR-context controls, exact-head workflow inspection, outside-repository live collection, PR reconciliation, and fresh whole-PR exact-SHA review.
Last reviewed: 2026-07-12
```

### live repository contradiction is mistaken for unavailable evidence

```text
Risk: A readable, structurally valid different repository name is reported as unavailable evidence and bypasses the intended identity-quarantine path.
Status: Active / controlled in C3.2 developer review
Evidence: Structural validation now accepts syntactically valid owner/repository names without substituting the requested name; comparison classifies a different observed identity as quarantined with exit 2. Missing or malformed names remain unavailable with exit 3.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: Offline contradictory-repository behavior, live current-repository behavior, complete controls, and fresh exact-SHA review all pass on the C3.2 head.
Last reviewed: 2026-07-12
```

### scope-bound authority fields are present but not classification-bound

```text
Risk: Collected local-head, default-branch, nullable live-field, review-timestamp, or canonical lifecycle evidence is structurally present but does not constrain classification, allowing stale or malformed authority evidence to appear safe.
Status: Active / controlled in C3.3 developer review
Evidence: The historical 1.3.3 collector scope-binds active and closed source identities, requires nullable authoritative live field presence, treats only null auto-merge requests as inactive, validates decisive RFC3339 review timestamps before approval selection, and compares validated canonical lifecycle and consistency values.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: C3.3 exact head passes focused and complete tests, deterministic/schema checks, all controls, live collection, new-head workflow inspection and fresh whole-PR exact-SHA review.
Last reviewed: 2026-07-12
```

### C3.4 evidence identity and provenance binding

```text
Risk: Permission response identity, executable worktree provenance, normalized review structure, timestamp ordering, closeout timestamp, or closed-gate base evidence could be misattributed or malformed while appearing authoritative.
Status: Active / controlled in C3.4 developer validation
Evidence: Case-folded response/candidate identity binding, before/after clean worktree hashes, exact bounded review schema, UTC ordering, RFC3339 `closedAt`, and verified-default-branch closed-gate base binding are implemented and covered by focused adversarial tests.
Owner: ContractorOS development lead / external red-team gate
Resolution condition: C3.4 exact head passes focused and complete tests, deterministic/schema checks, all controls, live collection, new-head workflow inspection and fresh whole-PR exact-SHA review.
Last reviewed: 2026-07-12
```
