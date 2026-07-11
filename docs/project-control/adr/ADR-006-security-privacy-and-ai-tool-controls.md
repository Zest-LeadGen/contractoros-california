# ADR-006 — Security, Privacy, And AI Tool Controls

## Status
Approved direction; security program and tool identities are not implemented.

## Related Owner Decision IDs
D18, D19.

## Context
Future AI tools increase data, capability, and supply-chain risk.

## Decision
Build a versioned, evidence-based security/privacy program and require least privilege, strict schemas, separated identities, protected approvals, prompt-injection defenses, traces, rate/cost limits, and kill switches.

## Alternatives Considered
Permanent broad credentials; implicit trust; framework claims without current evidence.

## Rejected Alternatives
They weaken containment and auditability.

## Consequences
Sensitive capabilities remain blocked until a dedicated gate proves controls.

## Risks
Secret exposure, over-privilege, unsafe tool output, and outdated framework mapping.

## Controls
Deny by default, data classification, official-source mapping, incident handling, and negative tests.

## Implementation Prerequisites
Threat model, current framework verification, identity design, and incident plan.

## Non-Authorized Scope
No credential, service, agent, or security claim is implemented.

## Validation Requirements
Capability-denial, injection, trace, limit, revocation, and incident tests.

## Supersession Links
Later versioned security ADRs must cite the official framework version and this ADR.
