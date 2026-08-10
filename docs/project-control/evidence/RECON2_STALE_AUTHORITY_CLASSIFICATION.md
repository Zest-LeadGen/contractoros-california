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
| All docs/archive/**, phase_*_report.md (self-describing), DECISION_LOG/DEVELOPMENT_LEDGER/MODEL_RUN_LOG dated entries, content/claims, artifacts, test fixtures | Era records describing their own phase | AH | Untouched |

Sweep summary: FILES_SWEPT=118; FILES_WITH_FINDINGS=30; corrections applied in this PR to 27 maintained documents + 2 registers' append-only notes; 1 finding out-of-lane (apps/web/README.md, routed); 1 finding owner-surface (resolved by owner comment 5245520671); formal RT-H0 version-chain updates routed (H7A-5/H9). Files re-checked clean: README.md, AGENTS.md, PROGRAM_CONSTITUTION.md, SECURITY.md, CONTRIBUTING.md, docs/TOOLCHAIN.md, all workflows, red-team pack, and the ~40 other maintained files enumerated in the sweep record.
