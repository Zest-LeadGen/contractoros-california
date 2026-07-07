# Red-Team Reviewer Files

This folder contains reviewer/control execution files.

It is not developer implementation scope.

It is not product feature scope.

It does not authorize new app functionality.

It supports verification, claim downgrade, repo hygiene, and recovery.

## Files

- `RED_TEAM_ANCHOR.md` — fallback reviewer anchor and evidence order.
- `PR_REVIEW_CHECKLIST.md` — step-by-step PR review checklist.
- `MAIN_VERIFICATION_CHECKLIST.md` — post-merge main verification checklist.
- `CLAIM_DOWNGRADE_MATRIX.md` — claim/evidence downgrade guide.
- `FORBIDDEN_SCOPE_SCAN_PLAYBOOK.md` — negative-scope scans and forbidden path checks.
- `RECOVERY_PLAYBOOK.md` — recovery steps when evidence is unclear or project drift appears.
- `REVIEW_DECISION_LABELS.md` — standard decision vocabulary.
- `RED_TEAM_HANDOFF_TEMPLATE.md` — standard red-team response format.

## Role Boundary

These files are visible in GitHub for durability and auditability. Developers must not treat them as product scope or build instructions unless explicitly approved in a control/infrastructure milestone.
