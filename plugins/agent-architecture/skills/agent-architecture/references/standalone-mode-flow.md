# Standalone Mode Flow

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Standalone Mode Flow
  - Step 1: Modes
  - Step 2: Find capabilities OR baseline
  - Step 2.5: Approved deliverables (Script-comparison standalone)
  - Step 3: Run Steps 3–12 from Hub mode
  - Step 4: Write canonical state + markdown export
  - Step 5: Confirm to the user

## Standalone Mode Flow

The skill runs as a self-contained tool. No engagement state, no hub callback — just `capabilities.yaml` (Greenfield / Redesign) or a baseline `.agent` (Channel-customisation / Script-comparison) → architecture composition → `architecture.json` + markdown export.

### Step 1: Modes

Infer the mode from the current request and supplied inputs. Ask the mode-detection prompt only when the choice remains ambiguous (same wording as Hub Mode → Mode Detection). Multi-select applies. Standalone supports all four modes, including Script-comparison — the difference is that Step 1.6 (deliverables to cite) asks the user for paths manually because there's no `project.config.json` to auto-populate from.

> "Brief description for the markdown header (one line — e.g. 'Property sales agent — MVP architecture proposal')"

### Step 2: Find capabilities OR baseline

- **Greenfield / Redesign** — look for `capabilities.yaml` in the cwd or `./_local/data/`. If absent, ask the user to point at one or paste the list; a pasted list is written to `./_local/data/capabilities.yaml` as described in the Prerequisite Check. Don't proceed without one of the two.
- **Channel-customisation / Script-comparison** — run Step 1.5 (baseline `.agent` input). `capabilities.yaml` is optional in these modes; the baseline is authoritative.

### Step 2.5: Approved deliverables (Script-comparison standalone)

In Hub mode, deliverables come from the engagement's `sections[]` array. In standalone, use supplied paths and content first; ask only for missing sources needed to ground the requested comparison:

> "Script-comparison needs approved deliverables to cite as the 'after' side of every recommendation. Point me at each one you have (skip any that don't apply):
>
> 1. **Persona doc** — path to markdown or a paste
> 2. **Conversation design** — path to JSON, markdown, or a paste
> 3. **Requirements** — path to JSON, markdown, or a paste
> 4. **Style guide** — path to JSON, markdown, or a paste
> 5. **Additional sources** — workshop decisions, transcript verdicts, or any other authoritative source. Free-text label + content per source.
>
> Supply only what is missing; I can continue with the sources already provided."

The skill persists whatever's supplied under `./_local/data/` (`persona.md`, `conversation-design.json`, etc.) so a subsequent hub-mode migration finds them in the expected places.

### Step 3: Run Steps 3–12 from Hub mode

Same as hub mode, with these adjustments:
- Skip the "engagement context" reads (no `project.config.json`)
- Skip the "transcript insights" read unless the user explicitly points at a `_local/data/transcripts/` directory containing `intents.json` (and optionally `coverage.json`)
- All file paths are relative to cwd
- No call to update `project.config.json` — there isn't one
- Steps 1.6 and 1.7 use the paths captured at Step 2.5 above rather than config-driven auto-detect.

### Step 4: Write canonical state + markdown export

Same writes as hub mode: `subagents.yaml`, `actions.yaml`, `global-instructions.md`, `build-map.md`, `architecture.json`, plus mode-specific outputs (`decision-points.yaml`, `agent-baseline/*.agent`) and a markdown export at `./_local/exports/agent-architecture.md`.

The markdown export uses this template (rendered against the same data shape as `architecture.json`):

```markdown
# Agent Architecture

*{{description}}*

{{intro}}

## Architecture overview

{{#diagram.stages}}
- **{{name}}** — {{#subagents}}[{{name}}](#{{id}}){{^last}}, {{/last}}{{/subagents}}
{{/diagram.stages}}

{{#diagram.cross_cutting}}
**Always-on:** {{description}}
{{/diagram.cross_cutting}}

{{#platform_dependency}}
> ⚠ **{{title}}**
>
> {{body}}
{{/platform_dependency}}

## Subagents

{{#subagents}}
### {{name}} {#{{id}}}

**Stage:** {{stage}} · **Owner:** {{owner}}{{#risk}} · **Continuity:** {{risk_label}}{{/risk}}

{{what_it_does}}

**Why it exists:** {{why_it_exists}}

#### Intents owned
{{#intents_owned}}
- **{{id}}** — {{name}}{{#sessions}} ({{sessions}} sessions{{#verdict}}, {{verdict}}{{/verdict}}){{/sessions}}
{{/intents_owned}}

#### Capabilities delivered
{{#capabilities}}
- **{{id}}** — {{name}}
{{/capabilities}}

{{#carries_forward}}
**Carries forward:** {{carries_forward}}
{{/carries_forward}}

{{#changes_from_today}}
**Changes from today:** {{changes_from_today_text}}
{{/changes_from_today}}

#### Candidate actions
{{#actions}}
- **{{name}}** *({{type}}, {{impl_type}})* — {{purpose}}
{{/actions}}

{{#open_questions.length}}
**Open questions:**
{{#open_questions}}
- {{.}}
{{/open_questions}}
{{/open_questions.length}}

{{/subagents}}

## Global instructions

{{global_instructions_content}}
```

### Step 5: Confirm to the user

> "Done. Architecture composed from [N] capabilities into [M] subagents with [L] actions:
>
> - `./_local/data/architecture.json` — denormalised composite (drives the rich page if you ever scaffold one)
> - `./_local/data/subagents.yaml` + `./_local/data/actions.yaml` + `./_local/data/global-instructions.md` + `./_local/data/build-map.md` — structured truth
> - `./_local/exports/agent-architecture.md` — markdown export
>
> Re-run any time to refine. If your `capabilities.yaml` or `_local/data/transcripts/` files update, re-running picks up the changes.
>
> **Next step pointers:** If you're moving into build, `agentforce-generate` reads the subagent + action shapes 1:1. If you're writing the Agent Spec next, `agentforce-architecture-analyze` can reconcile this design against the deployed metadata once there is one. Patterns picked at Step 4.5 (see `references/patterns/`) resolve in each downstream skill against the same contract shape — no re-authoring."

---
