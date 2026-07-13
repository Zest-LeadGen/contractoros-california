# AI Development Operating Model

## Purpose

Define how AI assistance may be used for ContractorOS California without weakening GitHub evidence, red-team separation, owner judgment, or protected PR governance.

## Source Of Truth

GitHub is source of truth for code, PRs, review evidence, and text project-control records.

Chat memory is not source of truth. Unversioned local notes, transient tool state, and connector memory are not source of truth.

Every assumption, design decision, source, model run, validation task, and originality requirement must be captured in versioned repo files.

## Prompt Convention

Every future implementation, review, or correction prompt must include model and effort recommendation.

Model/effort selection must follow `docs/project-control/PROMPT_CONVENTION.md`.

Missing model/effort header is a stop condition.

Phase 4J-0 documents this convention only.

## GitHub Phase Issue Intake

After Phase 4J-1, every future phase PR must link a GitHub phase issue.

The phase issue is the durable intake record for owner-approved objective, lane, file allowlist, forbidden scope, assumptions, risks, validation tasks, red-team requirements, human approval requirements, and auto-merge status.

Chat prompts may initiate discussion, but chat memory is not sufficient phase intake once the linked-issue requirement is active.

Missing linked phase issue reference is a PR control-gate failure.

## AI Role

Codex is developer executor only. Codex may prepare scoped file changes, run permitted local checks, and open PRs. Codex must not self-review, act as red-team, merge, approve its own PR, bypass branch protection, or continue into the next phase.

Red-team remains separate. Red-team decisions must become GitHub PR evidence tied to the exact PR head SHA reviewed.

The required plain-text marker begins with `RED_TEAM_DECISION` and includes PR number, PR head SHA, decision, reviewer role, review date, scope reviewed, conditions, forbidden-scope confirmation, and the statement `This decision applies only to the listed PR head SHA.`

`scripts/control/check_red_team_marker.py` validates the marker text against the current PR head SHA and fails when the marker is missing, stale, malformed, or records `CHANGES_REQUESTED` or `BLOCKED`.

Phase 4J-3 wires the marker validator into the required ContractorOS control-gates workflow for pull requests. The workflow reruns on PR body edits so red-team can add the marker after review, and any later commit changes the PR head SHA and requires a fresh marker.

Current state:

Human/write-access approval remains required before merge. No auto-merge is currently authorized.

## Red-Team Operating Protocol

Future red-team windows must inherit operating behavior from committed GitHub files, not chat memory.

Primary protocol files:

- `docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md`
- `docs/project-control/RED_TEAM_STATE_MACHINE.md`
- `docs/project-control/HANDOFF_PLAYBOOK.md`

GitHub is source of truth. Chat memory, sandbox state, local scratch files, connector memory, connector state, and unversioned notes are not source of truth.

Every material decision, approval, rejection, condition, assumption, scope boundary, and handoff state must be reflected in GitHub issue evidence, PR evidence, committed project-control docs, GitHub PR comments/reviews, or terminal output explicitly pasted by the owner.

If evidence is missing, status is `not proven`. If evidence is insufficient for the next action, status is `blocked`.

Red-team must classify lifecycle state before giving next steps and must not present next-phase options while review, marker, checks, approval, merge, main verification, or issue closeout is unresolved.

Whenever red-team provides GitHub CLI or terminal commands, it must include expected success output, failure indicators, stop conditions, and the next allowed action after confirmation.

Red-team must include the project progress snapshot unless the response is only a brief acknowledgment or the owner explicitly asks for no progress section.

Do not approve if the exact current pull request head SHA is not known.

Do not start the next phase until prior phase post-merge verification and issue closeout are recorded.

Do not resume paused phases unless explicitly authorized.

## Automation Meaning

Current state:

95% automation means reducing relay work, paperwork, repetitive checks, and handoff friction. It does not remove owner judgment, red-team accountability, protected PR governance, or human/write-access approval for merge.

Future target:

95% automation should reduce owner monitoring and manual merge work for low-risk, mechanically verifiable lanes after required safeguards are implemented.

Future lane-based automation must be separately approved in a later phase. Phase 4J-0 does not authorize auto-merge.

Owner interruption triggers:

Owner interruption remains required for legal, financial, paid-service, public-release, production/readiness, app-store/build/distribution, scope expansion, unresolved red-team BLOCKED decisions, dependency/security risk acceptance, and architecture-threshold decisions.

## Owner-Trigger And Lane Eligibility Evidence

After Phase 4J-4, every future PR must include a machine-checkable `OWNER_TRIGGER_REVIEW` marker before the pull request control gate can pass.

The marker records owner interruption status, trigger categories, lane eligibility, human approval requirement, auto-merge eligibility, and rationale. `scripts/control/check_owner_trigger_review.py` ignores HTML comments and fenced code examples, then fails missing, malformed, or internally inconsistent evidence.

Allowed trigger categories are `NONE`, `LEGAL`, `FINANCIAL`, `PAID_SERVICE`, `PUBLIC_RELEASE`, `PRODUCTION_READINESS`, `APP_STORE_BUILD_DISTRIBUTION`, `SCOPE_EXPANSION`, `UNRESOLVED_RED_TEAM_BLOCKED`, `DEPENDENCY_SECURITY_RISK_ACCEPTANCE`, and `ARCHITECTURE_THRESHOLD`.

Any trigger category other than `NONE` makes the PR `NOT_AUTOMATION_ELIGIBLE`. A `FUTURE_LOW_RISK_CANDIDATE` marker is only internally consistent when `Owner interruption required: NO` and `Trigger categories: NONE`.

Current required values remain `Human approval required: YES` and `Auto-merge eligible: NO`.

Phase 4J-4 does not activate auto-merge, reduce owner judgment, remove red-team review, or reduce human/write-access approval requirements.

## Tool Governance

The following controls apply to Codex and other AI developer executors:

- Do not run `/init`.
- Do not call `api_tool.list_resources`.
- Do not call broad connector discovery, broad list-resource calls, or tool-schema dump calls.
- If direct tools are unavailable, stop and report the limitation instead of discovering tools broadly.
- Do not trust unrelated hooks.
- Do not use cockroachdb hooks.
- Do not use unrelated Claude-imported Codex project context.
- Do not add paid API, paid services, hosted bots, hosted CI, or hosted tools in this phase.

## Bootstrap Exception

Phase 4J-0 is allowed to create `AGENTS.md` and the AI governance files before those files exist. This bootstrap exception exists because the prior developer connector implementation path failed twice before implementation by calling `api_tool.list_resources`.

The exception is active only for Phase 4J-0. It does not permit product work, dependency work, native build work, backend work, merge, auto-merge, self-review, branch-protection bypass, or future bypass.

## Stop Conditions

Stop instead of proceeding when:

- A required direct tool is unavailable.
- The requested work would touch files outside the approved allowlist.
- A hook or connector context appears unrelated to ContractorOS California.
- A command would add dependency, build, backend, database, native, release, or product scope.
- Red-team review or human/write-access approval is missing for merge.

## Program Constitution Alignment

The Program Constitution and Owner Decision Register govern public-safe program direction. The four-level AI decision-power model, least-privilege tools, separate read/write identities, and read-only-first continuity collector are architecture direction only. This documentation does not grant credentials, approval, merge, release, budget, policy-amendment, or production decision power.

## Capability, Effort, Speed, And Agent Routing

`PROMPT_CONVENTION.md` is the canonical execution profile. Capability discovery must use visible selectors when available and must never fabricate hidden metadata. Hidden model, effort, or speed metadata alone does not stop authorized work; the exact fallback attestations are used instead.

Terra is the routine bounded-work route, Sol is reserved for complex security, architecture, integration, or final high-stakes review, and Luna is the low-risk mechanical or lightweight-volume route when those selectors are visible. Medium is the normal effort default. Higher effort is not automatically better: Low, High, Extra High, Max, and Ultra are proportional routes with bounded justifications and the owner-authorization rules in the prompt convention.

Standard speed is the Plus default and Fast is off by default. Fast requires material latency need, narrow scope, quota disclosure, authorization, model support, and a durable checkpoint. Speed is not a proxy for intelligence or reasoning quality.

One lead agent is the default. Ultra and parallel fan-out are never defaults, and Ultra subagents are not independent red-team review.

## Plus Atomic Packets And Context Rotation

Substantial work is split into quota-aware atomic packets declaring objective, permitted files/functions, model, effort, speed, agent count, focused validation, checkpoint, stop conditions, and next packet. Recovery, architecture review, correction clusters, adversarial testing, documentation reconciliation, CI investigation, and final exact-SHA handoff should not be collapsed into one Plus packet.

Context behavior is fail-closed by band: normal bounded work at 0-59%; no scope expansion and checkpoint preparation at 60-74%; smallest-safe-unit completion plus new-window handoff at 75-84%; and handoff-only with no implementation at 85-100%. A visible 79% requires a new window before broad implementation. An unavailable percentage must not be invented.

## Evidence-Based Progress Presentation

Substantive responses must provide a concise product-development-stage statement, current lifecycle state, a compact current-phase table, and a compact program-capability table. Current-phase rows cover durable intake/scope, implementation, tests/validation, documentation reconciliation, external exact-SHA review, human approval, merge/main verification, issue closeout, and overall. Program rows cover governance/control, workflow automation, product implementation, content governance/production, dependency/runtime, backend/data platform, build/distribution, business/market validation, and overall program.

Percentages are estimates, not completion evidence. Unsupported values are `NOT_PROVEN`; material changes require evidence; gated work cannot reach 100% before applicable review, approval, merge, main verification, and closeout. Governance documentation cannot increase actual product or operational capability.

Where supported, exactly one detailed interactive chart is rendered at the absolute bottom with nothing after it. Raw chart configuration is never presented to the owner. Where unsupported, compact tables remain structured rather than becoming compressed paragraph strings, and the response records `INTERACTIVE_CHART=UNSUPPORTED_IN_CURRENT_SURFACE`.
