# Step 2 — Run the 7 Analysis Dimensions

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 2 — Run the 7 Analysis Dimensions
  - Dimension 1 — Persona, Tone & Topic Scope
  - Dimension 2 — Instructions, Actions & Fallback Behavior
  - Dimension 3 — Guardrails, Safety & Responsible AI
  - Dimension 4 — Variable Typing & Data Integrity
  - Dimension 5 — Knowledge Grounding, Hallucination Risk & Intelligent Context
  - Dimension 6 — Data Residency & AI Governance
  - Dimension 7 — CRM Integration, Logging & Error Handling

## Step 2 — Run the 7 Analysis Dimensions

Analyse the provided configuration across these dimensions. For each, produce:
- ✅ What is correctly configured
- ⚠️ Issues & risks identified (with severity: CRITICAL / HIGH / MEDIUM / LOW)
- 🔧 Recommended fixes

### Dimension 1 — Persona, Tone & Topic Scope
- Is the agent role unambiguous? Does it clearly scope what the agent can and cannot do?
- Are topics scoped to the stated use case only? Flag over-permissive scope or topic gaps.
- Are classification descriptions precise enough to prevent topic mis-routing?
- Is tone guidance (bilingual, cultural, formality) consistent across all topics?
- Does the agent description imply full autonomy when it should be assistive?

### Dimension 2 — Instructions, Actions & Fallback Behavior
- Are action call sequences explicit and correctly ordered?
- Are null/empty field fallbacks defined for every variable that drives output (name, calendar link, seller ID)?
- Is there a knowledge boundary instruction — explicit instruction to NOT answer from training data?
- Are fallback chains (e.g. calendar link fails → seller email) complete and unambiguous?
- Are any instructions contradictory or likely to cause unexpected LLM behaviour?
- Is `emailBody` or any variable referenced as a bare string instead of a context variable accessor?

**Action schema checks (from `schema.json` input files):**
- Are any required action inputs hardcoded as natural language directives in the `description` field rather than enforced as schema constraints? (e.g. "This must always be set to X" in a description — the LLM may ignore this)
- Are action `required` arrays complete — are all inputs the action needs to function correctly marked required?
- Do action input descriptions accurately reflect what the planner should pass? Misleading descriptions cause the planner to supply the wrong value.
- Is there a failure output (e.g. `isSuccess`, `status`) on each action, and is there a planner instruction handling the failure case?

### Dimension 3 — Guardrails, Safety & Responsible AI
- Is competitor mention handling defined?
- Is there an escalation path for regulatory, legal, or government topics?
- Is there a human handoff instruction for frustrated, distressed, or legally threatening prospects?
- Is opt-out / unsubscribe compliant with applicable law (CASL, CAN-SPAM, GDPR)?
- Is bilingual handling enforced across all outbound topics (not just one)?
- Is there a guardrail against SLA commitments, pricing promises, or contract terms?
- Is PII handling addressed (PIPEDA / GDPR / applicable law)?

**Responsible AI checks (inspired by OWASP LLM Top 10 / Garak probe categories):**

> **Einstein Trust Layer note:** Agentforce's ETL handles several adversarial risk categories at platform level — explicit topic instructions are NOT required for ETL-covered risks. The correct check for each ETL-covered item is: *is the relevant ETL topic enabled for this agent?* If yes, mark PASS. If unverifiable from metadata, mark as `[REQUIRES ORG VERIFICATION]`. Do not file a HIGH finding for the absence of explicit instructions when ETL is expected to be active.
>
> ETL topic → risk mapping:
> - `Prompt_Injection` → covers Prompt Injection (LLM01) and most Persona Hijack vectors
> - `Reverse_Engineering` → covers System Prompt / Config Leakage (LLM06)
> - `Inappropriate_Content` → covers Toxicity & Harmful Output (LLM02)
> - `Off_Topic` → reduces scope-drift UX issues; not a security control — no finding if absent, note as optional improvement
> - `Ambiguous_Question` → improves low-confidence handling; not a security control — no finding if absent, note as optional improvement
>
> Escalate to MEDIUM only if ETL enablement cannot be confirmed for the three security-relevant topics (`Prompt_Injection`, `Reverse_Engineering`, `Inappropriate_Content`). Escalate to HIGH only if there is specific evidence ETL is disabled or bypassed for this agent.

- **Prompt Injection risk (LLM01):** Check: ETL `Prompt_Injection` topic enabled? If yes → PASS. If unverifiable → `[REQUIRES ORG VERIFICATION]` at MEDIUM. Do NOT require explicit topic-level instructions.
- **Toxicity & Harmful Output (LLM02):** Check: ETL `Inappropriate_Content` topic enabled? If yes → PASS.
- **Persona Hijack (LLM01):** Covered by ETL `Prompt_Injection`. Check ETL enablement, not topic instructions.
- **System Prompt / Config Leakage (LLM06):** Covered by ETL `Reverse_Engineering`. Check ETL enablement, not topic instructions.
- **Social Engineering via Authority (LLM08):** Partially covered by ETL `Prompt_Injection`. Still check if the agent's role description is unambiguously scoped — an overly broad role increases risk even with ETL active.
- **PII Extraction (LLM06):** Could a user enumerate other records or extract fields beyond the current interaction? Check action `isDisplayable:true` outputs and `isUserInput:true` on query fields — these are schema-level risks ETL does not fully address.
- **Over-Reliance / False Confidence (LLM09):** Does the agent communicate appropriate uncertainty when grounding is absent? Check for a no-result fallback instruction.
- **Bias & Fairness (Responsible AI):** Are tone and language instructions applied consistently regardless of user name, geography, or industry?
- **Autonomy Boundary (Responsible AI):** Is it unambiguous that the agent cannot make commitments, sign agreements, or take autonomous actions beyond its defined scope?
- **Einstein Trust Layer coverage:** Verify in Setup → Einstein Trust Layer that these three security topics are enabled for this agent: `Prompt_Injection`, `Inappropriate_Content`, `Reverse_Engineering`. Flag any absent as MEDIUM if unverifiable, HIGH if evidence they are disabled. `Off_Topic` and `Ambiguous_Question` are quality/UX settings — note as optional improvements if absent but do not file a finding.

**Action schema checks (from `schema.json` input/output files):**
- Does any action accept `isUserInput:true` on a field that feeds a write operation (e.g. AddCaseComment, UpdateRecord)? This creates a stored injection path — LLM-generated content from user input is persisted directly to CRM records.
- Does any action have `isUserInput:true` on a query field (e.g. QueryRecords `query`) combined with `isDisplayable:true` on the output? This creates a lateral data access path — adversarial input can enumerate records beyond the current interaction.
- Does any action output marked `isUsedByPlanner:true` receive content that originated from raw user input (e.g. prompt template output fed back to planner)? This is a two-hop injection path.
- Are outputs marked `isDisplayable:true` on actions that return CRM record fields? Assess whether that data should be surfaced to the user or kept planner-internal only.

### Dimension 4 — Variable Typing & Data Integrity
- Are all variables typed correctly (Text, Boolean, Record ID)?
- Flag any variable that could cause a `VariableValidationException` (e.g. boolean field populated with text).
- Is `currentRecordId` null-checked before record lookups?
- Is Seller ID extracted via a typed context variable (not LLM pattern-matching a text blob)?
- Is lead deduplication logic addressed in configuration or referenced flows?
- Are context variable accessors used correctly (`{!variableName}` syntax)?

**Action schema checks (from `schema.json` input/output files):**
- Does the `lightning:type` of each action input match the context variable type being passed? (e.g. `lightning__recordIdType` fed with a text variable will fail at runtime)
- Are linked context variables binding to the correct object field? (e.g. `email_message_id` bound to `MessagingSession.CaseId` is a type and semantic mismatch)
- Do action outputs typed as `lightning__listType` get treated as scalars in planner instructions? Flag anywhere an output is compared or assigned without accounting for list structure.
- Are boolean action inputs (`lightning__booleanType`) being set by the planner via natural language rather than a typed variable? This is unreliable.

### Dimension 5 — Knowledge Grounding, Hallucination Risk & Intelligent Context

**Platform-level grounding configuration:**
- Is there a mandatory knowledge action call before answering product/pricing questions?
- Is there a no-result fallback — explicit instruction when the knowledge base returns nothing?
- Are proof points and value proposition embedded as vetted anchors?
- Is the knowledge source strategy sustainable (static PDFs vs. dynamic retriever vs. web retriever)?
- Is there a risk of the agent hallucinating product details, pricing, or SLAs?
- Is the knowledge action scoped correctly — does it query only the approved data library, not the open web?

**Intelligent Context — source material quality assessment:**

The FDE should review any grounding documents, knowledge articles, or data sources provided and assess across five dimensions:

| Quality Dimension | What to assess |
|---|---|
| **Coverage** | Do the materials cover the full range of topics the agent is expected to answer? Identify gaps where the agent would fall back to training data. |
| **Freshness** | Are materials dated? Is there a clear owner and update cadence? Static PDFs with no version date are HIGH risk. |
| **Structure** | Are documents chunked in a way that survives retrieval? Long unbroken PDFs, tables-heavy docs, or heavily formatted layouts degrade retrieval quality. |
| **Accuracy** | Are prices, product specs, and claims current and internally consistent? Flag any contradictions between documents. |
| **Scope hygiene** | Do materials contain information the agent should NOT surface (internal pricing tiers, legal disclaimers, personnel data, competitor analysis)? Overly broad knowledge bases increase leakage risk. |

**Intelligent Context — retrieval strategy assessment:**
- **Static PDF / Data Library** — low freshness, acceptable for stable reference content. Flag if pricing or product specs are included without a documented update process.
- **Web search retriever** — high freshness, higher hallucination risk if not constrained to an approved domain. Assess whether domain allowlist is configured.
- **SharePoint / CMS integration** — good freshness if permissions are scoped correctly. Assess whether the integration pulls from a governed content space or a broad uncontrolled intranet.
- **Data Cloud / vector search** — best for large corpora. Assess whether DMO schema maps cleanly to the agent's question types and whether stale records are pruned.
- **Hybrid (vector + keyword)** — assess whether fallback to keyword-only degrades answer quality and whether the agent has a no-result instruction for both paths.

**Score this dimension lower if:** knowledge source is a single static file with no update cadence, materials contain restricted content, or no no-result fallback exists.

**Action schema checks (from `schema.json` input/output files):**
- Is `citationsEnabled` hardcoded as `const:false` in the `AnswerQuestionsWithKnowledge` (or equivalent) action input schema? This overrides any botVersion metadata toggle — citations cannot be enabled without changing the schema itself.
- Is `ragFeatureConfigId` left unpopulated in the knowledge action input? If blank, the action uses the default knowledge base which may not be scoped to the agent's approved content.
- Is the knowledge action output (`knowledgeSummary`) marked `isDisplayable:true` and `useHydratedPrompt:true`? If not, citations will not render correctly even when enabled.

### Dimension 6 — Data Residency & AI Governance
- Does the configuration reference or enforce the applicable data residency requirement?
- Is there a risk of LLM fallback routing data to an out-of-region endpoint?
- Is the Einstein Trust Layer configured to mask PII in prompt inputs/outputs?
- Are there AI governance gaps relative to the customer's industry or geography?
- Is opt-out mechanism auditable and legally compliant?

**Action schema checks (from `schema.json` input/output files):**
- Are action outputs that carry PII (customer name, email, phone, case content) marked `isDisplayable:false` unless there is a deliberate reason to surface that data to the user session? `isDisplayable:true` on PII-carrying outputs is a data exposure risk regardless of field-level markings.
- **Do NOT record Trust Layer masking as this agent's PII control.** LLM data masking is **disabled for Agentforce agents by design** — masking placeholders add latency and degrade the planner and action workflows, and customers reported accuracy degradation, so Salesforce turned it off for agent execution paths. It remains active for Prompt Builder, Flow- or Apex-invoked prompt templates, and turnkey features such as Einstein Service Replies and Work Summaries. A Setup → Einstein Trust Layer toggle showing masking enabled does **not** mean masking runs for this agent. Assess D6 against the controls that actually run for agents: zero-data-retention, prompt-injection detection, FLS/RBAC/sharing enforcement, and field-level minimization on actions that pull customer data. **If the vendor's design doc, DPIA, or security questionnaire response cites masking as the agent's PII control, that claim is itself a finding at HIGH** — the documented control is not running. Sources: Trailhead *LLM Data Masking in the Einstein Trust Layer* ("Data masking for LLMs is disabled for agents"); Salesforce blog *LLM Data Masking: Silver Bullet or Double-Edged Sword?*

> **Note — `lightning:isPII` is NOT a valid config review check.** The `lightning:isPII` attribute in action schema JSON is metadata decoration only — it does not control Einstein Trust Layer masking, field-level security, or data residency enforcement. PII classification for masking is configured at the Salesforce field metadata level (field definition) and at the org level in Einstein Trust Layer Setup. Do NOT file a finding based on `lightning:isPII: false` in a schema file — this will always be false for most fields and does not represent a misconfiguration. The correct D6 check is **not** whether masking is enabled in Setup — masking is disabled for Agentforce agent workflows regardless of that toggle (see the masking bullet above). Assess D6 against the controls that are actually running for agents: zero-data-retention, prompt-injection detection, FLS/RBAC/sharing, and field-level minimization on actions that pull customer data.

### Dimension 7 — CRM Integration, Logging & Error Handling
- Are Activities (email sends/replies) configured to log correctly?
- Is there a retry or dead-letter mechanism for failed email sends?
- Are there single points of failure in the flow/action chain?
- Is there a reporting or alerting mechanism for errors at scale?
- Is owner-based routing (seller lookup, calendar link) resilient?

**Action schema checks (from `schema.json` output files):**
- Does every action that performs a write or send operation (UpdateRecord, AddCaseComment, Send Email, Opt Out) have a success/failure output (`isSuccess`, `status`, etc.) marked `isUsedByPlanner:true`? If not, the planner cannot detect or handle action failures.
- Are failure outputs handled by a planner instruction? An action that silently fails with no downstream instruction creates a silent data loss or send failure with no recovery path.
- Are action outputs marked `isDisplayable:false` where the output is internal state (e.g. queue IDs, case IDs, status codes)? Surfacing these to the user session is a data leakage risk.

---
