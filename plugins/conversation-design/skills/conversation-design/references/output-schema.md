# Output Schema

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Output Schema
  - Voice bundle shape
  - Field rules

## Output Schema

Single source of truth for `conversation-design.json`. Every run rewrites the file; the team flips per-scenario `draft` flags manually (or via a future skill) as scenarios get expanded into the full design.

```yaml
status: in-progress | complete     # in-progress while any scenario is still flagged draft; complete when all draft flags false
draft: true | false                # mirrors per-scenario; complete = all draft flags false
channel: chat | voice | multimodal
phase: design-fidelity | concept-fidelity
drafted_at: YYYY-MM-DD
drafted_by_axs: boolean

scenarios:
  - id: [kebab-case slug]
    title: [string, persona-voiced]
    type: happy-path | error-state | fallback
    capability_id: [from capabilities.yaml]
    subagent_id: [from subagents.yaml or null]
    goal: [string]
    phase_marker: [string — primary outcome label, error subtype, or fallback subtype]
    preconditions:
      auth: anonymous | authenticated | staff
      channel_mode: chat | voice | multimodal
      prior_context: [string or null]
    flow:
      - turn: [1..8]
        role: user | agent | system
        utterance: [string]
        actions: [action_id, ...]                            # gated on actions.yaml; empty array if missing — never fabricated
        components: [{ type, purpose, content?, style_ref }] # gated on visual upstream; empty array if missing — never fabricated
        prosody_cues: [{ type, marker, target_phrase? }]     # voice / multimodal only; channel-intrinsic
    draft: true | false                                       # team flips when scenario is shipped
    notes: [string, ...]                                      # open questions / voice flags / decisions deferred

global_notes: [string, ...]                                   # overall draft-level notes (e.g. why arrays are empty)
design_decisions_pending: [string, ...]                       # explicit list of decisions still open

voice: null | object                                          # populated by Step 9.5 on voice / multimodal channels via vendored voice-ux. See "Voice bundle shape" below.
```

### Voice bundle shape

When `channel` is `voice` or `multimodal` AND `agentforce-generate` is installed AND voice-ux ran successfully, `voice` is populated with the parsed 5-layer rewrite. Otherwise `null` (the page renders an explainer in that case).

```yaml
voice:
  voiceUx:
    version: [from voice-ux SKILL.md frontmatter]
    runMode: migrate | optimize        # voice-ux confirmed mode
    sourceShape: chat | voice          # input shape
    summary:
      principlesChecked: 12
      patternsChanged: N
      patternsOk: N
      patternsReviewNeeded: N
  layers:
    instructions:
      blurb: [string]
      sections:
        - heading: [string]
          body: [string]
          principles: [P1 ..., P9 ...]
    copy:
      blurb: [string]
      changes:
        - kind: changed | review needed
          location: [string]
          before: [string]
          after: [string]
          why: [string]
    phrasebook:
      blurb: [string]
      tokens:
        acknowledgment: [string, ...]
        empathy: [string, ...]
        thinking: [string, ...]
        handover: [string, ...]
        closing: [string, ...]
    opening:
      blurb: [string]
      ivrLayer:   { speaker, copy, why }
      agentLayer: { speaker, copy, why }
      contrastNote: [string]
    handoff:
      blurb: [string]
      items:
        - owner: [string]
          note: [string]
          severity: required | recommended
  audit:
    title: Audit — voice UX principles
    blurb: [string]
    rows:
      - id: P1..P12
        name: [string]
        status: changed | ok | review needed
        count: N
```

### Field rules

**Always present:** `status`, `draft`, `channel`, `phase`, `drafted_at`, `scenarios` (length === 3).

**Always present per scenario:** `id`, `title`, `type`, `capability_id`, `goal`, `phase_marker`, `preconditions`, `flow`, `draft`, `notes`.

**Conditional fields:**

| Field | Populate condition |
|---|---|
| `subagent_id` | Only when architecture has run (`subagents.yaml` exists). Null otherwise. |
| `flow[].actions` | Only when `actions.yaml` exists AND the turn maps to a real action ID. Empty array otherwise — never fabricated. |
| `flow[].components` | Only when a visual upstream exists (Concept Design markdown OR a Style Guide draft with components). Empty array otherwise — never fabricated. |
| `flow[].prosody_cues` | Only when channel is `voice` or `multimodal`. Empty array for chat. |
| `notes` | Always present per scenario; empty array allowed but rare. |
| `global_notes` | Always present at top level. Empty allowed; in practice usually carries the "actions / components empty because upstream missing" callouts. |
| `design_decisions_pending` | Always present; empty allowed (rare — there's almost always something open). |

**Type counts:** exactly one each of `happy-path`, `error-state`, `fallback` per run. Re-runs replace; they don't accumulate.

**Page rendering note.** The scaffold's ConversationDesign page reads this file and renders three tabs (Happy Paths · Error States · Fallbacks), filtering scenarios by `type`. The page surfaces a top-of-page draft banner while any scenario has `draft: true`; per-turn rendering shows role + turn number + utterance only. The `actions[]`, `components[]`, and `prosody_cues[]` arrays are intentionally not surfaced as turn-level chips — they exist in the JSON for downstream tools (build maps, style-guide resolution, future coverage tooling).

---
