---
name: |-
  agentforce-workshop-facilitator
description: |-
  Prepare and document discovery for an Agentforce workshop. Return tailored questions, use cases, and a customer workshop document. Use agentforce-technical-design-doc for implementation documentation.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.

For industry-specific agents, cross-industry ideation, or role/personality choices, read the selected patterns in [industry and role design](references/shared/industry-patterns.md). Use them within this skill’s ownership; distinguish documented capabilities from proposed designs.


# agentforce-workshop-facilitator: Agentforce Workshop Facilitator Skill

Use this skill when an FDE needs to prepare for, run, or document an Agentforce discovery workshop with a customer.

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## When This Skill Owns the Task

- User wants to prepare a question bank before a customer discovery session
- User is mid-workshop and wants structured use case capture
- User wants a post-workshop output document for customer delivery
- User asks for a stakeholder map or facilitation guide for an Agentforce engagement

Delegate elsewhere when:

- Reviewing existing agent config → `agentforce-config-review`
- Generating architecture / design documentation → `agentforce-technical-design-doc`
- Building or modifying agents → `agentforce-generate`
- Testing agent behavior → `agentforce-test`

---

## Manage the workshop and document handoff

Use compact tables for questions, stakeholders, and captured use cases. Ask for confirmation when a material workshop input or decision is missing. When the captures are ready, keep the structured context beside the deliverable in the approved working directory and use the Phase 4 instructions. Use a document authoring tool available on the current host or render the same structure locally with Python and python-docx. If neither can produce a Word file, return the structured draft and identify the missing capability.

## Step 1 — Gather Context

Before producing any output, confirm or ask for the following:

| Field | Required? | Why needed |
| --- | --- | --- |
| Customer name | Required | Cover page + file naming |
| Industry vertical | Required | Scopes question bank, compliance auto-adds (FinServ/Healthcare/Gov) |
| Primary agent type(s) being discussed | Required | Scopes use case templates and capability checks |
| Greenfield vs. existing Agentforce deployment | Required | Determines question depth on existing config, data readiness |
| Stakeholder count + roles attending | Required | Drives Phase 2 stakeholder map |
| Workshop goals (discovery / roadmap / go-live / value review) | Required | Frames executive summary and next steps |
| Current Salesforce clouds in use | Recommended | Scopes data, integration, and action feasibility questions |
| Customer branding (logo + brand colours) | Recommended | Brands the output `.docx` to the customer — logo on cover, primary/accent/text colours throughout (see "Resolve Customer Branding" below) |
| Known use cases or pain points already discussed | Optional | Pre-seeds Phase 3 use case table |
| Prepared by (FDE name + team) | Optional | Cover page — defaults to "Forward Deployed Engineering" |
| Regulatory context (PIPEDA/GDPR/HIPAA/FINRA) | Optional | Auto-added if industry is FinServ/Healthcare/Gov — otherwise ask |

**If the user provides a whiteboard photo, notes, or transcript:** extract structured data from it and pre-populate Phases 2 and 3. Flag extracted fields with `[extracted]`. Do not invent data not visible in the source.

**Auto-add Compliance section rule:**<br />If industry is Financial Services, Healthcare, or Government, automatically include a Compliance & Privacy Constraints section in the output document (Section 8). List applicable regulations (PIPEDA, GDPR, HIPAA, FINRA as relevant), flag any known data residency requirements, and note Einstein Trust Layer requirements. Do not add this section for other industries unless the user explicitly mentions regulatory context.

---

## Step 1b — Resolve Customer Branding

The output `.docx` must be branded to the **customer**, not to Salesforce. Salesforce navy/blue is only the fallback. Resolve branding in this priority order:

1. **User-provided assets (highest priority).** If the user attaches or points to a logo file and/or gives brand colours, use exactly those. Verify the logo is a valid image and copy it to `/tmp/[customer]-logo.png` (copy first — customer file paths often contain spaces that break python-docx/shell calls).
2. **Research the customer's brand.** If not provided, offer to look up the customer's corporate brand. Use available research tools to find: primary + secondary/accent + dark-text HEX/RGB values, and a usable logo image URL (transparent PNG preferred). Good sources: [brandfetch.com](http://brandfetch.com), the customer's newsroom/press media kit, Wikimedia Commons, the customer site CSS. Confirm the palette with the user before building.
3. **Salesforce fallback.** Only if the customer has no discoverable brand (or the user declines), use the Salesforce palette + `assets/salesforce-logo.png` documented in the .docx Style Standard below.

**Cover-style rule — pick by the LOGO, not the palette:**

- **Dark / monochrome wordmark on transparent** (reads only on white) → use a **LIGHT cover**: white background, dark brand-colour title text, a bold accent-colour rule, logo top-centre. Set `cover_style: "light"`.
- **Light / reversed / white logo** (or a colourful mark that reads on dark) → a dark full-bleed cover in the brand's dark colour is fine. Set `cover_style: "dark"`.
- When unsure, default to a **light cover** — it is safe for almost every logo.

**Guardrails:**

- Never recolour, stretch, or distort a customer logo. Keep clear space. Keep the mark square if it is square.
- Use the accent/primary colour for **thin rules, table-header accents, and callout borders** — do NOT flood full rows or section backgrounds with a bright accent (yellows/oranges/reds especially become unreadable as fills). Use the dark brand colour for section-header fills and body text.
- Third-party marks are trademarks. A Salesforce deliverable *for* the customer is normal engagement usage, but flag to the user that logo use should be cleared if the doc will be distributed beyond the account team.
- Never invent a brand colour or fabricate a logo. If a value is unknown, ask or fall back to Salesforce.

Record the resolved branding in the JSON `brand` object (schema in Phase 4).

---

## Phase 1 — Tailored Question Bank

Generate a question bank tailored to the customer's industry, agent type, and whether this is greenfield or existing. Output as a table — no prose.

**Table schema:**

| # | Question | Category | Stakeholder Target | Priority |
| --- | --- | --- | --- | --- |
| 1 | … | Business Value | Business Sponsor | HIGH |

**Category definitions:**

| Category | Scope |
| --- | --- |
| Business Value | Outcomes, ROI, success metrics, executive drivers |
| Process & Workflow | Current-state process, handoff points, human steps being automated |
| Data Readiness | Data quality, availability, CRM hygiene, integration complexity |
| Platform Readiness | Existing Salesforce/Agentforce config, licenses, API versions |
| Stakeholder & Change | Adoption risk, training needs, champions and blockers |
| Guardrails & Trust | Compliance requirements, escalation paths, trust layer expectations |
| Integration & Actions | External systems, APIs, approval flows, data write operations |
| Scope & Constraints | Timeline, budget, in-scope vs. out-of-scope boundaries |

**Priority definitions:**

- HIGH — must be answered before any use case can be properly scoped
- MEDIUM — important for sizing and risk assessment
- LOW — good to have, skip if time is short

**Industry-specific additions:**

- FinServ: Add questions on KYC/AML policy, data residency (Canadian/EU), advisor licensing constraints
- Healthcare: Add questions on PHI data scope, HIPAA agent user restrictions, Epic/Cerner integration
- Retail: Add questions on inventory system access, POS integration, return/refund policy guardrails
- Telecom: Add questions on case routing logic, existing IVR integration, subscriber identity validation
- Government: Add questions on accessibility standards (WCAG), data classification, sovereign cloud

**Greenfield vs. existing additions:**

- Greenfield: Include questions on Salesforce cloud licensing, admin capacity, change management readiness
- Existing: Include questions on existing automation conflicts, current bot/IVR displacement, agent user setup

**Minimum question count:** 20 questions. If the user wants a shorter guide, ask which categories to drop.

---

## Phase 2 — Stakeholder Map

Produce a stakeholder map for everyone attending or named by the user. Output as a table.

**Table schema:**

| Name | Role / Title | Department | RACI (R/A/C/I) | Decision Authority | Engagement Level | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| … | … | … | … | … | … | … |

**Field definitions:**

- **RACI**: R = Responsible (owns execution), A = Accountable (signs off), C = Consulted (input), I = Informed
- **Decision Authority**: Can Approve / Can Recommend / No Authority
- **Engagement Level**: Champion / Supporter / Neutral / Skeptic / Unknown
- **Notes**: Specific interests, concerns, or context for this person

**If stakeholder details are limited**, generate a placeholder row per role the user named and mark fields as `[TBD]`. Never fabricate names, titles, or org details.

**Add an Influence/Interest grid summary below the table:**

```javascript
High Interest + High Influence → Manage Closely (Champions, Blockers)
High Interest + Low Influence  → Keep Informed (End Users, ICs)
Low Interest + High Influence  → Keep Satisfied (Exec Sponsors)
Low Interest + Low Influence   → Monitor (Adjacent Teams)
```

Place each named stakeholder into the appropriate quadrant.

---

## Phase 3 — Use Case Capture

For each use case discussed, capture a structured record. Output one table row per use case — no prose.

**Table schema:**

| # | Use Case Name | Description | Agent Type | Cloud(s) | Trigger | Key Actions | Data Required | Systems | Licensing | Pilot Readiness | Priority | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | … | 1-line | Service/SDR/Employee/AgentScript | Sales/Service/… | User message / Record event / Schedule | List | What CRM data needed | Salesforce + external | Metered/Unmetered | High/Med/Low | New/In-Flight/Existing | … |  |

**Field definitions:**

| Field | What to capture |
| --- | --- |
| Use Case Name | Short memorable label (e.g. "Case Auto-Triage", "Lead Qualification Bot") |
| Description | One sentence: what it does, who benefits |
| Agent Type | Service Agent / SDR Agent / Employee Agent / AgentScript / Field Service |
| Cloud(s) | Which Salesforce cloud(s) this use case lives in |
| Trigger | How the agent is initiated (user message, record event, scheduled, email2case) |
| Key Actions | Actions the agent takes: QueryRecords, CreateRecord, Send Email, Summarize, etc. |
| Data Required | CRM objects and fields the agent reads or writes |
| Systems | External systems involved (ERP, ticketing, identity, IVR) |
| Licensing | Metered (per conversation) or Unmetered (flat fee) |
| Pilot Readiness | High = ready now; Medium = 1–2 blockers; Low = significant gaps |
| Priority | Relative priority among use cases: P1 / P2 / P3 |
| Status | New / In-Flight / Existing (already live) |
| Notes | Blockers, open items, dependencies |

**Pilot Readiness scoring guide:**

| Score | Criteria |
| --- | --- |
| High | Data is clean and accessible; process is well-defined; no integration dependencies; no compliance blockers |
| Medium | 1–2 blockers present (e.g. data hygiene issue, API not yet available) |
| Low | 3+ blockers or compliance gap that requires legal/IT sign-off before scoping |

**Use case intake from whiteboard or notes:** If the user provides a photo, transcript, or bullet list, extract every use case mentioned and create one row per use case. Mark fields that could not be determined from the source as `[TBD]`.

**SEAP use case category mapping (reference only — do not include in output):**<br />Use this mapping internally to label use cases by Salesforce category for completeness assessment:

- Account & Contact Intelligence
- Lead & Opportunity Management
- Case & Service Management
- Email & Messaging Automation
- Analytics & Reporting
- Field Service Coordination
- HR & Employee Experience
- Finance & Billing Operations

After capturing all rows, produce a **Use Case Summary** showing:

- Total count by Agent Type
- Count by Pilot Readiness (High / Medium / Low)
- Count by Priority (P1 / P2 / P3)
- Any categories from the SEAP map with zero coverage (potential blind spots)

---

## Phase 4 — Workshop Output Document

Consult [`references/phase-4-workshop-document.md`](references/phase-4-workshop-document.md) before Phase 4 (document build, structure, and .docx style). Covers: Document Structure (8 sections standard); .docx Style Standard.

## Use Case Reference Library (internal — do not include in output)

Read [`references/use-case-reference-library.md`](references/use-case-reference-library.md) when tailoring questions or capturing use cases (internal only, never copy into output).

## Constraints & Guardrails

These constraints are non-negotiable and must be applied regardless of customer or use case:

1. **Never invent data.** If a field is unknown, write `[TBD]` — never fabricate names, dates, metrics, or system names.
2. **Never present a use case as "ready" unless the customer confirmed it.** Pilot Readiness = High only when criteria are explicitly met.
3. **Use correct Agentforce terminology.** Service Agent (not "chatbot"), Action (not "function"), Topic (not "intent"), Einstein Trust Layer (not "safety filter").
4. **Flag compliance gaps explicitly.** Do not downgrade a regulatory gap to a note — it is always at minimum a MEDIUM constraint.
5. **Framework-agnostic.** Do not impose the 5-column whiteboard (Role/Channel/Data/Actions/Human Intervention) or any other methodology as a required structure. Use whatever framework the FDE brought to the session — this skill captures output, not process.
6. **Auto-add compliance section for FinServ, Healthcare, and Government.** Set `include_compliance_section: true` automatically.
7. **Customer-facing language only.** The output document must not contain: `InternalCopilot`, `ExternalCopilot`, `GenAiPlanner`, `ReAct`, `isUsedByPlanner`, Salesforce internal org IDs, internal Jira/GUS ticket numbers, or FDE-internal slack references.
8. **Brand to the customer, not Salesforce.** Resolve the customer's logo + colours per Step 1b and drive the `.docx` from the `brand` object. Salesforce navy/blue is only the fallback. Never invent a brand colour or fabricate a logo; choose `cover_style` by the logo (dark/mono wordmark → light cover), and never flood full rows/sections with a bright accent colour.
