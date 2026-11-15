# agentforce-workshop-facilitator

**Version:** 1.1.0  
**Author:** Salesforce Forward Deployed Engineering  
**Output:** `[CustomerName]_Agentforce_Workshop_Output.docx` — branded to the **customer's** own logo + colours

---

## What this skill does

Turns raw workshop inputs — a whiteboard photo, stakeholder list, or spoken use cases — into a structured, customer-ready Workshop Output Document.

Covers the full arc:

1. **Pre-workshop:** Tailored question bank (20+ questions, 8 categories, prioritized by stakeholder)
2. **During workshop:** Stakeholder map + structured use case capture (13 fields per use case, readiness scoring)
3. **Post-workshop:** Branded `.docx` with Executive Summary, Use Case Catalogue, Stakeholder Map, Scope, Constraints, Success Criteria, Open Items, and Next Steps

Framework-agnostic — works with any FDE facilitation style (5-column whiteboard, TriNet-style readiness assessment, SEAP use case review, or freestyle).

---

## Trigger

Say any of:
- `/agentforce-workshop-facilitator`
- "run a workshop for [Customer]"
- "help me prep for an Agentforce discovery session"
- "build the workshop output doc"
- "generate a use case catalogue from this whiteboard"

---

## Minimum required inputs

| Input | Example |
|---|---|
| Customer name | Rogers, TriNet, OpenTable |
| Industry | Telecom, HR/Benefits, Hospitality |
| Agent type(s) | Service Agent, SDR Agent, Employee Agent |
| Stakeholders (count + roles) | 6 people: CTO, VP Sales, Salesforce Admin, 2 AEs, IT Architect |
| Workshop goal | Discovery / Roadmap / Go-live readiness / Use case expansion |
| Greenfield or existing | Existing — Sales Cloud + Service Cloud live |
| Customer branding (recommended) | Logo file + brand colours — else the skill researches them; Salesforce is the fallback |

---

## Output document sections

| # | Section | Notes |
|---|---|---|
| 1 | Executive Summary | Narrative: themes, readiness posture, path forward |
| 2 | Use Case Catalogue | Full table + summary (count by type, readiness, priority) |
| 3 | Stakeholder Map | Table + Influence/Interest grid |
| 4 | Recommended Scope | P1 use cases + rationale + out-of-scope list |
| 5 | Constraints & Risks | Technical, process, data, compliance |
| 6 | Success Criteria | Measurable outcomes per P1 use case |
| 7 | Open Items | Owner + due date table |
| 8 | Next Steps | Sequenced action plan |
| (conditional) | Compliance & Privacy | Auto-added for FinServ, Healthcare, Government |

---

## Related skills

| Skill | When to use instead |
|---|---|
| `agentforce-config-review` | When reviewing existing agent configuration metadata |
| `agentforce-technical-design-doc` | When documenting agent architecture for handover |
| `developing-agentforce` | When building or modifying agent metadata |
| `testing-agentforce` | When creating functional test cases |
