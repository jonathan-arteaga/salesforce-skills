# Step 6 — Produce the Word Document

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 6 — Produce the Word Document
  - Why a sub-agent?
  - Sub-agent prompt template
  - Fallback: manual batching

## Step 6 — Produce the Word Document

Use the available document authoring capability. The local Python procedure is an option where Python and python-docx are available. The handoff below can be reused when delegation is available and authorized.

### Why a sub-agent?

By the time analysis (Steps 2–4) is complete, the main session context is heavily loaded with findings text. Use the verified JSON from Step 4a as the compact input. Draft or render by section if the report is large.

### Sub-agent prompt template

When spawning the sub-agent, pass this prompt (fill in the bracketed values). **Substitute `[OUTPUT_DIR]` with the resolved absolute path captured in Step 1** — the sub-agent runs in a clean context and cannot see the main session's variables, so it must receive concrete paths, not a placeholder.

```
You are building a branded Salesforce Agentforce configuration review Word document using python-docx.

Findings are in: [OUTPUT_DIR]/review-findings-[AgentName].json
Logo path (bundled asset): <skill-dir>/assets/salesforce-logo.png
Output file: [OUTPUT_DIR]/agentforce-config-review-[AgentName]-[Date].docx

Read the JSON file first, then write and run these scripts in sequence — ONE per message, wait for result before next.

## Logo download (Script 1 — run once before building the document)
```python
import urllib.request, io
import pathlib, inspect
LOGO_PATH = pathlib.Path(__file__).parent / "assets" / "salesforce-logo.png"
# Fallback for sub-agent context where __file__ is unavailable:
# LOGO_PATH = pathlib.Path.home() / ".agents/skills/agentforce-config-review/assets/salesforce-logo.png"
```

## Brand colours (use RGBColor, not hex strings)
SF_BLUE    = RGBColor(0x00, 0xA1, 0xE0)   # Salesforce brand blue
DEEP_NAVY  = RGBColor(0x03, 0x2D, 0x60)   # Salesforce dark navy
LIGHT_GREY = RGBColor(0xF4, 0xF6, 0xF9)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
BLACK      = RGBColor(0x00, 0x00, 0x00)
GREEN      = RGBColor(0x70, 0xAD, 0x47)
AMBER      = RGBColor(0xFF, 0xC0, 0x00)
ORANGE     = RGBColor(0xFF, 0x66, 0x00)
RED        = RGBColor(0xC0, 0x00, 0x00)

## Cover page (Script 1)
Two visually distinct zones:

Zone 1 — white background (no shading):
- 4 blank spacer paragraphs
- Salesforce cloud logo: doc.add_picture(LOGO_PATH, width=Inches(1.6)), paragraph alignment=CENTER
- "Agentforce" label: SF_BLUE, bold, 18pt, centered
- Accent bar: paragraph with SF_BLUE background shading (#00A1E0), font size 3pt, single space character

Zone 2 — DEEP_NAVY background shading (#032D60) on every paragraph:
- "Configuration Review": WHITE, bold, 30pt, centered
- data['agent_name']: WHITE, 15pt, centered
- data['customer']: SF_BLUE, 13pt, centered
- data['review_date']: WHITE, 11pt, centered
- blank navy line
- "Prepared by: " + data['prepared_by']: WHITE, 11pt, centered
- ~10 blank navy spacer paragraphs
- page break paragraph (navy background)

set_para_bg helper:
  pPr = para._p.get_or_add_pPr()
  shd = OxmlElement('w:shd')
  shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_val)
  pPr.append(shd)

## Body page header (Script 1 — set on doc.sections[0])
- section.different_first_page_header_footer = True  (keeps cover page clean)
- header paragraph: logo run (add_picture height=Inches(0.25)) + tab run ('\tForward Deployed Engineering  |  Agentforce Configuration Review', DEEP_NAVY, 8pt)
- Right-aligned tab stop at pos='8640' twips on the paragraph
- Bottom border on header paragraph: w:pBdr > w:bottom val=single sz=6 color=032D60

## Section headings (all scripts)
DEEP_NAVY paragraph background, WHITE bold 13pt text, "  " prefix:
  p = doc.add_paragraph(); set_para_bg(p, DEEP_NAVY)
  run = p.add_run("  " + text); run.bold=True; run.font.size=Pt(13); run.font.color.rgb=WHITE

## Findings tables (Severity | Finding | Detail)
Column widths: 1.0" | 1.8" | 3.5"
Header row: LIGHT_GREY fill, DEEP_NAVY bold text
Severity cell colours: CRITICAL=RED+WHITE, HIGH=ORANGE+WHITE, MEDIUM=AMBER+BLACK, LOW=LIGHT_GREY+BLACK

## Score disclaimer callout
Paragraph background RGBColor(0xFF, 0xF4, 0xCC), italic 10pt, text colour RGBColor(0x7F, 0x60, 0x00)

Script 1 — Cover page + header + Executive Summary. Save. Verify.
Script 2 — Dimensions 1–4. Save. Verify.
Script 3 — Dimensions 5–7. Save. Verify.
Script 4 — Scorecard (Section 8) + Remediation (Section 9) + KPIs (Section 10) + Score Disclaimer. Verify size > 25KB. Print "DOCUMENT COMPLETE".
  Note for Script 4: After the 7-dimension scorecard table, add a visually separated "Permission Readiness" row:
  - Label (italic): "Permission Readiness (Supplemental — D8)"
  - Status badge: CRITICAL GAPS (RED/WHITE) | HIGH GAPS (ORANGE/WHITE) | NO GAPS CONFIRMED (GREEN/WHITE) | NOT RUN — metadata required (LIGHT_GREY/BLACK)
  - Note (italic, 9pt): "Excluded from composite score — requires org verification. See Priority Remediation for findings."
  - If data['permissions']['status'] == 'NOT_RUN': render the not_run_reason instead of a badge.
  D8 findings (if any) are included in the Priority Remediation table in Section 9 at full severity alongside D1–D7 findings.
Script 5 (optional, only if Garak opted in) — Adversarial Test Suite (Section 11).
Script 6 (optional, only if D8 was run) — Dimension 8 body section between D7 and the Scorecard. Contains: running user identity, permission sets + PSL licenses found, findings table (Severity | Check | Label | Detail), and SOQL commands for any items requiring FDE follow-up verification.

Script 7 (optional, only if D9 was run) — Dimension 9 body section, placed after D8 and before the Scorecard. Contains: pricing model + assumed rate, the modeled path cost table (Path | Billable Actions | Credits | USD), findings table (Severity | Rule | Label | Detail), and the Vendor Disclosures list for org-level items. In Script 4's scorecard, add a "Consumption Posture" row beside "Permission Readiness": CRITICAL WASTE (RED/WHITE) | HIGH WASTE (ORANGE/WHITE) | EFFICIENT (GREEN/WHITE) | NOT RUN (LIGHT_GREY/BLACK), with the italic 9pt note "Excluded from composite score. See Priority Remediation for findings." If data['cost']['status'] == 'NOT_RUN', render not_run_reason instead of a badge.

Note: action schema findings are incorporated directly into the relevant dimension sections — they are not a separate section.
```

### Fallback: manual batching

If a document tool is unavailable, render locally when the required runtime exists. Check that the finished document contains the required sections and the applicable permission findings.

**Document structure:**
1. Cover page — Zone 1 (white: Salesforce logo + "Agentforce" + SF_BLUE accent bar) + Zone 2 (DEEP_NAVY: title, agent, customer, date, prepared_by)
2. Body page header — Salesforce logo (0.25" height) + "Forward Deployed Engineering | Agentforce Configuration Review" (right-aligned, DEEP_NAVY, 8pt, navy bottom rule)
3. Executive Summary
4–10. Dimensions 1–7 / Sections 1–7 (each: DEEP_NAVY pill heading, "What's Working" bullets in SF_BLUE, findings table with action-schema findings integrated inline, numbered fixes)
11. Configuration Health Scorecard (Section 8)
12. Priority Remediation Summary (Section 9)
13. KPI / Success Criteria (Section 10, FDE callout + table)
14. Score Disclaimer (amber callout)
15. Adversarial Test Suite — Garak-Scoped Probes (Section 11, optional)

**Severity colours in findings tables:**
- CRITICAL: RED `RGBColor(0xC0,0x00,0x00)` fill, WHITE text
- HIGH: ORANGE `RGBColor(0xFF,0x66,0x00)` fill, WHITE text
- MEDIUM: AMBER `RGBColor(0xFF,0xC0,0x00)` fill, BLACK text
- LOW: LIGHT_GREY `RGBColor(0xF4,0xF6,0xF9)` fill, BLACK text

**Score colours in scorecard:**
- 8–10: GREEN `RGBColor(0x70,0xAD,0x47)`
- 6–7: AMBER `RGBColor(0xFF,0xC0,0x00)`
- 4–5: ORANGE `RGBColor(0xFF,0x66,0x00)`
- 1–3: RED `RGBColor(0xC0,0x00,0x00)`

---
