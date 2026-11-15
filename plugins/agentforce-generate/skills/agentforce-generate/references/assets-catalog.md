# Assets

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Assets

The `assets/` directory contains templates and examples. Read when you need a starting point or a concrete reference for artifacts and source files.

- **`assets/agent-spec-template.md`** — Agent Spec template with all sections and placeholder content. Copy to `<AgentName>-AgentSpec.md` in project directory, then fill in during design. Save Agent Spec as file — significant design artifact that benefits from proper rendering, especially Mermaid Subagent Map diagram.

- **`assets/agents/local-info-agent-annotated.agent`** — Complete annotated example based on Local Info Agent, showing all major Agent Script constructs in context with inline comments explaining why each construct is used. Read when you need concrete reference for how concepts compose into working agent, or as fallback when focused examples in reference files aren't sufficient.

- **`assets/agents/template-single-subagent.agent`** — Compatibility-named focused starter with one `start_agent` execution block and no router or subagent blocks.

- **`assets/agents/template-multi-subagent.agent`** — Minimal agent with multiple subagents and transitions. Copy and modify for complex agents.

- **`assets/agents/router-first.agent`** — Transition-only router example with
  HyperClassifier and concise router instructions.

- **`assets/agents/verification-gate.agent`** — Identity/authorization gate
  with protected action availability.

- **`assets/agents/simple-qa.agent`**, **`production-faq.agent`**, and
  **`order-service.agent`** — Complete examples at increasing behavioral and
  action complexity.

- **`assets/patterns/README.md`** — Route to focused complete patterns for
  callbacks, input binding, lifecycle, delegation, and multi-step workflows.
  Use a pattern only when its stated use-case preconditions apply.

- **`assets/invocable-apex-template.cls`** — Reference for invocable Apex
  classes. Copy and modify when complex Apex action implementations are desired.
