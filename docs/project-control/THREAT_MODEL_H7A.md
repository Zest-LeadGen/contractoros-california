# H7A Threat Model — Repository, Actions, Dependency, Secret, and Supply-Chain — 2026-08-10 <!-- documentation scope -->

Phase issue: #137 (parent #65). Companion evidence: `evidence/H7A1_SECURITY_POSTURE_INVENTORY.md` (baseline at main 3310052, reads 2026-08-10T08:56:39Z).
Scope: the twelve threat classes #65 requires, each assessed against the observed baseline with current mitigations, residual exposure, and the H7A deliverable that addresses it. This is analysis, not control change. Assessments marked [ASSESSMENT] are executor judgment on verified evidence; nothing here claims a control exists unless the inventory proves it.

## Assets under threat

Governance evidence chain (PA records, DECISION_LOG, markers), control scripts (`scripts/control/`), CI workflows and their required-check status, product lockfiles/manifests, the two-account credential boundary (H2-WAIVER-001), and the public repository's integrity as source of truth.

## The twelve classes

### T1 — Malicious or compromised dependency/action
Mitigations now: exact-pinned npm deps + lockfile digest gate (H6-A.2); Dependabot alerts active; CodeQL active. Exposure: Actions tag-pinned only — a moved tag (`v4`) executes unreviewed code with `contents: read` + (codeql) `security-events: write`; no dependency-review workflow on PRs. [ASSESSMENT] Highest-likelihood class today. → H7A-3 (dependency-review, dependabot.yml), H7A-4 (SHA pins).

### T2 — Workflow self-modification
Mitigations now: armed path wall — PA records enumerate allowed paths; `.github/workflows/control-gates.yml` is forbidden-path in recent PAs; owner-only merge; CODEOWNERS on control surfaces. Exposure: a PA that carelessly allowlists `.github/workflows/**` would let a PR alter its own gates; R-STRESS-002 hardening (checkers run from main) mitigates in-PR gate tampering. → H7A-4 keeps workflow edits under exact-path PAs.

### T3 — `pull_request_target` misuse
Baseline: zero occurrences in any workflow (inventory §2). [ASSESSMENT] Not present; keep it that way. → H7A-2 CONTRIBUTING.md prohibits introducing it without owner-authorized threat review.

### T4 — Untrusted issue/PR prompt injection
Exposure: public repo — outside actors can file issues/PRs whose text reaches AI-agent contexts (this program's operating model). Mitigations now: R-PROV-001 (authority only from owner-authored on-platform comments, verified by actor login); executor never treats issue text as authorization. → H7A-2 documents the actor-verification rule as standing policy; H8 governs agent integrations fully (#68).

### T5 — Exfiltration through logs/artifacts
Mitigations now: workflows upload no artifacts; logs are public by design (public repo); documentation_scope=public_safe discipline. Exposure: a future workflow echoing secrets or private paths into public logs. → H7A-4 (bounded workflows), H7A-2 (incident response for exposure events).

### T6 — Credential or private-document exposure
Mitigations now: no secrets in tree (repo carries no deploy credentials); private evidence lives outside the repo (ContractorOS-Support). Exposure: secret-scanning/push-protection state NOT_PROVEN (inventory L-1) — cannot claim GitHub would block a pushed credential. Two-account single-keyring residual (H2-WAIVER-001) stands, structural fix at H9. → H7A-3 verifies/enables push protection (owner read or key-turn), private-data pattern scan.

### T7 — Poisoned lockfile or registry
Mitigations now: lockfile digest binding (H6), exact pins, npm-ci enforced via pin gate. Exposure: registry-level compromise of a pinned version (integrity hashes in lockfiles mitigate); no SBOM publication yet. → H7A-5 SLSA/SSDF gap assessment scopes what provenance is honestly claimable.

### T8 — Check-name spoofing
Mitigations now: three required contexts enforced by ruleset since 2026-08-10T04:21Z; required checks bound by name — a fork workflow cannot attach a required context to the protected branch merge path without repo write. [ASSESSMENT] Residual is name-collision confusion in PR UI, not gate bypass. → H7A-4 documents required-context inventory in evidence.

### T9 — Stale or fabricated provenance
Mitigations now: R-STRESS-005 captured-read timestamps; SHA-bound red-team markers (stale on head change); PA base_sha binding; github_verified_at plausibility check in the hourly Opus 5 audit routine. → H7A-5 extends provenance discipline to security evidence.

### T10 — Compromised AI-agent token
Exposure: executor token (push:true) on the shared keyring; a compromised agent session could push branches (not merge — owner-only) or file misleading evidence. Mitigations now: owner-only merge authority, required checks, armed wall limiting path scope, machine-verifiable PA chain. Residual held under H2-WAIVER-001 (Q11), structural fix at H9. → H8 (#68) governs integrations under least privilege; H7A-2 records rotation procedure.

### T11 — Malicious generated code
Exposure: the program is AI-operated — generated changes are the norm. Mitigations now: default-deny path wall, forbidden-scope checker, owner review + key-turn on every merge, CodeQL on merges, red-team SHA-bound review separate from executor. → H7A-3 adds dependency-review; H7B (#66) adds adversarial/mutation testing of the control surface itself.

### T12 — Public/private evidence boundary failure
Mitigations now: documentation_scope=public_safe field in canonical state; private material kept in local Support tree, never committed. Exposure: no automated scan enforces the boundary — discipline-only today. → H7A-3 private-data/credential-pattern scan makes it machine-checked.

## Prioritization for H7A deliverables

[ASSESSMENT] Ordered by exposure × likelihood on this baseline: T1 (unpinned actions + no dependency review) > T6 (unproven push protection) > T12 (unscanned boundary) > T4/T10 (agent-surface residuals, partially deferred to H8/H9) > remainder mitigated-with-residuals as noted. H7A-2..H7A-5 sequencing in #137 follows this ordering; no class is closed by this document.
