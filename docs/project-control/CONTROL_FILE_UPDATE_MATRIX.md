# Control File Update Matrix

## Purpose

This document explains when ContractorOS project-control files must be updated and when a file may be marked `reviewed, no update required`.

The machine-readable companion file is `docs/project-control/control-file-update-matrix.yml`.

## General Rule

Every PR must declare documentation impact. No paperwork impact means a documented no-op, not silence.

## When Each Control File Must Be Updated

| Control file | Update when |
|---|---|
| `DEVELOPMENT_LEDGER.md` | A phase opens, patches, merges, or changes verified state. |
| `RISK_REGISTER.md` | A new risk appears, an active risk changes, or a risk is resolved by evidence. |
| `DECISION_LOG.md` | A durable architecture, process, scope, or source-of-truth decision changes. |
| `ARTIFACT_INDEX.md` | A ZIP, binary, build artifact, Drive artifact, or archive/reference artifact is created or moved. |
| `PROJECT_SCOPE_BOUNDARIES.md` | Current approved scope, blocked scope, or future scope changes. |
| `KNOWN_GAPS_AND_NON_GOALS.md` | Known gaps are added, resolved, or reclassified. |
| `CLAIM_LEVELS_AND_RELEASE_GATES.md` | Claim level definitions, gate definitions, or release claims change. |
| `PROJECT_VISION_AND_PHASE_TRACKER.md` | Original vision, phase map, gate status, or source-of-truth hierarchy changes. |
| `PROJECT_IMPLEMENTATION_ROADMAP.md` | Long-term architecture, module strategy, or future implementation sequencing changes. |

## Reviewed, No Update Required

A required file may be left unchanged only when the phase report states `<file path>: reviewed, no update required`.

## Required Updates By Event Type

### App/mobile
Phase report, forbidden-scope scan, lockfile absence, QA evidence, and Documentation Impact section are required.

### Project-control
Decision/risk/ledger impact must be declared. Red-team docs cannot be treated as product scope.

### Dependency
Dependency lane, risk register update, lockfile provenance check, vulnerability status, and dependency/lockfile handling are required.

### Build/native
Build/distribution lane, claim-level gate, artifact index update, build evidence, and install/distribution limits are required.

### Backend/content
Explicit approval, scope boundary update, risk register update, decision log update, and content/currentness limits are required.

### Artifact
Artifact index update, GitHub source equivalent, and Drive ID or URL when Drive is used are required.

### Release
Claim/release gate review, risk register, known gaps/non-goals, and owner approval evidence are required.

## Examples

If `apps/mobile/App.js` changes, update or review the phase report, risk register, development ledger, claim level, and lockfile handling.

If `docs/project-control/**` changes, update or review the decision log, risk register, and ledger.

If `package.json` or a lockfile changes, update risk register, dependency handling report, and lockfile provenance evidence.

If `android/**`, `ios/**`, or `eas.json` appears, update artifact index, claim level, risk register, and build/install limitations.
