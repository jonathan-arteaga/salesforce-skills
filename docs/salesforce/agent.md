# Agent guidance

- Identify the agent type, builder generation, channel, release, and actual execution user. Employee agents use the logged-in user; Service agents can use an agent user or a verified site user depending on channel/setup. A contact ID in context does not itself enforce record access.
- For Service agents running as the agent user, scope sensitive actions to a verified customer identity in backing Apex/Flow. Test cross-customer denial; prompts and action visibility filters do not replace authorization in the action.
- Use deterministic Agent Script logic for mandatory prerequisites and transitions; reserve natural-language instructions for reasoning. Validate syntax with the target compiler. Prevent transition loops and do not assume discarded prompts survive a transition.
- Einstein Trust Layer LLM masking is disabled for agents, including prompt templates invoked through agent actions. Provider zero retention is not proof of no stored Salesforce traces. Verify minimization, access controls, storage, and any separately configured masking.
- Testing Center can change CRM data and consumes requests/credits. Use a sandbox with synthetic fixtures; record agent version, test suite, execution mode, and actual results. A simulated action pass does not validate live permissions, DML, integration, or handoff.

## Persona, instructions, and current authoring

- Prefer the new Builder / Agent Script for new agents when the target supports it; Canvas, Script view, and DX are authoring paths for the same language. Assess existing agents before migration. Current docs call topics **subagents**; preserve API identifiers and compatibility with older terminology.
- Separate three deliverables: persona (voice and contextual calibration), task instructions (goal, inputs, grounded answers, clarification and recovery), and enforced controls (authorization, prerequisites, sequencing, side effects). Persona owns the semantic specification; agentforce-generate encodes it; agent-architecture owns control decisions. Do not turn a persona worksheet into a second script generator.
- Begin with a few concrete, positive behavioral directions and contrasting sample replies. Specify audience, channel, vocabulary, brevity, empathy, humor boundaries, uncertainty, and handoff behavior. Test frustrated users, unavailable information, and failures. A confident voice must not imply verified facts or completed actions.
- Use short, distinct task instructions and unambiguous subagent/action descriptions. Avoid overlapping routing descriptions and inconsistent terms. Add instructions in response to observed failures, then rerun regressions. Writing “first”, “always”, or “STOP” in a prompt does not enforce execution order.
- Implementation owner: place shared persona guidance in global `system.instructions` and contextual task guidance in `reasoning.instructions`; align welcome/error messages too. A subagent `system` block **replaces**, rather than appends to, global instructions. Review every replacement for lost behavioral requirements and conflicts; preserve required controls independently of prompts.
- Use trusted action results for verification and eligibility gates, not a customer assertion or a model-set flag. Enforce authorization in backing Apex/Flow/API even when script controls visibility and order. Recheck before consequential execution; use idempotency and reconcile uncertain outcomes before retrying.
- Treat lifecycle logic as repeatable. The reference describes `after_reasoning` on each request after the reasoning loop, but it is skipped when the subagent transitions away mid-execution. It is not guaranteed cleanup or a one-time commit hook. Keep required checks on the actual action path. Verify hook timing with target traces; hooks are unsupported with EinsteinHyperClassifier.

## Documented capabilities: evaluate, do not enable indiscriminately

- Check the current Blocks reference for `config.runtime`, `config.file_upload`, and `context` before using them. Record target release, agent type, channel, license, compiler/CLI version, documentation URL/date, availability evidence, and preview results. A documented field or announcement is not proof of availability in this org.
- Make multi-turn restart/resume behavior explicit. The Blocks reference documents `runtime.reset_to_initial_node`; high-level Flow of Control prose differs. Do not assume every turn restarts at `start_agent`. Compile and preview a two-turn trace against the target version before relying on routing state.
- Review memory and user-profile context only where supported and needed. Specify consent, retention/deletion behavior, data minimization, and cross-user isolation. Memory is not identity verification or authorization. Turning memory off does not itself delete existing memories.
- Decide uploaded-file handling deliberately; untrusted attachments may contain prompt injection or other customers' data. Restrict which subagent receives files. Keep citations and groundedness appropriate to knowledge answers; do not disable them merely to improve latency or enable internal thought streaming without reviewing the channel and audience.
- Use the current reference and target scaffold for configuration fields: `default_agent_user` belongs under `access`; reference examples can disagree on older `agent_name` versus current `developer_name`. Never bulk-rewrite working bundles from an overview sample. Record disagreements and the compiler/preview result.
- Before release, test persona consistency, override inheritance/replacement, ambiguous routing, denied access, duplicate calls, action failure, multi-turn continuation, grounding, and escalation. Separate offline checks from org compilation, preview, and live action evidence. No org evidence means those checks remain unverified.

## Sources checked 2026-11-15

- [Agent Execution Context and Data Access by Type](https://help.salesforce.com/s/articleView?id=ai.agent_execution_data.htm&release=264.0.0&type=5)
- [Data Masking Limitations in Agentforce](https://help.salesforce.com/s/articleView?id=ai.agent_trust_data_masking.htm&release=264.0.0&type=5)
- [Agent Script Pattern: Subagent Transitions](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-patterns-transitions.html)
- [Agentforce Testing Center](https://help.salesforce.com/s/articleView?id=ai.agent_testing_center.htm&release=264.0.0&type=5)

- [agent-script](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html)
- [ascript-ref-instructions](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-instructions.html)
- [ascript-patterns](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-patterns.html)
- [ascript-patterns-system-overrides](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-patterns-system-overrides.html)
- [ascript-ref-before-after-reasoning](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-before-after-reasoning.html)
- [ascript-blocks](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html)
- [ascript-flow](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-flow.html)
- [Salesforce persona design guide](https://www.salesforce.com/agentforce/personas/)
