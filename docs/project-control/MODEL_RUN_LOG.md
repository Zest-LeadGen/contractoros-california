# Model Run Log

Purpose: record AI/developer-executor runs that affect ContractorOS California governance.

## Runs

| Run ID | Date | Executor | Scope | Inputs used | Commands / tools used | Prohibited calls | Output |
|---|---|---|---|---|---|---|---|
| MRL-4J0-001 | 2026-07-08 | Codex developer executor | Phase 4J-0 control/infrastructure documentation only | Phase prompt, `origin/main` at `41835c3d361cce07b77f3708381a54d3a87a6e1f`, existing project-control files, local control scripts, owner-provided true-state correction | Git remote setup, `git fetch origin main` for documentation source sync, branch creation, local file edits, local validation scripts, local commits, failed initial push attempt, unavailable initial `gh` check, owner GitHub CLI setup evidence | `/init`: not run; `api_tool.list_resources`: not called; broad discovery/list-resource/tool-schema calls: not called; cockroachdb hooks: not trusted | Initial local implementation and local commit succeeded. Initial push failed due missing HTTPS credential setup. `gh` was initially unavailable. Owner installed GitHub CLI 2.96.0, authenticated as Zest-LeadGen, pushed the branch, and created PR #15. Correction commit was required because the initial PR body/report did not distinguish successful, failed, unavailable, and owner-completed commands. Final correction must be pushed and PR body updated before red-team approval. |
| MRL-4J0-002 | 2026-07-08 | Codex developer executor | Phase 4J-0 prompt convention documentation/control only | Owner-approved prompt convention correction and existing Phase 4J-0 governance files | Local file edits, local validation scripts, local amend preparation | `/init`: not run; `api_tool.list_resources`: not called; broad discovery/list-resource/tool-schema calls: not called; cockroachdb hooks: not trusted | Phase 4J-0 added prompt convention requirement after owner approval. This update was documentation/control only. No product/app/dependency/build/backend/mobile/web scope was touched. |
| MRL-4J1-001 | 2026-07-08 | Codex developer executor | Phase 4J-1 GitHub issue intake control/infrastructure | Phase 4J-1 prompt, verified main SHA `0f04efa564c4f28bd351881c00f72d41f540c319`, existing control scripts/templates/docs | Local branch creation, template edits, control script edit, governance docs/report updates, local validation scripts | `/init`: not run; `api_tool.list_resources`: not called; broad discovery/list-resource/tool-schema calls: not called; cockroachdb hooks: not trusted | Added GitHub phase issue template, PR linked-issue requirement, PR contract enforcement, workflow step label update, and governance docs. No product/app/dependency/build/backend/mobile/web scope touched. |
| MRL-4J1-002 | 2026-07-08 | Codex developer executor | Phase 4J-1 linked issue finalization | Owner-provided issue #16 and Phase 4J-1 governance files | Local documentation updates, local validation scripts, commit, push, PR create pending | `/init`: not run; `api_tool.list_resources`: not called; broad discovery/list-resource/tool-schema calls: not called; cockroachdb hooks: not trusted | Owner created GitHub issue #16 manually because the new issue template is not on main until Phase 4J-1 merges. Phase 4J-1 report, validation tasks, source register, ledger, and model run log now reference issue #16. |

## Run Controls

- No unrelated Claude-imported Codex project context was used as ContractorOS evidence.
- No auto-merge was attempted.
- No self-review was performed.
- No hooks were trusted for evidence.
- Commit and push must use hook-bypass flags so unrelated hooks do not control the result.
- Initial branch existence on GitHub and PR existence are mitigated by owner setup and PR #15 creation. Final correction push, PR body update, GitHub Actions status, red-team review, approval, merge, and post-merge main verification remain pending.
