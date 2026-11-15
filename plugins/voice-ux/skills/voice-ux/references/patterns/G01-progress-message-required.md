---
id: G01
name: progress-message-required
category: latency-masking
severity: high
applies_to: [migrate, optimize]
detection:
  - structural: "action defined without progress_indicator_message"
    in: [actions]
  - regex: 'progress_indicator_message:\s*"(Loading|Processing)"'
    in: [actions]
principle_refs: [P7]
pattern_refs: [T-latency-pre-announce]
---

# Progress message required

## Why it matters

Voice latency without a verbal cue is interpreted as "the line dropped" or "the agent is stuck". Silence beyond ~700ms is perceptible; >1s triggers user remedial action ("hello? are you there?"). Every action call that takes more than a second needs a verbal pre-announce.

In Agent Script, `progress_indicator_message` is the field. In chat, it's a UI status string ("Validating postcode…"). In voice, it must be **conversational** ("just checking that postcode…").

Two gotchas that turn this into the exact unmanaged-silence failure mode:
- **`include_in_progress_indicator` defaults to `false`.** A `progress_indicator_message` on its own is dead config — it never plays, and the caller sits in silence while the action runs. The message is only voiced when `include_in_progress_indicator: True` is set alongside it.
- **Both fields live on the action *definition*, not on the binding** in `reasoning.actions`. Putting them on the `topic: @actions.foo` reference line does nothing; they belong in the `actions:` block where the action's `target:` is declared.

## Detection

Source has actions with:
- No `progress_indicator_message` at all
- `progress_indicator_message: "Loading…"` or `"Processing"` (chat-shaped status, not voice-conversational)
- `include_in_progress_indicator: False` or absent (so the message never plays)
- `progress_indicator_message` set but the action is fast (<1s) — not strictly wrong, but unnecessary

## Chat example (before)

```yaml
Validate_Postal_Code:
    description: "..."
    target: "generatePromptResponse://Postal_Code_Validator"
```

(No progress message. In chat, fine — no audible gap. In voice, ~2 seconds of silence.)

```yaml
AgentForce_Appointment_Booking:
    target: "flow://AgentForce_Appointment_Booking"
    include_in_progress_indicator: True
    progress_indicator_message: "Booking Appointment"
```

(Has a message but it's chat-shaped — "Booking Appointment" reads as a status banner, not a sentence.)

## Voice example (after) — recommended

**Conversational message, `include_in_progress_indicator: True`:**

```yaml
Validate_Postal_Code:
    description: "..."
    target: "generatePromptResponse://Postal_Code_Validator"
    include_in_progress_indicator: True
    progress_indicator_message: "Just checking that postcode…"
```

```yaml
AgentForce_Appointment_Booking:
    target: "flow://AgentForce_Appointment_Booking"
    include_in_progress_indicator: True
    progress_indicator_message: "Booking that now. One moment…"
```

**Vary across actions (rotation):**
- Postcode validation: "Just checking that postcode…"
- Hospital lookup: "Let me find your nearest hospitals…"
- Slot search: "Let me check what's available…"
- Booking commit: "Right, booking that now. One moment…"
- Adviser availability: "Just checking who's free…"
- Case creation: "Setting that up for you…"

## Three things fill silence

Voice latency has three separate affordances, and they get blurred easily. Use them together, because they solve different parts of the problem:

| Layer | What | Scope | Carries meaning? |
|---|---|---|---|
| 1. Filler audio (`beepboop_config`) | Platform-played `.wav` during any action call | Every action, automatic | No, non-verbal floor |
| 2. Filler sentences (`outbound_filler_sentences`) | Spoken lines the platform plays during a long wait | Agent-wide, authored once | A little: generic "still working" |
| 3. `progress_indicator_message` | Conversational line voiced when a specific action runs | Per-action, authored | Yes: "let me look that up…" |

Layer 1 is the always-on safety net (the caller never hits raw silence). Layer 3 is the meaningful, per-action cue you prioritise on the long/slow actions. Layer 2 sits in between: agent-wide spoken filler for waits the other two don't cover. A well-tuned voice agent has Layers 1 and 3 at minimum.

### Layer 1: `beepboop_config` (platform filler audio)

Agentforce Voice ships with `beepboop_config`: a `.wav` filler that begins playing once an action call has been running for a configurable delay. **The default delay is 6000ms; the recommended value is 500ms.** The delay is authored **in the `.agent` file** (`modality voice: → additional_configs: → beepboop_config: → max_wait_time_ms:`, accepts 500–60000ms), so the skill writes it directly rather than deferring it to a human. See **H06** for the full `additional_configs` block. (The `.wav` audio itself is platform-supplied; only the delay is scripted. The 6000ms figure is the platform default, not a schema default: omit the key and you get 6000ms.)

**Why start it at ~0.5s, not 6s:** starting the noise only after several seconds *accentuates* that the response is slow. Starting it almost immediately instead (a) makes it obvious the caller is talking to an AI, (b) makes clear the call hasn't dropped, (c) signals something is happening, and (d) reads as ambient "working" rather than a "this is super slow, hold on" sentinel. Typical action latency is 3–4s and sometimes 7–8s, so a 6s delay leaves most waits partly uncovered; 0.5s covers all of them.

This is the floor, not the whole story: on the long/slow actions (the 7–8s ones), add a per-action `progress_indicator_message` (Layer 3) so the wait is filled with meaning, not just a tone.

### Layer 2: `outbound_filler_sentences` (spoken filler)

In the flat `modality voice:` format, filler sentences are a list under a `waiting` key:

```yaml
modality voice:
    outbound_filler_sentences:
        - waiting: ["Still on it, one moment.", "Nearly there.", "Thanks for bearing with me."]
```

Write these in the persona's voice. Three variations of "Please wait." undo everything the persona work bought: the caller hears a call-centre hold loop, not the agent they were just talking to. (The enablement deck shows a nested `outbound: filler_sentences:` form; that home is unverified against the compiler, see H03 `[review needed]`.)

### Layer 3: `progress_indicator_message` (per-action)

- **Leave it empty to have the agent write one.** `progress_indicator_message: ""` with `include_in_progress_indicator: True` makes the agent generate the line at runtime, in the caller's language. This is the simplest correct choice for multilingual agents and a reasonable default when you can't author one per action. Fence it: a generated line can leak action and field names ("Calling retrieveSessions with sessionTypes…"), so add a sentence to the action's `description` naming which inputs the progress line may mention and forbidding the rest (`T-translate-plumbing`).
- **A fixed message also renders as text on web.** If the same agent serves a web channel, the authored line shows up there as a status string. Write it so it works read as well as heard.
- **Rotate with `\n`.** Several variants separated by `\n` in one string rotate across calls (`"Let me find that for you.\nOne moment while I pull up your return."`). This works in Script view only; the Builder form field doesn't preserve it.
- **Word each action differently**, so a turn with two lookups doesn't say the same line twice.

**Diagnostic: if the caller hears "let me check" over and over, the fix is usually fewer tool calls, not better wording.** Repeated progress lines mean the agent is making several action calls per turn. Trim or merge the actions (or move the lookup to `before_reasoning`) before you polish the copy.

## Voice example — alternatives

**Pre-action narration in instructions** (couples with G02): for irreversible commits, narrate before the call rather than during, so the caller hears it before the action starts:

```
| Pre-announce: 'Right, booking that now. One moment…'.
| Then call confirm_booking.
```

This combines with the action's `progress_indicator_message` for a layered cue.

## Anti-patterns

- **No message at all.** Caller sits in silence; thinks the call dropped.
- **"Loading…".** Reads as a status word, not conversation. Use a phrasebook holding token.
- **"Processing" / "Please wait".** Same problem — chat status language.
- **Text-shaped progress messages.** Even non-status phrasing can be text-shaped. **Good (conversational):** "Let me look that up…". **Bad (text-shaped):** "Getting answers…" — reads as a loading-spinner caption, not something a person says aloud. Voice it the way a human colleague would narrate the same pause.
- **`include_in_progress_indicator: False` while having a `progress_indicator_message`.** The message exists but never plays. Misleading config.
- **Same message for fast and slow operations.** "Let me check…" for both a 100ms cache hit and a 12-second multi-system join. The slow case needs warning ("This might take a few seconds. Bear with me…").
- **Narrating the action's name.** "Calling Validate_Postal_Code". Implementation detail leak.

## Where it lives

Action definitions inside topic `actions:` blocks AND topic-level `actions:` blocks (per-topic action definitions).

## Mis-applications (optimize mode)

- **Pattern: voice script has progress messages on slow actions but not on medium ones.** A 1-3 second postcode validation gets missed because "it's not that slow". Everything > 1 second needs one.
- **Pattern: voice script has identical messages on all actions.** No rotation. The caller hears "Let me check…" 6 times in 30 seconds. Vary.
- **Pattern: voice script has progress messages but `include_in_progress_indicator: False`.** Misconfigured. Silent wait.
- **Pattern: progress message is too long.** "I'm just running a quick check on the system to find what's available, please bear with me, this may take a moment…" The progress message is itself longer than the wait. Keep <2 seconds spoken.
