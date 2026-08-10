# Stress-Run-3 Corrections Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #64)

## Phase

Stress-run-3 corrections + post-#129 reconciliation, batched per owner questionnaire Q4 (2026-08-10).

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under owner H6 authorization (issue #118 comment 5235003178; PA-0013 via bootstrap, closing PA-0012 — schema 1.1.0 record, first live use of an exact-path delete rule). Every disposition herein traces to the owner's 13-question decision questionnaire answered 2026-08-10; the questionnaire outcomes are recorded in DECISION_LOG. AUTOMATIC_CONTINUATION=NO.

## Scope

1. Snapshot reconciled to live main 1f493f6 (#129 merged by owner 03:30:34Z) with a REAL second-precision github_verified_at (03:32:21Z, captured at the actual gh read) and a new snapshot_semantics rule forbidding rounded/projected verification timestamps.
2. R-STRESS-005 recorded: the authorized spot-check of all 22 snapshot revisions found EIGHT with verification timestamps after their own commit time — fabricated, systemic to the 2026-08-08/09 sessions. Underlying facts independently re-verified true; history disclosed, not rewritten; the Opus 5 hourly auditor now independently checks timestamp plausibility.
3. Evidence-of-record corrections with dated annotations (verify-number-freshness): mobile resolved URLs 473→481; npm ci count 463→471; web license line → 43 lockfile entries (npm ci installs 20). The two merged phase reports carrying the stale numbers are left unedited as historical records, corrected here and in DECISION_LOG.
4. R-DEP-SEC-001 status → ACCEPTED with dated revisit (owner Q2 + #129 approval text); next revisit H6-B closeout.
5. Committed .pyc removed from scripts/control/tests/ (exact-path delete rule in PA-0013); __pycache__/ gitignored.
6. Stress-test workflow script committed to scripts/control/stress/contractoros-st.workflow.js — the path the /contractoros-st skill references, now versioned with current-era targets.
7. Owner questionnaire outcomes recorded in DECISION_LOG, including the Q10 override: hourly auditor repinned to claude-opus-5 (sole permitted non-Fable model under OD-017, read-only cloud audit only) with a PA-chain-era prompt; and Q3: the undisclosed amkb80 credential logged out by the owner, verified absent — closing stress-run-3's first HIGH.

## Starting Main SHA

1f493f6 (post-H6-A reconciliation merge of PR #129).

## Changed Files

- docs/project-control/state/contractoros-state.yaml (modify)
- docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md (modify; dated correction annotations)
- docs/project-control/RISK_REGISTER.md (modify; R-DEP-SEC-001 disposition + R-STRESS-005)
- docs/project-control/DECISION_LOG.md, DEVELOPMENT_LEDGER.md (modify)
- docs/project-control/authorizations/PA-0013.json (new), PA-0012.json (supersession closure only)
- scripts/control/stress/contractoros-st.workflow.js (new)
- docs/project-control/phase_stress3_corrections_report.md (this report)
- .gitignore (modify), scripts/control/tests/__pycache__/test_phase_authorization.cpython-314.pyc (delete)

## Commands Run

- Live verification read at 03:32:21Z (main SHA, open PR count 0, 3 open Dependabot alerts)
- Timestamp spot-check across all 22 snapshot revisions (git log + git show per revision)
- Recounts on the digest-bound lockfiles (resolved URLs, package entries, license distribution)
- Six control validators against the real PR body pre-push; adversarial + continuity suites; armed checker self-test (bootstrap, closes PA-0012, exercises the delete rule)

## Dependency / Lockfile Handling

None — no manifest or lockfile changes; corrections are to the evidence text describing them.

## Documentation Impact

Evidence-of-record and risk register now match reality; snapshot semantics carry the timestamp rule; the stress workflow is versioned at its referenced path.

## Validation Evidence

Armed phase-authorization gate validates this PR in bootstrap mode (closed_records=[PA-0012]) including the exact-path .pyc delete; validators green vs real body; suites green.

## Risk Register Impact

R-DEP-SEC-001 → ACCEPTED with dated revisit (owner disposition). R-STRESS-005 added (systemic fabricated timestamps; rule + independent auditor check now live).

## Decision Log Impact

Full owner questionnaire record (Q1–Q13, including the Opus 5 auditor override and OD-017 scope note), R-STRESS-005, and the evidence corrections.

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required.

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — control records, risk register, evidence annotations, one binary-artifact deletion, and the stress workflow file only; no product code, no control-script logic (scripts/control/*.py forbidden to this PA), no workflows, no governance mutation.

## Claim Level

Record corrections and reconciliation only. Nothing new is claimed about the toolchain; the corrected numbers carry dated annotations preserving what was originally (wrongly) recorded.

## Known Limitations

- The eight fabricated historical timestamps remain in git history by design (archive-don't-rewrite); their falsity is now a first-class disclosed record.
- The two merged H6-A phase reports still contain the stale 463/473 numbers in their historical text; corrected here rather than by editing history.
- CODEOWNERS consolidation (stress-run-3's second HIGH) intentionally NOT in this PR — it follows immediately as its own dedicated PR per owner Q7.

## Next Phase Status

Next: CODEOWNERS consolidation PR (owner Q7), project-report Edition 5 (owner Q5), then H6-B (owner Q13 go). AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Record-integrity corrections including a disclosed systemic timestamp fabrication; owner review required.
