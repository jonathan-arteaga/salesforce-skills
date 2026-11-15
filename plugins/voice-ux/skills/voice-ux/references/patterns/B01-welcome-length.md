---
id: B01
name: welcome-length
category: welcome-and-static
severity: high
applies_to: [migrate, optimize]
couples_with: [B02]
detection:
  - structural: "greeting turn > 35 words, or agent layer > ~18 words (~7 seconds spoken)"
    in: [welcome]
  - regex: '<br>'
    in: [welcome]
  - structural: "welcome contains chat ID / transcript ID interpolation"
    in: [welcome]
principle_refs: [P4]
pattern_refs: [T-opening]
---

# Welcome length

## Why it matters

Voice openings have a hard 5–7 second budget (P4). After that, the user starts to feel they've been put on hold. Chat welcome messages routinely run 30+ seconds when read aloud — they pack identity, capabilities, regulatory disclaimers, privacy notes, emergency redirects, and the first question into one block. Voice users have already forgotten the disclaimers by the time the question arrives.

The fix is structural: split the welcome into two layers (T-opening) — a system layer for legal/regulatory content (recording and transcription notice, AI disclosure, emergency redirect) and an agent layer for self-identification + first question. Each layer has its own constraints.

The agent layer also has to *frame scope*. First impressions are decisive in voice: callers default to "human please" quickly when an opening feels robotic or overlong. So the capability frame should say what the agent can do — "I can help with your orders, deliveries, and returns" or "I'll take a few details and log a case for the team to follow up by the next business day" — rather than an open-ended "ask me anything," which invites requests the agent can't handle. (See T-opening for the agent layer's three recurring elements.)

**Who owns which part of the welcome.** When a completed Persona is supplied, it owns the welcome's *wording and register*: how the agent introduces itself, the words of the capability frame, the tone of the invitation. This skill owns the *spoken structure*: the system/agent split, the ~5–7s budget, where the disclosure sits, and the call to action as the last thing in the turn. You may re-chunk, shorten, or re-voice the Persona's welcome to fit that structure. Any change to what it *means* is `[review needed]`. Legal text is immutable for both skills.

**Resolve `[Agent Name]` from the Persona.** The examples below use `[Agent Name]` and "Northwind" as placeholders. In a real rewrite, take the agent name and brand from the Persona, and give both a pronunciation entry (H04) and an STT keyword (H05). A name the TTS says wrong in the first second undoes the whole opening.

## Detection

Source `messages.welcome` (or equivalent) contains any of:
- More than 35 words for the whole greeting turn (Voice Agent Optimization Guide §2.3), or more than about 15–18 words in the agent layer (~6–7 seconds at 140 wpm). Disclosure the law requires on outbound or recorded calls doesn't count against the agent layer; move it to the system layer instead
- Multiple sentences joined with `<br>`
- Chat-shaped interpolation: chat ID, transcript ID, "your chat ID is X"
- Privacy policy reference, disclaimers, "we don't offer emergency services"
- Credit-card / data warnings

## Chat example (before)

```
"Hi {!@variables.First_Name}, I'm the Northwind Customer Experience virtual assistant.<br>
I can help with your orders, deliveries, returns, and product questions, but I
can't process payments or change your account password here.<br>
This chat may be recorded and transcribed for quality and training.<br>
Please don't share any credit card details or full account numbers.
To find out how we use your data, see our privacy policy.<br>
Your chat ID is {!@variables.Transcript_Id_Formula}. Please keep this for
reference.<br>
How can I help you today?"
```

## Voice example (after) — recommended

**Two-layer opening (T-opening):**

**System layer** — formal, distinct TTS voice, no contractions, voiced first:

> "Thanks for calling Northwind Customer Experience. This call may be recorded and transcribed for quality and training. You will be speaking with our AI voice assistant. For our full privacy terms, visit northwind dot com."

**Handover** — 600–900ms pause.

**Agent layer** — in the Persona's register (here: warm), varied prosody, contractions normal, voiced second:

> "Hi, I'm [Agent Name], Northwind's AI assistant. I can help with your orders, deliveries, and returns. How can I help you today?"

The agent layer is ~6 seconds at 140 wpm and ends with the question (P9 end-focus). The system layer carries the legal weight.

## Voice example — alternatives

**IVR / carrier-side pre-call announcement:** if the platform supports it, the system layer plays before the agent connects — the institutional disclosures live in the IVR / carrier layer and the agent welcome stays to a single warm greeting (see T-opening worked example). Verify availability with the platform/CTI team — most don't have it by default.

**Single-layer short welcome (no system layer):** if there's no regulatory requirement for recording/transcription/AI disclosure in the jurisdiction, drop the system layer entirely:

> "Hi, you're through to Northwind. I'm [Agent Name], an AI assistant. I can help with orders, deliveries, and returns. How can I help you today?"

Verify the regulatory minimum with legal/compliance — different markets have different requirements.

**Returning-caller variant:** if CTI provides a known caller, personalise:

> "Hi, welcome back to Northwind. What can I help you with today?"

**Capability-frame shapes:** the agent-layer capability frame takes more than one shape depending on what the agent does. When the agent answers questions, frame the topics it covers; when it logs a case for later follow-up, frame that instead — either way, state the scope rather than leaving it open-ended.

> Scope: "…I'm [Agent Name], Northwind's AI assistant. I can help with your orders, deliveries, and returns. How can I help you today?"
>
> Transactional: "…I'm [Agent Name], Northwind's AI assistant. I'll take a few details and log a case for the team to follow up by the next business day. Can I start with your name?"

## Anti-patterns

- **Reading the chat-ID line.** "Your chat ID is X-Y-Z-1-2-3" is meaningless in voice — the user has no way to retain it without a screen.
- **Asking the question first, then disclosing.** P9 violation in the wrong direction — the user starts answering before they've heard the disclosure.
- **Repeating the AI disclosure on every turn.** Once is required (B02). After that it's noise.
- **Open-ended agent layer with no capability frame.** "Hi, I'm [Agent Name] — how can I help?" with no statement of scope invites out-of-scope requests and erodes trust when the agent then can't handle them. Name what the agent can do (or the case it will log).
- **Skipping the handover pause.** Without 600–900ms between layers the user perceives one long welcome and the layered structure collapses.

## Where it lives

`messages.welcome` (agent-layer content). System-layer content lives either in IVR / carrier config (Layer E item) or, if voiced by the agent in sequence, prepended to `messages.welcome` with the handover pause.

## Mis-applications (optimize mode)

- **Pattern: two-layer structure exists but both layers use the same TTS voice.** No perceptual contrast — the user hears one long welcome. Configure distinct voices (Layer E item).
- **Pattern: agent layer is short but system layer is too long (>13s).** Push the system layer to the IVR / carrier-side announcement.
- **Pattern: handover pause is <300ms.** No perceptual gap; the layers blend. Configure ≥600ms.
- **Pattern: agent layer doesn't end with a question.** P9 violation — fix the end-focus.
