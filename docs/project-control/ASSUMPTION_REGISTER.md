# Assumption Register

Purpose: record assumptions that affect ContractorOS California control, delivery, or review.

## Historical Phase 4J-0 Assumptions

Documentation scope: the status cells in this first table record their original Phase 4J-0 state. Starting SHAs, missing-file observations, initial tool availability, initial authentication, PR #15 correction state, and bootstrap-path assumptions are historical or closed by later GitHub evidence. They are not current H1 assumptions and cannot authorize work.

| ID | Assumption | Evidence | Risk if wrong | Control | Status |
|---|---|---|---|---|---|
| ASM-4J0-001 | GitHub `origin/main` at `41835c3d361cce07b77f3708381a54d3a87a6e1f` is the starting source-of-truth SHA for Phase 4J-0. | `git fetch origin main` for documentation source sync, then branch creation from `origin/main`. | Branch could miss newer governance changes. | PR base is `main`; red-team verifies base/head before merge. | Active |
| ASM-4J0-002 | "Work locally only" means local implementation work, while GitHub PR creation is still required by the phase prompt. | Prompt says "Work locally only" and also requires opening a PR into `main`. | Remote PR evidence could be delayed if direct GitHub CLI is unavailable. | If direct PR tooling fails, stop and report the limitation. | Active |
| ASM-4J0-003 | No `AGENTS.md` existed on `origin/main` before Phase 4J-0. | `git ls-tree` / working tree inspection showed no `AGENTS.md` on the starting SHA. | Codex is creating operating rules before the repo-level Codex file exists. | Bootstrap exception, strict allowlist, no merge, red-team review, human/write-access approval. | Active |
| ASM-4J0-004 | The developer connector implementation path is blocked after repeated `api_tool.list_resources` violations. | Phase 4J-0 prompt records two prior failures before implementation. | Retrying the same path could repeat prohibited calls. | Use strict direct Codex execution for Phase 4J-0 only; future use requires updated control evidence. | Active |
| ASM-4J0-005 | Existing control-gate scripts remain the available local validation path for this documentation PR. | Scripts exist under `scripts/control/` on `origin/main`. | New governance docs may need future gate expansion. | Record validation tasks and known limits; red-team verifies after PR opens. | Active |
| ASM-4J0-006 | Local GitHub authentication was initially unavailable for the documentation PR push. | Initial `git push --no-verify -u origin phase-4j-0-codex-operating-model` failed with username/device configuration error; owner later completed GitHub CLI authentication for documentation PR setup. | Final correction could be assumed pushed before it is actually in GitHub. | Treat initial condition as mitigated; final resolution still requires corrected push, PR body update, workflow, review, approval, merge, and post-merge verification. | Mitigated after owner setup / final resolution pending |
| ASM-4J0-007 | The Phase 4J-0 branch was initially local-only after the correction commit. | Initial PR branch was later pushed to GitHub by owner; PR #15 initial GitHub head SHA was `9427c667e992af1134b80f82a3cb1aef33458be6`; local correction head before this final correction was `459f8173f9152e02d9710de98dbce3ccebfe30d2`. | The corrected local head could differ from the current GitHub PR head until pushed. | Verify branch exists on GitHub again after the final correction push. | Mitigated for initial branch push / final correction pending |
| ASM-4J0-008 | `gh` was initially not installed. | `gh auth status` initially failed with command not found; owner installed GitHub CLI 2.96.0 and completed GitHub CLI authentication for documentation PR setup as Zest-LeadGen. | PR state could be misreported from stale local assumptions. | Record owner setup and verify PR #15 body after the final correction is applied. | Mitigated after owner setup / final PR body update pending |
| ASM-4J0-009 | Owner wants future 95% automation with owner interruption only for major, legal, financial, or scope decisions. | Correction prompt requires lane-based future policy and owner-interruption triggers. | Future automation could be too manual or too permissive if not versioned. | Keep current owner approval mandatory; future phases must implement safeguards before reducing manual approval. | Active |
| ASM-4J0-010 | PR #15 now exists. | Owner created `https://github.com/Zest-LeadGen/contractoros-california/pull/15` after GitHub CLI setup. | Red-team could review stale PR evidence if the corrected report is not pushed and the PR body is not updated. | Final correction must be pushed and PR body updated before red-team approval. | Active / correction pending |
| ASM-4J0-011 | "Extra High" is a UI-observed label and official config value is `xhigh` unless later official UI docs prove otherwise. | Owner prompt records the UI label caveat and the official Codex Config Reference value. | Repo policy could overclaim a UI mapping. | Cite official config value `xhigh` and avoid claiming official UI mapping. | Active |

## Register Rule

Assumptions must remain versioned here until confirmed, replaced by a design decision, or closed by evidence.

## Current H1 Recovery Assumptions And Unknowns

| ID | Assumption or unknown | Evidence | Control | Status |
|---|---|---|---|---|
| ASM-H1-001 | External archive provider and location are not durably selected. | Issue #58 comment `4975617497`. | Record no provider, folder, URL, or Drive ID until later verified owner authority exists. | Open unknown. |
| ASM-H1-002 | Mac-local artifacts outside the recovery inventory are inaccessible in this packet. | Issue #58 recovery inventory. | Classify as `NOT_ACCESSIBLE`; do not infer bytes, hashes, contents, or acceptance. | Open unknown. |
| ASM-H1-003 | The nine H1 engineering decisions listed in the risk register are unresolved. | Issue #58 comment `4975617497`. | Keep them as requirements/risks; do not convert them into implementation facts. | Open unknown. |
| ASM-H1-004 | Exact future minimal inert bootstrap bytes, actor, mechanism, mutation window, rollback point, and protections are undecided. | D29 and Issue #58 recovery authority. | Require a later separate owner decision packet and exact authorization. | Open unknown. |
| ASM-H1-005 | Local artifact byte sizes are unproven where Issue #58 records only filenames and hashes. | Recovery authority inventory; documentation scope only. | Artifact index records `NOT_PROVEN` size rather than inferring it. | Open unknown. |

Verified owner decisions D27-D32 are decisions, not assumptions.

## Pre-4K-9 Assumptions

| ID | Assumption | Evidence | Risk if wrong | Control | Status |
|---|---|---|---|---|---|
| ASM-PRE4K9-001 | Issue #47 owner amendment is the public-safe representation of the signed D1–D26 source. | Issue comment `4949071184`; private originals were not accessed or committed. | A private condition may be omitted. | Owner and external red-team review the register; later corrections use explicit supersession. | Active |
| ASM-PRE4K9-002 | No current official source was retrieved to verify GPT-5.6 Sol, Terra, or Luna as official taxonomy. | This gate used only UI-observed labels and repository evidence. | Permanent policy could record unstable naming. | Leave `PROMPT_CONVENTION.md` unchanged and require official-source refresh later. | Active |
| ASM-PRE4K9-003 | A committed snapshot cannot prove the live head SHA of the PR that contains it. | PR #48 exists and every correction commit changes its head after file content is fixed. | Static state could falsely present stale review evidence as current. | Live GitHub evidence controls; the snapshot records PR #48 without a static observed head and uses `requires_live_verification` while lifecycle evidence changes. | Active limitation / prior null-PR assumption superseded |
