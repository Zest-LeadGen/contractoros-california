# H5-D Authorization Bootstrap + Wall Arming Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #63)

## Phase

H5-D — final H5 piece: PA-bootstrap, exact-path relocation authorization, single-live-record consolidation, and arming the path-scope wall.

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under owner H5+H6 authorization (issue #118 comment 5233703034; PATH_WALL_DECISION=ARM_NOW; PA-0009, introduced by this PR via the bootstrap mechanism it delivers). Scope trace disclosed: the comment's gate list names H5-A..H5-C; this delivery is the comment's "arm the path wall" first-deliverable item plus the two prerequisites the committed state snapshot records for it ("PA-bootstrap + exact-path deletion authorization, then arming the path wall"). AUTOMATIC_CONTINUATION=NO — owner approval of this PR is the continuation consent.

## Scope

1. check_phase_authorization.py BOOTSTRAP extension: a PR may introduce exactly one authorization record for its linked issue. Mandatory conditions: filename matches authorization_id; record not revoked; evidence_id is on-platform (issue-N-comment-id for the linked issue); repository binding matches; every live base record for the issue is closed in the same PR by a content-verified supersession edit (only supersession.revoked false->true and revocation_evidence null->string naming the new record may change) with each closed ID listed in the new record's supersedes; the record must self-authorize its own addition and each closure via exact-path rules.
2. RELOCATE extension: content-identical renames (git R100) are authorizable only by exact-path relocate rules (pattern = old path, "to" = new path). Renames with content drift (R<100), copies, and pattern renames remain denied. Authorization records are never deletable or relocatable.
3. Defect fix (found in pre-arming verification): all six H5 records (PA-0003..PA-0008) were live simultaneously for issue #118, so the checker's exactly-one resolution computed DENY found=6 for every #118 PR — invisible under observe mode. PA-0009 supersedes and revokes all six; the bootstrap closure rule enforces a single-live-record-per-issue invariant going forward.
4. Wall ARMED: control-gates.yml job renamed authorization-observe -> phase-authorization; continue-on-error and the observation step removed; job added to the aggregate needs list and required on pull_request events (skipped tolerated on main pushes, matching pr-contract/red-team-marker). OPS-005 observe-only window ended.
5. Companion governance PR: phase-authorization schema 1.1.0 — change_kinds enum gains "delete" and "relocate" (fixing the 1.0.0 contradiction where the checker and PA-0007's disclosed limitation assumed delete rules the enum forbade), optional "to" field, schema_version enum ["1.0.0","1.1.0"]. PA-0009 uses only add/modify and remains 1.0.0-conformant.

## Starting Main SHA

59949ed (post-H5-C reconciliation merge of PR #124).

## Changed Files

- scripts/control/check_phase_authorization.py (bootstrap/closure/relocate extensions, armed docstring)
- scripts/control/tests/test_phase_authorization.py (adversarial suite 8 -> 25 cases)
- .github/workflows/control-gates.yml (phase-authorization armed and required)
- docs/project-control/authorizations/PA-0009.json (new; bootstrap record)
- docs/project-control/authorizations/PA-0003..PA-0008.json (supersession closure only)
- docs/project-control/phase_h5d_authorization_bootstrap_arming_report.md (this report)
- docs/project-control/DECISION_LOG.md, DEVELOPMENT_LEDGER.md, RISK_REGISTER.md

## Commands Run

- python3 scripts/control/tests/test_phase_authorization.py (25/25 PASS)
- Full continuity suite; six control validators against the real PR body pre-push
- Live checker self-test: the armed checker validates THIS PR in bootstrap mode (PA-0009 governs; six closures verified)

## Dependency / Lockfile Handling

None.

## Documentation Impact

Control-surface only: authorization mechanics, risk register, decision log, ledger. No product documentation affected.

## Validation Evidence

Adversarial suite 25/25; continuity suite green; checker PASS (mode=bootstrap, closed_records=PA-0003..PA-0008) against this PR's real diff and body; validators green vs real body.

## Risk Register Impact

R-STRESS-001 RESOLVED (wall armed) with a dated resolution note disclosing the bootstrap trust model and the found=6 defect.

## Decision Log Impact

Adds the H5-D entry: authority trace, defect record, extension semantics, governance schema companion, and the PA-0001/PA-0002 out-of-scope note.

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Security Hardening

The wall cutover is itself the hardening: path-scope enforcement moves from advisory (observe-only, result discarded) to blocking (aggregate-required). Default-deny now has teeth: unmatched paths, forbidden paths, drifted renames, copies, unauthorized deletes, and authorization-record tampering (delete/relocate/foreign-issue add/non-closure modify) all block merge. Residual trust model disclosed under Known Limitations.

## Workflow Validation

control-gates.yml changes reviewed as a job graph: phase-authorization has no continue-on-error, is listed in the aggregate needs, and is required-success on pull_request events with skipped tolerated only on main pushes (identical treatment to pr-contract and red-team-marker, whose push-skip semantics are already proven on main). YAML parsed and job-condition logic verified locally; the H4A no-masking architecture (independent always-run jobs, single aggregate) is preserved.

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required — this PR edits the enforcement checker and CI gates (R-STRESS-002: CI is self-referential; owner review is the primary control for checker changes).

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — control checker, control tests, control workflow, authorization records, and control documentation only; no product code, no continuity scripts, no state snapshot, no governance-repository mutation from this PR (the schema change is a separate owner-approved governance PR).

## Claim Level

Delivered for owner review. The wall is armed only when this PR merges; nothing is claimed as merged-and-main-verified before the owner key-turn.

## Known Limitations

- Bootstrap shifts the wall from pre-authorized-on-main to authorized-in-same-PR; the authorization judgment rests on CODEOWNERS owner review of docs/project-control/** plus owner-only merge. Structural hardening (checkers run from main; author-identity checks) remains tracked to H6-B.
- Relocations must be content-identical (R100); a move-plus-edit must land as an authorized relocate plus a separate authorized modify, or it is denied.
- PA-0001 (#111) and PA-0002 (#113) remain live for closed issues (no live collision; expiry 2026-08-16); closure deferred to the next reconciliation.
- The state snapshot still lists arming as remaining; the post-merge reconciliation PR updates it (state file is forbidden to this PA by design).

## Next Phase Status

Next: post-H5-D reconciliation (snapshot), then H5 closeout on #118 and H6 intake — H6 requires its own owner authorization comment first. AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Enforcement checker and CI gate changes with wall arming; owner walk-through and review required.
