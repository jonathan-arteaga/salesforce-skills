# agentforce-technical-design-doc

Generates a branded HTML Technical Design Document for any Agentforce agent.

## Invoke with

```
/agentforce-technical-design-doc
```

Then paste or describe the agent configuration. The skill will ask clarifying questions if required inputs are missing, then generate the HTML document in batched parts.

## Output

`~/Desktop/[AgentName]_TDD.html` — a single self-contained HTML file with:
- Salesforce-branded cover page (navy + SF blue)
- Sticky page header
- Table of contents
- 10 sections with tables, callout boxes, issue cards, and Mermaid flow diagrams
- Mermaid diagrams rendered client-side via CDN (no build step required)

## Required inputs

At minimum, provide:
- Agent API name and type
- Customer / org name
- Topic names, scope, and instructions
- Action names and key outputs
- Flow hierarchy (main flow + subflows)

## Sections generated

| # | Section |
|---|---|
| 1 | Overview & Purpose |
| 2 | Agent Configuration (settings, variables, dialogs) |
| 3 | Topics & Instructions |
| 4 | Actions & Integrations |
| 5 | Flow Architecture (Mermaid diagrams) |
| 6 | Channel & Deployment Configuration |
| 7 | Apex Classes (if applicable) |
| 8 | Process Flows (end-to-end Mermaid) |
| 9 | Future Enhancements & Roadmap |
| 10 | Reference (API names, glossary) |

## Token budget

The skill writes HTML in 7 separate Python scripts to avoid context exhaustion. For agents with more than 3 topics or 5 Flows, it spawns a sub-agent. Do not attempt to generate the full document in a single turn.

## Style reference

The skill follows a Salesforce-branded HTML style (navy + SF blue palette, sticky page header, numbered section headings, topic cards, callout boxes, Mermaid diagrams). See the **HTML Style Standard** section in `SKILL.md` for the full spec.

If you have a previously generated TDD you want to match, paste it as a style reference when invoking the skill — it will copy CSS and section patterns from that document.

## Troubleshooting

| Problem | Fix |
|---|---|
| Mermaid diagrams not rendering | Open in a browser (not a preview pane). Requires internet access for CDN. |
| Output file < 20KB | A part was lost — check which `cat` command failed and rerun that part |
| Diagrams overflow their container | Shorten node labels; split complex flows into two diagrams |
| Delegation unavailable | Author the sections directly with the available HTML tools |
