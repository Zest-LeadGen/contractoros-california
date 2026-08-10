# Phase H7A-3 Report — Automated Scanning <!-- documentation scope -->

## Linked Phase Issue

Phase issue: #137 (parent #65). Standing authorization: issue-137-comment-5238006617; owner "Proceed" recorded in-session after the P0-RECON hold lifted (PR #142 merged, #141 closed, main 1f67dc9 verified 18:48:27Z).

## Phase

H7A-3 — automated scanning deliverable of H7A: Dependabot configuration, dependency-review workflow re-add, secret-scanning/push-protection verification path, private-data/credential-pattern scan.

## Lane

Control / Infrastructure

## Scope

PA-0023 bootstrap closing PA-0020 (base advanced to 1f67dc9). Adds `.github/dependabot.yml` and `.github/workflows/dependency-review.yml`; executes and evidences the private-data scan; stages the owner setting authorization for secret scanning + push protection (L-1 closure path); records + state snapshot. No product, dependency, or control-script change; the four existing workflows and CODEOWNERS are PA-forbidden and untouched.

## Starting Main SHA

1f67dc93178e9d4231f899369b179077a883bc2e (PR #142 merge, verified live 2026-08-10T19:06:17Z).

## Changed Files

- .github/dependabot.yml (add)
- .github/workflows/dependency-review.yml (add)
- docs/project-control/authorizations/PA-0023.json (add)
- docs/project-control/authorizations/PA-0020.json (modify — supersession closure only)
- docs/project-control/evidence/H7A3_SCANNING_EVIDENCE.md (add)
- docs/project-control/phase_h7a_3_scanning_report.md (add — this report)
- docs/project-control/DECISION_LOG.md (modify — append only)
- docs/project-control/DEVELOPMENT_LEDGER.md (modify — append only)
- docs/project-control/state/contractoros-state.yaml (modify)

## Commands Run

Read-only grounding reads (captured timestamps): live main (19:06:17Z), `actions/dependency-review-action` latest release tag + tag-object SHA (v5.0.0 → a1d282b3, resolved live); one-time private-data scan over `git ls-files` (258 files, nine pattern classes, 19:04:50Z; method recorded in the evidence file; scan script not committed). Local control checker battery and continuity suite (see Validation Evidence). No GitHub write commands; no dependency installs or builds.

## Dependency / Lockfile Handling

None. No manifest or lockfile touched. Dependabot is configured as an advisory signal only: its PRs cannot pass the default-deny wall (no PA record) and cannot merge (owner-only); real dependency changes ride authorized dependency-lane PRs under the H6 exact-pin + digest baseline.

## Documentation Impact

Evidence file records the scanning delta from the H7A-1 baseline, the scan result (clean; one benign test fixture classified), and the pending items honestly (Dependabot first-run function evidence; owner secret-scanning key-turn). docs/project-control/RISK_REGISTER.md: reviewed, no update required. docs/project-control/AUTHORITY_AND_SUPERSESSION_INDEX.md: reviewed, no update required. docs/project-control/VALIDATION_TASKS.md: reviewed, no update required. docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Workflow Validation

New workflow only (`dependency-review.yml`): `on: pull_request`, single job, single step, minimal `permissions: contents: read`, `timeout-minutes: 10`, concurrency group with cancel-in-progress, the sole action ref SHA-pinned to a1d282b36b6f3519aa1f3fc636f609c47dddb294 (commit behind lightweight tag v5.0.0, independently verified by Opus 5 round 1), `fail-on-severity: high`. NO checkout step: the action reads the dependency diff via the API and needs no repository contents — Opus 5 round 1 caught the earlier draft carrying an unnecessary tag-pinned `actions/checkout@v4` while the records claimed full pinning; the step was removed rather than pinned, and the whole-file-pinned claim is now true because the file has exactly one ref. No `pull_request_target`, no secrets, no write permissions. The four existing workflows are untouched (PA-forbidden); their 15 tag-pinned refs are H7A-4 scope.

## Security Hardening

Dependency-review closes the T1 (malicious/compromised dependency) PR-time gap identified in THREAT_MODEL_H7A.md; the new workflow carries minimal permissions, a timeout, concurrency control, a single SHA-pinned ref, and no checkout (scoped claim — full-fleet SHA pinning and hardening of the four existing workflows is H7A-4); the private-data scan closes the T12 machine-check gap for the base snapshot (recurring CI scan routed to H7A-4/H7B where workflow/control-script lanes open). Secret scanning + push protection (T6) verified state lands via the staged owner key-turn.

## Validation Evidence

Local checker battery at head via event payload: check_phase_authorization PASS (mode=bootstrap, PA-0023, closed_records=[PA-0020]); check_pr_contract, check_owner_trigger_review, check_forbidden_scope, check_changed_files, check_required_control_updates, check_manifest_pins, check_low_risk_lane, check_contract_consumption PASS. Continuity suite 348/348 OK (fixture-based, per the recorded caveat). Digest quoted in the PR body recomputed at the PR head. actionlint-equivalent manual review of the new workflow recorded above (Workflow Validation).

## Risk Register Impact

Reviewed, no update required. R-DEP-SEC-001 next revisit remains H7A closeout or H7B intake; the new dependency-review gate does not alter the accepted alerts (they are existing lockfile alerts, not PR-introduced changes).

## Decision Log Impact

H7A-3 entry appended: deliverables, advisory-signal posture, scan result with the classified fixture, staged L-1 key-turn, and the not-yet-required-context disclosure.

## Artifact Index Impact

Reviewed, no update required — no files under artifacts/ changed.

## PR Template / CODEOWNERS Implemented

No CODEOWNERS or PR-template change in this PR (CODEOWNERS is PA-forbidden here; its catch-all already covers the two new .github files).

## Red-Team Status

Per owner Decision 4: Opus 5, read-only, exact-head review with the 12-field marker attestation. Marker added to the PR body after the PR exists; stale on any head change.

## Human Approval Status

Required. MERGE_AUTHORITY=OWNER_ONLY; owner review and key-turn merge required. Approver principals per PA-0023.

## Auto-Merge Status

Not eligible. Auto-merge remains prohibited. Dependabot PRs are advisory signals with no merge path.

## Forbidden Scope Confirmation

- [x] Scanning configuration, evidence, and authorization records only. PA-0023 forbids `apps/**`, `scripts/**`, `policy/**`, `content/**`, `docs/archive/**`, the four existing workflows, and CODEOWNERS; the diff touches none of them. No dependency, build, backend, product, or content scope; no historical evidence rewritten.

Forbidden scope confirmation: confirmed.

## Claim Level

Configuration + evidence only. Dependency-review runs on PRs but is NOT yet a required ruleset context (owner act, considered at H7A-5) — no enforcement claimed beyond what the ruleset actually requires. Dependabot version-update function evidence is PENDING the first scheduled run. Secret-scanning/push-protection state remains NOT_PROVEN until the owner key-turn read-back lands. H7A-4/H7A-5 are unstarted and unclaimed.

## Known Limitations

1. L-1 open pending the staged owner key-turn; the evidence file's §3 records the pending marker and is updated on execution. 2. Dependabot first-run evidence pending (captured at next phase boundary). 3. Recurring private-data CI scan deferred to the phase whose lane holds workflows/control scripts. 4. The two P0-RECON advisory wording remnants (PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md phase-sequence section) are NOT in this PR's allowlist — they remain routed to the next control phase holding that path, per the Opus 5 marker on PR #142.

## Next Phase Status

On merge: H7A-3 recorded; next is H7A-4 (workflow hardening: SHA pins for all remaining refs, timeouts, concurrency, persist-credentials, workflow security analysis) as its own PA-bound PR under #137 — its allowlist will name the four existing workflows and may carry the two advisory wording remnants. AUTOMATIC_CONTINUATION=NO.
