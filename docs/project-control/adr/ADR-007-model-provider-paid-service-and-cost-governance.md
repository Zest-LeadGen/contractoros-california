# ADR-007 — Model, Provider, Paid-Service, And Cost Governance

## Status
Approved policy direction; no paid service or router is activated.

## Related Owner Decision IDs
D20, D21.

## Context
Named-model guidance ages quickly and paid fallback can bypass owner budget intent.

## Decision
Use provider-agnostic evaluation and official-source verification for current vendor facts. Zero spend is default; only an owner-approved bounded pilot may spend before revenue. Require ceilings, no automatic recharge, no uncapped fallback, and hard shutdown.

## Alternatives Considered
Permanent named-model routing; unrestricted fallback; absolute ban on bounded pilots.

## Rejected Alternatives
They cause vendor lock-in, uncontrolled cost, or conflict with D21.

## Consequences
Vendor details may be `not proven` until refreshed.

## Risks
Quality regression, quota pressure, sensitive-data mismatch, and runaway cost.

## Controls
Evaluation sets, data classes, budgets, duration, exit criteria, portability, and retirement.

## Implementation Prerequisites
Paid-pilot approval or model-router evaluation gate.

## Non-Authorized Scope
No purchase, recharge, provider activation, or model-policy factual update.

## Validation Requirements
Quality, latency, cost, privacy, quota, fallback, and shutdown evidence.

## Supersession Links
Provider-specific guidance is subordinate to current official evidence and later approved policy.
