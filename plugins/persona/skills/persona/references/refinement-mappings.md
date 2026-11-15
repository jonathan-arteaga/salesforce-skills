---
version: "1.4.1"
date: 2026-09-10
---

## PHASE 2 — REFINE

Run controlled Persona calibration and let the user iterate. This phase does not design a conversation flow or claim runtime behavior.

### Persona calibration

Use `templates/persona-calibration-template.md` as the canonical `persona-calibration.md` shape and preserve its YAML **version and date frontmatter** on every regeneration. For a newly generated artifact, set `date` to the current local date; do not copy the template revision date.

Use one supplied utterance and a fixed fact set to produce bounded Persona evidence:

- one routine response showing the baseline character;
- one Tone Flex response using an approved trigger and lexical/discourse cue;
- one reset response showing return to baseline; and
- one boundary response when a Never-Say, Tone Boundary, or immutable constraint needs demonstration.

Each item is a controlled response, not a multi-turn scenario. Do not invent actions, branches, system outcomes, or conversation progression. When the team needs happy-path, error, and fallback scenarios, hand `persona.md` and the use cases to `conversation-design`. When a built agent needs behavioral proof, hand the Persona acceptance criteria to `agentforce-test`.

For voice-bearing channels, the calibration validates word choice and response patterns only. Pass `persona.md` to `voice-ux` for prosodic realization after a working Script and representative sample exist.

### Refinement Loop

After presenting the Persona calibration:

> "Tell me what to change — 'make it warmer,' 'drop the humor,' 'don't say that' — or pick:
> - Looks good — back to the hub
> - Try a different controlled example
> - (free-text always available)"

When the user types a natural-language adjustment, apply it via these mappings, regenerate the sample with the change held single-axis, and re-present:

| User says | Dimension change | Also consider |
|---|---|---|
| "warmer" | Warmth: increase one position | Empathy: increase one |
| "cooler" / "less warm" | Warmth: decrease one | Empathy: decrease one |
| "more formal" | Formality: increase one | Register: shift toward Advisor |
| "less formal" / "more casual" | Formality: decrease one | |
| "shorter" / "more concise" | Brevity: decrease one (toward Terse) | |
| "longer" / "more detail" | Brevity: increase one (toward Expansive) | |
| "more personality" | Personality Intensity: increase one | Humor: enable if None |
| "less personality" / "more neutral" | Personality Intensity: decrease one | |
| "less robotic" | Warmth: increase + Personality Intensity: increase | |
| "more professional" | Formality: Professional, Humor: None or Dry | Personality Intensity: Moderate |
| "friendlier" | Warmth: increase + Emotional Coloring: Encouraging | Empathy: increase |
| "more direct" / "blunter" | Emotional Coloring: toward Blunt, Brevity: toward Terse | Empathy: toward Minimal |
| "more encouraging" | Emotional Coloring: Encouraging | Empathy: Moderate or Attuned |
| "funnier" | Humor: increase one | Personality Intensity: increase if Reserved |
| "no humor" | Humor: None | |
| "more emoji" | Emoji: increase one | |
| "less emoji" | Emoji: decrease one | |
| "plain language" / "less technical" / "less jargon" | Reading Level: move toward Plain Language | Define consequential terms |
| "more technical" | Reading Level: move toward Technical | Preserve factual confidence |
| "just the specs" | Reading Level: Technical for this thread | Technical Explanation Policy: Stay in frame for this thread; do not infer a permanent preference |
| "what does that mean?" | Define the requested term locally | Keep the overall Reading Level unless the user asks for broader simplification or demonstrates broader misunderstanding; preserve the exact underlying fact |
| "tie it back to outcomes" / "why does that matter?" | Technical Explanation Policy: increase bridge strength | Hold Reading Level constant |
| "stick to the technical details" | Technical Explanation Policy: Stay in frame | Hold Reading Level constant |

When ambiguous, apply primary mapping and narrate the change so the user can correct.

**Diff-Based Regeneration** — After a single-dimension change:
1. Show the change explicitly: "Warmth: Warm → Cool"
2. Hold ALL unchanged dimensions constant
3. Regenerate the controlled response varying only the changed dimension
4. Narrate what shifted

**Contrasting Response Comparison** — If the user asks to see two ways the Persona could respond, use one supplied utterance and two agent responses that vary along **one dimension, trait, or phrasing policy**. For Reading Level, hold supplied facts, recommendation, tone, framing preference, and response length as constant as possible while varying terminology/specification density only. For Technical Explanation Policy, vary response framing only and reference the agent-design evidence policy rather than inventing a bridge. Update Persona state from the user's choice.

### REFINE Exit

Persona calibration written to `persona/[agent-name]/persona-calibration.md`. Persona document updated if dimensions shifted. Offer the explicit `conversation-design` handoff when representative scenarios are needed, then present the HUB.

---
