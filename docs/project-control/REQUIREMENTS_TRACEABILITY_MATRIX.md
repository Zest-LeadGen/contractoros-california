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
