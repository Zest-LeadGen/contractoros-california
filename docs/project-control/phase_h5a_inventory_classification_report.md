# H5-A — Governance Document Inventory & Classification

Phase issue: #118 (H5+H6 batched; parent #63)
Lane: Control / Infrastructure — read-only inventory, no file moves in this deliverable.
Date: 2026-08-09

## Finding: topology is overgrown (confirms #63 premise)

`docs/project-control/` holds **134 files**. Breakdown:

- **51 `phase_*` reports** — historical evidence. Target: move to `docs/archive/` immutably (H5-B), no history rewrite.
- **~40 files** assert some form of "current status / roadmap / source of truth" — multiple competing CURRENT records that must each collapse to ONE.
- **9 ADRs** — the decision system; keep, formalize as the single ADR authority.
- **9 `red-team/` docs** — operational runbooks; target `docs/operations/` or `docs/security/`.
- **6 registers**, **6 state/schema files**, plus policy/constitution docs.

## Classification (target class per artifact group)

| Class (target boundary) | Artifacts | H5 disposition |
|---|---|---|
| **Constitution / single policy authority** (`policy/`) | PROGRAM_CONSTITUTION, PROJECT_FOUNDATION, PROGRAM_ARCHITECTURE_DECISION_INDEX, AUTHORITY_AND_SUPERSESSION_INDEX, AI_AUTHORITY_MODEL_AND_TOOL_SECURITY, ROLE_BOUNDARIES, PROJECT_SCOPE_BOUNDARIES | Collapse overlaps into ONE constitution + explicit supersession; move under `policy/`. |
| **ONE current roadmap** (`docs/product/`) | PROJECT_IMPLEMENTATION_ROADMAP, AUTOMATION_PHASE_ROADMAP, PROJECT_VISION_AND_PHASE_TRACKER, PHASE_ONE_* | Competing roadmaps → single current roadmap; the rest archived. |
| **ONE current source-of-truth** (policy vs generated split) | PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH, ARTIFACT_INDEX, PROJECT_VISION_AND_PHASE_TRACKER | De-duplicate; the volatile parts become generated (below). |
| **Generated current status** (`generated/`) | state/contractoros-state.yaml, ARTIFACT_INDEX (live parts) | Move to `generated/` with `generated_at`/`expires_at`/source-queries/staleness (H5-C). |
| **ADR / decision system** | adr/ADR-001..009, DECISION_LOG, OWNER_DECISION_REGISTER, CONTRACTOROS_DESIGN_DECISIONS, DEVELOPMENT_CONTROL_MODEL_V3 | Keep ADRs as the authority; reconcile DECISION_LOG↔register divergence (already cross-referenced this session). |
| **Registers (keep, one each)** | RISK_REGISTER (1050 lines), RED_TEAM_FINDINGS_REGISTER, SOURCE_REGISTER, ASSUMPTION_REGISTER, ORIGINALITY_REGISTER, REQUIREMENTS_TRACEABILITY_MATRIX | Keep distinct; RISK_REGISTER is oversized — candidate to split active vs resolved. |
| **Operational runbooks** (`docs/operations/`) | red-team/*, HANDOFF_PLAYBOOK, WORKFLOW_OPERATOR_RUNBOOK, WORKFLOW_AUTOMATION_COMMAND_PACK, RED_TEAM_OPERATING_PROTOCOL/STATE_MACHINE/STARTUP_PACKET_SPEC | Move under `docs/operations/`. |
| **Security / controls** (`docs/security/`) | EPISTEMIC_INTEGRITY_AND_NON_FABRICATION_STANDARD, CLAIM_LEVELS_AND_RELEASE_GATES, LOW_RISK_LANE_POLICY, CONTROL_FILE_UPDATE_MATRIX, PRIVATE_CONTROL_PLANE_POLICY | Move under `docs/security/`. |
| **Historical evidence** (`docs/archive/`, immutable) | all 51 phase_* reports, H0_FINAL_DISPOSITION_REPORT, incidents/*, sanitation/*, H1_CLOSEOUT_LINEAGE | Archive; never rewrite. |
| **Schemas** (`generated/` or `schemas/`) | state/*.schema.*, governance-contract-pin.json | Co-locate with generated boundary. |
| **Control code** (unchanged) | scripts/control/*.py (10), scripts/continuity/*.py | Not docs; governed by CODEOWNERS. |

## Recommended H5-B move-order (next deliverable, after this lands)

1. Create `docs/archive/` and move the 51 phase reports (git mv, history preserved).
2. Pick the single roadmap and single constitution; mark the losers `SUPERSEDED_BY:` and archive.
3. Establish `policy/ docs/{architecture,security,product,operations} generated/` boundaries.
4. Update every consumer reference (control scripts' matrix, README) — with the H5-C stale-reference check to catch breakage.

## Notes
- No file is moved in this deliverable — this is the inventory contract H5-B/C execute against.
- The 10-field prompt ceremony → smaller execution contract (H5-C) will also shrink this surface.
