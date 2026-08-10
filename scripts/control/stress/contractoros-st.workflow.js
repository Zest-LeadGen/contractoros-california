export const meta = {
  name: 'full-tree-adversarial-stress',
  description: 'Seven adversarial auditors attack drift, provenance, gates, CI logic, tree, corpus, and the report itself',
  phases: [{ title: 'Adversarial sweep', detail: 'seven independent attackers, one dimension each' }],
}
phase('Adversarial sweep')
const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['dimension','probes_run','findings','summary'],
  properties: {
    dimension: {type:'string'},
    probes_run: {type:'integer'},
    findings: {type:'array', items: {type:'object', additionalProperties:false,
      required:['claim','verdict','severity','evidence'],
      properties:{
        claim:{type:'string'},
        verdict:{type:'string', enum:['GROUNDED','DRIFT','ASSUMPTION','HALLUCINATION','VIOLATION','GAP','REFUTED_CLAIM']},
        severity:{type:'string', enum:['critical','high','medium','low','info']},
        evidence:{type:'string'},
        detail:{type:'string'}}}},
    summary: {type:'string'}}}
const COMMON = `You are an ADVERSARIAL auditor for the ContractorOS program. Your job is to REFUTE, not confirm — default to suspicion; a claim is GROUNDED only if you personally verified it against a primary source (live GitHub via gh CLI [authenticated as collaborator danidon-wq — read-only; NEVER merge/close/edit/comment/switch accounts; NEVER run gh auth switch], local git in /Users/adnankhan/Documents/GitHub/contractoros-california and /Users/adnankhan/Documents/GitHub/contractoros-governance, or file contents you read). Anything you could not verify = ASSUMPTION. Anything contradicted by a primary source = DRIFT (stale) or HALLUCINATION (never true) or VIOLATION (authority act without owner record). GAP = a real weakness/bypass you found. Do NOT mutate anything: no commits, pushes, PR/issue writes, no file writes outside /tmp. KNOWN CONTEXT (verify, don't trust): PR #129 (post-H6-A reconciliation) is OPEN and unmerged — the committed snapshot on main intentionally lags it; that lag alone is documented, not a fresh finding, but verify the #129 branch content actually closes it. Report every finding, including ones that embarrass the operators. Return ONLY structured output.`
const AGENTS = [
 {k:'records-vs-live', p:`${COMMON}
Dimension: COMMITTED RECORDS vs LIVE GITHUB.
In /Users/adnankhan/Documents/GitHub/contractoros-california (run git fetch origin first, work from origin/main):
1) Read docs/project-control/state/contractoros-state.yaml at origin/main. Test EVERY checkable field against live gh reads: current_main_sha vs gh api repos/Zest-LeadGen/contractoros-california/commits/main; completed_prior_phase (issue #118 state, PR #125 merged, merge SHA); each evidence_identifiers entry (comment IDs exist + author via gh api, PR states, ruleset 20598456 via gh api).
2) Read the last 4 sections of docs/project-control/DECISION_LOG.md at origin/main; verify their factual claims (merge actors + timestamps via gh pr view N --json mergedBy,mergedAt for PRs 125-128; comment authorship for 5233703034 and 5235003178 via gh api repos/Zest-LeadGen/contractoros-california/issues/comments/ID).
3) Read the same snapshot at origin/post-h6a-reconciliation (PR #129 branch): does it correctly record main 396d4a3, lifecycle h6_in_progress, and the R-DEP-SEC-001 blocker? Verify the 3 Dependabot alerts it claims via gh api repos/Zest-LeadGen/contractoros-california/dependabot/alerts (state, severity, package, patched version).
Probe count = number of distinct field/claim checks. Be exhaustive.`},
 {k:'silence-as-yes', p:`${COMMON}
Dimension: PROVENANCE / SILENCE-AS-YES.
Enumerate EVERY authority-creating event in Zest-LeadGen/contractoros-california since 2026-08-09T00:00Z: all merged PRs (gh pr list --state merged --limit 40 --json number,mergedAt,mergedBy,reviews), all closed issues (gh issue list --state closed --limit 30 --json number,closedAt — especially #63), all authorization comments cited in docs (5233703034 [H5+H6, ARM_NOW], 5235003178 [H6]) — verify author association OWNER + timestamp via gh api repos/Zest-LeadGen/contractoros-california/issues/comments/ID.
For each merge #119..#129-era: does a Zest-LeadGen APPROVED review exist at the merged head SHA, and who merged? Any event whose authority traces only to session text or silence = VIOLATION. Also verify: the H5-D authorization chain claims every PA record cites an on-platform owner comment — spot-check PA-0009..PA-0012 evidence_id comments exist and are owner-authored. Is issue #118 still OPEN (it should be — H6-B pending)? Was closing #63 backed by delivered work (H5 PRs merged)?`},
 {k:'gate-bypass', p:`${COMMON}
Dimension: CONTROL-GATE BYPASS PROBES.
Work in a detached worktree: git -C /Users/adnankhan/Documents/GitHub/contractoros-california worktree add /tmp/stress-main origin/main, cd /tmp/stress-main, and git -C /Users/adnankhan/Documents/GitHub/contractoros-california worktree remove /tmp/stress-main --force when done.
1) Run existing suites: PYTHONDONTWRITEBYTECODE=1 python3 scripts/control/tests/test_phase_authorization.py and PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/continuity/tests -p 'test_*.py'. Record pass/fail counts.
2) CONFIRM THE WALL IS ARMED: read .github/workflows/control-gates.yml — phase-authorization job must have NO continue-on-error, appear in the aggregate needs list, and be required-success on pull_request in the aggregate shell logic. Any regression = critical GAP.
3) Craft >=7 FRESH adversarial PR-context JSONs in /tmp (GITHUB_EVENT_PATH format, env GITHUB_EVENT_NAME=pull_request GITHUB_BASE_REF=main) that SHOULD be rejected, and verify each checker rejects: (a) PR linking #118 touching apps/web/src/anything -> check_phase_authorization (PA-0012 forbids apps/**) AND check_changed_files; (b) missing OWNER_TRIGGER_REVIEW marker -> check_owner_trigger_review; (c) RED_TEAM_DECISION bound to WRONG head SHA -> check_red_team_marker; (d) overclaim 'complete with no open blockers' -> check_pr_contract --claims-only (R-STRESS-004 fix); (e) PR linking #118 that ADDS a second bootstrap PA record while PA-0012 lives at base without closing it -> check_phase_authorization BOOTSTRAP_CLOSURE_REQUIRED; (f) bootstrap record with off-platform evidence_id 'chat-approval-1' -> BOOTSTRAP_EVIDENCE_FORMAT; (g) content-drifted rename (R<100) -> RELOCATE_CONTENT_DRIFT_DENIED (build a tiny scratch git repo if easier for rename probes, or verify via the unit suite's coverage and say so).
ANY probe that passes when it should fail = GAP (severity high/critical). Report exact commands + outcomes.`},
 {k:'ci-logic', p:`${COMMON}
Dimension: CI WORKFLOW LOGIC HOLES.
Read .github/workflows/control-gates.yml, web-ci.yml, codeql.yml at origin/main in /Users/adnankhan/Documents/GitHub/contractoros-california. Hunt adversarially:
1) Aggregate job: needs list complete vs all defined jobs (phase-authorization now ARMED and required — verify); result-mapping: can a 'skipped' or 'cancelled' core job slip through as pass on pull_request events? Trace the shell logic literally, including the push-branch case.
2) Event triggers: pull_request types — 'edited' present (marker edits must re-run)? Any workflow_dispatch/pull_request_target bypass? web-ci path filters: could a mobile-lockfile-only PR skip web-ci while claiming CI coverage?
3) Permissions: any write permission abusable from a PR branch? Does check_red_team_marker read the body from the event payload (spoofable by the PR author editing the body? that is by design owner-reviewed — assess honestly) vs API?
4) Required-check coupling: gh api repos/Zest-LeadGen/contractoros-california/rulesets/20598456 — required context vs aggregate job name; would renaming silently drop enforcement? Also self-referential risk: a PR can still edit control-gates.yml + checkers (R-STRESS-002, tracked to H6-B) — verify that is honestly recorded, not silently fixed-claimed.
5) Race: dismiss_stale_reviews / require_last_push_approval config vs a post-approval push.
Each real hole = GAP with severity; each verified-solid mechanism = GROUNDED finding.`},
 {k:'tree-integrity', p:`${COMMON}
Dimension: FULL LOCAL TREE INTEGRITY.
1) /Users/adnankhan/Documents/GitHub/contractoros-california: git fetch; git status --porcelain on the MAIN checkout (dirty?); git branch -vv (stale locals vs origin; branches merged-but-undeleted); local main == origin/main? git worktree list — enumerate worktrees; an ACTIVE session worktree (.claude/worktrees/h5d-authorization-bootstrap-arming) is expected, but flag any OTHER stale worktree. Untracked junk scan.
2) /Users/adnankhan/Documents/GitHub/contractoros-governance: same checks incl. git worktree list (an h5d-schema-1-1-0 worktree may remain from the merged schema PR — if its branch is merged, flag as cleanup-due); HEAD vs git ls-remote origin main.
3) Inventory /Users/adnankhan/Documents/ContractorOS-Support/: Rescue folder scripts — any re-runnable one-time act dangerous today (check the superseded/ refusal-guards actually refuse: run one with bash and confirm exit 2 WITHOUT it doing anything); Archive clones — push URLs still disabled (git -C <clone> remote -v shows DISABLED_NON_CANONICAL_CLONE)?
4) Scan /Users/adnankhan/Documents (maxdepth 2) for OTHER ContractorOS copies mistakable for canonical.
5) gh auth status — active account must be danidon-wq; two accounts on one keyring is a known accepted waiver (H2-WAIVER-001) — verify its disclosure exists in the principal matrix or decision log rather than re-flagging it as new.
Stale/dangerous leftovers = DRIFT or GAP with specifics.`},
 {k:'governance-corpus', p:`${COMMON}
Dimension: GOVERNANCE CORPUS VERIFICATION.
In /Users/adnankhan/Documents/GitHub/contractoros-governance (git fetch origin; expect HEAD==origin/main==56eaef95d3d95dc946c065cd6047c15a91f72fc0 after schema PR #9 — report drift from that expectation either way, and verify the local main checkout is not behind):
1) Read policy/corpus/governing-files.json at origin/main. Verify: corpus_version (expect 1.7.0 after PR #9 — confirm), entry count vs expected_entry_count field, and the phase-authorization schema entry's lineage note mentions 1.1.0. For ANY entry carrying a digest/sha field: recompute (shasum -a 256) and compare — mismatch = critical DRIFT.
2) Validate schemas/authorization/phase-authorization.schema.json at origin/main: valid JSON; schema_version enum [1.0.0,1.1.0]; change_kinds enum includes delete+relocate; 'to' field present. Then validate ALL product PA records (docs/project-control/authorizations/PA-0001..PA-0012.json at origin/main of the product repo, PLUS PA-0012 at origin/post-h6a-reconciliation) against it using /Users/adnankhan/.claude/jobs/a6a58a40/tmp/gvenv/bin/python3 (has jsonschema 4.26.0). Every record must also validate the single-live-record invariant: exactly one non-revoked record per issue at product origin/main.
3) Run the governance validators with that same python: scripts/validate_corpus.py, scripts/scan_tree.py, tests/adversarial/probes.py — record results.
4) Check H2-WAIVER-001 compensating controls against reality where checkable (ruleset 20598456 active via gh api; hourly auditor routine referenced in DECISION_LOG).`},
 {k:'report-honesty', p:`${COMMON}
Dimension: HONESTY AUDIT OF THE OPERATOR'S OWN LATEST RECORDS.
Two targets, current content only:
1) WebFetch https://claude.ai/code/artifact/9610e33c-3a75-4a41-af26-fc8ff31faf4e — read its edition label and EVERY headline number/claim as they appear NOW. For each numeric claim the CURRENT edition makes, recount from primary sources (git log --first-parent origin/main --merges; gh pr list --state merged --json number,mergedBy; gh api commits/main; gh api rulesets). A claim already corrected in the current edition is not a live finding. If the artifact is unreachable, say so as ASSUMPTION and move to target 2 — do not guess its contents.
2) The newest phase reports on the #129 branch and origin/main (phase_h6a_toolchain_report.md, phase_h6a_dependency_pins_report.md, phase_post_h6a_reconciliation_report.md, docs/project-control/evidence/H6A_TOOLCHAIN_EVIDENCE.md): refute their claims — lockfile sha256 digests (recompute against origin/main files), '25/25' and '348/348' test counts (rerun the suites), 'byte-identical re-resolution' (cannot re-run network resolution deterministically now — classify honestly if unverifiable), 'all 12 checks green' style claims vs gh pr checks history, the five-failure-test claims incl. the DISCLOSED npm-ci/latest gap (verify the disclosure is present, and spot-verify the npm-ci-accepts-latest behavior in /tmp with a copy of the manifest+lockfile if npm is available).
Hunt for spin: any headline glossing a correction the body makes; any 'delivered' phrased as merged-and-verified before the owner key-turn. Wrong current number = HALLUCINATION/DRIFT with the correct value.`},
]
const results = await parallel(AGENTS.map(a => () =>
  agent(a.p, {label: `attack:${a.k}`, schema: SCHEMA})))
const out = {}
AGENTS.forEach((a,i) => { out[a.k] = results[i] })
const all = results.filter(Boolean).flatMap(r => r.findings)
log(`probes: ${results.filter(Boolean).reduce((s,r)=>s+r.probes_run,0)}, findings: ${all.length} (critical/high: ${all.filter(f=>['critical','high'].includes(f.severity)).length})`)
return out
