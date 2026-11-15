# Pattern: business-topic-slot

## Intent

An **engagement-specific typed slot** that captures a business entity (an order, a tracking number, a policy, a case) with:
- A typed contract (not free-text)
- Deterministic record selection (one record → unambiguous)
- A verbatim read-back step before the agent acts on the record

The pattern replaces "LLM-guesses-which-record" with "slot captures identifier → facade returns record → agent reads record identity back → user confirms before any action." It is the primary defence against the agent operating on the wrong record (updating the wrong order, discussing the wrong policy) — a class of failure that erodes customer trust faster than any other.

## Contract shape

```yaml
business_topic_slot:
  slot_name: <stable-slug>              # e.g. "order_id", "policy_number"
  typed_contract:
    type: string | int | regex
    format: <regex-or-schema>           # e.g. "^[A-Z]{2}\d{9}$"
    normalisation:                      # transformations before match
      - lowercase | uppercase | strip_whitespace | remove_hyphens | ...
  deterministic_record_selection:
    source: <action-or-flow-name>       # the lookup that returns 0..n records
    disambiguation: single_match_only | ask_to_disambiguate
    on_zero_matches: <action>           # typically: tell user, re-prompt once, handoff
    on_multiple_matches: <action>       # typically: list top N with distinguishing fields
  verbatim_readback:
    template: <string-with-field-refs>  # e.g. "I've got order {order_id} for {customer_name}, placed {date}. Is that the one?"
    required: true | false              # true for high-stakes topics; false for low-risk lookups
  error_contract:
    on_invalid_format: <message-id>
    on_lookup_failure: <message-id>
    on_user_rejects_readback: <action>
```

## Why the readback matters

The readback is the final checkpoint before any state-changing action. In two engagements we observed the agent happily looking up and discussing the wrong order because the typed slot captured a plausible-but-wrong identifier and no readback caught it. The readback converts "the slot captured something that passed regex" into "the user confirmed the record is theirs." It also surfaces off-by-one record errors to the user before the agent commits to them.

The readback can be skipped (`required: false`) for genuinely low-risk lookups — "what are your store hours" doesn't need a readback. It must be present for any topic where getting the wrong record costs the customer time or trust.

## When to use

- Any topic where the agent needs to name a specific record (order status, policy details, claim progress, balance).
- Any topic where the agent takes a state-changing action against a record (update, cancel, refund).
- Any topic where multiple similar records could legitimately exist for the same user (multi-account, household policies, repeat orders).

## When NOT to use

- Catalogue / public-information lookups where there's no user-specific record.
- Topics where the identifier is already resolved upstream (deep-link, authenticated session with a selected record in context).

## Cross-skill resolution

- `agentforce-generate` renders the slot as a typed input on the relevant topic + wires the readback into the topic's reasoning block.
- `voice-ux` reads the typed contract for ASR-safe capture — alphanumeric spelling, digit-grouping, repair-tier ladders — and shapes the readback for spoken prose.
- `conversation-design` renders the readback turn explicitly and shows the branching for "yes, that's it" / "no, different one" / "user says a different number altogether."
- `agentforce-test` asserts the slot + readback as a deterministic path per record-selection scenario.

## Evidence threshold

Observed in two engagements: AusPost (`tracking_number` slot with phone + full-number ladder, verbatim read-back) and SCCU (`account_id` slot with multi-account disambiguation and R-numbered readback invariant). Promoted on that basis.
