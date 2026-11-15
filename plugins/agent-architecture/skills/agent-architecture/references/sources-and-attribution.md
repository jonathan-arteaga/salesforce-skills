# Sources and Attribution

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Sources and Attribution

This skill applies the following frameworks:

- **Salesforce Agentforce architecture** — subagent (formerly topic), action, classification description, global instructions concepts
- **Cassandra Popli** — original framework elements: persona-voiced classification descriptions, build-owner-as-gate pattern, the two-tab architecture page (Overview / Subagent Detail), engagement-type-aware continuity pills, and the upstream-composition pattern (architecture.json as a denormalised join over capabilities + actions + transcript insights + persona). Multi-mode framing (Greenfield / Redesign / Channel customisation / Script comparison) and the baseline-`.agent`-as-authoritative-shape pattern.
- **Australia Post engagement (AusPost Receiver Agent voice migration)** — inline `voice_variant` block per subagent + action, `voice_open_questions[]` for unresolved investigations, severity pill rendering. Multi-channel `variants:` map shape carried forward from this engagement's hand-shaped YAML.
- **SCCU engagement (Nova Build V2 voice sandbox)** — decision-points-as-cards, `change_scope` (script / flow / ivr) categorisation, `requirement_ref` grounding into persona §N / R-ID / CD scenario turn, `pending:` flag for sources still in flux, the Agent Script Comparison tab pattern, and the gated proposed-`.agent` output with `# AXS PROPOSED CHANGE:` markers.

Originally promoted from Phases 3–4 of `capability-prioritisation` to its own skill so it can run standalone (FDE / architect with an existing capability list, no engagement context) and so the architecture page can be a richer artefact: an Overview + Subagent Detail page modelled on the Scape engagement, plus an optional Integration tab (hidden by default; surfaces when integrations are captured). Extended in v1.1 with Channel-customisation and Script-comparison modes derived from the AusPost and SCCU engagements respectively — patterns that both engagements built bespoke are now first-class in the shared skill. The Integration tab remains a pragmatic bridge until the future Technical Spec skill ships and takes that content over — it gives FDEs a home for build-detail today rather than asking them to keep it in private notes.

The included pattern library, routing contracts, instruction overrides, and dialect guidance remain available. The optional upstream deviation register is excluded from this local distribution.
