# H5-A — Governance Document Inventory & Classification Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parents #63, #64)

## Phase

H5-A — governance document inventory & classification (read-only; no file moves).

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

H5+H6 batched phase authorized by owner "go" (2026-08-09), recorded on-platform via the owner authorization comment on issue #118 (PA-0003 evidence_id). No new gate, product, or authority is created by this deliverable; it is a read-only inventory.

## Scope

Inventory every artifact under `docs/project-control/` and classify each into its target boundary (policy / current-source-of-truth / generated / operational / security / historical evidence). Introduce PA-0003 (default-deny) for the batch. **No file is moved** in H5-A — this is the contract H5-B/H5-C execute against.

## Starting Main SHA

cd6af16 (post-stress reconciliation).

## Finding: topology is overgrown (confirms #63 premise)

`docs/project-control/` holds **134 files**:

- **51 `phase_*` reports** — historical evidence → `docs/archive/` (H5-B), no history rewrite.
- **~40 files** assert some "current status / roadmap / source of truth" — competing CURRENT records that must each collapse to ONE.
- **9 ADRs** (decision system), **9 `red-team/` runbooks**, **6 registers**, **6 state/schema files**, plus policy/constitution docs.

## Classification (target class per artifact group)

| Class (target boundary) | Representative artifacts | H5 disposition |
|---|---|---|
| Constitution / single policy authority (`policy/`) | PROGRAM_CONSTITUTION, PROJECT_FOUNDATION, AUTHORITY_AND_SUPERSESSION_INDEX, AI_AUTHORITY_MODEL_AND_TOOL_SECURITY, ROLE_BOUNDARIES, PROJECT_SCOPE_BOUNDARIES | Collapse overlaps into ONE constitution + explicit supersession. |
| ONE current roadmap (`docs/product/`) | PROJECT_IMPLEMENTATION_ROADMAP, AUTOMATION_PHASE_ROADMAP, PROJECT_VISION_AND_PHASE_TRACKER, PHASE_ONE_* | Single current roadmap; rest archived. |
| ONE current source-of-truth (policy vs generated) | PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH, ARTIFACT_INDEX | De-duplicate; volatile parts become generated. |
| Generated current status (`generated/`) | state/contractoros-state.yaml, ARTIFACT_INDEX (live parts) | Move to `generated/` with generated_at/expires_at/source-queries/staleness (H5-C). |
| ADR / decision system | adr/ADR-001..009, DECISION_LOG, OWNER_DECISION_REGISTER, CONTRACTOROS_DESIGN_DECISIONS | Keep ADRs as authority; DECISION_LOG↔register cross-reference already added. |
| Registers (keep, one each) | RISK_REGISTER (1050 lines), RED_TEAM_FINDINGS_REGISTER, SOURCE_REGISTER, ASSUMPTION_REGISTER, ORIGINALITY_REGISTER, REQUIREMENTS_TRACEABILITY_MATRIX | Keep distinct; RISK_REGISTER oversized — split active vs resolved. |
| Operational runbooks (`docs/operations/`) | red-team/*, HANDOFF_PLAYBOOK, WORKFLOW_OPERATOR_RUNBOOK, WORKFLOW_AUTOMATION_COMMAND_PACK | Move under `docs/operations/`. |
| Security / controls (`docs/security/`) | EPISTEMIC_INTEGRITY_AND_NON_FABRICATION_STANDARD, CLAIM_LEVELS_AND_RELEASE_GATES, LOW_RISK_LANE_POLICY, CONTROL_FILE_UPDATE_MATRIX | Move under `docs/security/`. |
| Historical evidence (`docs/archive/`, immutable) | all 51 phase_* reports, H0_FINAL_DISPOSITION_REPORT, incidents/*, sanitation/*, H1_CLOSEOUT_LINEAGE | Archive; never rewrite. |
| Schemas (`schemas/` or `generated/`) | state/*.schema.*, governance-contract-pin.json | Co-locate with generated boundary. |
| Control code (unchanged) | scripts/control/*.py (10), scripts/continuity/*.py | Not docs; governed by CODEOWNERS. |

## Changed Files

- `docs/project-control/authorizations/PA-0003.json` (new)
- `docs/project-control/phase_h5a_inventory_classification_report.md` (new)
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`

No other path is changed. No file is moved.

## Commands Run

- `find docs/project-control -type f` inventory; class counts by group; `grep` for competing "current/roadmap/source-of-truth" records.
- PA-0003 JSON-schema validated against the governance authorization contract (PASS).
- Six PR-context control validators run against the real PR body pre-push.

## Dependency / Lockfile Handling

None. No dependency or lockfile change.

## Documentation Impact

Adds the H5-A inventory/classification report; updates DECISION_LOG and DEVELOPMENT_LEDGER. No existing document is moved or superseded in H5-A.

## Validation Evidence

PA-0003 SCHEMA=PASS; six control validators green vs the real PR body; inventory counts reproducible via the find/grep commands above.

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required

## Decision Log Impact

Adds the H5-A Intake + PA-0003 section (intake, arming-sequencing note, batch-operating-mode change).

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required (H5-A adds a phase report; index consolidation is an H5-B target).

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Required: YES (owner-only merge; part of the batched H5 owner key-turn).

## Auto-Merge Status

Auto-merge eligible: NO.

## Forbidden Scope Confirmation

Confirmed — read-only inventory + PA record + control-file updates only. No product, dependency, workflow-logic, or governance-repository mutation.

## Claim Level

Inventory/classification only. No consolidation or file move is performed or claimed complete.

## Known Limitations

Classification is by artifact group; per-file supersession decisions are made in H5-B. Arming the path wall is a separate follow-up PR (an armed checker self-denies the PR that introduces its own PA — the PA-0001/PA-0002 bootstrap).

## Next Phase Status

H5-B (consolidation / archive moves) follows on the same batched authorization; arming the path wall is its first act once PA-0003 is on base. AUTOMATIC_CONTINUATION=NO.
