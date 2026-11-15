# Dimension 9 — Cost & Consumption Efficiency

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Dimension 9 — Cost & Consumption Efficiency

> **Supplemental, like D8.** Excluded from the composite score so it does not skew the 7-dimension average, but findings feed Section 9 (Priority Remediation) at full severity and can block go-live. The scorecard shows a "Consumption Posture" row with one of: `CRITICAL WASTE` / `HIGH WASTE` / `EFFICIENT` / `NOT RUN — pricing model unknown`, with the note *"Excluded from composite — see Priority Remediation for findings."*

> **When D9 applies:** any agent where the customer pays per action or per conversation — in practice every metered deployment. **When D9 is not run:** confirmed-unmetered internal agents, or where the pricing model could not be established. Set `cost.status = "NOT_RUN"` with a reason rather than omitting it silently.

---

### Gate — establish the pricing model before quoting any number

Cost findings are arithmetic, and the arithmetic depends on the commercial model. **Ask first:**

| Model | How cost scales | Review framing |
|---|---|---|
| **Flex Credits** | Per action. 20 credits production / 16 sandbox; **voice 30 / 24** | Count billable actions per conversation path |
| **$2.00 per conversation** | Per conversation, not per action | Action count does not drive cost — reframe around latency and conversation volume |

Credits list at roughly $500 per 100,000, so a production action is about $0.10 and a voice action about $0.15. Verified against the Flex Credits Rate Card dated 3 February 2026 — **re-check the current card before quoting, the rates have moved before.**

**REQUIRED:** Use `agentforce-generate` — read the **Credit Consumption Table** in its `references/production-gotchas.md` for which operations bill and which are free. Where it and this skill disagree, canonical wins. If the table cannot be read, label the rates below *unverified against canonical* in the report rather than presenting them as authoritative.

> Upstream has renamed this skill to `agentforce-generate`. Update this reference when the plugin's other cross-references are renamed, so it moves in one pass.

This dimension owns only the review-side delta: the sandbox and voice rates (canonical carries a flat 20 with no channel or environment split), the per-conversation-path arithmetic, and the waste patterns below.

Two qualifications the canonical table does not carry:

- The credit unit covers up to **10,000 tokens**. A single logical action exceeding that bills as multiple actions, so token bloat is a direct billing concern and not only a latency one.
- A design that expresses branching through billable actions instead of the free framework primitives is paying for something available free. Take the list of free operations from the canonical table — it includes the `reasoning` LLM turn itself, which is easy to assume is billed.

If the pricing model cannot be established, set `cost.status = "NOT_RUN"` and say so. Do not guess.

---

### Checks

Walk the `AF-COST-*` rules in `references/static-checks.md`. They cover ungated actions reachable from reasoning, per-path billable action count, uncached repeated lookups, chained two-step knowledge retrieval, multiple searches inside one action, orchestration depth beyond one delegation layer, retrieval-only subagents, tool-schema bloat, and oversized instruction blocks.

### Report the arithmetic, not an adjective

State the per-conversation number explicitly, with the assumed rate and model inline so the customer can audit it:

> *"The WISMO path fires 5 actions = 100 credits ≈ $0.50 per conversation. At the forecast 2,000 conversations/day that is 100K credits/day ≈ $500/day. Assumes Flex Credits at 20 credits/action, production rate, rate card 2026-02-03."*

A number the customer can check beats an adjective. Where an expensive design is defensible, write it as a trade-off rather than a defect.

### Out of scope — request as disclosures, do not assert

Org-level consumption risks are frequently larger than anything visible in the config, but a metadata review cannot see them. Route these to Vendor Disclosures rather than inventing findings:

- **Unmetered entitlement stack** — the product PSL alone is not sufficient. The "Unmetered User Based AI" PSL, *plus* a permission set backed by it with the system permission enabled, *plus* a Standard User or System Administrator profile are all required. Custom profiles burn credits even with the PSL stack correct, and the failure is completely silent.
- **Builder / preview consumption** during the build phase, isolated from production usage
- **RAG Quality Data & Metrics sample rate** — the default fires several LLM judge calls across a large share of conversations
- **Unstructured data ingestion** — LLM-based intelligent processing bills per MB and re-runs on every sync; standard parsing does not
- **Other Einstein features drawing on the same credit pool** — work summaries, service replies, embedded prompts
- **Digital Wallet export** for a representative window, plus the forecast traffic volume to model against
- **Whether the agent is invoked by automation** (record-triggered Flow, Platform Event, scheduled Apex) and whether an idempotency guard exists. A programmatically-invoked agent with no guard both burns credits and, where it writes reasoning output to records, produces divergent results on retry — pair with `AF-VAR-16`.

---

### Severity Summary

| Check | Severity if failing |
|---|---|
| Automation-invoked agent with no idempotency guard | CRITICAL |
| Ungated action reachable from reasoning | HIGH |
| Conversation path exceeding ~5 billable actions | HIGH |
| Uncached repeated lookup | HIGH |
| Orchestration deeper than one delegation layer | HIGH |
| More than ~10 tools bound to one subagent | HIGH |
| More than one search inside a single action | HIGH |
| Chained two-step knowledge retrieval with no caching | MEDIUM |
| Instruction block beyond ~200 lines | MEDIUM |
| Retrieval-only subagent | MEDIUM |

---
