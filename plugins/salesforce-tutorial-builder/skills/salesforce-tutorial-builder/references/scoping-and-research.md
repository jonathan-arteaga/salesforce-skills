# Scoping, Local Extraction & Research Protocol

Confirm all 8 scoping parameters before scaffolding. Extract anything already given in the user's request and ask only for missing items (group concise questions or ask one-by-one if the user requests a guided interview). Confirm understanding in one sentence before proceeding.

## 8 Scoping Inputs

| # | Dimension | Choices / Guidance |
| --- | --- | --- |
| 1 | Topic | Specific Salesforce feature, cloud, or Agentforce capability to document |
| 2 | Audience | Admins/developers (Setup + CLI), business stakeholders (plain language), or mixed |
| 3 | Detail level | Step-by-step (every click), high-level overview (phases & why), or reference card (cheat sheet) |
| 4 | End goal | Target outcome shaping inclusions/exclusions (e.g., Experience Cloud embed, third-party site, internal tool) |
| 5 | Branding | Neutral baseline, Salesforce SLDS brand, or custom (company name, hex colors, verified logo URL) |
| 6 | Local source | Read current workspace code/README/configs (`yes`) or docs-only (`no`) |
| 7 | Research depth | `Minimal` (no web fetch), `Moderate` (1–2 targeted official pages), or `Deep` (cross-reference & full gotchas) |
| 8 | Output format | Single shareable interactive HTML (default), local Vite dev server, both, or Print/PDF-ready static HTML |

## Local-First Extraction (When Source = Yes)

Always inspect workspace files before external documentation:

1. Read `README.md`, `AGENTS.md` / `CLAUDE.md`, `CONTRIBUTING.md`, and inline setup notes.
2. Read key implementation artifacts: `.agent` definitions, Flow/Apex/LWC files, `sfdx-project.json`, and metadata XMLs.
3. Extract real API names, prerequisites, and configuration parameters—sanitizing any org-specific IDs or secrets into placeholders.
4. Where local code disagrees with public Salesforce docs, **trust the local files** and flag the discrepancy in a `warning` callout.

## External Research Tiers

- **Minimal:** Skip external fetches; rely on local files and training knowledge. Add a visible `info` callout reminding readers to verify UI paths against their target Salesforce release.
- **Moderate:** Fetch 1–2 targeted official doc pages covering the core setup area(s); do not crawl beyond those pages.
- **Deep:** Fetch all relevant official docs, cross-reference contradictions, and document every timing delay, license prerequisite, sequencing rule, and known error.

When Salesforce Docs MCP is available, discover live slash-delimited collections via `collection://list` (for example `admin/ai`, `developer/lwc`) and use `search_mode: hybrid` for exact API names or errors. Common official starting URLs:

- Enhanced Chat / Embedded Messaging: `https://developer.salesforce.com/docs/ai/agentforce/guide/enhanced-chat-inline-mode.html`
- Agentforce Agent Setup: `https://developer.salesforce.com/docs/ai/agentforce/guide/get-started-agents.html`
- Agent API: `https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-get-started.html`
- Agentforce Data Library: `https://developer.salesforce.com/docs/ai/agentforce/guide/adl.html`
- Omni-Channel Routing: search Salesforce Help for "Omni-Channel routing configuration"

## Content Quality Bar

Every tutorial step must provide:

1. **Exact Setup path:** e.g., `Setup -> Quick Find -> Routing Configurations`.
2. **Concrete field entries:** Exact field labels and sanitized example values—never vague "fill out the form".
3. **Watch-outs:** Propagation delays, hidden prerequisites, sequencing dependencies, or benign warnings.
4. **Failure impact:** What breaks and what symptoms appear if the step is skipped or misconfigured.
5. **Typed callouts:** Use `warning` (missed steps/sequencing), `error` (misconfiguration diagnosis), `tip` (shortcuts/clarity), and `info` (decision context).
