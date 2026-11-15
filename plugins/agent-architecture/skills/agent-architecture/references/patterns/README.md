# Pattern library

This folder holds the founding patterns the skill uses to shape subagent / action / routing decisions. Patterns are not inventions — each one has been observed in two or more AXS engagements and promoted here only after that threshold is met. The library grows by promotion, not by speculation.

## When patterns apply

Patterns are picked at **Step 4.5** (Pattern selection) during Greenfield, and surfaced at **Step 6.5** (Routing contract capture) during Redesign / Script comparison when the baseline already uses them. The skill names the pattern on the architecture page so reviewers can see what shape the design is leaning on, and so downstream skills (`conversation-design`, `persona`, `agentforce-generate`) can resolve the same contract.

- Reference only patterns included in `references/patterns/`. Describe an unsupported design as a proposal; do not claim an existing pattern or upstream approval.

## Founding patterns

| Pattern | One-line purpose | Where it shows up |
|---|---|---|
| [`deterministic-router`](deterministic-router.md) | Design contract for the `start_agent` entry — stage variables, escape hatches, ordered transitions (mapped to Agent Script by `agentforce-generate`) | Any agent with a non-trivial routing surface at the entry point |
| [`identity-ladder`](identity-ladder.md) | Ordered sequence of identity factors with per-factor cap + backstop | Verification subagents (customer verification, account recovery) |
| [`verification-facade`](verification-facade.md) | Server-side verdict facade that returns an enum, not the raw data | Any flow where the agent must decide "verified / not verified" without seeing underlying PII |
| [`escalation-reason-key`](escalation-reason-key.md) | Terminal-handoff contract — a stable key per reason, linked to persona + CD + transfer target | Any subagent that can hand off to a human (every production agent, in practice) |
| [`business-topic-slot`](business-topic-slot.md) | Engagement-specific typed slot with deterministic record selection + verbatim read-back | Billing lookups, order status, policy details — anywhere a specific record has to be named correctly |

## Promoting a new pattern

A candidate becomes a pattern when:

1. It appears in **two or more engagements** (not two subagents in the same engagement).
2. The contract is stable across both — same shape, same decisions, same failure handling.
3. A reviewer-visible name exists (not just internal jargon from one team).
4. The pattern is written down here in the same shape as the founding five: contract, when-to-use, when-not-to-use, cross-skill resolution.

