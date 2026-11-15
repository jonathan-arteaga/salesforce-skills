# Entry points

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Entry points

Both entry points work for all modes.

**Hub mode** — invoked from inside an AXS engagement. Detected by finding `project.config.json` in the working directory or a parent. Reads engagement context (use case, channel, region, **engagement type**, persona signals, transcripts metadata, regulatory context if any) from the config; reads upstream data files (`capabilities.yaml`, `actions.yaml` if a prior architecture run exists, the Transcript Insights files at `_local/data/transcripts/intents.json` + `coverage.json` if transcript-insights ran, persona doc, `conversation-design.json` as a soft input when present); writes canonical state to `_local/data/`; returns control to the hub for publish.

**Standalone mode** — runs from any folder. Greenfield / Redesign need `capabilities.yaml` (or a pasted list, written to that file per the Prerequisite Check); Channel customisation / Script comparison need a baseline `.agent` file (and, for Script comparison, paths to approved deliverables asked manually since there's no config to auto-detect them from). Produces `architecture.json` (and, when relevant, `decision-points.yaml`) plus a markdown export at `./_local/exports/agent-architecture.md`.

**What it produces (all modes):**

- `_local/data/subagents.yaml` — subagent grouping (id, name, classification_description, scope_in, scope_out, handoff_triggers, capabilities[]). Channel-customisation adds `<channel>_variant` (severity, summary, deltas[]) and optional `voice_open_questions[]` per subagent.
- `_local/data/actions.yaml` — per-capability actions (id, capability_id, type, impl_type, inputs, outputs, dependencies, build_owner). Channel-customisation adds `<channel>_variant` (severity, progress_message, modifications[]) per action.
- `_local/data/global-instructions.md` — global instructions topic, persona-voiced. Channel-customisation additionally records `channel_deltas` per target channel.
- `_local/data/build-map.md` — human-readable architecture handoff for the FDE.
- `_local/data/architecture.json` — denormalised composite that drives the rich page (see [Output: architecture.json](#output-architecturejson) below).

**What it produces (Channel customisation / Script comparison):**

- `_local/data/agent-baseline/<name>.agent` — the parsed baseline `.agent` file, persisted so downstream re-runs pick up the same reference. Written when the user pastes contents or supplies a path outside this directory.

**What it produces (Script comparison only):**

- `_local/data/decision-points.yaml` — array of surgical before/after recommendations, each with `id`, `iteration`, `requirement_ref`, `subagent`, `title`, `change_scope` (script / flow / ivr / knowledge / integration / site), `before_text`, `after_text`, `recommendation`, optional `pending`, optional `decision` (will-implement / wont-implement / needs-discussion).
- **Gated handoff, not a file this skill writes:** a proposed `.agent` is produced by `agentforce-generate` from the approved recommendations, and only when the user explicitly asks after refining `decision-points.yaml`. It stays labelled "proposed, not validated" until that skill compiles and validates it. See Step 13, item 7.

**What it produces (standalone only, additive):**

- `_local/exports/agent-architecture.md` — customer-clean markdown export.

**What it co-iterates with and feeds:**

- **Conversation Design** — co-iterates. Many engagements draft happy-path scenarios first and let the handoffs reveal natural subagent boundaries; others decompose architecture first and let subagent scope shape conversation design. Both orderings are valid. When `_local/data/conversation-design.json` already exists, this skill reads it as a soft input — handoff triggers in scenarios surface as candidate subagent boundaries; refusal points surface as candidate scope-out lines. When this skill runs first, the architecture page's design-reference chips deep-link out to Conversation Design scenarios as they're written.
- **Style Guide** — referenced from the architecture page's design-reference chips for the components called out in subagent UI.
- **Testing & Performance** — uses the action specs as test boundaries.
- **Agent Script change worklist** — once Script-comparison decisions are approved, `designing-agentforce-labs:agentscript-change-worklist` can turn them into a source-grounded developer handoff (exact excerpts, dependencies, ownership, proof seams). Agent Architecture is one optional upstream source; the worklist also accepts approved changes from other review artifacts or an accepted baseline/candidate delta. The optional worklist lives in `designing-agentforce-labs` and requires a separate install. The worklist enriches decisions without revising them. Agent Architecture stays authoritative for recommendations it produced, and current Agent Script tooling establishes exact source, compile status, and runtime evidence. The worklist appears inside this page's **Agent Script** view when one is published.
- **Technical Spec** (future skill) — will eventually own the integration map / build detail / data dependencies for FDE-internal use. Until that skill ships, this skill captures integration data on an optional "Integration" tab so FDEs aren't left without a home for it (see [Integration tab](#integration-tab) below).

---
