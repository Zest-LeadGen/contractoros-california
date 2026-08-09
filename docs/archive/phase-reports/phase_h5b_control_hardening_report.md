# H5-B Control-Script Hardening Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #63)

## Phase

H5-B — control-script hardening (scanner archive/control exemption + R-STRESS-004 overclaim fix).

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under the owner H5+H6 authorization on issue #118 (comment 5233703034; PA-0005). This PR edits the control checkers themselves — the highest-trust surface — and is presented for deliberate owner review rather than routine merge.

## Scope

Two checker fixes required before the H5 archive move and before arming the path wall:

1. `check_forbidden_scope.py` — exempt `docs/archive/` and `scripts/control/` from term-scanning. Archive holds immutable historical reports whose legacy language is audit evidence, not new work; control code legitimately contains the scanned term literals (`auth`, `fetch`, `readiness`). Both are governed by CODEOWNERS review and the control-script test suite instead.
2. `check_pr_contract.py` — fix R-STRESS-004: an overclaim is downgraded only when a negation PRECEDES the term (forward qualifiers such as "only after" still count anywhere), so "complete with no open blockers" no longer bypasses the gate.

This PR does not arm the path wall and does not move any archive files; those are separate follow-ups.

## Starting Main SHA

a1aac8a (post H5-B.1 merge).

## Changed Files

- `scripts/control/check_forbidden_scope.py` (archive/control term-scan exemption)
- `scripts/control/check_pr_contract.py` (R-STRESS-004 proximity fix)
- `docs/project-control/authorizations/PA-0005.json` (new)
- `docs/project-control/phase_h5b_control_hardening_report.md` (new)
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/DEVELOPMENT_LEDGER.md`

## Commands Run

- PA-0005 JSON-schema validated (PASS).
- Phase-authorization adversarial suite and 344-test continuity suite re-run after the edits (both PASS).
- Overclaim fix exercised against 8 in-line cases (bypass now flagged; legitimate downgrades still pass).
- Six PR-context control validators run against the real PR body pre-push, using the edited checkers.

## Dependency / Lockfile Handling

None.

## Documentation Impact

Adds this report; records the R-STRESS-004 resolution in the risk register.

## Validation Evidence

PA-0005 SCHEMA=PASS; adversarial + continuity suites PASS post-edit; overclaim regression cases pass; forbidden-scope no longer flags exempt paths.

## Risk Register Impact

Marks R-STRESS-004 corrected and records the fix detail plus the residual (a dedicated pr-contract regression test is not yet wired into CI).

## Decision Log Impact

Adds the H5-B control-hardening entry describing both checker changes and the CI-self-referentiality reason they were needed.

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step. Note: this PR changes the very checkers that enforce claims, so owner review is the primary control here (R-STRESS-002).

## Human Approval Status

Owner approval is required; highest-trust surface, deliberate review requested.

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — edits only `check_forbidden_scope.py` and `check_pr_contract.py` plus documentation. Does not touch `check_phase_authorization.py`, `check_changed_files.py`, product code, workflows, or the governance repository.

## Claim Level

Two scoped checker fixes with in-line verification. Nothing beyond these two fixes is claimed; the archive move and wall arming are explicitly not performed here.

## Known Limitations

A dedicated regression test for `check_pr_contract` is not yet wired into the control-script-tests CI job (follow-up). Exempting `scripts/control/` from term-scanning means control code is not term-scanned; that surface is instead protected by CODEOWNERS and the control-script tests, a disclosed tradeoff forced by CI self-referentiality (R-STRESS-002).

## Next Phase Status

Next: PA-bootstrap handling + arming the path wall (separate PR), then the archive move (now unblocked by the archive exemption). AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Edits the enforcement checkers themselves; owner review is the primary control for this change.
