# Step 10: Global instructions topic

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 10: Global instructions topic
- Step 11: Design references (computed)
- Step 12: Present and confirm
- Step 13: Write canonical files
- Step 14: Update engagement state
- Step 15: Return to hub for publish

### Step 10: Global instructions topic

The global instructions topic is the runtime context the master agent reads on every turn. In Agentforce specifically, anything that applies to every subagent belongs here; anything subagent-specific belongs in that subagent's classification description. Putting too much here blows the context budget.

**Five elements belong in global instructions:**

1. **Persona voice** — *who* the agent is, *how* it speaks. Sourced from `_local/data/persona.md`.
2. **Channel-specific output rules** — voice agents need *"speak naturally; never read URLs aloud or use markdown formatting"*; chat agents need *"use markdown for structure where it helps comprehension"*; multimodal agents need both. Sourced from `engagement.channel`.
3. **Escalation + refusal policy** — when the agent hands off to a human, how it declines out-of-scope requests. Cross-cuts subagents — putting it per-subagent produces inconsistent escalation language.
4. **Compliance disclosures** — AI-disclosure language (mandatory in many jurisdictions: EU AI Act, California SB 1001, voice telephony rules), brand-required disclaimers, industry-specific phrasing. Sourced from `engagement.regulatory` if set; otherwise asked once during this step.
5. **Brand language guardrails** — "never-say" terms (deprecated product names, competitor names, claims the brand doesn't make legally). Sourced from persona's never-say list when present.

**If persona is absent, refuse to generate.** Past versions wrote a "functional but voice-flagged" generic version; the team consistently reported that the generic content shipped without ever getting re-tuned, and was worse than no global instructions at all (the master agent ran with nothing rather than with subtly-wrong-voice instructions baked in).

The refuse copy:

> "Global instructions inherit voice from the persona doc, and persona isn't on file (`_local/data/persona.md` not found). I won't generate a generic version — past runs that did this shipped persona-less voice into the build and rarely got re-tuned. Two options:
>
> 1. **Run `persona` first**, then re-run this step. Recommended.
> 2. **Skip global instructions for now** — the rest of the architecture writes; global-instructions.md isn't created. You can re-run this step (`/agent-architecture` → 'refresh global instructions') once persona lands.
>
> What would you like to do?"

If user picks 2, set `architecture.global_instructions = null` in the composite, omit the markdown file, and surface a banner on the architecture page: *"Global instructions pending — persona not yet on file."*

**Content (when persona IS available):**

Identity and voice are sourced from `persona-handoff.json` (the structured handoff `persona` already emits). The physical layout of the `system.instructions` block in Agent Script — section ordering, header shape, placement of hard rules — is owned by `agentforce-generate` `references/instruction-resolution.md`. This skill does not restate the template.

What this skill captures is the **design content** that feeds the template:

- **What the agent can do** — a list of MVP subagent areas in plain language.
- **What the agent can't do** — out-of-scope categories.
- **When uncertain** — escalation / refusal policy, cross-cutting, grounded in persona's escalation language and the `escalation-reason-key` pattern (see [`references/patterns/escalation-reason-key.md`](patterns/escalation-reason-key.md)).
- **Compliance needs** — AI-disclosure language, jurisdictional phrasing, brand-required disclaimers, drawn from `engagement.regulatory` and persona.
- **Hard rules / never-say** — non-negotiables from persona's never-say list plus universal rules (never invent data, never claim to be human, etc.).

The canonical skill resolves these into the final `system.instructions` block at build-time; this skill emits them as structured content, not as a positional template.

If `engagement.regulatory` is unset, ask once during this step:

> "Are there any compliance phrases the agent must include? Common examples: an AI-disclosure ('I'm an AI assistant'), industry-specific disclaimers (financial advice, medical information), or jurisdictional phrasing. Skip if none apply."

**Mode-specific behaviour:**

- **Greenfield / Redesign** — draft the full global instructions body as above.
- **Channel customisation** — do not regenerate the body. Draft a `channel_deltas` map per target channel and merge on write:
  ```yaml
  global_instructions:
    body_md: <existing from persona>
    channel_deltas:
      voice:
        - Add: "Never read URLs aloud — paraphrase to the section of the website."
        - Add: "Structured close: confirm resolution, summarise outcomes, clear sign-off."
        - Remove: "Use markdown for structure where it helps comprehension." (chat-only)
  ```
  Add / Remove lines are human-readable — the render displays them as an accordion under the primary body. Reviewers see the shared voice single-source alongside the channel overrides.
- **Script comparison** — do not regenerate the body. Instead, produce decision-points cards comparing the baseline's `system.instructions` block against the checked deliverables (typically persona §9 "Global Persona Block"). Each divergence becomes one card with `change_scope: script` and its own `before_text` / `after_text`. Individual cards keep the review surgical; if the divergence is genuinely wholesale (>50% rewrite), collapse into a single "replace global block" card rather than fragmenting.

### Step 11: Design references (computed)

For each subagent, compute design-reference chips at write time. The page uses these to deep-link reviewers from architecture into Conversation Design and Style Guide.

```yaml
design_references:
  scenarios: [{ id, label, note }]   # deep-links to /conversation-design#[id]
  components: [{ id, label, note }]  # deep-links to /style-guide#[id]
  voice_notes: [string]              # short reminders pulled from persona / fallbacks
```

Compute by reading `_local/data/conversation-design.md` and `_local/data/style-guide.json` if present, mapping subagent capabilities to scenarios that reference them. If neither file exists, skip — the page renders the subagent without a design references block.

### Step 12: Present and confirm

Show the architecture summary before writing the requested deliverables. A request to create or update these files authorizes local draft output; stakeholder sign-off and publication remain separate decisions. The summary lists whichever artefacts the picked modes will produce:

> "Here's the architecture I've drafted:
>
> **Modes:** [greenfield] / [redesign + channel-customisation] / [script-comparison] / ...
>
> **[N] subagents** covering [M] MVP capabilities:
> - **[Subagent name]** ([stage]) — [brief what_it_does], owns [X] intents, [Y] actions ([new/modified/preserved/stretch breakdown])[, voice variant: major/minor]
> - ...
>
> **Global instructions:** [drafted / preserved with channel_deltas / referenced from baseline / pending — persona missing]
>
> **Integration map:** [K integrations captured / skipped]
>
> **Platform dependency banner:** [yes / no]
>
> **Voice variants** *(channel-customisation only)*: [P subagents with variants, Q open questions]
>
> **Decision points** *(script-comparison only)*: [R recommendations across S sections — T script / U flow / V IVR / …]
>
> I will save the requested draft and flag any unresolved decisions."

Iterate on user feedback when supplied. Continue with already-authorized file creation without a second confirmation. For review-only requests, return the summary without writing. Ask about unresolved decisions only when they block correct output; retain draft status until explicitly approved.

### Step 13: Write canonical files

Writes to canonical `_local/data/`. The hub's publish step copies into the site. Files that don't apply to the picked modes aren't written.

```bash
# 1. subagents.yaml — structured truth for subagent shape.
# Includes voice_variant / variants.<channel> when channel-customisation is picked.
node -e '
const fs = require("fs");
const yaml = require("js-yaml");  // assume installed; fall back to manual if not
const subagents = [/* ... */];
fs.writeFileSync("./_local/data/subagents.yaml", yaml.dump({subagents}));
'

# 2. actions.yaml — structured truth for action specs.
# Includes voice_variant / variants.<channel> when channel-customisation is picked.
node -e '
const fs = require("fs");
const yaml = require("js-yaml");
const actions = [/* ... */];
fs.writeFileSync("./_local/data/actions.yaml", yaml.dump({actions}));
'

# 3. global-instructions.md — markdown, persona-voiced.
# When channel-customisation is picked, append a "## Channel deltas" section.
# When script-comparison is picked, DO NOT rewrite — divergences flow into
# decision-points.yaml as individual cards.
# Write directly using the Write tool.

# 4. build-map.md — human-readable architecture for the FDE.
# Each subagent + its capabilities + actions, in build order.
# Write directly using the Write tool.

# 5. decision-points.yaml (Script-comparison mode only) — the recommendation cards.
node -e '
const fs = require("fs");
const yaml = require("js-yaml");
const points = [/* ... */];
const pending_sources = [/* free-text list from Step 1.6 follow-up */];
const additional_sources = [/* workshop decisions, transcript verdicts from Step 1.6 */];
fs.writeFileSync(
  "./_local/data/decision-points.yaml",
  yaml.dump({ points, pending_sources, additional_sources })
);
'

# 6. agent-baseline/<name>.agent (Channel-customisation / Script-comparison) —
# persist the parsed baseline so re-runs have a stable reference. Only write
# when the user pasted content or supplied a file outside _local/data/agent-baseline/.
# Skip if the baseline was auto-detected in place.

# 7. Proposed .agent emission (Script-comparison, GATED) — this skill does NOT
# write the proposed .agent with file tools. The approved decision-points.yaml
# is the artefact this skill owns. Generating the proposed .agent (candidate
# source + validation) is `agentforce-generate`'s job; packaging
# approved changes into an optional developer worklist is the separately
# installed `designing-agentforce-labs:agentscript-change-worklist` skill's job. The gate stays here (explicit user ask after refining
# decision-points.yaml); the proposed .agent is labelled "proposed, not
# validated" until agentforce-generate validates and compiles it.

# 8. architecture.json — DENORMALISED composite, drives the page
node -e '
const fs = require("fs");
const composite = {
  status: "[status string, e.g. \"Draft v0.1 — first cut\"]",
  intro: "[paragraph framing the architecture]",
  modes: ["greenfield" | "redesign" | "channel-customisation" | "script-comparison"],
  target_channels: ["voice", "multimodal"] || null,   // Channel-customisation only
  baseline: {                                          // Present when a baseline .agent was loaded
    filename: "Nova_Build_V2_sandbox.agent",
    parsed_at: "[YYYY-MM-DD]",
    topic_count: 5,
    action_count: 8,
  } || null,
  platform_dependency: { title, body } || null,
  // Global instructions: inlined here so the Architecture page can render the
  // panel without a separate fetch. Source-of-truth markdown stays at
  // _local/data/global-instructions.md. Set to null when persona was missing
  // and the user picked "Skip global instructions for now" — the page renders
  // a "Pending — persona not yet on file" banner in that case.
  global_instructions: {
    persona_source: "[agent name]",          // the persona doc this drew from
    body_md: "[full markdown content from global-instructions.md, inlined]",
    generated_at: "[YYYY-MM-DD]",
    has_compliance: true | false,            // whether engagement.regulatory or in-skill ask produced compliance content
    channel_deltas: {                        // Channel-customisation only
      voice: [{ verb: "Add" | "Remove" | "Replace", text: "..." }],
    } || null,
  } || null,
  diagram: {
    router: { name: "Router", description: "..." },
    stages: [{ name, color, subagents: [ids] }],
    cross_cutting: { name: "Always-on", subagents: [ids], description: "..." } || null
  },
  subagents: [
    // each subagent enriched by joining:
    // - capabilities (from capabilities.yaml — looked up by ID)
    // - actions (from actions.yaml — filtered by capability_id)
    // - intents_owned (already on the subagent if transcript-insights ran)
    // - design_references (computed in Step 11)
    // - carries_forward / changes_from_today / risk (only if redesign)
    // - failure_triage / open_questions (only if upstream data has them)
    // - voice_variant OR variants.<channel> (channel-customisation only) — inlined from subagents.yaml
    // - voice_open_questions[] (channel-customisation only, per AusPost pattern)
    // - patterns[] + pattern_contract (Step 4.5, only when patterns were picked)
    // - handoff_triggers[].routing_contract + entry_route (Step 6.5)
    // - instruction_override (Step 9.5, only when the subagent overrides global instructions)
    // Shapes: see "Output: architecture.json" below.
  ],
  // Integrations: drives the Integration tab. Empty array = tab hidden.
  // integrations_pending: true means the user skipped capture; tab shows a
  // "FDE input pending" panel instead of detail rows. Channel-agnostic —
  // per-channel notes captured inside each integration's `notes` field.
  integrations: [
    // each integration: { id, name, type, purpose, used_by, ownership,
    //                     blocks_e2e_testing, blocker_reason, auth,
    //                     data_classification, notes }
  ],
  integrations_pending: false,
  // Decision points: drives the Agent Script Comparison tab. Only populated
  // for Script-comparison mode. Empty / null = tab hidden. When present, the
  // hub renders the tab as its own top-level view on the Architecture page.
  decision_points_available: true | false,
  // Downloads block for baseline / proposed .agent files. Renders only when
  // modes include channel-customisation or script-comparison. Each entry is
  // { pillTone: "current" | "proposed" | "rebuilt", label, filename, href, description }.
  downloads: [] || null,
  // Next steps: the downstream handoff. show_spec_handoff lights up the hub's
  // Agent Spec handoff tab (Greenfield / Redesign).
  next_steps: {
    show_spec_handoff: true | false,
    required: { skill: "agentforce-generate", input: "_local/data/architecture.json", purpose: "build" },
    phases_ahead: [{ label, skill, description }],
  } || null,
  // Grounded-in: the authoritative sources this architecture was composed
  // against. The hub Grounded-in footer reads this block; the hub PR renders
  // one row per source. Tier the sources from most authoritative (Salesforce
  // docs, Agent Script Reference) down to this plugin's version. The reader
  // can audit how fresh each source was at the time of composition.
  grounded_in: [
    {
      source: "Agent Script Reference",
      url: "https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-reference.html",
      verified_date: "[YYYY-MM-DD when the skill last confirmed the reference URL resolves]",
    },
    {
      source: "agentforce-generate",
      version: "[git sha or release tag of the canonical skill at the time of composition]",
      date: "[YYYY-MM-DD]",
      notes: "architecture-patterns, instruction-resolution, actions-reference, agent-spec-template",
    },
    {
      source: "agentforce-test",
      version: "[git sha or release tag]",
      date: "[YYYY-MM-DD]",
      notes: "test design for verdict + routing — only when test design surfaced from this architecture run",
    },
    {
      source: "agentforce-observe",
      version: "[git sha or release tag]",
      date: "[YYYY-MM-DD]",
      notes: "production session evidence — only when transcript-insights or similar observe-sourced data was consumed",
    },
    {
      source: "designing-agentforce plugin",
      version: "[plugin.json version at compose time]",
      date: "[YYYY-MM-DD]",
      notes: "pattern library · founding patterns referenced at Step 4.5",
    },
  ],
};
fs.writeFileSync("./_local/data/architecture.json", JSON.stringify(composite, null, 2) + "\n");
'
```

### Step 14: Update engagement state

```bash
node -e '
const fs = require("fs");
const path = "./project.config.json";
const c = JSON.parse(fs.readFileSync(path, "utf8"));
const today = new Date().toISOString().slice(0, 10);
const s = c.sections.find(x => x.id === "agent-architecture");
if (s) s.status = "complete";
c.changelog = c.changelog || [];
c.changelog.unshift({
  date: today,
  type: "section-complete",
  entry: "Agent Architecture completed — [N] subagents, [M] actions across [L] capabilities.",
});
fs.writeFileSync(path, JSON.stringify(c, null, 2) + "\n");
'
```

### Step 15: Return to hub for publish

Tell the hub: *"Architecture written to `_local/data/`. Run publish."*

The hub runs `publish('agent-architecture', config)` and emits the per-mode notice (reload the page in site mode; markdown bundle path in markdown mode).

---
