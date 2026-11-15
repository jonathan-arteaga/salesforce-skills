---
name: |-
  agentforce-technical-design-doc
description: |-
  Turn Agentforce implementation evidence into a customer-facing HTML technical design with diagrams. Use agentforce-architecture-analyze for a metadata inventory.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# agentforce-technical-design-doc: Agentforce Technical Design Document Skill

Use this skill when the user wants a full technical design document produced for an Agentforce agent.

## When This Skill Owns the Task

- User asks for a "technical design doc", "TDD", "design documentation", or "architecture doc"
- User wants to document an agent for handover, onboarding, or reference
- User wants an HTML document covering agent config, flows, actions, and known issues

Delegate elsewhere when:

- Reviewing agent health / producing findings → `agentforce-config-review`
- Building or editing the agent → `agentforce-generate`
- Functional test plans → `agentforce-test`
- Production session analysis → `agentforce-observe`

---

## Structure the technical design

Gather evidence before drafting. Diagrams must reflect the actual Flow structure. If it is unavailable, report the gap or ask for the needed metadata. For large documents, draft by section and check each section against the required document structure. Verify the final HTML and open it in an available renderer when possible.

## Step 1 — Gather Context

Before writing anything, confirm or ask for:

| Field | Why needed |
| --- | --- |
| Agent name, API name, agent type | Cover page + Section 2 config table |
| Customer / org name + environment | Cover page metadata |
| Agent role / description | Section 1 overview |
| Topic names, scope, instructions | Section 3 |
| Action names, inputs, outputs, Show in Conversation status | Section 4 |
| Flow names and architecture (main flow + subflows) | Section 5 — required for Mermaid diagrams |
| Conversation variables (name, type, visibility, purpose) | Section 2 |
| Context variables (name, source object, source field) | Section 2 |
| Channel configuration (Email2Case, Messaging, Voice, etc.) | Section 6 |
| Apex class names and purpose | Section 7 — skip if none |
| Planned enhancements | Section 9 |
| Prepared by (name + team) | Cover page |

If the user pastes full agent metadata, infer as much as possible and proceed. Flag inferred fields inline with `[inferred]`.

---

## Step 2 — Write and verify HTML

Use the available HTML authoring or local file tools to assemble a single document with its styles, table of contents, and diagrams. Verify the required headings, navigation, links, and diagram syntax. If file output is unavailable, provide the structured draft and identify what remains to render. Use the user's requested output location or the working directory.

## Document Structure (10 sections standard)

1. **Overview & Purpose** — agent role, design goals, migration history if applicable
2. **Agent Configuration** — agent settings table, conversation variables, context variables, system dialogs, topic overview
3. **Topics & Instructions** — one card per topic with scope, actions, key instructions table
4. **Actions & Integrations** — action input/output tables, Show in Conversation status, OmniChannel, routing
5. **Flow Architecture** — Mermaid flowchart for each Flow, key decision logic, fault paths
6. **Channel & Deployment Configuration** — Email2Case, Messaging, Voice, routing flows, auth context
7. **Apex Classes** — InvocableMethod classes, input/output tables, error handling, test class coverage
8. **Process Flows** — end-to-end Mermaid diagram, counter logic, state tables
9. **Future Enhancements & Roadmap** — planned work, unresolved risks
10. **Reference** — API names table, glossary

---

## HTML Style Standard

The document uses a consistent Salesforce-branded style. Copy the CSS block from the Email2Case TDD reference document — do not deviate from it.

### Colour palette

- `--navy: #032D60` — section headers, page header, cover background
- `--blue: #00A1E0` — accent bar, links, TOC, section numbers
- `--light-blue: #e8f4fd` — topic cards, callout-info background
- `--amber: #f4a623` — callout-warn
- `--red: #c23934` — callout-critical, CRITICAL badge
- `--green: #2e7d32` — callout-success, resolved badges
- `--orange: #e65100` — HIGH badge

### Key components to include

- **Cover page** — navy background, agent name in SF blue, customer + date metadata
- **Sticky page header** — navy bar with brand name left, doc title right
- **Section headers** — navy background, white bold text, numbered in SF blue
- **Topic cards** — light blue header, body with kv-grid
- **Callout boxes** — info (blue), warn (amber), critical (red), success (green)
- **Severity badges** — inline `<span class="badge badge-critical">CRITICAL</span>` etc.
- **Mermaid diagrams** — `<div class="mermaid">` blocks, CDN loaded in `<head>`
- **kv-grid** — two-column definition grid for settings (label left, value right)

---

## Reference Section Rules

The Reference section (Section 11) contains only:

- **Key API Names table** — component names and their API/developer names
- **Glossary** — customer-facing terms only

**Never include in the TDD:**

- Configuration Health Scorecard — belongs in the config review doc only
- Related Documents table — internal file paths are not customer-appropriate
- Glossary terms that expose internal Salesforce metadata implementation: `InternalCopilot`, `ExternalCopilot`, `ReAct Planner`, `GenAiPlanner`, `isUsedByPlanner`
- Internal API suffixes in config tables (e.g. `AiCopilot__ReAct`, `/ InternalCopilot`, `/ ExternalCopilot`)

---

## Agent-Type Variants

### Service Agent (EinsteinServiceAgent / ExternalCopilot)

- Include dedicated agent user details (email, Profile, License)
- Document OmniChannel routing and Service Email Connection
- Section 6 must cover Email2Case or Messaging channel config
- Flag any `isPII: false` on PII-carrying action fields

### Employee Agent (InternalCopilot)

- No dedicated agent user required
- Section 6 covers Slack or internal channel config
- Note if this is a v1 that has been or will be migrated to Service Agent

### AgentScript Agent

- Section 3 becomes "Script Topics & Branches" — document deterministic branches, guards, transitions
- Section 5 becomes "Script Flow Architecture" — Mermaid FSM diagrams showing state transitions
- Section 7 covers any Apex action targets

### SDR / Sales Agent

- Section 3 includes CASL opt-out topic and competitor guardrail topic
- Section 9 should document any email retry or lead dedup known issues

---

## Mermaid Diagram Guidelines

- Use `flowchart TD` for top-down flow architecture diagrams
- Use `stateDiagram-v2` for AgentScript FSM diagrams
- Keep node labels short — long labels cause rendering overflow
- Always include fault/error paths as distinct branches
- Subflow invocations: show as a node with label `Subflow: [Name]` — do not inline the subflow steps unless the diagram has fewer than 12 total nodes
- Record-triggered Flows: show separately from the main Flow hierarchy

---

## Reference Style

Follow the HTML Style Standard above when generating each TDD:

- Salesforce navy `#032D60` + SF blue `#00A1E0` palette
- Cover page (navy background, agent name in SF blue, customer + date metadata)
- Sticky page header (navy bar with brand name left, doc title right)
- Numbered section headings (navy background, white bold text, SF blue numbers)
- Topic cards (light blue header, kv-grid body)
- Callout boxes — info / warn / critical / success
- Severity badges as inline `<span class="badge badge-critical">` etc.
- Mermaid diagrams as `<div class="mermaid">` blocks with the CDN loaded in `<head>`

If the user provides a previously generated TDD as a style reference, copy the CSS and section patterns from that document.
