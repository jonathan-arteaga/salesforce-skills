# Pattern: verification-facade

## Intent

A **server-side verdict facade** that the agent calls to verify a user without ever seeing the underlying data. The facade accepts whatever the user has provided (a tracking number + a phone number, a date of birth + a postcode) and returns a bounded verdict enum. The agent reasons on the enum; the raw data stays in the system of record.

The facade keeps PII and regulated data off the LLM input tape. The agent reads *verified*, not *the DOB string*; the agent reads *mismatch*, not *the retrieved record*. Audit trails, data-residency controls, and PII-leak surfaces are all narrower as a result.

## Contract shape

```yaml
verification_facade:
  verdict_enum: [verified, mismatch, not_found, backoff_required, blocked]
  invariants:
    - R2-style:
        name: <stable-id>
        statement: <one-sentence invariant>
        action_on_violation: <what the facade does — refuse, log, backoff, handoff>
  facade_action:
    name: <flow-or-apex-action-name>
    inputs: [...]                         # fields the agent passes in (hashed / tokenised where applicable)
    output: { verdict: <enum>, reason_key?: <string> }
```

## Why `verdict_enum`, not boolean

A boolean collapses *not_found* / *mismatch* / *rate-limited* into one bucket. The agent then can't distinguish between "ask again" (mismatch — one attempt remains) and "fail-safe handoff" (rate-limited — stop asking). An enum of 3–5 verdicts keeps the downstream reasoning distinct and auditable.

## Invariants (R2-style)

Each invariant is a one-sentence statement with a stable name and an explicit action-on-violation. Example:

> **R2.3** — The facade MUST NOT return a verdict for an input that fails format validation. On violation: return `mismatch`, log `invalid_input_format`, and do not increment the attempt counter.

Invariants travel with the facade — they're part of the contract, not implementation detail. The agent-side reasoning assumes them.

## When to use

- Any verification that touches regulated data (financial, health, government ID).
- Any flow where the LLM input tape must not include raw PII (compliance / data-residency requirement).
- Any agent where a single bad verdict → wrong outcome is costly (billing adjustments, policy changes, account unlocks).

## When NOT to use

- Public-information lookups (store hours, product catalogue). The facade overhead buys nothing.
- Agents where the data the facade would hide is already in the prompt from upstream context — the facade can't un-leak it.

## Cross-skill resolution

- `agentforce-generate` wires the facade action into the verification topic — the topic references the action by name and reads the verdict enum.
- `conversation-design` branches scenarios per verdict (`verified` → next subagent; `mismatch` → repeat ladder; `blocked` → handoff).
- `agentforce-test` asserts each verdict path independently.

## Evidence threshold

Observed in two engagements: SCCU (verifyCustomerFacade with 4 verdicts) and the LNE pattern-of-record pilot (verifyPolicyholder with 3 verdicts + R-numbered invariants). Promoted on that basis.
