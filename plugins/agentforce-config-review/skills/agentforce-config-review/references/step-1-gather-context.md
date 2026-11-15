# Step 1 — Gather Context

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Step 1 — Gather Context

Before reviewing, confirm or ask for:

| Field | Why needed |
|---|---|
| Agent name + type (SDR / Service / Field Service / Employee) | Scopes which review checks apply |
| Agent role, description, and topic instructions | Primary review input |
| **GenAI Planner file** (`genAiPlanners/[PlannerName].genAiPlanner-meta.xml`) | Required for topic instruction, action binding, and escalation analysis — without this, D2 findings are inferred not confirmed |
| **GenAI Function / Plugin files** (`genAiFunctions/` or `genAiPlugins/`) | Required for reviewing action input/output mappings, variable bindings, and action failure paths |
| Known prior issues or bugs | Seeds the review with real failure history |
| Customer name, industry, geography | Drives compliance checks (CASL, PIPEDA, GDPR, etc.). If industry is **healthcare, life sciences, financial services, insurance, or pharma** (or unclear — ask *"Is this agent part of a regulated industry?"*), it triggers **Step 2b** (regulated-industry guardrail review via the `regulated-industry-agents-review` skill). |
| LLM backend and data residency requirement | Required for Section 6 |
| Output audience (engineering, leadership, customer-facing) | Calibrates tone of findings |
| Grounding materials available? (PDFs, URLs, KB articles, SharePoint) | Required for Section 5 Intelligent Context assessment |
| Generate Garak adversarial test cases? (yes / no) | If yes: produces Testing Center CSV + Word doc Section 11 |
| **Prepared by** (name + team, e.g. "Sarah Khalid, Forward Deployed Engineering") | Appears on cover page — ask if not already known; default to `"Forward Deployed Engineering"` if no name provided |
| **Output directory** (where the review artifacts are written) | Optional. Capture as `[OUTPUT_DIR]`. If the user does not specify one, default to `~/Downloads`. Every artifact this skill writes — findings JSON, `.docx`, Garak CSV, builder scripts — resolves against this directory; do not hardcode `~/Downloads` anywhere once a value is set. Expand `~` and create the directory if it does not exist before the first write. |
| **Dedicated running user** (username or name) + permission set name(s) — *Service / SDR agents only* | **REQUIRED for D8 — do not defer.** If unknown, the skill will query the org directly in Turn 2 (Section A). If the org is not connected and no metadata is available, D8 will be marked NOT RUN. Do not skip asking for this — D8 is mandatory for these agent types. Not applicable for Employee Agents (running user context — see agent-type-variants.md). |

If the user pastes a full configuration block, infer as much as possible and proceed without blocking questions.

**If planner or action metadata is absent**, explicitly flag in the document which findings in Sections 2, 4, and 7 are **inferred from bot dialog structure** rather than confirmed from topic/action source files. Use the label `[INFERRED — planner not reviewed]` on affected findings. This is not a blocker for producing the document, but the FDE must validate these findings against the live planner before sharing the review with the customer.

**REQUIRED — Always retrieve and read action schemas before starting analysis. This is not optional.**

Before writing a single finding, run these discovery commands to locate all action metadata in the local project:

```bash
# 1. Find the planner bundle and all local action input/output schemas
find <project-root>/force-app/main/default/genAiPlannerBundles -type f -name "schema.json" | sort

# 2. Find any GenAiPlugin or GenAiFunction files
find <project-root>/force-app/main/default -type f \( -name "*.genAiPlugin-meta.xml" -o -name "*.genAiFunction-meta.xml" \) | sort

# 3. Read each schema.json found — input and output — for every action in the bundle
```

**Why this matters:** Action input/output schemas reveal findings that are invisible from bot-meta and planner instruction text alone:
- `isDisplayable:true` on action outputs that carry PII (customer name, email, phone, case content) — surfaces data to user session unnecessarily
- Hardcoded values in schema `description` fields used as LLM-facing instructions (unreliable enforcement)
- `copilotAction:isUserInput:true` on output-bound fields creating data exfiltration paths
- `citationsEnabled: const:false` hardcoded at schema level (not overridable via botVersion)
- Two-hop injection paths: action output marked `isUsedByPlanner:true` flowing raw user content back into planner context
- Actions marked `isDisplayable:true` on outputs that expose CRM record data to the user session

**Failure to read action schemas before analysis will produce an incomplete review.** Action schema findings must be incorporated directly into the relevant dimensions — they are not a separate section or a supplement added afterwards.

**Retrieval note:** `GenAiPlannerBundle` throws an `UNKNOWN_EXCEPTION` on some sandbox orgs at API v66/v67 — this is a known platform bug. Retrieve `GenAiPlugin` and `GenAiFunction` separately; they succeed independently. Use: `sf project retrieve start --metadata "GenAiPlugin" --target-org <alias>` and `sf project retrieve start --metadata "GenAiFunction" --target-org <alias>`. If the local project already has `genAiPlannerBundles/` or `agents/` directories, read those directly instead of retrieving.

**How to incorporate action schema findings:** When a schema check reveals an issue, file it in the dimension it belongs to — not in a separate section:
- `isDisplayable:true` on PII-carrying outputs → **Dimension 6** (Data Residency & AI Governance)
- Hardcoded values in schema `description` fields → **Dimension 2** (Instructions, Actions & Fallback)
- `isUserInput:true` on query/write actions → **Dimension 3** (Guardrails — data exfiltration/injection)
- `citationsEnabled: const:false` at schema level → **Dimension 5** (Knowledge Grounding)
- Two-hop injection (`isUsedByPlanner:true` on action that receives raw user content) → **Dimension 3** (Guardrails — prompt injection)
- `isDisplayable:true` exposing CRM data to session → **Dimension 3** (Guardrails — PII/data leakage)
- Action output not handled on failure (`isSuccess` not checked) → **Dimension 7** (CRM Integration & Error Handling)
- Variable type mismatch between action schema and context variable → **Dimension 4** (Variable Typing & Data Integrity)

Mark any finding sourced from an action schema with `[action schema]` in the label so the FDE knows it was confirmed from metadata, not inferred from instructions.

---
