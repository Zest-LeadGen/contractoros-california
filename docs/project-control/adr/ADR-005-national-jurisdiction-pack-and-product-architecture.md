# ADR-005 — National Jurisdiction Packs And Product Architecture

## Status
Approved architecture direction; no product implementation.

## Related Owner Decision IDs
D10, D11, D17.

## Context
National expansion requires reusable structure without assuming identical jurisdiction rules or premature distributed services.

## Decision
Use ContractorOS Core, Federal Base Pack, State Packs, County/City/AHJ Overlays, Licensing-Body Overlays, and Utility/Service-Territory Overlays. Start with a modular monolith. Extract services only after measured need.

## Alternatives Considered
One undifferentiated national dataset; state-specific forks; microservices first.

## Rejected Alternatives
They increase drift, duplication, or operational complexity before evidence.

## Consequences
Clear module and pack contracts are required before expansion.

## Risks
Overlay conflicts, pack divergence, and hidden coupling.

## Controls
Versioned contracts, applicability metadata, state launch gates, and extraction criteria.

## Implementation Prerequisites
California pack evidence, contrasting-state selection, and product architecture gate.

## Non-Authorized Scope
No module, pack, service, database, or public content is built.

## Validation Requirements
Boundary, conflict, portability, load, ownership, and extraction evidence.

## Supersession Links
Obsolete ZIP phase labels do not supersede repository phase history.
