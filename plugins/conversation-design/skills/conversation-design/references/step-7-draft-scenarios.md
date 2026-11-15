# Step 7: Draft the three scenarios

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 7: Draft the three scenarios
  - Actions field
  - Components field (chat / multimodal)
  - Prosody cues (voice / multimodal)

### Step 7: Draft the three scenarios

Draft each scenario in turn — present each as a compact preview before writing anything to disk.

**Per-scenario shape:**

```yaml
id: [kebab-case slug]
title: [short label, persona-voiced]
type: happy-path | error-state | fallback
capability_id: [from capabilities.yaml — the primary capability the scenario sits inside]
subagent_id: [from subagents.yaml if present, else null]
goal: [one sentence — what the user is trying to accomplish; what the agent is trying to do]
phase_marker: [happy: "primary outcome" | error: error_subtype | fallback: fallback_subtype]
preconditions:
  auth: anonymous | authenticated | staff
  channel_mode: [chat | voice | multimodal — matches engagement.channel]
  prior_context: [string — anything the master agent / preceding flow handed in]
flow:
  - turn: 1
    role: user | agent | system
    utterance: [string — the actual line]
    actions: [array of action_ids from actions.yaml — see "Actions field" below; EMPTY if no actions.yaml exists]
    components: [chat / multimodal only — see "Components field" below; EMPTY if no visual upstream exists]
    prosody_cues: [voice / multimodal only — see "Prosody cues" below]
  # 4–8 turns total
notes: [array of strings — open questions, voice flags, decisions deferred for downstream design work]
```

**Turn count rules:**

- Hard min: 4 turns. Anything below isn't a scenario, it's a one-shot.
- Hard max: 8 turns. Beyond that, either split into two scenarios or recognise it isn't ready to be designed yet — leave a note in the scenario.
- Number turns sequentially from 1.
- Roles alternate naturally — `user` and `agent` for most turns, `system` only for system-injected events (auth challenge, handoff initiated, capability deferred message).

**Voicing the agent:**

- Persona present → quote-or-paraphrase from persona's phrase book / never-say. Reference the persona section briefly in scenario `notes` for traceability (e.g. *"Agent voice draws from persona §3 — Voice. Re-tune for error voice that doesn't blame the user."*)
- Persona absent → use a friendly, neutral voice and add a top-level scenario note: *"Persona not available at draft time — voice is generic. Re-voice every agent turn once persona lands."*
- Don't fabricate a persona. If voice signals are thin, write functional turns and flag.

**Principle audit — load `references/conversation-design-principles.md` before drafting.**

The skill audits every scenario against six principles (CD1–CD6: One Breath Test, Tapering, No Dead Ends, End-Focus, Persona-Voiced Turns, Cooperative Principle). The rubric defines what each principle requires, the common mis-applications, and the citation format. Before writing turns:

1. Read `references/conversation-design-principles.md`.
2. Draft the scenario.
3. Walk every turn against CD1–CD6. For each principle, determine: `ok` (honoured), `changed` (rewrite applied), `[review needed]` (violated but with intentionality signal), `[consider]` (present but weak), or `[out-of-scope]` (pattern this rubric doesn't cover).
4. Surface every non-`ok` finding in the scenario's `notes` field with a citation: `"Turn 3 — split per CD1 (one breath test); recovery turn 4 picks up after acknowledgement."`
5. Every scenario must carry at least one citation. Uncited scenarios fail the coverage contract.

The audit is *load-bearing*, not decorative. The rubric tells the model what to check; the citations tell the reviewer (or a future AXS) why each turn was written the way it was. A scenario without citations is a draft, not a preview.

#### Actions field

For each turn where the agent invokes a build-side action, record the action ID(s) on `actions[]`.

**Strict rule — gated on upstream:**

```bash
# Before populating any actions field:
test -f _local/data/actions.yaml || ACTIONS_AVAILABLE=false
```

- **`actions.yaml` exists** → look up real action IDs and record them on the turns where they fire. The skill must not invent IDs that aren't in `actions.yaml`. If a turn would invoke an action that isn't yet in `actions.yaml`, leave the field empty and surface in `notes` (e.g. *"Turn 5 implies a `bill_breakdown` action that isn't in the architecture yet — flag for an architecture re-pass."*).
- **`actions.yaml` does not exist** → every turn's `actions` array is `[]`. Add to `global_notes`: *"Action IDs not recorded — `actions.yaml` not present. Run /agent-architecture to populate."*

The renderer does **not** display action chips on the page; the data is preserved for build-map / coverage tooling. Honesty over cosmetics: empty arrays are correct when grounding is missing.

#### Components field (chat / multimodal)

For each turn that renders a UI component, record an entry on `components[]`.

**Strict rule — gated on visual upstream:**

```bash
# Before populating any components field:
test -f _local/data/concept-design.md || \
  ([ -f _local/data/style-guide.json ] && jq -e '.components | length > 0' _local/data/style-guide.json) || \
  COMPONENTS_AVAILABLE=false
```

- **Concept Design markdown exists** → use the surface decisions from Concept Design to ground component types and `style_ref` slugs. Honour Concept Design's vocabulary; don't introduce slugs it doesn't reference.
- **A prior Style Guide draft exists** → use the slugs already defined in `style-guide.json` for `style_ref`. The Style Guide is the source of truth on the slug vocabulary once it has run.
- **Neither exists** → every turn's `components` array is `[]`. Add to `global_notes`: *"Component callouts not recorded — no visual upstream (Concept Design or Style Guide). Pair with Concept Design or run /style-guide to populate."*

When populated, each entry follows this shape:

```yaml
components:
  - type: [slug — must come from Concept Design's vocabulary or Style Guide's components]
    purpose: [one-line — what this component is doing in the turn]
    content: [optional — short preview of the rendered text/labels, if useful]
    style_ref: [slug that resolves into the Style Guide's components array]
```

Don't author the component spec here. Style references are slugs only.

The renderer does **not** display component chips on the page; the data is preserved for the Style Guide skill to resolve and for future tooling.

#### Prosody cues (voice / multimodal)

Voice and multimodal scenarios record per-turn prosody cues. Channel is intrinsic to the scenario, so this field doesn't need an external upstream gate — the persona doc grounds the markers.

```yaml
prosody_cues:
  - type: [pace | pitch | pause | stress | tone]
    marker: [short label — e.g. "measured-on-confirmation", "rising-on-question", "long-pause-pre-handoff"]
    target_phrase: [optional — the specific words the cue applies to]
```

**Rules:**

- Voice is craft work — defaults are conservative. Don't fabricate elaborate prosody patterns unless the persona explicitly calls for them.
- Common cue patterns to default to (the team will refine):
  - `pace: measured-on-confirmation` — agent slows when confirming a destructive or financial action
  - `pause: long-pre-handoff` — half-beat pause before handing to a human, signals transition
  - `tone: warm-on-error` — error voice is warm, not blameful
  - `stress: emphasis-on-action-verbs` — when offering options, action verbs are emphasised
- Surface the cues in scenario `notes` if they encode a non-obvious decision (e.g. *"Used `pace: measured-on-confirmation` because the persona's hard rules include 'never invent a price'; the agent is confirming, not stating, an offer."*).
