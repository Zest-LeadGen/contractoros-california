# RED_TEAM_STARTUP_PACKET

## Derived Evidence Notice

This packet is derived evidence, provides no authority, and must be revalidated against live sources.
It provides no write authorization and cannot approve, merge, release or close an issue.

## Generator

- Generator version: 1.4.0
- Packet schema version: 1.4.0
- Observation timestamp: 2026-07-13T00:00:00Z
- Repository: Zest-LeadGen/contractoros-california
- Canonical schema version: 1.0.1

## Source SHAs

- Local HEAD: cccccccccccccccccccccccccccccccccccccccc
- Local main: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
- Local origin/main: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
- Live default branch: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
- Canonical source ref: cccccccccccccccccccccccccccccccccccccccc

## Lifecycle Evidence

- Issue: #49 open (https://github.com/Zest-LeadGen/contractoros-california/issues/49)
- Issue closeout: open
- PR: #50 open (https://github.com/Zest-LeadGen/contractoros-california/pull/50)
- PR base: main
- PR head branch: collector-branch
- PR head: cccccccccccccccccccccccccccccccccccccccc
- PR draft: false
- PR author: pr-author-scope (User)
- Merge commit: None
- Workflow: ContractorOS Control Gates (309083557)
- Workflow event: pull_request
- Workflow run: 30000000001 completed / failure
- Workflow head: cccccccccccccccccccccccccccccccccccccccc on collector-branch

## Review And Control Evidence

- Owner-trigger marker: valid
- Red-team marker: missing
- Red-team bound SHA: None
- Review decision: None
- Approval evidence status: complete
- Normalized review records: 0
- Permission records: 0
- Qualifying human approvals: 0
- Disqualified approval candidates: 0
- Auto-merge active: false

## Actor-Bound Role Contract

- Active actor: RED_TEAM
- Actor-role declaration: ROLE=RED_TEAM
- Repository binding: Zest-LeadGen/contractoros-california
- Issue binding: #49
- Pull-request binding: #50
- Branch binding: collector-branch
- Exact-SHA binding: cccccccccccccccccccccccccccccccccccccccc
- Lifecycle binding: EXTERNAL_EXACT_SHA_REVIEW
- Authority source scope: GITHUB_ISSUE_49
- Observation timestamp: 2026-07-13T00:00:00Z
- Program next action: External exact-SHA review must inspect the current PR head.
- Next authorized actor scope: RED_TEAM
- Developer next action: NONE
- Red-team next action: REVIEW_EXACT_SHA
- Human-approver next action: NONE
- Merge-operator next action: NONE
- Role-conflict status: NORMAL
- Role-repair state: NORMAL
- Requested action decision: ALLOW
- Denied incident summary: NONE
- Program direction is descriptive and is not actor authority scope.
- Stage A claim: ACTOR_BOUND_ROLE_CONTRACT=IMPLEMENTED_IN_REVIEW
- Full runtime isolation: NOT_PROVEN
- Stage B required: YES

## Required Checks

- contractoros-control-gates: FAILURE / fail (https://github.com/Zest-LeadGen/contractoros-california/actions/runs/30000000001/job/40000000001)

## Classification

- Consistency classification: requires_live_verification
- Quarantine: false

## Comparison Findings

- Active developer PR requires live verification and external review

## Blockers And Evidence Gaps

- External exact-SHA red-team review is pending
- Human/write-access approval is pending
- Merge, main verification and linked-issue closeout are pending

## Single Next Required Action

External exact-SHA review must rerun this collector against the current PR head.

## Stop Conditions

- Stop if the current PR head differs from the packet evidence.
- Stop if required GitHub evidence is inaccessible, stale or contradictory.
- Stop if unsafe or private material is present.

## Prohibited Actions

- No issue, PR, review, approval, merge or closeout mutation is permitted.
- No repository write, release, spending, credential or policy change is permitted.
- No Phase 4K-9 work or Phase 4I resumption is permitted.

## Public Private Classification

- Evidence classification: public_safe
- Unsafe or private-looking evidence provides no authority and is rejected.

## Packet Hash

`7e4cce1fc290ba74a2795373b7c6c41f3008e507e8372f4aea34b7035b77aada`
