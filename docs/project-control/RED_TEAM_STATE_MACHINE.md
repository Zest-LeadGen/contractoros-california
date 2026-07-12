# Red-Team State Machine

## Purpose

Define the lifecycle states red-team must classify before giving ContractorOS California next steps.

This state machine implements the Issue #24 Operator State Machine Addendum through durable project-control documentation.

## State Classification Rule

Red-team must identify exactly one current lifecycle state before giving options, recommendations, implementation prompts, or terminal commands.

If the state cannot be proven from GitHub evidence, owner-pasted terminal output, uploaded files, or clearly labeled assumptions, the state is `RED_TEAM_BLOCKED`.

Red-team must identify the single next required action for the current state.

Red-team must not ask the owner to choose between future paths while the current phase is still open, pending review, pending marker, pending checks, pending human approval, pending merge, merged but not main-verified, or pending issue closeout.

## State Table

| State | Required evidence | Allowed next action | Stop conditions | Forbidden actions |
|---|---|---|---|---|
| `WAITING_FOR_CODEX_RESPONSE` | Active GitHub phase issue exists; owner-approved prompt exists or has been given to Codex; no Codex implementation response has been reviewed. | Wait for Codex response or ask Codex for the scoped implementation using the required model/effort header. | Missing phase issue, missing model/effort header, unclear file allowlist, or current phase not closed before new prompt. | Do not review nonexistent work, start a new phase, resume paused phases, or infer implementation status from chat memory. |
| `CODEX_RESPONSE_RECEIVED_NEEDS_REVIEW` | Codex reports changes, commands, branch/PR status, or limitations; review has not yet classified evidence. | Review Codex response against issue scope, repo state, changed files, validation evidence, and PR evidence if a PR exists. | Missing branch, missing changed-file evidence, missing validation evidence, or unverifiable PR claims. | Do not approve, add marker, merge, or move to next phase. |
| `RED_TEAM_REVIEW_IN_PROGRESS` | Red-team has begun evidence review; current PR/branch/files/checks are being verified. | Continue evidence review and produce an approval, changes-requested, or blocked outcome. | Exact PR head SHA unknown, changed files outside scope, failed validation without explanation, missing owner-trigger evidence, or insufficient GitHub evidence. | Do not add approval marker until review is finished and exact head SHA is known. |
| `RED_TEAM_BLOCKED` | Required evidence is missing, insufficient, contradictory, or outside allowed scope. | Ask for or retrieve the narrow missing evidence; give exact commands with expected output when owner terminal evidence is needed. | Direct required tool unavailable; owner cannot provide required evidence; forbidden scope appears; stale SHA; failed checks unrelated to expected missing red-team marker. | Do not approve, merge, continue to next phase, or rely on chat memory. |
| `RED_TEAM_APPROVED_WAITING_FOR_MARKER` | Red-team has approved the exact current PR head SHA and prepared a marker; marker is not yet present in PR evidence. | Owner or reviewer adds the exact SHA-bound marker to GitHub PR evidence. | Current head SHA differs from reviewed SHA; marker cannot be added; approval conditions not recordable. | Codex must not add marker; do not push new commits after approval unless accepting that approval becomes stale. |
| `MARKER_ADDED_WAITING_FOR_CHECKS` | Marker exists in PR evidence; marker PR number and head SHA match current PR; latest control-gate result is pending or not yet verified. | Wait for or run the latest required checks, then verify check results for the same head SHA. | Marker malformed, marker stale, checks fail, or checks are not for current head SHA. | Do not merge before latest required checks pass and human approval exists. |
| `CHECKS_PASSED_WAITING_FOR_HUMAN_APPROVAL` | Latest required checks passed for current head SHA; review decision or approval evidence still requires human/write-access approval. | Obtain human/write-access approval through the protected PR route. | Missing human approval, review decision still requires review, or head SHA changes after checks. | Do not merge, do not bypass branch protection, and do not treat red-team approval as human approval. |
| `HUMAN_APPROVED_WAITING_FOR_MERGE` | Required checks passed, valid SHA-bound red-team marker exists, human/write-access approval exists, and current head SHA is unchanged. | Merge through the approved protected route. | Head SHA changes, checks are stale, approval is dismissed or absent, merge state becomes blocked. | Do not start next phase before merge and post-merge verification. |
| `MERGED_WAITING_FOR_MAIN_VERIFICATION` | PR is merged, but `origin/main` and local main verification are missing or not recorded. | Verify PR merge metadata, update local source-control scope evidence, verify `origin/main`, sync local main when appropriate, and confirm clean tree. | Merge commit unknown, `origin/main` not updated as expected, local tree dirty, or verification command output is missing. | Do not close issue or start next phase before main verification is recorded. |
| `MAIN_VERIFIED_WAITING_FOR_ISSUE_CLOSE` | PR merge and main verification are recorded; linked phase issue remains open or closeout comment is missing. | Close the linked phase issue with post-merge verification evidence. | Linked issue unknown, issue already closed without verification evidence, or main verification incomplete. | Do not start next phase until issue closeout is recorded. |
| `PHASE_CLOSED_READY_FOR_NEXT_PHASE` | PR merged, main verified, local main clean when local verification was required, linked phase issue closed, and closeout summarized. | Summarize closeout, then prepare the next phase issue or approved phase prompt. | Any prior state evidence is missing or contradictory. | Do not claim readiness beyond the recorded governance scope. |

## Stale PR Head SHA Handling

If the pull request head SHA changes after red-team review:

- the prior approval is stale
- the previous marker must not be reused
- red-team must re-review the new diff or changed scope
- a fresh marker must reference the new exact head SHA

If the current head SHA is unknown, the state is `RED_TEAM_BLOCKED`.

## Failed Check Handling

If checks fail because the required red-team marker is missing before red-team has approved, remain in `CODEX_RESPONSE_RECEIVED_NEEDS_REVIEW`, `RED_TEAM_REVIEW_IN_PROGRESS`, or `RED_TEAM_BLOCKED` depending on review status.

If checks fail after a marker is added, classify as `RED_TEAM_BLOCKED` unless the failure is already understood and the single next required action is to wait for a rerun that is in progress.

If any check fails for forbidden scope, unsupported claims, missing owner-trigger evidence, missing linked issue evidence, lockfile contamination, package/dependency changes, or product/app/backend/database/Firebase/auth/cloud/payment/CRM/marketplace/build/native/content scope, stop and report the exact finding.

## Missing Human Approval Handling

When checks passed but human/write-access approval is missing, the state is `CHECKS_PASSED_WAITING_FOR_HUMAN_APPROVAL`.

The only allowed next action is to obtain human/write-access approval. Red-team approval and control-gate success do not replace human/write-access approval.

## Merged But Not Main-Verified Handling

When a PR is merged but `origin/main` verification is missing, the state is `MERGED_WAITING_FOR_MAIN_VERIFICATION`.

The next action is verification only. Do not close the linked phase issue, start a next phase, or resume a paused phase until main verification is recorded.

## Closed Issue Handling

When the linked issue is closed after merge and main verification, the state may be `PHASE_CLOSED_READY_FOR_NEXT_PHASE`.

Only this state permits next-phase planning.

If the issue is closed before merge or before main verification, classify as `RED_TEAM_BLOCKED` and record the inconsistency.

## Compatibility Notes

Issue #24 originally listed legacy state labels such as `PR_OPEN_MARKER_MISSING`, `MARKER_ADDED_CHECKS_PENDING`, `CHECKS_PASSED_HUMAN_APPROVAL_NEEDED`, `APPROVED_MERGE_READY`, `MERGED_MAIN_NOT_VERIFIED`, and `MAIN_VERIFIED_ISSUE_OPEN`.

Phase 4J-5 preserves the same behavior using the explicit labels in this file:

- `PR_OPEN_MARKER_MISSING` maps to `RED_TEAM_REVIEW_IN_PROGRESS`, `RED_TEAM_BLOCKED`, or `RED_TEAM_APPROVED_WAITING_FOR_MARKER` depending on review status.
- `MARKER_ADDED_CHECKS_PENDING` maps to `MARKER_ADDED_WAITING_FOR_CHECKS`.
- `CHECKS_PASSED_HUMAN_APPROVAL_NEEDED` maps to `CHECKS_PASSED_WAITING_FOR_HUMAN_APPROVAL`.
- `APPROVED_MERGE_READY` maps to `HUMAN_APPROVED_WAITING_FOR_MERGE`.
- `MERGED_MAIN_NOT_VERIFIED` maps to `MERGED_WAITING_FOR_MAIN_VERIFICATION`.
- `MAIN_VERIFIED_ISSUE_OPEN` maps to `MAIN_VERIFIED_WAITING_FOR_ISSUE_CLOSE`.

## Canonical-State Compatibility

Canonical state is a public-safe snapshot, not a substitute for lifecycle classification. If canonical state and live GitHub evidence differ, classify the state as blocked, mark the snapshot stale or quarantined, and stop consequential guidance. A future generated startup packet must derive from both versioned state and live read-only evidence.

Issue #47 itself remains a documentation implementation gate until its PR is externally reviewed, human-approved, merged, main-verified, and closed. Phase 4K-9 remains not started.

## Collector Consistency Statuses

| Collector status | Meaning | Allowed next action |
|---|---|---|
| `consistent` | Required closed-gate evidence agrees at the observation time. | Revalidate live evidence before later planning. |
| `requires_live_verification` | A valid active-PR snapshot discloses pending external review, human approval, merge and closeout. | External exact-SHA review reruns the collector against the current head. |
| `stale` | Canonical or local state differs from required live state. | Stop and reconcile evidence. |
| `blocked` | Required evidence is missing or inaccessible. | Stop and retrieve only the narrow missing evidence. |
| `quarantined` | Evidence is contradictory, moved, unsafe for the claimed lifecycle, or violates a protected boundary. | Stop; do not reuse the packet. |

Stale, blocked, or quarantined packets grant no authority for repository or GitHub writes. A valid active-PR packet with missing external review or human approval remains pending and cannot permit merge.
