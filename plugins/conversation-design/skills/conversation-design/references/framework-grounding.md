# Framework grounding — conversation design

The lineage and vocabulary the conversation-design skill works inside. Read this once before drafting; the rubric in `conversation-design-principles.md` is what the skill cites against turn-by-turn.

Conversation design is an established craft. This skill's vocabulary, scenario shape, and turn rules sit inside that tradition — they aren't invented for Agentforce. Naming the lineage so the model and the reader work from the same anchors:

- **Conversation Design Institute (CDI)** — sample-dialog-first design (write the conversation before the flow), tapering (the agent's verbosity reduces as the user demonstrates competence), the One Breath Test (a turn the agent can't speak in one breath is too long), and persona-led voice (every agent turn is voiced through the persona, not generic-friendly default).
- **Google Conversation Design Guidelines** — cooperative principle (Grice's maxims of quantity, quality, relation, manner) applied to agent turns; no dead ends (every fallback offers a next move); turn-taking discipline (one ask per turn); recognition over recall in the user's cognitive load.
- **Cathy Pearl, *Designing Voice User Interfaces*** — the canonical error typology for conversational systems: **no-input** (silence / abandonment), **no-match** (recognition or classification failure), **recognition-error** (confidence mis-grounded). The skill's error-state subtypes (`recognition_failure`, `timeout`, `validation_failure`, `repeat_failure`) map directly to this typology.
- **NN/g (Nielsen Norman Group)** — voice (persistent) vs tone (contextual) distinction inherited from the persona skill; error-message principles (acknowledge, locate, instruct); graceful degradation as a usability principle.
- **Salesforce Agentforce architecture** — topic boundaries, classification descriptions, action invocation constraints, and the master-agent / subagent routing model. These are runtime constraints the design must respect; flows that ignore them won't survive build.

## A well-formed scenario

- Has one **goal** the user is trying to accomplish (not a tour of capability)
- Has one **type** — happy / error / fallback — and earns that type with the kind of friction it models (no error scenario where nothing breaks; no fallback where the agent ultimately succeeds)
- **Tapers** — early turns calibrate; later turns shorten as the user finds rhythm
- Survives the **One Breath Test** on every agent turn
- Ends with the user knowing what just happened and what's next (no dead ends, even on fallback)

## Why three scenarios, not one or twelve

One scenario is a demo; it doesn't expose the failure surface. A full corpus is craft work that takes an AXS days. Three scenarios — one happy, one error, one fallback — cover the minimum surface a design reviewer needs to feel the agent's shape: how it succeeds, how it breaks, and what it does when it can't help. This is the same minimum CDI uses for early-stage persona pressure-testing.

## Why 4–8 turns

Below 4, a scenario is a one-shot — there's no place for tapering, error recovery, or progressive disclosure. Above 8, the scenario is either two scenarios fused or a flow that wasn't ready to be designed at this fidelity. The cap is tradition, not arbitrary.

## Constraints over the framework

These are recommendations, not hard locks — engagements with deep prior research, novel modalities, or specific compliance contexts may push past them. The skill flags exceptions in scenario `notes` rather than silently breaking the rule.
