---
name: |-
  agent-architecture
description: |-
  Plan Agentforce architecture and design-only proposals with subagents, actions, and routing. Use agentforce-generate when asked to create, build, or modify an agent implementation; use agentforce-architecture-analyze to inventory deployed metadata.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.

For industry-specific agents, cross-industry ideation, or role/personality choices, read the selected patterns in [industry and role design](references/shared/industry-patterns.md). Use them within this skill’s ownership; distinguish documented capabilities from proposed designs.


# Agent Architecture

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## Canonical-source boundary

This skill authors design-time artefacts from AXS deliverables (capabilities, persona, conversation design, requirements). It does **not** introspect a deployed agent in an org. For runtime introspection of an existing deployed agent — walking `BotDefinition` / `GenAiPlanner*` / `Flow` / `ApexClass` metadata from a Salesforce org — defer to `agentforce-architecture-analyze` (canonical source). This skill accepts a `.agent` file (an Agentforce metadata export) as input for channel-customisation / script-comparison modes; if the user needs to *obtain* the `.agent` from a running org, they can either export from Setup → Agents → \[name\] → Export Metadata, or run `agentforce-architecture-analyze` first to inventory what's there.

Resolve companion skills by their skill name in the current host catalog; do not assume an older package namespace is installed. If a companion is unavailable, complete the independent design work from supplied evidence and report the unavailable capability. Do not invent a tool or claim deployed metadata was inspected.

## How to Use

The skill takes a finalised capability cut (`capabilities.yaml`) and/or a baseline `.agent` file, plus approved AXS deliverables, and produces:

- **Subagent decomposition** — start with one focused execution block; add subagents only for distinct responsibilities, tool access, or handoff needs. Each subagent owns a coherent set of capabilities, each with a classification description (the "when to route here" instruction the master agent reads at runtime), in-scope / out-of-scope boundaries, and handoff triggers.
- **Action specs per capability** — type (Standard Action / Flow / Apex / Prompt Template / MCP / Headless), implementation type (Apex / Flow / CLT / Knowledge / Data 360 / Agent instruction), inputs, outputs, dependencies, build owner.
- **Global instructions topic** — the persona-voiced instructions that run across every subagent.
- **Integration map** — the external systems the agent depends on, with ownership pills (FDE / Customer / Joint / External) and "blocks end-to-end testing" warnings where applicable.
- **Denormalised composite** — `architecture.json` that drives the rich agent architecture page on the AXS site (Overview, Subagent Detail, and Integration tabs — Integration appears only when one or more integrations are captured).

**This is the design artefact, not the technical spec.** The architecture page tells reviewers what the agent's shape is and why; the technical spec deliverable (separate skill, produces `technical-spec.md`) gives the FDE the build-detail their Apex/Flow/MCP work runs against. They share IDs but they're different documents for different audiences.

### Modes (multi-select)

The skill runs in one or more of four modes. Greenfield is exclusive (can't combine with the others); Redesign, Channel customisation, and Script comparison compose freely.

| Mode | When to use | Key input | Key output(s) |
| --- | --- | --- | --- |
| **Greenfield** | New agent from a prioritised capability list. No existing agent to reference. *(Exclusive — can't combine.)* | `capabilities.yaml` | `subagents.yaml`, `actions.yaml`, `global-instructions.md`, `architecture.json` |
| **Redesign** | Existing agent whose subagent boundaries / actions are being reshaped. | Baseline `.agent` (or previous `subagents.yaml`/`actions.yaml`) + `capabilities.yaml` | Same as greenfield, with continuity pills (`risk`, `carries_forward`, `changes_from_today`) per subagent |
| **Channel customisation** | Existing agent adapted for a new channel (typically chat → voice). Shape stays; behaviour overlays per channel. | Baseline `.agent`  • target channel(s) | Extends `subagents.yaml`  • `actions.yaml` with `voice_variant` (or matching `<channel>_variant`) blocks; optional `voice_open_questions[]` |
| **Script comparison** | Existing `.agent` needs surgical edits to align with approved deliverables (persona / CD / requirements). Produces a review-ready recommendation list for the FDE. | Baseline `.agent`  • approved deliverables (persona, CD, requirements, etc.) | `decision-points.yaml` — array of before/after cards with `change_scope`, `requirement_ref`, `pending?` |

The hub-side render adapts to which modes are in play — Channel customisation adds voice-variant blocks to the subagent detail view; Script comparison surfaces an "Agent Script Comparison" tab reading `decision-points.yaml`; both add a Downloads block for the baseline `.agent` (and, in Script-comparison, a proposed `.agent` once `agentforce-generate` produces one from the approved recommendations).

### Entry points

Consult [`references/entry-points-and-outputs.md`](references/entry-points-and-outputs.md) before Step 1 in either mode (what each entry point reads and writes).

## Framework Grounding

Read [`references/framework-grounding.md`](references/framework-grounding.md) for design lenses, source tiers, and `grounded_in[]`.

## Dialect discipline

Consult [`references/dialect-discipline.md`](references/dialect-discipline.md) before drafting any text: every artefact uses the dialect in `engagement.language`, with no silent fallback to US English.

## Entry Point Detection

```bash
# Look for project.config.json in cwd or up to 3 parents.
node -e '
const fs = require("fs");
const path = require("path");
let dir = process.cwd();
for (let i = 0; i < 4; i++) {
  if (fs.existsSync(path.join(dir, "project.config.json"))) {
    console.log("hub:" + dir);
    process.exit(0);
  }
  const parent = path.dirname(dir);
  if (parent === dir) break;
  dir = parent;
}
console.log("standalone");
'
```

- **`hub:<engagement-root>`** → **Hub mode**.
- **`standalone`** → **Standalone mode**.

**Override.** If the user explicitly says *"standalone mode"*, honour that even inside an engagement folder.

---

## Prerequisite Check

Select the requested mode before checking inputs. Greenfield and Redesign need a prioritized capability list, supplied in the request or in `capabilities.yaml`. Channel customisation and Script comparison use the supplied baseline `.agent`; a capability file is optional for those modes.

For Greenfield or Redesign, use the supplied list first; otherwise look in `<engagement-root>/_local/data/capabilities.yaml` (hub) or `./capabilities.yaml` and `./_local/data/capabilities.yaml` (standalone). Ask for a missing list only after checking the available request and sources.

Normalize a pasted list without changing its meaning or priority. Preserve provided IDs; otherwise assign `P1`, `P2`, and so on in order. When file output is requested, save it under `_local/data/capabilities.yaml`; for an inline-only request, keep the normalized list in the response without writing files. Continue the authorized design without a second confirmation. Carry forward explicit finalization of the supplied capabilities, but label the architecture as draft until approved. Ask only if normalization would materially change meaning or scope.

If the capability list has `signoff.status: pending`, identify that limitation and proceed with draft architecture; do not claim stakeholder sign-off.

---

## Mode Detection

Use the explicit mode in the current request first, then `engagement.modes` from `project.config.json` (hub mode). Otherwise infer the mode from the requested outcome and inputs; ask only if it remains ambiguous. Modes are multi-selectable except **Greenfield**, which is exclusive.

### Prompt (only when the intended mode is unresolved)

<quote>
"What kind of agent architecture work is this? Pick one or more.

- [ ] **Greenfield** — designing a new agent from a prioritised capability list. No existing agent to reference. *(Exclusive — can't combine with the others.)*
- [ ] **Redesign** — reshaping an existing agent's subagent boundaries and actions. Continuity gets tracked per subagent (what carries forward, what's changing).
- [ ] **Channel customisation** — the agent's shape is settled; we're adapting it for an additional channel (typically chat → voice). Produces a per-subagent + per-action variant overlay layered on top of the existing structure.
- [ ] **Script comparison against approved design** — an existing agent needs surgical edits to match approved deliverables (persona, conversation design, requirements). Produces a review-ready list of before/after recommendations for the FDE to work through.

Which apply?"
</quote>

**Enforcement:** If Greenfield is picked alongside anything else, warn: *"Greenfield can't combine with the others — it's for a new agent with no existing baseline. Which did you mean?"* Re-ask.

### Mode-driven branching

| Mode | Continuity pills | Carries-forward / changes-from-today | Baseline `.agent` input | Extra outputs |
| --- | --- | --- | --- | --- |
| **Greenfield** | Skipped | Skipped | Not asked | — |
| **Redesign** | Required per subagent | Required per subagent (auto-drafted from baseline when present, else user-driven) | Optional but recommended — offers verbatim before-side references | — |
| **Channel customisation** | Required only if combined with Redesign | Required only if combined with Redesign | **Required** — the channel variant overlays the baseline shape | `<channel>_variant` blocks in `subagents.yaml`  • `actions.yaml`; optional `voice_open_questions[]`; channel-deltas in `global-instructions.md`; Downloads block on hub for baseline + rebuilt `.agent` |
| **Script comparison** | Skipped (structure doesn't change) | Skipped | **Required** — the baseline is the "before" side, verbatim | `decision-points.yaml`; Downloads block on hub for baseline + (gated, produced by `agentforce-generate`) proposed `.agent`; Agent Script Comparison tab on hub |

Continuity pills (`risk: Low|Medium|High` mapping to "Mostly preserved" / "Substantial rework" / "Mostly new") and the carries-forward / changes-from-today blocks **only render on the page when the data is present**. Modes that skip them mean the page renders cleanly without those fields, not with empty pills.

If the user states a different mode framing during the conversation (e.g. calls a Redesign engagement "just some tweaks" that actually reshapes boundaries), ask once and update `engagement.modes` in the config — don't silently override.

---

## Hub Mode Flow

### Step 1: Read engagement context

Consult [`references/hub-steps-1-3-intake.md`](references/hub-steps-1-3-intake.md) before Hub mode Step 1, and before Standalone Step 3 (which runs Hub Step 3). Covers: Step 1.5: Baseline `.agent` input (Channel customisation / Script comparison / Redesign-with-baseline); Step 1.6: Approved deliverables to cite (Script comparison mode only); Step 1.7: Target channel(s) (Channel customisation mode only); Step 2: Re-run mode (only if existing architecture); Step 3: Grouping lens.

### Step 4: Draft subagents

Consult [`references/steps-4-9-design.md`](references/steps-4-9-design.md) before Step 4 in either mode (Standalone mode runs these steps too). Covers: Step 4.5: Pattern selection; Step 5: Classification descriptions; Step 6: Routing clarity test; Step 6.5: Routing contract capture; Step 7: Scope per subagent; Step 8: Action definition; Step 8.5: Integration map (optional, FDE-leaning); Step 8.6: Voice / channel variant capture (Channel customisation mode only); Step 8.7: Decision-points capture (Script comparison mode only); Step 9: Platform dependency banner (optional); Step 9.5: Instruction override capture.

### Step 10: Global instructions topic

Consult [`references/steps-10-15-write.md`](references/steps-10-15-write.md) before Step 10 in either mode (Standalone mode runs Steps 10-12 too). Covers: Step 11: Design references (computed); Step 12: Present and confirm; Step 13: Write canonical files; Step 14: Update engagement state; Step 15: Return to hub for publish.

## Standalone Mode Flow

Consult [`references/standalone-mode-flow.md`](references/standalone-mode-flow.md) before any step in Standalone mode.

## Output: architecture.json

Consult [`references/architecture-json.md`](references/architecture-json.md) before writing or validating `architecture.json`.

## Quality Standards

Consult [`references/quality-standards.md`](references/quality-standards.md) before Step 12 (Present and confirm) and before writing any deliverable.

## Interaction Design

**Output before questions.** Show drafted subagents and proposed actions before asking what to change. Never ask empty clarifying questions before showing a draft.

**Default the framework.** Hybrid grouping is the recommended default — confirm rather than offer a menu unless the user pushes back.

**Get to a draft fast.** A first cut at 80% accuracy is more useful than a slow perfect one. The team will refine in the review loop.

**Surface routing overlaps early.** Pairwise classification description checks happen before scope, not after — wrong subagent boundaries are expensive to undo.

**Make build ownership explicit.** Every action gets an owner. Unowned actions don't ship; flag them and either reassign or demote.

**Preserve persona voice.** If persona is available, use it for subagent names, classification descriptions, and global instructions. If absent, flag every voice-shaped output for revisit.

**Don't fabricate continuity data.** For Redesign mode, if the user can't articulate `carries_forward` for a subagent, leave it null. Don't invent rationale.

**Don't fabricate transcript verdicts.** Verdict pills should only appear when transcript-insights has actually run. Never hardcode "Covered well" because it sounds good — that's the kind of thing that erodes trust in the artefact.

**Draft from baseline when it's there; confirm rather than compose.** When a baseline `.agent` is loaded, seed subagent shape, carries-forward paragraphs, and channel-variant drafts from the baseline text. Ask the user to confirm or edit rather than composing blind. Confirming a drafted paragraph is fast; composing one from scratch is slow and drops signal.

**Section-by-section confirmation for decision-points.** With 20–50 recommendations typical in Script-comparison mode, per-record confirmation is exhausting; silent-then-summary is easy to miss. Group by baseline section (config → global → per-subagent → actions) and present a compact table with bulk-accept and "open \[#\]" per section. Reviewers naturally read a `.agent` this way — the interaction matches the artefact.

<b>Gate the proposed </b>**`.agent`**<b> handoff.</b> Automatic generation creates the illusion that everything's approved when only the yaml has been reviewed. Users refine `decision-points.yaml` first, then explicitly ask for the proposed `.agent`, which `agentforce-generate` produces and validates.

---

## Sources and Attribution

Read [`references/sources-and-attribution.md`](references/sources-and-attribution.md) for framework provenance.
