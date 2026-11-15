# Step 8: Present each scenario for review

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 8: Present each scenario for review
- Step 9: Write canonical state
- Step 9.5: Voice-mode rewrite (voice / multimodal channels only)
- Step 10: Update engagement state
- Step 11: Return to hub for publish

### Step 8: Present each scenario for review

After drafting each scenario, show a compact preview to the user **before** writing anything. Iterate per scenario:

> "**Scenario 1 — Happy path: [title]**
>
> - **Capability:** [P3 — Inventory accuracy alignment]
> - **Goal:** [one-line goal]
> - **Channel:** [chat | voice | multimodal]
> - **Turns:** [N]
> - **Voice source:** persona §3 / generic-friendly (flagged for re-voice)
> - **Actions:** [M] recorded · [or: 'not recorded — actions.yaml absent']
> - **Components:** [K] recorded · [or: 'not recorded — no visual upstream']
>
> [render the flow as a turn-by-turn list]
>
> **Open questions:**
> - [open question 1]
> - [open question 2]
>
> Anything to refine before I move on to scenario 2?"

Iterate until the user confirms. Move on to scenario 2 (error state), then 3 (fallback). **Don't write the file until all three are confirmed.**

If the user wants to add a fourth scenario (e.g. a second happy path covering a different capability), point at the cap: *"The skill produces three scenarios per run — one of each type. Adding a fourth would mean replacing one of the existing types or running the skill again later. Which would you prefer?"*

### Step 9: Write canonical state

```bash
mkdir -p _local/data
node -e '
const fs = require("fs");
const today = "[YYYY-MM-DD]";   // pass in from the calling environment; do not generate at write time
const data = {
  status: "in-progress",           // matches section status; flips to "complete" when every scenario's draft flag is false
  draft: true,                     // top-level — true until the team / an AXS marks the scenarios as shipped; mirrors per-scenario flag
  channel: "[CHANNEL]",            // chat | voice | multimodal
  phase: "design-fidelity",        // or concept-fidelity
  drafted_at: today,
  drafted_by_axs: false,           // flips true if an AXS was in the seat (option 1 in the gate)
  scenarios: [
    {
      id: "[SLUG]",
      title: "[STRING]",
      type: "happy-path",
      capability_id: "[ID]",
      subagent_id: "[ID_OR_NULL]",
      goal: "[STRING]",
      phase_marker: "primary outcome",
      preconditions: { auth: "[VALUE]", channel_mode: "[VALUE]", prior_context: "[STRING_OR_NULL]" },
      flow: [
        { turn: 1, role: "user", utterance: "[STRING]", actions: [], components: [], prosody_cues: [] }
        // ...
      ],
      draft: true,
      notes: ["[STRING]", "..."]
    },
    // ... error-state, fallback
  ],
  global_notes: ["[STRING]", "..."],          // overall briefing notes for the AXS
  design_decisions_pending: ["[STRING]", "..."],  // explicit list of decisions the AXS still needs to make
  voice: null,                                 // populated by Step 9.5 on voice / multimodal engagements; null otherwise
};
fs.writeFileSync("./_local/data/conversation-design.json", JSON.stringify(data, null, 2) + "\n");
'
```

### Step 9.5: Voice-mode rewrite (voice / multimodal channels only)

**Skip this step entirely if `engagement.channel` is `chat`.** Run only when channel is `voice` or `multimodal`.

The hub bundles voice-ux at `voice-ux/` (vendored from forward-deployed-engineering-emu/fde-skills). On voice / multimodal engagements, this step drives voice-ux to produce a 5-layer rewrite (Instructions / Copy / Phrasebook / Opening / Handoff notes) plus an audit citing each change to a voice UX principle. The output augments the three scenarios already written; the page renders the bundle on a fourth `Voice` tab.

**Dependency delegation:**

Do not probe `agentforce-generate`, copy dependency paths, or reproduce installation guidance here. `voice-ux` owns and runs its own Phase 0 dependency gate when invoked, including harness-specific resolution and recovery.

Handle the result from `voice-ux`:

- **Ready:** continue with its rewrite workflow.
- **Blocked on the dependency:** surface the recovery guidance returned by `voice-ux`, then offer to retry after the user resolves it or skip voice mode.
- **Skip:** leave `voice: null` and continue to Step 10. The Voice tab will render the explainer.

Re-invoking `voice-ux` reruns its gate. Do not cache or reinterpret the dependency result in `conversation-design`.

**Branch question — existing chat agent or greenfield?**

Prepare the required inputs before invoking `voice-ux`. Ask via `AskUserQuestion`:

- **Yes — use existing chat AgentScript** *(if available)*: collect path to `.agent` file (or YAML / text instructions) + path to a sample conversation transcript (production log, hand-written mockup, or best-guess turn-by-turn).
- **No — synthesize from upstream artefacts**: skill drafts a chat AgentScript from `requirements.json` + `jtbd.json` + `architecture/actions.yaml` + the happy-path scenario just written; uses the same happy-path scenario as the sample transcript.

**Branch A (existing agent):**

```bash
mkdir -p _local/data/voice-ux-inputs
cp [user-supplied-script-path]     _local/data/voice-ux-inputs/source.agent
cp [user-supplied-transcript-path] _local/data/voice-ux-inputs/sample.md
```

**Branch B (synthesize):**

Draft a minimal chat AgentScript from upstream artefacts. The synthesis has to be honest — voice-ux's audit quality depends on it being representative. Use the priority capability (Step 4), its actions from `architecture/actions.yaml`, the persona's tone, and the happy-path scenario already drafted as both the script's flow and the sample. Write to `_local/data/voice-ux-inputs/source.agent` (text-instructions form is fine — voice-ux accepts YAML, `.agent`, or text). Use the happy-path scenario verbatim as `_local/data/voice-ux-inputs/sample.md`.

**Run voice-ux:**

```bash
cd $(git rev-parse --show-toplevel) || cd ~  # voice-ux runs against the engagement repo
[invoke voice-ux skill, pointing at the two input files]
```

Voice-ux writes its bundle to `artifacts/voice-ux/[agent-name]-voice-{migration,optimization}.md`. **Long-running phase** — voice-ux's Phase 4 audit + Phase 5 layer-write together typically take 8–15 minutes; emit progress every 60s per voice-ux's own conventions.

**Parse voice-ux output into the JSON shape:**

The page's `VoiceUxPreview.jsx` consumes a structured object. Parse voice-ux's labeled markdown (each Layer A–E section is delimited by `## Layer X — [name]` headings) into:

```javascript
voice: {
  voiceUx: {
    version: "[from voice-ux SKILL.md frontmatter]",
    runMode: "migrate" | "optimize",         // voice-ux confirmed mode
    sourceShape: "chat" | "voice",           // input shape
    summary: {
      principlesChecked: 12,
      patternsChanged: N,
      patternsOk: N,
      patternsReviewNeeded: N,
    },
  },
  layers: {
    instructions: {
      blurb: "[short framing]",
      sections: [{ heading, body, principles: ["P1 ...", "P9 ..."] }],
    },
    copy: {
      blurb: "[short framing]",
      changes: [{ kind: "changed"|"review needed", location, before, after, why }],
    },
    phrasebook: {
      blurb: "[short framing]",
      tokens: { acknowledgment: [...], empathy: [...], thinking: [...], handover: [...], closing: [...] },
    },
    opening: {
      blurb: "[short framing]",
      ivrLayer:   { speaker, copy, why },
      agentLayer: { speaker, copy, why },
      contrastNote: "[STRING]",
    },
    handoff: {
      blurb: "[short framing]",
      items: [{ owner, note, severity: "required"|"recommended" }],
    },
  },
  audit: {
    title: "Audit — voice UX principles",
    blurb: "[short framing]",
    rows: [{ id: "P1", name, status: "changed"|"ok"|"review needed", count }],
  },
}
```

Set this as the `voice` field in `_local/data/conversation-design.json` (already scaffolded as `null` in Step 9; rewrite the file with the populated object).

**Failure handling:**

- Voice-ux refuses inputs (Phase 1 / Phase 2 / Phase 3 fails) → surface the voice-ux error verbatim, leave `voice: null`, the Voice tab renders the explainer.
- Markdown parse fails → leave `voice: null` and write the markdown bundle path to `_local/data/conversation-design.voice.md` so the user can read it manually.
- User cancels mid-run → `voice: null`, continue to Step 10.

In all failure modes, the three chat-shaped scenarios from Step 7 are unaffected. Voice mode is additive.

### Step 10: Update engagement state

```bash
node -e '
const fs = require("fs");
const path = "./project.config.json";
const c = JSON.parse(fs.readFileSync(path, "utf8"));
const today = "[YYYY-MM-DD]";
const s = c.sections.find(x => x.id === "conversation-design");
if (s) {
  s.status = "in-progress";
  s.limitedPreview = true;
}
c.changelog = c.changelog || [];
c.changelog.unshift({
  date: today,
  type: "section-state",
  entry: "Conversation Design — three-scenario starter draft written.",
});
fs.writeFileSync(path, JSON.stringify(c, null, 2) + "\n");
'
```

The section sits at `in-progress` (with `limitedPreview: true` flagging that the deliverable is a starter draft, not corpus-grade). The page renders the three scenarios with a top-of-page draft banner — that banner is the user-facing signal that the work is a starter, not the section status pill.

### Step 11: Return to hub for publish

> "Three-scenario starter draft written to `_local/data/conversation-design.json`. The page renders the three scenarios across tabs (Happy Paths · Error States · Fallbacks) with a top-of-page draft banner. The team can flip per-scenario `draft` flags (or replace scenarios outright) as they expand from this draft into the full conversation design pass.
>
> If you'd like AXS support for the full pass, drop a note in `#axs-team-hub-skill`."

The hub runs `publish('conversation-design', config)` — emits the per-mode notice. Section sits as `in-progress` (with `limitedPreview: true`) until the team flips every scenario's `draft` flag to false (manual edit or future skill); at that point set `status: 'complete'` and clear `limitedPreview`.

---
