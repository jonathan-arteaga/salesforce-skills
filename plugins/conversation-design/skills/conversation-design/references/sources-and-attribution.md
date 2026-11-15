# Sources and Attribution

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Sources and Attribution

This skill applies the following frameworks:

- **Three-scenario starter draft** — bounds the output so this skill's deliverable doesn't drift into "the full conversation design". Cassandra Popli, drawing on the AXS-led work gate pattern shared across Architecture / Concept Design / Style Guide / Testing & Performance / User Testing.
- **Channel-aware turn payloads** — `prosody_cues` for voice, `components` for chat (when a visual upstream exists), both for multimodal. Keeps the JSON shape unified across channels while making each channel's design surface explicit.
- **Strict upstream gating for `actions[]` and `components[]`** — record only what's grounded in real upstream files. Empty arrays plus a `global_notes` line beats fabricated IDs that point at nothing.
- **`draft: true` flag with team-side flip** — keeps the starter draft honest. The skill cannot mark anything as shipped; the team (or an AXS in the seat) flips per-scenario flags as scenarios get expanded into corpus-grade design.
- **Phase split (`design-fidelity` vs `concept-fidelity`)** — captures whether the draft is concrete enough to brief a build or still loose enough to brief a concept. Most engagements pass through both; this skill can run in either.
- **Salesforce Agentforce conversation-design conventions** — turn-based flow shape, role taxonomy (user / agent / system), action ID references back to `actions.yaml`.
- **Cassandra Popli** — the starter-draft framing, the notes-as-honest-handoff pattern, the integration with the AXS-led work gate, the upstream-gating rules for actions / components, and the explicit "this is a starter, not the deliverable" framing baked into every user-facing message.
