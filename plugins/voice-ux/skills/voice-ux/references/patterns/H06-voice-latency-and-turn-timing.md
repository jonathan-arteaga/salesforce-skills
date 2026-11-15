---
id: H06
name: voice-latency-and-turn-timing
category: configuration
severity: high
applies_to: [migrate, optimize]
couples_with: [H01, H03, G01]
applies_after: [H01]
detection:
  - structural: "modality voice block present without an additional_configs block"
    in: [config]
  - regex: 'beepboop_config|speak_up_config'
    in: [config]
principle_refs: [P3, P7]
pattern_refs: [T-latency-filler-audio, T-config]
---

# Voice Latency and Turn Timing (additional_configs)

## Why it matters

Two of the timings that govern how a voice turn feels are authored **in the `.agent` file**, inside `modality voice: → additional_configs:`. They are not Workbench-only settings, and leaving them unset means the platform defaults silently apply — which are wrong often enough to matter:

- **`beepboop_config` (filler-audio delay)** — the non-verbal floor under latency (P7). The platform default is 6000ms, which leaves most 3–4s waits uncovered and makes the agent read as slow. Recommend **500ms**.
- **`speak_up_config` (no-input pursuit)** — how long the agent waits before prompting a silent caller, and what it says (P3). The compiler floor is 10000ms; the message should be a phrasebook holding/repair token, not silence. **After three unanswered speak-ups the platform ends the call without saying anything.** That makes `speak_up_message` the last words a silent caller hears, and it may play up to three times in a row, so it has to hold up on repetition.

The compiler enforces the ranges, so some designs are simply not expressible — know that before promising them.

## Detection

Source `modality voice:` block (added by H01) has no `additional_configs:` child, OR has one with some sub-blocks missing. In optimize mode, an `additional_configs:` block may be present but carry platform-default values (e.g. `beepboop_config` still at 6000).

Ranges the compiler enforces (verified against the offline AgentScript validator):

| Key | Path under `additional_configs:` | Range (ms) | Recommended |
|---|---|---|---|
| `max_wait_time_ms` | `beepboop_config:` | 500–60000 | **500** |
| `speak_up_first_wait_time_ms` | `speak_up_config:` | 10000–300000 | **10000** |
| `speak_up_follow_up_wait_time_ms` | `speak_up_config:` | 10000–300000 | **10000** |
| `speak_up_message` | `speak_up_config:` | string | a holding/repair token |

## Chat example (before)

(Not applicable — chat agents have no voice channel and no `modality voice:` block. This pattern adds config that has no chat equivalent.)

## Voice example (after) — recommended

**Full `additional_configs:` block inside `modality voice:` (siblings of the voice settings from H03):**

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"
    outbound_speed: 0.9
    outbound_stability: 0.85
    outbound_similarity: 0.85
    additional_configs:
        beepboop_config:
            max_wait_time_ms: 500               # filler audio at ~0.5s, not the 6000ms platform default
        speak_up_config:
            speak_up_first_wait_time_ms: 10000  # wait 10s of no-input before pursuing
            speak_up_follow_up_wait_time_ms: 10000
            speak_up_message: "Take your time. I'm here when you're ready."
```

The skill **writes these values** into the generated `.agent` in Phase 7 using the recommended defaults, and flags each as `[review needed]` so the developer tunes against a real call. `beepboop 500` is a low-risk latency win; `speak_up` changes no-input behavior, so it especially wants a listen before shipping.

`speak_up_message` is a spoken line — treat it like any other copy: pull it from the persona phrasebook (Repair / Holding function, see T-phrasebook), don't leave it as a robotic default.

**Don't use "Are you still there?"** It's the most common speak-up line and the one the Voice Quality Heuristics name as a failure. It puts the problem on the caller, sounds like a dropped call, and on its third play it's the last thing they hear before a silent hang-up. Give the caller room ("Take your time…") or move the call forward ("If it's easier, I can put you through to someone.").

**Leave `endpointing_config` at the platform default.** Lowering it to make the agent feel snappier clips callers who pause mid-sentence, such as someone reading a number off a card. Field experience with an in-script endpointing value made agents feel unresponsive, so the skill doesn't emit one (see README, v0.6.0).

## Voice example — alternatives

**beepboop only (minimum latency hygiene):** if you're only willing to change one thing, set `beepboop_config.max_wait_time_ms: 500` and leave speak-up at platform defaults. It's the highest-value, lowest-risk knob.

```yaml
    additional_configs:
        beepboop_config:
            max_wait_time_ms: 500
```

**Longer no-input pursuit:** for IVR-style flows where the caller may be fetching a card or reference number, raise `speak_up_first_wait_time_ms` above the 10000ms floor so the agent doesn't nag someone who's mid-task.

## Anti-patterns

- **Leaving `beepboop_config` unset "because there's a default".** The default is 6000ms — most waits finish before the filler even starts, so the caller hears raw silence. Set it to 500.
- **Treating these as Workbench settings.** They are in-script. Deferring them to a human via Layer E was the old (incorrect) guidance; the skill now writes them.
- **`speak_up_message` left as a default or blank.** A silent no-input timeout, or a robotic "Please respond", both fail P3. Use a warm pursuit line from the phrasebook.
- **"Are you still there?" as the speak-up line.** It blames the line, not the design, and it can be the last thing the caller hears before the silent hang-up after three unanswered speak-ups.
- **Lowering endpointing to cut latency.** It clips callers who pause mid-utterance. Get speed from beepboop, progress messages and fewer actions, not from cutting the caller off.
- **Values that don't compile.** `beepboop` below 500 or above 60000, or speak-up timers below 10000, are rejected by the compiler. Stay in range (the table above).

## Where it lives

`modality voice: → additional_configs:` in the `config:` region of the `.agent` file — siblings of the H03 voice settings, added by/after H01. Both sub-blocks are optional; add the ones the design needs.

## Mis-applications (optimize mode)

- **Pattern: `additional_configs` present but `beepboop_config` still at 6000 (or unset).** The most common miss — the block exists but the latency floor was never lowered. Set to 500.
- **Pattern: `speak_up_message` is a text-shaped or default string** ("No input received", "Please respond", "Are you still there?"). Rewrite as a phrasebook pursuit token.
- **Pattern: speak-up timers set below the 10000ms floor in the source** — won't compile; surface as `[changed]` with the floor value.
