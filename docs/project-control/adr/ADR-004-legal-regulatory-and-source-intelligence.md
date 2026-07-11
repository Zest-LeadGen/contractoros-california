# ADR-004 — Legal, Regulatory, And Source Intelligence

## Status
Approved architecture direction; system and legal conclusions are not implemented.

## Related Owner Decision IDs
D8, D9, D16.

## Context
Jurisdictional content requires provenance, effective dates, conflict handling, and qualified reliance boundaries.

## Decision
Use hierarchical source and rule records, lineage, L0–L5 reliance, freshness deadlines, supersession, and quarantine. External or binding reliance requires a qualified human.

## Alternatives Considered
Flat citations, unversioned summaries, autonomous legal conclusions.

## Rejected Alternatives
They cannot prove applicability, currentness, or responsible reliance.

## Consequences
Claims may remain blocked when evidence or qualified review is missing.

## Risks
Stale law, wrong jurisdiction, licensing/terms conflict, and over-reliance.

## Controls
Official-primary-source preference, hashes, dates, conflicts, qualified review, and release gates.

## Implementation Prerequisites
Dedicated lawful ingestion and source-intelligence gate.

## Non-Authorized Scope
No scraping, database construction, advice, determination, filing, or binding action.

## Validation Requirements
Lineage, freshness, conflict, terms, applicability, and reviewer evidence.

## Supersession Links
No historical legal conclusion is superseded by this architecture-only ADR.
