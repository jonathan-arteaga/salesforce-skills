# Subagents, Actions, Overrides & Hooks

Current Agentforce documentation calls topics **subagents** (preserving API identifiers for backward compatibility). Keep topology minimal: place focused reasoning and actions directly in `start_agent` until a distinct objective, tool set, instruction boundary, authority level, or escalation path justifies adding a subagent.

## Subagent Transitions & Reachable Outcomes

- **One primary outcome per branch:** Each reachable branch should choose one clear next step: answer, ask, invoke an action, transition, refuse, or escalate.
- **Prevent transition loops:** Guard transitions with deterministic state or eligibility flags from trusted action outputs—never customer assertions or unverified model-set booleans.
- **Discarded prompt caveat:** Do not assume discarded reasoning text or transient model state survives a subagent transition; pass required context through typed variables or explicit action outputs.
- **Consume Persona handoffs faithfully:** When `persona-handoff.json` from `agentforce-design` is supplied, place shared character guidance in global `system.instructions` and task-specific guidance in `reasoning.instructions`; keep welcome/error copy aligned without mutating semantic persona decisions.

## System Overrides (`system.instructions`)

- **Replacement, not append:** A subagent-level `system` block **replaces** global `system.instructions` instead of merging with it.
- **Mandatory override checklist:** Whenever authoring a subagent `system` block, explicitly verify that required persona constraints, Never-Say entries, grounding rules, PII/voice masking rules, and compliance constraints are preserved (and that hard controls live independently in deterministic logic or backing Apex/Flow).

## `before_reasoning` & `after_reasoning` Lifecycle Blocks

- **Repeatable per-turn hooks:** `before_reasoning` and `after_reasoning` execute around each reasoning turn, not once per session.
- **Critical skip behavior:** `after_reasoning` is **skipped** if the subagent transitions away mid-execution. Never use `after_reasoning` as a guaranteed cleanup, audit-log, or one-time commit hook—keep mandatory side effects and checks on the actual action path.
- **Classifier restriction:** Reasoning lifecycle hooks are unsupported with `EinsteinHyperClassifier`. Always verify hook timing with target-org preview traces.

## Action Implementations, MCP & Execution Security

- **Valid action targets only:** Actions must bind to supported targets: `@InvocableMethod` Apex, Autolaunched Flows, active Prompt Templates, Standard Actions, Data Libraries/Retrievers, or allowlisted MCP tools. Never wire arbitrary non-invocable Apex classes.
- **Stub-first policy:** Default new actions to `NEEDS STUB` during spec/scaffolding. Ask the user before scanning org/repo for existing implementations or generating Apex/Flow/Prompt stubs via `scripts/scaffold.py`.
- **Backing authorization & idempotency:** Employee Agents run as the logged-in user; Service Agents run as an Agent User or verified site user. Enforce record scoping (`with sharing`, verified customer identity) inside backing Apex/Flow—prompts and `available when` filters are UI/routing controls, not security boundaries. Re-check eligibility before writes and make external mutations idempotent.
- **MCP server hygiene:** Keep secrets off CLI command lines, review individual MCP tools before allowlisting, and require confirmation for consequential MCP changes.
