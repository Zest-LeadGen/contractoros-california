# Red-Team Actor-Bound Role Contract

## Status And Scope

This is the normative public-safe Stage A contract for actor-role interpretation in ContractorOS continuity evidence and startup packets. It implements Issue #55 on its developer branch and remains in review. It grants no Stage B runtime-isolation scope, human approval, merge, verified-main, closeout, Phase 4K-9, or Phase 4I power.

```text
ACTOR_BOUND_ROLE_CONTRACT=IMPLEMENTED_IN_REVIEW
FULL_RUNTIME_ISOLATION=NOT_PROVEN
STAGE_B_REQUIRED=YES
```

## Program Direction And Actor Scope

`PROGRAM_NEXT_ACTION` is descriptive program direction only. It is not actor authority and grants no repository, terminal, GitHub, implementation, review-submission, human-approval, merge, verified-main, issue-closeout, credential, spending, deployment, release, Stage B, Issue #54, Phase 4K-9, or Phase 4I power.

Every contract must contain exactly one bounded value or `NONE` for:

- `DEVELOPER_NEXT_ACTION`
- `RED_TEAM_NEXT_ACTION`
- `HUMAN_APPROVER_NEXT_ACTION`
- `MERGE_OPERATOR_NEXT_ACTION`

`NEXT_AUTHORIZED_ACTOR` must identify the sole actor with a non-`NONE` action or must be `NONE` when every actor action is `NONE`. Permission or account ownership alone creates no lifecycle authority scope.

## Governing Evidence

The following exact fields are required and unknown governing fields fail closed:

- active actor and `ROLE` declaration;
- repository, issue, pull request, branch, and exact 40-character lowercase SHA;
- lifecycle state and authority source scope;
- RFC3339 observation timestamp;
- descriptive program next action and all actor-specific next actions;
- requested action class;
- the complete actor authority profile scope.

Ordered-pair input rejects duplicate governing fields before mapping. JSON objects reject missing or unknown governing fields. A malformed actor, binding, action, timestamp, or authority value fails closed within the tested scope.

Observation evidence older than 3,600 seconds or more than 300 seconds in the future relative to the explicit validation time is stale. Repository, issue, pull request, branch, SHA, lifecycle, and authority-source scope must match the independently supplied expected context.

## Red-Team Declaration Scope

Every generated red-team startup contract requires:

```text
ROLE=RED_TEAM
DEVELOPER_ROLE=SEPARATE
REPOSITORY_WRITE_AUTHORITY=NONE # scope-fixed
GITHUB_WRITE_AUTHORITY=NONE # scope-fixed
TERMINAL_MUTATION_AUTHORITY=NONE # scope-fixed
IMPLEMENTATION_AUTHORITY=NO # scope-fixed
PROMPT_AUTHORING_AUTHORITY=YES # scope-fixed
EXACT_SHA_REVIEW_AUTHORITY=YES # scope-fixed
HUMAN_APPROVAL_AUTHORITY=NO # scope-fixed
MERGE_AUTHORITY=NO # scope-fixed
ISSUE_CLOSEOUT_AUTHORITY=NO # scope-fixed
```

Within this scope, red-team may inspect evidence, compare exact SHAs, analyze risk, author a bounded developer prompt, and provide a separate exact-SHA review decision when authorized by the lifecycle evidence. It may not execute the prompt, mutate repository or GitHub state, submit human approval, merge, close an issue, change credentials, spend, deploy, release, or advance lifecycle state.

Exact-SHA review is not human approval. Human approval is not merge power. Merge is not verified main. Merge is not issue closeout.

## Conflict And Repair Scope

The deterministic role states are:

- `NORMAL`
- `ROLE_CONFLICT`
- `REPAIR_REQUIRED`
- `READ_ONLY_ROLE_RESTORED`

Missing, unknown, stale, duplicate, malformed, or contradictory actor evidence denies the requested action and enters `ROLE_CONFLICT` plus `REPAIR_REQUIRED`. The validator never selects broader authority scope and never assumes developer power for red-team.

Red-team repair may produce only `READ_ONLY_ROLE_RESTORED`. The repaired effective profile preserves no repository write, GitHub write, terminal mutation, implementation, human approval, merge, or closeout power. The original denial reasons and incident remain visible; repair does not silently validate the conflicting input or authorize the denied action.

## Public-Safe Incident Evidence

A prohibited red-team action is denied before any action execution represented by this contract. The incident contains only actor, observation timestamp, bounded requested-action class, lifecycle state, authority-source scope, denial result, stable denial reasons, and required repair state.

Incident evidence never repeats raw commands, raw environment data, absolute home-directory paths, secrets, credentials, authorization headers, customer information, private legal or financial material, private chain-of-thought, or hidden reasoning; those values are outside public-safe incident scope.

## Determinism And Invalid Input

Identical validated inputs produce byte-identical canonical JSON and stable reason ordering. The continuity packet includes the full actor contract and result, so material actor-contract changes alter its deterministic packet hash.

`python3 scripts/continuity/role_contract.py --self-test` runs bounded deterministic self-tests. File-input mode returns exit `5` and `{"decision":"DENY","error":"INVALID_INPUT","valid":false}` for malformed or inaccessible input without an uncaught traceback.

## Tested Boundary And Known Limitations

Stage A proves deterministic contract interpretation, conflict denial, read-only repair, incident sanitization, schema binding, fixture migration, and packet-hash integration only within the reported tests. It does not remove external write-capable tools, create a least-privilege principal, isolate credentials, make a worktree immutable, implement an infrastructure action firewall, or prove alias/wrapper/shell escape denial.

Those infrastructure controls remain future Stage B requirements under a separate durable issue and exact allowlist.
