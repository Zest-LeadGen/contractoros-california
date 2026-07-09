# ContractorOS Design Decisions

Purpose: record ContractorOS California design and operating decisions that must be preserved as repo evidence.

## Active Decisions

### CDR-4J-001 — GitHub source of truth

```text
Status: Proposed / active
Decision: GitHub is the source of truth for code, PRs, review evidence, and text project-control records.
Rejected alternative: relying on chat memory, local scratch files, or connector memory as project truth.
Risk: contributors may overclaim from memory.
Control: every material governance record must be committed in repo files.
```

### CDR-4J-002 — Chat memory is not source of truth

```text
Status: Proposed / active
Decision: Chat memory is not source of truth for ContractorOS California.
Rejected alternative: treating prior chat context as durable evidence.
Risk: stale or missing chat context could drive incorrect work.
Control: assumptions, decisions, sources, model runs, validation tasks, and originality requirements live in repo files.
```

### CDR-4J-003 — Codex developer executor role

```text
Status: Proposed / active
Decision: Codex is developer executor only.
Rejected alternative: allowing Codex to self-review, red-team, approve, merge, or advance phases.
Risk: role collapse weakens governance.
Control: red-team and human/write-access approval remain separate.
```

### CDR-4J-004 — Separate red-team function

```text
Status: Proposed / active
Decision: Red-team remains separate from developer execution.
Rejected alternative: letting developer output stand in for red-team review.
Risk: unsupported claims or forbidden scope could pass without independent challenge.
Control: red-team review is required before merge.
```

### CDR-4J-005 — Human/write-access approval before merge

```text
Status: Proposed / active
Decision: Human/write-access approval remains required before merge.
Rejected alternative: AI-driven merge approval.
Risk: owner judgment could be removed from phase control.
Control: no merge without protected PR review and human/write-access approval.
```

### CDR-4J-006 — No auto-merge or branch-protection bypass

```text
Status: Proposed / active
Decision: No auto-merge and no branch-protection bypass are permitted.
Rejected alternative: using automation to merge or bypass review gates.
Risk: unsafe changes could reach `main`.
Control: protected PR route remains required.
```

### CDR-4J-007 — Bootstrap Codex use for Phase 4J-0

```text
Status: Proposed / active for Phase 4J-0 only
Decision: Codex may implement Phase 4J-0 under strict bootstrap constraints because the prior developer connector path failed twice before implementation by calling api_tool.list_resources.
Rejected alternative: retrying the same developer connector path.
Risk: Codex is creating governance files before AGENTS.md exists.
Control: strict file allowlist, no /init, no product files, no merge, red-team review, human approval.
```

### CDR-4J-008 — No paid services in AI governance path

```text
Status: Proposed / active
Decision: No paid API, paid services, hosted bots, hosted CI, or hosted tools may be added by Phase 4J-0.
Rejected alternative: using paid hosted automation to replace local control work.
Risk: cost, custody, and governance drift.
Control: local files and GitHub PR evidence only.
```

### CDR-4J-009 — No unrelated imported context or hooks

```text
Status: Proposed / active
Decision: No unrelated Claude-imported Codex project context may be used, and unrelated hooks must not be trusted.
Rejected alternative: inheriting external project context or hook behavior.
Risk: wrong project assumptions could enter ContractorOS evidence.
Control: rely on this repo, the current phase prompt, and direct local/GitHub evidence.
```

### CDR-4J-010 — No cockroachdb hooks

```text
Status: Proposed / active
Decision: Do not use cockroachdb hooks for ContractorOS California.
Rejected alternative: letting unrelated database hooks influence this control lane.
Risk: unrelated infrastructure behavior could affect evidence.
Control: ignore unrelated hooks and record that none were trusted.
```

### CDR-4J-011 — No broad connector discovery

```text
Status: Proposed / active
Decision: Do not call broad connector discovery, broad list-resource tools, or tool-schema dump tools.
Rejected alternative: discovering tools broadly when direct tools are missing.
Risk: prohibited calls could recur and contaminate governance work.
Control: stop if direct tools are unavailable.
```

### CDR-4J-012 — Direct-tool stop rule

```text
Status: Proposed / active
Decision: If direct tools are unavailable, stop instead of discovering alternate tools broadly.
Rejected alternative: searching broad tool surfaces to work around missing direct tools.
Risk: repeated list-resource or schema dumping violations.
Control: document blocked status and wait for owner direction.
```

### CDR-4J-013 — Future red-team SHA artifact rule

```text
Status: Proposed / future Phase 4J-2 control target
Decision: Red-team decisions must become GitHub artifacts tied to the exact PR head SHA in future Phase 4J-2.
Rejected alternative: unversioned or head-SHA-ambiguous red-team decisions.
Risk: review evidence could detach from the code being reviewed.
Control: Phase 4J-2 must define the exact artifact path and SHA binding.
```

### CDR-4J-014 — Automation preserves judgment

```text
Status: Proposed / active
Decision: 95% automation means reducing relay, paperwork, repetitive checks, and handoff; it does not remove owner judgment.
Rejected alternative: treating automation as permission to remove owner or red-team decisions.
Risk: governance could appear faster while becoming weaker.
Control: protected PR route, red-team review, and human/write-access approval remain required.
```

### CDR-4J-015 — Versioned governance registers

```text
Status: Proposed / active
Decision: Every assumption, design decision, source, model run, validation task, and originality requirement must be versioned in repo files.
Rejected alternative: leaving governance evidence in chat or local scratch.
Risk: evidence cannot be reviewed or diffed.
Control: maintain the Phase 4J-0 register files under docs/project-control/.
```

### CDR-4J-016 — Developer connector path currently blocked

```text
Status: Proposed / active
Decision: The developer connector implementation path is currently blocked after repeated api_tool.list_resources violations.
Rejected alternative: retrying that path immediately.
Risk: the same prohibited call pattern could recur.
Control: use strict Phase 4J-0 bootstrap Codex execution and record the limitation.
```

### CDR-4J-017 — Bootstrap exception does not expand scope

```text
Status: Proposed / active for Phase 4J-0 only
Decision: Bootstrap Codex use for Phase 4J-0 does not permit product, dependency, build, backend, merge, self-review, or future bypass.
Rejected alternative: treating bootstrap as a durable exception.
Risk: temporary control gap becomes precedent.
Control: strict allowlist, report evidence, PR review, red-team review, and human/write-access approval.
```

### CDR-4J-018 — Lane-based automation and owner-interruption policy

```text
Status: Proposed / future policy target only
Decision: Current owner approval remains required. Future automation phases may reduce manual owner approval for low-risk documentation/control PRs only after SHA-bound red-team markers, required checks, and owner-trigger detection exist. Phase 4J-0 does not activate auto-merge.
Rejected alternative: Require human owner approval for every low-risk future PR forever.
Risk: Removing human approval too early could allow unsafe scope into main.
Control: Only future approved phases may enable lane-based auto-merge eligibility. Owner approval remains mandatory for legal, financial, paid-service, public-release, production/readiness, app-store/build/distribution, scope expansion, unresolved red-team BLOCKED decisions, dependency/security risk acceptance, and architecture-threshold decisions.
```

### CDR-4J-019 — Required prompt model/effort header

```text
Status: Proposed / active after Phase 4J-0 merge
Decision: Every future ContractorOS prompt for Codex, developer agents, red-team agents, or automation agents must include recommended model, recommended reasoning effort, rationale, and conditions for changing model/effort.
Rejected alternative: Allow agents or chat participants to silently choose model/effort per task without durable policy.
Risk: Wrong model/effort can increase cost, latency, weak reasoning, or overthinking, and can make audits harder.
Control: docs/project-control/PROMPT_CONVENTION.md defines the required prompt header and model/effort selection policy. Missing model/effort header is a stop condition.
```
