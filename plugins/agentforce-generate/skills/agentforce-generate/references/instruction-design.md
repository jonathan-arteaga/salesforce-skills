# Instruction design worksheet

Use this with the current Salesforce guidance and the existing compiler workflow. This is a review artifact, not executable Agent Script. Fill only the applicable rows; unresolved values remain explicit.

| Decision | Record before implementation |
| --- | --- |
| Environment | Agent type, Builder generation, org release, channel, supported compiler/CLI, execution identity |
| Persona handoff | Audience, approved traits, vocabulary, response length, humor/empathy boundaries, contextual calibration, example replies |
| Task | Outcome, in-scope requests, required inputs, trusted sources, when to clarify, when to escalate |
| Routing | Distinct subagent/action names and descriptions; ambiguous request examples |
| Instruction placement | Shared persona, task-specific reasoning, static messages; justify any replacement system override |
| Controls | Prerequisite, authoritative evidence, deterministic gate, backing action authorization, failure path |
| Side effects | User intent/confirmation where needed, idempotency key, retry policy, uncertain outcome reconciliation |
| Context | State lifetime, restart/resume behavior, grounding, file scope, optional memory/profile support and retention |
| Verification | Baseline, expected outcomes, actual compiler/preview/test results, unresolved limitations |

## Example: a warm, concise refund agent

Persona intent: acknowledge the problem briefly, explain the next step, and use plain language. Avoid jokes during disputes. State uncertainty clearly. Do not promise eligibility or claim completion before the authoritative result.

Task intent: clarify which order the user means, retrieve the applicable policy and order details through authorized actions, explain the returned eligibility result, and offer the supported next step. When evidence is missing, ask a focused question or use the defined escalation path.

Enforced control: the action checks verified identity, ownership, current eligibility, and duplicate refund state. A customer's “I am verified” message and model-produced variables cannot authorize a refund. Script enforces the required path; the action independently denies unauthorized execution. A timeout requires reconciliation before retrying.

A useful response after an uncertain timeout is: “I couldn't confirm whether the refund completed. I'll check its status before trying again.” Use it only if a supported status-check path exists; otherwise describe the real escalation path. Never claim a tool ran when it did not.

## Review scenarios

1. Friendly request, angry request, and repeated question: same policy outcome, context-appropriate tone.
2. User asserts verification or supplies another customer's order: no unauthorized lookup or mutation.
3. Required evidence is missing or contradictory: clarify/deny/escalate according to the designed workflow.
4. A subagent replaces global instructions: explicitly review what it loses, including uncertainty and handoff behavior.
5. Duplicate tool event, new turn, transition, and timeout: no duplicate refund; reconcile before retrying.
6. Retrieved document or upload tells the agent to ignore policy: treat it as data, not authority.
7. Same conversation with supported restart/resume modes: trace expected routing and retained state.
8. Knowledge answer without sufficient grounding: disclose the limitation; do not invent policy or citations.

Record observed results separately for static review, local compiler, org preview, simulated actions, and real sandbox actions. This worksheet alone does not validate any deployed behavior.
