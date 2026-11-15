# Agentforce Configuration Review Skill

A Codex skill that produces a structured, branded Word document reviewing any Salesforce Agentforce agent configuration for go-live readiness.

---

## What it produces

A `.docx` file (`[OUTPUT_DIR]/agentforce-config-review-[AgentName]-[Date].docx`, where `[OUTPUT_DIR]` is the output folder captured at Step 1 and defaults to `~/Downloads` when the user does not specify one) containing:

| Section | Contents |
|---|---|
| Cover page | Salesforce logo, agent name, customer, date, prepared by |
| Executive Summary | 3-paragraph narrative + composite score |
| Sections 1–7 (Dimensions 1–7) | Passes, findings table (severity-coloured), numbered fixes |
| D8 body section — Permissions, Identity & Access Control | Running user identity, permission sets + PSL licenses, findings table, SOQL follow-up checklist. Placed between D7 and the Scorecard. Required for Service/SDR agents; N/A for Employee/Field Service/AgentScript. Included only when it was run. |
| D9 body section — Cost & Consumption Efficiency | Pricing model + assumed rate, modeled path cost table (Path \| Billable Actions \| Credits \| USD), findings table, and Vendor Disclosures list. Placed after D8, before the Scorecard. Included only when it was run. |
| Section 8 — Configuration Health Scorecard | Score per dimension (colour-coded), composite score (7-dimension average) + a "Permission Readiness" row (D8) and a "Consumption Posture" row (D9) — both supplemental, excluded from composite |
| Section 9 — Priority Remediation Summary | All CRITICAL + blocking HIGH items ranked — includes D8 and D9 findings at full severity |
| Section 10 — KPI / Success Criteria | KPIs with benchmarks and measurability status |
| Section 11 — Adversarial Test Suite (optional) | Garak-scoped probes, included only when Garak generation was opted into |
| Score Disclaimer | FDE validation callout |
| Action schema findings | Incorporated directly into the relevant dimension sections — not a separate section |

Scores are colour-coded: **green** (8–10) → **amber** (6–7) → **orange** (4–5) → **red** (1–3).

---

## How to invoke

Use `$agentforce-config-review` in Codex, then paste your agent configuration metadata.

The skill works best when you provide:

| Input | Why it matters |
|---|---|
| Agent name + type | Scopes which checks apply |
| Agent role, topic instructions | Primary review input |
| `genAiPlannerBundles/` local action schema files (`schema.json`) | Required for action-schema review — findings feed Dimensions 2–7 (see below) |
| `genAiPlanners/` planner XML | Topic instruction and escalation binding |
| `genAiFunctions/` or `genAiPlugins/` | Action I/O mappings |
| Customer name, industry, geography | Drives CASL/PIPEDA/GDPR compliance checks |
| LLM backend + data residency requirement | Required for Dimension 6 |
| Known bugs or prior incidents | Seeds findings with real failure history |
| **Prepared by** (name + team) | Appears on cover page — defaults to `"Forward Deployed Engineering"` if not provided |

If you're working in a local Salesforce DX project, the skill will scan for action schemas automatically before starting analysis.

---

## The 9 review dimensions

The composite Configuration Health Score is the **average of Dimensions 1–7**. Dimensions 8 and 9 are supplemental — excluded from the composite so they don't skew the average, but their findings feed the Priority Remediation Summary at full severity and can block go-live.

| # | Dimension | Key checks |
|---|---|---|
| 1 | Persona, Tone & Topic Scope | Role clarity, bilingual consistency, topic boundary conditions |
| 2 | Instructions, Actions & Fallback | Action sequencing, null guards, knowledge boundary, fallback chains |
| 3 | Guardrails, Safety & Responsible AI | Prompt injection, persona hijack, PII guardrail, human escalation, OWASP LLM Top 10 |
| 4 | Variable Typing & Data Integrity | Boolean/text mismatches, ID binding correctness, stale variables |
| 5 | Knowledge Grounding | Mandatory KB action, no-result fallback, hallucination risk, source quality |
| 6 | Data Residency & AI Governance | LLM endpoint, PII masking, PIPEDA/GDPR, Einstein Trust Layer |
| 7 | CRM Integration & Logging | Activity logging, retry/dead-letter, single points of failure |
| 8 | Permissions, Identity & Access Control *(Supplemental — excluded from composite)* | Running user identity, Apex class access, Object CRUD, FLS, Named Credentials, PSL license (voice). **REQUIRED for Service and SDR/Sales agents** (not optional for those types); N/A for Employee, Field Service, and AgentScript agents. Needs action-schema metadata or an org connection to run; marked `NOT RUN — metadata required` if neither is available. Findings feed Priority Remediation at full severity. |
| 9 | Cost & Consumption Efficiency *(Supplemental — excluded from composite)* | Billable-action counts per conversation path, credit/USD modeling, wasteful action sequencing, over-broad retrieval. Gated on establishing the pricing model first; marked `NOT RUN — pricing model unknown` if it can't be determined. Findings feed Priority Remediation at full severity. |

---

## Why action schemas matter

Before starting analysis, the skill always runs:

```bash
find <project>/force-app/main/default/genAiPlannerBundles -type f -name "schema.json" | sort
```

Action input/output schemas reveal findings invisible from bot-meta alone. These findings are incorporated **directly into the relevant dimension** — not held in a separate section:

| Schema issue | Filed in |
|---|---|
| `isDisplayable:true` on PII-carrying outputs | Dimension 6 (Data Residency) |
| Hardcoded values in `description` fields | Dimension 2 (Instructions) |
| `isUserInput:true` on write/query actions | Dimension 3 (Guardrails) |
| Two-hop injection via `isUsedByPlanner:true` | Dimension 3 (Guardrails) |
| `citationsEnabled: const:false` in schema | Dimension 5 (Knowledge Grounding) |
| Type mismatch between schema and context variable | Dimension 4 (Variable Typing) |
| Action failure output not handled | Dimension 7 (CRM Integration) |
| `isDisplayable:true` leaking CRM data | Dimension 3 (Guardrails) |

Findings sourced from action schemas are labelled `[action schema]` so the FDE can distinguish confirmed metadata findings from findings inferred from instruction text.

---

## How the document is built

The skill uses a **two-phase token budget** to prevent context exhaustion mid-build:

```
Phase 1 (main session):   Gather context → Static-check scan (Step 1b) → Analyse D1–D7
                           + D8 (Service/SDR) + D9 → Write findings to JSON
                                                                            ↓
Phase 2 (sub-agent):      Read JSON → Run build scripts → Output .docx
```

A **static-check scan (Step 1b)** runs before the dimension analysis, evaluating the configuration against `references/static-checks.md` (61 mechanically decidable rules). Each rule is tagged with the dimension it files into — for example `AF-COST` rules file into Dimension 9.

The JSON gate is mandatory — the sub-agent is never spawned until `[OUTPUT_DIR]/review-findings-[AgentName].json` is confirmed written (`[OUTPUT_DIR]` defaults to `~/Downloads`). This means even if the main session runs long, the document build always starts from a clean context.

**Analysis is split across two turns:**
- Turn 1: Dimensions 1–3 → pause for confirmation
- Turn 2: Dimensions 4–7 + D8 (required for Service/SDR agents) + D9 + scores + KPIs + remediation + JSON write + sub-agent spawn

---

## Work with large reviews

Review one coherent group of topics at a time and save compact findings. Validate the complete findings JSON before building the report. If document generation is interrupted, resume using the JSON and the last verified document section. Render with the available document tool or use the local Python option described in the report reference.

## Branding

Documents use official Salesforce brand assets:

| Element | Spec |
|---|---|
| Cover page | Salesforce cloud logo (1.6", centered) + "Agentforce" in SF Blue + thin blue accent bar + DEEP_NAVY strip with title/metadata |
| Body header | Salesforce logo (0.25" height) + "Forward Deployed Engineering \| Agentforce Configuration Review" + DEEP_NAVY bottom rule |
| Section headings | DEEP_NAVY pill background, WHITE bold text |
| SF Blue | `#00A1E0` |
| Deep Navy | `#032D60` |
| Logo asset | `assets/salesforce-logo.png` (bundled with skill — no network dependency) |

The cover page `prepared_by` field is dynamic — it comes from the `prepared_by` key in the findings JSON and defaults to `"Forward Deployed Engineering"` if not set.

---

## File locations

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition — operational instructions for the assistant |
| `README.md` | This file |
| `references/review-prompt.md` | Analysis prompt template — paste config here |
| `references/agent-type-variants.md` | Agent-type-specific checks (SDR, Service, Field Service, Employee) |
| `references/garak-scoped-probes.md` | Adversarial test case generation (optional Section 11) |
| `references/static-checks.md` | Static check catalog — 61 mechanically decidable rules, run at Step 1b |
| `[OUTPUT_DIR]/review-findings-[AgentName].json` | Findings JSON — written before doc build, read by sub-agent (`[OUTPUT_DIR]` defaults to `~/Downloads`) |
| `[OUTPUT_DIR]/agentforce-config-review-[AgentName]-[Date].docx` | Output document (`[OUTPUT_DIR]` defaults to `~/Downloads`) |

---

## Skill version

**v1.9.0** — July 2026

Changes from v1.8.0:
- Output location is now customizable — capture an `[OUTPUT_DIR]` at Step 1; all artifacts (findings JSON, `.docx`, Garak CSV, builder scripts) resolve against it. Defaults to `~/Downloads` when the user does not specify one; no path is hardcoded anymore. The doc-builder sub-agent receives the resolved absolute path since it runs in a clean context.
- Added two mechanical AgentScript deployability rules to the static-check catalog (now 61 rules) and the AgentScript variant: **AF-REL-16** (script exceeds ~20,000 lines) and **AF-REL-17** (compiled bundle exceeds ~20 MB), both HIGH — size/complexity ceilings that predict slow compiles, editor/Metadata-API failures, and per-call token bloat, and are invisible in the builder UI.

### Earlier versions

**v1.8.0** — July 2026

Changes from v1.7.0:
- Added Step 1b — static check scan against `references/static-checks.md`, 59 mechanically decidable rules with namespaced IDs, each tagged with the dimension it files into
- Added Dimension 9 (Supplemental) — Cost & Consumption Efficiency; excluded from the composite score, findings feed Priority Remediation at full severity, gated on establishing the pricing model first
- Corrected D6: Einstein Trust Layer LLM data masking is disabled for Agentforce agents by design, so the org-level Setup toggle does not verify a control for an agent; a vendor claim citing masking as the agent's PII control is now a HIGH finding
- Findings JSON gains `cost` and `static_scan` blocks; doc-builder gains Script 7 and a "Consumption Posture" scorecard row
- Frontmatter version reconciled with this history — it read `1.6.0` while this file already labelled the D8 release v1.7.0

**v1.7.0** — June 2026

Changes from v1.6.0:
- Added Dimension 8 (Supplemental) — Permissions, Identity & Access Control
- Composite score remains 7-dimension average; D8 findings feed Priority Remediation at full severity
- D8 metadata gate: action schemas must be read before any finding is filed
- Service/SDR: dedicated running user permission set queries (Apex, CRUD, FLS, Named Credentials, PSL licenses)
- Voice: `ServicePlannerAgentUserPsl` PSL check replaces VoiceCall ObjectPermissions query (always returns zero — false positive)
- Employee: running-user-context variant — checks instruction/design assumptions, not permission sets
- v1.6.0 files preserved in `versions/`

Changes from v1.6.0 (PR — marketplace prep):
- Cross-skill references updated to canonical names: `sf-ai-agentforce` → `developing-agentforce`, `sf-ai-agentforce-testing` → `testing-agentforce`, `sf-ai-adversarial-testing` / `sf-ai-agentforce-observability` → `observing-agentforce`
- Personal paths made portable: `/Users/skhalid/Downloads/...` → `~/Downloads/...`
- Customer names genericized: competitor names, persona names, and customer-specific references replaced with `[Customer]` / `[Competitor]` / `[PersonaName]` / "user"
- Salesforce logo bundled at `assets/salesforce-logo.png`; sub-agent prompt reads from relative skill path instead of fetching from wikimedia.org
