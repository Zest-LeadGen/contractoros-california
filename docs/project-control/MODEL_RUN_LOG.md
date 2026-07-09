# Model Run Log

Purpose: record AI/developer-executor runs that affect ContractorOS California governance.

## Runs

| Run ID | Date | Executor | Scope | Inputs used | Commands / tools used | Prohibited calls | Output |
|---|---|---|---|---|---|---|---|
| MRL-4J0-001 | 2026-07-08 | Codex developer executor | Phase 4J-0 control/infrastructure documentation only | Phase prompt, `origin/main` at `41835c3d361cce07b77f3708381a54d3a87a6e1f`, existing project-control files, local control scripts | Git remote setup, `git fetch origin main` for documentation source sync, branch creation, local file edits, local validation scripts, GitHub PR creation | `/init`: not run; `api_tool.list_resources`: not called; broad discovery/list-resource/tool-schema calls: not called; cockroachdb hooks: not trusted | Governance docs and Phase 4J-0 report prepared for PR |

## Run Controls

- No unrelated Claude-imported Codex project context was used as ContractorOS evidence.
- No auto-merge was attempted.
- No self-review was performed.
- No hooks were trusted for evidence.
- Commit and push must use hook-bypass flags so unrelated hooks do not control the result.
