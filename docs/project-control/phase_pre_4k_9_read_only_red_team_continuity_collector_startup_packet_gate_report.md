# Pre-4K-9 Read-Only Red-Team Continuity Collector / Startup Packet Gate Report

## Linked Phase Issue

Closes #49

## Phase

Pre-4K-9 — Read-Only Red-Team Continuity Evidence Collector / Startup Packet Gate.

## Lane

Control / Infrastructure

## Scope

Implement a Python standard-library-only read-only continuity evidence collector with fixture and live modes, deterministic JSON evidence, a deterministic derived Markdown startup packet, fail-closed classifications, external-output enforcement, sensitive-data rejection, schemas, fixtures, tests, and required project-control reconciliation.

This report records implementation in review. Merged capability is not yet proven.

## Starting Main SHA

`01b90ab8b12416101b4be067794bf543a3488779`

## Prior Phase Evidence

- Issue #47: closed with state reason `COMPLETED`.
- PR #48: merged; reviewed head `8a81d429a93a342527e0efe7962f9bfef22d22d4`.
- PR #48 merge commit: `01b90ab8b12416101b4be067794bf543a3488779`.
- ContractorOS Control Gates run `29176103821`: completed/success for the reviewed head.

## Source Anchors

- Issue #49: https://github.com/Zest-LeadGen/contractoros-california/issues/49
- Issue #47 closeout: https://github.com/Zest-LeadGen/contractoros-california/issues/47
- PR #48: https://github.com/Zest-LeadGen/contractoros-california/pull/48
- Prior successful run: https://github.com/Zest-LeadGen/contractoros-california/actions/runs/29176103821
- Starting main: `01b90ab8b12416101b4be067794bf543a3488779`
- Issue #49 owner amendments: comments `4950672136`, `4950911091`, `4950952134`, `4950969409`, and `4950978131`.
- OpenAI Codex Models: https://developers.openai.com/codex/models/ — verified 2026-07-12.
- OpenAI Codex Pricing: https://developers.openai.com/codex/pricing/ — verified 2026-07-12.
- ChatGPT Learn Speed: https://learn.chatgpt.com/docs/agent-configuration/speed — verified 2026-07-12.
- Governance-hardening workflow run `29203963944`: https://github.com/Zest-LeadGen/contractoros-california/actions/runs/29203963944
- G1.1 correction workflow run `29205093385`: https://github.com/Zest-LeadGen/contractoros-california/actions/runs/29205093385

## Changed Files

The current permitted 32-file branch set is:

1. `scripts/continuity/red_team_continuity.py`
2. `scripts/continuity/README.md`
3. `scripts/continuity/tests/test_red_team_continuity.py`
4. `scripts/continuity/tests/fixtures/consistent_closed_gate.json`
5. `scripts/continuity/tests/fixtures/active_pr_requires_live_verification.json`
6. `scripts/continuity/tests/fixtures/stale_main.json`
7. `scripts/continuity/tests/fixtures/moved_pr_head.json`
8. `scripts/continuity/tests/fixtures/missing_evidence.json`
9. `scripts/continuity/tests/fixtures/unsafe_private_value.json`
10. `scripts/continuity/tests/fixtures/expected_startup_packet.md`
11. `docs/project-control/RED_TEAM_STARTUP_PACKET_SPEC.md`
12. `docs/project-control/state/red-team-continuity-evidence.schema.json`
13. `docs/project-control/state/red-team-startup-packet.schema.json`
14. `docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md`
15. `docs/project-control/ARTIFACT_INDEX.md`
16. `docs/project-control/AUTOMATION_PHASE_ROADMAP.md`
17. `docs/project-control/DECISION_LOG.md`
18. `docs/project-control/DEVELOPMENT_LEDGER.md`
19. `docs/project-control/HANDOFF_PLAYBOOK.md`
20. `docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md`
21. `docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md`
22. `docs/project-control/RED_TEAM_CONTINUITY_ARCHITECTURE.md`
23. `docs/project-control/RED_TEAM_STATE_MACHINE.md`
24. `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
25. `docs/project-control/RISK_REGISTER.md`
26. `docs/project-control/SOURCE_REGISTER.md`
27. `docs/project-control/VALIDATION_TASKS.md`
28. `docs/project-control/state/contractoros-state.yaml`
29. `AGENTS.md`
30. `docs/project-control/PROMPT_CONVENTION.md`
31. `docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md`
32. `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`

The G1.1 correction packet changes exactly these seven existing files:

1. `docs/project-control/PROMPT_CONVENTION.md`
2. `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
3. `docs/project-control/SOURCE_REGISTER.md`
4. `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
5. `docs/project-control/VALIDATION_TASKS.md`
6. `docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md`
7. `scripts/continuity/tests/test_red_team_continuity.py`

The C1A marker-semantics packet changes exactly these five existing files:

1. `scripts/continuity/red_team_continuity.py`
2. `scripts/continuity/tests/test_red_team_continuity.py`
3. `docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md`
4. `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
5. `docs/project-control/VALIDATION_TASKS.md`

The C1B required-check and workflow-provenance packet changes exactly these sixteen existing files:

1. `scripts/continuity/red_team_continuity.py`
2. `scripts/continuity/README.md`
3. `scripts/continuity/tests/test_red_team_continuity.py`
4. `scripts/continuity/tests/fixtures/consistent_closed_gate.json`
5. `scripts/continuity/tests/fixtures/active_pr_requires_live_verification.json`
6. `scripts/continuity/tests/fixtures/stale_main.json`
7. `scripts/continuity/tests/fixtures/moved_pr_head.json`
8. `scripts/continuity/tests/fixtures/missing_evidence.json`
9. `scripts/continuity/tests/fixtures/unsafe_private_value.json`
10. `scripts/continuity/tests/fixtures/expected_startup_packet.md`
11. `docs/project-control/RED_TEAM_STARTUP_PACKET_SPEC.md`
12. `docs/project-control/state/red-team-continuity-evidence.schema.json`
13. `docs/project-control/state/red-team-startup-packet.schema.json`
14. `docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md`
15. `docs/project-control/VALIDATION_TASKS.md`
16. `docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md`

No workflow, existing control script, package manifest, lockfile, application, mobile, web, backend, database, build, release, content, production, credential, cloud, hosted-service, or paid-resource file changed.

## Commands Run

Bootstrap and source-of-truth verification included:

- `git status --short --branch`
- `git branch --show-current`
- `git rev-parse HEAD`
- startup-scope `git fetch origin main` evidence refresh
- `git rev-parse main`
- `git rev-parse origin/main`
- direct `gh issue view`, `gh pr view`, `gh run view`, `git ls-remote`, and `gh pr list` reads required by the developer prompt
- `git switch -c pre-4k-9-read-only-continuity-collector 01b90ab8b12416101b4be067794bf543a3488779`
- bootstrap report validators, commit, push, and non-draft PR creation

Implementation validation run so far included:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/continuity/tests -p 'test_*.py'`
- two identical consistent-fixture CLI generations and byte comparisons
- explicit active, stale, moved-head, missing, unsafe and malformed CLI runs
- independent packet-hash recomputation
- `python3 -m json.tool` for both schemas
- `python3 scripts/control/check_forbidden_scope.py`
- the required live starting-main stale baseline command recorded below
- 32 focused C1A marker-semantics tests
- the full 87-test continuity suite
- 28 focused C1B workflow-provenance tests
- the full 115-test continuity suite
- live C1B verification against Issue #49, PR #50 and run `29205653852`

The full current-control sequence remains required immediately before the implementation commit.

## Dependency / Lockfile Handling

No package was installed. The implementation uses only the Python standard library. No dependency declaration, package manifest, lockfile, dependency directory, or package-manager configuration changed.

## Collector Architecture

The CLI exposes `fixture` and `live` subcommands. Fixture mode reads a bounded JSON fixture. Live mode requires an explicit repository root, repository identity, issue number, PR number, workflow-run ID, exact canonical ref, observation timestamp, and external output directory.

Live mode reads bounded local Git metadata and narrowly selected GitHub CLI JSON fields. It compares canonical state with live main, issue, PR, head, checks, run, marker, approval, auto-merge, merge and closeout evidence. It renders exactly two derived files outside the repository using safe atomic replacement.

Supported classifications are exactly `consistent`, `requires_live_verification`, `stale`, `blocked`, and `quarantined`.

C1A replaces permissive marker summaries with one bounded parser and two semantic evaluators. Both marker types ignore fenced and HTML-comment examples, reject duplicate fields, reject duplicate or conflicting governing blocks, preserve stable reason ordering, and never use first-marker-wins or last-marker-wins behavior. The red-team evaluator enforces exact required fields, numeric PR binding, full current SHA binding, decisions, date shape and SHA-bound statement. The owner evaluator enforces fields, enumerations, category consistency, lane consistency, human approval `YES`, auto-merge `NO`, and non-empty rationale. The collector does not import or execute either control validator.

C1B adds one deterministic workflow evaluator. It binds the bounded GitHub repository field, workflow name `ContractorOS Control Gates`, workflow database ID `309083557`, `pull_request` event, PR head SHA and branch, exact-run PR check link, one `contractoros-control-gates` job and the ordered governed step matrix. Missing required job or step evidence is blocked. Mismatches, duplicates, ordering errors, pre-marker failures, premature post-marker success, unexplained failures and run/check/step contradictions are quarantined. Pending runs cannot support approval or completed-gate claims. This does not implement remote normalization, collaborator permission, human-approval qualification, merge logic or inaccessible-evidence exit remapping.

Exit contract:

- `0`: safe `consistent` or valid `requires_live_verification` packet generated.
- `2`: `stale` or `quarantined` evidence.
- `3`: required evidence missing or inaccessible, classified `blocked`.
- `4`: unsafe/private evidence or prohibited output path.
- `5`: invalid arguments, malformed input, malformed canonical state, or schema failure.

No stale, blocked, quarantined, or unsafe result returns exit `0`.

## Read-Only Command Boundary

Every subprocess uses an argument array, `shell=False`, a finite timeout, captured output, and normalized return-code evidence. The positive allowlist permits only the exact documented Git metadata reads and narrowly shaped `gh repo view`, `gh issue view`, `gh pr view`, `gh pr checks`, and `gh run view` JSON reads.

Unknown executables, subcommands, flags, and command shapes are rejected. Git remote-ref, branch, index, worktree, and remote mutations are forbidden at collector runtime. GitHub API and issue, PR, review, approval, merge, and closeout mutations are forbidden at collector runtime.

## Evidence Schema

`red-team-continuity-evidence.schema.json` uses Draft 2020-12 and defines required version, time, repository, source SHA, command-result, canonical, live-state, comparison, blocker, missing-evidence, classification, quarantine, public-safe, packet-hash and structured-packet fields. C1B migrates fixture, evidence, packet and generator contracts to `1.1.0` and requires PR head branch, check link, workflow identity/event/head branch, bounded jobs and numbered step status/conclusion. Nested bounded objects use `additionalProperties: false` where the runtime structure is controlled.

Standard-library runtime validation checks the bounded fixture and required canonical-state shape. No third-party schema validator or dependency was added.

## Startup Packet Specification

`RED_TEAM_STARTUP_PACKET_SPEC.md` defines input provenance, command security, lifecycle-sensitive classification, exit codes, deterministic normalization, output protection, sensitive-data rejection, packet content, schemas, and the no-decision-power boundary.

The packet identifies source SHAs, issue/PR/run evidence, exact head, checks, markers, approval state, auto-merge state, classification, findings, blockers, gaps, one next action, stop conditions, prohibited actions, public-safe status, and packet hash. It grants no write permission.

## Determinism Evidence

At fixed observation time `2026-07-12T02:55:00Z`, two consistent-fixture runs produced:

- JSON byte comparison: exit `0` from `cmp`.
- Markdown byte comparison: exit `0` from `cmp`.
- Packet hash from both runs: `7e5501d2fb20e23fa506d76aa19217ab48812990fef8fa933752763f689ca1f0`.
- Independent packet-hash recomputation: `MATCH`.

Hash normalization is UTF-8, LF newlines, stable headings, stable list and JSON ordering, no trailing whitespace, exactly one final newline, and exclusion of the displayed hash heading/value from the hash payload.

## Security Test Evidence

The 115-test suite includes the prior 87 tests plus 28 C1B workflow-provenance tests. It covers collector command/output security; governance hardening; marker semantics; repository/workflow/event/head/branch/check-link binding; job and step presence, duplication, status and order; pre-marker and post-marker matrices; pending evidence; expected and unknown check contradictions; unexplained failures; unknown contradictory steps; deterministic classification; and prior-head workflow truthfulness.

The forbidden-scope validator passed after the security-control literals were kept on explicitly forbidden, blocked, no-authority, or risk lines.

## Functional Test Evidence

Observed explicit CLI exit matrix:

- consistent closed gate: `0`
- active PR requiring live verification: `0`
- stale main: `2`
- moved PR head: `2`
- missing evidence: `3`
- unsafe/private evidence: `4`
- malformed JSON: `5`

The 32-test focused marker class and full 87-test suite passed in the C1A validation sequence. The 28-test focused workflow-provenance class and full 115-test suite passed in the C1B implementation sequence.

## Baseline Stale-State Evidence

Command:

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/continuity/red_team_continuity.py live \
  --repo-root '/Users/adnankhan/Documents/ContractorOS workspace' \
  --repository Zest-LeadGen/contractoros-california \
  --issue-number 47 \
  --pr-number 48 \
  --run-id 29176103821 \
  --canonical-ref 01b90ab8b12416101b4be067794bf543a3488779 \
  --observed-at 2026-07-12T02:55:00Z \
  --output-dir /tmp/contractoros-issue49-baseline
```

Observed exit: `2`.

Observed classification: `stale`.

Observed packet hash: `a0d86fd3e7ac279435fef3ac6c364cfd123a2b7c068ba38f62733389754978c1`.

Observed findings:

- canonical main `b99fc7d1fe0882380fc53041be42bb0aad35c02e` differs from verified live main `01b90ab8b12416101b4be067794bf543a3488779`;
- canonical Issue #47 active differs from live closed/completed;
- canonical PR #48 open differs from live merged;
- canonical lifecycle `red_team_changes_requested` differs from the closed gate.

Repository status before and after the collector run was unchanged. Output resolved to `/private/tmp/contractoros-issue49-baseline`, outside the repository. The stale baseline was not suppressed.

## Live Read-Only Evidence

PR #50 is open, non-draft, based on `main`, and uses branch `pre-4k-9-read-only-continuity-collector`. Bootstrap head `6aabfd9cd25889d4f0bbdf4dae11008291fce9f0` was verified live with auto-merge inactive and the external review marker absent.

Intermediate implementation head: `ee0ffc7c17072543cf818849252a8c07d2019538`.

Intermediate workflow run: `29177537570`.

The run completed with every pre-marker step passing, the mandatory exact-SHA marker step failing as expected because external review is pending, and later steps skipped.

Intermediate live collector command used Issue #49, PR #50, run `29177537570`, canonical ref `ee0ffc7c17072543cf818849252a8c07d2019538`, observation time `2026-07-12T03:00:00Z`, and `/tmp/contractoros-issue49-intermediate`.

Observed intermediate result:

- exit `0`;
- classification `requires_live_verification`;
- PR head `ee0ffc7c17072543cf818849252a8c07d2019538`;
- external review marker missing and pending;
- qualifying human approvals `0` and pending;
- auto-merge `false`;
- packet hash `4dcf61157d2ca1a6c2b4deb90666c67110aa1802f283ebeb93d6f7d7aca4f3f8`;
- output `/private/tmp/contractoros-issue49-intermediate`;
- repository status unchanged.

This intermediate run is bound only to the implementation head. The final evidence-reconciliation commit creates a new head and therefore requires a fresh external exact-SHA collector run, fresh external review, and a new SHA-bound marker only after external approval.

Governance-hardening head `9a684f427bc45e5cf8575e4bd105671a22baf1fd` was evaluated by ContractorOS Control Gates run `29203963944`. The run completed with overall conclusion `failure`. Checkout and all pre-marker controls passed, including changed-file, forbidden-scope, required-control update, PR contract, owner-trigger, and low-risk lane checks. The mandatory SHA-bound red-team marker step failed because no current-head marker existed, and the post-marker checks were skipped. This expected pre-review failure created no review, approval, merge, or release decision power.

The G1.1 correction commit creates a new head. Run `29203963944` remains historical evidence only for `9a684f427bc45e5cf8575e4bd105671a22baf1fd`; the new head requires a fresh Actions run and fresh external exact-SHA review.

G1.1 head `09e867ff984384676032e1aa0cf87f9cb990d55d` was evaluated by run `29205093385`. The run completed with overall conclusion `failure`; every pre-marker control passed, the mandatory current-head marker step failed because no marker existed, and post-marker checks skipped. The bounded governance subreview later passed, but PR #50 remained changes-requested for collector defects. C1A creates another head and requires a fresh run and external exact-SHA review.

C1A head `0801bd6497a3e16fa0565c7ac13a6a455da962f9` passed its bounded subreview. Run `29205653852` is `ContractorOS Control Gates` workflow ID `309083557`, event `pull_request`, exact branch `pre-4k-9-read-only-continuity-collector`, exact C1A head and expected `contractoros-control-gates` job. Its linked PR check points to that exact run. The C1B live collector observed all eight pre-marker steps successful, the marker step failed with marker evidence missing, both post-marker steps skipped, and run/job/check failure; consequential action remains blocked with auto-merge inactive and human approval pending. At `2026-07-12T19:30:00Z` it returned exit `0`, classification `requires_live_verification`, packet hash `49614f0f6afd703fd05efca4f45bcc056a6a5f407020e589c9e3c5330ea34af1`, and left repository status unchanged apart from authorized C1B edits.

## Canonical-State Reconciliation

The canonical snapshot now records:

- current main `01b90ab8b12416101b4be067794bf543a3488779`;
- active Issue #49 and actual PR #50;
- `observed_head_sha: null` with live GitHub required;
- developer implementation in review;
- Issue #47 / PR #48 / prior reviewed head / successful run / merge evidence;
- external exact-SHA review, human approval, merge/main/closeout and Phase 4K-9 blockers;
- `requires_live_verification`.

The snapshot does not embed a commit's own SHA as live authority and is not updated automatically.

## Documentation Impact

Authorized records now identify the source/specification/test artifacts, risks and controls, implementation decision, requirements mapping, validation tasks, future red-team invocation, collector statuses, Issue #47/PR #48 closeout, active Issue #49/PR #50, Phase 4K-9 not started, and Phase 4I paused.

The Issue #49 governance-hardening packet adds the ten-field prompt profile; red-team generated-prompt inheritance; honest hidden-metadata fallback; proportional Terra/Sol/Luna, effort, and speed routing; Standard/Medium/one-lead Plus defaults; Max/Ultra exceptions; atomic quota packets; context rotation; dated official-source reconciliation; compact structured progress tables; conditional interactive-chart capabilities; raw-chart-configuration prohibition; and phase/program capability separation without governance inflation.

C1A hardens collector marker semantics only. Missing red-team evidence on an otherwise valid active PR remains pending. Exact current-head approval may be represented as valid evidence but grants no merge power. Stale, malformed, adverse, duplicate, conflicting or ambiguous red-team evidence and invalid owner-trigger evidence are quarantined. Required-check evaluation, workflow identity, human approval qualification, repository identity, inaccessible-evidence handling, output-path changes, lifecycle reconciliation and schema expansion remain outside this packet.

C1B makes required-check and exact workflow/run/PR/event/job/step evidence classification inputs and performs the explicit `1.1.0` schema/fixture migration. Human/write-access approval qualification, collaborator permission reads, remote normalization, inaccessible-evidence exit changes, output-directory corrections, merge logic and closeout remain outside this packet.

No existing workflow or control script changed.

docs/project-control/DECISION_LOG.md: reviewed, no update required

docs/project-control/DEVELOPMENT_LEDGER.md: reviewed, no update required

docs/project-control/RISK_REGISTER.md: reviewed, no update required

## Validation Evidence

Fixture, schema, forbidden-scope, baseline and unit evidence is recorded above. C1A passed 32 focused marker tests, the complete 87-test suite and the required eleven-command local-control sequence. C1B passed 28 focused provenance tests, the complete 115-test suite, both schema parses, byte-identical deterministic JSON and Markdown comparisons, the required live starting-head verification and the required eleven-command local-control sequence. The consistent-fixture packet hash is `556ef5a137869e896ad25a4da3cf2e10065aa3f1674ea0da282efa7477ba55b9`. The cumulative branch changed-file set remains within the permitted 32-file set and C1B changes exactly sixteen existing files; no workflow, existing control script, manifest, lockfile, application/runtime, cache, repository temporary artifact, private path or credential was added.

## Risk Register Impact

The risk register records stale-state false negatives, command allowlist bypass, shell execution, output-path/symlink escape, private-evidence leakage, moved-head approval reuse, misleading derived packet authority, inaccessible GitHub evidence, deterministic drift, contradictory lifecycle, active auto-merge, hidden-metadata fabrication, quota/context loss, and governance-progress inflation, with controls and validation tasks.

## Decision Log Impact

The decision log records a standard-library-only CLI, positive command allowlist, external-only output, derived packet with no authority, fail-closed classification, no automatic canonical update, and no write decision power.

## Artifact Index Impact

The artifact index records source, specification, schemas, fixtures, and tests. A generated live packet or evidence manifest is explicitly excluded as a repository artifact.

## Red-Team Status

The C1A bounded subreview passed for `0801bd6497a3e16fa0565c7ac13a6a455da962f9`. PR #50 remains changes-requested. External exact-SHA review is pending for the later C1B head, and no C1B red-team marker exists.

## Human Approval Status

Human/write-access approval is pending.

## Auto-Merge Status

Auto-merge is inactive and prohibited.

## Forbidden Scope Confirmation

Confirmed:

- no write-capable collector or automatic Git/GitHub mutation;
- no workflow or existing control-script modification;
- no credential, secret, permission elevation, cloud resource, hosted service, paid resource, or private storage;
- no package, lockfile, dependency, application, mobile, web, backend, database, build, distribution, release, content, or production work;
- no self-review, red-team action, approval, merge, issue closeout, branch-protection bypass, administrator override, or auto-merge;
- no Issue #24 update or later phase issue;
- no Phase 4K-9 work;
- no Phase 4I resumption.

## Claim Level

Read-only local/CLI continuity evidence collection and deterministic derived startup-packet implementation in review only. Merged capability is not yet proven.

## Known Limitations

- A packet is point-in-time derived evidence and may become stale immediately.
- GitHub CLI availability and read access remain runtime prerequisites.
- Inaccessible evidence is blocked and cannot be inferred.
- Canonical state has no live decision power and is not updated automatically.
- Private evidence remains outside this public gate.
- Intermediate live evidence will be bound to the implementation commit; the later reconciliation commit makes that head stale and requires a fresh external run and review.
- Official model choices, Plus usage ranges, Fast support, and speed/consumption multipliers are dated 2026-07-12 and require revalidation before future recommendation.
- C2 still must address human/write-access approval qualification.
- C3 still must address remote normalization, inaccessible-evidence handling, output-path safety and lifecycle reconciliation.

## Next Phase Status

- Phase 4K-9 not started.
- Phase 4I paused.
- Phase 4K-9 may only be evaluated after Issue #49 review, merge, main verification and closeout.

## OWNER_TRIGGER_REVIEW marker

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: This gate implements the first read-only continuity evidence collector and deterministic derived startup-packet generator. It defines security boundaries, stale-state behavior, quarantine behavior, command allowlists and future red-team handoff foundations. It must not receive write, approval, merge, release, budget, credential-management, policy-amendment, Phase 4K-9 or Phase 4I authority.
