# Phase 4 — Workshop Output Document

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Phase 4 — Workshop Output Document
  - JSON context file
  - Sub-agent prompt
- Document Structure (8 sections standard)
- .docx Style Standard
  - Colour palette — map from the `brand` object
  - python-docx script structure (3 scripts)

## Phase 4 — Workshop Output Document

After Phases 1–3, serialize the workshop context and use the available document authoring capability. The script procedure below is a local option. The handoff prompt is reusable when delegation is available and authorized.

### JSON context file

Write to: `~/Downloads/workshop-context-[CustomerName].json`

Schema:
```json
{
  "customer_name": "",
  "industry": "",
  "agent_types": [],
  "workshop_goals": "",
  "clouds": [],
  "greenfield": true,
  "prepared_by": "Forward Deployed Engineering",
  "workshop_date": "",
  "regulatory_context": [],
  "brand": {
    "source": "user-provided | researched | salesforce-fallback",
    "primary": [0, 0, 0],
    "secondary": [0, 0, 0],
    "dark_text": [39, 35, 51],
    "light_row_tint": [244, 243, 245],
    "logo_path": "/tmp/[customer]-logo.png",
    "cover_style": "light",
    "notes": "How primary/secondary/dark are used; any logo usage constraints"
  },
  "stakeholders": [
    {
      "name": "",
      "role": "",
      "department": "",
      "raci": "",
      "decision_authority": "",
      "engagement_level": "",
      "notes": ""
    }
  ],
  "use_cases": [
    {
      "id": 1,
      "name": "",
      "description": "",
      "agent_type": "",
      "clouds": [],
      "trigger": "",
      "key_actions": [],
      "data_required": [],
      "systems": [],
      "licensing": "",
      "pilot_readiness": "",
      "priority": "",
      "status": "",
      "notes": ""
    }
  ],
  "question_bank": [
    {
      "id": 1,
      "question": "",
      "category": "",
      "stakeholder_target": "",
      "priority": ""
    }
  ],
  "executive_summary": "",
  "scope_in": [],
  "scope_out": [],
  "constraints": [],
  "success_criteria": [],
  "open_items": [],
  "next_steps": [],
  "compliance_notes": "",
  "include_compliance_section": false
}
```

### Sub-agent prompt

If delegation is available and authorized, use the prompt below. Otherwise, follow it in the current session.

> Read the JSON file at `~/Downloads/workshop-context-[CustomerName].json`.
> Generate a python-docx script named `build_workshop_[CustomerName].py` in `/tmp/` and run it.
> The script must produce `~/Downloads/[CustomerName]_Agentforce_Workshop_Output.docx`.
> Use the document structure and style standard defined in this skill's own `SKILL.md`
> (`<skill-dir>/SKILL.md`). The main session must substitute the concrete absolute path here,
> since the sub-agent runs in a clean context — pass the installed plugin's skill path, or the
> `~/.agents/skills/agentforce-workshop-facilitator/SKILL.md` personal-install fallback.
> **Brand the document using the JSON `brand` object** — use `brand.primary`/`brand.secondary`/
> `brand.dark_text` RGB values (NOT the Salesforce navy/blue) and embed `brand.logo_path` on the
> cover. Honour `brand.cover_style` (`light` = white cover with dark brand-colour text; `dark` =
> dark full-bleed cover). Use the accent colour only for thin rules, table-header accents, and
> callout borders — never as a full-row or full-section fill. If `brand.source` is
> `salesforce-fallback`, use the Salesforce palette + logo instead.
> Write the script, run it with python3, and confirm the output file exists and is > 30KB.

---

## Document Structure (8 sections standard)

The output document is customer-facing. Write in professional, clear language. Do not expose internal SF metadata terms (GenAiPlanner, InternalCopilot, etc.).

| Section | Title | Content |
|---|---|---|
| 1 | Executive Summary | 2–3 paragraph narrative: why this workshop happened, top themes, readiness posture, recommended path forward |
| 2 | Use Case Catalogue | Full use case table from Phase 3 + Use Case Summary (counts by type, readiness, priority) |
| 3 | Stakeholder Map | Table from Phase 2 + Influence/Interest grid summary |
| 4 | Recommended Scope | Prioritized list of P1 use cases with rationale; out-of-scope list |
| 5 | Constraints & Risks | Technical, process, data, and compliance constraints identified during the session |
| 6 | Success Criteria | Measurable outcomes for each P1 use case (deflection rate, handle time, CSAT, etc.) |
| 7 | Open Items | Table: Item | Owner | Due Date | Status |
| 8 | Next Steps | Table: Action | Owner | Due Date — sequenced and numbered |
| (conditional) | Compliance & Privacy | Only added if `include_compliance_section: true` — regulations, ETL requirements, data residency |

**Section 7 — Open Items table schema:**

| # | Open Item | Owner | Due Date | Status |
|---|---|---|---|---|
| 1 | … | … | [TBD] | Open |

**Section 8 — Next Steps table schema:**

| # | Action | Owner | Due Date |
|---|---|---|---|
| 1 | … | … | [TBD] |

---

## .docx Style Standard

The document is **branded to the customer** using the JSON `brand` object resolved in Step 1b.
The layout/structure below is fixed; the **colours and logo are driven by `brand`**. The
Salesforce palette is only the fallback (`brand.source == "salesforce-fallback"`).

### Colour palette — map from the `brand` object
| Role | Source | Used for |
|---|---|---|
| **dark** | `brand.dark_text` | Section-header backgrounds, headings, body text (and the cover background if `cover_style: "dark"`) |
| **primary/accent** | `brand.primary` | Thin accent rules, table-header accents, section-number prefix, callout left-borders — NEVER a full-row/section fill |
| **secondary** | `brand.secondary` | Sparing emphasis only (e.g. HIGH-priority tags) |
| **light tint** | `brand.light_row_tint` (default `(244,243,245)`) | Alternating table data rows, callout backgrounds |
| **white** | `(255,255,255)` | Cover background when `cover_style: "light"`; text on dark fills |
| amber `(244,166,35)` | fixed | Risk/constraint callouts (skip if it clashes with brand; use `brand.primary` border instead) |
| green `(46,125,50)` | fixed | Success/positive callouts |

**Salesforce fallback palette** (only when `brand.source == "salesforce-fallback"`):
- `navy = (3, 45, 96)`, `blue = (0, 161, 224)`, `light_blue = (232, 244, 253)`, `dark_text = (33, 33, 33)`, logo `assets/salesforce-logo.png`.

### python-docx script structure (3 scripts)

Split across 3 scripts to stay within context limits:

| Script | File | Content |
|---|---|---|
| Script 1 | `build_workshop_[CustomerName]_p1.py` | Document setup, CSS equivalent (styles), Cover page, Section 1 (Executive Summary) |
| Script 2 | `build_workshop_[CustomerName]_p2.py` | Sections 2–4 (Use Cases, Stakeholder Map, Scope) |
| Script 3 | `build_workshop_[CustomerName]_p3.py` | Sections 5–8 (Constraints, Success Criteria, Open Items, Next Steps) + optional Compliance section + save |

Each script opens the in-progress `.docx` file and appends to it except Script 1 which creates it.

**Cover page elements** (driven by `brand.cover_style`):
- `light` (default, safe for dark/mono logos): white background; **dark** brand-colour title; bold **primary/accent** rule under the title; logo top-centre.
- `dark` (only for light/reversed logos): full-page **dark** brand-colour background; logo top; title in white; subtitle in the **primary/accent** colour.
- Customer logo from `brand.logo_path` (fallback: `assets/salesforce-logo.png`). Keep it square if square; never stretch.
- Customer name large (28pt bold) — dark text on a light cover, white on a dark cover.
- "Agentforce Discovery Workshop" subtitle (18pt) in the primary/accent colour.
- Prepared by, date, confidentiality note in small text at bottom (dark on light cover, white on dark cover).

**Section headers:** **dark** brand-colour background, white bold text, 14pt, all caps. Number prefix in the **primary/accent** colour.

**Tables:**
- Header row: **dark** brand-colour background, white bold text, 10pt (accent used as a thin rule, not the fill).
- Data rows: alternating white and **light tint** (`brand.light_row_tint`), 9pt, 1.2 line spacing.
- Borders: thin light grey (0.5pt).

**Callout boxes:**
- Risk/Constraint: **primary/accent** (or amber) left border (4pt), light tint background.
- Success/Positive: green left border (4pt), light green background.
- Info/Note: **primary/accent** left border (4pt), light tint background.

---
