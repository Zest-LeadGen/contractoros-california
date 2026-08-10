# H6-B.1 Control Hardening Gate Report

## Linked Phase Issue

#118 (H5+H6 batched; parent #64)

## Phase

H6-B.1 — product-CI foundations + control hardening: manifest pin scan, overclaim-gate fix, path-wall-from-main defense, Node-pin alignment, mobile CI.

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Under owner H6 authorization (issue #118 comment 5235003178; PA-0015 via bootstrap, closing PA-0014). Scope routed here by owner questionnaire Q8 (overclaim fix), Q9 (required-check wiring — CI jobs delivered here, ruleset act remains the owner's), and Q13 (H6-B go). Checker/CI edits presented for deliberate owner walk-through per R-STRESS-002 discipline. AUTOMATIC_CONTINUATION=NO.

## Scope

1. check_manifest_pins.py (NEW) + 11-case adversarial suite: exact-semver-only enforcement for every dependency declaration in governed manifests (dist-tags, ranges, wildcards, OR bars, URL/git/file specifiers rejected; absent root manifest skips by recorded decision). Closes the disclosed npm-ci/latest gap with a machine gate, wired into the required policy-validators job. Live scan: 7 declarations, all exact.
2. check_pr_contract.py: stress-run-3 overclaim regression fixed — "forbidden"/"blocked" moved out of FORWARD_QUALIFIERS to preceding-only semantics. Five-way verification recorded in DECISION_LOG (both bypass phrasings now flag; legitimate downgrades unaffected; original R-STRESS-004 case still flags).
3. phase-authorization-from-main (NEW blocking job in the aggregate needs): runs the BASE branch's copy of the path-wall checker against the PR, so a PR that edits the checker in its own tree still faces main's version (R-STRESS-002 structural mitigation). Scope disclosed: protects the wall; other validators remain PR-tree, backstopped by total CODEOWNERS coverage.
4. Node-pin single-sourcing: web-ci and the new mobile-ci read .nvmrc via node-version-file.
5. contractoros-mobile-ci (NEW workflow; advisory until the owner's required-check ruleset act): registry provenance, npm ci from the committed lockfile, drift check, expo config static validation, entry-module resolution. Every step verified locally against the committed manifest before delivery (expo config exit 0; entry resolves).
6. Root-manifest decision closed: none needed — per-app `npm ci --prefix` is the documented deterministic path; revisit only with separately-authorized monorepo tooling.

## Starting Main SHA

3e99f7d (CODEOWNERS consolidation merge of PR #131).

## Changed Files

- scripts/control/check_manifest_pins.py (new), scripts/control/tests/test_manifest_pins.py (new)
- scripts/control/check_pr_contract.py (modify: FORWARD_QUALIFIERS fix)
- .github/workflows/control-gates.yml (modify: pin-scan step, pin-suite step, phase-authorization-from-main job + aggregate wiring)
- .github/workflows/web-ci.yml (modify: node-version-file), .github/workflows/mobile-ci.yml (new)
- docs/project-control/authorizations/PA-0015.json (new), PA-0014.json (supersession closure only)
- docs/project-control/phase_h6b1_control_hardening_report.md (this report), DECISION_LOG.md, DEVELOPMENT_LEDGER.md

## Commands Run

- python3 scripts/control/tests/test_manifest_pins.py (11/11 PASS); live pin scan (7/7 exact)
- Five-way unit probe of overclaim_downgraded (all cases correct)
- Local verification of mobile-ci steps against the committed manifest (npx expo config exit 0; require.resolve('./App.js') OK)
- Six control validators against the real PR body pre-push; adversarial + continuity suites; armed checker self-test (bootstrap, closes PA-0014)

## Dependency / Lockfile Handling

None — no manifest or lockfile changes; this PR adds the gate that polices them.

## Documentation Impact

Control records only; TOOLCHAIN.md already documents the per-app install path this PR's decision confirms.

## Validation Evidence

Suites green (11/11 pins, 25/25 phase-authorization, 348/348 continuity); armed checker validates this PR in bootstrap mode (closed_records=[PA-0014]); the new from-main job validates this PR in CI using MAIN's checker (its first live exercise); validators green vs real body.

## Risk Register Impact

docs/project-control/RISK_REGISTER.md: reviewed, no update required by this PR (the npm-ci/latest gap's blocker entry in state.yaml clears at the next reconciliation; R-STRESS-002's structural mitigation is recorded in DECISION_LOG).

## Decision Log Impact

Adds the H6-B.1 entry: all five deliverables, the five-way overclaim verification, the root-manifest closure, and the remaining H6-B items.

## Artifact Index Impact

docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Security Hardening

Three enforcement upgrades: the manifest pin gate closes a proven npm blind spot; the from-main job removes the single-PR self-edit path around the wall; the overclaim fix restores claim-language integrity. No enforcement is weakened anywhere in this PR.

## Workflow Validation

control-gates.yml re-verified as a job graph: phase-authorization-from-main has no continue-on-error, is in the aggregate needs, is required-success on pull_request, and maps skipped-on-push exactly like its siblings; the pin-scan step is inside the always-required policy-validators job on both events; the H4A no-masking architecture is preserved. web-ci/mobile-ci parse cleanly; mobile-ci steps proven locally.

## Red-Team Status

RED_TEAM_MARKER=NOT_ADDED_PENDING_REVIEW — SHA-bound marker added at the review step.

## Human Approval Status

Owner approval required — this PR edits enforcement checkers and CI gates.

## Auto-Merge Status

Not eligible for auto-merge; owner-only merge.

## Forbidden Scope Confirmation

Confirmed — control scripts, control tests, CI workflows, and control records only; no app source, no continuity scripts, no path-wall checker edit (forbidden to this PA), no state snapshot, no governance mutation.

## Claim Level

Control hardening delivered for owner review. The new web-ci/mobile-ci contexts become ENFORCING only after the owner's ruleset act (required-check wiring) — until then they are advisory and labeled so.

## Known Limitations

- Required-check wiring is an owner console/ruleset act — the command is handed with this PR's key-turn; CI contexts are advisory until run.
- Design flaw caught before the ruleset act: path-filtered workflows cannot safely be required checks (an untriggered required check leaves the PR 'expected' forever). Fixed in this PR: web-ci and mobile-ci run on every pull request (11s + 23s cost) while main pushes remain path-filtered; the ruleset act is now safe.
- The from-main defense covers the path-wall checker only; other validators remain PR-tree (disclosed; CODEOWNERS total coverage is the backstop).
- Mobile validation remains static (install/config/entry); emulator/device layers stay tracked-blocked per the test-layer ledger.
- H6-B.2 (lint/format/typecheck/unit tests inside the apps, Product / QA lane) is the remaining H6-B deliverable.

## Next Phase Status

Next: owner key-turn for this PR + the required-check ruleset act, then H6-B.2 (Product / QA), then H5+H6 closeout on #118/#64. AUTOMATIC_CONTINUATION=NO.

## Owner Trigger Review

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Enforcement checker and CI gate changes; owner walk-through and review required.
