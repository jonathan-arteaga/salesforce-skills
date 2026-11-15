---
id: H05
name: key-term-prompting
category: configuration
severity: medium
applies_to: [migrate, optimize]
detection:
  - structural: "agent collects domain-specific terms from user input"
    in: [instructions]
principle_refs: [P10]
---

# Key-term prompting (STT bias)

## Why it matters

STT engines have generic vocabularies. Domain-specific terms — insurer names, hospital names, consultant names, medical specialties — get mistranscribed at high rates because the model's prior probability for these tokens is low. "AXA" becomes "axe a", "Aviva" becomes "a viva", "Cardio-Thoracic" becomes "cardio thora SIC".

The fix is **key-term prompting** (also called context biasing or hot-words): a list of expected terms passed to the STT engine to raise their prior probability during recognition.

The predictable terms are authored **in the `.agent` file**, at `modality voice: → inbound_keywords: → keywords:` (a list). This is a sibling of the voice settings (H03) and the `additional_configs` timings (H06) inside the same `modality voice:` block — the skill writes it directly, it is not Workbench-only. Fill it with the vocabulary you can predict or know from testing: product names, plan tiers, insurer/brand names, branch locations, specialties. Unbounded or caller-specific vocabulary (every possible surname) can't be enumerated — for those, the repair ladder (P10 / D-category spell-confirm) is the fallback, not biasing.

`inbound_keywords` is in-script — a sibling of H04's in-script `pronunciation_dict`. The skill still generates a starter list as a side artifact for review and for overflow vocab that exceeds a vendor hot-word cap, but the core list goes into the script.

## Detection

Source has topics that collect or recognize:
- Insurer names (`find_insurer`)
- Consultant names (`find_closest_consultant_names`)
- Hospital names (from `Get_Hospitals_within_Specified_Distance` results)
- Medical specialties (the supported-list mapping in E04)
- Postcodes (the alphanumeric structure benefits from biasing toward UK-format)

## Chat example (before)

(Not applicable — chat input is typed text.)

## Voice example (after) — recommended

**Author the predictable terms in-script (`modality voice: → inbound_keywords:`):**

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"
    outbound_speed: 0.9
    inbound_keywords:
        keywords:
            - "AXA"
            - "Aviva"
            - "Bupa"
            - "Cardio-Thoracic Surgery"
            - "Orthopaedics"
            - "Tunbridge Wells"
```

The skill writes this block from the predicted term list in Phase 7 and surfaces it as `[review needed]` so the developer trims/extends it against real recognition.

**Generate a companion starter list as a side artifact** (for review, and for overflow vocab beyond a vendor hot-word cap):

```markdown
# Key-Term Prompting — starter list (verify with STT preview)

## Insurer names
- AXA
- Aviva
- Bupa
- Vitality
- WPA
- Cigna
- Allianz

## Hospital cities (UK)
- Newcastle
- Guildford
- Highgate
- Chichester
- Tunbridge Wells
- ...

## Specialties
- Anaesthetics
- Cardiology
- Cardio-Thoracic Surgery
- Dermatology
- ENT
- Gynaecology
- Neurosurgery
- Oncology
- Ophthalmology
- Oral Maxillo-Facial Surgery
- Orthopaedics
- Paediatrics
- Pathology
- Plastic Surgery
- Psychiatry
- Radiology
- Rheumatology
- Sports Medicine
- Urology

## Postcode patterns (regex / context hint)
- /^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$/i — UK postcode format

⚠️ Load into Voice Settings → Key-Term Prompting (or platform equivalent).
Verify recognition with sample utterances ("AXA", "Aviva", "Orthopaedics")
before deploy.
```

## Voice example — alternatives

**Inline biasing per topic:** some platforms allow per-action / per-topic biasing. Useful if the term list varies (e.g., bias toward specialty names only when in the specialty-collection turn).

**Confidence-driven explicit confirmation as fallback:** if biasing isn't available or doesn't fix recognition, accept that some terms will mishear and design Tier-2 repair for them ("Sorry, did you mean AXA, A-X-A, or something similar?"). Combines with D-category spell-confirm patterns.

**Org-level vocabulary lists:** for large term sets (full hospital list across the country), load into the org's persistent voice vocab rather than per-call biasing.

## Related inbound knob: `inbound_filler_words_detection`

`modality voice:` has a sibling inbound flag, `inbound_filler_words_detection` (flat boolean, default `False`). When `True`, the recognizer strips disfluencies — "um", "uh", false starts — from the transcript before it reaches the agent, so filler doesn't get mistaken for content or trip a keyword match.

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"
    inbound_filler_words_detection: True     # [review needed] ignore um/uh/false starts
    inbound_keywords:
        keywords: [ "AXA", "Aviva", "Bupa" ]
```

**Light steer, not a rule:** telephony callers hesitate and self-correct out loud, so `True` is often the right default for phone agents — it keeps the transcript clean for slot-filling and intent matching. Leave it `False` (or test both ways) when disfluency itself is signal — e.g. a de-escalation flow (P13) where hesitation is a distress cue, or when you're debugging what the STT actually heard. It interacts with barge-in and repair: cleaner transcripts mean fewer spurious no-match/repair loops, but over-aggressive stripping can swallow a genuine short utterance, so confirm by preview.

In the emerging nested format this is `inbound: → filler_words_detection:` (see H03).

## Anti-patterns

- **Listing 1000+ terms.** STT engines have practical limits (varies by vendor — some hard-cap at 100-500 hot-words). Prioritize the top recurring terms.
- **Including common English words.** Biases the engine away from natural speech. Domain-specific only.
- **Generating the list once and never updating.** New consultants, new insurers, new hospitals — the list ages. Add to a periodic refresh process.
- **Ignoring postcode biasing.** Postcodes mishear constantly; biasing to UK format dramatically improves capture.

## Where it lives

- **In-script:** `modality voice: → inbound_keywords: → keywords:` (the predictable terms — written by the skill). Sibling of H03 voice settings and H06 `additional_configs`.
- **In-script:** `modality voice: → inbound_filler_words_detection` (flat boolean, default `False`) — the sibling filler-word recognizer flag.
- **After publishing:** confirm `inbound_keywords` is in the compiled agent (SKILL.md Phase 8, step 6). A field build reported it missing after a clean publish. It survives the offline compile, so the drop is org-side and not yet reproduced.
- Side artifact output: `key-term-prompting.md` (generated by Phase 5/7) — for review and for overflow vocab beyond a vendor hot-word cap.
- Org-level voice configuration for anything the in-script list can't hold (large persistent vocab / custom-vocabulary uploads, depending on platform).

## Mis-applications (optimize mode)

- **Pattern: list covers insurers but not specialties.** Specialties mishear at higher rates than insurers (more syllables, more medical-Latin). Add.
- **Pattern: list copied verbatim from another org.** Locale and customer base differ. Regenerate from this agent's actual vocabulary.
- **Pattern: list deployed but not verified with sample utterances.** Recognition still fails for terms that aren't actually being biased correctly. Test before relying.
