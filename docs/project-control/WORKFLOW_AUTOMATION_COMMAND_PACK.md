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

require_safe_marker_values() {
  local variable_name
  local variable_value
  local reserved_label
  local heading_pattern='^[[:space:]]*#{1,6}[[:space:]]'
  local reserved_labels=(
    "PR number:"
    "PR head SHA:"
    "Decision:"
    "Reviewer role:"
    "Review date:"
    "Scope reviewed:"
    "Conditions:"
    "Forbidden-scope confirmation:"
    "SHA-bound statement:"
  )

  for variable_name in "$@"; do
    variable_value="${!variable_name-}"

    if [[ -z "$variable_value" ]]; then
      echo "FAIL: marker value $variable_name is empty or unset."
      return 1
    fi

    if [[ "$variable_value" == *$'\r'* || "$variable_value" == *$'\n'* ]]; then
      echo "FAIL: marker value $variable_name must be one line."
      return 1
    fi

    if [[ "$variable_value" == *"<"* || "$variable_value" == *">"* ]]; then
      echo "FAIL: marker value $variable_name contains placeholder brackets."
      return 1
    fi

    if [[ "$variable_value" == *"RED_TEAM_DECISION"* || "$variable_value" == *"OWNER_TRIGGER_REVIEW"* ]]; then
      echo "FAIL: marker value $variable_name contains a reserved marker token."
      return 1
    fi

    if [[ "$variable_value" =~ $heading_pattern ]]; then
      echo "FAIL: marker value $variable_name contains a Markdown section heading."
      return 1
    fi

    for reserved_label in "${reserved_labels[@]}"; do
      if [[ "$variable_value" == *"$reserved_label"* ]]; then
        echo "FAIL: marker value $variable_name contains reserved field label $reserved_label"
        return 1
      fi
    done
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
set -euo pipefail

START_SHA="<start_sha>"

require_resolved_variables START_SHA
[[ "$START_SHA" =~ ^[0-9a-f]{40}$ ]]

test -z "$(git status --porcelain=v1)"

git fetch origin main # documentation source sync
git switch main

test -z "$(git status --porcelain=v1)"
test "$(git branch --show-current)" = "main"
test "$(git rev-parse HEAD)" = "$START_SHA"
test "$(git rev-parse origin/main)" = "$START_SHA"
git remote get-url origin
gh issue view "$PRIOR_ISSUE" --repo "$REPO" --json number,title,state,stateReason,closedAt,url
gh pr view "$PRIOR_PR" --repo "$REPO" --json number,state,mergedAt,mergeCommit,headRefOid,url
gh issue view "$ACTIVE_ISSUE" --repo "$REPO" --json number,title,state,stateReason,url
```

Success: the worktree is clean before and after the fetch/switch, main and `origin/main` equal the exact starting SHA, the prior issue is `CLOSED` / `COMPLETED`, the prior PR is `MERGED`, the active issue is `OPEN`, and remote identity matches `REPO`. Do not use `git pull` during initial evidence verification. If local main and `origin/main` differ, stop for a separately controlled recovery step.

## 2. Branch Preparation

```bash
test -z "$(git status --porcelain=v1)"
test "$(git branch --show-current)" = "main"
test "$(git rev-parse HEAD)" = "$START_SHA"
test "$(git rev-parse origin/main)" = "$START_SHA"
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

require_safe_marker_values \
  PR \
  HEAD_SHA \
  REVIEW_DATE \
  SCOPE_REVIEWED \
  CONDITIONS \
  FORBIDDEN_SCOPE_CONFIRMATION

[[ "$PR" =~ ^[0-9]+$ ]]
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]]
[[ "$REVIEW_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]

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

if grep -Fq 'requires corrections' "$PR_BODY_FILE"; then
  echo "FAIL: stale changes-required lifecycle text remains in approved PR body."
  exit 1
fi

test "$(grep -c '^## Red-Team Status$' "$PR_BODY_FILE")" -eq 1
test "$(grep -c '^RED_TEAM_DECISION$' "$PR_BODY_FILE")" -eq 1
test "$(grep -c '^OWNER_TRIGGER_REVIEW$' "$PR_BODY_FILE")" -eq 1
test "$(grep -c '^## OWNER_TRIGGER_REVIEW marker$' "$PR_BODY_FILE")" -eq 1
grep -Fqx "PR head SHA: ${HEAD_SHA}" "$PR_BODY_FILE"

DECISION_FIELDS_FILE="$(mktemp)"
awk '
  /^RED_TEAM_DECISION$/ {
    in_decision = 1
    next
  }

  in_decision && /^## OWNER_TRIGGER_REVIEW marker$/ {
    exit
  }

  in_decision && NF {
    print
  }
' "$PR_BODY_FILE" > "$DECISION_FIELDS_FILE"

test "$(wc -l < "$DECISION_FIELDS_FILE" | tr -d ' ')" -eq 9

DECISION_FIELD_LABELS=(
  "PR number"
  "PR head SHA"
  "Decision"
  "Reviewer role"
  "Review date"
  "Scope reviewed"
  "Conditions"
  "Forbidden-scope confirmation"
  "SHA-bound statement"
)

for field_label in "${DECISION_FIELD_LABELS[@]}"; do
  test "$(grep -c "^${field_label}: " "$DECISION_FIELDS_FILE")" -eq 1
done

while IFS= read -r decision_field; do
  case "$decision_field" in
    "PR number: #"*|\
    "PR head SHA: "*|\
    "Decision: "*|\
    "Reviewer role: "*|\
    "Review date: "*|\
    "Scope reviewed: "*|\
    "Conditions: "*|\
    "Forbidden-scope confirmation: "*|\
    "SHA-bound statement: "*)
      ;;
    *)
      echo "FAIL: unknown decision field: $decision_field"
      exit 1
      ;;
  esac
done < "$DECISION_FIELDS_FILE"

DECISION_LINE="$(grep -n '^RED_TEAM_DECISION$' "$PR_BODY_FILE" | cut -d: -f1)"
OWNER_LINE="$(grep -n '^OWNER_TRIGGER_REVIEW$' "$PR_BODY_FILE" | cut -d: -f1)"
test "$DECISION_LINE" -lt "$OWNER_LINE"
test "$(grep '^## ' "$PR_BODY_FILE" | tail -n 1)" = "## OWNER_TRIGGER_REVIEW marker"
test "$(awk 'NF { line=$0 } END { print line }' "$PR_BODY_FILE")" = "Rationale: Phase 4K-8 defines the canonical operator workflow, command sequence, role boundaries, marker handling, and future automation handoff controls. These operating rules affect future development-control architecture and automation execution safety, so owner interruption, external red-team review, and human approval are required. This phase must not activate automation, reduce current approval requirements, enable auto-merge, or authorize Phase 4K-9."

CURRENT_HEAD="$(
  gh pr view "$PR" \
    --repo "$REPO" \
    --json headRefOid \
    --jq '.headRefOid'
)"

test "$CURRENT_HEAD" = "$HEAD_SHA"

gh pr edit "$PR" \
  --repo "$REPO" \
  --body-file "$PR_BODY_FILE"
```

Do not execute this marker-write command during Phase 4K-8 implementation. Codex must not add red-team decision evidence.

## No-Write Marker And Replacement-Body Adversarial Test Suite

Run this suite before any marker write. It obtains the current PR head through read-only GitHub metadata, creates files only under a temporary directory, and compares the repository status before and after execution. It contains no GitHub write command and no repository write command. Every invalid case must be rejected; acceptance of any invalid case stops the suite.

```bash
set -euo pipefail

REPO="Zest-LeadGen/contractoros-california"
PR="46"
TEST_TMP="$(mktemp -d)"
trap 'rm -rf "$TEST_TMP"' EXIT
STATUS_BEFORE="$(git status --porcelain=v1)"

LIVE_HEAD="$(
  gh pr view "$PR" \
    --repo "$REPO" \
    --json headRefOid \
    --jq '.headRefOid'
)"

REVIEW_DATE="2026-07-11"
SCOPE_REVIEWED="Phase 4K-8 documentation-only correction."
CONDITIONS="None."
FORBIDDEN_SCOPE_CONFIRMATION="Confirmed documentation-only scope."
OWNER_RATIONALE="Phase 4K-8 remains documentation-only and requires owner interruption, external red-team review, and human approval."

validate_marker_value() {
  local value="$1"
  local label
  local reserved_labels=(
    "PR number:"
    "PR head SHA:"
    "Decision:"
    "Reviewer role:"
    "Review date:"
    "Scope reviewed:"
    "Conditions:"
    "Forbidden-scope confirmation:"
    "SHA-bound statement:"
  )

  [[ -n "$value" ]] || return 1
  [[ "$value" != *$'\r'* ]] || return 1
  [[ "$value" != *$'\n'* ]] || return 1
  [[ "$value" != *"<"* ]] || return 1
  [[ "$value" != *">"* ]] || return 1
  [[ "$value" != *"RED_TEAM_DECISION"* ]] || return 1
  [[ "$value" != *"OWNER_TRIGGER_REVIEW"* ]] || return 1
  [[ ! "$value" =~ ^[[:space:]]*#{1,6}[[:space:]] ]] || return 1

  for label in "${reserved_labels[@]}"; do
    [[ "$value" != *"$label"* ]] || return 1
  done

  return 0
}

validate_review_inputs() {
  [[ "$PR" =~ ^[0-9]+$ ]] || return 1
  [[ "$LIVE_HEAD" =~ ^[0-9a-f]{40}$ ]] || return 1
  [[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || return 1
  [[ "$HEAD_SHA" = "$LIVE_HEAD" ]] || return 1
  [[ "$REVIEW_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || return 1
  validate_marker_value "$SCOPE_REVIEWED" || return 1
  validate_marker_value "$CONDITIONS" || return 1
  validate_marker_value "$FORBIDDEN_SCOPE_CONFIRMATION" || return 1
  return 0
}

write_decision_section() {
  cat <<EOF
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
EOF
}

write_owner_section() {
  cat <<EOF
## OWNER_TRIGGER_REVIEW marker

OWNER_TRIGGER_REVIEW
Owner interruption required: YES
Trigger categories: ARCHITECTURE_THRESHOLD
Lane eligibility: NOT_AUTOMATION_ELIGIBLE
Human approval required: YES
Auto-merge eligible: NO
Rationale: ${OWNER_RATIONALE}
EOF
}

build_valid_body() {
  local body_file="$1"
  {
    printf '%s\n\n' 'Context: harmless colon-delimited prose outside the decision block.'
    write_decision_section
    printf '\n'
    write_owner_section
  } > "$body_file"
}

build_reversed_body() {
  local body_file="$1"
  {
    printf '%s\n\n' 'Context: harmless colon-delimited prose outside the decision block.'
    write_owner_section
    printf '\n'
    write_decision_section
  } > "$body_file"
}

validate_generated_body() {
  local body_file="$1"
  local fields_file="$TEST_TMP/decision-fields"
  local field_label
  local decision_field
  local decision_line
  local owner_line

  ! grep -Eq '<[^>]+>' "$body_file" || return 1
  ! grep -Fiq 'requires corrections' "$body_file" || return 1
  [[ "$(grep -c '^RED_TEAM_DECISION$' "$body_file")" -eq 1 ]] || return 1
  [[ "$(grep -c '^OWNER_TRIGGER_REVIEW$' "$body_file")" -eq 1 ]] || return 1
  [[ "$(grep -c '^## OWNER_TRIGGER_REVIEW marker$' "$body_file")" -eq 1 ]] || return 1
  grep -Eq '^PR number: #[0-9]+$' "$body_file" || return 1
  grep -Eq '^PR head SHA: [0-9a-f]{40}$' "$body_file" || return 1
  grep -Fqx "PR head SHA: ${LIVE_HEAD}" "$body_file" || return 1
  grep -Fqx 'Decision: APPROVED' "$body_file" || return 1
  grep -Eq '^Review date: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$body_file" || return 1
  grep -Fqx 'SHA-bound statement: This decision applies only to the listed PR head SHA.' "$body_file" || return 1

  awk '
    /^RED_TEAM_DECISION$/ { in_decision = 1; next }
    in_decision && /^## OWNER_TRIGGER_REVIEW marker$/ { exit }
    in_decision && NF { print }
  ' "$body_file" > "$fields_file" || return 1

  [[ "$(wc -l < "$fields_file" | tr -d ' ')" -eq 9 ]] || return 1

  for field_label in \
    "PR number" \
    "PR head SHA" \
    "Decision" \
    "Reviewer role" \
    "Review date" \
    "Scope reviewed" \
    "Conditions" \
    "Forbidden-scope confirmation" \
    "SHA-bound statement"; do
    [[ "$(grep -c "^${field_label}: " "$fields_file")" -eq 1 ]] || return 1
  done

  while IFS= read -r decision_field; do
    case "$decision_field" in
      "PR number: #"*|\
      "PR head SHA: "*|\
      "Decision: "*|\
      "Reviewer role: "*|\
      "Review date: "*|\
      "Scope reviewed: "*|\
      "Conditions: "*|\
      "Forbidden-scope confirmation: "*|\
      "SHA-bound statement: "*)
        ;;
      *)
        return 1
        ;;
    esac
  done < "$fields_file"

  decision_line="$(grep -n '^RED_TEAM_DECISION$' "$body_file" | cut -d: -f1)" || return 1
  owner_line="$(grep -n '^OWNER_TRIGGER_REVIEW$' "$body_file" | cut -d: -f1)" || return 1
  [[ "$decision_line" -lt "$owner_line" ]] || return 1
  [[ "$(grep '^## ' "$body_file" | tail -n 1)" = '## OWNER_TRIGGER_REVIEW marker' ]] || return 1
  [[ "$(awk 'NF { line=$0 } END { print line }' "$body_file")" = "Rationale: ${OWNER_RATIONALE}" ]] || return 1
  return 0
}

run_input_case() {
  local variable_name="$1"
  local invalid_value="$2"
  printf -v "$variable_name" '%s' "$invalid_value" || return 1
  validate_review_inputs || return 1
  return 0
}

run_body_case() {
  local mutation="$1"
  local body_file="$TEST_TMP/invalid-body"
  local valid_file="$TEST_TMP/valid-source"

  build_valid_body "$valid_file" || return 1
  case "$mutation" in
    duplicate_field)
      awk '/^Conditions: / { print } { print }' "$valid_file" > "$body_file" || return 1
      ;;
    unknown_field)
      awk '/^Conditions: / { print "Unexpected field: injected" } { print }' "$valid_file" > "$body_file" || return 1
      ;;
    placeholder)
      sed 's/^Scope reviewed: .*/Scope reviewed: <unresolved-scope>/' "$valid_file" > "$body_file" || return 1
      ;;
    stale_text)
      { printf '%s\n' 'External red-team review requires corrections.'; cat "$valid_file"; } > "$body_file" || return 1
      ;;
    duplicate_decision)
      awk '/^RED_TEAM_DECISION$/ { print } { print }' "$valid_file" > "$body_file" || return 1
      ;;
    duplicate_owner)
      { cat "$valid_file"; printf '%s\n' 'OWNER_TRIGGER_REVIEW'; } > "$body_file" || return 1
      ;;
    owner_not_final)
      { cat "$valid_file"; printf '%s\n' 'Trailing text is forbidden.'; } > "$body_file" || return 1
      ;;
    decision_after_owner)
      build_reversed_body "$body_file" || return 1
      ;;
    *)
      return 2
      ;;
  esac
  validate_generated_body "$body_file" || return 1
  return 0
}

harness_early_failure_control() {
  [[ 1 -eq 2 ]] || return 1
  [[ 1 -eq 1 ]] || return 1
  return 0
}

expect_reject() {
  local test_id="$1"
  local condition="$2"
  shift 2
  if ( "$@" ); then
    printf '%s|%s|EXPECTED=REJECT|OBSERVED=ACCEPT|FAIL\n' "$test_id" "$condition"
    return 1
  fi
  printf '%s|%s|EXPECTED=REJECT|OBSERVED=REJECT|PASS|NO_GITHUB_WRITE=YES|NO_REPO_MUTATION=YES|NO_LIVE_RED_TEAM_DECISION_ADDED=YES\n' "$test_id" "$condition"
}

HEAD_SHA="$LIVE_HEAD"
validate_review_inputs || exit 1
VALID_BODY="$TEST_TMP/valid-body"
build_valid_body "$VALID_BODY" || exit 1

if harness_early_failure_control; then
  printf '%s\n' 'HARNESS|early failure cannot be masked by later success|FAIL'
  exit 1
fi
printf '%s\n' 'HARNESS|early failure cannot be masked by later success|PASS|NO_GITHUB_WRITE=YES|NO_REPO_MUTATION=YES|NO_LIVE_RED_TEAM_DECISION_ADDED=YES'

expect_reject T01 'multiline CONDITIONS' run_input_case CONDITIONS $'First line\nSecond line'
expect_reject T02 'CONDITIONS contains Decision: BLOCKED' run_input_case CONDITIONS 'Decision: BLOCKED'
expect_reject T03 'SCOPE_REVIEWED contains RED_TEAM_DECISION' run_input_case SCOPE_REVIEWED 'Scope RED_TEAM_DECISION injection'
expect_reject T04 'FORBIDDEN_SCOPE_CONFIRMATION contains OWNER_TRIGGER_REVIEW' run_input_case FORBIDDEN_SCOPE_CONFIRMATION 'OWNER_TRIGGER_REVIEW injected'
expect_reject T05 'Markdown heading injection' run_input_case SCOPE_REVIEWED '## Injected heading'
expect_reject T06 'invalid review-date format' run_input_case REVIEW_DATE '07/11/2026'
expect_reject T07 'short SHA' run_input_case HEAD_SHA 'abc123'
expect_reject T08A 'uppercase SHA' run_input_case HEAD_SHA '87D0378EE933596A9FFE0303902A7D56BF4BA8E5'
expect_reject T08B 'non-hex SHA' run_input_case HEAD_SHA 'gggggggggggggggggggggggggggggggggggggggg'
expect_reject T09 'wrong SHA versus live PR head' run_input_case HEAD_SHA '0000000000000000000000000000000000000000'
expect_reject T10 'duplicate supported decision field' run_body_case duplicate_field
expect_reject T11 'unknown colon-delimited decision field' run_body_case unknown_field
expect_reject T12 'unresolved runtime placeholder' run_body_case placeholder
expect_reject T13 'stale requires corrections text' run_body_case stale_text
expect_reject T14 'duplicate RED_TEAM_DECISION' run_body_case duplicate_decision
expect_reject T15 'duplicate owner marker' run_body_case duplicate_owner
expect_reject T16 'owner marker not final' run_body_case owner_not_final
expect_reject T17 'decision marker after owner marker' run_body_case decision_after_owner

validate_generated_body "$VALID_BODY" || exit 1
printf '%s\n' 'VALID|live-head complete control body|EXPECTED=ACCEPT|OBSERVED=ACCEPT|PASS|NO_GITHUB_WRITE=YES|NO_REPO_MUTATION=YES|NO_LIVE_RED_TEAM_DECISION_ADDED=YES'

STATUS_AFTER="$(git status --porcelain=v1)"
[[ "$STATUS_AFTER" = "$STATUS_BEFORE" ]] || exit 1
printf '%s\n' 'SUITE|repository status unchanged|PASS' 'SUITE|GitHub operations read-only|PASS' 'SUITE|no live RED_TEAM_DECISION added|PASS'
```

Expected output is one `PASS` row for each `T01` through `T17` case (including both `T08A` and `T08B`), one valid-control `PASS`, and three final suite confirmations. The temporary files are removed on exit. Do not run any PR-body write from this suite.

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
