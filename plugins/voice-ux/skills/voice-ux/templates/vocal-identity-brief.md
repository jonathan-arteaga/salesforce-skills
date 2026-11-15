# Vocal identity brief and casting record — output skeleton

Generated in Phase 4b (H08 → H09 → H03). One file per agent. It holds the brief, the casting sides, the audition scores, and the decision record. The rewrite bundle summarises it and links here.

Suggested filename: `artifacts/voice-ux/[agent-name]-vocal-identity.md`

The brief never contains voice IDs or settings. Those appear only in the casting record (section B) and in the `.agent` `modality voice:` block.

---

```markdown
# Vocal identity: [agent name] ([locale])

**Persona source:** [persona-handoff.json / persona.md path + SHA-256 / inferred from Script and sample]
**Persona handoff status:** [approved / draft / not supplied]
**Brief status:** [derived from Persona / inferred — review needed]

---

## A. Vocal Identity brief (H08)

### 1. Derivation trace
| Persona field | Value | Vocal implication |
|---|---|---|
| Personification | [Not personal / Individuated / Anthropomorphic] | [e.g. restrained expressivity, no character voice] |
| Register / Formality | [...] | [...] |
| Warmth / Emotional Coloring | [...] | [resting profile, P5] |
| Personality Intensity | [...] | [stability band, tag density, pitch range] |
| Empathy | [...] | [size of shift on distress triggers] |
| Negative Identity | [...] | [must-not-sound-like items] |
| [other fields that matter here] | [...] | [...] |

### 2. Audience and listening conditions
- Callers: [age profile, L2 share, stress state, hearing-impaired share]
- Channel: [PSTN narrowband 8 kHz / mobile / voice-over-web]
- Environments: [car, home, workplace noise]

### 3. Perceived identity
- **Gender presentation:** [female / male / deliberately ambiguous] — decided by [who], [date], because [why]. *(Elicited, never inferred from the role. "Ambiguous" means the most neutral-sounding voice the catalog offers, validated by listeners in section B.)*
- **Age band:** [...]
- **Accent per locale:** [locale → local / neutral-standard / brand-specified]
- **Pitch zone:** [...]
- **Voice quality:** [clear, resonant, low breathiness, ...]
- **Baseline tempo:** [brisk / moderate / unhurried]

### 4. Perceptual target
- **Must sound:** [3–5 adjectives a listener could rate]
- **Must not sound like:** [2–3 items, from Negative Identity]

### 5. Expressive range
- **Resting profile:** [Calm Authority / Grounded Warmth / Dynamic / Conversational Baseline]
- **Allowed shifts:** [Tone Flex trigger → prosodic shift → ceiling → reset]
- **Forbidden effects:** laughter, breaths, sighs, filler sounds, simulated presence (Z05), [others]

### 6. Two-voice relation
- **System / IVR voice:** [description; how it contrasts: timbre or gender, formal, no persona expression]

### 7. Locale variants
| Locale | Voice requirement | Pronunciation notes |
|---|---|---|
| [en_US] | [...] | [...] |

### 8. Name block
| Term | IPA / respelling | STT keyword | Notes |
|---|---|---|---|
| [Agent name] | [...] | yes | [v3: respelling in copy; Flash v2: `pronunciation_dict`, H04] |
| [Brand] | [...] | yes | [...] |

---

## B. Casting record (H09)

### Hard filters
- Locale / language: [...]
- Model: [eleven_v3 / eleven_flash_v2 / eleven_flash_v2_5 / kotoba] because [H03 reason]
- Target org: [alias]; catalog snapshot taken [YYYY-MM-DD]

### Shortlist
| # | Voice name | voice_id | Model | Why shortlisted |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Casting sides
1. **Welcome:** "[agent-layer welcome, with name and brand]"
2. **Readback:** "[alphanumeric or number readback]"
3. **Distress turn:** "[Tone Flex distress response]"
4. **Repair turn:** "[tier 1 or 2 repair]"
5. **Name, brand, Lexicon:** "[sentence with name, brand, and three hard terms]"
6. **Long turn (~25s):** "[...]"

### Audition
- **Channel:** [phone / Builder Preview] *(Preview only: rendering may differ on a phone line; re-check on a call before go-live if a number becomes available.)*
- **Listener tier:** [minimum: 1 listener / recommended: 3–5 independent listeners, ≥1 from the target audience]
- **Listeners:** [roles, not necessarily names]

| Voice | Listener | [adj 1] | [adj 2] | [adj 3] | Perceived gender | Defects |
|---|---|---|---|---|---|---|
| 1 | L1 | 1–5 | 1–5 | 1–5 | female / male / hard to say | [accent drift, garbled alphanumerics, loudness drift, tags read aloud, none] |

### Decision
- **Chosen:** [name / voice_id / model]
- **Runner-up:** [name / voice_id / model] (fallback if the chosen voice is deprecated)
- **Rationale:** [one or two sentences against the brief]
- **Approved by:** [name, role, date] *(human sign-off; until then the `voice_id` stays `[review needed]`)*

---

## C. Light tuning log (H03)

Change one parameter at a time and re-audition the same casting sides.

| Step | Parameter | From → To | Model honours it? | Heard effect | Keep? |
|---|---|---|---|---|---|
| 1 | outbound_stability | 0.5 → 0.6 | yes (all models) | [...] | [y/n] |
```
