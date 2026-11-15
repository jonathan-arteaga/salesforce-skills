---
id: H04
name: pronunciation-dictionary
category: configuration
severity: medium
applies_to: [migrate, optimize]
detection:
  - structural: "agent uses brand / product / jargon terms recurringly"
    in: [welcome, instructions, response_templates]
principle_refs: [P5]
---

# Pronunciation dictionary

## Why it matters

TTS engines mispronounce brand names, product names, medical specialties, and domain jargon at predictable rates. "Nuffield" gets read as "Nu-field" or "Nuh-feeld". "Orthopaedics" mispronounces in en-US engines defaulting to en-GB content. Hospital town names pronounce inconsistently ("Newcastle" stress varies).

The fix is an **in-script** `modality voice` key: `pronunciation_dict`, a list of grapheme→phoneme entries the TTS consults before synthesis. Each entry pairs a `grapheme` (the written term) with a `phoneme` (its pronunciation) and a `type` (`IPA` or `CMU`/ARPAbet). It lives in the `.agent` file alongside the other voice settings — the skill writes it directly, and also emits a human-readable starter list as a side artifact (`pronunciation-dictionary.md`) for review before the entries go into the script.

**Model dependency — this is really a Flash v2 feature.** Custom pronunciation is honored by **Flash v2** (the model with the best custom pronunciation of any). **Flash v2.5 doesn't support it at all**, and it is **not a documented capability of the default v3 model** — v3's strength is reading entities like numbers, emails, and IDs correctly out of the box, not honoring a custom dictionary. So a `pronunciation_dict` on the default model may be silently inert: if custom pronunciation genuinely matters for an English agent, that is itself a reason to select **Flash v2** (nested format — see H03). Confirm every entry in **live preview**, on the model the agent will actually run.

**The agent's own name and the brand are always on the list.** Take them from the Persona (and the H08 name block). The name is the first thing the caller hears, so a wrong stress or vowel there costs more than anywhere else. On Flash v2, add both to `pronunciation_dict`. On the default v3, where the dictionary is likely inert, use a respelling strategy instead: test the name in the casting sides (H09), and if v3 says it wrong, spell it phonetically in the spoken copy only (e.g. "Ny-AH-mh" for "Niamh" in the welcome), never in fields that are displayed or logged. Add both to `inbound_keywords` too (H05), so the recognizer hears the caller say them.

## Detection

Source uses recurring proper nouns or domain terms:
- Brand names ("Nuffield", "Bupa", "AXA")
- Hospital / location names ("Newcastle", "Guildford", "Highgate")
- Medical specialties ("Orthopaedics", "Otolaryngology", "Cardio-Thoracic")
- Insurer names
- Foreign-origin terms or names

The skill scans user-visible content + topic instructions and proposes candidates.

## Chat example (before)

(Not applicable — chat displays text correctly without phonetic guidance.)

## Voice example (after) — recommended

**Write the entries in-script** as a `pronunciation_dict` under `modality voice:` (this is what the validator checks and what real voice agents use):

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"
    pronunciation_dict:
        - grapheme: "Nuffield"
          phoneme: "ˈnʌfiːld"
          type: "IPA"
        - grapheme: "Orthopaedics"
          phoneme: "ɔːθəˈpiːdɪks"
          type: "IPA"
        - grapheme: "Bupa"
          phoneme: "ˈbuːpə"
          type: "IPA"
```

**Stage candidates as a side artifact first** (couples with `templates/pronunciation-dictionary.md`) — the skill scans the agent's terms and proposes a starter list for human review before the entries land in `pronunciation_dict`:

```markdown
# Pronunciation Dictionary — starter list (verify in voice preview)

| Term | IPA | Notes |
|---|---|---|
| Nuffield | ˈnʌfiːld | Brand name. Default en-GB engine often gets wrong. |
| Orthopaedics | ɔːθəˈpiːdɪks | Stress on "pae". |
| Cardio-Thoracic | ˌkɑːdɪoʊθəˈræsɪk | Hyphenated; some engines split as two words. |
| Newcastle (upon Tyne) | ˈnjuːkɑːsl | Stress on "New", not "cas". |
| Bupa | ˈbuːpə | Insurance brand. |

⚠️ All entries unverified — transcribe into `modality voice: → pronunciation_dict` (or the org's Voice Settings dictionary if you use that instead), then test in voice preview on the model the agent runs. Adjust the phoneme if pronunciation is still wrong. Custom pronunciation is a Flash v2 capability (see H03).
```

## Voice example — alternatives

**SSML `<phoneme>` overrides** inline in instructions: works without a `pronunciation_dict`, but the LLM has to emit the tag consistently:

```
| When mentioning the company, use:
| "<phoneme alphabet='ipa' ph='ˈnʌfiːld'>Nuffield</phoneme> Health"
```

Brittle — the LLM occasionally drops the phoneme tag. The in-script `pronunciation_dict` is more reliable.

**Org-level Voice Settings dictionary** — if your platform exposes a pronunciation dictionary in Agentforce Builder → Voice Settings, entries there apply org-wide across agents. Use it for terms shared by many agents; use the in-script `pronunciation_dict` for agent-specific vocabulary that should travel with the script.

**Skip if all terms have standard pronunciations.** If the agent's vocabulary is everyday English with no brand names or jargon, no dictionary needed.

## Anti-patterns

- **Setting IPA without testing.** The engine's interpretation of IPA varies. Always verify in voice preview, not by reading the IPA back.
- **Adding every English word.** The dictionary is for non-default pronunciations only. Adding everything bloats config and slows TTS.
- **Leaving the starter list un-transcribed.** The skill outputs `pronunciation-dictionary.md` as a *candidate* list; the entries only take effect once they're written into `modality voice: → pronunciation_dict` (or, if used, the org's Voice Settings dictionary). Add to the V1 review checklist.
- **Hard-coding ARPAbet on an IPA-only engine** (or vice versa). Verify the engine's accepted format before generating.

## Where it lives

- **In-script:** `modality voice: → pronunciation_dict` (voice channel config — encoding-model surface #3), a list of `{grapheme, phoneme, type: IPA|CMU}` entries. This is what the skill writes and what the offline validator checks.
- **Side artifact (staging):** `pronunciation-dictionary.md` (generated by Phase 5/7) — the human-review candidate list before entries land in `pronunciation_dict`.
- **Org-level (alternative):** a platform Voice Settings dictionary, if your org uses one, for terms shared across many agents.

## Mis-applications (optimize mode)

- **Pattern: dictionary exists but only covers brand names, not specialties.** Add the specialty list (these mispronounce often).
- **Pattern: dictionary entries are hard-coded for one TTS engine and the org switched engines.** IPA is portable but verify; CMU/ARPAbet may not be.
- **Pattern: dictionary loaded once and never updated as new terms enter the agent.** Add to a periodic review process.
- **Pattern: `pronunciation_dict` set but the agent runs on the default v3 model.** Custom pronunciation is a Flash v2 capability — on v3 (and Flash v2.5) the dictionary is likely inert. If the terms genuinely mispronounce, the fix is model selection (Flash v2, nested format — H03), not more entries.
