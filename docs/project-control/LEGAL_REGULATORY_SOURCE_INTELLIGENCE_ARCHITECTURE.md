# Legal, Regulatory, And Source Intelligence Architecture

## Purpose And Boundary

This public-safe documentation defines a future evidence architecture. It does not validate every law, scrape sources, provide individualized legal advice, make licensing determinations, file regulatory documents, bind the company, or accept material legal risk.

## Jurisdiction Hierarchy

Records support federal, state, county, city/AHJ, licensing-body, and utility/service-territory levels. Applicability is explicit; a lower-level overlay may supplement or conflict with higher-level evidence but cannot silently replace it.

## Source Record

Required documentation-scope fields: source ID, issuing authority, jurisdiction, title, public URL or private opaque reference, publication date, effective date, retrieval date, content hash, licensing/terms status, freshness deadline, supersedes, superseded-by, reviewer, review status, and evidence classification.

## Rule Record

Required fields: rule ID, source IDs, normalized proposition, jurisdiction, applicability, exceptions, effective period, source-to-rule lineage, source-to-claim lineage, conflict set, qualified-review status, and release status.

## Reliance Classes

- L0: discovery lead; no reliance.
- L1: retrieved but unverified evidence.
- L2: provenance and date verified; internal research only.
- L3: qualified review complete for internal educational preparation.
- L4: approved public educational use with citations and release gate.
- L5: external or binding use only under qualified-human responsibility and applicable professional rules.

## Freshness, Conflict, And Quarantine

Expired freshness, changed source hashes, broken provenance, unresolved conflicts, missing terms, or supersession ambiguity automatically quarantine dependent claims. Quarantine blocks public use and external reliance until qualified review. Current vendor, framework, statute, regulation, and service details are `not proven` unless retrieved from an official primary source with a recorded date.

## Non-Autonomous Boundary

AI may prepare evidence packets under approved controls but may not independently give individualized legal advice, determine licensing, submit filings, take binding action, or accept material legal risk.
