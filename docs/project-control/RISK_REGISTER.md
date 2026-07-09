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

## Active Risks

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
Evidence: apps/mobile/package.json uses latest for expo, react, and react-native.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Dependencies are pinned or otherwise controlled under an approved reproducibility plan.
Last reviewed: 2026-07-07
```

### no clean public npm lockfile

```text
Risk: no clean public npm lockfile
Status: Active
Evidence: Phase reports document no committed clean public npm lockfile for apps/mobile.
Owner: ContractorOS development lead / red-team gate
Resolution condition: A clean public npm lockfile is generated and verified before commit.
Last reviewed: 2026-07-07
```

### contaminated lockfiles generated locally

```text
Risk: contaminated lockfiles generated locally
Status: Active
Evidence: Prior local npm installs produced lockfiles with non-public registry references.
Owner: ContractorOS development lead / red-team gate
Resolution condition: No non-public registry reference appears in any committed lockfile.
Last reviewed: 2026-07-07
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
