# Phase H7A-4 Report — Workflow Hardening <!-- documentation scope -->

## Linked Phase Issue

Phase issue: #137 (parent #65). Standing authorization: issue-137-comment-5238006617; resumption basis on-platform (RECON-2 merged as PR #148, main ff2400e verified 21:14:33Z, #144 closed); owner "Go" concurred in-session with scope chosen as workflows + bytecode removal only.

## Phase

H7A-4 — workflow hardening deliverable of H7A: full-SHA action pins, bounded timeouts, concurrency control, credential-persistence hardening, and the routed control-checker bytecode removal.

## Lane

Control / Infrastructure

## Scope

PA-0025 bootstrap closing PA-0023 (base advanced to ff2400e). Modifies the four pre-existing workflows (codeql, control-gates, web-ci, mobile-ci) mechanically; deletes the tracked `scripts/control/__pycache__` bytecode via the wall's explicit exact-path delete rule (first use of the delete change_kind); evidence + records + state refresh. The routed apps/web/README.md fix is NOT included (owner chose plain "go"; it remains routed to H7A-5). dependency-review.yml, CODEOWNERS, dependabot.yml, and all control/continuity scripts are PA-forbidden and untouched.

## Starting Main SHA

ff2400e32fd17385f7828a76e7369438cc361fec (PR #148 merge, verified live 2026-08-10T21:29:27Z).

## Changed Files

Exactly the PA-0025 allowlist: 3 adds (PA-0025.json, evidence/H7A4_WORKFLOW_HARDENING_EVIDENCE.md, this report), 8 modifications (four workflows, PA-0023 supersession closure, DECISION_LOG, DEVELOPMENT_LEDGER, state), 1 delete (the tracked .pyc).

## Commands Run

Live tag resolutions (captured 21:25:23Z): `gh api repos/{actions/checkout,actions/setup-node}/git/ref/tags/v4` and `repos/github/codeql-action/git/ref/tags/v3` with annotated-tag dereference via `git/tags/{sha}`; local js-yaml parse validation of all four edited workflows; fresh main read (21:29:27Z); local checker battery + continuity suite (see Validation Evidence). No dependency installs, no GitHub writes beyond branch push and PR records.

## Dependency / Lockfile Handling

None. No manifest or lockfile touched. Action SHA pins change WHAT CODE runs in CI, not product dependencies; each pin is commented with its human-readable tag for auditability.

## Documentation Impact

Evidence file records the SHA resolution table (with the annotated-tag dereference), the before/after ref inventory, the per-workflow hardening matrix, the bytecode-removal record, and the concurrency-cancellation disclosure; DECISION_LOG and DEVELOPMENT_LEDGER carry the phase entries; canonical state advances to h7a_4_in_review from fresh live reads. docs/project-control/RISK_REGISTER.md: reviewed, no update required. docs/project-control/AUTHORITY_AND_SUPERSESSION_INDEX.md: reviewed, no update required. docs/project-control/VALIDATION_TASKS.md: reviewed, no update required. docs/project-control/ARTIFACT_INDEX.md: reviewed, no update required.

## Workflow Validation

All four edited workflows parse-validated locally (js-yaml). Hardening per workflow recorded in the evidence matrix: 16 of 16 `uses:` refs across all five workflows now full-commit-SHA pinned (zero tag pins remain — `grep "@v[0-9]"` empty); timeouts 30/15/15/10; per-workflow concurrency groups with cancel-in-progress (superseded-run cancellation disclosed; required contexts re-evaluate on the latest run); persist-credentials:false on all 11 checkouts. control-gates.yml: mechanical hardening only — every job, step, command, needs-list, and aggregate rule byte-unchanged; the diff is reviewable line-by-line as pins/timeouts/concurrency/credential flags plus one header comment.

## Security Hardening

Closes the H7A-1 inventory §2 gaps for the entire fleet (T1 moved-tag exposure eliminated by commit pins including the annotated-tag dereference; runaway-job and stale-run exposure bounded by timeouts/concurrency; checkout token persistence removed). The T2 self-modification caution for control-gates.yml is honored by mechanical-only scope, the R-STRESS-002 from-main wall copy checking this very PR, and the Opus 5 exact-head review. The .gitignore-violating tracked bytecode of check_forbidden_scope is removed (H7A-3 scan classification, routed here).

## Validation Evidence

Local checker battery at head via event payload: check_phase_authorization PASS (mode=bootstrap, PA-0025, closed_records=[PA-0023], changed_paths=12 including the delete); all other checkers PASS. Continuity suite 348/348 OK (fixture-based, per the recorded caveat). Digest quoted in the PR body recomputed at the PR head. SHA resolutions captured live with the annotated-tag dereference recorded.

## Risk Register Impact

Reviewed, no update required — no risk accepted, closed, or changed; the hardening closes inventory gaps, not register rows; R-DEP-SEC-001 next revisit remains H7A closeout.

## Decision Log Impact

H7A-4 entry appended: resumption basis, scope choice (readme fix excluded per owner word), pin resolutions, control-gates caution, first delete-rule use.

## Artifact Index Impact

Reviewed, no update required — no files under artifacts/ changed.

## PR Template / CODEOWNERS Implemented

No CODEOWNERS or PR-template change (CODEOWNERS is PA-forbidden here; its catch-all covers all touched paths).

## Red-Team Status

Per owner Decision 4: Opus 5, read-only, exact-head review with the full attestation including TECHNICALLY_ENFORCED_READ_ONLY=NOT_PROVEN. This PR touches the control-gates workflow itself, so the review's byte-level verification that gate logic is unchanged is the load-bearing check. Stale on any head change.

## Human Approval Status

Required. MERGE_AUTHORITY=OWNER_ONLY; owner review and key-turn merge required. Approver principals per PA-0025.

## Auto-Merge Status

Not eligible. Auto-merge remains prohibited.

## Forbidden Scope Confirmation

- [x] CI hardening configuration and records only. PA-0025 forbids `apps/**`, `policy/**`, `content/**`, `docs/archive/**`, CODEOWNERS, dependabot.yml, dependency-review.yml, and ALL control/continuity script sources (`scripts/control/*.py`, `scripts/continuity/**`); the 12-path diff touches none of them — the sole scripts/ path is the exact-ruled bytecode DELETE, not a source change. No gate logic, dependency, build, backend, product, or content scope.

Forbidden scope confirmation: confirmed.

## Claim Level

CI hardening configuration only. Workflow parse validity is proven locally; runtime behavior is proven by this PR's own CI runs (each hardened workflow executes on this PR — the strongest available evidence). No gate logic changed; if any check behaves differently at this head beyond cancellation semantics, that is a defect, not an intended change. H7A-5 remains unstarted and unclaimed.

## Known Limitations

1. SHA pins freeze action code until a future authorized re-pin; Dependabot's github-actions ecosystem (H7A-3) surfaces new releases as advisory signals — the re-pin cadence is an H7A-5 closeout note. 2. Concurrency cancellation on rapid successive events is disclosed in the evidence file. 3. The routed apps/web/README.md fix remains open (owner scope choice), candidate for H7A-5. 4. The H7A-1 inventory document itself still shows the pre-hardening baseline (AH-class dated record per the RECON-2 review's non-blocking observation; the evidence file carries the after-state).

## Next Phase Status

On merge + verified main: H7A-5 closeout is the final H7A deliverable (consolidated evidence, NIST SSDF mapping, SLSA gap assessment, RT-H0 finding-version updates under owner authority, dependency-review required-context owner decision, R-DEP-SEC-001 revisit, Dependabot first-run evidence, routed readme fix if the owner extends scope). On H7A-5's merge, #137 and #65 close. H7B (#66) requires its own intake. AUTOMATIC_CONTINUATION=NO.
