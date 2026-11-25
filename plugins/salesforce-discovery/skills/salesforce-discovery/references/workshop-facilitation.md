# Agentforce Workshop Facilitation & Deliverables

Remain framework-agnostic: capture workshop outputs in the customer's or facilitator's chosen methodology without imposing a mandatory whiteboard layout. Extract whiteboard photos, transcripts, or notes directly, tagging extracted values `[extracted]` and unknowns `[TBD]`.

## Context Intake & Customer Branding

Confirm required inputs before generating artifacts: customer name, industry vertical, primary agent type(s), greenfield vs. existing deployment, stakeholder count/roles, and workshop goals (discovery / roadmap / go-live / value review). Recommended: Salesforce clouds in use, customer branding, known pain points, preparer, and regulatory context.

- **Auto-add Compliance rule:** For **Financial Services**, **Healthcare**, or **Government**, automatically include a Compliance & Privacy Constraints section (applicable regulations such as PIPEDA/GDPR/HIPAA/FINRA, data residency, Einstein Trust Layer constraints). Never downgrade a regulatory gap to a footnote—minimum MEDIUM constraint.
- **Customer-first branding:** Resolve in order: (1) user-supplied logo + hex/RGB palette, (2) verified corporate brand research confirmed with the user, (3) Salesforce navy/blue fallback (`#032D60` / `#00A1E0`).
- **Cover-style rule:** Pick by logo contrast—dark/monochrome wordmark uses a **light cover** (default when unsure); light/reversed mark may use a dark full-bleed cover. Never stretch or recolor logos; use bright accent colors only for thin rules, accents, and callout borders—never full-row fills. Flag third-party trademark clearance for external distribution.

## Phase 1 — Tailored Question Bank

Output as a compact table (`# | Question | Category | Stakeholder Target | Priority`) with a **20-question minimum** (ask which categories to drop if the user requests a shorter bank):

- **8 Categories:** Business Value, Process & Workflow, Data Readiness, Platform Readiness, Stakeholder & Change, Guardrails & Trust, Integration & Actions, Scope & Constraints.
- **Priorities:** `HIGH` (blocks scoping), `MEDIUM` (sizing/risk), `LOW` (optional).
- **Additions:** FinServ (KYC/AML, residency, advisor licensing), Healthcare (PHI scope, HIPAA agent user bounds, EHR integration), Retail (inventory/POS, refund guardrails), Telecom (routing, IVR, subscriber identity), Government (WCAG, classification, sovereign cloud). Greenfield adds licensing/admin capacity/change readiness; Existing adds automation conflicts, bot/IVR displacement, and agent user setup.

## Phase 2 — Stakeholder Map

Output table (`Name | Role/Title | Department | RACI | Decision Authority | Engagement Level | Notes`), using `[TBD]` for missing details—never invent names or titles.

- **RACI:** Responsible / Accountable / Consulted / Informed. **Authority:** Can Approve / Can Recommend / No Authority. **Engagement:** Champion / Supporter / Neutral / Skeptic / Unknown.
- **Influence/Interest Grid:** Place each stakeholder in Manage Closely (High/High), Keep Informed (High Interest/Low Influence), Keep Satisfied (Low Interest/High Influence), or Monitor (Low/Low).

## Phase 3 — Use Case Capture & Coverage Check

Output one row per use case (`# | Use Case Name | Description | Agent Type | Cloud(s) | Trigger | Key Actions | Data Required | Systems | Licensing | Pilot Readiness | Priority | Status | Notes`).

- **Pilot Readiness:** `High` (clean accessible data, clear process, zero integration/compliance blockers, customer-confirmed), `Medium` (1–2 blockers), `Low` (3+ blockers or compliance sign-off required). Never mark a use case `High` without customer confirmation.
- **Use Case Summary:** Count by Agent Type, Pilot Readiness, Priority (`P1`/`P2`/`P3`), and flag zero-coverage blind spots against internal SEAP categories (Account/Contact, Lead/Opportunity, Case/Service, Email/Messaging, Analytics/Reporting, Field Service, HR/Employee, Finance/Billing).
- **Cloud Reference Library (internal ideation only—never copy verbatim into output):** Sales (lead qualification, meeting prep, pipeline coach, proposal drafting, competitive intel), Service (case triage, email drafting, Knowledge suggestions, close summaries, identity verification), Experience (FAQ/product advisor, account self-service, order/returns), SDR (outbound cadence, inbound routing, event follow-up), Employee (HR Q&A, IT helpdesk, onboarding), Field Service (work order scheduling, parts lookup, job closure notes).

## Phase 4 — Customer-Facing Workshop Document & Styling

Deliver structured Markdown or a customer-branded `.docx` using an available authoring tool or Python `python-docx`. Keep structured JSON context (`customer_name`, `brand`, `stakeholders`, `use_cases`, `question_bank`, `scope_in/out`, `constraints`, `success_criteria`, `open_items`, `next_steps`, `include_compliance_section`) beside the deliverable in the approved workspace; if `.docx` tooling is unavailable, return the structured draft and state the missing capability.

- **8 Standard Sections:** (1) Executive Summary, (2) Use Case Catalogue + Summary, (3) Stakeholder Map + Influence/Interest Grid, (4) Recommended Scope (P1 rationale + out-of-scope), (5) Constraints & Risks, (6) Success Criteria, (7) Open Items (`Item | Owner | Due Date | Status`), (8) Next Steps (`Action | Owner | Due Date`), plus conditional (9) Compliance & Privacy Constraints.
- **`.docx` Palette & Cover Standard:**
  - Map `brand.dark_text` to section-header fills (14pt white bold caps), table-header fills (10pt white bold), and body text (9pt).
  - Map `brand.primary` to thin accent rules, section-number prefixes, and 4pt callout left-borders—never full-row fills; map `brand.light_row_tint` to alternating table rows and callout tints; use fixed green (`#2E7D32`) for positive callouts.
  - Drive cover layout by `brand.cover_style` (`light` = white background with dark title + accent rule + top-centered logo; `dark` = dark fill only for light/reversed marks).
- **Modular `.docx` Generation:** For large decks built with `python-docx`, split generation across 3 scripts (cover + Executive Summary, Sections 2–4 tables, Sections 5–8 + optional Compliance) and confirm the output file is non-empty and valid.
- **Language hygiene:** Use customer-facing Agentforce terms (Service Agent, Action, Topic, Einstein Trust Layer). Exclude internal metadata terms (`InternalCopilot`, `ExternalCopilot`, `GenAiPlanner`, `ReAct`, `isUsedByPlanner`, internal org IDs, Jira/GUS tickets, internal Slack references).
