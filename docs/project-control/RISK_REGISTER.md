# ContractorOS Risk Register

Purpose: track active risks until evidence proves they are resolved.

Template:

```text
Risk:
Status:
Evidence:
Owner:
Resolution condition:
Last reviewed:
```

## Active Risks

### dependencies use latest

```text
Risk: dependencies use latest
Status: Active
Evidence: apps/mobile/package.json uses latest for expo, react, and react-native.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Dependencies are pinned or otherwise controlled under an approved reproducibility plan.
Last reviewed: 2026-07-07
```

### no clean public npm lockfile

```text
Risk: no clean public npm lockfile
Status: Active
Evidence: Phase reports document no committed clean public npm lockfile for apps/mobile.
Owner: ContractorOS development lead / red-team gate
Resolution condition: A clean public npm lockfile is generated and verified before commit.
Last reviewed: 2026-07-07
```

### contaminated lockfiles generated locally

```text
Risk: contaminated lockfiles generated locally
Status: Active
Evidence: Prior local npm installs produced lockfiles with non-public registry references.
Owner: ContractorOS development lead / red-team gate
Resolution condition: No non-public registry reference appears in any committed lockfile.
Last reviewed: 2026-07-07
```

### 10 moderate npm vulnerabilities reported during mobile npm install

```text
Risk: 10 moderate npm vulnerabilities reported during mobile npm install
Status: Active
Evidence: Phase 4C and Phase 4D reports document npm audit output.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Dedicated dependency triage phase resolves or accepts the risk with evidence.
Last reviewed: 2026-07-07
```

### visual/device QA not yet complete

```text
Risk: visual/device QA not yet complete
Status: Active
Evidence: Runtime QA reached Metro locally but did not visually inspect a device or emulator.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved visual QA is completed and documented.
Last reviewed: 2026-07-07
```

### no APK build yet

```text
Risk: no APK build yet
Status: Active
Evidence: Prior phase reports explicitly exclude APK creation.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved Android build phase creates and verifies an APK.
Last reviewed: 2026-07-07
```

### no install test yet

```text
Risk: no install test yet
Status: Active
Evidence: No Android install test has been completed.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved install test is completed and documented.
Last reviewed: 2026-07-07
```

### CI automation not yet implemented

```text
Risk: CI automation not yet implemented
Status: Active
Evidence: Current checks are manual report/red-team gates.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved CI validates boundaries, dependency policy, and smoke checks.
Last reviewed: 2026-07-07
```

### no full content system

```text
Risk: no full content system
Status: Active
Evidence: Current mobile app uses a minimal internal fixture placeholder only.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved content system architecture and implementation are completed.
Last reviewed: 2026-07-07
```

### no production/public MVP claim allowed

```text
Risk: no production/public MVP claim allowed
Status: Active
Evidence: Current work is internal-only and fixture-only.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Production/public MVP readiness is explicitly approved after required gates.
Last reviewed: 2026-07-07
```

### foundation scope file newly added but must remain living document

```text
Risk: foundation scope file newly added but must remain living document
Status: Active
Evidence: PROJECT_FOUNDATION.md is a control document, not implementation proof.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Foundation file remains updated as project evidence changes.
Last reviewed: 2026-07-07
```

### Phase One acceptance not yet achieved

```text
Risk: Phase One acceptance not yet achieved
Status: Active
Evidence: Acceptance criteria now exist, but evidence for all levels has not been completed.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Required acceptance levels are verified and documented.
Last reviewed: 2026-07-07
```

### release gates not yet passed

```text
Risk: release gates not yet passed
Status: Active
Evidence: Claim/release gates are defined but not completed.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Relevant gates are passed with evidence.
Last reviewed: 2026-07-07
```

### full project scope beyond Phase One remains future/controlled, not implemented

```text
Risk: full project scope beyond Phase One remains future/controlled, not implemented
Status: Active
Evidence: PROJECT_FOUNDATION.md lists long-term categories as not necessarily implemented.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Each future scope area is separately approved, implemented, and verified.
Last reviewed: 2026-07-07
```

### red-team files are visible in the same repo and could be misread as developer scope

```text
Risk: red-team files are visible in the same repo and could be misread as developer scope.
Status: Active / Controlled
Evidence: Red-team files are committed for auditability in GitHub.
Owner: ContractorOS development lead / red-team gate
Resolution condition: ROLE_BOUNDARIES.md and red-team README clearly mark them as reviewer/control files; developer must not treat them as implementation scope.
Last reviewed: 2026-07-07
```
