# Pattern: escalation-reason-key

## Intent

Terminal handoffs — the agent giving up and routing to a human — need a **stable key per reason**, not free-text. The key links three artefacts: the persona line the agent speaks on handoff, the Conversation Design turn that renders the handoff in review, and the transfer target (queue, Flow, telephony skill group) that catches the handoff downstream.

Without a reason-key contract, telemetry reports "handoff" with no structure, personas drift into inconsistent handoff copy per subagent, and ops teams can't route handoffs to the right queue because the reason isn't preserved.

## Contract shape

```yaml
escalation_reason_keys:
  - key: <stable-slug>                   # e.g. "verification_cap_reached"
    transfer_target: <string>            # queue id, flow id, telephony skill group
    log_fields:
      - { name, source }                 # fields logged alongside the reason key
    linked_persona_line: <persona-ref>   # e.g. "persona §12 line 4"
    linked_cd_turn: <cd-scenario-ref>    # e.g. "verification-fail-path Turn 7"
```

## Why stable keys matter

A stable key means the same reason reports the same way across subagents, across releases, and across channels (chat / voice). Grep-ability for ops; stable aggregation for analytics; one place to tune the persona line without hunting through topics.

Free-text reasons regress on all three: "could not verify" and "verification failed" and "unable to confirm identity" are the same reason reported three ways, which is one reason reported zero ways to anyone counting.

## When to use

- Every production agent that can hand off to a human (which is nearly all of them).
- Any agent where ops / contact-centre is a stakeholder in the review — they need to see the reason keys to confirm routing.
- Any agent where compliance requires an auditable handoff reason (regulated domains).

## When NOT to use

- Prototype / sandbox agents with no live handoff plumbing.
- Agents whose only handoff is "general escalation to any human" — a single key is fine; the full contract overhead isn't needed.

## Enumerating reasons

Reasons are drawn from four sources:
1. **Verification ladder failure** — one key per factor-exhausted condition (e.g. `verification_cap_reached`).
2. **Out-of-scope requests** — one key per out-of-scope cluster (e.g. `oos_billing_dispute`), not one per utterance.
3. **Compliance refusals** — one key per refusal category (e.g. `refuse_medical_advice`, `refuse_legal_opinion`).
4. **Hard escalation triggers** — explicit keywords or signals (e.g. `agent_requested_by_user`, `distress_signal_detected`).

Don't let the reason list grow unbounded. Fewer, broader keys with structured `log_fields` for context is better than one key per unique utterance.

## Cross-skill resolution

- `agentforce-generate` wires each key into the escalation action's output. The action returns `{ reason_key, log_fields }`; downstream Flow routes by `reason_key`.
- `persona` owns the `linked_persona_line` for each key — the exact words the agent speaks on handoff.
- `conversation-design` owns the `linked_cd_turn` — the scenario turn that renders the handoff in review.
- `agentforce-observe` reads the keys from telemetry and aggregates by key.

## Evidence threshold

Observed in two engagements: SCCU (6 reason keys for Nova Build V2 with telephony skill-group targets) and AusPost (4 reason keys for voice handoff with queue-id targets). Promoted on that basis.
