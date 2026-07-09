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
- Google Drive is for archive artifacts.
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

## Review Condition

Update decisions through project-control PRs or explicitly approved control milestones.
