# H1-B1A-P Sanitation Manifest

```text
GATE=H1_B1A_P
DATE=2026-08-08
PHASE_ISSUE=96
SCAN_BASIS=git grep over the full tracked tree at the branch base (post-#93 main lineage)
PATTERN_CLASSES_SCANNED=/Users/ ; /private/tmp ; ~/Documents ; /home/
TOTAL_OCCURRENCES_FOUND=11
SANITIZED=10
EXEMPT=1
DELETIONS=0
HISTORY_REWRITE=NONE
```

Requirement basis: H1B1-SAN-001 (token replacement), SAN-002 (this manifest), SAN-003 (evidence preservation), SAN-004 (no deletion or history rewrite), SAN-006 (historical blobs remain accessible through prior SHAs). Owner decisions H1B1-OD-007 and H1B1-OD-008 are resolved by the owner phase authorization recorded on Issue #96.

## Occurrence table

| # | File | Original pattern class | Replacement token | Text class | Justification |
|---|---|---|---|---|---|
| 1 | phase_4k_0_…_report.md (Commands Run) | Owner home absolute path (`.codex/attachments`) | `<OWNER_HOME>` | Historical | Operator-machine path in evidence text; no evidentiary value in the literal username |
| 2 | phase_4k_1_…_report.md (Commands Run) | Owner home absolute path (`.codex/attachments`) | `<OWNER_HOME>` | Historical | Same class as #1 |
| 3 | phase_4k_2_…_report.md (Commands Run) | Owner home absolute path (`.codex/attachments`) | `<OWNER_HOME>` | Historical | Same class as #1 |
| 4 | phase_4k_3_…_report.md (Commands Run) | Owner home absolute path (`.codex/attachments`) | `<OWNER_HOME>` | Historical | Same class as #1 |
| 5 | phase_4k_5_…_report.md (line 259) | Owner home absolute path (`.codex/attachments`) | `<OWNER_HOME>` | Historical | Same class as #1 |
| 6 | phase_4k_5_…_report.md (line 269) | Owner home absolute path (`.cache/codex-runtimes`) | `<OWNER_HOME>` | Historical | Runtime path in evidence text |
| 7 | phase_4k_5_…_report.md (line 270) | Owner home absolute path (`.cache/codex-runtimes`) | `<OWNER_HOME>` | Historical | Same class as #6 |
| 8 | phase_pre_4k_9_…_report.md (line 269) | Owner home absolute path (workspace clone) | `<OWNER_HOME>` | Historical | Local clone path in collector invocation record |
| 9 | phase_pre_4k_9_…_report.md (line 292) | Temp directory absolute path | `<TEMP_DIRECTORY>` | Historical | Collector output location |
| 10 | phase_pre_4k_9_…_report.md (line 315) | Temp directory absolute path | `<TEMP_DIRECTORY>` | Historical | Same class as #9 |
| 11 | scripts/continuity/tests/test_red_team_continuity.py:249 | `/Users/example/…` synthetic value | NONE — EXEMPT | Fixture | Deliberate synthetic test value; contains no real identity or machine information; changing it would mutate a tested fixture |

## Preservation statement (SAN-006)

The original text of every sanitized report remains byte-accessible through prior commit SHAs; this sanitation changes the current tree only, preserves all git history and supersession chains, deletes nothing, and rewrites no history. Any future history rewrite requires the separate SAN-005 finding and owner authorization.
