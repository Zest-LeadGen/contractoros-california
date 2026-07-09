# ContractorOS Prompt Convention

## Purpose

Define the required prompt header and model/effort selection policy for prompts given to Codex, developer agents, red-team agents, and future automation agents.

## Required Prompt Header

Every future implementation, correction, review, or automation prompt must begin with:

```text
Recommended Codex model:
Recommended reasoning effort:
Why this model/effort:
Do not change model/effort unless:
```

## Official Source Basis

Official OpenAI Codex Models docs record these model-selection facts:

- Recommended Codex models include `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, and `gpt-5.3-codex-spark`.
- For most Codex tasks, start with `gpt-5.5`.
- `gpt-5.5` is strongest for complex coding, computer use, knowledge work, and research workflows.
- `gpt-5.4-mini` is faster/lower-cost for lighter coding tasks or subagents.
- `gpt-5.3-codex-spark` is a text-only research preview optimized for near-instant, real-time coding iteration and available to ChatGPT Pro users.
- `gpt-5.2` and `gpt-5.3-codex` are deprecated in Codex when signing in with ChatGPT.

Official OpenAI Codex Config Reference records these `model_reasoning_effort` values:

- `minimal`
- `low`
- `medium`
- `high`
- `xhigh`

`xhigh` is model-dependent.

Official OpenAI GPT-5.5 guidance records these effort-selection facts:

- GPT-5.5 default reasoning effort is `medium`.
- Use `low` for efficient reasoning.
- Use `medium` as the balanced starting point.
- Use `high` for complex agentic tasks requiring hard reasoning where latency matters less.
- Use `xhigh` for the hardest asynchronous agentic tasks or evals.
- Higher reasoning effort is not automatically better; increase effort only when task risk/complexity or eval evidence justifies latency/cost.

Do not overclaim.

Do not claim that the UI label "Extra High" is officially verified unless an official source is added later.

## ContractorOS Model Selection Policy

Use:

- Governance / architecture / red-team / phase-control:
  `gpt-5.5`, `high`

- Red-team-critical architecture, repo-wide control design, or eval-like governance tasks:
  `gpt-5.5`, `xhigh` only when the task risk justifies it

- Major implementation touching product behavior:
  `gpt-5.5`, `high`

- Small correction commit, documentation cleanup, evidence formatting:
  `gpt-5.5`, `medium`
  or `gpt-5.4-mini`, `medium` only when risk is low and speed/cost matters

- Fast mechanical typo/style fix:
  `gpt-5.4-mini`, `low` or `medium`

- Near-real-time low-risk text-only coding iteration:
  `gpt-5.3-codex-spark` only if available and appropriate

- Deprecated / not recommended:
  `gpt-5.2`
  `gpt-5.3-codex`

## Effort Selection Policy

Use:

- `low` for efficient reasoning on low-risk tasks;
- `medium` as the balanced default;
- `high` for complex agentic tasks requiring hard reasoning;
- `xhigh` only for hardest asynchronous agentic tasks, red-team-critical architecture, repo-wide control design, or eval-like work.

Higher effort is not automatically better. Increase effort only when task risk, complexity, or eval evidence justifies additional latency/cost.

## UI Label Rule

If the Codex UI shows "Extra High," record it as the UI-observed label for the official config value `xhigh` unless official UI documentation later proves otherwise.

## Prompt Convention Enforcement

Every future prompt must include model and effort recommendation.

If the model/effort header is missing, the agent must stop and ask for the header before implementation.

Agents must not choose their own model/effort silently for ContractorOS work.

## Phase 4J-0 Scope Note

This file documents the convention only.

It does not activate auto-merge.

It does not change app/product/dependency/build/backend/mobile/web files.

It does not start Phase 4J-1.

It does not resume Phase 4I.
