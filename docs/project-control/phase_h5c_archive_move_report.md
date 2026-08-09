# H5-C Archive Move Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #63)

## Phase

H5-C — move historical evidence into docs/archive/ (no history rewrite).

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under owner H5+H6 authorization (issue #118 comment 5233703034; PA-0007). Delivers the topology cleanup #63 exists for; no new gate or authority created.

## Scope

Relocate 52 completed-phase reports plus H0/H1 closeout lineage, incident records, and sanitation manifests from docs/project-control/ into docs/archive/. Add docs/archive/README.md. No file content is rewritten; git history is preserved via renames.

## Starting Main SHA

38499c8 (post H5 state reconciliation).

## Changed Files

- docs/archive/phase-reports/*.md (52 moved reports)
- docs/archive/H0_FINAL_DISPOSITION_REPORT.md, docs/archive/H1_CLOSEOUT_LINEAGE.md, docs/archive/incidents/*, docs/archive/sanitation/* (moved)
- docs/archive/README.md (new)
- docs/project-control/authorizations/PA-0007.json (new)
- docs/project-control/phase_h5c_archive_move_report.md (new)
- docs/project-control/DECISION_LOG.md, docs/project-control/DEVELOPMENT_LEDGER.md

## Commands Run

- git mv of the historical reports/dirs; docs/archive scanner exemption (landed in H5-B) keeps their legacy language from tripping forbidden-scope.
- PA-0007 schema validated (PASS); six control validators run against the real PR body pre-push.

## Dependency / Lockfile Handling

None.

## Documentation Impact

Large: docs/project-control/ no longer holds historical phase reports; they live under docs/archive/. Current source-of-truth documents are unaffected.

## Validation Evidence

PA-0007 SCHEMA=PASS; validators green vs real body; docs/project-control retains only 3 phase reports that are live continuity-test fixtures; the other 52 are archived.

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required

## Decision Log Impact

Adds the H5-C archive-move entry, including the disclosed deletion-authorization limitation.

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required (index references are updated in H5-B.2 link-validation; no link-checker gate blocks today)

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required.

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — documentation relocation only; no product, workflow, checker, or governance-repository mutation.

## Claim Level

Archive relocation only. Nothing beyond the move is claimed; roadmap/constitution collapse and wall arming remain separate.

## Known Limitations

Three reports (phase_h0_durable_red_team_finding_governance_report.md, phase_h1_next_window_handoff_contract_gate_report.md, phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md) remain in docs/project-control/ because the continuity test suite loads them as fixtures by path; moving them would require editing scripts/continuity/tests, which the scanner is not yet exempted for. Tracked for a later pass.

The renames/deletes of moved reports are not pattern-authorizable (schema allows add/modify only); executed under observe-only phase-authorization and disclosed. An exact-path deletion-authorization mechanism is a prerequisite for arming the wall. Cross-document links to moved reports are not yet updated (no link-checker gate today); tracked for H5-B.2.

## Next Phase Status

Next: PA-bootstrap + exact-path deletion authorization + wall arming (final H5 piece), then H6. AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Large documentation relocation into docs/archive/; owner authorization and review required.
