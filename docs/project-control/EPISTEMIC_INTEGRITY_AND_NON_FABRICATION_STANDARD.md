# ContractorOS Epistemic Integrity and Non-Fabrication Standard

## Purpose And Claim Limit

This standard governs material claims, evidence, uncertainty, and action boundaries for ContractorOS. It applies to owners, developer executors, red-team reviewers, automation, and future providers or models. It reinforces protected GitHub governance and does not create implementation, approval, merge, release, production, or next-packet power.

A perfect non-hallucination guarantee is not claimed. The objective is measurable prevention, detection, containment, correction, and durable learning.

## Core Rules

```text
NO_EVIDENCE=NO_CLAIM
MISSING_EVIDENCE=NOT_PROVEN
CONFLICTING_EVIDENCE=BLOCKED
STALE_EVIDENCE=REVERIFY
INFERENCE=LABEL_REQUIRED
ASSUMPTION=LABEL_REQUIRED
UNCERTAINTY=DISCLOSE
```

Documentation rule: an action requires both factual support and durable authority. Evidence that an action is technically possible is not authority to perform it.

## Source Hierarchy

Use the highest applicable source and record provenance:

1. applicable law and binding obligations;
2. live protected GitHub evidence;
3. current official primary external sources;
4. exact source, schemas, logs, reproducible tests, runtime or build evidence, and hashed artifacts;
5. peer-reviewed primary research where no issuing authority exists;
6. reputable secondary sources for discovery or counteranalysis only;
7. owner statements, AI output, chat, local files, scratch state, and connector state as unverified input until independently confirmed and durably recorded.

Later owner decisions control only when they are durable, explicit, within lawful authority, and name the superseded record. A repeated claim does not become independent evidence.

## Claim Classifications

Every material claim is one of:

- `PROVEN`: directly supported by current cited evidence.
- `NOT_PROVEN`: required evidence is missing or inaccessible.
- `BLOCKED`: evidence conflicts or is insufficient for the consequential action.
- `STALE_REVERIFY`: evidence was once relevant but freshness is no longer established.
- `INFERENCE`: a reasoned conclusion that names supporting facts and alternatives.
- `ASSUMPTION`: an explicit temporary premise with risk and validation plan.
- `UNKNOWN`: neither evidence nor a defensible bounded inference is available.
- `HISTORICAL`: accurate for a named past state and not current authority; documentation classification only.
- `SUPERSEDED`: preserved evidence whose controlling effect was replaced by a named later record.

Do not present planning approval as implementation, local output as project authority, documentation as runtime proof, or a passing candidate-owned test as independent acceptance.

## Citation Contract

A material claim records source identity, exact location or durable identifier, relevant SHA or content hash when available, observation time, and the specific proposition supported. Citations must be reachable by the intended reviewer or explicitly classified as inaccessible/private evidence with an opaque identifier or accepted hash.

Citation rules:

- no orphan citation that supports no stated claim;
- no citation laundering through an AI summary when the primary source is available;
- no scope expansion beyond what the cited source proves;
- no private path, secret, token, or sensitive payload in public records;
- no invented URL, archive location, Drive ID, issue, PR, SHA, test result, or review state.

## Freshness Contract

Freshness is claim-specific. Mutable GitHub lifecycle, current SHA, checks, protections, permissions, external official policy, provider behavior, and repository state require live reverification before consequential use. A stable historical hash may remain evidence of exact past bytes but not of current lifecycle state.

Every freshness-sensitive claim records when and how it was observed. A changed PR head invalidates prior SHA-bound review. A conflict between canonical state and live GitHub evidence blocks consequential guidance until reconciled.

## Anti-Echo-Chamber Review

Independent review must retrieve primary evidence without relying only on the developer summary. It must seek disconfirming evidence, identify shared-source dependence, challenge candidate-owned tests and oracles, test negative and adversarial cases, and distinguish repeated assertions from independent corroboration.

A fresh review context must challenge at least source identity, current SHA, allowlist, historical preservation, supersession lineage, role separation, artifact classification, incident chronology, unsupported guarantees, ambiguous next-gate language, and forbidden-scope absence.

## Developer Executor Obligations

The developer executor must:

- operate only inside durable objective, allowlist, and stop conditions;
- verify starting state before mutation;
- label unknowns, assumptions, and inferences;
- preserve raw failure evidence and correct prior errors plainly;
- run required positive and negative validation;
- stop rather than alter controls, widen scope, bypass hooks, or promote local evidence to authority;
- report actual commands and results, including failures and skipped steps;
- refrain from self-review, final review markers, approval, merge, issue closeout, and automatic continuation.

## Red-Team Obligations

Red-team may lead architecture, requirements, threat modeling, sequencing, and adversarial review. It must remain separate from the developer implementation it audits. It independently retrieves exact-current-head evidence, checks source freshness and conflicts, challenges the strongest permitted claim, and uses only `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED` for the final SHA-bound decision.

Red-team cannot convert missing evidence to a pass, treat a stale decision as current, or treat its architecture role as implementation authority; this is a scope prohibition.

## Automation Obligations

Automation must be least-privileged, fail closed, deterministic where promised, bounded by exact identities and inputs, and unable to approve its own output. It records provenance, refuses unknown schemas or duplicate keys where policy requires strictness, prevents candidate code from defining acceptance, and stops on missing, conflicting, stale, unsafe, or out-of-scope evidence.

Automation output is evidence, not authority. Provider or model substitution cannot change policy or weaken gates; this is a documentation claim.

## Provider And Model Independence

Documentation scope: this standard is provider- and model-independent. Product labels, personalities, reasoning settings, speed settings, tool availability, and generated confidence are not evidence of correctness. Hidden metadata must not be guessed. Any model or provider must satisfy the same evidence, authority, role-separation, validation, privacy, and stop-condition requirements.

## Machine-Enforcement Layers

Defense in depth includes:

1. exact schemas and strict parsing;
2. source identity, SHA, freshness, and provenance binding;
3. changed-file and forbidden-scope checks;
4. claim-language and citation checks;
5. deterministic positive, negative, mutation, rename, move, delete, and substitution tests;
6. candidate-independent oracles and no execution of untrusted candidate policy;
7. protected workflow evidence and immutable action provenance;
8. exact-SHA independent review and separate human approval;
9. incident logging, rollback, quarantine, and later regression tests;
10. continuous measurement in observation mode before enforcement cutover.

No single layer is treated as perfect or sufficient.

## Zero-Event Metrics

The enforced target is zero for:

```text
UNSUPPORTED_MATERIAL_CLAIMS=0
ORPHAN_CITATIONS=0
UNLABELED_ASSUMPTIONS=0
UNRESOLVED_CONTRADICTIONS_PRESENTED_AS_FACT=0
STALE_SOURCE_USED_WITHOUT_REVALIDATION=0
UNAUTHORIZED_ACTIONS=0 # target claim
SELF_APPROVAL_EVENTS=0
SOURCE_IDENTITY_MISMATCHES_ACCEPTED=0
PACKETS_ADVANCED_WITHOUT_DURABLE_CLOSEOUT=0
```

A zero target is not a guarantee. Measurement must define denominator, observation window, detector coverage, false-positive/false-negative review, and unresolved gaps.

## Incident Response

When a material unsupported claim or unauthorized action occurs:

1. stop consequential work and preserve evidence;
2. identify affected claims, actions, repositories, branches, PRs, issues, artifacts, and people;
3. classify blast radius and whether any external state changed;
4. correct or withdraw the claim/action through the protected route;
5. record root cause, contributing process or control gaps, and known unknowns;
6. add regression tests or procedural controls without weakening unrelated protections;
7. require fresh review for any affected SHA or decision;
8. resume only from durable owner-approved conditions.

History is preserved. Correction adds explicit supersession rather than silent erasure.

## Exceptions And Change Control

An exception must be lawful, narrowly scoped, time-bounded, owner-approved in durable evidence, independently reviewed where applicable, and include rollback and expiry. No local prompt, model output, connector state, or emergency label creates an exception.

Changes to this standard require a protected project-control PR, fresh exact-SHA review, separate human/write-access approval, merge, main verification, and durable closeout.
