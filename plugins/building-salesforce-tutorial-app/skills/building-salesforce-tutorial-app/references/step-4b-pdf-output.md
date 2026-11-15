# Step 4b — PDF Output (only if user chose PDF in Q8)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 4b — PDF Output (only if user chose PDF in Q8)
  - PDF file naming
  - Required page structure (in order)
  - Required CSS rules
  - Cover page CSS
  - Section / concept structure
  - Tables
  - Callouts
  - Code blocks
  - Card grid (for overview/concept summary pages)
  - FAQ (print-optimized, no accordion — all expanded)
  - Print rules
  - PDF content rules

## Step 4b — PDF Output (only if user chose PDF in Q8)

If the user chose **PDF-ready**, skip the Vite/React stack entirely. Build a **single static HTML file** with all CSS inlined in a `<style>` tag. No JavaScript required.

### PDF file naming
Output to: `[feature-name]-guide-print.html`

### Required page structure (in order)
1. **Cover page** — full-bleed gradient, title, subtitle, badge tags, date. `page-break-after: always`.
2. **Table of contents** — section numbers, titles, sub-items with dot leaders. `page-break-after: always`.
3. **One section per major topic** — each section starts on a new page (`page-break-before: always`).
4. **FAQ / Troubleshooting** — final section, no forced page break before it.

### Required CSS rules

```css
@page { size: letter; margin: 0.75in 0.85in 0.85in 0.85in; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 9.5pt; line-height: 1.55; color: #1a1a1a; background: white;
}
```

### Cover page CSS
```css
.cover {
  background: linear-gradient(135deg, #014486 0%, #0176D3 60%, #1589ee 100%);
  color: white; padding: 60pt 52pt 52pt;
  margin: -0.75in -0.85in 0 -0.85in;
  page-break-after: always; min-height: 9in;
  display: flex; flex-direction: column; justify-content: space-between;
}
.cover h1 { font-size: 30pt; font-weight: 700; line-height: 1.15; margin-bottom: 16pt; }
.cover-sub { font-size: 11pt; opacity: 0.9; line-height: 1.65; max-width: 460pt; }
.cover-badge {
  background: rgba(255,255,255,0.16); border: 1pt solid rgba(255,255,255,0.32);
  border-radius: 20pt; padding: 4pt 13pt; font-size: 8.5pt; font-weight: 600;
  display: inline-block; margin: 3pt;
}
```

### Section / concept structure
```css
.section { page-break-before: always; }
.section-tag { font-size: 7.5pt; font-weight: 700; letter-spacing: 2pt; text-transform: uppercase; color: #0176D3; margin-bottom: 4pt; }
.section > h2 { font-size: 19pt; font-weight: 700; color: #181818; margin-bottom: 6pt; }
.section-intro { font-size: 10pt; color: #555; margin-bottom: 22pt; }

.concept { margin-bottom: 22pt; page-break-inside: avoid; }
.concept-header { display: flex; align-items: center; gap: 10pt; background: #eef5ff; border-left: 4pt solid #0176D3; padding: 9pt 14pt; margin-bottom: 12pt; }
.concept-num { width: 24pt; height: 24pt; background: #0176D3; color: white; border-radius: 50%; font-size: 10pt; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }
.concept-title { font-size: 12pt; font-weight: 700; color: #014486; }
.concept-body { font-size: 9pt; line-height: 1.6; }
.concept-body p { margin-bottom: 8pt; }
.concept-body ul { padding-left: 16pt; margin-bottom: 8pt; }
.concept-body li { margin-bottom: 3pt; }
```

### Tables
```css
table { width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 10pt; page-break-inside: avoid; }
thead th { background: #014486; color: white; padding: 6pt 9pt; text-align: left; font-size: 8pt; font-weight: 700; }
tbody td { padding: 6pt 9pt; border-bottom: 0.5pt solid #e0e0e0; vertical-align: top; }
tbody tr:nth-child(even) td { background: #f8f8f8; }
```

### Callouts
```css
.callout { border-radius: 3pt; padding: 8pt 12pt; margin-bottom: 10pt; display: flex; gap: 9pt; font-size: 8.5pt; page-break-inside: avoid; }
.callout.info    { background: #e8f4ff; border-left: 3pt solid #0176D3; }
.callout.warning { background: #fef4e6; border-left: 3pt solid #E07816; }
.callout.tip     { background: #eef8ee; border-left: 3pt solid #2E844A; }
.callout.error   { background: #fdecea; border-left: 3pt solid #C23934; }
.callout-icon { font-size: 11pt; flex-shrink: 0; }
.callout strong { display: block; font-size: 8pt; margin-bottom: 2pt; color: #014486; }
```

### Code blocks
```css
.code-block { background: #1e2433; border-radius: 4pt; margin-bottom: 10pt; overflow: hidden; page-break-inside: avoid; }
.code-header { background: #2d3348; padding: 5pt 12pt; font-size: 8pt; color: #8892a4; font-family: 'SF Mono','Consolas',monospace; }
.code-block pre { padding: 10pt 14pt; font-size: 7.8pt; font-family: 'SF Mono','Cascadia Code','Consolas',monospace; line-height: 1.6; color: #c8d0e0; white-space: pre-wrap; word-break: break-word; }
code { font-family: 'SF Mono','Consolas',monospace; font-size: 7.5pt; background: #eef2f8; padding: 1pt 4pt; border-radius: 2pt; color: #014486; }
```

### Card grid (for overview/concept summary pages)
```css
.card-row { display: flex; gap: 7pt; margin-bottom: 10pt; flex-wrap: wrap; }
.card { flex: 1; min-width: 115pt; border: 1pt solid #dde; border-radius: 4pt; padding: 8pt 10pt; background: #fafbfc; page-break-inside: avoid; }
.card.blue   { border-left: 3pt solid #0176D3; background: #f0f7ff; }
.card.green  { border-left: 3pt solid #2E844A; background: #f0f9f0; }
.card.purple { border-left: 3pt solid #7526E3; background: #f8f0ff; }
.card.orange { border-left: 3pt solid #E07816; background: #fef7ed; }
```

### FAQ (print-optimized, no accordion — all expanded)
```css
.faq-item { border-bottom: 0.5pt solid #e5e5e5; padding: 9pt 0; page-break-inside: avoid; }
.faq-q { font-size: 9.5pt; font-weight: 700; color: #014486; margin-bottom: 4pt; }
.faq-a { font-size: 8.5pt; color: #333; line-height: 1.6; }
```

### Print rules
```css
@media print {
  .cover { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .code-block, .callout, .card { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  thead { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  a { color: inherit; text-decoration: none; }
}
```

### PDF content rules
- **No interactive elements** — no checkboxes, no toggle buttons, no copy buttons, no nav sidebar
- **All content visible** — nothing collapsed; FAQ entries fully expanded
- **`page-break-inside: avoid`** on every concept, callout, code block, card, and table
- **Inline all styles** — no external stylesheets; the file must be self-contained

---
