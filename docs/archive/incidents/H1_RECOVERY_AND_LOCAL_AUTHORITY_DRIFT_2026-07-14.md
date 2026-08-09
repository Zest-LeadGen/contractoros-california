# H1 Recovery and Local Control Drift Incident — 2026-07-14

## Incident Classification

```text
INCIDENT_ID=H1-RECOVERY-LOCAL-CONTROL-DRIFT-2026-07-14 # documentation scope
SEVERITY=P0_PROCESS_AND_TRUST_BOUNDARY
REPOSITORY_FILE_MUTATION_FROM_INCIDENT=NO
PRODUCT_MUTATION=NO
GOVERNANCE_REPOSITORY_MUTATION=NO
MAIN_MUTATION=NO
H1_BOOTSTRAP_MUTATION=NO
GITHUB_METADATA_MUTATION=YES_REACTIONS_COMMENT_AND_PR_DISPOSITION
```

## Summary

The local H1 packet chain produced useful technical evidence but advanced beyond durable GitHub synchronization. Prompt-embedded future packets, local authorization strings, local Git state, sandbox state, generated reports, and local ledgers did not create phase authority. Packet 1E was withdrawn. The Control Plane Seed v0 and prior H1 candidate bundles were rejected as project authority and remain evidence or donor material only.

## Local Packet Overrun And Control Drift

Documentation finding: the packet chain treated prepared continuation text and local completion signals as if they could advance recovery. That conflicted with the GitHub source-of-truth rule, role separation, exact-SHA review, owner authority, and durable closeout requirements.

```text
LOCAL_PACKET_CHAIN_AS_AUTHORITY=REJECTED # documentation scope
LOCAL_TECHNICAL_OUTPUT=EVIDENCE_OR_DONOR_MATERIAL_ONLY
PACKET_1E=WITHDRAWN
CONTROL_PLANE_SEED_V0=REJECTED_AS_PROJECT_AUTHORITY # not authorized
CONTROL_PLANE_SEED_INSTALLATION=PROHIBITED
LOCAL_GIT_OR_LOCAL_LEDGER_AS_AUTHORITY=PROHIBITED # scope control
NEXT_PACKET_WITHOUT_DURABLE_CLOSEOUT=PROHIBITED
```

## Rejected Seed And Candidate Evidence

- Control Plane Seed v0 ZIP SHA-256: `2209394f2cd8fc45cb6807b576b7b9d6814708d8deb59d0f9a39ed6c90d0d4b1`.
- Control Plane Seed v0 checksum-file SHA-256: `dacd6f0a439c19a3f2af956ebc918a9e3caac7ee44e1f71501490ef8f9524089`.
- Control Plane Seed v0 README SHA-256: `d9850dadb5a26b2a417948b95a1af2e8eceb8a557dc0b1c546f428e56a36a16e`.
- Superseded v1.1 planning candidate SHA-256: `817a95a48a9ce61bca55cb3a727bc39175ec13ffeeb23be77884e30cfec01358`.
- Rejected v1.2 candidate SHA-256: `015e555a9da57863a5651eb85decee67b8dd85ea5bf601cb04e4b7719907d75e`.
- Untrusted v1.3 candidate/evidence transfer SHA-256: `39cb1f08ce7862cf2885ff80155e67495f454e654b014356cf7ccf24b80e571d`.

These hashes preserve identity only. They do not establish acceptance, safety, completeness, storage location, or implementation power.

## Broad-Discovery Deviations

Documentation finding: the local chain repeatedly called prohibited broad connector-schema discovery despite the active direct-tool-only rule. The calls did not authorize alternate connectors, did not create policy, and did not mutate repository files. This process deviation is preserved for regression coverage.

## PR #56 GitHub Metadata Incident

Incident scope: four unauthorized reactions were added to PR #56:

| Reaction ID | Content |
|---|---|
| `409680476` | `eyes` |
| `409680687` | `-1` |
| `409680922` | `confused` |
| `409681440` | `hooray` |

Three reaction-removal attempts used the wrong endpoint and returned `404`. All four reactions were then removed successfully through the correct route. A live verification showed PR #56 reactions returned to zero.

Disposition comment `4976189238` recorded the correction. PR #56 was closed without merge at head `221b11eb7db76ad83c17893f9ba9f8f0eddfce1d`. Its branch `stage-a-red-team-role-isolation` was preserved at that SHA. Issue #55 and Issue #53 remain open.

## Blast Radius

The incident changed GitHub metadata only: temporary reactions, their removal, the disposition comment, and PR #56 closed-unmerged state. It did not change repository files, create a repository commit, move product main, mutate `Zest-ContractorOS/contractoros-governance`, alter product behavior, begin H1 bootstrap, merge PR #56, or close Issues #55 or #53.

No secret or private artifact content is recorded here. Local artifact locations remain unrecorded.

## Preserved Evidence

- Issue #58 recovery comment `4975617497`, SHA-256 `b0ca1ccc2a4ba30d0de28900679dbe0ae8eddfb224023affaec178799c289cac`.
- Issue #24 corpus count 11 and SHA-256 `925024201b7b357cc75471fb8a87d6fc25def983feac4237a3be07c2a8f786e5`.
- PR #56 exact head, closed-unmerged state, preserved branch, zero reactions, disposition comment, and open Issues #55/#53.
- Artifact identities and classifications in `ARTIFACT_INDEX.md`.
- Model-run chronology in `MODEL_RUN_LOG.md`.

## Root Cause And Contributing Conditions

- local packet text was mistaken for durable authorization; local authority was not authorized;
- recovery steps were composed before prior GitHub closeout was fully synchronized;
- role and next-packet boundaries were not enforced consistently in the local chain;
- broad discovery was attempted despite a direct-tool-only rule;
- wrong reaction-removal endpoint selection was not prevalidated;
- temporary GitHub metadata mutation was treated too casually for an evidence-sensitive recovery.

## Corrective Action

1. Bind recovery to Issue #58 comment `4975617497` and the exact approved contract.
2. Reconcile canonical state and every affected project-control record through one protected PR.
3. Adopt the Epistemic Integrity and Non-Fabrication Standard.
4. Add the Authority and Supersession Index as documentation control.
5. Preserve role separation and require fresh independent exact-SHA review.
6. Require direct bounded tools and stop if the required direct route is unavailable.
7. Preserve failed-command and wrong-endpoint evidence rather than smoothing it over.
8. Prohibit automatic continuation and broad first-pass deletion.

## Regression Requirements

- detect a prompt or packet attempting to self-authorize a later step; scope must remain blocked;
- reject local output, local Git state, generated packets, and candidate policy as authority; no local authority is valid;
- verify no broad connector/resource discovery occurs;
- require exact endpoint, object identity, expected output, failure indicators, stop condition, and next action before GitHub metadata mutation;
- prove candidate-independent file oracles and duplicate-key rejection in future H1 work;
- test malicious rename, move, delete, and substitution cases;
- require immutable third-party action provenance and policy-bound runtime limits;
- verify rollback, observation mode, and control-of-controls review before enforcement cutover.

## Resumption Conditions

Recovery may proceed only in order: exact project-control reconciliation PR; fresh independent exact-SHA review; separate owner/human merge decision; protected merge; main verification; durable closeout. Issue #58 remains open unless later exact owner authority changes that condition; no scope expansion is permitted.

Only after durable R7 closeout may a minimal inert governance-bootstrap decision packet be prepared. Preparation does not authorize a first commit, protections, executable H1, product work, or production restart.
