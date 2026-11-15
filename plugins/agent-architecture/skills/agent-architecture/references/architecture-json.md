# Output: architecture.json

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Output: architecture.json
  - Field rules

## Output: architecture.json

The denormalised composite that drives the rich page (Overview · Subagent Detail · Integration tab when populated). The page reads only this file; the other four (subagents.yaml, actions.yaml, global-instructions.md, build-map.md) feed the markdown adaptor and machine consumers. The page also reads the global instructions inline from `composite.global_instructions.body_md` rather than fetching `global-instructions.md` separately — keeps the page on a single fetch.

Integration / build detail is intentionally not represented here — that's the Technical Spec deliverable's territory.

```json
{
  "status": "Draft v0.1 — first cut",
  "intro": "A working draft of the subagent map, grounded in [the X-session transcript corpus and the Y MVP capabilities | the Y MVP capabilities]. The architecture uses [N] subagents...",

  "platform_dependency": {
    "title": "Property data layer — schema agreed; two parallel workstreams",
    "body": "The custom Salesforce object..."
  },

  "diagram": {
    "router": {
      "name": "Router",
      "description": "Detects user state at session start and routes..."
    },
    "stages": [
      { "name": "Property Intelligence", "color": "#1D4ED8", "subagents": ["property_intel"] }
    ],
    "cross_cutting": {
      "name": "Always-on",
      "subagents": ["escalation", "off_topic_b2b"],
      "description": "Always-on — fires whenever..."
    }
  },

  "subagents": [
    {
      "id": "property_intel",
      "name": "Property Intelligence",
      "stage": "Property Intelligence",
      "color": "#1D4ED8",
      "owner": "fde",
      "what_it_does": "Handles everything from first contact through to decision...",
      "why_it_exists": "This is the largest cluster in the corpus...",
      "risk": "Medium",
      "carries_forward": "The Discover/Browse/Decide subagents merge into one...",
      "changes_from_today": "Removes the routing boundary between funnel stages...",
      "intents_owned": [
        { "id": "discovery_open", "name": "Property discovery — no specific property in mind", "sessions": 96, "verdict": "Covered weakly" }
      ],
      "capabilities": [
        { "id": "P3", "name": "Inventory accuracy alignment with website" }
      ],
      "actions": [
        { "name": "search_properties", "type": "new", "impl_type": "apex", "purpose": "SOQL narrow → index rank → shortlist" }
      ],
      "failure_triage": [
        { "status": "fixed", "text": "Wrong inventory shown", "addressed_by": "search_properties uses live Data 360 index" }
      ],
      "open_questions": [
        "Should short-term-stay queries route here or to a dedicated subagent?"
      ],
      "design_references": {
        "scenarios": [{ "id": "discovery-happy-path", "label": "Discovery happy path", "note": "Reviewer should pressure-test this flow first" }],
        "components": [{ "id": "property-card-carousel", "label": "Property card carousel", "note": "Used by search_properties output" }],
        "voice_notes": ["Default to inclusive 'we' — 'let's find one that fits'"]
      },
      "patterns": [
        { "name": "business-topic-slot", "rationale": "A shortlist must be read back before booking." }
      ],
      "pattern_contract": {
        "business-topic-slot": {
          "slot_name": "property_id",
          "verbatim_readback": { "template": "I've got {property_name} on {street}. Is that the one?", "required": true }
        }
      },
      "entry_route": {
        "mechanism": "judgment",
        "condition": "The student is exploring without a specific property in mind",
        "reason": "Discovery intent is open-ended."
      },
      "handoff_triggers": [
        {
          "when": "The student is ready to book a specific room",
          "target": "booking",
          "routing_contract": {
            "mechanism": "judgment",
            "reason": "Booking readiness is read from the conversation.",
            "invariant_fields": [{ "name": "property_id", "type": "string", "source": "search_properties" }],
            "filtered_fields": [{ "name": "search_history", "reason": "Booking does not need the full shortlist." }]
          }
        }
      ],
      "instruction_override": {
        "summary": "Uses plainer language for international students.",
        "overrides_rule": "Global: match the student's register.",
        "reason": "Transcripts show non-native speakers dropping off.",
        "must_restate": ["AI disclosure", "Never quote prices not in the system"],
        "risk_if_omitted": "The discovery subagent loses the AI disclosure."
      }
    }
  ],
  "next_steps": {
    "show_spec_handoff": true,
    "required": { "skill": "agentforce-generate", "input": "_local/data/architecture.json", "purpose": "build" }
  },
  "grounded_in": [
    { "source": "Agent Script Reference", "url": "https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-reference.html", "verified_date": "2026-10-01" },
    { "source": "designing-agentforce plugin", "version": "2.2.0", "date": "2026-10-01" }
  ]
}
```

### Field rules

**Always present:** `status`, `intro`, `diagram`, `subagents`, `grounded_in`. The page falls back to a load placeholder without these. `grounded_in[]` is always written — at minimum, this skill records the Salesforce Agent Script Reference verification date and the `designing-agentforce` plugin version so the Grounded-in footer always has something to render.

**Always present per subagent:** `id`, `name`, `stage`, `color`, `owner`, `what_it_does`, `why_it_exists`, `capabilities`, `actions`. Page renders without optional fields.

**Conditional fields (omit when not applicable):**

| Field | Render condition |
|---|---|
| `risk` + `carries_forward` + `changes_from_today` | Redesign mode only |
| `intents_owned[].sessions` + `intents_owned[].verdict` | Only when transcript-insights has run |
| `failure_triage` | Only when transcript-insights has run |
| `open_questions` | Only when the team flagged any during Step 4 |
| `design_references` | Only when conversation-design and/or style-guide files exist |
| `platform_dependency` | Only when explicitly captured in Step 9 |
| `subagent.voice_variant` / `subagent.variants` | Channel-customisation mode only |
| `subagent.voice_open_questions[]` | Channel-customisation, only for subagents with unresolved investigations |
| `action.voice_variant` / `action.variants` | Channel-customisation mode only |
| `global_instructions.channel_deltas` | Channel-customisation mode only |
| `baseline` | Only when a baseline `.agent` was loaded (any mode) |
| `target_channels` | Channel-customisation mode only |
| `decision_points_available: true` | Script-comparison mode only (drives the Agent Script Comparison tab) |
| `downloads[]` | Channel-customisation OR Script-comparison modes only |
| `subagent.patterns[]` + `subagent.pattern_contract` | Only when Step 4.5 picked patterns; `pattern_contract` is keyed by pattern slug and only holds settled contracts |
| `subagent.handoff_triggers[].routing_contract` | Only when Step 6.5 captured a contract for that handoff |
| `subagent.entry_route` | Only when Step 6.5 captured the `start_agent` entry into this subagent |
| `subagent.instruction_override` | Only when Step 9.5 recorded an override for this subagent |
| `next_steps` | Optional; `show_spec_handoff: true` for Greenfield / Redesign handoffs to `agentforce-generate` |

The page's existing component (`scaffold/template/src/pages/AgentArchitecture.jsx` after the Scape promotion) handles all of these gracefully — empty / missing fields don't render empty pills. Channel-customisation renders `subagent.voice_variant` inline on the Subagent Detail view; Script-comparison exposes decision points as a separate tab on the same page when `decision_points_available: true` and reads `_local/data/decision-points.yaml` on demand. This skill writes the data shape; the hub owns how it displays. The hub's `tests/architecture-contract.test.mjs` renders a fixture of this contract, so a change to these fields should update that fixture in the same PR.

---
