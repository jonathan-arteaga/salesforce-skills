---
version: "1.0.0"
date: 2026-09-10
---

# Persona handoff template

Write the generated artifact to:

`persona/[agent-name]/persona-handoff.json`

The generated file is valid JSON. It carries Persona decisions to the canonical Agent Script owner without reproducing Agent Script syntax.

```json
{
  "schema_version": "1.0",
  "mode": "greenfield | brownfield",
  "source_persona": {
    "path": "persona/[agent-name]/persona.md",
    "artifact_version": "[version]",
    "sha256": "[sha256]"
  },
  "source_agent": "[existing .agent path | null]",
  "channel": "[channel]",
  "persona_contract": {
    "identity": ["[trait plus behavioral definition]"],
    "negative_identity": ["[character anti-pattern]"],
    "personification": "[decision plus boundaries]",
    "register": "[decision-ownership behavior]",
    "linguistic_voice": {
      "formality": "[value and cue]",
      "warmth": "[value and cue]",
      "personality_intensity": "[value and cue]",
      "reading_level": "[baseline and flex policy]"
    },
    "tone": {
      "emotional_coloring": "[value and cue]",
      "empathy": "[value and cue]",
      "boundaries": ["[plausible drift plus preferred behavior]"],
      "lexical_flex": [
        {
          "trigger": "[observable trigger]",
          "shift_and_maximum": "[shift]",
          "wording_or_response_cue": "[cue]",
          "reset": "[reset]",
          "hard_boundary": "[boundary]"
        }
      ]
    },
    "delivery": {
      "brevity_intent": "[value]",
      "humor": "[value and suppression rules]"
    },
    "chatting_style": "[emoji, formatting, punctuation, capitalization]",
    "phrase_book": "[situation-keyed palette]",
    "never_say": "[exact anti-phrases plus preferred behavior]",
    "lexicon": "[terms, definitions, usage, immutability]",
    "immutable_content": "[exact spans plus surrounding-response rule]",
    "technical_explanation_framing": "[not applicable | stay in frame | selective bridge | pair routinely]"
  },
  "semantic_deltas": [
    {
      "scope": "global | existing-subagent:[name] | static-copy-candidate:[kind]",
      "desired_character_behavior": "[approved delta]",
      "evidence": "[source or explicit user request]",
      "approval": "pending | approved"
    }
  ],
  "adjacent_constraints": [
    {
      "owner": "agent-architecture | agentforce-generate | voice-ux",
      "source_reference": "[path/section]",
      "verbatim_reference": "[exact supplied constraint; do not transform]",
      "text_role": "agent_instruction",
      "preservation": "exact",
      "intended_scope": "[each supplied placement or unresolved]",
      "approval_authority": "[supplied authority/status or unknown]"
    }
  ],
  "downstream_acceptance": {
    "preserve_facts_and_status": true,
    "preserve_action_and_routing_contracts": true,
    "preserve_uncertainty": true,
    "preserve_never_say": true,
    "preserve_immutable_content": true,
    "reset_tone_flex_on_declared_condition": true,
    "representative_scenarios_owner": "conversation-design",
    "runtime_validation_owner": "agentforce-test",
    "agent_script_owner": "agentforce-generate",
    "voice_adaptation_owner": "voice-ux"
  },
  "next_owner": "agentforce-generate",
  "status": "draft | approved"
}
```

## Optional protected-instruction metadata

For an explicitly protected instruction block, retain the exact text in `adjacent_constraints[].verbatim_reference` and include the preservation fields shown above. For ordinary adjacent references, omit these optional preservation fields. Omit a protected entry entirely when none is supplied. Approval of the Persona handoff does not establish Legal approval. Keep supplied scope separate from resolved Agent Script placement; this handoff does not apply or verify the block in source.

## Rules

- Do not include Agent Script code, field paths, syntax, metadata, actions, routes, variables, access users, or deployment targets.
- Do not convert adjacent Guardrails or evidence policies into Persona content.
- Do not mark `status` approved without explicit user approval.
- A generated handoff is not a compiled or preview-ready agent.
