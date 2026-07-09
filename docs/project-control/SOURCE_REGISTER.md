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
| SRC-4J0-006 | OpenAI Codex Models docs | Official OpenAI documentation named by owner prompt | Codex model selection, recommended Codex models, deprecated Codex model warning | Owner-provided official-source basis; direct official URL not added in this correction | Used for `PROMPT_CONVENTION.md` model policy. |
| SRC-4J0-007 | OpenAI Codex Config Reference | Official OpenAI documentation named by owner prompt | `model_reasoning_effort` values and `xhigh` config value | Owner-provided official-source basis; direct official URL not added in this correction | Used for effort-value policy and UI label caveat. |
| SRC-4J0-008 | OpenAI GPT-5.5 guidance / latest model guide | Official OpenAI documentation named by owner prompt | GPT-5.5 effort guidance and higher-effort caveat | Owner-provided official-source basis; direct official URL not added in this correction | Used for effort-selection policy. |
| SRC-4J1-001 | Phase 4J-1 owner prompt | Owner/project phase instruction | GitHub issue intake objective, file allowlist, required controls, validation commands, and prohibitions | Current turn prompt | Durable implementation evidence captured in Phase 4J-1 files and report. |
| SRC-4J1-002 | `main` at `0f04efa564c4f28bd351881c00f72d41f540c319` | Repository source | Starting SHA for Phase 4J-1 | Verified locally before branch creation | GitHub remains source of truth. |
| SRC-4J1-003 | Existing `.github/pull_request_template.md`, `.github/workflows/control-gates.yml`, and `scripts/control/check_pr_contract.py` | Repository source | Local control-gate integration pattern | Read locally before editing | Used to add linked-issue enforcement without removing existing gates. |
| SRC-4J1-004 | GitHub issue #16 | GitHub issue source | Durable issue intake for Phase 4J-1 | Owner provided issue number and URL | Phase issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/16 |
| SRC-4J2-001 | Phase 4J-2 owner prompt | Owner/project phase instruction | SHA-bound red-team marker objective, file allowlist, required fields, validation commands, and prohibitions | Current turn prompt | Durable implementation evidence captured in Phase 4J-2 files and report. |
| SRC-4J2-002 | `main` at `a3d8e88f11200b01b0f1ef54960d1a39938b78db` | Repository source | Starting SHA for Phase 4J-2 | Verified locally before branch creation | GitHub remains source of truth. |
| SRC-4J2-003 | GitHub issue #18 | GitHub issue source | Durable issue intake for Phase 4J-2 | Owner provided issue number and URL | Phase issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/18 |
| SRC-4J2-004 | Existing `.github/pull_request_template.md`, `scripts/control/check_pr_contract.py`, and project-control docs | Repository source | Control-gate integration and report-contract style | Read locally before editing | Used to add marker validation without weakening existing gates. |
| SRC-4J3-001 | Phase 4J-3 owner prompt | Owner/project phase instruction | Mandatory red-team marker enforcement objective, issue #20, file allowlist, validation commands, and prohibitions | Current turn prompt | Durable implementation evidence captured in Phase 4J-3 files and report. |
| SRC-4J3-002 | `main` at `cfe01c7e381b3d2c0f26f0dba187d0a030368219` | Repository source | Starting SHA for Phase 4J-3 | Verified locally before branch creation | GitHub remains source of truth. |
| SRC-4J3-003 | GitHub issue #20 | GitHub issue source | Durable issue intake for Phase 4J-3 | Owner provided issue number and URL | Phase issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/20 |
| SRC-4J3-004 | Existing `.github/workflows/control-gates.yml`, `.github/pull_request_template.md`, `scripts/control/check_red_team_marker.py`, and project-control docs | Repository source | Workflow integration, PR template instruction, validator behavior, and report-contract style | Read locally before editing | Used to activate mandatory marker enforcement without weakening existing gates or adding elevated permissions. |
| SRC-4J4-001 | Phase 4J-4 owner prompt | Owner/project phase instruction | Owner-trigger detection objective, issue #22, file allowlist, required marker fields, validation behavior, and prohibitions | Current turn prompt | Durable implementation evidence captured in Phase 4J-4 files and report. |
| SRC-4J4-002 | `main` at `21d5ecea173e13cfbb58fe6a69cce5cd5a07c413` | Repository source | Starting SHA for Phase 4J-4 | Verified locally before branch creation | GitHub remains source of truth. |
| SRC-4J4-003 | GitHub issue #22 | GitHub issue source | Durable issue intake for Phase 4J-4 | Owner provided issue number and URL | Phase issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/22 |
| SRC-4J4-004 | Existing `.github/workflows/control-gates.yml`, `.github/pull_request_template.md`, `scripts/control/check_red_team_marker.py`, `scripts/control/check_pr_contract.py`, and project-control docs | Repository source | Workflow integration, PR template instruction, validator style, report contract, and governance register update style | Read locally before editing | Used to add owner-trigger marker enforcement without weakening red-team enforcement or adding elevated permissions. |
| SRC-4J5-001 | GitHub issue #25 | GitHub issue source | Durable phase intake for Phase 4J-5 | Verified with direct GitHub API read during this run | Phase issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/25 |
| SRC-4J5-002 | GitHub issue #24 | GitHub issue source | Red-team handoff and memory reconciliation anchor | Verified with direct GitHub API read during this run | Issue URL: https://github.com/Zest-LeadGen/contractoros-california/issues/24 |
| SRC-4J5-003 | Issue #24 Red-Team Operating Protocol Addendum | GitHub issue comment source | Source-of-truth rule, evidence hierarchy, role boundary, required route, and durable memory-sync rule | Verified with direct GitHub API read during this run | Comment URL: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4923968200 |
| SRC-4J5-004 | Issue #24 CLI Expected Output Requirement | GitHub issue comment source | Command-output requirement for red-team terminal and GitHub CLI guidance | Verified with direct GitHub API read during this run | Comment URL: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4924223781 |
| SRC-4J5-005 | Issue #24 Progress Snapshot Requirement | GitHub issue comment source | Progress snapshot categories, baseline, and claim downgrade rule | Verified with direct GitHub API read during this run | Comment URL: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4924313115 |
| SRC-4J5-006 | Issue #24 Red-Team Operator State Machine Addendum | GitHub issue comment source | Lifecycle-state classification, sequencing, handoff, and no premature option-list behavior | Verified with direct GitHub API read during this run | Comment URL: https://github.com/Zest-LeadGen/contractoros-california/issues/24#issuecomment-4924596374 |
| SRC-4J5-007 | `main` / `origin/main` at `b01cd5829621c20f6bd837a9d570553a6a408573` | Repository source | Starting SHA for Phase 4J-5 | Verified locally before branch creation | GitHub remains source of truth. |

## Source Rules

External paid services, hosted bots, and unversioned connector memory are not sources for Phase 4J-0.

The UI label "Extra High" is recorded only as UI-observed terminology unless an official OpenAI UI source is added later.
