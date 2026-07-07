# ContractorOS Decision Log

Purpose: record durable architectural and process decisions.

Template:

```text
Decision:
Status:
Reason:
Evidence:
Review condition:
```

## Decisions

### GitHub is source of truth for code and text project-control records

```text
Decision: GitHub is source of truth for code and text project-control records.
Status: Active
Reason: Pull requests, commits, reports, and verification history must remain reviewable in source control.
Evidence: Prior phase reports and PR history are stored in this repository.
Review condition: Revisit only if a formally approved source-control replacement is adopted.
```

### Google Drive is for ZIP/binary/archive artifacts

```text
Decision: Google Drive is for ZIP/binary/archive artifacts.
Status: Active
Reason: Large or binary artifacts should not be committed to GitHub.
Evidence: Project-control instructions separate GitHub source truth from archive artifact storage.
Review condition: Revisit only if artifact storage policy changes.
```

### Local files are temporary scratch/testing only

```text
Decision: Local files are temporary scratch/testing only.
Status: Active
Reason: Local sandbox files are not durable project truth.
Evidence: Phase reports document local checks while committing durable records to GitHub.
Review condition: Revisit only if a controlled local-to-source promotion process is approved.
```

### Controlled Milestone Development Model v3 is active

```text
Decision: Controlled Milestone Development Model v3 is active.
Status: Active
Reason: Development must move faster while preserving traceability, review gates, and scope boundaries.
Evidence: This control scaffold introduces ledger, risk register, decision log, and artifact index records.
Review condition: Revisit at the next formal development-control milestone.
```

### No contaminated lockfile may be committed

```text
Decision: No contaminated lockfile may be committed.
Status: Active
Reason: Lockfiles with non-public registry references are not acceptable project truth.
Evidence: Prior phase reports document generated lockfiles being excluded after scan hits.
Review condition: Revisit only after clean public provenance is proven.
```

### No package-lock may be committed unless clean public provenance is proven

```text
Decision: No package-lock may be committed unless clean public provenance is proven.
Status: Active
Reason: Package-lock files control reproducibility and must not carry sandbox or private registry provenance.
Evidence: Phase 4C and Phase 4D reports document no committed mobile package-lock.
Review condition: Revisit in a dedicated dependency-lock phase.
```

### No EAS/APK/AAB/iOS/native folders until explicitly approved

```text
Decision: No EAS/APK/AAB/iOS/native folders until explicitly approved.
Status: Active
Reason: Build/distribution work is a separate scope gate from internal scaffold development.
Evidence: Phase reports explicitly excluded EAS, APK, AAB, iOS build, android folder, ios folder, and eas.json.
Review condition: Revisit only in an approved build/distribution phase.
```

### No backend/auth/payments/scoring/readiness/pass-fail/public content unless explicitly approved

```text
Decision: No backend/auth/payments/scoring/readiness/pass-fail/public content unless explicitly approved.
Status: Active
Reason: These are product-scope expansions that require independent design, risk, and review gates.
Evidence: Prior phase reports document internal-only, fixture-only mobile scope.
Review condition: Revisit only through an explicitly authorized milestone.
```
