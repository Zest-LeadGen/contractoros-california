# Read-Only Red-Team Continuity Collector

`red_team_continuity.py` collects bounded public-safe continuity evidence and writes a deterministic derived startup packet. The packet is not authoritative, grants no write decision power, and must be revalidated against live GitHub evidence.

The implementation uses only the Python standard library. It has no network library, dependency declaration, package installation, or lockfile impact.

## Fixture mode

```text
python3 scripts/continuity/red_team_continuity.py fixture \
  --fixture scripts/continuity/tests/fixtures/consistent_closed_gate.json \
  --observed-at 2026-07-13T00:00:00Z \
  --output-dir /tmp/contractoros-continuity-fixture
```

## Live mode

```text
python3 scripts/continuity/red_team_continuity.py live \
  --repo-root <repository-root> \
  --repository Zest-LeadGen/contractoros-california \
  --issue-number 49 \
  --pr-number 50 \
  --run-id <actions-run-id> \
  --canonical-ref <exact-40-character-git-sha> \
  --observed-at <rfc3339-timestamp> \
  --output-dir <outside-repository-directory>
```

Every option is explicit. This correction packet bounds live collection to repository `Zest-LeadGen/contractoros-california`, Issue #49, and PR #50. The requested root must strictly equal Git's top level and contain a valid `.git` directory or worktree control file. Origin is accepted only in the four permitted HTTPS/SSH GitHub forms and is stored only as public-safe normalized identity evidence. `--canonical-ref` must be an exact lowercase SHA. `--observed-at` must be RFC3339. `--output-dir` must resolve outside the repository.

## Generated files

The supplied external output directory receives exactly:

- `continuity-evidence.json`
- `RED_TEAM_STARTUP_PACKET.md`

Both files use UTF-8, LF line endings, stable ordering, no trailing whitespace, and one final newline. A live packet must not be committed.

The packet hash is SHA-256 over the canonical rendered packet payload before the displayed `Packet Hash` heading and value are appended. The evidence manifest records this rule.

## Runtime command boundary

Commands use argument arrays, `shell=False`, finite timeouts, captured output, and normalized return-code evidence. The positive allowlist permits only:

- `git remote get-url origin`
- `git rev-parse HEAD`
- `git rev-parse main`
- `git rev-parse origin/main`
- `git rev-parse --show-toplevel`
- `git status --porcelain=v1 --branch`
- `git show <exact-sha>:docs/project-control/state/contractoros-state.yaml`
- one exact repository GraphQL query for `nameWithOwner` and `defaultBranchRef { name target { oid } }`
- narrowly shaped `gh issue view`, `gh pr view`, `gh pr checks`, and `gh run view` JSON reads
- `gh api --method GET repos/Zest-LeadGen/contractoros-california/pulls/50/reviews?per_page=100&page=<1-5>`
- `gh api --method GET repos/Zest-LeadGen/contractoros-california/collaborators/<sourced-reviewer>/permission`

The runtime rejects unknown executables, subcommands, flags, and shapes. The GraphQL allowlist admits only the fixed repository query above and no mutation or caller-supplied field. Review pages are sequential, fixed at 100 records, stop on the first short page, and are limited to five pages. A full fifth page marks review evidence truncated and blocked. Permission reads are limited to normalized exact-head submitted human approval candidates, with at most 100 candidates. Command output is size-bounded. `git fetch`, `git pull`, `git push`, `git commit`, `git merge`, `git reset`, `git clean`, `git checkout`, and `git switch` are forbidden runtime commands. Every other `gh api` shape and all issue, pull-request, review, approval, merge, or closeout mutations are forbidden runtime commands.

## Classification and exit contract

- `consistent`: exit `0`
- valid `requires_live_verification`: exit `0`
- `stale`: exit `2`
- `quarantined`: exit `2`
- `blocked`: exit `3`
- unsafe/private evidence or a prohibited output path: exit `4`
- invalid arguments, forbidden command shapes, malformed fixture input, malformed canonical state, or schema failure: exit `5`

Missing external red-team evidence and human approval are pending blockers for a valid active developer PR. They do not cause false approval and do not grant merge permission. A moved head, stale approval marker, contradictory lifecycle, active auto-merge, or unsupported approval/readiness claim is quarantined. Inaccessible required evidence is blocked.

## Output and sensitive-data boundary

Before creating anything, the collector strictly resolves the nearest existing output ancestor, projects any nonexistent suffix, and rejects the repository root, prospective repository descendants, symlinks into the repository, an output-directory symlink, output-file symlinks, and non-regular targets. Only a passing external destination is created. It repeats the boundary check after creation and performs safe atomic replacement with temporary-file cleanup.

Unsafe/private-looking input is rejected. Forbidden categories include token forms, bearer values, API-key or secret assignments, cloud credential identifiers, passwords, private keys, authorization headers, local absolute home paths, private customer information, and confidential owner, legal, vendor, or budget material. Sanitization never converts unsafe material into decision power. A public-safe opaque identifier or content hash may be used only when the governed source permits it.

Raw chat input cannot become decision power. The collector reads canonical state as a versioned observed snapshot and requires live evidence for changing lifecycle facts.

## Approval evidence contract

Only normalized public-safe review fields are retained: review ID, reviewer login and account type, state, submission time, exact commit ID, and author association. Review bodies are never persisted. Permission evidence retains only reviewer login, calculated base permission, role name, and account type. These fields are scope-bound approval evidence.

For each reviewer, decisive current-head records are sorted by validated RFC3339 submission timestamp and numeric review ID. A live submission timestamp must be null or RFC3339; decisive `APPROVED`, `CHANGES_REQUESTED`, and `DISMISSED` records require a valid non-null timestamp. Malformed live timestamp evidence blocks with exit `3`; malformed fixture timestamp evidence returns exit `5` before candidate selection. The latest `APPROVED`, `CHANGES_REQUESTED`, or `DISMISSED` state governs; a later `COMMENTED` record does not erase approval. Duplicate IDs, conflicting duplicates, malformed commit IDs, identity mismatches, or a coarse approved decision without a qualifying reviewer are quarantined. Missing or truncated approval evidence is blocked.

A reviewer qualifies only with a submitted exact-current-head approval, account type `User`, separation from the PR author, and calculated base permission `write` or `admin`. GitHub maps maintain access to base permission `write`. Read, none, unknown, bot, PR-author, stale, dismissed, superseded, unsubmitted, inaccessible, or association-only evidence does not qualify. External red-team evidence and human approval remain separate requirements.

Permission-command rejection remains invalid-command exit `5`, unsafe evidence remains exit `4`, and genuinely unavailable permission evidence maps to exit `3`. A permission response must contain the requested candidate's valid scope-bound identity under the shared case-folded canonical rule, a supported account type, an allowed calculated permission, and a bounded role name before any normalized record is created. A different, missing, or malformed response identity blocks and cannot become approval evidence.

## Workflow provenance contract

Fixture, evidence, startup-packet, and generator versions are `1.3.5`. Live collection captures public-safe normalized worktree-status hashes before and after all authoritative reads; both must be clean and identical. Active, externally-approved, and merge-ready claims require the collected local HEAD to equal the PR head, default branch and PR base to be `main`, and run SHA/branch to equal the PR; differences quarantine. Closed-gate claims additionally bind the PR base to the verified default branch, require local HEAD, local main, and merge commit to equal verified live main, and retain the pre-merge PR head as a separate value. Required live PR keys remain present even when nullable: `mergeCommit`, `mergedAt`, `autoMergeRequest`, and `reviewDecision`; an empty auto-merge mapping is active because only `null` means inactive. Completed live runs, jobs, and steps require a nonempty conclusion, while pending items may use null. A non-null Issue `closedAt` must be RFC3339. Missing or malformed authoritative values block with exit `3`.

Before approval evaluation, comparison, rendering, or output creation, the `1.3.5` runtime contract validates exact repository, issue, pull-request, check, workflow-run, job, step, marker, auto-merge, full normalized-review, and optional source-command shapes with bounded list sizes and no unknown nested properties. Decisive reviews sort by parsed UTC instant, numeric review ID, then deterministic record content. Canonical schema version and lifecycle state are nonempty strings, and canonical consistency status is a supported classification compared against the active or closed lifecycle family. Malformed fixture/evidence input returns exit `5` without a traceback; unavailable or malformed authoritative live responses remain exit `3`.

The governed job must contain one ordered copy of every step declared by `.github/workflows/control-gates.yml`. Before external review, only the exact completed matrix of successful pre-marker steps, a failed marker step with missing marker evidence, skipped post-marker steps, failed run/job, and failed linked PR check is valid pending evidence. After a valid exact-head marker, all governed steps, the job, run, and linked check must succeed. Missing jobs or steps are blocked; identity mismatches, duplicates, impossible ordering, and contradictory run/check/step states are quarantined. Pending or in-progress evidence cannot support approval or completed-gate claims.

## Tests

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s scripts/continuity/tests \
  -p 'test_*.py'
```

Tests cover determinism, packet hashing, lifecycle classifications, clean-and-unchanged worktree provenance, missing evidence, malformed input and nested canonical objects, authoritative live repository/default-branch and `closedAt` validation, command rejection and exception-class preservation, response-identity-bound permission validation, UTC review ordering, shell avoidance, output and symlink escape, sensitive-data rejection, moved-head handling, contradictory lifecycle evidence, active auto-merge, raw chat rejection, exact workflow provenance, the required step matrix, linked-check contradictions, bounded REST pagination, reviewer-state reduction, scope-bound author/bot rejection, calculated permission qualification, approval contradictions, review-body exclusion, and the exact two-file output boundary.

## C3.5 correction contract

Version `1.3.5` separates collected four-field review evidence (`decision`, `evidence_status`, `review_records`, and `permission_records`) from the seven-field evaluated normalized review. Nested collected records are validated before reduction. Fixture-derived approvals, disqualified identities, and reason maps must equal deterministic recomputation or quarantine; they cannot be silently discarded. Final reviewer identities are canonical-unique and disjoint, every disqualified reviewer has a nonempty supported reason list, and `_evidence` is reserved only for the documented evidence-wide malformed-record reason.

Live collection uses exactly `git status --porcelain=v1 --branch --untracked-files=all` before and after authoritative reads, plus exact public `HEAD` reads at both points. Both statuses must be clean and hash-identical, and the heads must agree. An `OPEN` live issue requires null `closedAt`; a `CLOSED` issue requires valid non-null RFC3339 `closedAt`. Normalized active evidence requires open closeout state and closed evidence requires closed closeout state. Malformed authoritative live evidence blocks with exit `3`; malformed fixture evidence returns exit `5` without a traceback.
