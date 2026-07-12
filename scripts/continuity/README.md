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
  --issue-number <issue-number> \
  --pr-number <pull-request-number> \
  --run-id <actions-run-id> \
  --canonical-ref <exact-40-character-git-sha> \
  --observed-at <rfc3339-timestamp> \
  --output-dir <outside-repository-directory>
```

Every option is explicit. `--canonical-ref` must be an exact lowercase SHA. `--observed-at` must be RFC3339. `--output-dir` must resolve outside the repository.

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
- narrowly shaped `gh repo view`, `gh issue view`, `gh pr view`, `gh pr checks`, and `gh run view` JSON reads

The runtime rejects unknown executables, subcommands, flags, and shapes. `git fetch`, `git pull`, `git push`, `git commit`, `git merge`, `git reset`, `git clean`, `git checkout`, and `git switch` are forbidden runtime commands. `gh api` and all issue, pull-request, review, approval, merge, or closeout mutations are forbidden runtime commands.

## Classification and exit contract

- `consistent`: exit `0`
- valid `requires_live_verification`: exit `0`
- `stale`: exit `2`
- `quarantined`: exit `2`
- `blocked`: exit `3`
- unsafe/private evidence or a prohibited output path: exit `4`
- invalid arguments, malformed input, malformed canonical state, or schema failure: exit `5`

Missing external red-team evidence and human approval are pending blockers for a valid active developer PR. They do not cause false approval and do not grant merge permission. A moved head, stale approval marker, contradictory lifecycle, active auto-merge, or unsupported approval/readiness claim is quarantined. Inaccessible required evidence is blocked.

## Output and sensitive-data boundary

The collector rejects the repository root, repository descendants, symlinks into the repository, and output-file symlinks. It performs safe atomic replacement inside the approved external directory.

Unsafe/private-looking input is rejected. Forbidden categories include token forms, bearer values, API-key or secret assignments, cloud credential identifiers, passwords, private keys, authorization headers, local absolute home paths, private customer information, and confidential owner, legal, vendor, or budget material. Sanitization never converts unsafe material into decision power. A public-safe opaque identifier or content hash may be used only when the governed source permits it.

Raw chat input cannot become decision power. The collector reads canonical state as a versioned observed snapshot and requires live evidence for changing lifecycle facts.

## Tests

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s scripts/continuity/tests \
  -p 'test_*.py'
```

Tests cover determinism, packet hashing, lifecycle classifications, missing evidence, malformed input, command rejection, shell avoidance, output and symlink escape, sensitive-data rejection, moved-head handling, contradictory lifecycle evidence, active auto-merge, raw chat rejection, and the exact two-file output boundary.
