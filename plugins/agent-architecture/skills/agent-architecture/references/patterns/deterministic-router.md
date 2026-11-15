# Pattern: deterministic-router

## Intent

Make the entry point of an Agentforce agent a **deterministic routing surface**, not a reasoning surface. Every request begins at the `start_agent` block; if it reasons about state, latency and routing variance both climb. The pattern makes it a dispatcher with a fixed decision table instead.

## How it maps to Agent Script

The contract below is a **design abstraction** for review. `stage_variables`, `escape_hatches`, and `ordered_transitions` are not Agent Script fields. They name the decisions the design has to make about the entry point, and `agentforce-generate` maps them to Agent Script:

- `stage_variables` → variables declared in the agent's top-level `variables` block (or linked variables for session context), read by `start_agent`
- `escape_hatches` and `ordered_transitions` → conditional `transition to` lines placed first in the `start_agent` reasoning instructions, transition actions offered to the router, and `available when` filters on those actions

`start_agent` is the entry block where classification, filtering, and routing happen ([Agent Script Reference](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-reference.html), [Subagent Transitions](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-patterns-transitions.html), [Enforce Required Workflows](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-patterns-required-flow.html)). The exact syntax belongs to those references and `agentforce-generate`, not to this pattern.

## Contract shape

```yaml
deterministic_router:                       # design contract, mapped by agentforce-generate
  stage_variables:
    - { name, type, source, default? }    # auth_state, channel, locale, resumed_session, ...
  escape_hatches:
    - { condition, action, log_key }      # ordered — first match wins
  ordered_transitions:
    - { when, to_subagent, pre_handoff_fields? }  # ordered — first match wins
```

## When to use

- Any agent with **three or more subagents** where routing is non-trivial.
- Any agent where routing drift between runs has been observed in testing (deterministic entry eliminates the variance source).
- Voice agents specifically — audible routing pauses while the master agent reasons are a real UX regression.

## When NOT to use

- Single-subagent agents. The pattern adds structure that doesn't buy anything.
- Agents where routing is genuinely intent-shaped and the entry block has to classify free-form user utterances. The deterministic surface sits *underneath* intent classification; it doesn't replace it.

## Cross-skill resolution

- `agentforce-generate` maps the contract to Agent Script: `stage_variables` → declared variables read by `start_agent`; `escape_hatches` and `ordered_transitions` → conditional transitions, transition actions, and `available when` filters in `start_agent`. Validation happens there.
- `conversation-design` uses the `ordered_transitions.when` conditions as scenario entry points so happy paths and edge paths are both grounded in the same routing table.
- `agentforce-test` can assert the routing table deterministically (one assertion per `ordered_transitions` row).

## Evidence threshold

Observed in two engagements: Nova (SCCU) and the Scape router scaffold. Promoted on that basis.
