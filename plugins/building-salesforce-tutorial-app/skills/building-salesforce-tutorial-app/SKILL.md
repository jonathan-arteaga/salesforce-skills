---
name: |-
  building-salesforce-tutorial-app
description: |-
  Turn a Salesforce or Agentforce teaching brief into a standalone interactive tutorial or companion material. Use experience-lwc-generate for production components.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# Building Salesforce Tutorial Apps

Builds interactive, locally-hosted React tutorial apps for Salesforce features, agents, and configurations. Output is always a single self-contained HTML file that anyone can open in a browser — no install, no server needed.

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## Scope

**Use this skill when the user wants to:**

- Create an interactive setup guide for a Salesforce feature or Agentforce agent
- Build a step-by-step walkthrough or tutorial app
- Make a shareable how-to guide (as a React app or single HTML file)
- Create a locally-runnable reference app for Salesforce configuration steps
- Create a print-ready / PDF guide for formal deliverables

**DO NOT use this skill when the user wants to:**

- Build a production Salesforce app deployed to an org (use `generating-lightning-app`)
- Build a UI Bundle / Experience Cloud app (use `building-ui-bundle-app`)
- Just answer a question — only use this skill when they want an actual app built

---

## Step 1 — Discovery (REQUIRED before writing any code)

**Ask questions one at a time. Wait for the user's answer before asking the next. Do not write any code until all eight questions are answered.**

**Do not present all questions at once.** Ask them in sequence, one per message:

**Q1 (ask first):**

> What is the tutorial about? What Salesforce feature, product, or agent are you documenting?<br />*(e.g. "setting up HAA + Knowledge", "configuring Agentforce for Service", "deploying an LWC to Experience Cloud")*

**Q2 (ask after Q1 is answered):**

<quote>
Who is the audience?

- Salesforce admins / developers (technical, comfortable with Setup UI and CLI)
- Business users / stakeholders (non-technical, plain-language explanations)
- Mixed
</quote>

**Q3 (ask after Q2 is answered):**

<quote>
How much detail do you want?

- **Step-by-step** — every click documented
- **High-level overview** — what phases exist and why, without sub-step detail
- **Reference card** — quick lookup / cheat sheet format
</quote>

**Q4 (ask after Q3 is answered):**

> What is the person following this guide ultimately trying to accomplish? This shapes which steps to include and which to skip.<br />*(e.g. "expose agent on Experience Cloud", "embed on a third-party site", "internal employee tool")*

**Q5 (ask after Q4 is answered):**

<quote>
Any branding preferences?

- No branding (clean neutral Salesforce-style)
- Salesforce brand (official blue, SLDS aesthetic)
- Custom — if so, what company name, colors, and do you have a publicly accessible logo URL?
</quote>

**Q6 (ask after Q5 is answered):**

<quote>
Is there a project directory or agent in the current workspace you'd like me to read and document from? If yes, I'll scan the code, README, and config files to extract accurate steps.

- Yes — use files in the current directory
- No — research from Salesforce docs only
</quote>

**Q7 (ask after Q6 is answered):**

<quote>
How deeply should I research external Salesforce docs?

- **Minimal** — skip external research; use what I already know plus any local files. Fastest, but may miss recent changes.
- **Moderate** — fetch the 1–2 most relevant doc pages to verify key steps. Good balance of speed and accuracy.
- **Deep** — fetch all relevant docs, cross-reference multiple sources, and flag every known gotcha. Most accurate, takes longer.
</quote>

**Q8 (ask after Q7 is answered):**

<quote>
Output format?

- Single shareable HTML file (recommended — open in any browser, attach to email/Slack)
- Local dev server (Vite + React, `npm run dev`)
- Both
- **PDF-ready** — print-optimized single HTML file; open in browser → Cmd+P → Save as PDF. No React, no build step. Best for formal deliverables, slide-deck companions, or offline reading.
</quote>

Once all eight are answered, confirm your understanding back to the user in one sentence, then proceed to Step 2.

---

## Step 2 — Research

Before writing content, gather accurate source material. Apply the rules below based on what the user answered in Q6 and Q7.

### Step 2a — Local files (if user said YES to Q6)

Always read local files first — they reflect the actual implementation more accurately than public docs:

1. **Read the README** — setup steps, config fields, prerequisites, gotchas
2. **Read key source files** — agent `.agent` files, LWC JS/HTML, config XMLs, metadata
3. **Read any existing docs** — `CLAUDE.md` or `AGENTS.md`, `CONTRIBUTING.md`, inline comments
4. **Note discrepancies** between what the code does and what docs claim — flag these in the tutorial with a callout

Where local files and public docs conflict, **trust the local files**.

### Step 2b — External research depth (based on Q7 answer)

Apply exactly one of the following based on the user's Q7 answer:

---

**MINIMAL** — Do not fetch any external URLs. Use existing knowledge plus local files only.

- Skip all `WebFetch` calls
- Note in the tutorial that steps are based on knowledge as of your training cutoff and may not reflect the latest Salesforce UI changes
- Still apply the Always rules below

---

**MODERATE** — Fetch 1–2 targeted pages most relevant to the topic. Stop after those.

- Identify the single most relevant doc URL from the list below and fetch it
- If the topic spans two clearly distinct areas (e.g. agent setup + embed), fetch one page per area — max 2 total
- Do not follow links or fetch additional pages beyond those 2
- Apply the Always rules below

---

**DEEP** — Fetch all relevant docs, cross-reference multiple sources, surface every known gotcha.

- Fetch all applicable URLs from the list below
- Follow links to sub-pages if they cover required setup steps
- Cross-reference multiple sources; note any contradictions between them
- Proactively flag every timing delay, prerequisite, sequencing requirement, and common error you find
- Apply the Always rules below

---

**Key Salesforce doc URLs (use for Moderate and Deep; pick based on topic):**

- Enhanced Chat / Embedded Messaging: `https://developer.salesforce.com/docs/ai/agentforce/guide/enhanced-chat-inline-mode.html`
- Agentforce Agent setup: `https://developer.salesforce.com/docs/ai/agentforce/guide/get-started-agents.html`
- Agent API: `https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-get-started.html`
- Agentforce Data Library: `https://developer.salesforce.com/docs/ai/agentforce/guide/adl.html`
- Omni-Channel / Routing: search Salesforce Help for "Omni-Channel routing configuration"

### Always (regardless of Q6 and Q7)

- Flag steps that are commonly missed, abstracted away, or have known gotchas
- Flag prerequisites not obvious from surface-level reading
- If external research was skipped (Minimal), add a brief callout in the tutorial noting that steps are based on training knowledge and users should verify against their current Salesforce release

---

## Step 3 — Plan the App Structure

Before scaffolding, outline:

1. **Section breakdown** — what are the major phases? (e.g. Prerequisites → Agent Setup → Channel Setup → Embed → Troubleshooting)
2. **Interactive elements** — what should users be able to do? At minimum include:
   - ✅ Per-step "mark as done" checkboxes with progress tracking
   - 📋 Copy-to-clipboard code snippets
   - 🔧 Live config inputs that auto-fill generated code snippets
   - 🗂️ Tabs for multiple paths (if the topic has branching paths)
   - 🔎 Collapsible troubleshooting FAQ
3. **Navigation** — sticky left nav with progress bar
4. **Branding** — confirm colors, logo, and fonts before building

---

## Step 4 — Build the App

### Tech stack (always use this stack)

- **Vite + React** (no TypeScript unless requested)
- **Plain CSS** (CSS custom properties for theming — no Tailwind, no CSS-in-JS)
- **No UI library** — hand-written components only, styled to match Salesforce SLDS aesthetic
- **`vite-plugin-singlefile`** for the shareable HTML output

### Directory structure

```javascript
tutorial-app/
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── index.css          # All global styles and design tokens
│   ├── context/
│   │   └── TutorialContext.jsx   # Progress state, config values, path selection
│   ├── components/
│   │   ├── Nav.jsx               # Sticky left nav with IntersectionObserver active state
│   │   ├── StepCard.jsx          # Collapsible step with done toggle
│   │   ├── CopyBlock.jsx         # Syntax-highlighted copy block (fake terminal chrome)
│   │   ├── Callout.jsx           # Info / warning / tip / error callout boxes
│   │   ├── Tabs.jsx              # Tab switcher for branching paths
│   │   └── ConfigPanel.jsx       # Live config inputs → auto-generated code
│   └── sections/
│       ├── Section1*.jsx
│       ├── Section2*.jsx
│       └── SectionNTroubleshoot.jsx
├── index.html
├── vite.config.js
└── package.json
```

### vite.config.js (always use this for single-file output)

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  server: { port: 3000 },
  build: {
    target: 'esnext',
    assetsInlineLimit: 100000000,
    chunkSizeWarningLimit: 100000000,
    cssCodeSplit: false,
  }
})
```

### Design tokens (CSS custom properties — always use these)

```css
:root {
  --sf-blue: #0176D3;
  --sf-blue-dark: #014486;
  --sf-blue-light: #D8EDFF;
  --sf-green: #2E844A;
  --sf-green-light: #EAF5EA;
  --sf-orange: #E07816;
  --sf-orange-light: #FEF1E2;
  --sf-red: #C23934;
  --sf-red-light: #FDECEA;
  --sf-purple: #7526E3;
  --sf-purple-light: #F3EEFF;
  --sf-gray-1: #F3F3F3;
  --sf-gray-2: #E5E5E5;
  --sf-gray-3: #AEAEAE;
  --sf-gray-4: #706E6B;
  --sf-gray-5: #3E3E3C;
  --sf-text: #181818;
  --sf-white: #FFFFFF;
}
```

### Branding

If the user requested **Salesforce branding**:

- Use the tokens above
- Hero gradient: `linear-gradient(135deg, #014486 0%, #0176D3 60%, #1589ee 100%)`
- If a publicly accessible Salesforce logo URL is needed, search for one with `WebFetch` — only use URLs you have confirmed exist and are publicly accessible

If the user provided **custom brand colors/logo**:

- Override the CSS custom properties with their brand colors
- Only use logo image URLs that the user confirmed are publicly accessible
- If no URL is available, use a text/letter logo placeholder instead — never generate or guess a URL

If **no branding**:

- Use the Salesforce design tokens as a neutral professional baseline

### Interactive requirements (every app must have these)

1. **Progress tracking** — `TutorialContext` holds a `done` map; each `StepCard` has a "Mark as done" toggle; left nav shows `X/Y steps` and a progress bar
2. **Collapsible steps** — `StepCard` is collapsed by default, opens on click, shows done state
3. **Copy-to-clipboard** — `CopyBlock` component wraps every code snippet with a Copy button
4. **Live config panel** — inputs for the key values (org ID, API names, URLs); generated code snippets update in real-time as the user types
5. **Path switching** — if the topic has multiple deployment paths, show a path selector at the top; the Step 3 embed section uses tabs to show each path's specific instructions
6. **Troubleshooting FAQ** — collapsible accordion of common errors, always at the end

---

## Step 4b — PDF Output (only if user chose PDF in Q8)

Consult [`references/step-4b-pdf-output.md`](references/step-4b-pdf-output.md) before Step 4b, whenever the user chose PDF output in Q8.

## Step 5 — Build and Export

### For HTML / Interactive output:

```bash
npm install
npm run build   # outputs dist/index.html — single self-contained file
```

Copy `dist/index.html` to a well-named file in the project root:

```bash
cp dist/index.html ../[feature-name]-setup-guide.html
```

Open it in the browser to verify before reporting done:

```bash
open ../[feature-name]-setup-guide.html
```

### For PDF output:

No build step. Write the complete static HTML file directly to:

```javascript
[feature-name]-guide-print.html
```

Open it in the browser to verify layout, then tell the user:

```bash
open [feature-name]-guide-print.html
```

**To export as PDF:**

1. Open the file in Chrome or Safari
2. Press **Cmd+P** (Mac) or **Ctrl+P** (Windows)
3. Set destination to **"Save as PDF"**
4. Set paper size to **Letter**, margins to **None** (the `@page` CSS controls margins)
5. Enable **"Background graphics"** so gradient covers and colored callouts print correctly
6. Click **Save**

---

## Content Quality Standards

Every step in the tutorial must include:

- **Exact navigation path** in Setup (e.g. "Setup → Quick Find → Routing Configurations")
- **What to fill in** — specific field names and example values, not just "fill in the form"
- **What to watch out for** — timing delays, commonly missed sub-steps, things that look like errors but aren't
- **What breaks if this step is wrong** — so the user understands why it matters

Use callout boxes liberally:

- `warning` — steps that are commonly missed or have sequencing requirements
- `error` — what a misconfiguration looks like and how to diagnose it
- `tip` — non-obvious shortcuts or clarifying context
- `info` — background context the user needs to make a decision

---

## Sharing Options to Tell the User

When done with an **interactive HTML guide**, tell the user:

<quote>
**Your guide is at:** `path/to/feature-setup-guide.html`

Share it by:

- Emailing it as an attachment (opens in any browser)
- Uploading to a shared drive (Google Drive, SharePoint, Confluence)
- Dropping it in Slack/Teams as a file
- Hosting on any static file server or CDN — it's one file with no dependencies

To run the live dev version: `cd tutorial-app && npm run dev`<br />To rebuild after changes: `npm run build`
</quote>

When done with a **PDF-ready guide**, tell the user:

<quote>
**Your print guide is at:** `path/to/feature-guide-print.html`

**To save as PDF:**

1. Open the file in Chrome or Safari
2. Press **Cmd+P** → destination: **Save as PDF**
3. Paper: **Letter** · Margins: **None** · Enable **Background graphics**
4. Click Save

Share the resulting PDF by:

- Attaching to email or Slack
- Uploading to Confluence, SharePoint, or Google Drive
- Embedding in a slide deck as a reference appendix
</quote>
