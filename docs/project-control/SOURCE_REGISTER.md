# Source Register

Purpose: record sources used for ContractorOS California control decisions.

## Sources

| Source ID | Source | Type | Used for | Verification status | Notes |
|---|---|---|---|---|---|
| SRC-4J0-001 | Phase 4J-0 bootstrap implementation prompt | Owner/project phase instruction | Scope, prohibitions, allowed files, required decisions, PR body evidence | Recorded in this PR context | Chat text is not source of truth after merge; durable requirements are captured in repo files. |
| SRC-4J0-002 | GitHub `origin/main` at `41835c3d361cce07b77f3708381a54d3a87a6e1f` | Repository source | Starting base SHA and existing control-document style | Retrieved before branch creation | GitHub remains source of truth. |
| SRC-4J0-003 | Existing docs under `docs/project-control/` on starting main | Repository source | Style, report contract, risk/decision/ledger conventions | Read locally after checkout | No product scope was derived from these docs. |
| SRC-4J0-004 | Existing scripts under `scripts/control/` on starting main | Repository source | Local validation task definitions | Read locally after checkout | Scripts were used for validation only. |
| SRC-4J0-005 | `AGENTS.md` created by Phase 4J-0 | Repository source after this PR | Future Codex operating rules | Pending red-team review and merge | Bootstrap-only creation before the file existed. |

## Source Rules

External paid services, hosted bots, and unversioned connector memory are not sources for Phase 4J-0.
