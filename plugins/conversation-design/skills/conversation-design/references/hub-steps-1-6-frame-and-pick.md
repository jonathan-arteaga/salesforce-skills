# Step 1: Frame the limited preview

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Step 1: Frame the limited preview

Print this once at the top of the run:

> "Quick framing — this skill produces **three scenarios**: one happy path, one error state, one fallback. It's a starter draft you (or an AXS, if one is staffed) expand from. Each flow is capped at 4–8 turns. The full design pass — voice rewrite, error coverage at scale, refusal points — is the next step beyond what this skill produces. I'll mark every scenario `draft: true` so the page surfaces a top banner until the team flips it."

### Step 2: Read engagement context

Load from `project.config.json`:

- `engagement.useCase.summary` — used to anchor scenario narratives
- `engagement.channel` — required. Drives turn payload shape: `chat` → components, `voice` → prosody cues, `multimodal` → both. If missing, ask the user once and write back to config.
- `engagement.region` and `engagement.language` — drives voice cadence (US English vs British English vs other)
- `brand.agentName` — used as the agent's role identifier in flows
- `brand.toneSignals` — hints when persona is absent

Load upstream data files (each one optional — the skill degrades gracefully):

- `_local/data/capabilities.yaml` → required (prerequisite check above)
- `_local/data/persona.md` → if present, voice the agent turns in persona; if absent, generate generic-friendly voice and flag for AXS pass
- `_local/data/subagents.yaml` and `_local/data/actions.yaml` → if present, anchor each scenario to an owning subagent and reference relevant action IDs
- `_local/data/jtbd.yaml` → if present, the happy-path scenario picks a top job-to-be-done as its goal
- `_local/data/transcripts/intents.json` → if present, error state and fallback scenarios are grounded in real intents that failed (`Covered poorly` / `Missed`)

### Step 3: Determine fidelity moment

Ask:

> "Where in the journey are we? This shapes how concrete the scenarios need to be:
>
> 1. **Design fidelity** *(default)* — persona, capability cut, and (ideally) architecture are in place. The scenarios will be fairly concrete: real turns, real component callouts, plausible error language.
> 2. **Concept fidelity** — earlier moment: persona + use case + capability sketch only. The scenarios will be looser — closer to concept narratives than designed flows."

Set `phase: design-fidelity | concept-fidelity`. Default to design-fidelity if persona + capabilities + architecture are all present and the user doesn't object.

### Step 4: Pick the happy-path capability

For the **happy-path** scenario, the choice is what to demonstrate first. Default ranking:

1. If JTBD exists, pick the highest-priority job and the MVP capability that serves it.
2. Else if architecture exists, pick the subagent named first in `diagram.stages` and a capability inside it.
3. Else pick the first MVP capability in `capabilities.yaml`.

Surface the pick to the user — let them override:

> "I'd start the happy path with **[Capability ID — name]** — *[one-line why: it's the top JTBD / it's the first subagent / etc.]*. Want me to use this one, or pick a different capability?"

If the user names another, use it.

### Step 5: Pick the error-state scenario

The error scenario captures a *plausible* break in the flow, not a worst-case enumeration. Default rules:

- If transcript insights exist, pick an intent marked `Covered poorly` or `Missed` — the failure mode is grounded in a real failure.
- Else default to a category appropriate to the channel:
  - `chat` → `validation_failure` (user input doesn't parse) or `repeat_failure` (agent can't classify intent)
  - `voice` → `recognition_failure` (ASR couldn't parse the user) or `timeout` (silence / off-mic)
  - `multimodal` → `surface_handoff_failure` (user attempts to switch surface mid-flow and the handoff drops state)

Surface the pick:

> "For the error state I'd model **[error type]** — *[one-line why]*. Use this, or pick a different break to model?"

Capture as `error_subtype` — used in scenario metadata.

### Step 6: Pick the fallback scenario

The fallback captures a path the agent **can't complete**. Default rules:

- If capabilities are tagged with phase, pick a Phase 2 / Stretch capability the user might ask for that doesn't exist in MVP — model the deferral fallback.
- Else default to an out-of-scope ask grounded in `engagement.useCase` (e.g. for a property-discovery agent, an out-of-scope ask about billing).
- Always include the escalation path — even if the fallback is "deferred capability", the closing turn should offer a human handoff if the user pushes back.

Surface:

> "For the fallback I'd model **[fallback subtype, e.g. 'capability not in MVP — deferred to Phase 2']** — *[one-line why]*. Use this, or pick a different fallback?"

Capture as `fallback_subtype`.
