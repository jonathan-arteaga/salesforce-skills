# Print / PDF-Ready Static HTML Guide

When the user selects **Print / PDF-ready**, skip Vite, React, and npm completely. Emit a single self-contained static HTML file named `[feature-name]-guide-print.html` with all CSS inlined and zero JavaScript.

## Required Page Architecture (In Order)

1. **Cover page:** Full-bleed gradient header, title, subtitle, metadata badge tags, and date (`page-break-after: always`).
2. **Table of Contents:** Section numbers, titles, and sub-items (`page-break-after: always`).
3. **Topic sections:** One section per major setup phase, each beginning on a fresh page (`page-break-before: always`).
4. **Troubleshooting FAQ:** Final section with no forced page break before it; every Q&A fully expanded.

## Print CSS Invariants

Apply these foundational layout and print-color rules so Chrome and Safari render crisp PDF pages:

```css
@page { size: letter; margin: 0.75in 0.85in 0.85in 0.85in; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 9.5pt; line-height: 1.55; color: #1a1a1a; background: #ffffff;
}
.cover {
  background: linear-gradient(135deg, #014486 0%, #0176D3 60%, #1589ee 100%);
  color: #ffffff; padding: 60pt 52pt 52pt; margin: -0.75in -0.85in 0 -0.85in;
  page-break-after: always; min-height: 9in;
  display: flex; flex-direction: column; justify-content: space-between;
}
.section { page-break-before: always; }
.concept, table, .callout, .code-block, .card, .faq-item { page-break-inside: avoid; }
@media print {
  .cover, .code-block, .callout, .card, thead {
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
  a { color: inherit; text-decoration: none; }
}
```

Override cover gradient and accent hex values (`#014486`, `#0176D3`) when custom branding is requested.

## Print Component Standards

- **Concept blocks:** Numbered circle badge + left-accent header bar (`#eef5ff`, `4pt solid #0176D3`) wrapping each logical step or concept.
- **Tables:** Full-width collapsed borders, dark brand header row (`#014486`, white `8pt` bold text), alternating `#f8f8f8` body rows (`8.5pt`).
- **Callouts:** `3pt` left border with light tinted background for `info` (`#0176D3` / `#e8f4ff`), `warning` (`#E07816` / `#fef4e6`), `tip` (`#2E844A` / `#eef8ee`), and `error` (`#C23934` / `#fdecea`).
- **Code blocks:** Dark surface (`#1e2433`) with header bar (`#2d3348`), monospace `7.8pt`, `white-space: pre-wrap; word-break: break-word;` so long Salesforce CLI commands never clip off the right margin.
- **Card grid:** Flex wrap row (`min-width: 115pt`) with 4 accent variants (`blue`, `green`, `purple`, `orange`) for architecture or prerequisite summaries.
- **Expanded FAQ:** Plain `.faq-item` blocks with bold `.faq-q` (`9.5pt`) and `.faq-a` (`8.5pt`) separated by hairline dividers.

## Strict Print Content Rules & PDF Export Handoff

- **Zero interactive chrome:** Omit checkboxes, collapsible accordions, copy buttons, nav sidebars, and `<script>` tags.
- **All content visible:** Never hide instructions behind tabs or toggles—lay out branching paths as clearly labeled subsections or side-by-side comparison tables.
- **Self-contained:** Inline every stylesheet rule; never rely on external CDN fonts or stylesheets.
- **User Save-as-PDF steps:** Instruct the user to open `[feature-name]-guide-print.html` in Chrome or Safari, press `Cmd+P` (Mac) or `Ctrl+P` (Windows), pick **Save as PDF**, set Paper to **Letter**, Margins to **None** (`@page` controls margins), enable **Background graphics**, and click **Save**.
