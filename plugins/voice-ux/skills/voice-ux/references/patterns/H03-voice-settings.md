---
id: H03
name: voice-settings
category: configuration
severity: high
applies_to: [migrate]
couples_with: [H01, A08, H08, H09]
detection:
  - structural: "modality voice block has placeholder voice_id"
    in: [config]
  - structural: "modality voice block missing speed/stability/similarity"
    in: [config]
principle_refs: [P5]
---

# Voice settings and light tuning

## Why it matters

The voice the agent uses realizes the Persona audibly. `voice-ux` owns the whole chain: the Vocal Identity brief (H08), casting and audition (H09), and the **light tuning** in this pattern, plus the emitted `voice_id`. Work from the completed Persona contract when one exists. The target org constrains which IDs are valid, and a human listening sign-off approves the result. Do not pick the first available voice or silently alter Persona register to fit it. If the source has no coherent character contract, run `persona` before casting. Defaults are rarely right; settings should match the brief and the audience constraints captured in Phase 3.

**Light tuning is deliberately small.** Casting does the heavy lifting: a well-cast voice needs little adjustment, and a miscast voice can't be tuned into the right one. In scope:
- model choice (below)
- the stability band
- `outbound_speed`, on Flash models only
- the similarity floor (≥0.75)
- resting and shift tags, on v3 (A08)
- pauses through punctuation: a comma buys a beat, a full stop resets pitch (not `<break>` tags, which are unreliable)

Out of scope: style exaggeration, heavy SSML, and per-utterance parameter tricks. **Method:** change one parameter at a time, re-audition the *same* casting sides (H09), and log each step in the vocal identity file. If two parameters move at once, you can't tell which one you heard.

**The model behind the voice — read this before tuning.** Every voice runs on a TTS *model*, and the model decides which delivery parameters actually do anything. Each language has a default model (most languages: **ElevenLabs v3 Conversational**; Japanese: Kotoba), set by a platform lifecycle gate. The flat/legacy config in this pattern **can't select a model** — model selection exists only in the emerging nested format (see "Choosing a voice model" and "Emerging: selecting a non-default model" below) — so a flat block runs on the language default. On v3 Conversational that has a concrete consequence: **v3 ignores `outbound_speed` and `outbound_similarity`; only `outbound_stability` is honored, and v3's default stability is 0.5.** So on today's default model, setting speed or similarity has no audible effect — those parameters only bite once you select a **Flash** model, which requires the nested format. Stability is the one delivery knob that works on the default model.

Five parameters are expressible in the flat format — but which ones *do* anything depends on the model:

| Parameter | Schema range | Usable range | Starting point | Honored by | When to deviate |
|---|---|---|---|---|---|
| `voice_id` | org library | — | (from the casting record, H09) | all models | Recast via H08/H09, not by tuning |
| `outbound_speed` | 0.5–2.0 | 0.7–1.1 | 0.9 | Flash v2 / v2.5 only — **inert on default v3** | Faster (1.0–1.1) for terse personas; slower (0.80–0.93) for warm/expansive or older audiences |
| `outbound_stability` | 0–1 | — | **v3: 0.5** (the model default) · **Flash: 0.85** | all models | **v3:** stay near 0.5 so tags can move the delivery; raise toward 0.6–0.7 for a measured or formal persona; above ~0.8 tags barely register. **Flash:** lower (0.55–0.70) for expressive; higher (0.85–0.95) for clinical/measured |
| `outbound_similarity` | 0–1 | ≥0.75 | 0.85 | Flash v2 / v2.5 only — **inert on default v3** | Keep ≥0.75 — below this the voice drifts |
| `outbound_style_exaggeration` | 0–1 | — | (omit) | Flash-family (not in the vendor model-parameter doc — verify by ear) | Raise slightly for more expressive delivery; omit to use the persona's tuned default |

**Schema range vs. usable range:** the compiler accepts `outbound_speed` anywhere in 0.5–2.0, but that's not the same as *intelligible* — and it only matters at all under a Flash model. Above ~1.1 the voice gets hard to follow on a phone line; below ~0.7 it drags. The 0.7–1.1 band is where usable settings live (the vendor's own range for the model parameter is 0.7–1.2) — the schema won't stop you from shipping a value outside it, so treat that band as a guardrail and confirm by ear. The usable band and the ≥0.75 similarity floor are properties of the *model*, so they apply only when a Flash model is actually honoring the parameter.

**No single setting is "right."** `outbound_speed`, `outbound_stability`, and `outbound_similarity` shape the voice's linguistic character — pace, expressiveness, and consistency respectively — *on the models that honor them*. The values throughout this pattern are **illustrative starting points, not targets**: tune them by ear against the persona and audience, and preview with real audio before shipping. Experiment freely — the guardrails below (the ~1.1 intelligibility ceiling, the ≥0.75 similarity floor, monotone at stability 1.0) mark the edges of the usable space when the model honors the parameter, not the destination.

## Choosing a voice model

**Default heuristic:** stay on the language default (v3 Conversational for most languages) unless you have a specific reason to switch. Reach for a **Flash** model when you need one of: reliable custom pronunciation (Flash v2, English — see H04), steadier UK / Australian / other non-US English accents (Flash v2), regional non-English accents like Argentinian Spanish or French Canadian (Flash v2.5), lower latency, or working `speed` / `similarity` control. Selecting a non-default model requires the nested format (below), and confirm the result by **live preview** — never by a static sample.

| Model | Model ID | Strengths | Delivery parameters | Custom pronunciation | Reach for it when |
|---|---|---|---|---|---|
| **v3 Conversational** (default) | `eleven_v3` | Most natural / expressive; reads entities (numbers, emails, IDs) correctly out of the box | Ignores `speed` & `similarity`; honors `stability` (model default 0.5) | Not a documented capability | Default for most languages — you want expressiveness and correct entity read-out and don't need speed/similarity control. Less reliable on UK / AU accents. |
| **Flash v2** | `eleven_flash_v2` | Highest-quality English; steadier UK / AU accents than v3; lower latency | Honors `speed`, `stability`, `similarity` | **Best of any model** | English agents needing custom pronunciation, non-US English accents, faster responses, or fine delivery control |
| **Flash v2.5** | `eleven_flash_v2_5` | Best secondary accents for non-English (e.g. Argentinian Spanish, French Canadian, European Portuguese); lower latency | Honors `speed`, `stability`, `similarity` | **Not supported** | Non-English agents needing regional accents, faster responses, or delivery control |
| **Kotoba** | `kotoba` | Japanese speech | Takes no parameters (omit the block) | — | Japanese (`ja`) — it's already the default there |

Like `voice_id` itself, model choice must be constrained by the Persona and audience, then designed in `voice-ux` and approved through the human listening sign-off (H09). Canvas (Agentforce Builder) does not expose a model selector; v3 is the only model available there, so any non-default model lives in Agent Script only.

**Tone tags are a v3-only expressivity layer (see A08).** Audio/tone tags like `[warmly]` or `[reassuring]`, written into `system.instructions` as delivery directions (the persona-expression device covered by A08), work *only* on v3 Conversational — and only when the voice has emotional range and `outbound_stability` sits low enough to modulate (roughly 0.5–0.7; at 0.85+ the voice is too steady to shift). This is the mirror image of `speed`/`similarity`: those are Flash-only and inert on v3, whereas tone tags are **v3-only and inert on Flash** — worse, a Flash voice may *read a stray tag aloud* instead of acting on it. So the expressivity path forks by model: **v3 → tone tags (A08); Flash / anything else → contractions, cadence, punctuation, and voice settings (A09).** If you've selected a Flash model for pronunciation or accent reasons, lowering stability won't buy you tag support — don't script tone tags expecting delivery changes.

## Detection

Source `modality voice:` block (added by H01) has:
- `voice_id: "REPLACE_ME"` or absent
- Missing `outbound_speed`, `outbound_stability`, `outbound_similarity`
- Settings hardcoded from another org without verification

## Chat example (before)

(Not applicable — chat agents have no voice settings.)

## Voice example (after) — recommended

> These blocks use the **flat/legacy format** — the one the offline validator recognizes and that every deployed voice agent currently uses. A flat block runs on the language default model (v3 Conversational for most languages), so `outbound_speed` and `outbound_similarity` are **inert here**; they're kept as tuned starting points that take effect only if you later select a Flash model (see "Emerging: selecting a non-default model" below). `outbound_stability` *does* apply on v3.

Map from the Persona, not from a stock register. The dimension → delivery table in P5 says which Persona values move which setting. The three examples below are illustrations for three common Persona shapes; they aren't defaults to copy.

**Example — warm, measured healthcare persona (illustrative; the register comes from that engagement's Persona):**

```yaml
modality voice:
    voice_id: "<voice_id from the casting record>"   # H09
    outbound_speed: 0.9                               # inert on v3; takes effect only under Flash
    outbound_stability: 0.55                          # v3: just above the 0.5 default, tags still move
    outbound_similarity: 0.85                         # inert on v3
```

**Example — encouraging / wellness-coach persona:**

```yaml
modality voice:
    voice_id: "<voice_id from the casting record>"
    outbound_speed: 0.92                              # inert on v3
    outbound_stability: 0.5                           # v3 default: full room for [encouraging] / [warm]
    outbound_similarity: 0.85                         # inert on v3
```

**Example — formal / financial-services persona:**

```yaml
modality voice:
    voice_id: "<voice_id from the casting record>"
    outbound_speed: 0.95                              # inert on v3
    outbound_stability: 0.7                           # v3: steadier; occasional [reassuring] still lands
    outbound_similarity: 0.88                         # inert on v3
```

On a Flash model (nested format, below) the same three personas would start nearer 0.85 / 0.65 / 0.9 stability, because Flash's default is steadier and it has no tags to protect.

## Voice example — alternatives

**Two-voice opening (couples with B01):** if implementing T-opening's two-voice structure, set the **agent layer** voice here. The **system layer** voice lives in carrier config (Layer E item) — different speaker, more formal.

**Per-locale voice IDs:** in multi-locale agents (`en_GB`, `fr_FR`), each locale needs its own voice ID. Some platforms surface this as a per-locale block; others require runtime selection.

## Emerging: selecting a non-default model (nested format)

To use anything other than the language default model, the vendor documents a **nested** `modality voice` format carrying a `persona_id` (the voice's hash ID from the Voice Catalog — model-specific), a `model.id`, and a `model.parameters` passthrough.

**Glossary: `persona_id` is a voice, not a Persona.** Despite the name, the platform's `persona_id` is the hash ID of a *voice* in the Voice Catalog. It has nothing to do with the `persona` skill's character contract or `persona.md`. Record it in the casting record (H09) like any other voice ID.

```yaml
modality voice:
    outbound:
        persona_id: "a029af9d692c"        # April (en_US), a Flash v2 voice — hash ID from the Voice Catalog
        model:
            id: "eleven_flash_v2"          # or eleven_flash_v2_5 (non-English), eleven_v3 (default), kotoba (ja)
            parameters:
                speed: 1.0                 # Flash honors speed/stability/similarity; v3 ignores speed & similarity
                stability: 0.8
                similarity: 0.75
    inbound:
        filler_words_detection: True       # nested spelling of the flat inbound_filler_words_detection (H05)
        keywords:                          # nested spelling of the flat inbound_keywords → keywords (H05)
            - "urgent"
            - "emergency"
```

Per-language model overrides (e.g. Kotoba for `ja`) nest under `language_settings: → <locale>: → outbound:`.

**The nested block needs a `language:` block with `default_locale`.** Without one, publish quietly falls back to the platform default voice and the persona's voice is lost, with no error. Always pair a nested `modality voice` block with:

```yaml
language:
    default_locale: "en_US"
```

**Speech-to-text (inbound) is not really a builder choice yet.** The enablement deck lists Nova 2 Phone Call, Nova 3 and Nova 3 Medical Boosted under `inbound: → model:`, but as of August 2026 inbound runs on Nova-3 unless product provisions a custom model for the org. Don't design around an STT model switch; use `keywords` (H05) for terms the recognizer actually gets wrong.

**Treat this as emerging, not the skill's emitted default.** Five load-bearing caveats:

1. **The offline validator (2.9.8) doesn't model it yet.** The nested keys (`outbound:`, `model:`, `parameters:`, `persona_id`, `inbound:`) validate as `unknown-field` **warnings**, and the compiled output then has an **empty** `modality_parameters.voice` (checked October 2026). A field build saw the same thing after publishing with the Agent Script SDK. Flat keys are fully validated and come through.
2. **No deployed agent uses it yet.** Every real `modality voice` block seen in the field is flat. Nested is doc-ahead-of-runtime.
3. **You can't mix the two formats in one script.** Moving to nested means rewriting the *entire* `modality voice` block — there's no automatic conversion. Critically, the flat latency / turn-timing config (`additional_configs` beepboop + speak-up, H06) and `pronunciation_dict` (H04) have **no documented nested home**, so a nested migration today risks silently dropping them. The enablement deck shows nested `outbound: → filler_sentences:` and `outbound: → pronunciations:` (grapheme / phoneme / `CMU` type) keys; those homes are not yet confirmed against the compiler, so treat them as `[review needed]` and verify on a preview before relying on them.
4. **A nested block without `language: → default_locale` publishes as the default voice.** See above. It's a silent failure, so check it every time.
5. **The vendor recommends nested for new configuration** — but for the reasons above, this skill still emits flat by default. Switch to nested only when you specifically need a non-default model; when you do, port the whole block by hand and re-preview.

So: **flat stays canonical for what the skill emits; nested is the path to model selection when v3's defaults don't fit.**

## Anti-patterns

- **Leaving `voice_id` as a placeholder.** Deploy succeeds with platform default. Easy to miss until first voice preview.
- **`outbound_speed: 1.5` for "faster calls".** The schema accepts up to 2.0, but above ~1.1 is rarely intelligible on a phone line and 1.5 is effectively unusable. A legal value is not a good one.
- **`outbound_similarity` below 0.7.** The voice drifts from the original speaker — sounds different turn-to-turn.
- **`outbound_stability: 1.0`.** Monotone. On v3 start at the 0.5 default; on Flash start at 0.85 and tune down for warmth, never up beyond 0.95.
- **`outbound_stability: 0.85` on a v3 agent that uses tags.** That's the Flash starting point. On v3 it flattens the delivery so far that A08's tags barely move it.
- **Tuning to fix a casting problem.** If the voice sounds wrong for the brief, no stability value will fix it. Recast (H09).
- **Changing several parameters at once.** You can't tell which one you heard. One at a time, same casting sides.
- **Voice ID from one org used in another.** Voice IDs are org-scoped. Always look up the target org's voice library before setting.
- **Hardcoded voice ID in source-controlled `.agent`.** Better: use a config variable / environment substitution if the deployment target varies.
- **Tuning `outbound_speed` or `outbound_similarity` and expecting the default voice to change.** On the default v3 Conversational model these are ignored — only `outbound_stability` moves. If you need working speed/similarity control, select a Flash model (nested format); otherwise you're editing dead config.
- **Nested block with no `language:` / `default_locale`.** Publishes, then plays the platform default voice. The persona's voice never reaches the caller.
- **Generic filler sentences.** Three variations of "Please wait." in `filler_sentences` / `outbound_filler_sentences` undo the persona work. Write them in the persona's voice (G01).
- **Reaching for the nested format just to set speed/stability.** If v3's defaults are fine and you don't need a different model, stay flat — nested buys you model selection, not tuning, and costs you validator coverage plus your beepboop/speak-up config.

## Where it lives

`modality voice:` block (added by H01) — the **flat/legacy format** (`voice_id` + `outbound_*` as direct children), which is what the skill emits and what the validator checks. Model selection lives in the emerging **nested** format (`outbound: → model:`), documented above but not emitted by default. After publishing, confirm the settings reached the compiled agent (SKILL.md Phase 8, step 6): a clean publish doesn't prove they did.

## Application order

Apply with H01 (Application order step 1). The voice settings need to be present before any later patterns reference voice behavior.

## Human steps (casting sign-off)

The skill designs the casting (H08, H09) and emits the chosen `voice_id`, but it can't see the org's voice library or hear the result. Two steps stay human and go into the V1 review checklist, not Layer E:

> **Voice pick and sign-off:** open Agentforce Builder → Voice Settings, confirm the shortlisted voices exist in this org, and record the IDs in the casting record. Audition with the casting sides, on a phone call where possible (Preview is acceptable with a caveat). Sign off against the brief. If a two-voice opening is used, the system-layer voice lives in carrier/IVR config, which *is* a Layer E item.
