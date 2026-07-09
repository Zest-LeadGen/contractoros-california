# Requirements Traceability Matrix

Purpose: map Phase 4J-0 governance requirements to versioned ContractorOS California evidence.

## Phase 4J-0 Traceability

| Requirement ID | Requirement | Evidence files | Validation |
|---|---|---|---|
| RTM-4J0-001 | GitHub is source of truth. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md` | Red-team verifies PR evidence against GitHub. |
| RTM-4J0-002 | Chat memory is not source of truth. | `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `SOURCE_REGISTER.md` | Review confirms no unversioned chat-only requirement is needed for merge. |
| RTM-4J0-003 | Codex is developer executor only. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md` | PR remains unmerged until external red-team and human/write-access approval. |
| RTM-4J0-004 | Red-team remains separate. | `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `DECISION_LOG.md` | Red-team decision is separate from developer evidence. |
| RTM-4J0-005 | Human/write-access approval remains required before merge. | `AGENTS.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `DECISION_LOG.md` | Branch is not merged by Codex. |
| RTM-4J0-006 | No auto-merge. | `AGENTS.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `DECISION_LOG.md` | PR is opened without merge. |
| RTM-4J0-007 | No branch-protection bypass. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md` | Protected PR route remains required. |
| RTM-4J0-008 | No paid API, services, hosted bots, CI, or tools. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `ORIGINALITY_REGISTER.md` | Dependency/build/service scope remains absent. |
| RTM-4J0-009 | No unrelated Claude-imported Codex project context. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `MODEL_RUN_LOG.md` | Model run log records no unrelated imported project context used. |
| RTM-4J0-010 | No trusting unrelated hooks such as cockroachdb. | `AGENTS.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `MODEL_RUN_LOG.md` | Commit and push use hook-bypass flags; no hook evidence is trusted. |
| RTM-4J0-011 | No broad connector discovery, list-resource, or tool-schema calls. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `MODEL_RUN_LOG.md` | Model run log records prohibited calls not used. |
| RTM-4J0-012 | If direct tools are unavailable, stop instead of discovering tools. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md` | Stop condition is versioned. |
| RTM-4J0-013 | Future red-team decisions must become GitHub artifacts tied to exact PR head SHA in Phase 4J-2. | `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `VALIDATION_TASKS.md` | Phase 4J-2 must define artifact path and SHA binding. |
| RTM-4J0-014 | 95% automation reduces relay, paperwork, repetitive checks, and handoff; it does not remove owner judgment. | `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `DECISION_LOG.md` | PR route still requires red-team and human/write-access approval. |
| RTM-4J0-015 | Every assumption, decision, source, model run, validation task, and originality requirement is versioned in repo files. | `ASSUMPTION_REGISTER.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `SOURCE_REGISTER.md`, `MODEL_RUN_LOG.md`, `VALIDATION_TASKS.md`, `ORIGINALITY_REGISTER.md` | Registers are changed in the Phase 4J-0 PR. |
| RTM-4J0-016 | Developer connector implementation path is blocked after repeated `api_tool.list_resources` violations. | `ASSUMPTION_REGISTER.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `RISK_REGISTER.md`, `MODEL_RUN_LOG.md` | Retry of the same connector path is rejected. |
| RTM-4J0-017 | Bootstrap Codex use is allowed only because Phase 4J-0 creates the Codex governance files. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `phase_4j_0_codex_operating_model_report.md` | Bootstrap scope is limited to the allowed files. |
| RTM-4J0-018 | No app, product, dependency, build, backend, or database scope is touched. | `phase_4j_0_codex_operating_model_report.md`, `VALIDATION_TASKS.md` | Changed-file list and forbidden-scope scan verify only governance docs changed. |
| RTM-4J0-019 | Command evidence must distinguish successful commands from failed attempts, unavailable initial commands, and owner-completed commands. | `phase_4j_0_codex_operating_model_report.md`, `MODEL_RUN_LOG.md` | Report includes `## Commands Run` with subheadings for successful, failed, unavailable-at-initial-attempt, and owner-completed commands. |
| RTM-4J0-020 | GitHub PR review requires the branch and PR to exist in GitHub source of truth. | `RISK_REGISTER.md`, `VALIDATION_TASKS.md`, `MODEL_RUN_LOG.md` | PR #15 exists; final correction still requires corrected push, PR body update, workflow run, review, approval, merge, and post-merge verification. |
| RTM-4J0-021 | Lane-based auto-merge eligibility is a future policy target, not current authorization. | `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `AGENTS.md` | Future phase approval is required before auto-merge or owner-approval reduction. |
| RTM-4J0-022 | Owner-interruption triggers must be versioned before future automation changes. | `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md`, `AGENTS.md` | Trigger list includes legal, financial, paid service, public release, production/readiness, app-store/build/distribution, scope expansion, unresolved red-team BLOCKED decisions, dependency/security risk acceptance, and architecture-threshold decisions. |
| RTM-4J0-023 | Phase 4J-0 does not activate auto-merge. | `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `CONTRACTOROS_DESIGN_DECISIONS.md` | Current owner approval remains required and auto-merge is not active. |
| RTM-4J0-024 | Every future prompt must include model/effort recommendation. | `PROMPT_CONVENTION.md`, `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md` | Future prompts are blocked when the required header is missing. |
| RTM-4J0-025 | Model/effort policy must be based on official OpenAI sources or repo-versioned policy. | `PROMPT_CONVENTION.md`, `SOURCE_REGISTER.md` | Source register records OpenAI Codex Models docs, Codex Config Reference, and GPT-5.5 guidance as policy basis. |
| RTM-4J0-026 | Extra High/xhigh mapping must be treated as UI-observed unless official UI source is added. | `PROMPT_CONVENTION.md`, `ASSUMPTION_REGISTER.md`, `SOURCE_REGISTER.md` | Repo policy documents `xhigh` as the official config value and treats "Extra High" as UI-observed terminology only. |
| RTM-4J0-027 | Missing model/effort header creates a stop condition. | `PROMPT_CONVENTION.md`, `AGENTS.md`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `VALIDATION_TASKS.md` | Agent must stop and ask for the header before implementation. |

## Phase 4J-1 Traceability

| Requirement ID | Requirement | Evidence files | Validation |
|---|---|---|---|
| RTM-4J1-001 | Future phase PRs must link a GitHub phase issue. | `.github/pull_request_template.md`, `scripts/control/check_pr_contract.py`, `AI_DEVELOPMENT_OPERATING_MODEL.md`, `AGENTS.md` | PR contract check fails in PR context when the PR body lacks an accepted issue reference. |
| RTM-4J1-002 | GitHub phase issue template must capture owner-approved scope and review requirements. | `.github/ISSUE_TEMPLATE/phase_issue.yml` | Template includes phase name, lane, objective, allowlist, forbidden scope, evidence, assumptions, risks, validation tasks, red-team requirement, approval requirement, auto-merge status, and trigger checkboxes. |
| RTM-4J1-003 | PR template must require linked phase issue and phase evidence. | `.github/pull_request_template.md` | Template includes linked phase issue, phase, lane, scope summary, changed files, commands, validation evidence, forbidden scope, red-team status, human approval status, auto-merge status, and next phase status. |
| RTM-4J1-004 | Linked issue formats must include closing keywords and explicit issue labels. | `scripts/control/check_pr_contract.py`, `.github/pull_request_template.md` | Accepted formats include `Closes #123`, `Fixes #123`, `Resolves #123`, `Linked issue: #123`, and `Phase issue: #123`. |
| RTM-4J1-005 | Phase 4J-1 does not activate auto-merge. | `phase_4j_1_github_issue_intake_report.md`, `RISK_REGISTER.md`, `CONTRACTOROS_DESIGN_DECISIONS.md` | Auto-merge remains prohibited/currently inactive unless a future approved phase changes policy. |
