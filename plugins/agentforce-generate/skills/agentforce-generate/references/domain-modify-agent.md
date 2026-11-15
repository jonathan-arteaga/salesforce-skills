# Modify an Existing Agent

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Modify an Existing Agent

Use for an approved change to an existing response, route, action, subagent,
state flow, grounding source, or modality.

1. Comprehend the affected paths first. For a material design change, update the
   Agent Spec and obtain approval; for a narrow specified repair, record the
   affected use case without forcing a full spec rewrite.
2. Read [Core Language](agent-script-core-language.md) and only the
   feature references needed for the change. Preserve unrelated metadata,
   contracts, formatting, and behavior.
3. Edit the existing bundle in place. Generate action implementations only when
   explicitly requested.
4. Compile locally and, when available, validate against the target org. Preview
   every changed and adjacent path and inspect traces. Iterate in draft.
5. Use the release workflow only if the user separately requests release.
