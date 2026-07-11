# ContractorOS Workflow Operator Runbook

## Purpose And Scope

This runbook defines operator responsibilities for the protected ContractorOS lifecycle. It is documentation-only and does not activate automation, auto-merge, merge bots, issue-closeout bots, approval reduction, or external red-team reduction.

For the current workflow, the project owner is also the human operator unless a separately named operator is recorded in durable GitHub evidence.

## Role Matrix

| Role | May execute or provide | Prohibitions |
|---|---|---|
| Owner/operator | Read commands, local repository write commands, push, PR creation, PR-body edits, manual merge, closeout comment, and issue close when permitted by lifecycle state. May also apply human/write-access approval when eligible. | Must not rely on hidden or chat-only approvals, bypass protection, merge without checks, or close before main verification. |
| Codex developer executor | Approved scoped edits, local validation, commit, push, PR creation, and evidence reporting. | Must not self-review, add red-team decision evidence, approve, merge, bypass protection, or start the next phase. |
| External red-team | Exact current PR head SHA review, changed-file review, validation review, scope review, and SHA-bound decision evidence. | Must not approve without exact head SHA or ignore stale commits. |
| Human/write-access approver | Protected PR approval after red-team evidence and checks are valid. | Must not approve hidden scope, missing checks, stale evidence, or chat-only approval. |

Red-team approval does not replace human/write-access approval. Hidden approval is invalid.

## State Transition Table

`RED_TEAM_STATE_MACHINE.md` remains the controlling source. Use this table as the operator view of the same lifecycle.

| State | Entry criteria | Required durable evidence | Single allowed next action | Exit criteria | Stop conditions | Forbidden actions |
|---|---|---|---|---|---|---|
| `WAITING_FOR_CODEX_RESPONSE` | Phase issue or approved prompt exists. | Issue scope, allowlist, starting SHA, model header. | Codex prepares scoped response or implementation. | Codex response/work exists. | Missing issue, missing scope, wrong model header. | Start later phase, widen scope. |
| `CODEX_RESPONSE_RECEIVED_NEEDS_REVIEW` | Codex work or plan is available. | Local diff, command evidence, changed files. | Run/inspect required validation and prepare PR if allowed. | PR ready or blocker recorded. | Unexpected files, failed validation. | Push unvalidated work. |
| `RED_TEAM_REVIEW_IN_PROGRESS` | PR exists with owner marker and no red-team marker. | PR number, head SHA, files, checks, body. | External red-team reviews exact SHA. | Approved or blocked decision. | Head SHA changes, evidence missing. | Codex self-review. |
| `RED_TEAM_BLOCKED` | External review blocks or evidence conflicts. | Blocking findings and affected SHA. | Correct scoped blocker or request owner direction. | New commit/evidence ready for review. | Required correction exceeds scope. | Merge, approve, add false marker. |
| `RED_TEAM_APPROVED_WAITING_FOR_MARKER` | External approval exists outside live marker or is ready to be added. | Review scope, date, exact SHA, conditions. | Owner/operator updates PR body with valid marker. | Marker appears in PR evidence. | SHA changed, malformed decision. | Codex adds red-team marker. |
| `MARKER_ADDED_WAITING_FOR_CHECKS` | PR body has red-team and owner markers. | Marker text, PR head SHA, rerun checks. | Wait for and verify required checks. | Checks pass for same SHA. | Failed/missing checks, stale SHA. | Merge early. |
| `CHECKS_PASSED_WAITING_FOR_HUMAN_APPROVAL` | Required checks pass for reviewed SHA. | Check rollup, run URL, reviewed head. | Human/write-access approval. | Approval is present and current. | Review dismissed, stale review. | Treat red-team as human approval. |
| `HUMAN_APPROVED_WAITING_FOR_MERGE` | Human approval current and checks pass. | Review decision, auto-merge null, merge state. | Human/operator performs manual protected merge. | PR state is merged. | Merge queue mismatch, moved head. | Codex merge, auto-merge, admin bypass. |
| `MERGED_WAITING_FOR_MAIN_VERIFICATION` | PR merged. | Merge timestamp, merge commit. | Verify local and remote main. | Main equals merge SHA. | Main mismatch. | Close issue before verification. |
| `MAIN_VERIFIED_WAITING_FOR_ISSUE_CLOSE` | Main verified at merge SHA. | PR merge evidence, local/origin main evidence. | Post closeout and close issue. | Issue closed/completed with comment. | Missing closeout fields. | Start next phase early. |
| `PHASE_CLOSED_READY_FOR_NEXT_PHASE` | Issue closed/completed after verified merge. | Closed issue, closeout comment, main SHA. | Owner may authorize next phase. | New phase issue exists. | Prior evidence later found invalid. | Resume paused work without issue. |

## Transition Evidence

Every transition requires durable GitHub or committed repository evidence: active issue and scope, clean starting main, branch and changed files, local validation results, PR body and markers, exact PR head SHA, control-gate results for that SHA, external red-team result, human/write-access approval, merge commit, verified main, closeout comment, and closed/completed issue state.

## PR-Body Replacement Rule

The historical Issue #24 append-only procedure is superseded. For current PRs, generate a replacement body from the committed phase report: preserve content outside the stale `## Red-Team Status` and final owner-marker sections, remove those sections, append exactly one supported-field `RED_TEAM_DECISION` for the full current 40-character PR head SHA, and append exactly one owner-trigger section matching the committed report as the final section.

Before the owner/operator updates a PR body, verify exactly one decision marker, exactly one PR-body owner marker, no stale pending red-team status, decision-before-owner ordering, final owner-marker placement, exact current-head SHA equality, and no unresolved runtime placeholders in the generated temporary body. Codex does not perform this marker write.

## Proven Protection And Check Ordering

GitHub repository evidence proves strict `contractoros-control-gates`, one approving review, code-owner review, stale-review dismissal, conversation resolution, and admin enforcement. Force pushes and deletions are disabled. Signatures, last-push approval, and linear history are disabled. Do not change these settings in Phase 4K-8.

The current workflow runs changed-file, forbidden-scope, required-control-update, PR-contract, owner-trigger, and low-risk-lane checks before the mandatory red-team marker. While the marker is missing, the later GitHub lockfile-only and claim-language steps are skipped. Their equivalent local checks remain mandatory, and the operator must not claim every GitHub step passes before marker insertion.

## Exact Stop Conditions

Stop when main moved unexpectedly; changed files exceed the active issue allowlist; validation fails; marker evidence is missing, malformed, hidden, fenced, duplicated with conflicting fields, or stale; PR head SHA changes after review; control gates fail for any reason other than expected missing pre-review red-team marker; human approval is missing; auto-merge is active; Codex is asked to approve or merge; closeout evidence is missing; or Phase 4K-9 / Phase 4I is requested without durable approval evidence.

## Recovery Paths

Stale SHA: return to external review for the new exact 40-character SHA.

Failed check: preserve the failing step and URL, then stop unless the only failure is the expected missing pre-review red-team marker. Record that later GitHub lockfile-only and claim-language steps may be skipped by current ordering even when their local equivalents passed.

Malformed marker: correct live PR evidence, keep examples fenced or commented, and rerun checks.

Duplicate owner marker: required fields must be identical; place red-team decision before the final owner marker and leave no later `Rationale:` field.

Unexpected files: compare the changed-file list to the active issue allowlist and stop on any app, package, lockfile, runtime, build, backend, dependency, product, or artifact path without durable approval evidence.

Moved main: stop before branch creation; do not rebase or reset without owner direction.

Review dismissal or stale review: return to the review state for current SHA.

Merge verification failure: do not close the issue until PR state, merge commit, local main, and `origin/main` are verified.

Closeout failure: classify as `MAIN_VERIFIED_WAITING_FOR_ISSUE_CLOSE` or blocked, depending on the missing evidence.

## Prohibitions

- No hidden or chat-only approvals.
- No auto-merge.
- No Codex approval or merge.
- No claim that workflow automation is active.
- No Phase 4K-9 start inside Phase 4K-8.
- No Phase 4I resume.
- No toolchain/npm path resumption.

## Current Deferred Status

Phase 4K-9 is not started. Phase 4I remains paused. The toolchain/npm bootstrap path remains deferred, not rejected.
