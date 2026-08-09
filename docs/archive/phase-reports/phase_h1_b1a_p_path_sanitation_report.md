# H1-B1A-P Path Sanitation Gate Report

## Linked Phase Issue

Phase issue: #96

Parent issue: #58

## Phase

H1-B1A-P — Product-Repository Path Sanitation (manifest, token replacement, history preservation)

## Lane

Control / Infrastructure

## Authority <!-- documentation scope -->

Owner phase authorization posted on Issue #96 resolves open decisions H1B1-OD-007 and H1B1-OD-008 and acknowledges the disclosed H1B1-GATE-001 sequence deviation. This report grants no closeout, next-gate, product, or production authority.

## Scope

Replace the 10 non-exempt absolute-path occurrences in 6 historical phase reports with sanitation tokens per SAN-001; add the SAN-002 sanitation manifest; record decisions and risk; and apply the bounded sanitation-companion amendment to the two affected control validators (necessity documented under Changed Files). No deletion, no history rewrite, no branch mutation, no product source change.

## Starting Main SHA

`d031fd23efa1059015f265aabe1aafbf0a0b7fc1`

## Changed Files

- 6 historical phase report files (token replacement only; listed in the manifest)
- `docs/project-control/sanitation/H1_B1A_P_SANITATION_MANIFEST.md` (new)
- `docs/project-control/DEVELOPMENT_LEDGER.md`
- `docs/project-control/DECISION_LOG.md`
- `docs/project-control/RISK_REGISTER.md`
- `docs/project-control/phase_h1_b1a_p_path_sanitation_report.md` (new)
- `scripts/control/check_required_control_updates.py` (bounded amendment)
- `scripts/control/check_low_risk_lane.py` (bounded amendment)

No other path is changed. The two validator amendments add only the sanitation-companion rule: when the change set carries a sanitation manifest, pre-existing phase reports are treated as historical sanitized text rather than the current phase report. Discovered necessity: without this rule, any sanitation of historical reports structurally cannot pass the gates (seven files were counted as "current phase reports" and their historical owner-trigger markers conflicted).

## Commands Run

- Read-only scope: `git grep` over the full tracked tree for the pattern classes `/Users/`, `/private/tmp`, `~/Documents`, `/home/` — 11 occurrences found and classified.
- Token replacement via bounded per-file substitution; residual scan confirms only the single EXEMPT synthetic fixture remains.
- Control validators, continuity tests, and `git diff --check` — results in Validation Results.

## Dependency / Lockfile Handling

No dependency or lockfile path is changed. No install, package-manager, build, or dependency-resolution command is authorized or run.

## Documentation Impact

Six historical reports now carry `<OWNER_HOME>` / `<TEMP_DIRECTORY>` tokens in place of operator-machine absolute paths; their original bytes remain accessible through prior SHAs per SAN-006, and the sanitation manifest records every occurrence with classification and justification. The decision log records the OD-007/OD-008 resolutions and the owner-accepted sequence deviation.

## Validation Evidence

- Residual scan: zero non-exempt absolute-path occurrences in the current tree after replacement.
- Manifest completeness: 11/11 scanned occurrences classified (10 sanitized, 1 exempt).
- Continuity suite and all control validators run on the branch.

## Validation Results

- Continuity test discovery: passed, 344 tests.
- All six control validators: passed locally in replicated PR context.
- `git diff --check`: passed.
- Current remote, PR-body, workflow, and review outcomes are `LIVE_GITHUB_REQUIRED` and cannot be asserted from repository text.

## Risk Register Impact

Adds `R-B1AP-001` (public-tree absolute-path exposure superseded), mitigated for the current tree with documented residual (historical blobs unchanged by design).

## Decision Log Impact

Adds the H1-B1A-P Sanitation Decisions section: OD-007 and OD-008 resolutions, the sequence-deviation record, and the fixture exemption record.

## Artifact Index Impact

No artifact index update is required. This phase creates no binary, archive, build, release, hosted, or external artifact.

`docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required`

## Red-Team Status

No review of this PR has occurred yet. The developer did not self-review and did not add a `RED_TEAM_DECISION` marker. Per the owner-selected both-keys flow, an owner-directed verification review with disclosed non-independence follows delivery at the exact head SHA.

## Human Approval Status

Human/write-access approval is not granted by this report and remains required before merge.

## Auto-Merge Status

Auto-merge is inactive and ineligible. No automatic continuation is authorized.

## Forbidden Scope Confirmation

- [x] No product source, mobile, web, content, backend, or database mutation.
- [x] No dependency, lockfile, build, deployment, release, or production mutation.
- [x] No workflow, credential, or governance-repository mutation; the two control-validator amendments are the disclosed sanitation-companion rule only, named in the allowlist and covered by the owner phase authorization.
- [x] No deletion, no git-history rewrite, no branch mutation (SAN-003/004/005 honored).
- [x] No review, approval, merge, issue closeout, or next-gate start within this delivery.

Forbidden scope confirmation: confirmed for this bounded sanitation phase.

## Claim Level

Current-tree sanitation only. `ABSENCE_OF_UNDISCOVERED_FILES=NOT_PROVEN`; the scan covered four pattern classes over tracked files and does not prove exhaustive absence of every possible leak class. Historical blobs intentionally retain original text per SAN-006.

## Known Limitations

Pattern-class scanning cannot prove completeness (H1B1-TREE-016 analog applies); H1_B2 adversarial validation is the designated deeper check. Non-main branches retain original text by owner decision OD-008.

## Remaining Gates

1. Hosted control-gates run on this PR head.
2. Owner-directed verification review at the exact head SHA.
3. Owner phase authorization on Issue #96 resolving OD-007/OD-008 (documentation scope), then protected merge.
4. Verify `main`; close Issue #96.
5. Remaining H1 gates in canonical order: B1B_P, B2, B3, B4, B5.

## Next Phase Status

No next phase is authorized by this report. `NEXT_GATE=HOSTED_GATES_THEN_OWNER_DIRECTED_REVIEW`.

## Owner Trigger / Lane Eligibility Evidence

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Sanitation touches historical evidence text and resolves two open owner decisions, so owner and review gates remain required.
