# Pattern: identity-ladder

## Intent

Ordered sequence of identity factors with a per-factor cap and a per-factor backstop. The pattern replaces free-form "ask for ID" verification with a shaped ladder the master agent walks top-down. Each factor is tried once; if it fails, the agent moves to the next factor rather than retrying the same one indefinitely.

The ladder makes verification auditable: for any given session you can trace exactly which factors were attempted, in what order, how many retries each burned, and which backstop ultimately fired.

## Contract shape

```yaml
identity_ladder:
  factors:
    - name: <string>                 # e.g. "caller_phone_match"
      cap: <int>                     # max attempts for this factor (typically 1 or 2)
      backstop: <string>             # what runs if this factor fails
      log_key: <stable-slug>         # the key logged on attempt + verdict
  escape_hatches:
    - condition: <string>            # e.g. "caller requests a human"
      action: handoff | refuse
      transfer_target: <string>
```

## When to use

- Any verification subagent in a regulated or sensitive domain (financial, health, government services).
- Any voice agent where open-ended retry loops are a known UX failure (callers hang up before the third repeat).
- Any agent where the compliance team or legal has asked for a verifiable attempt trail.

## When NOT to use

- Anonymous / public-information agents. Verification isn't on the critical path.
- Agents where identity is delegated upstream (SSO, authenticated session) — the ladder is already resolved before the agent runs.

## Factor ordering guidance

Order factors by **inverse friction**: start with the lowest-friction factor the user has already given (caller phone, in-session account), end with the highest-friction (full tracking number read-back, security questions). The ladder should bias toward "most sessions complete at factor 1 or 2."

## Cross-skill resolution

- `agentforce-generate` reads `identity_ladder.factors` as an ordered sequence inside a dedicated verification topic's reasoning block.
- `conversation-design` renders one scenario turn per factor; the backstop becomes the next turn, not a retry.
- `voice-ux` reads the ladder for ASR-safe capture guidance per factor (digit-grouping, alphanumeric spelling, repair tiers).
- `agentforce-test` asserts the ladder deterministically — one driver run per factor-fails-at-cap path.

## Evidence threshold

Observed in two engagements: SCCU (customer verification subagent, 3-factor ladder) and AusPost (receiver verification, 2-factor ladder with voice-specific repair tiers). Promoted on that basis.
