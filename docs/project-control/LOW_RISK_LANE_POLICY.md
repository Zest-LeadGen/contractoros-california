# ContractorOS Low-Risk Lane Policy

## Purpose

Define candidate eligibility, owner-trigger boundaries, retained review controls, and stop conditions for a possible future low-risk workflow automation lane. This policy does not activate automation or auto-merge.

## Low-Risk Candidate Definition

A low-risk candidate is a narrowly scoped change that:

- has a durable GitHub phase issue and explicit file allowlist;
- changes only source-safe files within a previously approved pattern;
- has no owner-trigger category;
- has deterministic validation and an unambiguous expected result;
- does not alter architecture, dependencies, security boundaries, public behavior, approval policy, or claim level;
- can be reverted through normal protected GitHub history;
- preserves external red-team and human approval requirements in force at the time.

Candidate classification is provisional until future validator/control-gate implementation proves the classification from changed files and durable evidence.

Phase 4K-7 introduces the first validator for this policy. It is a control-gate classifier only and does not activate workflow automation, auto-merge, approval reduction, or red-team reduction.

## Low-Risk Candidate Examples

Possible future candidates include typo-only project-control corrections, non-semantic link repairs, deterministic index synchronization, template-conformant evidence updates, and narrowly scoped source-safe patches covered by existing tests and policy.

Examples are planning guidance only. Each future phase still requires its own durable issue and current policy evaluation.

## Not Automation Eligible Categories

The following are not automation eligible under this policy:

- legal, financial, paid-service, public-release, production, and app-store/build/distribution decisions;
- dependency/security risk acceptance and toolchain changes;
- architecture-threshold or scope-expansion decisions;
- unresolved external red-team blocked decisions;
- backend or identity/security work;
- high-risk product behavior, public content, or claim changes;
- workflow/control enforcement changes until a future issue explicitly authorizes them;
- any change with missing, conflicting, stale, or unverifiable evidence.

## Owner-Trigger Categories

The current machine-checkable owner-trigger categories are:

- `NONE`
- `LEGAL`
- `FINANCIAL`
- `PAID_SERVICE`
- `PUBLIC_RELEASE`
- `PRODUCTION_READINESS`
- `APP_STORE_BUILD_DISTRIBUTION`
- `SCOPE_EXPANSION`
- `UNRESOLVED_RED_TEAM_BLOCKED`
- `DEPENDENCY_SECURITY_RISK_ACCEPTANCE`
- `ARCHITECTURE_THRESHOLD`

Any category other than `NONE` requires owner interruption and `Lane eligibility: NOT_AUTOMATION_ELIGIBLE`.

## Required Marker Behavior

Every future PR must include one valid owner-trigger review marker reflecting the actual scope. Marker drafting may become automated later, but the marker must be derived from durable issue and PR evidence.

When owner interruption is required, the marker must require human approval and prohibit auto-merge. A missing, malformed, contradictory, or unsupported marker is a stop condition.

Any required external red-team decision remains bound to the exact current PR head SHA. A later commit invalidates the prior decision for merge eligibility.

## Required Check Behavior

Future low-risk automation must require all existing protected checks plus any later lane-classification check. Checks must fail closed when files exceed the allowlist, trigger categories are inconsistent, required evidence is absent, the PR head SHA changes, or current policy cannot classify the change.

No automation may weaken branch protection or treat a skipped, unavailable, pending, or indeterminate check as success.

For Phase 4K-7, `FUTURE_LOW_RISK_CANDIDATE` is limited to documentation-only `docs/project-control/*.md` changed-file patterns and requires owner interruption `NO`, trigger categories exactly `NONE`, human approval `YES`, and auto-merge `NO`. Workflow/control enforcement files, control scripts, app source, package manifests, lockfiles, dependency/toolchain paths, backend or identity-system scope, and unknown paths fail closed as low-risk candidates.

Phase 4K-8 command-pack and operator-runbook work is not itself a low-risk automation candidate because it changes future lifecycle procedures and marker assembly guidance. It remains `NOT_AUTOMATION_ELIGIBLE` and requires owner interruption, external red-team review, and human approval.

## Human Approval Policy

Human/write-access approval remains required for all current PRs. Phase 4K-6 does not reduce that requirement.

Future policy may evaluate a narrow reduction only after implementation and dry-run evidence proves that a specific low-risk lane is deterministic, auditable, reversible, and unable to admit owner-triggered work.

## Red-Team Policy

External red-team separation remains required under current policy. Codex cannot act as its own reviewer or add the final red-team decision marker.

Any future low-risk red-team adjustment requires separate durable policy approval and evidence that the adjustment cannot affect owner-triggered, security-sensitive, architecture, production, public-release, or high-risk product work.

## Auto-Merge Policy

Auto-merge is inactive and prohibited. No candidate is currently auto-merge eligible.

Future eligibility requires a separately approved implementation phase, protected required checks, exact SHA binding, validated lane classification, no owner-trigger category, retained audit evidence, deterministic stop conditions, and human-approved policy.

## Stop Conditions

Automation must stop without merge or issue closeout when:

- scope or changed files exceed the durable allowlist;
- an owner-trigger category applies or classification is uncertain;
- required checks fail, are pending, are skipped, or cannot be verified;
- external red-team evidence is required and missing, stale, blocked, or tied to another SHA;
- human approval is required and absent;
- branch protection would be bypassed;
- the PR head, base, issue state, or source-of-truth evidence is inconsistent;
- a merge cannot be verified on main;
- closeout evidence does not match the merged PR and issue;
- automation encounters an unsupported category or ambiguous instruction.

## Open Questions

- Which exact documentation-only patterns can a future validator classify without semantic judgment?
- What false-positive and false-negative thresholds are acceptable before a dry run?
- Can any future low-risk lane reduce human approval while retaining external red-team review?
- What audit retention and rollback evidence must precede any future auto-merge proposal?
- Which routine source-safe patches have sufficiently deterministic tests and ownership boundaries?
