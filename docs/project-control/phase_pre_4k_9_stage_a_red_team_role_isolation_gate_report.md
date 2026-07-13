# Pre-4K-9 Stage A Red-Team Role-Isolation Gate Report

## Linked Phase Issue

Closes #55

## Linked Issues

- Implementation authority scope: Issue #55.
- Parent planning and security-requirements record: Issue #53.
- Issue #49 is closed and PR #50 is merged; neither is modified by this work.

## Phase

Pre-4K-9 Stage A — Actor-Bound Red-Team Role Contract and Anti-Drift Validator.

## Stage

Stage A deterministic repository and startup-packet enforcement in review. Full runtime isolation is not proven.

## Lane

Control / Infrastructure

## Scope

Implement only the Issue #55 actor-role contract, continuity integration, schemas, fixtures, tests, and allowlisted public-safe governance reconciliation. Stage B, Issue #54, Phase 4K-9, Phase 4I, product, dependency, workflow, control-script, credential, deployment, release, approval, merge, and closeout work are excluded.

## Starting Main SHA

`7d00343c233e45185e6c4d77e50eb870f408c01f`

## Correction Authority Scope And Exact-SHA Boundary

PR #56 was created on `stage-a-red-team-role-isolation`. Within the correction scope, formal review `4687524310` by the separate `Zest-LeadGen` reviewer returned `CHANGES_REQUESTED` for exact head `18ddffae1c2781ccb560bad7a8a468d4e8822f57` with two blocking findings: Issue #55 live construction used the Issue #49 authority source, and actor routing depended on PR open/closed state instead of validated lifecycle evidence.

That decision authorizes only this bounded developer-correction scope. The correction commit creates a different PR head, so the old decision cannot approve it. The correction head SHA is intentionally live-derived after commit and push because a commit cannot contain its own final SHA. Fresh whole-PR external exact-SHA review remains required for the new head.

## Actor Assignment

`CODEX_DEVELOPER` implements Issue #55 only. External exact-SHA red-team review, human/write-access approval, merge operation, verified-main verification, and issue closeout remain separate roles with no developer authority overlap.

## Exact File Allowlist

The Issue #55 exact allowlist controls. No wildcard expansion or substitute path is permitted. The final exact changed-file list is recorded in `Changed Files` after validation.

## Changed Files

Thirty changed paths are currently present and every path is verbatim allowlisted by Issue #55:

- `AGENTS.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/HANDOFF_PLAYBOOK.md`
- `docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md`
- `docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md`
- `docs/project-control/RED_TEAM_CONTINUITY_ARCHITECTURE.md`
- `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
- `docs/project-control/RED_TEAM_ROLE_CONTRACT.md`
- `docs/project-control/RED_TEAM_STARTUP_PACKET_SPEC.md`
- `docs/project-control/RED_TEAM_STATE_MACHINE.md`
- `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/SOURCE_REGISTER.md`
- `docs/project-control/VALIDATION_TASKS.md`
- `docs/project-control/phase_pre_4k_9_stage_a_red_team_role_isolation_gate_report.md`
- `docs/project-control/state/contractoros-state.yaml`
- `docs/project-control/state/red-team-continuity-evidence.schema.json`
- `docs/project-control/state/red-team-startup-packet.schema.json`
- `scripts/continuity/README.md`
- `scripts/continuity/red_team_continuity.py`
- `scripts/continuity/role_contract.py`
- `scripts/continuity/tests/fixtures/active_pr_requires_live_verification.json`
- `scripts/continuity/tests/fixtures/consistent_closed_gate.json`
- `scripts/continuity/tests/fixtures/expected_startup_packet.md`
- `scripts/continuity/tests/fixtures/missing_evidence.json`
- `scripts/continuity/tests/fixtures/moved_pr_head.json`
- `scripts/continuity/tests/fixtures/stale_main.json`
- `scripts/continuity/tests/fixtures/unsafe_private_value.json`
- `scripts/continuity/tests/test_red_team_continuity.py`
- `scripts/continuity/tests/test_role_contract.py`

## Actor-Bound Startup Contract

Version `1.4.0` makes actor evidence mandatory in newly generated packets. Program direction is not actor authority. Repository, issue, pull request, branch, exact SHA, lifecycle, authority-source scope, observation time, actor actions, and next authorized actor are deterministically bound. A single canonical mapping now supplies `GITHUB_ISSUE_49` for Issue #49 / PR #50 and `GITHUB_ISSUE_55` for Issue #55 / PR #56 to both construction and expected-context validation; crossed or unsupported pairs fail closed.

Open lifecycle routing now advances from external exact-SHA review to separate human approval and then merge operator only when each prior evidence gate is valid. Merged-but-unverified and verified-main/open-issue states authorize no actor mutation action and do not collapse merge, verified main, or issue closeout.

## Red-Team Role Declaration

Red-team scope fixes repository write, GitHub write, and terminal mutation power to `NONE`; implementation, human approval, merge, and issue closeout to `NO`; prompt authoring and separately authorized exact-SHA review to `YES`.

## Role-Conflict Handling

Missing, unknown, stale, duplicate, malformed, or contradictory governing evidence denies the action, records stable public-safe reasons, and enters `ROLE_CONFLICT` plus `REPAIR_REQUIRED`. Broader authority scope is never selected.

## Role-Repair State

Red-team repair may return only `READ_ONLY_ROLE_RESTORED` and preserves no write, implementation, approval, merge, or closeout power. The original incident and denial reasons remain.

## Incident Evidence

Mutation attempts are denied and represented only by bounded enumerated public-safe fields. Raw commands, absolute home paths, secrets, credentials, customer data, private legal or financial material, and private reasoning are excluded.

## Determinism Evidence

Two independent fixed-time runs at `2026-07-13T00:05:00Z` generated byte-identical evidence JSON and packet Markdown. The generated file SHA-256 values were:

- `continuity-evidence.json`: `08be644192bd04a46ba4b12d27cc0d59af53918e1b42e50daf40f4dc13e0568d`
- `RED_TEAM_STARTUP_PACKET.md`: `1c2e1e632ce2c45a4aacfde0fdc9bb72f58c231c3428494f3ec7edca27994193`
- recorded and independently recomputed packet hash: `323aa08fb007ec951edf992cd462b46f62070c7b516b629bc02e78f448fb9907`

Changing only `actor_contract.PROGRAM_NEXT_ACTION` changed the packet hash to `b77e7b487c2e79a2c8d631bd5585abc076ce1db3d58df9bc2f18bf082c37a01d`, proving actor-contract material participates in hashing.

## Security Test Evidence

Packet 2 role-contract self-test passed. The dedicated role-contract suite passed 40 test methods, including bounded authority scope, action-class, stale-binding, repair, incident, privacy, ordering, and CLI matrices.

## Functional Test Evidence

Packet 3 actor-contract integration tests passed 7 test methods. The correction-specific Issue #55 authority-scope/lifecycle matrix passed 16 test methods, including mocked Issue #55 live construction, both authority mappings, three active actor transitions, two verification-only states, stale/malformed/adverse marker cases, missing/pending/failed checks, self-approval rejection, contradictory actions, schema assertions, and incomplete merge evidence.

## Existing Continuity Regression Evidence

The full continuity suite passed 399 tests after the correction: the prior 383 plus 16 focused regressions. Existing Issue #49 classifications and failure precedence remain intact.

## Schema Evidence

Both Draft 2020-12 JSON schema files parse with the Python standard library. Actor fields are required, enumerated, bounded, and the red-team authority profile is conditionally fixed within schema scope.

## Documentation Reconciliation

Every changed governance record is bounded below. Each entry grants no new authority scope.

| FILE | RECONCILIATION_REASON | AUTHORITATIVE_SOURCE_SCOPE | EXACT_CHANGE_BOUNDARY | NEW_AUTHORITY_GRANTED |
|---|---|---|---|---|
| `AGENTS.md` | Make actor-bound startup behavior durable. | Issue #55 | One Stage A startup-scope section. | NO |
| `HANDOFF_PLAYBOOK.md` | Require actor fields in red-team handoffs. | Issue #55 | Startup checks and handoff template only. | NO |
| `RED_TEAM_CONTINUITY_ARCHITECTURE.md` | Replace stale Issue #49 review state and record Stage A/Stage B boundary. | Live Issue #49/PR #50 evidence and Issue #55 | Final Issue #49 paragraph plus one Stage A section. | NO |
| `RED_TEAM_OPERATING_PROTOCOL.md` | Define conflict, repair, and actor-action separation. | Issue #55 and normative role contract | One actor-bound scope section. | NO |
| `RED_TEAM_STARTUP_PACKET_SPEC.md` | Version and specify actor evidence in generated packets. | Issue #55 and `1.4.0` implementation | Status, inputs, actor section, determinism, content, and schema boundaries. | NO |
| `RED_TEAM_STATE_MACHINE.md` | Add deterministic actor role states before lifecycle action. | Issue #55 | One four-state table and separation rule. | NO |
| `REQUIREMENTS_TRACEABILITY_MATRIX.md` | Trace Issue #55 requirements to evidence. | Issue #55 | Ten Stage A rows. | NO |
| `RISK_REGISTER.md` | Record five Stage A risk families. | Issue #55 | Five appended public-safe risk records. | NO |
| `SOURCE_REGISTER.md` | Register live Issue #53/#55 and prerequisite sources. | GitHub issues, PR #50, prompt convention | Five Stage A source rows. | NO |
| `VALIDATION_TASKS.md` | Make Stage A acceptance evidence durable. | Issue #55 | Eight Stage A validation rows. | NO |
| `DEVELOPMENT_LEDGER.md` | Record active Stage A work and Issue #49 merge evidence. | Live GitHub preflight | One active entry and two Issue #49 status lines. | NO |
| `PROJECT_IMPLEMENTATION_ROADMAP.md` | Reconcile Issue #49 and insert Stage A before Phase 4K-9. | Live GitHub evidence and Issue #55 | Issue #49 status plus one Stage A section. | NO |
| `PROJECT_VISION_AND_PHASE_TRACKER.md` | Replace stale current snapshot without inflating program capability. | Live GitHub evidence and Issue #55 | Historical Issue #49 status plus current Stage A snapshot. | NO |
| `state/contractoros-state.yaml` | Reconcile the observed snapshot to open PR #56 and the rejected exact head. | Live PR/review preflight | Current main, open PR, rejected head, correction-head live-verification rule, lifecycle, blockers, evidence IDs, and references. | NO |
| `state/red-team-continuity-evidence.schema.json` | Require bounded actor input/result evidence. | Issue #55 and runtime contract | `1.4.0` version, properties, and actor definitions. | NO |
| `state/red-team-startup-packet.schema.json` | Require actor input/result fields in the packet schema. | Issue #55 and runtime contract | `1.4.0` version and two required references. | NO |

`docs/project-control/DECISION_LOG.md: reviewed, no update required`

`docs/project-control/RISK_REGISTER.md: reviewed, no update required`

## Documentation Impact

The normative role contract, startup specification, continuity architecture, handoff protocol, state machine, traceability, risks, sources, validations, ledger, roadmap, tracker, canonical state, and this report are reviewed within the exact allowlist. No product or operational capability progress is inferred.

## Risk Register Impact

The allowlisted risk register records program-direction confusion, role-repair overreach, stale actor binding, incident leakage, and Stage A overclaim risks.

## Decision Log Impact

`docs/project-control/DECISION_LOG.md: reviewed, no update required`

Issue #55 and `RED_TEAM_ROLE_CONTRACT.md` are the durable decision sources within this scope; the non-allowlisted decision log is not changed.

## Artifact Index Impact

No artifact-index file is allowlisted. The normative contract and this report are directly versioned under `docs/project-control/` and require no separate artifact-index change.

## Validation Evidence

The correction rerun passed the six-case role self-test, all 40 dedicated role-contract test methods, all 7 focused actor-integration test methods, all 16 focused Issue #55 correction tests, and all 399 continuity tests. Both schemas parse as JSON. Fixed-time generated outputs compare byte for byte, independent hash recomputation agrees, and an actor-contract mutation changes the hash.

## Validation Commands and Results

All Issue #55 focused, full-suite, schema, existing-control, allowlist, privacy, determinism, unstaged-diff, and staged cached-diff commands pass. Exact-current-head GitHub inspection is retained for the post-push packet.

## Privacy and Evidence-Safety Validation

Synthetic rejection-test inputs include a non-secret example home path so the validator proves it is denied; no such value appears in generated evidence or the PR/report evidence.

```text
PUBLIC_SAFE_EVIDENCE_CHECK=PASS
SECRET_LIKE_VALUE_FOUND=NO
PRIVATE_PATH_FOUND=NO
PRIVATE_CHAIN_OF_THOUGHT_FOUND=NO
```

## Commands Run

Read-only identity/SHA/issue/PR preflight, baseline suite, role self-test, focused role tests, focused integration tests, full continuity suite, schema parsing, deterministic fixture generation, byte comparison, independent hash recomputation, actor-change sensitivity, privacy review, local control validators, and Git whitespace validation were run. Exact command results are retained in this report and the PR handoff; exact-head GitHub inspection remains after push.

## Dependency / Lockfile Handling

No package, dependency, package installation, dependency installation, manifest, or lockfile change is authorized or performed.

## Forbidden Scope Confirmation

- [x] No workflow or control-script change.
- [x] No dependency, lockfile, product, app, backend, database, build, deployment, release, credential, permission, paid-service, Stage B, Issue #54, Phase 4K-9, or Phase 4I change.
- [x] No self-review, red-team marker, human approval, auto-merge, merge, verified-main claim, or issue closeout.

## Known Limitations

Stage A validates deterministic interpretation inside repository evidence and startup-packet generation. It does not prove infrastructure-level removal of tools, credentials, network access, mutable worktrees, wrapper or alias escapes, or runtime action-firewall enforcement.

## Stage A Claim Level

```text
ACTOR_BOUND_ROLE_CONTRACT=IMPLEMENTED_IN_REVIEW
FULL_RUNTIME_ISOLATION=NOT_PROVEN
STAGE_B_REQUIRED=YES
```

## Claim Level

Source and command behavior is verified within reported local Stage A tests only. The rejected old head has a durable `CHANGES_REQUESTED` decision; fresh external exact-SHA review and human approval for the correction head are pending. The PR remains unmerged and full runtime isolation is not proven.

## Stage B Remaining Requirements

Dedicated least-privilege read-only principal, infrastructure-level write-tool removal, immutable repository access, credential isolation, external action firewall, audit enforcement, and mutation-escape testing require a separate future issue and file scope.

## Red-Team Status

Formal review `4687524310` records `CHANGES_REQUESTED` for rejected head `18ddffae1c2781ccb560bad7a8a468d4e8822f57`. No developer-authored replacement marker or passing decision is added. The correction head requires fresh whole-PR external exact-SHA review.

## Human Approval Status

Not granted; zero qualifying human approvals are claimed for the correction head.

## Merge Status

Unmerged. Codex has no merge authority scope.

## Auto-Merge Status

Disabled and ineligible.

## Issue Status

Issue #55 remains open. Parent Issue #53 remains open and planning-only.

## Phase 4K-9 Status

Not started.

## Phase 4I Status

Paused.

## Next Authorized Actor Scope

After the correction commit and push, `EXTERNAL_EXACT_SHA_RED_TEAM` is the only next authorized actor in scope. The old `CHANGES_REQUESTED` review grants no approval, human-approval, merge, verified-main, or closeout power for the new head.

## Next Phase Status

Stage B, Issue #54, Phase 4K-9, and Phase 4I are not started or resumed. No next phase may begin from this report.

## OWNER_TRIGGER_REVIEW marker

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Stage A changes the actor and authority contract used by red-team startup packets and lifecycle handoffs. It must receive external exact-SHA red-team review and a separate human write-access approval. It grants no Stage B runtime-isolation claim, Phase 4K-9 authority, Phase 4I authority, credential authority, release authority, spending authority, auto-merge authority, or control-bypass authority.
