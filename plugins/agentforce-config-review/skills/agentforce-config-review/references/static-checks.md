# Static Check Catalog

Mechanically decidable rules for a delivered Agentforce configuration. Every rule here can be evaluated by a script or a `rg` invocation against the retrieved metadata — no org access, no runtime data, no judgement.

**Run this before writing any finding.** Scanning first produces a review shaped by evidence; drafting first produces one shaped by whatever you noticed first. It also makes the review reproducible — a second reviewer running this catalog should reach the same findings.

Findings from this catalog **file into the existing dimensions**, exactly as action schema findings do (see *How to incorporate action schema findings* in `SKILL.md`). This file is not a new review section. The one exception is `AF-COST`, which has no home in D1–D8 and files into the supplemental Cost & Consumption section.

## Scope — what is and is not in this file

A rule belongs here only if it is decidable from the metadata by one of: **literal presence or absence** of a token or attribute; **a structural property** of the state graph, call graph, or block nesting; **a set difference** between two enumerable lists; or **a count against a threshold**.

Rules requiring a human to judge whether prose adequately "addresses" a concept are **not** here — guardrail adequacy, escalation instruction ambiguity, and persona consistency are all judgement calls, and a keyword scan for them both misses real controls and passes useless ones. Those stay in the dimension prose in `SKILL.md` and in `references/agent-type-variants.md`.

**This is a floor, not a ceiling.** A clean scan is not a passing dimension. D3 in particular is mostly judgement — only three mechanical guardrail rules exist, and the most severe guardrail failure mode (an injection guardrail broad enough to block the agent's primary workflow) cannot be detected mechanically at all.

## Recording results

Record every rule as **PASS**, **FAIL** (with the file and line that proves it), or **N/A** (with a one-line reason). A rule you did not check is **NOT ASSESSED** — say so rather than implying a pass.

Rules marked **⚑** are decidable as a *signal* but need a read to confirm. The scan produces a candidate; it does not close the verdict.

Severity in the tables is a **starting point**. Apply the severity definitions in `SKILL.md` and the deployment context — POC versus production cutover, internal versus customer-facing, regulated versus not — before assigning final severity.

**Silent failures outrank loud ones.** A defect that throws a visible error gets caught in Testing Center. A defect that succeeds quietly and produces the wrong outcome — a dropped escalation message, a `set` that silently discards, a masked variable used as a lookup key — reaches production and stays there.

---

## Inventory first

```bash
# Agent Script bundles
fd -e agent
rg -c 'subagent |start_agent ' --stats          # subagent count
rg -c '@actions\.' --stats                      # action invocation sites
rg -n 'variables:' -A 40                        # variable declarations
rg -c 'reasoning:' --stats                      # LLM resolution points

# Classic Builder / planner metadata
fd -g '*.genAiPlugin-meta.xml'
fd -g '*.genAiFunction-meta.xml'
fd -g 'schema.json' -p genAiPlannerBundles
```

## Cheapest high-yield rules — run these five first

Each is a grep or a set difference, each takes seconds, and each has been the root cause of a production incident: `AF-SEC-01` (empty subagent description), `AF-PER-02` (unreplaced placeholder text), `AF-VAR-11` (masking explicitly disabled), `AF-REL-01` (deprecated parameter now a hard error), `AF-ARCH-07` (transition to an undefined state).

---

## AF-PER — files into D1 (Persona, Tone & Topic Scope)

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-PER-02 | Placeholder text not replaced | `rg -n -i 'placeholder\|\[company\|lorem\|TODO\|TBD\|XXX'` across the bundle | HIGH |
| AF-PER-07 ⚑ | UI labels hardcoded in English on a multi-locale agent | Multi-locale declared **and** literal English UI strings present. Confirm which strings are user-facing | LOW |

Persona consistency is otherwise a reading task — role/description alignment, tone drift across sibling topics, and topic scope collisions are all judgement calls and stay in the D1 prose.

---

## AF-ARCH — files into D2 (Instructions, Actions & Fallback)

Graph properties are decidable; latency is not. `AF-ARCH-06` and `AF-ARCH-07` are the highest-value rules in this catalog — both CRITICAL, both a single set difference or degree check, both invisible in the builder UI.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-ARCH-06 | State with no outbound transition and no terminal marker | Build the state graph; find nodes with out-degree zero not marked terminal | CRITICAL |
| AF-ARCH-07 | Transition references an undefined state | Set difference: every `transition to @subagent.X` target against declared subagents | CRITICAL |
| AF-ARCH-08 | No explicit terminal (end or handoff) state | No node marked terminal anywhere in the graph | HIGH |
| AF-ARCH-09 ⚑ | Slot-fill loop with no max-attempts bound | Find re-prompt cycles; check for a counter incremented within the cycle | HIGH |
| AF-ARCH-10 | Action with no failure branch | For each action invocation, test for a downstream conditional on its failure or status output | HIGH |
| AF-ARCH-01 | Per-turn LLM call count not modeled | Count maximum LLM round-trips per user turn across reachable reasoning blocks | HIGH (POC) / CRITICAL (cutover) |

---

## AF-REL — files into D2 (Instructions, Actions & Fallback)

**Version-sensitive. Record the target release and compiler version before applying these** — several values were silently accepted by older compilers and now fail lint, so a config that "worked" may not compile on the target org. Re-verify against release notes each major version.

These are release and deployability defects rather than instruction-quality defects, but they file into D2 because they determine whether the configured behavior runs at all. Note that in the findings JSON.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-REL-01 | `disable_graph_runtime` / `additional_parameter__disable_graph_runtime` present | `rg -n 'disable_graph_runtime'` — deprecated, now a hard error | HIGH |
| AF-REL-02 | `default_agent_user` under `config:` instead of `access:` | Locate the key, test its parent block. If set in both, `access` wins silently | MEDIUM |
| AF-REL-03 | Unrecognized `agent_type` value | Compare against the accepted enum — previously accepted silently, now fails lint | MEDIUM |
| AF-REL-05 | `sharing_policy` or `verified_customer_record_access` under `access:` on an Employee agent | Both keys are disallowed for that agent type; a common copy-paste artifact when a Service config is repurposed | MEDIUM |
| AF-REL-06 | Experimental `collect` construct in a production-bound config | `rg -n '\bcollect\b'` — behavior may change between releases | MEDIUM |
| AF-REL-07 | Empty `runtime:` block | Must declare at least one of `streaming`, `thought_chunks`, `citation`, `groundedness`, `reset_to_initial_node` | LOW |
| AF-REL-08 | Action with no `description` | The compiler derives one from the action name, and descriptions are the planner's primary selection signal | MEDIUM |
| AF-REL-09 | Action input identifier containing `:` emitted unquoted in a `with` clause | The parser reads the prefix as the parameter name and the action hard-fails | HIGH |
| AF-REL-10 | Nested or embedded `if` inside reasoning instructions | A known fragility point across compiler releases | MEDIUM |
| AF-REL-11 | Reserved `@InvocableVariable` names in backing Apex (`model`, `description`, `label`) | Requires Apex sources. Apex compiles fine; the agent script compiler fails on the action's I/O schema | MEDIUM |
| AF-REL-12 | Agent on the legacy builder runtime | Frozen runtime — no new features planned, and no new agents can be created there as of 13 July 2026. Existing agents keep running and remain editable, so this is a roadmap and enhancement-path blocker rather than end of support | HIGH |
| AF-REL-13 | SDR / Lead Nurturing agent type — metadata not deployable or retrievable via Metadata API | No reliable rollback path is a promotion blocker on its own | HIGH |
| AF-REL-14 | Legacy agent upgraded to the new builder with no template or agent-type association | Silently forecloses template-bound features in later phases | HIGH |
| AF-REL-15 | Deployment package mixes a `genAiFunction` deletion with a `GenAiPlannerBundle` change | Diff the deployment package or commit range. Forces a runtime index rebuild that registers only new and changed actions and **drops all unchanged ones** — the agent shows "0 Actions" in production while metadata still looks correct, and redeploying does not fix it | CRITICAL |
| AF-REL-16 | AgentScript exceeds **~20,000 lines** | `wc -l` the active `.agentScript-meta.xml` / `.agentScriptVersion-meta.xml`. Past this ceiling compile times climb sharply, the Builder editor becomes unresponsive, and Metadata API retrieve/deploy starts to time out — the script becomes hard to change safely. Treat as a refactor-into-subagents signal, not just a style note. AgentScript only | HIGH |
| AF-REL-17 | Compiled AgentScript bundle exceeds **~20 MB** | Size the deployed bundle (sum the `agentScripts/` metadata for the active version, or the retrieved package size). Beyond ~20 MB retrieve/deploy and runtime load are unreliable and can fail outright, and the whole bundle serializes into context on load, taxing every call. AgentScript only | HIGH |

---

## AF-ESC — files into D2 / D3 (Escalation & Handoff)

Escalation is the one path where a config defect converts directly into an abandoned customer, and nearly every failure mode is silent: routing succeeds, nothing errors, the user is simply never handed off.

These are **Agent Script config rules** and complement rather than replace the platform escalation coverage in `references/agent-type-variants.md` — the automatic escalation triggers, `EscalateHandler` GSM Hangup behavior, and the `flow_id` requirement in `escalate_function.json` remain the authoritative voice checks and are not duplicated here.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-ESC-01 | Escalation message interpolates a variable that is undeclared or out of scope | Extract every `{!@variables.X}` from escalation message bodies; fail if `X` is absent from `variables:` or not in scope on any path reaching the message. Renders as literal `{!@variables.x}` to the customer at the most sensitive moment in the conversation | HIGH |
| AF-ESC-03 | Email-channel agent relies on OOTB `@utils.escalate` | Email connection present **and** `rg -n '@utils\.escalate'` matches. Routing works, so it tests green — the agent simply goes silent and the customer is never told they were escalated | HIGH |
| AF-ESC-06 ⚑ | Voice escalation subagent emits spoken transfer text | Voice deployment **and** escalation subagent instructions matching `transfer\|hold\|connect you`. Collides with the telephony layer, which owns the transfer prompt | HIGH (voice) |
| AF-ESC-09 | Precondition action in an escalation path has no idempotency guard | For each action reachable inside an escalation path, check it is enclosed by a conditional testing a flag variable | MEDIUM |
| AF-ESC-10 | `delegate_escalation` left at default while connected subagents exist | When unset, escalation follows the subagent's outbound flow rather than the orchestrator's — silently the wrong path | HIGH |
| AF-ESC-11 | Escalation subagent's only instruction is to call escalate | Reasoning block contains an escalate call and no context capture | MEDIUM |
| AF-ESC-14 ⚑ | Deflection loop unbounded — knowledge retrieval sits in a cycle | Find cycles in the transition graph containing a knowledge retrieval action | HIGH |

**Not mechanically decidable, and the most severe of the set:** an escalation instruction that permits both a text response and a session end. One deployment's instruction read *"run go_to_escalation. Do not end the session and do not answer with transfer text alone"* and produced intermittent caller disconnects — callers requesting a human were dropped rather than transferred, blocking a production go-live. Ambiguity between "respond" and "escalate" in a single instruction resolves non-deterministically. Check this by reading, every time.

---

## AF-SEC — files into D3 (Guardrails, Safety & Responsible AI)

**Only three guardrail rules are mechanical.** Guardrail adequacy is prose, and the ETL coverage model in `SKILL.md` already governs when absence is a finding. Do not let a green block here imply D3 passed.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-SEC-01 | Any subagent has an empty or missing `description` | Enumerate subagents; fail any with absent or whitespace-only description | HIGH |
| AF-SEC-02 | Off-topic / fallback subagent has no description | `AF-SEC-01` scoped to the off-topic handler | HIGH |
| AF-SEC-12 ⚑ | No out-of-scope branch reachable from the router | Reachability analysis from the entry subagent for an off-topic or fallback target | HIGH |

**Why AF-SEC-01 is not cosmetic:** a missing description on an `Off_Topic` subagent caused an agent to self-identify as "Agentforce/Salesforce" to end users on day one of a pilot. One empty field, a persona and disclosure failure in production, invisible in the builder UI.

---

## AF-VAR — files into D4 (Variable Typing & Data Integrity)

The strongest dimension for mechanical checking — these are dataflow and type analysis.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-VAR-01 | `@context.*` referenced anywhere in Agent Script | `rg -n '@context\.'` — unsupported; correct form is `{!@variables.<name>}`. The canonical legacy-to-Agent-Script migration defect, and it manifests only as the agent behaving as though no record is open, so it survives casual testing | HIGH |
| AF-VAR-02 | `@inputs.*` used in a post-action `set` | Test whether the enclosing statement is a `set` following an action invocation. Silent — the action succeeds and the assignment drops with no trace error | HIGH |
| AF-VAR-03 | `@outputs.*` referenced outside the `set`/`if` immediately following its invocation | Check adjacency between each reference and its producing action | HIGH |
| AF-VAR-04 | Declared variable never referenced | Set difference: `variables:` block minus all `@variables.` reference sites. Co-occurs with `AF-VAR-01`, and fixing only the syntax leaves the agent broken | HIGH |
| AF-VAR-05 | Action invoked before a variable it depends on is established | For each `run @actions.X with y = @variables.z`, confirm `z` is assigned on every path reaching the invocation | HIGH |
| AF-VAR-07 | Boolean consumed as Text, or the reverse, in a conditional | Compare declared type against expected type at every comparison site. Silent branch failure | CRITICAL |
| AF-VAR-09 | Malformed or out-of-scope `{!@variables.x}` in a user-facing message | Scope analysis across all message bodies. Especially damaging on voice, where the user has no visual to recover from | HIGH |
| AF-VAR-11 | `additional_parameter__enable_data_masking` set to `false` | `rg -n 'enable_data_masking'` — a debug artifact that survives handoff and ships PII unmasked | CRITICAL |
| AF-VAR-16 ⚑ | Reasoning output written to a record | Dataflow: trace reasoning-block outputs into write-action inputs. Whether human review exists downstream needs a read | CRITICAL |

**Why AF-VAR-16 is CRITICAL:** in one production incident, 628 duplicate invocations of a triage agent produced a *different* classification from the original run in 276 cases — 44% divergence on identical inputs. An agent persisting non-deterministic classifications unattended makes a retry a silent data-corruption event, not just a double charge.

---

## AF-KNOW — files into D5 (Knowledge Grounding)

Grounding quality is mostly a property of the corpus, which is not in the metadata. Three rules are decidable from config.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-KNOW-03 | Citation not enabled in the `runtime:` block | Check `runtime:` for `citation`. Covers the platform toggle only — whether instructions request attribution is prose. See also the `citationsEnabled: const:false` schema check in D5 | MEDIUM |
| AF-KNOW-04 | Single-sourced grounding pipeline with no fallback retriever | Count distinct retriever or connector bindings; fail at 1. Any connector defect then becomes a go-live slip | HIGH |
| AF-KNOW-08 | Top-k retrieval not capped | Inspect retrieval config for an explicit bound. Each additional chunk multiplies input token cost for that action | MEDIUM |

---

## AF-GOV — files into D6 (Data Residency & AI Governance)

**Only three governance rules are decidable from metadata.** Residency and governance are contract-and-org questions — the rest require the customer contract, the delivered design doc, or org configuration, and belong in the Vendor Disclosures list rather than being asserted from the bundle.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-GOV-01 | Config references an MCP server or other external tool egress | `rg -n -i 'mcp'` and inspect matches. Data leaving over MCP is outside the Einstein Trust Layer and Salesforce zero-data-retention entirely — the customer is on the model provider's own terms at that point | CRITICAL |
| AF-GOV-06 | Record lookup returns the full record | From action schemas: flag actions retrieving records with no field projection — unnecessary PII into LLM context | HIGH |
| AF-GOV-07 | No field-level minimization on actions pulling customer data | `AF-GOV-06` applied per action | HIGH |

> **Masking is not the agent's PII control.** Do not record "Trust Layer masking enabled" as a D6 pass. LLM data masking is **disabled for Agentforce agents by design** — placeholders add latency and degrade planner and action accuracy, so Salesforce turned it off for agent workflows. It remains active for Prompt Builder, Flow-invoked prompt templates, and turnkey features such as Service Replies and Work Summaries. Zero-data-retention, prompt-injection detection, and FLS/RBAC/sharing all remain fully active for agents. **If the vendor's design doc or DPIA cites masking as the agent's PII control, that claim is itself a finding** — the documented control is not running. Sources: Trailhead *LLM Data Masking in the Einstein Trust Layer*; Salesforce blog *LLM Data Masking: Silver Bullet or Double-Edged Sword?*

---

## AF-TEST — files into D7 (CRM Integration, Logging & Error Handling)

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-TEST-05 | Default generic error string with no correlation ID | Inspect configured error strings for an identifier token — gives operations nothing to triage with | MEDIUM |
| AF-TEST-03 | No regression or evaluation suite in the repo | Search for `AiEvaluationDefinition` specs or equivalent. Absence means the customer inherits an agent they cannot regression-test | HIGH |
| AF-TEST-08 | No CI/CD gate blocking unvalidated agent versions | Check for pipeline config invoking agent tests before deploy. Without it, every finding in this review can silently regress on the next deploy | MEDIUM |

Evidence-package gaps that need artifacts rather than metadata — tested-versus-deployed channel coverage, adversarial test results, a last-known-good baseline, and an agreed mechanism for separating platform defects from implementation defects — belong in the Step 1 intake list and the Vendor Disclosures output, not here. WhatsApp, mobile/iOS, and voice have each produced defects invisible in Agent Builder preview, so preview-only validation is an incomplete test plan on any multi-channel deployment.

---

## AF-COST — files into the supplemental Cost & Consumption section

The only rule family with no home in D1–D8. Arithmetic rather than opinion, **once the pricing model is established.**

**Rate card, verified against the card dated 3 February 2026:**

| Usage type | Production | Sandbox |
|---|---|---|
| Standard or custom action | 20 credits | 16 |
| Voice standard or custom action | **30 credits** | 24 |

Credits list at roughly $500 per 100,000, so a production action is about $0.10 and a voice action about $0.15. Two qualifications change the arithmetic materially:

- **An action is not billed flat regardless of size.** The credit unit covers up to 10,000 tokens; a single logical action exceeding that bills as multiple actions. Token bloat is therefore a direct billing concern, not only a latency concern.
- **An alternative $2.00-per-conversation model exists.** Under it action count does not drive cost linearly, and a six-action conversation costs the same as a two-action one. **Establish the pricing model before quoting any figure.** On per-conversation pricing, reframe around latency and conversation volume instead.

**REQUIRED:** Use `developing-agentforce` — take the list of free operations from the Credit Consumption Table in its `references/production-gotchas.md`, which wins over the rates above where the two disagree. (Upstream has renamed that skill to `agentforce-generate`; this reference moves with the plugin's other cross-references.) The table above is the delta only: canonical carries a flat 20 credits with no sandbox or voice split. A design expressing branching through billable actions instead of the free framework primitives is paying for something available free.

| ID | Rule | Decision procedure | Severity |
|---|---|---|---|
| AF-COST-01 | Action reachable from a reasoning block with no gating condition | For each `@actions.` site reachable from `reasoning`, test for an enclosing conditional or entry condition. One prompt-template action wired this way consumed 17% of an org's total credits in two weeks | HIGH |
| AF-COST-02 | A conversation path exceeds ~5 billable actions | Enumerate paths, count billable actions per path, multiply by 20 — or 30 for voice | HIGH (>5), MEDIUM (3–5) |
| AF-COST-04 | Same lookup invoked from more than one reachable point with no caching | Count invocation sites per action; fail where >1 with no staleness flag gating them | HIGH |
| AF-COST-07 | Two chained retrieval actions per knowledge turn | Detect adjacent retrieval pairs — 40 credits where 20 would do | MEDIUM |
| AF-COST-08 | More than one retriever or search invocation inside a single action | Count search calls per action | HIGH |
| AF-COST-11 | Orchestration deeper than one delegation layer | Compute max depth of the subagent delegation graph; fail above 1. Each hop bills separately and adds latency | HIGH |
| AF-COST-12 ⚑ | Subagent exists only to retrieve data | Single lookup action, no branching or state mutation — should be a direct action or MCP tool call | MEDIUM |
| AF-COST-13 | More than ~10 tools bound to a single subagent | Count tool bindings. Schemas serialize into every LLM call in that scope | HIGH |
| AF-COST-14 | Instruction block exceeds ~200 lines | A per-call token tax on every reasoning step, and past 10,000 tokens it crosses into extra billing | MEDIUM |

**Report cost as arithmetic the customer can check.** *"The WISMO path fires 5 actions = 100 credits ≈ $0.50 per conversation; at a forecast 2,000 conversations/day that is 100K credits/day ≈ $500/day."* Name the assumed rate and pricing model inline so the figure is auditable. Where a design is defensible but expensive, write it as a trade-off rather than a defect.

**Org-level consumption risks are out of scope for a config review** — unmetered PSL stack completeness, RAG Quality sample rate, builder and preview burn, unstructured ingestion at ~150 credits/MB, and non-agent Einstein features drawing on the same credit pool. These are real and often larger than anything in the config, but a metadata review cannot see them. Request them as disclosures rather than asserting them.
