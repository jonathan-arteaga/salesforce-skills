# Agentforce Technical Design Document (HTML)

Turn verified Agentforce design or implementation evidence into a customer-facing, single-file Salesforce-branded HTML Technical Design Document (TDD) with embedded Mermaid diagrams for handover, onboarding, or architecture sign-off.

## Required Evidence Intake

Confirm or extract from provided metadata before authoring; mark any derived field inline with `[inferred]` and report missing Flow/Apex metadata instead of inventing diagram nodes:

- Agent name, API name, agent type, customer/org name, environment, prepared-by metadata.
- Agent role, subagents/topics (scope, instructions, transitions), actions (inputs, outputs, Show in Conversation, PII flags).
- Conversation variables (name, type, visibility, purpose) and context variables (source object/field).
- Flows (main + subflows + fault paths), invocable Apex classes (I/O, errors, test coverage), channel config (Email2Case, Messaging, Voice, Slack), and roadmap/known risks.

## Standard 10-Section Document Structure

1. **Overview & Purpose:** Business role, design goals, and migration context.
2. **Agent Configuration:** Settings key-value grid, conversation/context variables, system dialogs, subagent/topic overview.
3. **Topics / Subagents & Instructions:** One card per subagent with scope, actions, deterministic branches/guards (for Agent Script), and key instructions.
4. **Actions & Integrations:** Input/output tables, Show in Conversation flags, Omni-Channel routing, external dependencies.
5. **Flow / Script Architecture:** Mermaid flowcharts (`flowchart TD`) for Flows or FSM state diagrams (`stateDiagram-v2`) for Agent Script, including explicit fault paths.
6. **Channel & Deployment Configuration:** Channel setup, auth/execution identity, routing flows, voice/recording notes where applicable.
7. **Apex Classes:** `@InvocableMethod` inputs/outputs, error handling, sharing mode, and test coverage (omit if none).
8. **Process Flows:** End-to-end Mermaid sequence/flowchart, loop counters, and state transitions.
9. **Future Enhancements & Roadmap:** Planned capabilities, open dependencies, unresolved risks.
10. **Reference:** Key API Names table and customer-facing Glossary ONLY.

## Agent-Type Variants & Customer-Safe Rules

- **Service Agent:** Document dedicated Agent User (or verified site user), Omni-Channel routing, channel setup, and flag any `isPII: false` on PII-bearing action fields.
- **Employee Agent:** Document logged-in user execution context and Slack/internal surface setup.
- **Agent Script Agent:** Section 3 documents deterministic branches, guards, and transitions; Section 5 renders `stateDiagram-v2` FSM diagrams.
- **SDR / Sales Agent:** Document opt-out/CASL and competitor guardrails in Section 3 and retry/dedup caveats in Section 9.
- **Never include in a customer TDD:** Configuration Health Scorecards (route to `agentforce-review`), internal repo file paths, or internal metadata jargon (`InternalCopilot`, `ExternalCopilot`, `ReAct Planner`, `GenAiPlanner`, `isUsedByPlanner`, `AiCopilot__ReAct`).

## Branded HTML & Mermaid Visual Standard

- **Palette:** Navy `#032D60` (cover, sticky header, section headers), Salesforce Blue `#00A1E0` (accent bars, links, TOC, section numbers), Light Blue `#e8f4fd` (topic cards, info callouts), Amber `#f4a623` (warn), Red `#c23934` (critical), Orange `#e65100` (high), Green `#2e7d32` (success).
- **Components:** Navy cover page, sticky top bar, two-column `kv-grid` settings tables, light-blue topic cards, semantic callout boxes, inline severity badges, and Mermaid CDN rendering.
- **Mermaid hygiene:** Keep node labels concise to prevent overflow, show fault paths distinctly, collapse subflows into `Subflow: [Name]` unless total nodes < 12, and separate record-triggered Flows from main orchestration diagrams. Verify HTML structure, TOC anchor links, and Mermaid syntax before delivery.
