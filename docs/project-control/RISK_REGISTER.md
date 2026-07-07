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

### no visual/device QA yet

```text
Risk: no visual/device QA yet
Status: Active
Evidence: Runtime QA reached Metro locally but did not visually inspect a device or emulator.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved device or emulator visual QA is completed and documented.
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

### no CI automation yet

```text
Risk: no CI automation yet
Status: Active
Evidence: Current checks are manual report/red-team gates.
Owner: ContractorOS development lead / red-team gate
Resolution condition: Approved CI validates forbidden files, dependency policy, and smoke checks.
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
