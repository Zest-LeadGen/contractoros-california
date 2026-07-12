# Jurisdiction Pack Architecture

## Layered Model

1. ContractorOS Core: jurisdiction-neutral concepts, identity, versioning, lineage, accessibility, and module contracts.
2. Federal Base Pack: federal sources and cross-state rules with applicability metadata.
3. State Packs: state licensing, business, trade, and regulatory material.
4. County/City/AHJ Overlays: local amendments, permitting, and enforcement context.
5. Licensing-Body Overlays: board-specific classifications, procedures, and effective dates.
6. Utility/Service-Territory Overlays: utility and territory-specific applicability.

## Launch Gates

California is first; Law & Business is the first governed wedge and C-10 is a priority follow-on. A state launch requires identified authoritative sources, licensing/terms review, retrieval and effective dates, lineage, freshness controls, conflict handling, qualified review, product validation, accessibility, release approval, and measured demand. One contrasting pilot state is selected only from evidence; national expansion has no unconditional date.

## Product Architecture Boundary

The direction is modular monolith first. Packs expose explicit module boundaries and versioned contracts. Service extraction requires measured scaling, isolation, compliance, reliability, or ownership need. This gate does not implement product modules or services.
