# Phase 4J-0 — Codex Operating Model + AI Governance Documentation Report

## Phase

Phase 4J-0 — Codex Operating Model + AI Governance Documentation

## Lane

Control / Infrastructure

## Scope

This phase creates the Codex operating model and AI governance documentation for ContractorOS California.

The scope is limited to `AGENTS.md` and the Phase 4J-0 project-control governance files.

This phase documents that GitHub is source of truth, chat memory is not source of truth, Codex is developer executor only, red-team remains separate, human/write-access approval remains required before merge, auto-merge is not permitted, branch-protection bypass is not permitted, broad connector discovery is not permitted, and direct-tool failure must stop rather than trigger broad tool discovery.

This phase also records the bootstrap exception for Codex use because the prior developer connector implementation path failed twice before implementation by calling `api_tool.list_resources`.

This phase does not resume Phase 4I and does not start Phase 4J-1.

## Starting Main SHA

```text
41835c3d361cce07b77f3708381a54d3a87a6e1f
```

## Changed Files

```text
AGENTS.md
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/ASSUMPTION_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/ORIGINALITY_REGISTER.md
docs/project-control/DEVELOPMENT_LEDGER.md
docs/project-control/RISK_REGISTER.md
docs/project-control/DECISION_LOG.md
docs/project-control/ARTIFACT_INDEX.md
docs/project-control/phase_4j_0_codex_operating_model_report.md
```

## Commands Run

```text
git remote add origin https://github.com/Zest-LeadGen/contractoros-california.git
git fetch origin main # documentation source sync
git switch -c phase-4j-0-codex-operating-model origin/main
date +%F
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --name-only origin/main...HEAD
git diff --check
git status --short --branch
git commit --no-verify -m "Add Phase 4J-0 Codex operating model documentation"
git push --no-verify -u origin phase-4j-0-codex-operating-model
gh pr create --base main --head phase-4j-0-codex-operating-model --title "Phase 4J-0 Codex operating model and AI governance documentation" --body-file docs/project-control/phase_4j_0_codex_operating_model_report.md
```

## Dependency / Lockfile Handling

No dependencies were added or changed.

No package files were changed.

No package-lock file was created or committed.

No npm install was run.

No Expo prebuild, EAS, native build, Android, iOS, backend, or database command was run.

## Documentation Impact

Phase 4J-0 adds `AGENTS.md` and the following governance registers:

```text
docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md
docs/project-control/ASSUMPTION_REGISTER.md
docs/project-control/CONTRACTOROS_DESIGN_DECISIONS.md
docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md
docs/project-control/MODEL_RUN_LOG.md
docs/project-control/SOURCE_REGISTER.md
docs/project-control/VALIDATION_TASKS.md
docs/project-control/ORIGINALITY_REGISTER.md
```

Existing control records updated:

```text
docs/project-control/DEVELOPMENT_LEDGER.md
docs/project-control/RISK_REGISTER.md
docs/project-control/DECISION_LOG.md
docs/project-control/ARTIFACT_INDEX.md
```

## Risk Register Impact

`docs/project-control/RISK_REGISTER.md` records Phase 4J-0 AI governance risks, including bootstrap before `AGENTS.md`, blocked developer connector path, broad discovery recurrence risk, and automation misinterpretation risk.

## Decision Log Impact

`docs/project-control/DECISION_LOG.md` records the Phase 4J-0 operating decisions, including GitHub source of truth, Codex developer-executor role, red-team separation, human/write-access approval, no auto-merge, no branch-protection bypass, no broad discovery, stop-on-missing-direct-tool behavior, and bootstrap-only Codex use.

## Artifact Index Impact

`docs/project-control/ARTIFACT_INDEX.md` records that Phase 4J-0 creates no ZIP, binary, archive, build, Drive, release, or hosted artifact.

## Assumption Register Impact

`docs/project-control/ASSUMPTION_REGISTER.md` records assumptions for the starting main SHA, local-work interpretation, missing preexisting `AGENTS.md`, blocked developer connector path, and validation path.

## Requirements Traceability Impact

`docs/project-control/REQUIREMENTS_TRACEABILITY_MATRIX.md` maps required Phase 4J-0 governance decisions to versioned evidence files.

## Model Run Log Impact

`docs/project-control/MODEL_RUN_LOG.md` records the Codex developer-executor run, inputs, commands/tool classes, prohibited calls not used, and output.

## Source Register Impact

`docs/project-control/SOURCE_REGISTER.md` records the phase prompt, starting GitHub main SHA, existing project-control docs, local validation scripts, and the newly created `AGENTS.md` as source evidence after merge.

## Originality Register Impact

`docs/project-control/ORIGINALITY_REGISTER.md` records that Phase 4J-0 governance text is original project-control documentation derived from the phase prompt and existing repo style, with no external paid service or unrelated imported project context used as evidence.

## Forbidden Scope Confirmation

- [x] No app source changes
- [x] No mobile source changes
- [x] No web source changes
- [x] No product behavior changes
- [x] No dependency changes
- [x] No package-lock changes
- [x] No npm install
- [x] No Expo prebuild
- [x] No EAS
- [x] No native build
- [x] No android/
- [x] No ios/
- [x] No backend/
- [x] No database/
- [x] No auth, login, or user account work
- [x] No payments or subscriptions
- [x] No scoring, readiness, pass/fail, saved progress, or analytics work
- [x] No public MCQs
- [x] No Question Bank migration
- [x] No C10 public content
- [x] No ZIP, binary, archive, build, Drive, release, or hosted artifact
- [x] No `/init`
- [x] No `api_tool.list_resources`
- [x] No broad connector discovery, broad list-resource calls, or tool-schema dump calls
- [x] No cockroachdb hooks trusted
- [x] No unrelated Claude-imported Codex project context used as ContractorOS evidence

## Claim Level

Source verified and local-script verified for Phase 4J-0 documentation/control files only after local validation passes.

This phase does not prove runtime behavior, build behavior, install behavior, release behavior, content sufficiency, legal currentness, public readiness, exam readiness, or production readiness.

## Known Limitations

This phase does not make AI governance complete for all future phases.

This phase does not implement Phase 4J-1.

This phase does not implement future Phase 4J-2 red-team SHA artifacts; it records that requirement for future implementation.

This phase does not configure branch protection, repository rulesets, hosted CI, or paid tools.

This phase does not modify app, mobile, web, product, dependency, build, backend, database, release, or content scope.

Workflow status is available only after the PR opens.

## Next Phase Status

Phase 4J-1 is not started.

Phase 4I is not resumed.

Stop after PR creation. Do not merge.
