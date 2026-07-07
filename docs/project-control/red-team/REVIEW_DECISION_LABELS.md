# Review Decision Labels

Purpose: standard decision vocabulary for red-team reviews.

## VERIFIED / ACCEPTABLE FOR MERGE

Meaning: Evidence supports merge within approved scope.
Minimum evidence: PR metadata, file list, file inspection, and negative-scope check.
Allowed next action: Owner may authorize merge.

## PARTIAL / NEEDS PATCH

Meaning: Work is partly acceptable but requires a focused patch.
Minimum evidence: Specific blocker identified.
Allowed next action: Developer patches only the blocker.

## DO NOT MERGE

Meaning: PR is not acceptable for merge.
Minimum evidence: Missing evidence, scope issue, or unresolved blocker.
Allowed next action: Patch or stop.

## BLOCKED

Meaning: Work cannot proceed until required evidence or authorization exists.
Minimum evidence: Missing approval or unresolved safety/scope issue.
Allowed next action: Resolve blocker.

## ALLOWED FOR NEXT PHASE

Meaning: Prior phase is merged and main is verified.
Minimum evidence: Main verification record.
Allowed next action: Owner may authorize next phase.

## MERGE VERIFIED

Meaning: PR is closed, merged, and main verification passed.
Minimum evidence: PR merged status, merge SHA, timestamp, and main file checks.
Allowed next action: Record verified state.

## MAIN VERIFICATION FAILED

Meaning: Post-merge checks did not match expected state.
Minimum evidence: Specific missing/extra file or claim mismatch.
Allowed next action: Patch or revert plan.

## CLAIM OVERSTATED / DOWNGRADED

Meaning: Claim exceeds evidence.
Minimum evidence: Claim/evidence mismatch.
Allowed next action: Replace with lower claim level.

## SOURCE VERIFIED ONLY

Meaning: Source supports the claim but runtime has not been proven.
Minimum evidence: Source/file inspection.
Allowed next action: Command or runtime QA if approved.

## COMMAND VERIFIED ONLY

Meaning: Command output supports the claim but visual/build/install evidence is absent.
Minimum evidence: Command output.
Allowed next action: Visual or build gate if approved.

## RUNTIME VISUAL QA VERIFIED

Meaning: UI was observed in a runtime target.
Minimum evidence: Target, observation, and limitations.
Allowed next action: Build gate if approved.

## BUILD ARTIFACT VERIFIED

Meaning: Approved build artifact exists.
Minimum evidence: Artifact ID/path and build evidence.
Allowed next action: Install gate if approved.

## INSTALL VERIFIED

Meaning: Artifact was installed in an approved target.
Minimum evidence: Target, method, result, and artifact reference.
Allowed next action: Release gate if approved.
