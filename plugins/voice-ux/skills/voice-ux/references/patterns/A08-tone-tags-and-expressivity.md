---
id: A08
name: tone-tags-and-expressivity
category: system-instructions
severity: medium
applies_to: [migrate, optimize]
detection:
  - structural: "v3 voice agent whose system.instructions carry no delivery/tone direction"
    in: [system.instructions]
  - regex: '\[(warmly|warm|reassuring|encouraging|softly|curious|enthusiastic|cheerful|excited|sunny|calm|serious)\]'
    in: [system.instructions, response_templates]
  - structural: "tone tags present but the voice runs on a Flash model (tags inert)"
    in: [config, system.instructions]
principle_refs: [P5, P11]
pattern_refs: [T-phrasebook]
couples_with: [H03, A09]
---

# Tone tags and expressivity

## Why it matters

Text loses prosody on the way out: the same sentence can land warm, clipped, or flat, and plain instructions do not tell the voice which. **Audio tags** (also "tone tags") are bracketed delivery directions such as `[warmly]`, `[reassuring]`, and `[curious]`. They ride inside `system.instructions` and steer how a line is spoken, not what it says. When a completed `persona.md` is supplied, Persona Tone Flex remains authoritative for situational word choice, semantic shift, maximum, hard boundary, and reset. A08 maps that policy to audible delivery; it does not redefine the Persona Tone Flex policy. Any character change is `[review needed]`.

**They only work on ElevenLabs v3.** Tags are a v3 capability. On a Flash model they don't modulate delivery — and worse, a voice/tag mismatch can read the bracket text *aloud* ("...open bracket, warmly, close bracket..."). This is the same model-gating trap as `outbound_speed` / `outbound_similarity` (see H03): the default language model for most locales is v3 Conversational, so tags work out of the box there — but if the agent has been moved to a Flash model (nested format) for pronunciation or accent reasons, tags go inert and you fall back to A09 (contractions, cadence, punctuation-driven prosody) plus voice settings. Tags also need a voice with genuine emotional range and a **moderate-to-low `outbound_stability`** (≈0.5–0.7); at high stability (0.85+) the model suppresses variation and the tags barely move the delivery (H03).

**Humor is not a laughter licence.** A Persona with light humor licenses light prosodic play (a brighter `[curious]`, a smile in the voice on v3). Laughter and body-sound tags (`[laughs]`, `[chuckles]`, `[sighs]`) stay out: they simulate a person in the room (Z05).

Expressivity is not licence to overact. One tag per phrase, at the phrase start, chosen for the moment — never a stack, never a tag on every clause. "A tag on every reply" (a rule some enablement material uses) is the wrong unit: after a few turns it sounds performed. One tag per phrase where it adds something, varied, and none when unsure, ages better.

**The latency tradeoff.** Moving to a Flash model is a common latency recommendation, and Flash does respond faster. But tags only work on v3, so that one model switch quietly turns this whole pattern off. Treat it as a tradeoff to weigh with the persona owner: milliseconds versus the expressive layer. Don't tick it as a free latency win (H03, H06).

## Detection

- The agent runs on the default v3 model (no Flash selection) but `system.instructions` give the voice no delivery direction at all — every line is spoken at one flat setting.
- Tone tags are present but **stacked** (`[warmly][excited][reassuring]`), repeated identically every turn, or scattered so densely they'll be read aloud.
- Tone tags are present **and** the `modality voice` block selects a Flash model — the tags are inert (and at risk of being voiced literally). Cross-check H03.

## Chat example (before)

(Not applicable — chat has no audio delivery. Tone tags are a voice-only, v3-only concern; there's no chat equivalent to migrate.)

## Voice example (after) — recommended

**Method: one resting tag + situational shifts.** Give the agent a baseline delivery that matches its Persona contract (P5), then map each supplied Tone Flex trigger to a spoken shift and use the same reset condition. When no Persona is supplied, infer cautiously from the Script/sample and mark character assumptions `[review needed]`. Author the delivery rule in `system.instructions`, not in fixed copy:

```
DELIVERY (v3 only): Your resting delivery is [warm]: {resting profile from the
Persona, e.g. "grounded, unhurried"}.
Shift for the moment, then settle back:
- Reassure a worried caller: open the turn [reassuring] or [softly].
- Share good news / availability found: [encouraging] — never congratulatory (A05).
- Ask an exploratory or clarifying question: [curious].
- Deliver crisis or sensitive content: [serious], slow — never bright (F01).
One tag per phrase, at the phrase start. Never stack tags. Vary turn to turn — don't
open every turn with the same tag. If unsure, use no tag and let the words carry it.
```

**Lexical–prosodic sync.** Each Persona Tone Flex trigger has a lexical cue (Persona's) and gets one prosodic shift (this skill's). Write them as a pair, so they fire together and reset together. Excited words in a flat voice, or a bright voice on a sober line, sound insincere. If the shift you'd need contradicts the lexical cue, that's `[review needed]`, not a delivery fix.

```
Tone Flex trigger T2 (caller worried):  lexical cue "help first, plain words"  ↔  [reassuring], ~90% pace
                                        reset: after the issue is resolved      ↔  back to resting [warm]
```

**Map shifts to Persona Tone Flex through prosodic profiles (P5).** The four situational profiles give you the audible palette; they do not replace Persona's lexical/discourse cue:
- **Calm Authority** → `[calm]`, `[serious]`, measured — for commitments, compliance, escalation.
- **Grounded Warmth** (a common baseline) → `[warm]`, `[reassuring]`, `[softly]` — for reassurance and rapport.
- **Dynamic / High-Energy** → `[encouraging]`, `[enthusiastic]`, `[sunny]` — for good news; suppress in error/crisis (A05, F01).
- **Conversational Baseline** → little to no tagging; punctuation and cadence (A09) carry it.

**An upbeat-baseline variant.** For a bright, service-forward persona, a practical rule set from the field is: rest on `[sunny]`; open with `[reassuring]` when the caller sounds worried, and help first; go back to the baseline on purely logistical turns. It's the same method as above with a brighter rest state. Use it only when the Persona contract is upbeat, not as a default.

**Dynamic progress indicators can carry a tag too.** When G01's progress message is left empty so the agent generates it, the same delivery rule applies to that generated line (v3 only).

**A worked palette to generalise from — not a fixed list.** One production voice agent used `[warmly]`, `[encouraging]`, `[reassuring]`, `[softly]`, `[curious]`, `[enthusiastic]`, `[sunny]`. Treat that as an example of *range*, not a menu to copy — pick tags that match this agent's persona and the emotional beats its flow actually has. See the ElevenLabs v3 audio-tags reference: <https://elevenlabs.io/blog/v3-audiotags>.

## Voice example — alternatives

**Non-v3 voices (Flash v2 / v2.5): drop tags, lean on A09.** Tags are inert on Flash. Express persona through contractions and cadence (A09), punctuation-driven prosody (a comma buys a beat; a full stop resets pitch), and voice settings (H03) — a slightly lower `outbound_stability` on the models that honour it. Don't leave literal `[tags]` in the instructions of a Flash agent; they'll surface as spoken words.

**Sparing tags even on v3.** For a measured, formal persona (financial, legal), a nearly-untagged baseline with an occasional `[reassuring]` on the one worried moment is stronger than continuous colour. Expressivity earns attention by contrast.

## Anti-patterns

- **Stacking tags.** `[warmly][excited][reassuring]` — the model can't render three at once; delivery goes muddy or the brackets get read aloud.
- **The same tag every turn.** `[warmly]` on all forty turns is a monotone of warmth — it stops meaning anything. Vary, and rest at neutral.
- **A mandatory tag on every reply.** Same failure, by rule. One per phrase where it earns its place, none when unsure.
- **Switching to Flash for latency and keeping the tags.** The tags go inert, and may be read aloud. Decide the tradeoff explicitly; if Flash wins, remove the tags and move expressivity to A09.
- **Tags in fixed copy fields.** Put delivery direction in `system.instructions`, not baked into `messages.welcome` or response templates where it can't vary by context and is likelier to leak as spoken text.
- **Tags on a Flash agent.** Inert at best, voiced literally at worst. Gate on the model (H03).
- **Emotive tags in crisis / error paths.** `[enthusiastic]` while a caller is distressed is the tonal version of the congratulatory-language ban (A05, F01). Shift to `[serious]` / `[softly]`.
- **First-person emotion instead of a tag.** Writing "say you're thrilled" rather than tagging `[warmly]` — that's an A10 violation; convey warmth through delivery, not by the agent claiming feelings.

## Where it lives

- `system.instructions` (global) — the resting-delivery rule + the shift list.
- Per-topic `reasoning.instructions` — a topic with a distinct emotional beat (crisis, good news) may restate the shift for that moment.
- Gated by the `modality voice` model (H03): v3 only.

## Mis-applications (optimize mode)

- **Pattern: v3 agent with rich instructions but zero delivery direction.** `[consider]` — it's leaving the biggest expressivity lever unused.
- **Pattern: tone tags present but `outbound_stability` is 0.9.** The tags can't move a near-monotone voice; lower stability into ≈0.5–0.7 (H03) or the tags are decorative.
- **Pattern: tags present on a Flash-model agent.** `[changed]` — inert and at risk of being spoken; remove and route persona to A09 + voice settings.
- **Pattern: one tag repeated every turn.** `[consider]` — add variation and a neutral resting state.
