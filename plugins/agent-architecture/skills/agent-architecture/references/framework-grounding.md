# Framework Grounding

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Framework Grounding

Agent architecture is shaped by Salesforce's published Agentforce design patterns and by broader multi-agent system practice. The skill's vocabulary and decomposition rules aren't invented here — they sit inside an established frame.

**Agentforce platform semantics — defer to canonical.** The master-agent / subagent routing model, topic as the unit of capability scope, classification descriptions, action types (Standard / Flow / Apex / Prompt Template / MCP / Headless), and the "Smallest Architecture First" posture are owned by `agentforce-generate` (see its `references/architecture-patterns.md`). This skill does not restate them. The outputs here (`subagents.yaml`, `actions.yaml`, `global-instructions.md`) map 1:1 to those constructs; the shape definitions live upstream.

**What this skill owns** are the design lenses that shape the artefact *before* platform mapping:

- **Single Responsibility (Robert C. Martin)** — adapted to subagent design: each subagent should have one reason to change. A subagent that owns "discovery + service + billing" violates SRP; the next requirements pass will fragment it. The skill flags subagents whose scope-in spans more than one capability category.
- **Bounded Context (Eric Evans, *Domain-Driven Design*)** — adapted to scope-in / scope-out. The boundaries name what the subagent owns *and* what it explicitly doesn't, so handoff is unambiguous. Vague boundaries produce master-agent routing failures at runtime.
- **Persona-voiced global instructions** — global instructions inherit voice from the persona doc (when present); this is the single place where persona becomes runtime behaviour at the master-agent layer. Without persona, global instructions are functional but voice-flagged for re-tuning.
- **Channel-variant overlay** — when an agent designed for one channel needs to run on another, the shape usually survives but the behaviour needs channel-specific rules (voice: ASR-safe capture, spoken-prose rendering, repair-tier ladders; multimodal: companion-screen affordances; messaging: async semantics). Rather than fork the architecture per channel, the skill overlays a `<channel>_variant` block per subagent + action. Keeps the design single-source.
- **Surgical recommendation cards for existing agents** — when an existing `.agent` needs to be aligned to approved deliverables, the design conversation is *which lines change and why*, not *what does the agent look like*. Each recommendation is one before/after card with a change scope (script / flow / ivr / knowledge / integration / site), a rationale reference into the deliverables (persona §N, R-ID, CD scenario turn), and optional `pending` when finalisation is blocked. The unit is small so a reviewer can accept, reject, or flag one card at a time.

**Why design, not technical spec.** The architecture page tells reviewers *what the agent's shape is and why*. The technical spec deliverable (separate future skill) gives the FDE the build detail their Apex / Flow / MCP work runs against. They share IDs but they're different documents for different audiences. Mixing them produces a doc that's too detailed for design review and too design-y for build.

**Why engagement-type continuity matters.** Redesign engagements inherit subagent and action structure from a prior agent — the design conversation is *what changes vs preserves*, not *what to build from zero*. The continuity pills (preserved / substantial rework / mostly new) make that conversation legible on the page. Greenfield engagements skip the pills entirely.

### Grounded in

The skill treats these sources as authoritative, in tiered order. Any claim about Agentforce behaviour, Agent Script grammar, or build-time constraints should resolve against the highest tier that covers it; this skill writes against the layer above, never against anything below.

| Tier | Source | What it governs |
|---|---|---|
| **Tier 1** | **Salesforce platform docs** — Agent Script Reference, Agentforce Builder docs, metadata API docs on developer.salesforce.com | The grammar, enums, and runtime behaviour of Agent Script. If this disagrees with anything in a lower tier, Tier 1 wins. |
| **Tier 2** | **Salesforce Architects content** — architect.salesforce.com, published Agentforce design patterns, Salesforce-authored "Smallest Architecture First"-style guidance | Opinionated best-practice guidance that extends Tier 1 with design intent. |
| **Tier 3** | **Canonical ADLC skills** — `agentforce-generate`, `agentforce-test`, `agentforce-observe`, `agentforce-architecture-analyze` | The build-time, test-time, observe-time, and reconcile-time behaviours. This is the layer this skill's outputs feed into and resolve against. |
| **Tier 4** | **AXS skills in this plugin** — `designing-agentforce` siblings installed here (`persona`, `conversation-design`, `voice-ux`), including this skill | Design-time patterns and artefact shapes derived from AXS fieldwork. Must not contradict Tier 1–3. |

The `architecture.json` emitted at Step 13 includes a `grounded_in[]` block that records which Tier 1–4 sources were consulted at compose time, with versions / dates where meaningful. The hub-side architecture page surfaces this as a Grounded-in footer so reviewers can audit freshness.

---
