# ContractorOS Prompt Convention

## Purpose

Define the mandatory capability-discovery, model, effort, speed, quota, context, agent, checkpoint, and scope profile for ContractorOS prompts. This convention applies to every substantive implementation, correction, review, red-team, continuation, handoff, and automation prompt.

## Stable Policy

The rules in this section are durable ContractorOS policy. They do not depend on a current model catalog, message allowance, or speed multiplier.

All prompt claims and reported execution metadata also follow `EPISTEMIC_INTEGRITY_AND_NON_FABRICATION_STANDARD.md`. Local output or prompt text cannot create policy or next-packet authority. This cross-reference does not add, remove, reorder, or change the meaning of any required prompt-profile field.

### Required Ordered Prompt Profile

Every covered prompt must begin with these exact ordered, non-empty fields:

```text
Recommended Codex model:
Recommended reasoning effort:
Why this model/effort:
Do not change model/effort unless:
Recommended speed mode:
Agent strategy:
Plan/quota mode:
Context-window strategy:
Checkpoint cadence:
Maximum scope:
```

All ten fields must be present, occur in this order, and have explicit values. The profile must state the recommended model, effort, and speed. A visible selection must not be silently changed or downgraded.

A missing field, empty value, or out-of-order field is a stop condition. Hidden capability metadata is not a missing prompt field and is not a stop condition.

### Capability Discovery And Honest Fallback

Use an explicitly exposed selector when available. Do not guess a hidden model, effort, or speed value. When exact metadata is not exposed, proceed in the available compatible session and record:

```text
ACTUAL_CODEX_MODEL=GPT-5 family; exact identifier not exposed
ACTUAL_REASONING_EFFORT=NOT_EXPOSED
SPEED_MODE=NOT_EXPOSED
```

An explicit visible selection cannot be silently downgraded. If the recommended selection is unavailable, record the actual available selection and the bounded reason for the substitution.

Terra, Sol, and Luna are the stable ContractorOS routing labels when explicitly selectable. Their current availability and provider descriptions are time-sensitive facts recorded separately below.

### Model Routing

When selectors are explicitly available:

- Terra is the default for bounded implementation and routine repository work.
- Sol is for complex security, architecture, deep integration, or final high-stakes review.
- Luna is for low-risk mechanical or high-volume lightweight work.
- The lowest-capability route that can reliably complete the bounded task should be used.

When selectors are not exposed, use the honest fallback above. Hidden metadata alone must never stop permitted work.

### Reasoning Effort Policy

| Effort | Permitted use |
|---|---|
| Low | Mechanical, trivial, low-risk edits |
| Medium | Default for inspection, recovery, bounded implementation, fixtures, tests, and documentation |
| High | Complex security, lifecycle, architecture, integration, or difficult debugging |
| Extra High | One narrowly bounded difficult problem with explicit justification |
| Max | Owner-approved exception with a quota and checkpoint plan |
| Ultra | Owner-approved parallelizable exception; never the default |

Higher effort is not automatically better. Use the lowest effort that can reliably complete the task. Escalation must identify the unresolved problem and applies only to that bounded problem, not automatically to the full phase. Ultra subagents do not constitute independent red-team review.

### Speed Policy

`STANDARD` is the default for ContractorOS Plus-plan work. `FAST` is off by default.

Fast may be used only when the selected model supports it, latency is materially important, the task is narrowly bounded, increased quota or credit consumption is disclosed, the owner approves it or durable policy already permits the exact use, and a durable checkpoint exists. Speed is not intelligence or reasoning quality.

Every final handoff must record `SPEED_MODE=<STANDARD/FAST/NOT_EXPOSED>`. If speed is hidden, record `NOT_EXPOSED`; do not fabricate `STANDARD` or `FAST` as an observed setting.

### Agent And Plus Quota Defaults

One lead agent is the default. Subagents and parallel fan-out require task-specific justification and owner approval. Max and Ultra are owner-approved exceptions, never defaults.

Every substantial Plus-plan task must be divided into atomic packets. Each packet declares:

```text
Primary objective:
Permitted files/functions:
Model:
Reasoning effort:
Speed:
Agent count:
Focused validation:
Checkpoint:
Stop conditions:
Next packet:
```

Do not combine recovery, full architecture review, all correction clusters, all adversarial testing, all documentation reconciliation, CI investigation, and final exact-SHA review handoff in one packet. Prefer focused file reads and durable issue, comment, and SHA references over replaying entire governance documents.

### Context-Window Policy

| Context used | Required behavior |
|---|---|
| 0-59% | Normal bounded work |
| 60-74% | No scope expansion; prepare a checkpoint |
| 75-84% | Finish only the smallest safe unit; validate and prepare a new-window handoff |
| 85-100% | Handoff-only mode; no new implementation |

A reported level of 79% requires a new window before another broad implementation workstream. When the percentage is unavailable, do not invent it; use visible compaction warnings, context-loss symptoms, platform notices, or repeated instruction loss as risk indicators.

### Output Contract

Every substantive response follows the compact, structured progress requirements in `RED_TEAM_OPERATING_PROTOCOL.md`. Current-phase and program-capability values remain separate. Governance work must not inflate product, runtime, backend, build, content, business-validation, or overall-program progress.

Where interactive charts are supported, render exactly one detailed chart at the absolute bottom and place nothing after it. Never expose raw chart JSON, widget arguments, terminal representations, or implementation configuration as the chart. Where unsupported, use compact Markdown tables and record `INTERACTIVE_CHART=UNSUPPORTED_IN_CURRENT_SURFACE`; do not flatten structured progress into a delimiter-separated paragraph.

### Scope Note

This convention does not authorize product, dependency, build, backend, mobile, web, release, credential, paid-service, merge, auto-merge, self-review, branch-protection bypass, next-phase, or paused-phase work.

## Dated Current Guidance

Current official-source review date: 2026-07-12

This section is a dated snapshot, not permanent policy. Reverify it before relying on current model availability, usage ranges, speed support, or multipliers.

Official pages reviewed:

- OpenAI Codex Models: https://developers.openai.com/codex/models/
- OpenAI Codex Pricing: https://developers.openai.com/codex/pricing/
- ChatGPT Learn Speed: https://learn.chatgpt.com/docs/agent-configuration/speed

Current documented guidance as of the review date:

- The default Power setting uses GPT-5.6 Sol with Medium reasoning. Medium balances speed and depth for work needing more planning.
- Higher reasoning effort can improve complex results, but takes longer and uses more tokens.
- Ultra uses subagents for separable parallel work; most tasks do not need Max or Ultra.
- Sol, Terra, and Luna are documented GPT-5.6 choices. Sol targets complex open-ended work, Terra is the pragmatic everyday all-rounder, and Luna targets clear repeatable or high-volume work.
- Terra is the balanced everyday route for strong capability with a better performance/price balance.
- Plus usage varies with model, task size and complexity, local versus cloud execution, context, reasoning, tool use, retrieval, and caching.
- Local messages and cloud tasks share a five-hour window; additional weekly limits may apply.
- Current indicative Plus local-message ranges per five hours are Sol 15-90, Terra 20-110, and Luna 50-280.
- Fast mode increases supported-model speed and consumes credits or included limits more quickly than Standard mode.
- Fast-mode model support, speed factors, and consumption multipliers are time-sensitive and must be reverified before recommendation.
