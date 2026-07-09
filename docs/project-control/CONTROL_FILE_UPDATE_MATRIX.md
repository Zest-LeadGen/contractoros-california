# Control File Update Matrix

## Purpose

This document explains when ContractorOS project-control files must be updated and when a file may be marked `reviewed, no update required`.

Machine-readable companion file:

```text
docs/project-control/control-file-update-matrix.yml
```

## General Rule

Every PR must declare documentation impact. No paperwork impact means a documented no-op, not silence.

## Companion Phase Report Rule

A Product / QA PR may include exactly one current phase report under:

```text
docs/project-control/phase_*_report.md
```

That report is a **companion phase report** for the declared Product / QA lane. It does not convert the PR lane to Control / Infrastructure.

The companion report must still:

- be the only changed `phase_*_report.md` file in the PR;
- contain the required report sections for the non-control lane;
- contain exact `reviewed, no update required` markers for required control files that are not changed;
- preserve forbidden-scope confirmations;
- avoid production, public, exam-ready, build-ready, release-ready, scoring, readiness, or pass/fail claims unless separately approved by the relevant gate.

Report-only `docs/project-control/**` PRs remain Control / Infrastructure.

Non-report `docs/project-control/**` changes remain Control / Infrastructure.

A Product / QA PR may not use this companion-report rule to include unrelated project-control edits.

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

A required file may be left unchanged only when the current phase report states:

```text
<file path>: reviewed, no update required
```

Historical phase reports do not satisfy the current PR requirement.

## Required Updates By Event Type

### App/mobile

A phase report, forbidden-scope scan, lockfile absence, QA evidence, Documentation Impact section, and required no-update markers are required.

The current phase report may accompany the app/mobile change as documentation for the Product / QA lane.

### App/web

A phase report, forbidden-scope scan, QA evidence, Documentation Impact section, and required no-update markers are required.

The current phase report may accompany the app/web change as documentation for the Product / QA lane.

### Project-control

Decision/risk/ledger impact must be declared. Red-team docs cannot be treated as product scope.

Report-only project-control PRs are Control / Infrastructure.

Non-report project-control changes are Control / Infrastructure.

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

## Automation Route

The maintained development route is:

```text
GitHub Issue → Developer PR → Control Gates → Red-Team Decision → Human Approval → Merge
```

This route reduces owner copy/paste and manual supervision while preserving protected PR governance, red-team accountability, and human approval for major decisions.

## Examples

If `apps/mobile/App.js` changes, the PR may also include exactly one `docs/project-control/phase_*_report.md` companion report. The PR lane remains Product / QA.

If only `docs/project-control/phase_*_report.md` changes, the PR lane is Control / Infrastructure.

If `docs/project-control/DECISION_LOG.md` changes, the PR lane is Control / Infrastructure.

If `package.json` or a lockfile changes, update risk register, dependency handling report, and lockfile provenance evidence.

If `android/**`, `ios/**`, or `eas.json` appears, update artifact index, claim level, risk register, and build/install limitations.
