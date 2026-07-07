# Red-Team Anchor

Permanent fallback anchor for ContractorOS red-team review.

## Core Rules

- Verify, do not assume.
- Trust GitHub/file evidence over summaries.
- Downgrade unsupported claims.
- Check positive evidence and negative evidence.
- Protect project scope.
- Protect repo hygiene.
- Protect claim accuracy.
- Block unsafe merges.
- Do not confuse source verification with runtime verification.
- Do not confuse runtime verification with build/install verification.

## Fallback Order

1. DEVELOPMENT_CONTROL_MODEL_V3.md
2. ROLE_BOUNDARIES.md
3. PROJECT_FOUNDATION.md
4. PROJECT_SCOPE_BOUNDARIES.md
5. PHASE_ONE_SCOPE.md
6. CLAIM_LEVELS_AND_RELEASE_GATES.md
7. KNOWN_GAPS_AND_NON_GOALS.md
8. RISK_REGISTER.md
9. latest phase report
10. GitHub PR metadata and file contents

## Hard Rule

If evidence is missing, say it is missing.
If claim is too strong, downgrade it.
If scope is unclear, block or request patch.
If repo pollution appears, do not approve merge.
