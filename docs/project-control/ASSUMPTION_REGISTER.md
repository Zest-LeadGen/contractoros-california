# Assumption Register

Purpose: record assumptions that affect ContractorOS California control, delivery, or review.

## Active Assumptions

| ID | Assumption | Evidence | Risk if wrong | Control | Status |
|---|---|---|---|---|---|
| ASM-4J0-001 | GitHub `origin/main` at `41835c3d361cce07b77f3708381a54d3a87a6e1f` is the starting source-of-truth SHA for Phase 4J-0. | `git fetch origin main` for documentation source sync, then branch creation from `origin/main`. | Branch could miss newer governance changes. | PR base is `main`; red-team verifies base/head before merge. | Active |
| ASM-4J0-002 | "Work locally only" means local implementation work, while GitHub PR creation is still required by the phase prompt. | Prompt says "Work locally only" and also requires opening a PR into `main`. | Remote PR evidence could be delayed if direct GitHub CLI is unavailable. | If direct PR tooling fails, stop and report the limitation. | Active |
| ASM-4J0-003 | No `AGENTS.md` existed on `origin/main` before Phase 4J-0. | `git ls-tree` / working tree inspection showed no `AGENTS.md` on the starting SHA. | Codex is creating operating rules before the repo-level Codex file exists. | Bootstrap exception, strict allowlist, no merge, red-team review, human/write-access approval. | Active |
| ASM-4J0-004 | The developer connector implementation path is blocked after repeated `api_tool.list_resources` violations. | Phase 4J-0 prompt records two prior failures before implementation. | Retrying the same path could repeat prohibited calls. | Use strict direct Codex execution for Phase 4J-0 only; future use requires updated control evidence. | Active |
| ASM-4J0-005 | Existing control-gate scripts remain the available local validation path for this documentation PR. | Scripts exist under `scripts/control/` on `origin/main`. | New governance docs may need future gate expansion. | Record validation tasks and known limits; red-team verifies after PR opens. | Active |

## Register Rule

Assumptions must remain versioned here until confirmed, replaced by a design decision, or closed by evidence.
