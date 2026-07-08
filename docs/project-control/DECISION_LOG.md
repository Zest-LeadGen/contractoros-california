# ContractorOS Decision Log

Purpose: record durable architectural and process decisions.

## Active Decisions

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
