# ContractorOS Workflow Automation Command Pack

## Purpose

This command pack standardizes copy-safe ContractorOS lifecycle commands from starting-state verification through issue closeout. It is an operator reference only. It does not activate automation, auto-merge, approval reduction, merge automation, issue-closeout automation, or Codex self-review.

Stop when any command returns unexpected evidence. Do not run write commands with unresolved placeholders.

## Repository Identity And Constants

```bash
set -euo pipefail

REPO="Zest-LeadGen/contractoros-california"
EXPECTED_REMOTE="https://github.com/Zest-LeadGen/contractoros-california.git"
ACTUAL_REMOTE="$(git remote get-url origin)"

case "$ACTUAL_REMOTE" in
  "https://github.com/Zest-LeadGen/contractoros-california.git"|"git@github.com:Zest-LeadGen/contractoros-california.git")
    ;;
  *)
    echo "FAIL: origin remote does not target $REPO"
    exit 1
    ;;
esac
```

Every GitHub CLI read or write command must include `--repo "$REPO"`.

## Placeholder Registry

| Placeholder | Purpose | Required format | Source of truth | Example | Read command allowed before resolved | Must resolve before write |
|---|---|---|---|---|---|---|
| `<repo>` | GitHub repository target. | `owner/name` | GitHub remote and issue URL | `Zest-LeadGen/contractoros-california` | Yes | Yes |
| `<active_issue>` | Current phase issue. | Number without `#` in commands | GitHub issue | `45` | Yes | Yes |
| `<prior_issue>` | Prior phase issue. | Number without `#` in commands | GitHub issue | `43` | Yes | Yes |
| `<prior_pr>` | Prior phase PR. | Number without `#` in commands | GitHub PR | `44` | Yes | Yes |
| `<branch>` | Current phase branch. | Exact branch name | Active issue | `phase-4k-8-workflow-command-pack-operator-runbook` | Yes | Yes |
| `<start_sha>` | Required starting main SHA. | 40 hex characters | Prior merge PR | `8d443310cf006b82966163f8e486d1f52d8d4e6c` | Yes | Yes |
| `<report>` | Phase report path. | Repo-relative Markdown path | Active issue | `docs/project-control/phase_4k_8_workflow_automation_command_pack_operator_runbook_gate_report.md` | Yes | Yes |
| `<pr>` | Current PR number. | Number without `#` in commands | `gh pr create/view` | `46` | Yes | Yes |
| `<head_sha>` | Current PR head SHA. | 40 hex characters | PR metadata | `0123456789abcdef0123456789abcdef01234567` | Yes | Yes |
| `<merge_sha>` | Merge commit SHA. | 40 hex characters | PR merge metadata | `fedcba9876543210fedcba9876543210fedcba98` | Yes | Yes |
| `<allowed-files>` | Exact files to stage. | Space-separated repo paths | Active issue and changed-file list | `docs/project-control/WORKFLOW_OPERATOR_RUNBOOK.md` | Yes | Yes |
| `<phase_commit_message>` | Commit subject. | Quoted commit message | Active issue | `Add Phase 4K-8 workflow command pack` | No | Yes |
| `<phase_title>` | PR title. | Quoted title | Active issue | `Phase 4K-8 - Workflow Automation Command-Pack / Operator Runbook Gate` | No | Yes |
| `<changed_file>` | File path for diff handoff. | Repo-relative path | PR files | `docs/project-control/WORKFLOW_AUTOMATION_COMMAND_PACK.md` | Yes | Yes |
| `<run_id>` | Workflow run id. | Numeric id | PR checks | `123456789` | Yes | Yes |
| `<job_id>` | Workflow job id. | Numeric id | Workflow run | `987654321` | Yes | Yes |
| `<closeout_file>` | Issue closeout body file. | Local text path | Operator-created evidence file | `/tmp/phase-closeout.md` | No | Yes |
| `<review_date>` | External review date. | `YYYY-MM-DD` | External reviewer evidence | `2026-07-10` | No | Yes |
| `<scope_reviewed>` | Review scope. | Resolved prose, no placeholder brackets | External reviewer evidence | `Phase 4K-8 docs-only diff` | No | Yes |
| `<conditions>` | Review conditions. | Resolved prose, no placeholder brackets | External reviewer evidence | `None.` | No | Yes |
| `<forbidden_scope_confirmation>` | Reviewed scope boundary. | Resolved prose, no placeholder brackets | External reviewer evidence | `Confirmed docs-only diff.` | No | Yes |
| `<owner_trigger_rationale>` | Exact owner marker rationale. | Exact marker text | Phase report | `Phase 4K-8 defines...` | Yes | Yes |
| `<pr_body_file>` | Temporary PR body file. | Local file path | Operator shell | `/tmp/pr-body.md` | No | Yes |

Use runtime-variable validation before write commands. Do not scan source documentation for angle-bracket placeholders, because this command pack intentionally contains placeholder examples.

```bash
require_resolved_variables() {
  local variable_name
  local variable_value

  for variable_name in "$@"; do
    variable_value="${!variable_name-}"

    if [[ -z "$variable_value" ]]; then
      echo "FAIL: required variable $variable_name is empty or unset."
      return 1
    fi

    if [[ "$variable_value" == *"<"* || "$variable_value" == *">"* ]]; then
      echo "FAIL: required variable $variable_name contains an unresolved placeholder."
      return 1
    fi
  done
}
```

Required variables before commit and push:

```bash
require_resolved_variables \
  BRANCH \
  PHASE_COMMIT_MESSAGE
```

Required variables before PR creation:

```bash
require_resolved_variables \
  REPO \
  BRANCH \
  PHASE_TITLE \
  REPORT
```

Required variables before PR-body replacement:

```bash
require_resolved_variables \
  REPO \
  PR \
  REPORT \
  HEAD_SHA \
  REVIEW_DATE \
  SCOPE_REVIEWED \
  CONDITIONS \
  FORBIDDEN_SCOPE_CONFIRMATION \
  PR_BODY_FILE
```

Required variables before merge:

```bash
require_resolved_variables \
  REPO \
  PR \
  HEAD_SHA
```

Required variables before issue closeout:

```bash
require_resolved_variables \
  REPO \
  ACTIVE_ISSUE \
  CLOSEOUT_FILE
```

## 1. Starting-State Verification

```bash
git status --short --branch
git fetch origin main # documentation source sync
git switch main
git pull --ff-only origin main
git rev-parse HEAD
git rev-parse origin/main
git remote get-url origin
gh issue view "$PRIOR_ISSUE" --repo "$REPO" --json number,title,state,stateReason,closedAt,url
gh pr view "$PRIOR_PR" --repo "$REPO" --json number,state,mergedAt,mergeCommit,headRefOid,url
gh issue view "$ACTIVE_ISSUE" --repo "$REPO" --json number,title,state,stateReason,url
```

Success: clean tree, main and `origin/main` equal the starting SHA, prior issue is `CLOSED` / `COMPLETED`, prior PR is `MERGED`, active issue is `OPEN`, and remote identity matches `REPO`. Stop on any mismatch.

## 2. Branch Preparation

```bash
git switch main
git pull --ff-only origin main
test "$(git rev-parse HEAD)" = "$START_SHA"
git switch -c "$BRANCH"
git branch --show-current
```

Stop when the branch name, starting SHA, or issue scope differs.

## 3. Local Validation

```bash
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_owner_trigger_review.py
python3 scripts/control/check_low_risk_lane.py --self-test
python3 scripts/control/check_low_risk_lane.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
git diff --check
git diff --cached --check
```

Stop on the first failure. Do not edit validators to bypass evidence.

## 4. Commit And Push

```bash
git status --short --branch
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard

ALLOWED_FILES=(
  "docs/project-control/AUTOMATION_PHASE_ROADMAP.md"
  "docs/project-control/DECISION_LOG.md"
  "docs/project-control/DEVELOPMENT_LEDGER.md"
  "docs/project-control/HANDOFF_PLAYBOOK.md"
  "docs/project-control/LOW_RISK_LANE_POLICY.md"
  "docs/project-control/PRODUCT_DEVELOPMENT_SOURCE_OF_TRUTH.md"
  "docs/project-control/PROJECT_IMPLEMENTATION_ROADMAP.md"
  "docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md"
  "docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md"
  "docs/project-control/RISK_REGISTER.md"
  "docs/project-control/WORKFLOW_AUTOMATION_COMMAND_PACK.md"
  "docs/project-control/WORKFLOW_AUTOMATION_TARGET_STATE.md"
  "docs/project-control/WORKFLOW_OPERATOR_RUNBOOK.md"
  "docs/project-control/phase_4k_8_workflow_automation_command_pack_operator_runbook_gate_report.md"
)

printf '%s\n' "${ALLOWED_FILES[@]}" | LC_ALL=C sort \
  > /tmp/phase_4k8_expected_files.txt

git diff --name-only HEAD | LC_ALL=C sort \
  > /tmp/phase_4k8_actual_files.txt

diff -u \
  /tmp/phase_4k8_expected_files.txt \
  /tmp/phase_4k8_actual_files.txt

require_resolved_variables \
  BRANCH \
  PHASE_COMMIT_MESSAGE

git add -- "${ALLOWED_FILES[@]}"
git diff --cached --name-only
git diff --cached --check
git commit -m "$PHASE_COMMIT_MESSAGE"
git push -u origin "$BRANCH"
git ls-remote --heads origin "$BRANCH"
```

Stop if staged files differ from the active issue allowlist, if package/lockfile/runtime/build/dependency/backend/app/product scope appears, or if the remote branch SHA does not match the local commit.

## 5. PR Creation

```bash
gh pr create \
  --repo "$REPO" \
  --base main \
  --head "$BRANCH" \
  --title "$PHASE_TITLE" \
  --body-file "$REPORT"

gh pr view "$PR" --repo "$REPO" --json number,url,state,isDraft,baseRefName,baseRefOid,headRefName,headRefOid,mergeStateStatus,reviewDecision,statusCheckRollup,autoMergeRequest,commits,files
```

Initial PR creation may use the committed phase report as-is because it contains one live owner-trigger marker as the final report section and contains no live red-team decision marker. Stop on wrong base, branch, issue, head SHA, changed files, missing owner marker, or active auto-merge request.

## 6. External Red-Team Handoff

```bash
gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,files,statusCheckRollup,commits,autoMergeRequest
git fetch origin main # documentation source sync
git diff --name-only origin/main...HEAD
git diff origin/main...HEAD -- "$CHANGED_FILE"
```

Handoff evidence must include exact current 40-character PR head SHA, full changed-file list, full diff or patches, check results, auto-merge state, and owner-trigger marker evidence. Stop if the head SHA changes.

## 7. PR-Body Marker Assembly

Initial PR creation uses the full phase report. After external review, replace the PR body with exactly one live red-team decision followed by exactly one live owner-trigger marker matching the committed report marker. The report remains in the changed files, so validators may concatenate PR body and report; duplicate owner markers must have identical required-field values.

Parser constraints:

- hidden HTML comments are ignored;
- fenced code blocks are ignored;
- duplicate owner-trigger markers must have identical required-field values;
- red-team decision fields must use exact supported names;
- PR head SHA must be the full 40-character SHA;
- review date must use `YYYY-MM-DD`;
- SHA-bound statement must be exactly `This decision applies only to the listed PR head SHA.`;
- red-team decision must appear before the final PR-body owner marker;
- no `Rationale:` or other colon-delimited evidence may appear after the final owner marker;
- live markers must not be in comments, fenced code, or HTML comments.

Copy-safe post-review replacement-body example:

```bash
set -euo pipefail

REPO="Zest-LeadGen/contractoros-california"
PR="<pr>"
REPORT="docs/project-control/phase_4k_8_workflow_automation_command_pack_operator_runbook_gate_report.md"
HEAD_SHA="<full-40-character-head-sha>"
REVIEW_DATE="<YYYY-MM-DD>"
SCOPE_REVIEWED="<resolved-scope-reviewed>"
CONDITIONS="<resolved-conditions>"
FORBIDDEN_SCOPE_CONFIRMATION="<resolved-forbidden-scope-confirmation>"
PR_BODY_FILE="$(mktemp)"

test "${#HEAD_SHA}" -eq 40
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]]
test -f "$REPORT"

require_resolved_variables \
  REPO \
  PR \
  REPORT \
  HEAD_SHA \
  REVIEW_DATE \
  SCOPE_REVIEWED \
  CONDITIONS \
  FORBIDDEN_SCOPE_CONFIRMATION \
  PR_BODY_FILE

awk '
  /^## Red-Team Status$/ {
    skipping_section = 1
    next
  }

  /^## OWNER_TRIGGER_REVIEW marker$/ {
    skipping_section = 1
    next
  }

  skipping_section && /^## / {
    skipping_section = 0
  }

  !skipping_section {
    print
  }
' "$REPORT" > "$PR_BODY_FILE"

cat >> "$PR_BODY_FILE" <<EOF

## Red-Team Status

RED_TEAM_DECISION
PR number: #${PR}
PR head SHA: ${HEAD_SHA}
Decision: APPROVED
Reviewer role: External red-team reviewer
Review date: ${REVIEW_DATE}
Scope reviewed: ${SCOPE_REVIEWED}
Conditions: ${CONDITIONS}
Forbidden-scope confirmation: ${FORBIDDEN_SCOPE_CONFIRMATION}
SHA-bound statement: This decision applies only to the listed PR head SHA.

## OWNER_TRIGGER_REVIEW marker

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: Phase 4K-8 defines the canonical operator workflow, command sequence, role boundaries, marker handling, and future automation handoff controls. These operating rules affect future development-control architecture and automation execution safety, so owner interruption, external red-team review, and human approval are required. This phase must not activate automation, reduce current approval requirements, enable auto-merge, or authorize Phase 4K-9.
EOF

if grep -Eq '<[^>]+>' "$PR_BODY_FILE"; then
  echo "FAIL: unresolved placeholders remain in generated PR body."
  exit 1
fi

if grep -Fq 'External red-team review is pending' "$PR_BODY_FILE"; then
  echo "FAIL: stale pending red-team status remains in approved PR body."
  exit 1
fi

test "$(grep -c '^## Red-Team Status$' "$PR_BODY_FILE")" -eq 1
test "$(grep -c '^RED_TEAM_DECISION$' "$PR_BODY_FILE")" -eq 1
test "$(grep -c '^OWNER_TRIGGER_REVIEW$' "$PR_BODY_FILE")" -eq 1
test "$(grep -c '^## OWNER_TRIGGER_REVIEW marker$' "$PR_BODY_FILE")" -eq 1
grep -Fqx "PR head SHA: ${HEAD_SHA}" "$PR_BODY_FILE"

DECISION_LINE="$(grep -n '^RED_TEAM_DECISION$' "$PR_BODY_FILE" | cut -d: -f1)"
OWNER_LINE="$(grep -n '^OWNER_TRIGGER_REVIEW$' "$PR_BODY_FILE" | cut -d: -f1)"
test "$DECISION_LINE" -lt "$OWNER_LINE"
test "$(grep '^## ' "$PR_BODY_FILE" | tail -n 1)" = "## OWNER_TRIGGER_REVIEW marker"
test "$(awk 'NF { line=$0 } END { print line }' "$PR_BODY_FILE")" = "Rationale: Phase 4K-8 defines the canonical operator workflow, command sequence, role boundaries, marker handling, and future automation handoff controls. These operating rules affect future development-control architecture and automation execution safety, so owner interruption, external red-team review, and human approval are required. This phase must not activate automation, reduce current approval requirements, enable auto-merge, or authorize Phase 4K-9."

gh pr edit "$PR" \
  --repo "$REPO" \
  --body-file "$PR_BODY_FILE"
```

Do not execute this marker-write command during Phase 4K-8 implementation. Codex must not add red-team decision evidence.

## 8. Post-Marker Verification

```bash
gh pr view "$PR" --repo "$REPO" --json headRefOid,statusCheckRollup,reviewDecision,mergeStateStatus,autoMergeRequest
gh pr checks "$PR" --repo "$REPO" --required
gh run view "$RUN_ID" --repo "$REPO" --json status,conclusion,url,jobs
```

Success requires checks on the reviewed SHA, valid red-team marker, no later commit, human/write-access approval, inactive auto-merge, and a protected merge route. Stop on stale markers, failed checks, missing approval, moved head, or active auto-merge.

## 9. Manual Merge

Codex must never execute merge commands. A human/operator may merge only after durable verification that external SHA-bound red-team evidence is valid, required checks passed for `HEAD_SHA`, human/write-access review is approved, auto-merge request is null, and the merge state permits the protected route.

```bash
CURRENT_HEAD="$(
  gh pr view "$PR" \
    --repo "$REPO" \
    --json headRefOid \
    --jq '.headRefOid'
)"

test "$CURRENT_HEAD" = "$HEAD_SHA"

gh pr checks "$PR" \
  --repo "$REPO" \
  --required

gh pr merge "$PR" \
  --repo "$REPO" \
  --merge \
  --match-head-commit "$HEAD_SHA"
```

Stop if the repository uses a merge queue or protected route requiring a different human action. Omit or adapt `--merge` only when repository policy requires another permitted manual strategy. Do not use `--auto`, `--admin`, or any branch-protection bypass.

## 10. Post-Merge Verification

```bash
gh pr view "$PR" --repo "$REPO" --json state,mergedAt,mergeCommit,headRefOid,url
git fetch origin main # documentation source sync
git switch main
git pull --ff-only origin main
git rev-parse HEAD
git rev-parse origin/main
```

Success requires PR state `MERGED`, merge timestamp, merge commit equal to `MERGE_SHA`, and local main plus `origin/main` equal to `MERGE_SHA`. Stop if main does not match.

## 11. Issue Closeout

Closeout must include issue, PR, branch, starting SHA, reviewed head SHA, merge commit, verified main SHA, check result, review result, auto-merge status, completed scope, preserved boundaries, and next-phase status.

```bash
gh issue comment "$ACTIVE_ISSUE" --repo "$REPO" --body-file "$CLOSEOUT_FILE"
gh issue close "$ACTIVE_ISSUE" --repo "$REPO" --reason completed
gh issue view "$ACTIVE_ISSUE" --repo "$REPO" --json number,state,stateReason,closedAt,url
```

Stop if closeout evidence is incomplete or the issue closes before merge/main verification.
