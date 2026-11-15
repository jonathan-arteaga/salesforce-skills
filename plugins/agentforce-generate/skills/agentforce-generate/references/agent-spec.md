# The Agent Spec

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## The Agent Spec

**Agent Spec** is the central artifact this skill produces and consumes. A structured design document representing agent purpose, user outcomes, subagent graph, actions and implementations, variables, subagent posture, deterministic controls (when needed), and behavioral intent.

Agent Specs evolve with the agent. Sparse during agent creation (purpose, use cases, planned placeholders). Fleshed out during agent build (flowchart, action implementations mapped, posture choices documented, deterministic controls added only where justified). Reverse-engineered when comprehending existing agents. Critical for advanced troubleshooting, providing reference to compare expected vs. actual behavior. During testing, test coverage maps against it.

Produce or update an Agent Spec for greenfield work, material design changes,
or analysis whose result changes the documented contract. For a narrow,
already-specified repair, record the affected use case and evidence without
forcing a full spec rewrite.

Read [Design & Agent Spec](agent-design-and-spec-creation.md) for Agent Spec structure and production methodology.
