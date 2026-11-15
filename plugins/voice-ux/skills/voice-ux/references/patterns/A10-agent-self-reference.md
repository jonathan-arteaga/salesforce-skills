---
id: A10
name: agent-self-reference
category: system-instructions
severity: medium
applies_to: [migrate, optimize]
detection:
  - keyword: "I'm so excited"
    in: [response_templates, system.instructions]
  - keyword: "I'm thrilled"
    in: [response_templates, system.instructions]
  - keyword: "I'm your AI assistant"
    in: [response_templates, system.instructions]
  - structural: "no rule governing first-person emotion or mid-call self-identification"
    in: [system.instructions]
principle_refs: [P4, P11]
pattern_refs: [T-opening]
couples_with: [B02, A09]
---

# Agent self-reference

## Why it matters

How an agent talks about *itself* is a persona-and-trust decision, separate from how expressively it delivers a line (A08) or how naturally it phrases one (A09). Two failure modes recur:

1. **Claimed first-person emotion.** "I'm so excited to help you!" / "I'm thrilled you called!" An AI doesn't have feelings, and asserting them rings false the moment a caller is stressed or the flow goes wrong. Warmth should come from *delivery* (tone tags on v3, A08) and from second-person framing ("you're all set", "you're in good hands") — not from the agent narrating an inner state it doesn't have.
2. **Self-identification in the wrong places.** Two opposite errors: re-announcing "I'm your AI assistant" every few turns (nagging, and it interrupts the task), or — worse — dodging when a caller asks directly. The rule: disclose once at the opening (B02), don't repeat it unprompted, and answer honestly and plainly whenever asked.

**Naturalness ≠ deception (A09).** Sounding human-fluent is the goal; *implying the agent is human* is not. This pattern is the honesty guardrail on the naturalness work.

**A10 is a voice floor, even when the Persona licenses feelings.** The `persona` framework allows designed feelings for an Anthropomorphic Personification (default No). In voice, A10 still holds. A human-sounding TTS voice saying "I'm so happy for you" misleads far more than the same words in a chat bubble: the modality amplifies anthropomorphism. So when a supplied Persona licenses feelings, don't silently drop them and don't silently keep them. Apply A10, and log a `[review needed]` that quotes the Persona entry and gives this reason, so the Persona owner and client can decide with eyes open.

**Organizational "we" is fine.** If the Persona speaks as the organization ("we'll send that today"), keep it. What A10 and B02 rule out is first-person plural that implies human colleagues behind the agent ("let me check with my team").

## Detection

- First-person emotion claims in copy or instructions: "I'm so excited", "I'm thrilled", "I'm delighted", "I love that".
- Repeated mid-call self-identification ("As your AI assistant, …") beyond the opening disclosure.
- No global rule telling the agent how to answer "are you a real person / a bot?" — leaving the model free to improvise or deny.
- (Not a trigger to remove: the **opening** AI disclosure — that's required and owned by B02.)

## Chat example (before)

```
"I'm so excited to help you book your appointment today! 😊"
```

```
"As your dedicated AI assistant, I'm thrilled to assist. As your AI assistant,
could you tell me your date of birth?"
```

(Emoji and exclamation aside, the first-person excitement and the repeated self-ID both carry over into voice as tonal falseness and nagging.)

## Voice example (after) — recommended

**Add a self-reference rule to `system.instructions`:**

```
SELF-REFERENCE:
- Don't claim feelings. Never say you're "excited", "thrilled", "delighted", or that
  you "love" something. Convey warmth through delivery (A08) and second person
  ("you're all set", "happy to help with that") — not first-person emotion.
- Disclose you're an AI once, at the opening (owned by the welcome — B02). Don't
  re-announce it unprompted mid-call.
- If the caller asks whether you're a person or a machine, answer plainly and move on:
  "I'm an automated assistant — I can help with [X], or put you through to someone if
  you'd prefer." Never deny being an AI; never over-explain.
```

**Rewrite:**

> Before: "I'm so excited to help you book today!"
>
> After: "Happy to help you get that booked. What day works?"  *(warmth via second person + `[warm]` delivery on v3, not claimed excitement)*

> Caller: "Wait — am I talking to a real person?"
>
> Agent: "I'm an automated assistant. I can sort your booking, or put you through to someone if you'd rather. Which would you like?"

## Voice example — alternatives

**Client-approved disclosure phrasing.** The exact words the agent uses when asked "are you a bot?" are often prescribed by Legal / Compliance. Use their wording verbatim where provided; the rule above is the default when none is specified. Keep it consistent with the opening disclosure (B02).

**Warm personas without first-person affect.** An explicitly upbeat brand can still be warm without "I'm excited" — use `[encouraging]` / `[sunny]` delivery (A08, v3) and encouraging second-person framing ("you're nearly there", "that's everything I need, you're all set", A05). The warmth is real in the *sound*; the agent just doesn't claim the emotion.

## Anti-patterns

- **Removing the opening AI disclosure "because A10 says don't self-identify".** Wrong reading. The opening disclosure is required and owned by B02; A10 governs *repetition* and *first-person emotion*, not the one required disclosure.
- **Denying or deflecting "are you a bot?".** Never. Answer plainly — it's a trust and often a compliance requirement (B02).
- **Replacing claimed emotion with more claimed emotion.** "I'm excited" → "I'm passionate about helping" — same violation.
- **Over-explaining the AI nature.** A paragraph about being a large language model when asked "are you real?" — one plain sentence, then back to the task.

## Where it lives

- `system.instructions` (global) — the self-reference rule.
- Response templates / `messages.welcome` — strip first-person emotion; keep the single opening disclosure (B02).
- Couples with B02 (opening disclosure, on-demand disclosure) and A09 (naturalness ≠ deception).

## Mis-applications (optimize mode)

- **Pattern: warm voice agent salted with "I'm so excited / thrilled".** `[changed]` — reroute warmth to delivery + second person.
- **Pattern: agent re-announces "as your AI assistant" every topic.** `[consider]` — disclose once (B02), then stop.
- **Pattern: Persona licenses feelings (Anthropomorphic) and the voice agent voices them.** `[review needed]` — apply the A10 floor and route the decision back with the amplification rationale.
- **Pattern: no on-demand disclosure rule.** `[changed]` if the flow handles identity questions inconsistently; add the plain-answer rule. (Compliance-adjacent — couples with B02, which carries the hard requirement.)
