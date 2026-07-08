# PR Review Checklist

Purpose: step-by-step red-team PR review checklist.

## Checklist

1. Verify PR URL and number.
2. Verify state/open/closed.
3. Verify merged true/false.
4. Verify base branch and base SHA.
5. Verify head branch and head SHA.
6. Verify changed file count.
7. List changed filenames.
8. Compare changed files to allowed file list.
9. Inspect each changed file.
10. Check app source if app source changed.
11. Check reports for durable evidence.
12. Check commands and outputs.
13. Check dependency/lockfile handling.
14. Check forbidden-scope scan.
15. Check known risks.
16. Check claim level.
17. Check whether next phase was started.
18. Classify decision.

## Decision Outputs

- ACCEPTABLE FOR MERGE
- PARTIAL / NEEDS PATCH
- DO NOT MERGE
- BLOCKED
- CLAIM OVERSTATED / DOWNGRADED

## Output Rule

Every review must state evidence, limitation, and next allowed step.
