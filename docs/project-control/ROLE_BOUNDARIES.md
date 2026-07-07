# Role Boundaries

## 1. Purpose

Define clear role separation between the project owner, developer, red-team reviewer, and shared project-control files.

## 2. Project Owner Role

The project owner authorizes scope changes, merge decisions, and phase advancement.

## 3. Developer Role

The developer implements approved milestone scope only and must provide evidence for every claim.

## 4. Red-Team Reviewer Role

Red-team verifies evidence, downgrades unsupported claims, checks negative scope, and blocks unsafe merges.

## 5. Shared Project-Control Files

Shared files define project truth. Role files define execution responsibilities.

## 6. Developer-Facing Files

Developer-facing files include approved milestone prompts, scoped reports, and source/control files needed to complete assigned work.

## 7. Red-Team Files

Red-team files are reviewer/control files. They do not define product scope and do not authorize developer implementation work.

## 8. What Developers May Do

- Implement approved milestone scope only.
- Update approved files in the approved branch.
- Provide evidence, limitations, and negative-scope confirmations.
- Edit red-team files only when explicitly approved in a control/infrastructure milestone.

## 9. What Developers Must Not Do

- Treat red-team files as build instructions or product scope.
- Expand scope without project-owner approval.
- Edit red-team files outside approved control/infrastructure work.
- Claim readiness beyond evidence.

## 10. What Red-Team May Do

- Verify GitHub/file evidence.
- Downgrade unsupported claims.
- Check positive and negative evidence.
- Request patches or block unsafe merges.

## 11. What Red-Team Must Not Do

- Invent requirements outside approved owner/project-control scope.
- Approve a merge when evidence is missing.
- Convert reviewer guidance into product implementation scope.

## 12. Conflict Resolution

When role instructions conflict, use this order: project-owner authorization, GitHub/file evidence, development-control model, project foundation, scope boundaries, current phase report.

Because these files are stored in the same GitHub repository, they are visible to repository participants. Separation is role-based and process-based, not secrecy-based. Truly private red-team notes require a separate access-controlled location.
