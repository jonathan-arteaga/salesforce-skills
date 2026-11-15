---
version: "2.1.0"
date: 2026-10-12
---

# Workshop Question Policy

Question-selection techniques for persona stakeholder input. For independently answerable questions, use the WORKSHEET path and `references/stakeholder-question-policy.md`. In a WORKSHOP, these techniques inform prompts inside facilitated collaboration activities. Neither path requires a persona draft. Questions should be open-ended, scoped to what's actually unresolved, and respectful of stakeholder time.

## Guiding principle

**Quality over coverage. Better to ask 4 great questions than 12 generic ones.**

There is an infinite possible question set the framework could generate. Most of those questions are noise for any specific persona. The job here is identifying *what's actually unresolved or high-leverage* for *this* persona, given everything the skill already knows.

## Skip what you already know

Avoid questions the supplied input already answers explicitly. An “open” question is relevant to the requested stakeholder and not settled by that input; no decision log, draft persona, or hub project is required. A supplied draft can help target validation, but need not be formally approved. When no draft or brand input exists, leave choices open rather than pretending a default was approved. Stakeholder attention is the scarce resource.

**Examples of what to skip:**

- The brand input clearly says "always formal" → don't ask about Formality.
- A source explicitly says humor is off limits → don't ask "How much humor?" Do not treat an industry stereotype as a settled persona decision.
- Channel is locked to telephony → don't ask "Should the agent use emoji?" (no formatting in audio).
- Personification is locked to Not personal → don't ask stakeholders to choose a separate agent name.
- Identity is filled with strong-signal traits → don't ask the stakeholders to re-validate every adjective; pick one or two with productive tension.

This is harder than it sounds. The framework has 14 dimensions × 5+ persona artifacts × business context. Most could generate plausible questions. The skill must actively prune.

## What to ask about

In priority order:

1. **High up the dimensions ladder** — Identity, Personification, Register. These have the most leverage; getting them wrong cascades.
2. **Where confidence is low** — when a draft dimension was filled with a default rather than a strong signal, that's a candidate question.
3. **Where productive tension exists** — Tension Pairs in the framework (Cool Warmth + Bold Personality, Blunt Coloring + Playful Humor, etc.) are inherently questions stakeholders should weigh in on.
4. **Where the brand input is silent or contradictory** — e.g., the brand guide says "approachable" but doesn't say how much humor; that's worth asking.
5. **Where channel forces a tradeoff** — voice agents handling frustrated callers; humor in escalation flows.
6. **Where the use case raises a tone-flex question** — the framework's tone-flex triggers (system errors, content sensitivity, escalation) are stakeholder-relevant moments.
7. **Where the audience spans novice and expert users and the Reading Level Flex policy is unresolved.** Ask: "How diverse is the user population in its understanding of jargon?" Capture the Reading Level baseline plus Flex policy and range.
8. **Where technical evidence and outcome framing need a deliberate bridge policy.** Ask: "When answering a technical question, should the agent tie it back to outcomes, or stick to the technical details?" Capture Technical Explanation Policy bridge strength.

## What never to ask about

- Things the input or context already answers definitively.
- Things already settled for this experience. Formality may suggest a Chatting Style pairing, but does not prohibit a deliberate alternative; distinguish Formality from Register.
- Internal mechanics the stakeholders shouldn't be making decisions about (e.g., dimension constraint notes, tension-pair resolution rules).
- Anything that produces a "neutral default" answer — those questions waste stakeholder attention without changing the persona.

## Question styles

Three styles, picked per question based on what's needed:

### 1. Validate

Use when the skill has a strong-signal draft and wants stakeholder confirmation.

> "We assumed [X] from your brand guide. Confirm or push back."
> "The agent will speak in Coach register — instructive, takes a position. That fits the 'sales coach' framing in the brief. Right call?"

### 2. Choose between

Use when there are two genuinely different positions on a spectrum, with consequences spelled out.

> "When a customer expresses frustration, would you rather the agent (A) acknowledge the frustration before solving, or (B) skip to the solve? A reads as more empathetic; B reads as more efficient. Pick one."

The two options must be **meaningfully different**. Don't write false binaries where both options are the same with cosmetic differences. If you can't articulate the consequence of each choice, drop the question.

For technical comparisons, hold facts, recommendation, tone, and length as constant as possible. Vary **Reading Level or Technical Explanation Policy bridge strength — never both in the same pair.**

### 3. Open spectrum

Use when it's a blank slate — no signal in the input, and the stakeholders genuinely need to make the call.

> "Place the agent on this line: [Brisk] ⟷ [Languid]"
> "How separately person-like should the agent seem? [Not personal] ⟷ [Individuated] ⟷ [Anthropomorphic]"

These are dimension-card-shaped: print long, legible scales on large paper or use a collaborative board. Let each participant place one mark per open dimension before discussion; interpret the spread and reasons rather than treating marks as automatic votes or approvals. Use positions and definitions from `references/persona-framework.md` (for example, Personification: Not personal / Individuated / Anthropomorphic; Empathy Level is emotional validation, not response length). Especially useful for high-leverage decisions (Personification, Register, Warmth) when stakeholders need to compare positions.

## Output format constraints

A workshop plan is meant to guide live collaboration using a board and facilitation mechanics, not simply collect answers asynchronously. A standalone worksheet is a set of questions for stakeholders to answer without a facilitator. Neither is a long-form persona document.

- Aim for 4-8 total questions per workshop outline. Fewer if the persona is well-grounded.
- Group workshop prompts into actual activities (individual idea generation, comparison, convergence), rather than relabeling a worksheet as a session plan.
- Link to a persona draft or sample dialog only if one exists and is useful; neither is mandatory pre-read.
- Include a brief "Background" paragraph for the facilitator (≤1 paragraph) summarizing where the persona stands and what input is needed.

## Anti-patterns to refuse

- A 20-question workshop outline. If you're hitting 20, you haven't pruned.
- A workshop outline for a Not personal experience that asks for a character name. Skip—the selected degree already rules out a separate named identity.
- A workshop outline that asks every dimension "where on the spectrum?" — that's a coverage approach, not a leverage approach.
- A workshop outline where every option in a "choose between" pair reads as neutral or compromised. The job is to surface real tradeoffs, not to write safe choices.
