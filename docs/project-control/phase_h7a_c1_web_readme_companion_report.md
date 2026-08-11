# Phase H7A-C1 Report — Web README Deterministic-Install Companion <!-- Product / QA lane companion report -->

## Linked Phase Issue

Phase issue: #137 (parent #65). Authorization: PA-0027 (BASE mode — pre-authorized by the merged H7A-C0 PR under the standing H7A authorization issue-137-comment-5238006617; owner mid-gate direction "Go with readme", Option-B choice recorded in DECISION_LOG at H7A-C0).

## Phase

H7A-C1 — the owner-directed one-file companion: apps/web/README.md install instruction corrected from `npm install` to the delivered H6 deterministic baseline (`npm ci`).

## Lane

Product / QA

Lane: Product / QA — this blocked-without-approval category proceeds under explicit owner approval: the on-platform standing authorization issue-137-comment-5238006617 (which gates every H7A deliverable behind separate owner merge approval) plus the owner's merge key-turn on this PR itself (MERGE_AUTHORITY=OWNER_ONLY).

## Scope

Exactly two paths, both pre-authorized in PA-0027: apps/web/README.md (modify — install section only) and this companion report (add). BASE mode: this PR touches no authorization record and no other file. The doc change aligns the app readme with docs/TOOLCHAIN.md, the root README, and CONTRIBUTING.md (all H6/H7A-2 deliveries); `npm install` can mutate the committed lockfile, which the CI digest gate would then reject — the readme stops instructing that footgun.

## Starting Main SHA

9762ced9078fd689c1dd7566dfa440a54a5012cc (PR #151 merge, verified live 2026-08-11T00:06:41Z).

## Changed Files

- apps/web/README.md (modify — Install section: `npm install` -> `npm ci` with a one-line TOOLCHAIN pointer; no other line touched)
- docs/project-control/phase_h7a_c1_web_readme_companion_report.md (add — this report)

## Commands Run

Local checker battery + continuity suite at head (see Validation Evidence). No installs, no builds, no GitHub writes beyond branch push and PR records.

## Dependency / Lockfile Handling

None. No manifest or lockfile touched; the change makes the DOCUMENTED install command match the lockfile-preserving one CI already enforces.

## Documentation Impact

One app readme aligned with the toolchain authority. docs/project-control/RISK_REGISTER.md: reviewed, no update required. docs/project-control/DEVELOPMENT_LEDGER.md: reviewed, no update required (the H7A-C0 ledger entry covers this companion; the closure record follows with the owner's issue closures). docs/project-control/DECISION_LOG.md: reviewed, no update required (H7A-C0 entry covers it). docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Validation Evidence

Local checker battery at head via event payload: check_phase_authorization PASS (mode=base, PA-0027, changed_paths=2); all other checkers PASS including the Product/QA lane checks. Continuity suite 348/348 OK. The readme diff is exactly the Install section.

## Risk Register Impact

Reviewed, no update required.

## Decision Log Impact

Reviewed, no update required — the H7A-C0 entry records this companion's authorization and the owner decisions behind it.

## Artifact Index Impact

Reviewed, no update required.

## Red-Team Status

Per owner Decision 4: Opus 5, read-only, exact-head. Focus: the diff is exactly the two pre-authorized paths and the readme change is limited to the install instruction.

## Human Approval Status

Required. MERGE_AUTHORITY=OWNER_ONLY. On merge + verified main, the owner closes #137 and #65 — H7A reads COMPLETE only after those closures.

## Auto-Merge Status

Not eligible. Auto-merge remains prohibited.

## Forbidden Scope Confirmation

- [x] One readme instruction and this report only. PA-0027 forbids scripts/**, policy/**, content/**, docs/archive/**, .github/**, apps/web/src/**, both web manifests, and apps/mobile/**; the 2-path diff touches none of them. No product logic, dependency, scoring, readiness, auth-feature, backend, build, or release scope — the app's Not-included list is unchanged and true.

Forbidden scope confirmation: confirmed.

## Claim Level

Documentation alignment only; no runtime behavior changes. H7A reads COMPLETE only after this merge, verified main, and the owner's closures of #137/#65.

## Known Limitations

None beyond the standing routed items recorded at H7A-5 (this PR discharges routed item 1).

## Next Phase Status

H7A reads COMPLETE only after this merge, verified main, and the owner's closures of #137 and #65. Then H7B intake (own owner authorization; not-to-compress), then H8 intake carrying the owner's governed-automation decision (H8-ASAP intent recorded at H7A-C0 with its in-session qualifier). AUTOMATIC_CONTINUATION=NO.
