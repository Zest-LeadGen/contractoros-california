# P0-RECON-2 Stale-Authority Classification Table — 2026-08-10 <!-- documentation scope -->

Phase issue: #144. Owner authorization: issue-144-comment-5245410500. Sweep basis: repository-wide semantic scan of all 118 maintained non-archive tracked files against twelve stale-authority classes (listed in #144), executed from branch p0-recon-2-sweep at main 3fb3d4d. Classification contract: CURRENT_AND_CORRECT / CURRENT_BUT_STALE_CORRECT_NOW (CN) / HISTORICAL_MARK_EXPLICITLY (HM) / ARCHIVED_HISTORY_LEAVE_UNTOUCHED (AH). "Disposition" records what this PR did. Live facts verified before correction: PR #75 merged 2026-07-15T09:52:55Z; PR #77 merged 2026-07-15T21:11:13Z; PR #81 merged 2026-07-19T03:58:55Z; issues #67/#76/#80/#82 closed.

| File | Finding (class) | Classification | Disposition in this PR |
|---|---|---|---|
| PROJECT_VISION_AND_PHASE_TRACKER.md | "Current H1 Recovery Gate" section asserting #58/current activity (1,12) | CN | Section retitled Historical with supersession pointer |
| HANDOFF_PLAYBOOK.md | "Current H1 Recovery Handoff" + "PR #77 remains open" (1,12) | CN | Retitled Historical; era-facts reframed; PR #77 merge date recorded |
| HANDOFF_PLAYBOOK.md | #58 "active" authority ref; Codex phrasing; packet/Codex-window rules (1,2,3) | CN/HM | Line fixes + file banner covering packet rules |
| RED_TEAM_STATE_MACHINE.md | "PR #75 is the current open reconciliation PR"; #58 controls "current" reconciliation (1,12) | CN | Line fix with merge date; file banner covers R4-R7 table and WAITING_FOR_CODEX state names |
| RED_TEAM_OPERATING_PROTOCOL.md | "current Issue #58 recovery amendment"; "Codex is developer executor only"; fresh-context final review; ten-field profile + ACTUAL_CODEX_MODEL (1,2,3,6) | CN/HM | Line fixes (Decision 3/4 wording) + file banner |
| AI_DEVELOPMENT_OPERATING_MODEL.md | #58 "current H1 recovery lane"; stop-condition header rule; Codex executor; fresh-context review; "current recovery lifecycle"; PROMPT_CONVENTION "canonical" claim (1,2,3,6,8) | CN | Five line fixes + file banner |
| PROMPT_CONVENTION.md | Whole file presenting mandatory ten-field profile (3,2,8) | HM | Top-of-file SUPERSEDED banner (H5-C contract) |
| AUTHORITY_AND_SUPERSESSION_INDEX.md | "current Issue #80 / PR #81 activity" (L36) and "only current bounded documentation activity" (L76) (12) | CN | Both corrected with closure/merge facts (L76 found during implementation, beyond sweep table — disclosed) |
| LOW_RISK_LANE_POLICY.md | "current H1 reconciliation"; "Issue #58 is active"; toolchain deferred; Codex reviewer line (1,4,5,2) | CN | File banner naming those statements historical |
| WORKFLOW_AUTOMATION_TARGET_STATE.md | Codex handoff/executor; 4K pauses + toolchain deferred; #58 authorization (2,4,5,1) | CN | File banner |
| WORKFLOW_OPERATOR_RUNBOOK.md | Codex role table/state rows; "Current Deferred Status" toolchain section (2,4,5) | CN | File banner naming the deferred-status section historical |
| WORKFLOW_AUTOMATION_COMMAND_PACK.md | 4K-8-era Codex operator reference (2) | HM | File banner |
| AUTOMATION_PHASE_ROADMAP.md | #58 "only current activity"; 4K-9 Codex intake gate; toolchain deferred (1,2,4,5) | CN/HM | File banner |
| PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md | npm-bootstrap "deferred" (L67); "Codex is developer executor only" (L124); "current Issue #58 recovery boundary" (L178); runtime-QA blocked premise (L182); 4K-9 Codex deferred item (L193) (5,2,1,4,9) | CN/HM | Five line fixes (Decision 3 wording; H6-delivered facts; pauses re-grounded in current authority) |
| SOURCE_REGISTER.md | SRC-H1-002 "Active recovery authority"; SRC-H1-004 "Current reconciliation base"; SRC-H1-006 governance repo "empty" (1,12,10) | HM | Notes columns annotated historical/pre-bootstrap with dates |
| RISK_REGISTER.md | R-H1-02/-03 stale controls; four "Active" rows overtaken by H6/H1 deliveries; prompt-header row; R-H0-TD-R1-001 H0-blocking row (1,2,5,3,9,12) | CN | Append-only resolution appendix (register style honored; rows preserved) |
| REQUIREMENTS_TRACEABILITY_MATRIX.md | RTM-H1 "in progress/pending" rows; Codex/ten-field requirement rows (12,9,2,3) | HM | Append-only currency note |
| ASSUMPTION_REGISTER.md | "Current H1 Recovery Assumptions" heading (1) | HM | Heading retitled Historical |
| CONTRACTOROS_DESIGN_DECISIONS.md | CDR-H1-001 (#58/Codex); CDR-4J-003 (Codex executor); CDR-4J-019 (header stop condition) (1,2,3) | HM | Superseded-by pointers added to Status lines; decisions preserved |
| MODEL_PROVIDER_COST_GOVERNANCE.md | "Current Model Policy Result" holding PROMPT_CONVENTION controlling (3,8) | CN | Section split historical/current (H5-C + OD-017 + Decisions 3-4) |
| OWNER_DECISION_REGISTER.yaml | D27/D28 empty superseded_by despite later supersessions (1,2,6) | CN | superseded_by populated (D27 -> P0-RECON #141 + Decision 1; D28 -> Decisions 3-4); last_reviewed updated; records otherwise preserved |
| RED_TEAM_FINDINGS_REGISTER.md | RT-H0 2.1.0 versions still H0-blocking (9) | CN | Append-only currency note; NO finding inferred resolved — formal version updates routed to H7A-5/H9 per the register's own contract |
| RED_TEAM_CONTINUITY_ARCHITECTURE.md | "future private governance repository" ambiguity vs populated public governance repo (10) | HM | Clarifying note distinguishing the populated PUBLIC governance repo from the still-future PRIVATE confidential-material repository (an initial conflating edit was self-caught and corrected in-branch) |
| THREAT_MODEL_H7A.md | Baseline NOT_PROVEN/discipline-only statements overtaken by H7A-3 deliveries (11) | HM | Dated Delivery Addendum; baseline preserved |
| state/contractoros-state.yaml | Lagging observation (h7a_3_in_review; L-1 blocker open) (12,11) | CN | Refreshed from fresh live reads in this PR (see state file source_queries) |
| PROJECT_FOUNDATION.md | "Current primary phase: Phase One" (4,12) | CN | Reworded to product-vision anchor under Decision 2 role |
| contractoros_project_control_recovery.md | Phase 3A-era "current scope" (4) | HM | File banner |
| KNOWN_GAPS_AND_NON_GOALS.md | "Non-Goals For Current Phase" anchored to 4K-0 (4) | HM | File banner |
| phase_post_h5_reconciliation_report.md | "tell one story" overclaim | CN | Corrected via dedicated evidence/P0_RECON_CLOSEOUT_ACCURACY_CORRECTION.md + DECISION_LOG + index row; the report file stays byte-unmodified (one-changed-phase-report-per-PR gate — disclosed) |
| evidence/H7A3_SCANNING_EVIDENCE.md | §3 PENDING marker overtaken by executed key-turn (11) | CN | Truth-up citing issue-137 comments 5245204102/5245222558 (per the head-preservation record) |
| apps/web/README.md | "npm install" instruction vs npm ci baseline (5) | CN — OUT OF LANE | NOT corrected here: apps/** is #144-forbidden. Routed to the next authorized phase touching apps docs (H7A-5 closeout candidate). Disclosed, not absorbed. |
| Issue #70 body | Stale "current summary" self-description | CN (owner surface) | Owner refresh comment posted: issue-70-comment-5245520671 (executor drafted; owner posted) |
| RED_TEAM_OPERATING_PROTOCOL.md | "Current recovery sequencing is R4..." (L165) — MISSED by the sweep, two lines from an edited line; caught by Opus 5 completeness hunt round 1 (1,12) | CN | Line corrected HISTORICAL with the catch credited |
| VALIDATION_TASKS.md | H1-R5 and H1-#76 sections presenting merged PRs #75/#77 as pending, no Historical markers — MISSED by the sweep AND the report certified the file "no update required"; caught by Opus 5 round 1 (12,9,1) | CN | HISTORICAL markers with era-completion facts (merge dates) added BENEATH the preserved-verbatim headings (the continuity suite binds to the exact heading text — a retitle broke 4 tests locally, was caught pre-push, and the binding is now noted in-file); dated cells preserved; report certification corrected |
| PROJECT_IMPLEMENTATION_ROADMAP.md L220 (#58 "active recovery authority") | Covered by its pre-existing P0-RECON banner at L224 | CURRENT_AND_CORRECT (banner-covered) | No change; recorded here for auditability per Opus round-1 note |
| All docs/archive/**, phase_*_report.md (self-describing), DECISION_LOG/DEVELOPMENT_LEDGER/MODEL_RUN_LOG dated entries, content/claims, artifacts, test fixtures | Era records describing their own phase | AH | Untouched |

Sweep summary (corrected in round 2 after the Opus 5 completeness hunt): corrections applied in this PR to 28 maintained documents plus 2 registers' append-only currency notes (30 total corrected surfaces); 1 finding out-of-lane (apps/web/README.md, routed); 1 finding owner-surface (resolved by owner comment 5245520671); formal RT-H0 version-chain updates routed (H7A-5/H9). Banner inventory, exact: ELEVEN per-file "P0-RECON-2 Supersession Note" banners plus PROMPT_CONVENTION.md's top-of-file SUPERSEDED banner (twelve banners total). The sweep analyst's FILES_SWEPT=118 was refuted as unauditable (no committed enumeration) — the Appendix below IS the auditable enumeration under a reproducible filter (121 files at this head; the analyst's count used a near-identical filter at base). Two residuals the analyst missed (rows above) were found by the Opus 5 hunt and corrected — the sweep's completeness claim is accordingly bounded: completeness within the twelve classes is asserted only as of the Opus-verified head, not the analyst's pass.

## Appendix — Auditable Sweep Enumeration (added in round 2 after the Opus 5 completeness hunt refuted the earlier unauditable "sweep record" reference)

Filter definition (reproducible): `git ls-files` entries ending `.md`/`.yaml`/`.yml`, excluding `docs/archive/**` and `artifacts/**`. Count under this filter at this head: 121. The originally reported FILES_SWEPT=118 was the sweep analyst's count under a near-identical filter at base 3fb3d4d; THIS enumeration at the PR head is the auditable record and supersedes that number where they differ (this PR adds 4 files matching the filter).

- .github/ISSUE_TEMPLATE/phase_issue.yml
- .github/dependabot.yml
- .github/pull_request_template.md
- .github/workflows/codeql.yml
- .github/workflows/control-gates.yml
- .github/workflows/dependency-review.yml
- .github/workflows/mobile-ci.yml
- .github/workflows/web-ci.yml
- AGENTS.md
- CONTRIBUTING.md
- README.md
- SECURITY.md
- apps/web/README.md
- content/claims/contractoros_phase_2e_law_claim_narrowing_report.md
- docs/TOOLCHAIN.md
- docs/project-control/AI_AUTHORITY_MODEL_AND_TOOL_SECURITY.md
- docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
- docs/project-control/ARTIFACT_INDEX.md
- docs/project-control/ASSUMPTION_REGISTER.md
- docs/project-control/AUTHORITY_AND_SUPERSESSION_INDEX.md
- docs/project-control/AUTOMATION_PHASE_ROADMAP.md
- docs/project-control/CLAIM_LEVELS_AND_RELEASE_GATES.md
- docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
- docs/project-control/CONTROL_FILE_UPDATE_MATRIX.md
- docs/project-control/CONTROL_GATE_AUTOMATION_PLAN.md
- docs/project-control/DECISION_LOG.md
- docs/project-control/DEVELOPMENT_CONTROL_MODEL_V3.md
- docs/project-control/DEVELOPMENT_LEDGER.md
- docs/project-control/DOCUMENTATION_MAINTENANCE_PROTOCOL.md
- docs/project-control/EPISTEMIC_INTEGRITY_AND_NON_FABRICATION_STANDARD.md
- docs/project-control/GOVERNANCE_CONTRACT_CONSUMPTION.md
- docs/project-control/HANDOFF_PLAYBOOK.md
- docs/project-control/INCIDENT_RESPONSE_AND_VULNERABILITY_TRIAGE_POLICY.md
- docs/project-control/JURISDICTION_PACK_ARCHITECTURE.md
- docs/project-control/KNOWN_GAPS_AND_NON_GOALS.md
- docs/project-control/LEGAL_REGULATORY_SOURCE_INTELLIGENCE_ARCHITECTURE.md
- docs/project-control/LOW_RISK_LANE_POLICY.md
- docs/project-control/MODEL_PROVIDER_COST_GOVERNANCE.md
- docs/project-control/MODEL_RUN_LOG.md
- docs/project-control/ORIGINALITY_REGISTER.md
- docs/project-control/OWNER_DECISION_REGISTER.yaml
- docs/project-control/PHASE_ONE_ACCEPTANCE_CRITERIA.md
- docs/project-control/PHASE_ONE_SCOPE.md
- docs/project-control/PHASE_ONE_TEST_PLAN.md
- docs/project-control/PRIVATE_CONTROL_PLANE_POLICY.md
- docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md
- docs/project-control/PROGRAM_ARCHITECTURE_DECISION_INDEX.md
- docs/project-control/PROGRAM_CONSTITUTION.md
- docs/project-control/PROJECT_FOUNDATION.md
- docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md
- docs/project-control/PROJECT_SCOPE_BOUNDARIES.md
- docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md
- docs/project-control/PROMPT_CONVENTION.md
- docs/project-control/RED_TEAM_CONTINUITY_ARCHITECTURE.md
- docs/project-control/RED_TEAM_FINDINGS_REGISTER.md
- docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md
- docs/project-control/RED_TEAM_STARTUP_PACKET_SPEC.md
- docs/project-control/RED_TEAM_STATE_MACHINE.md
- docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
- docs/project-control/RISK_REGISTER.md
- docs/project-control/ROLE_BOUNDARIES.md
- docs/project-control/SOURCE_REGISTER.md
- docs/project-control/THREAT_MODEL_H7A.md
- docs/project-control/VALIDATION_TASKS.md
- docs/project-control/WORKFLOW_AUTOMATION_COMMAND_PACK.md
- docs/project-control/WORKFLOW_AUTOMATION_TARGET_STATE.md
- docs/project-control/WORKFLOW_OPERATOR_RUNBOOK.md
- docs/project-control/adr/ADR-001-program-horizons-automation-and-product-priority.md
- docs/project-control/adr/ADR-002-ai-authority-development-and-write-boundaries.md
- docs/project-control/adr/ADR-003-red-team-continuity-and-public-private-control-plane.md
- docs/project-control/adr/ADR-004-legal-regulatory-and-source-intelligence.md
- docs/project-control/adr/ADR-005-national-jurisdiction-pack-and-product-architecture.md
- docs/project-control/adr/ADR-006-security-privacy-and-ai-tool-controls.md
- docs/project-control/adr/ADR-007-model-provider-paid-service-and-cost-governance.md
- docs/project-control/adr/ADR-008-product-validation-monetization-and-parallel-work.md
- docs/project-control/adr/ADR-009-program-constitution-supersession-and-decision-authority.md
- docs/project-control/contractoros_project_control_recovery.md
- docs/project-control/control-file-update-matrix.yml
- docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md
- docs/project-control/evidence/H6B2_TEST_LAYER_EVIDENCE.md
- docs/project-control/evidence/H7A1_SECURITY_POSTURE_INVENTORY.md
- docs/project-control/evidence/H7A3_SCANNING_EVIDENCE.md
- docs/project-control/evidence/P0_RECON_CLOSEOUT_ACCURACY_CORRECTION.md
- docs/project-control/evidence/RECON2_STALE_AUTHORITY_CLASSIFICATION.md
- docs/project-control/phase_codeowners_consolidation_report.md
- docs/project-control/phase_governance_corrections_52_report.md
- docs/project-control/phase_h0_durable_red_team_finding_governance_report.md
- docs/project-control/phase_h1_next_window_handoff_contract_gate_report.md
- docs/project-control/phase_h5c_archive_move_report.md
- docs/project-control/phase_h5d_authorization_bootstrap_arming_report.md
- docs/project-control/phase_h6_closeout_report.md
- docs/project-control/phase_h6a_dependency_pins_report.md
- docs/project-control/phase_h6a_toolchain_report.md
- docs/project-control/phase_h6b1_control_hardening_report.md
- docs/project-control/phase_h6b2_test_layers_report.md
- docs/project-control/phase_h6b2a_pre_authorization_report.md
- docs/project-control/phase_h7a_1_security_inventory_report.md
- docs/project-control/phase_h7a_2_policy_docs_report.md
- docs/project-control/phase_h7a_3_scanning_report.md
- docs/project-control/phase_p0_recon_2_report.md
- docs/project-control/phase_post_h5_reconciliation_report.md
- docs/project-control/phase_post_h5c_reconciliation_report.md
- docs/project-control/phase_post_h5d_reconciliation_report.md
- docs/project-control/phase_post_h6a_reconciliation_report.md
- docs/project-control/phase_post_h6b1_reconciliation_report.md
- docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md
- docs/project-control/phase_stress3_corrections_report.md
- docs/project-control/red-team/CLAIM_DOWNGRADE_MATRIX.md
- docs/project-control/red-team/FORBIDDEN_SCOPE_SCAN_PLAYBOOK.md
- docs/project-control/red-team/MAIN_VERIFICATION_CHECKLIST.md
- docs/project-control/red-team/PR_REVIEW_CHECKLIST.md
- docs/project-control/red-team/README.md
- docs/project-control/red-team/RECOVERY_PLAYBOOK.md
- docs/project-control/red-team/RED_TEAM_ANCHOR.md
- docs/project-control/red-team/RED_TEAM_HANDOFF_TEMPLATE.md
- docs/project-control/red-team/REVIEW_DECISION_LABELS.md
- docs/project-control/state/UNSYNCED_DECISIONS.schema.yaml
- docs/project-control/state/contractoros-state.schema.yaml
- docs/project-control/state/contractoros-state.yaml
- scripts/continuity/README.md
- scripts/continuity/tests/fixtures/expected_startup_packet.md
