# Step 1: Read engagement context

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 1: Read engagement context
- Step 1.5: Baseline `.agent` input (Channel customisation / Script comparison / Redesign-with-baseline)
- Step 1.6: Approved deliverables to cite (Script comparison mode only)
- Step 1.7: Target channel(s) (Channel customisation mode only)
- Step 2: Re-run mode (only if existing architecture)
- Step 3: Grouping lens

### Step 1: Read engagement context

Load from `project.config.json`:
- `engagement.modes` → drives branching above; multi-select array (`["greenfield"]` / `["redesign","channel-customisation"]` / `["channel-customisation","script-comparison"]` etc.). If unset, ask the mode-detection prompt.
- `engagement.type` → **deprecated** — read for backwards compatibility only. If present and `engagement.modes` isn't set, map (`New build` → `["greenfield"]`, `Redesign` → `["redesign"]`, `Assessment` → skip and ask). Log a one-line notice suggesting migration to `engagement.modes`.
- `engagement.useCase.summary` → used in subagent naming and global instructions
- `engagement.channel` → the current channel — chat / voice / multimodal. For Channel customisation mode, this is the *source* channel; the target channel(s) are asked separately at Step 1.7.
- `engagement.transcripts.hasTranscripts` → if true, look for `_local/data/transcripts/intents.json` (and `coverage.json` for `failure_triage` mapping)
- `brand.agentName` → used in classification descriptions and global instructions
- `brand.toneSignals` → seeds global instructions voice
- `sections[]` → the engagement's scoped sections. Read to auto-populate the deliverables list in Step 1.6 (Script comparison mode).

Load upstream data files (each one optional — the skill degrades gracefully):
- `_local/data/capabilities.yaml` → required for Greenfield / Redesign (prerequisite check above); optional for Channel customisation / Script comparison (baseline `.agent` is the authoritative shape for those modes).
- `_local/data/persona.md` → if present, seeds global instructions and subagent naming
- `_local/data/jtbd.yaml` → if present, intent IDs come from here for the per-subagent intents-owned list
- `_local/data/transcripts/intents.json` and `_local/data/transcripts/coverage.json` → if present, populate verdict pills + intents-owned sessions counts (from intents.json) and failure modes (derived from coverage.json's `Covered poorly` / `Missed` intents)
- `_local/data/conversation-design.json` → if present, scenarios are read as a soft input. Specifically: handoff turns (where the script hands off to a human, another subagent, or a deferred capability) become candidate `handoff_triggers` per subagent; refusal / out-of-scope turns become candidate `scope_out` lines; the set of capabilities exercised across happy-path scenarios pressure-tests the subagent grouping. The skill never overrides decisions encoded in `subagents.yaml` from a prior run; conversation design is suggestive, not authoritative.
- `_local/data/subagents.yaml` and `_local/data/actions.yaml` → if present from a prior run, load existing architecture; offer merge / refine / replace
- `_local/data/agent-baseline/*.agent` → if present, offer the newest file as the default baseline for Channel customisation / Script comparison.
- `_local/data/decision-points.yaml` → if present from a prior run, load existing recommendations; offer re-run options at Step 2 (including "add more recommendations" for Script-comparison-specific re-runs).

### Step 1.5: Baseline `.agent` input (Channel customisation / Script comparison / Redesign-with-baseline)

Skip this step for Greenfield-only runs. For any mode that benefits from a verbatim baseline:

> "I need a baseline of the current agent to diff against. What do you have?
>
> 1. **`.agent` file** — export from Agentforce Builder (Setup → Agents → [name] → Export Metadata). Best fidelity — every recommendation cites verbatim text.
> 2. **`subagents.yaml` + `actions.yaml` from a previous build** — I'll use those. Loses verbatim text but preserves shape.
> 3. **Describe the current shape verbally** — I'll ask about each subagent and action in the conversation. Slower; use when the current agent isn't in Agentforce yet.
> 4. **Paste it here** — drop the `.agent` contents into the chat and I'll parse from that.
> 5. **Skip baseline for now** — I'll draft the target shape without diffing. Re-run once the baseline is on file.
>
> Which?"

**Script-comparison mode tightens the list** to options 1, 2, 4 only — verbatim text is required for the "before" side of every recommendation. Options 3 and 5 aren't offered.

**Auto-detect** — before showing the prompt, scan `_local/data/agent-baseline/*.agent` and `_local/data/subagents.yaml` / `_local/data/actions.yaml`. If a plausible baseline is found, offer it inline:

> "Found `Nova_Build_V2_sandbox.agent` in `_local/data/agent-baseline/` (last modified 2026-07-07). Use that as baseline, or pick a different option?"

**Persist pasted content** — when the user picks option 4, save the pasted `.agent` to `_local/data/agent-baseline/<name>.agent` automatically so re-runs pick it up. Ask the user for a filename (default: `baseline.agent`).

**Parsing is handed off to canonical.** `.agent` is Agentforce metadata — reading it, enumerating topics / subagents / actions, and surfacing the shape is `agentforce-generate`'s job (same handoff pattern `persona` uses — see `persona/SKILL.md` for the shape). This skill does not read the file with file tools and does not restate the grammar; it receives the parsed inventory and runs the confirmation step below.

**Parse confirmation (always, once baseline loaded)** — after the canonical skill returns the inventory, echo it and confirm with the user:

> "Baseline parsed. Here's the inventory, as read by `agentforce-generate`:
>
> - **Subagents**: `nova_router`, `Identify_Customer`, `customer_verification`, `account_balance`, `escalation`
> - **Actions** (count by impl_type): …
> - **Global instructions block**: present / absent
>
> Does this match the agent you want to diff against? If a subagent is missing or the naming looks off, tell me now — otherwise I'll use this as the baseline for every downstream diff.
>
> 1. **Looks right, continue**
> 2. **Something's off** — describe what, and I'll re-run the canonical parse"

If the user picks option 2, re-run the canonical parse with their feedback. Don't proceed until they confirm.

### Step 1.6: Approved deliverables to cite (Script comparison mode only)

Read the engagement's `sections[]` array from `project.config.json` and populate a checklist. Include every section that produces citable content; auto-check any with `status: "complete"` or a `signoff` block; leave `status: "in-progress"` sections unchecked but visible.

**Never hardcode the section list.** The skill reads what the engagement actually has — different engagements scope different sections in.

Prompt shape (populated dynamically per engagement):

> "I found these sections in this engagement. Which am I citing as the 'after' side of every recommendation?
>
> - [✓] **All of them** *(picks everything below)*
> - [✓] **Persona** — signed off by Jessica Jackson 2026-07-06
> - [✓] **JTBD** — complete
> - [✓] **Requirements** — complete (34 requirements)
> - [✓] **Conversation Design** — signed off by Jessica Jackson 2026-07-09
> - [✓] **Style Guide** — complete
> - [ ] **Testing & Performance** — in progress (check to include; recommendations citing it will be flagged `pending`)
>
> Uncheck any you don't want cited, or say 'go'."

**Provenance rendering** — use whatever the section's `signoff` block gives, falling back gracefully:
- `signoff.approvedBy` + `signoff.approvedOn` present → `"signed off by <name> <YYYY-MM-DD>"`
- `status: "complete"` without signoff → `"complete"`
- `status: "in-progress"` → `"in progress"` (unchecked by default)
- Neither → `"not started"` (unchecked, greyed-out label)

**After the checklist**, ask two follow-ups:

> "For each recommendation I produce, I'll cite where the 'after' side comes from — e.g. `Persona §9`, `R6`, `CD hp-golden Turn 11`. Two quick things:
>
> 1. **Any deliverable sections that are still in flux?** I'll flag any recommendation that cites them as `pending: <reason>` so the FDE knows it isn't yet lockable. *(Example: 'Des is still confirming the balance read-back format — anything citing that shouldn't be finalised.')*
> 2. **Any workshop decisions or transcript verdicts to treat as authoritative that aren't in the deliverables above?** I'll capture them as inline notes with a source label. *(Example: '7 Jul workshop decision on R16 — Mel confirmed ask-first for multi-account.')*"

Both answers are free-text; skill records them in `_local/data/decision-points.yaml` as top-level `pending_sources[]` and `additional_sources[]` respectively so the render can surface a "waiting on" strip and cite workshop decisions with the same LinkifiedText treatment as deliverable references.

### Step 1.7: Target channel(s) (Channel customisation mode only)

Read `engagement.channel` from the config for the *source* channel, then ask about the *target*:

> "The current agent runs on **[detected: chat]**. What channel(s) are you customising it for? Pick one or more.
>
> - [ ] **Voice** — telephony agent (Vonage / Agentforce Voice / similar). Enables voice-specific defaults: ASR-safe capture patterns, spoken-prose rendering, repair-tier ladders, phrasebook rotation.
> - [ ] **Multimodal** — voice + visual companion (e.g. an in-app companion screen alongside the call). Combines voice defaults with visual affordance mapping.
> - [ ] **In-app / embedded** — chat inside a mobile app or an authenticated web surface where UI can render alongside the agent. Different from generic chat: components-first rendering.
> - [ ] **Messaging (async)** — SMS / WhatsApp / other. Longer-lived context, delivery-receipt semantics, no typing indicator.
> - [ ] **Other** — describe it.
>
> If more than one is picked, each subagent gets a `variants:` map keyed by channel so per-channel deltas live in a single file rather than forking."

**Storage shape** — with a single target channel, use `subagent.voice_variant` / `action.voice_variant` (AusPost pattern, single-channel). With multiple target channels, promote to `subagent.variants.<channel>` / `action.variants.<channel>` so each channel's deltas live under a keyed sub-map. The skill renames existing single-channel keys on write when the user later adds a second channel.

**Channel-defaults matrix** — the skill draws draft variants using per-channel rules:
- **Voice** — flag anything that captures user input (ASR-safety), any Markdown/HTML rendering (spoken prose), any list of >3 items (progressive disclosure), any URL emission (paraphrase / SMS), any error string (repair-tier ladder), any Markdown card / table (drop for prose). Voice-specific rewrites of persona, capture ladders, and repair tiers belong in `voice-ux`; voice latency trade-offs (how aggressive to be with pre-fetch, when to drop a subagent fan-out, timing between prompts) are owned by `agentforce-generate` `references/voice-latency-heuristics.md`. This step captures what *needs* a voice variant and the design intent per delta; the rewrite and the latency judgement happen downstream.
- **Multimodal** — voice defaults plus companion-screen affordance mapping (which subagent outputs render to the visual channel).
- **In-app / embedded** — components-first rendering (any subagent output that maps to a UI component gets a `component_ref`).
- **Messaging** — async semantics (no typing indicator, session-scoped context, delivery-receipt handling).
- **Other** — user describes; skill captures free-text and doesn't apply defaults.

### Step 2: Re-run mode (only if existing architecture)

If `subagents.yaml` (or `decision-points.yaml` for Script-comparison re-runs) already exists, ask:

> "There's existing architecture for this engagement — [N] subagents covering [M] capabilities[, and K decision-point recommendations]. What would you like to do?
>
> 1. **Refine** — keep the existing structure, walk me through what to change
> 2. **Refresh from upstream** — re-compose `architecture.json` from current capabilities / transcript insights / persona without re-asking architectural decisions (best when upstream data has updated but the architecture itself is unchanged)
> 3. **Start fresh** — discard the existing architecture and design from scratch
> 4. **Show me what's there first** — print the existing subagents and actions
> 5. **Add more recommendations** *(Script-comparison mode only)* — keep the existing decision-points and draft additional ones against changed or newly-added baseline sections. I'll skip already-covered sections and only surface what's new."

Option 2 is the cheapest path — it just re-reads upstream files and re-writes `architecture.json` without any user prompts. Useful when the cap-prio skill re-ran with new capabilities, or transcript-insights produced new verdicts.

Option 3 archives the existing files to `_local/data/_archived/[YYYY-MM-DD]/` rather than deleting (so the team can recover if they regret it).

Option 5 (Script-comparison only) diffs the current baseline `.agent` against the version referenced by the last `decision-points.yaml` run. Sections with a matching hash are skipped; sections with new or changed text are surfaced as new draft recommendations. Useful when the sandbox has been iterated between reviews.

### Step 3: Grouping lens

> **What this group of steps owns.** Steps 3–6 produce an **experience-design view** of the agent: how MVP capabilities cluster into subagents, named in persona voice, with classification descriptions written in **user language** (not config language). The downstream mapping — when a grouping becomes a runtime subagent, how Agent Script's Subagent Map renders the clusters, and the valid routing surface at build-time — is owned by `agentforce-generate` `references/architecture-patterns.md` and the `assets/agent-spec-template.md` Subagent Map section. Nothing in Steps 3–6 restates that; the output here is the design intent the canonical skill maps into platform shape.

**Skip entirely for Redesign / Script-comparison / Channel-customisation when a baseline `.agent` was loaded.** The baseline is the authoritative subagent shape; asking how to cluster capabilities makes no sense. Only ask this step when Greenfield is picked, or when the user explicitly signals in the re-run "start fresh" flow that they want to reshape boundaries.

Ask the team how to cluster MVP capabilities:

- **By user lifecycle stage** — Discovery / Consideration / Onboarding / Service
- **By data domain** — Property data / Booking / Account / Billing
- **By intent family** — Information-seeking / Transactional / Support / Escalation
- **Hybrid** — usually what teams land on

Recommend hybrid as default. Pure-lifecycle works for journey-shaped agents; pure-domain works for service agents with bounded data sources; most engagements need a mix.

If the target-channel array includes **voice** (or an otherwise low-bandwidth channel), note the bias toward fewer, broader subagents: *"You picked voice as a target channel — I'll bias toward fewer, broader subagents. Voice agents that fan out too much create audible routing pauses."*
