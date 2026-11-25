---
name: salesforce-tutorial-builder
description: "Build standalone interactive HTML or print/PDF setup tutorials and walkthroughs for Salesforce and Agentforce features. Use salesforce-lwc for production UI, agentforce-build for agent code, salesforce-discovery for workshops, or salesforce-devops-deploy for org releases."
---

# Salesforce Tutorial Builder

Turn a Salesforce or Agentforce teaching brief, repository, or configuration workflow into a standalone single-file interactive HTML tutorial app or a print/PDF-ready static HTML guide that opens directly in any browser with zero server setup.

## Mode & Reference Routing

Select the reference(s) matching the requested deliverable and skip unrelated output modes:

| Task / Mode | Load Reference |
| --- | --- |
| Scoping intake, local repo extraction, doc research tiers, content bar | [scoping-and-research.md](references/scoping-and-research.md) |
| Interactive HTML single-file app (Vite + React + singlefile or dev server) | [interactive-html-app.md](references/interactive-html-app.md) |
| Print / PDF-ready static HTML guide (zero JS, print CSS, Save as PDF) | [print-pdf-guide.md](references/print-pdf-guide.md) |

## Execution Spine

1. **Scope and confirm:** Resolve all 8 scoping inputs (topic, audience, detail level, end goal, branding, local source, research depth, output format). Extract values already given by the user, ask only for missing decisions, and confirm scope in one sentence before scaffolding.
2. **Research local-first, then docs:** Inspect workspace files (`README.md`, `.agent`, LWC/Flow/Apex metadata, `AGENTS.md`) before external Salesforce documentation; apply the chosen research tier (`Minimal`, `Moderate`, or `Deep`).
3. **Plan structure:** Outline major setup phases, branching deployment paths, live config fields, and troubleshooting entries before writing files.
4. **Build deliverable:** Scaffold the Vite + React + `vite-plugin-singlefile` app (or zero-Node single-file fallback) for interactive HTML, or write one zero-JS static HTML file for print/PDF.
5. **Verify and deliver:** Run the build/export check, copy the final self-contained HTML to a clean root filename, and return sharing or Save-as-PDF instructions.

## Core 2026 Invariants

- **Local implementation outranks public docs:** Trust local project code where it conflicts with public Salesforce docs and call out discrepancies explicitly in a `warning` callout.
- **Actionable step quality:** Every step must state the exact Setup navigation path, concrete field names with sanitized example values, timing delays or sequencing gotchas, and what breaks if misconfigured.
- **Output mode fidelity:** Interactive HTML deliverables bundle into one self-contained shareable file with all 6 interactive controls (progress tracking, collapsible steps, copy blocks, live config panel, path tabs, FAQ accordion). Print/PDF deliverables use zero JavaScript, zero interactive chrome, and fully expanded sections.
- **Release & version honesty:** Preserve the user's stated Salesforce release, API version, and builder generation; flag beta or pilot capabilities explicitly rather than treating latest release notes as target-org availability.
- **Honest branding:** Apply Salesforce SLDS tokens, neutral styling, or user-provided brand colors. Only reference verified logo URLs or fall back to a clean text/letter mark—never fabricate URLs or colors.

## Hard Org & Safety Gates

- **Local artifact authoring only:** NEVER mutate Salesforce orgs, deploy metadata, modify permissions, or run org-altering CLI commands. Explicit user authorization is required before any read-only org inspection.
- **Sanitized shareable output:** Tutorials are meant to be emailed, uploaded, or shared. Never embed live org IDs, credentials, OAuth secrets, session tokens, internal Jira/GUS links, or customer PII—populate live config inputs strictly with synthetic placeholders (`00D000000000000`, `https://example.my.salesforce.com`).
- **No fabricated platform claims:** Never invent Salesforce Setup paths, API names, or release-specific UI labels. Keep private project data out of external doc searches.

## Verification Integrity

- Track provenance explicitly: `observed` (local files or authorized org read), `stakeholder-reported` (user brief), `inferred` (training knowledge), or `Not verified` (not tested in a live Salesforce org).
- In **Minimal** research mode, include a visible callout noting steps reflect training knowledge and should be checked against the reader's current Salesforce release.
- Verify the generated build artifact before reporting done (confirm `npm run build` exits 0 and the single-file output exists for interactive apps, or confirm the static print HTML file is written and structurally valid).
- Report local build checks separately from live Salesforce walkthroughs; mark browser visual checks or live-org step execution `Not verified` whenever not run.

## Delegate Outside Tutorials

Do not use this skill to answer a quick question without building a guide or to ship production org artifacts:

- **Production UI / Experience Cloud components:** `salesforce-lwc`
- **Live Agentforce agent/prompt/retriever implementation:** `agentforce-build`
- **Customer discovery or workshop facilitation:** `salesforce-discovery`
- **Metadata packaging and org deployments:** `salesforce-devops-deploy`
