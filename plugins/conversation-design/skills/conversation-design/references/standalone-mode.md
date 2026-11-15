# Standalone Mode

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Standalone Mode

Same flow, with these adjustments:

- **No engagement context to read.** Step 2 asks the user to point at upstream files (capability list, persona doc, architecture file). Capability list is required; the rest are optional.
- **All file paths are relative to cwd.**
- **No `project.config.json` updates** — engagement state writes are skipped.
- **Markdown export at `./_local/exports/conversation-design.md`** — additional output, not present in hub mode.

The standalone Step 1 introduces the framing the same way:

> "Heads-up: this skill writes a **three-scenario starter draft** — one happy path, one error state, one fallback. It's a working set you expand from, not the conversation design itself. The full pass — voice rewrite, error coverage at scale, refusal points, calibrated clarification — is the next step beyond this skill. If your team has an Agentic Experience Specialist (AXS), they should lead that pass; otherwise the team picks it up.
>
> Continue with the starter draft?"

If yes, proceed with Steps 2–10 (skipping config-related writes). Add Step 11 below.

### Step 11 (standalone) — Markdown export

Render `./_local/exports/conversation-design.md` from the canonical JSON. The export mirrors the page: scenario header + turn-by-turn flow + per-scenario open questions. The `actions[]` and `components[]` arrays are recorded in the JSON but not surfaced in the markdown — they're load-bearing for build-map / coverage tooling, not for customer-facing reading.

```markdown
# Conversation Design — starter draft

*Three scenarios. Channel: {{channel}}. Phase: {{phase}}. Drafted on {{drafted_at}}.*

> This is a starter draft of three scenarios — one happy path, one error state, one fallback. Use it as a working set the team (or an Agentic Experience Specialist) expands into a full conversation design: voice rewrite, error coverage at scale, refusal points, calibrated clarification.

{{#global_notes.length}}
## Notes
{{#global_notes}}
- {{.}}
{{/global_notes}}
{{/global_notes.length}}

{{#design_decisions_pending.length}}
## Decisions pending
{{#design_decisions_pending}}
- {{.}}
{{/design_decisions_pending}}
{{/design_decisions_pending.length}}

---

{{#scenarios}}
## {{title}}

**Type:** {{type_label}} · **Capability:** {{capability_id}}{{#subagent_id}} · **Subagent:** {{subagent_id}}{{/subagent_id}}
**Goal:** {{goal}}
**Phase marker:** {{phase_marker}}

**Preconditions:** auth = {{preconditions.auth}}, channel = {{preconditions.channel_mode}}{{#preconditions.prior_context}}, prior context: *{{preconditions.prior_context}}*{{/preconditions.prior_context}}

| Turn | Role | Utterance |
|---|---|---|
{{#flow}}
| {{turn}} | {{role}} | {{utterance}} |
{{/flow}}

{{#hasProsody}}
**Prosody cues:**
{{#flow_with_prosody}}
- *Turn {{turn}}* — `{{type}}: {{marker}}`{{#target_phrase}} on "{{target_phrase}}"{{/target_phrase}}
{{/flow_with_prosody}}
{{/hasProsody}}

{{#notes.length}}
**Open questions:**
{{#notes}}
- {{.}}
{{/notes}}
{{/notes.length}}

---

{{/scenarios}}
```

The export is **customer-clean** — the framing line at top is the only meta-copy, and it explains plainly what the reader is looking at. Voice / multimodal scenarios surface prosody cues since those are intrinsic to the channel; chat-channel scenarios suppress that block entirely. Action IDs and component callouts are intentionally omitted from the markdown export (preserved in the JSON only).

---
