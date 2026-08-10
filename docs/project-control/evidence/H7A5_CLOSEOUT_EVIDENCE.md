# H7A-5 Closeout Evidence — 2026-08-10 <!-- documentation scope -->

Phase issue: #137 (parent #65). Standing authorization: issue-137-comment-5238006617; this PR under PA-0026 (bootstrap closing PA-0025). All reads captured at second precision (R-STRESS-005). Owner scope words for H7A-5: initial "go", then mid-gate "Go with readme" — the routed apps/web/README.md fix executes as a lane-separated companion PR (recorded in §7); the dependency-review required-context decision is DEFERRED (owner stated no decision; recorded in §5).

## 1. H7A delivered-evidence index (all owner-key-turned merges)

| Deliverable | PR | Merge | Evidence |
| --- | --- | --- | --- |
| H7A-1 inventory + threat model | #138 | 5c62275, 09:16:12Z | evidence/H7A1_SECURITY_POSTURE_INVENTORY.md; THREAT_MODEL_H7A.md (+ Delivery Addendum) |
| H7A-2 policy docs | #139 | 12977aa, 16:42:51Z | SECURITY.md; CONTRIBUTING.md; INCIDENT_RESPONSE_AND_VULNERABILITY_TRIAGE_POLICY.md; CODEOWNERS entries |
| H7A-3 scanning | #143 | 3fb3d4d, 20:07:10Z | evidence/H7A3_SCANNING_EVIDENCE.md; dependabot.yml; dependency-review.yml; PVR + secret scanning + push protection enabled (owner authorizations 5244162677, 5245204102; evidence 5245222558) |
| H7A-4 workflow hardening | #149 | 945031a, 21:44:25Z | evidence/H7A4_WORKFLOW_HARDENING_EVIDENCE.md; 16/16 SHA pins; timeouts/concurrency/credential flags; tracked .pyc removed |
| Companion reconciliation gates | #140/#142/#148 | merged | #52 supersession; P0-RECON; RECON-2 sweep + attestation contract |

## 2. #65 exit-criteria mapping

"Required security checks run on every applicable PR from the trusted CI design": control-gates (aggregate REQUIRED), web/mobile CI (REQUIRED), CodeQL (every PR), dependency-review (every PR, advisory pending §5). "Findings triaged through a documented process": INCIDENT_RESPONSE_AND_VULNERABILITY_TRIAGE_POLICY.md; R-DEP-SEC-001 practiced as the ACCEPT template. "Permissions and action pins verified": H7A-4 evidence, Opus-verified 16/16. "No unresolved critical/high finding silently accepted": the only open high alerts are R-DEP-SEC-001's, owner-accepted with dated revisits (§4); nothing suppressed.

## 3. NIST SSDF practice mapping (delivered controls; documentation scope, no certification claim)

- **PO (Prepare the Organization):** roles/authority model (Decisions 1-4; AGENTS.md; constitution); security policy set (H7A-2); toolchain baseline (TOOLCHAIN.md, H6).
- **PS (Protect Software):** protected main (ruleset, owner-only merge); default-deny path wall + from-main copy; exact pins + digest-bound lockfiles; secret scanning + push protection ENABLED; PVR ENABLED; no secrets in tree (H7A-3 scan clean).
- **PW (Produce Well-Secured Software):** CodeQL on every PR/push; dependency-review fail-on-high; lint/unit/coverage REQUIRED; SHA-pinned minimal-permission workflows; adversarial exact-SHA review (Decision 4) on every phase PR.
- **RV (Respond to Vulnerabilities):** Dependabot alerts + advisory PRs (live function §4); triage policy with FIX/ACCEPT/MITIGATE and expiring exceptions; private reporting route live.
Gaps, honestly: no SBOM publication; no formal training/records practice (single-human program); machine enforcement of some policies still discipline-backed pending H7B typed schemas.

## 4. R-DEP-SEC-001 phase-boundary revisit (H7A closeout) + Dependabot function evidence

Read 2026-08-10T21:50:48Z: alerts UNCHANGED — high|image-size ×2, medium|uuid ×1. Acceptance stands. Next revisit: H7B intake (or next reconciliation, whichever first).

**Dependabot version-update function PROVEN live:** within one minute of #143's merge, Dependabot opened three advisory PRs — #145 (actions/checkout 4.4.0→7.0.1), #146 (actions/setup-node 4.4.0→7.0.0), #147 (react 19.2.3→19.2.8 in /apps/mobile), created 20:07:58-20:08:28Z. Per the recorded advisory-signal posture they cannot pass the wall or merge; they stand as live signals. Owner disposition options recorded (close with comment, or leave open as signals); no default action taken.

## 5. Dependency-review required-context decision: DEFERRED

Live ruleset 20598456 (active) requires exactly: contractoros-control-gates, Web install + build from lockfile, Mobile install + static validation from lockfile. The owner stated no decision at H7A-5; recorded as DEFERRED — dependency-review continues to run on every PR (advisory), and the promotion to REQUIRED remains a one-line owner ruleset act available anytime (revisit at H7B intake or H8).

## 6. SLSA source/build gap assessment (no level claimed)

Source: version control with protected default branch, required checks, mandatory review (owner + disclosed AI legs), full history — strong source-integrity properties. Build: NO builds are produced or published (product frozen until H10); provenance/attestation is therefore NOT APPLICABLE today and unclaimed. When H10 authorizes releases, SBOM + build provenance become release-gate scope; recorded as the future path, not a present property.

## 7. Action re-pin cadence + remaining routed items

**Re-pin cadence:** SHA pins freeze action code; Dependabot's github-actions ecosystem surfaces new releases (already proving itself — #145/#146 arrived same-day). Cadence recorded: re-pin via an authorized control PR when Dependabot signals a security-relevant release, and at each H-phase boundary review; major-version jumps (e.g., checkout v4→v7) require their own compatibility check, never a blind bump.

**Remaining routed items at H7A closeout, none silently dropped:**
1. apps/web/README.md npm-install→npm-ci fix — owner EXTENDED scope mid-gate ("Go with readme"): executes as the immediately-following companion PR in the Product / QA lane under its own PA (the control-file update matrix assigns apps/web/** the Product / QA lane, making a single mixed PR structurally impossible); #137 closes after the companion merges.
2. H7A-1 inventory uniform truth-up (optional, AH-class dated record; owner call).
3. Continuity-parser typed schemas + dead state schema + marker-schema enforcement (H7B).
4. Technically enforced read-only review surface + least-privilege credentials (H8, #68).
5. Single-keyring structural residual H2-WAIVER-001 (H9).
6. RT-H0 underlying-finding re-adjudication (H9; lifecycle completion recorded this PR).
7. Dependabot advisory PRs #145/#146/#147 owner disposition.
