# ContractorOS Artifact Index

Documentation purpose: make the GitHub artifact index authoritative for artifact identity, accepted hash, classification, review status, retention, supersession, and any verified storage reference. External archives store non-authoritative bytes only.

Documentation claim: `GITHUB_ARTIFACT_INDEX=AUTHORITATIVE`.
Documentation claim: `EXTERNAL_ARCHIVE_BYTES=NON_AUTHORITATIVE`.
Documentation claim: `ARCHIVE_PROVIDER=NOT_YET_DURABLY_SELECTED`.

No storage URL, Drive ID, archive provider, or approved folder is inferred by this reconciliation.

## Artifact Index Template

| Artifact name | Drive ID or URL | Related phase | Related PR | Purpose | Source equivalent in GitHub | Notes |
|---|---|---|---|---|---|---|
| _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | Add only when artifact already exists and is approved for indexing. |

## Current Notes

- Historical Google Drive assumptions are superseded. Private artifact bytes belong only in a later verified external archive; provider and location are not yet selected.
- GitHub should contain durable source, text records, reports, and reviewable project-control documents.
- This index does not add or imply the existence of any new Drive artifact.
- Existing historical artifact details should be added only when the Drive reference is known and verified.
- Phase 4J-0 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.
- Phase 4J-0 is a source/text control documentation phase only.
- Phase 4I-A creates no ZIP, binary, build artifact, Drive artifact, or archive artifact.
- Phase 4I-A is a source/text control hotfix only.
- Phase 4J-3 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.
- Phase 4J-3 is a source/text control enforcement phase only.
- Phase 4J-4 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.
- Phase 4J-4 is a source/text control enforcement phase only.
- Phase 4J-5 creates no ZIP, binary, build artifact, Drive artifact, release artifact, hosted artifact, or archive artifact.
- Phase 4J-5 is a source/text control documentation phase only.
- Phase 4K-0 creates no artifact, ZIP, binary, build output, Drive artifact, hosted artifact, release artifact, or archive artifact.
- Phase 4K-0 is a source/text project-control planning and inventory phase only.
- Phase 4K-3 creates no artifact, ZIP, binary, build output, Drive artifact, hosted artifact, release artifact, install artifact, runtime visual artifact, device QA artifact, or archive artifact.
- Phase 4K-3 is source/text product-development source-of-truth reconciliation documentation only.
- Phase 4K-4 creates no artifact, ZIP, binary, build output, lockfile artifact, dependency archive, Drive artifact, hosted artifact, release artifact, install artifact, runtime visual artifact, device QA artifact, or archive artifact.
- Phase 4K-4 is source/text dependency-lockfile governance decision documentation only.
- Phase 4K-5 creates no artifact, ZIP, binary, build output, lockfile artifact, dependency archive, dependency directory, Drive artifact, hosted artifact, release artifact, install artifact, runtime visual artifact, device QA artifact, or archive artifact.
- Phase 4K-5 is source/text blocked-before-mutation dependency/toolchain evidence only.
- Phase 4K-6 creates no artifact, ZIP, binary, build output, lockfile artifact, dependency archive, dependency directory, Drive artifact, hosted artifact, runtime artifact, automation artifact, release artifact, install artifact, device QA artifact, or archive artifact.
- Phase 4K-6 is source/text workflow-automation policy, low-risk lane policy, and roadmap documentation only.
- Phase 4K-7 creates no artifact, ZIP, binary, build output, lockfile artifact, dependency archive, dependency directory, Drive artifact, hosted artifact, runtime artifact, automation artifact, release artifact, install artifact, device QA artifact, or archive artifact.
- Phase 4K-7 is source/text control-gate validator implementation and project-control evidence only.
- Historical Pre-4K-9 Issue #47 created public-safe Markdown and JSON-compatible YAML source records only.
- No raw PDF, DOCX, ZIP, binary, build output, private archive, hosted artifact, credential, service, or release artifact is added.
- The canonical state and schemas are governance source files, not operational collector output.

## Historical Issue #49 Source And Test Artifacts

- `scripts/continuity/red_team_continuity.py` is the historical bounded standard-library source implementation merged through closed Issue #49 and merged PR #50 at `7d00343c233e45185e6c4d77e50eb870f408c01f`.
- `scripts/continuity/README.md` and `docs/project-control/RED_TEAM_STARTUP_PACKET_SPEC.md` define the interface and security boundary.
- `docs/project-control/state/red-team-continuity-evidence.schema.json` and `docs/project-control/state/red-team-startup-packet.schema.json` define public-safe structured output.
- The listed fixture JSON files and `expected_startup_packet.md` are deterministic test artifacts.
- A generated live packet or live evidence manifest is not a repository artifact and must remain outside the repository.

## H1 Recovery Artifact Inventory

Every row below is indexed from Issue #58 comment `4975617497`. Byte size is `NOT_PROVEN` because exact local bytes were not accessed in this reconciliation. Storage status is evidence-only and no location is invented.

| Artifact ID | Filename | SHA-256 | Bytes | Classification | Authority claim | Related issue | Storage status/reference | Access class | Retention | Supersession |
|---|---|---|---|---|---|---|---|---|---|---|
| H1-A01 | `01_NEW_WINDOW_MASTER_PROMPT(2).md` | `486510d02f2c07ebe4ed47bd83d66445408add5c7f15f98a267d8417dff38d30` | NOT_PROVEN | DERIVED_HANDOFF_NAVIGATION_NOT_AUTHORITY | NONE | #58 | Historical evidence; location not recorded; no decision power | Private local evidence | Preserve | Superseded by durable GitHub recovery records |
| H1-A02 | `74b084ff-eef3-4410-9019-da468dbd2788.md` | `190b5a8a4a1ebc9aa73fcd451edc96492efaafa107b22fd70ea5a18204006c38` | NOT_PROVEN | LOCAL_POLICY_COPY_NOT_AUTHORITY | NONE | #58 | Verify exact repo blob before reuse; no decision power | Private local evidence | Preserve | Current committed policy controls |
| H1-A03 | `AUDIT_TRANSFER_MANIFEST.json` | `d27750e9455551eb8357d5755fcea629ea22cf6c4f7ad05cea315ecec4797467` | NOT_PROVEN | DEVELOPER_TRANSFER_INTEGRITY_EVIDENCE | EVIDENCE_ONLY | #58 | Preserve with transfer bundle; location not recorded | Private evidence | Preserve | No decision power |
| H1-A04 | `CODEX_LOCAL_OVERRUN_EVIDENCE.md` | `4d2233d3ad3fab7032affc4ac2ef8eb8403363d959b194c016bd8d9cfb1a1bd6` | NOT_PROVEN | DEVELOPER_CHRONOLOGY_AND_OVERRUN_EVIDENCE | NONE | #58 | Incident evidence; location not recorded | Private evidence | Preserve | Durable incident record controls |
| H1-A05 | `ContractorOS_Control_Plane_Seed_v0.zip` | `2209394f2cd8fc45cb6807b576b7b9d6814708d8deb59d0f9a39ed6c90d0d4b1` | NOT_PROVEN | REJECTED_PARALLEL_CONTROL_PLANE_EVIDENCE | NONE | #58 | Preserve; do not install | Private restricted | Preserve | Rejected as project authority |
| H1-A06 | `ContractorOS_Control_Plane_Seed_v0.zip.sha256` | `dacd6f0a439c19a3f2af956ebc918a9e3caac7ee44e1f71501490ef8f9524089` | NOT_PROVEN | REJECTED_PARALLEL_CONTROL_PLANE_EVIDENCE | NONE | #58 | Preserve; do not install | Private restricted | Preserve | Rejected as project authority |
| H1-A07 | `ContractorOS_Control_Plane_Seed_v0/README.md` | `d9850dadb5a26b2a417948b95a1af2e8eceb8a557dc0b1c546f428e56a36a16e` | NOT_PROVEN | REJECTED_PARALLEL_CONTROL_PLANE_EVIDENCE | NONE | #58 | Preserve; do not install | Private restricted | Preserve | Rejected as project authority |
| H1-A08 | `ContractorOS_H1_Adversarial_Test_Results_2026-07-13.json` | `1b357ba269807a850bcb2bb727a0aa2f0a58223c46546c50c4b620612deef99c` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A09 | `ContractorOS_H1_Red_Team_Audit_2026-07-13.md` | `b150b49822f15f7df4405ed71fa2749fb81d20420d46b2d7b968a1f9985b1cfb` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A10 | `ContractorOS_H1_v1_2_Independent_Findings.json` | `c5b0362054dd443ed356d97ac28b1f6533eb2d8b5c92a1c3b802e15a827aaaab` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A11 | `ContractorOS_H1_v1_2_Independent_Red_Team_Audit.md` | `d1182330d0bb6c6fd5b0b0aba639557312bd888072bc48510ef1304ead8d224a` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A12 | `ContractorOS_H1_v1_3_Packet1_Independent_Adversarial_Results.json` | `f759459b00e90d4cc0ef2296953a6d659ab5c2f6a9eb4b93ebe0160aa4bd57bb` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A13 | `ContractorOS_H1_v1_3_Packet1_Independent_Findings.json` | `dbc8bafe2193b48abf7876c1d3d79e7affee565e896f594fc2615ae40083600d` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A14 | `ContractorOS_H1_v1_3_Packet1_Independent_Red_Team_Audit.md` | `1e67c168faa527b3692cf08932dd96f510477d8615d37d22cb00d84b6b5fe2a8` | NOT_PROVEN | INDEPENDENT_REVIEW_EVIDENCE_NOT_YET_DURABLY_RECORDED | EVIDENCE_ONLY | #58 | Findings salvaged into Issue #58 | Private evidence | Preserve | No candidate acceptance |
| H1-A15 | `ContractorOS_H1_v1_3_packet1_verified_audit_transfer.zip` | `39cb1f08ce7862cf2885ff80155e67495f454e654b014356cf7ccf24b80e571d` | NOT_PROVEN | UNTRUSTED_CANDIDATE_AND_EVIDENCE_TRANSFER | NONE | #58 | Donor material pending reconstruction; no decision power | Private restricted | Preserve | Not bootstrap authority |
| H1-A16 | `ContractorOS_H1_v1_3_packet1_verified_audit_transfer.zip.sha256` | `1e97102df85758c3a33aa5d5d0019329c7a10eab8cfbd0110435640b7c35d285` | NOT_PROVEN | DEVELOPER_TRANSFER_INTEGRITY_EVIDENCE | EVIDENCE_ONLY | #58 | Preserve with transfer bundle | Private evidence | Preserve | No decision power |
| H1-A17 | `Pasted text(20).txt` | `c586ec0585c3bcd585fd52e1a573aa98972d10073988fe390af08dbd94e66b91` | NOT_PROVEN | CHAT_DERIVED_OVERSIGHT_INSTRUCTION | NONE | #58 | Incident evidence; location not recorded | Private evidence | Preserve | Durable GitHub recovery records control |
| H1-A18 | `contractoros_h1_bootstrap_planning_v1_1_clean(2).zip` | `817a95a48a9ce61bca55cb3a727bc39175ec13ffeeb23be77884e30cfec01358` | NOT_PROVEN | SUPERSEDED_DEVELOPER_CANDIDATE | NONE | #58 | Preserve; not bootstrap | Private restricted | Preserve | Superseded by Issue #58 recovery |
| H1-A19 | `contractoros_h1_bootstrap_planning_v1_2_corrected.zip` | `015e555a9da57863a5651eb85decee67b8dd85ea5bf601cb04e4b7719907d75e` | NOT_PROVEN | REJECTED_DEVELOPER_CANDIDATE_WITH_INDEPENDENT_FINDINGS | NONE | #58 | Donor material only | Private restricted | Preserve | Rejected as canonical candidate |
| H1-A20 | `contractoros_red_team_handoff_2026-07-13_v1(1).zip` | `1082029d035dbbe40eb030bb426d6d5e195dc477788e1e21afcb2fccc760d047` | NOT_PROVEN | DERIVED_HANDOFF_NAVIGATION_NOT_AUTHORITY | NONE | #58 | Historical evidence; location not recorded; no decision power | Private evidence | Preserve | Superseded by durable GitHub recovery records |
