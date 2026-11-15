---
id: H07
name: barge-in-recovery
category: configuration
severity: medium
applies_to: [migrate, optimize]
couples_with: [A04, I02]
detection:
  - structural: "voice agent whose system instructions say nothing about what to do after the caller interrupts"
    in: [system.instructions]
  - regex: '(?i)(continue|resume|pick up) (where you left off|your (previous|last) (answer|reply|response))'
    in: [system.instructions, instructions]
principle_refs: [P1]
pattern_refs: [T-repair]
---

# Barge-in recovery (experimental)

> **Experimental.** The core rule (stop, take the interruption as the turn, answer it directly) is established voice practice and is safe to emit. The `@system_variables.last_reply` variant depends on a recent platform release and is **not recognized by the offline validator**, so it's opt-in and `[review needed]`. Promote it once it has been confirmed on a target org.

## Why it matters

Barge-in is always on in Agentforce Voice. The platform detects the interruption and stops TTS, and there's no sensitivity setting to tune. What the script controls is **what the agent does next**, and that's where agents most often go wrong. After being cut off, a naive agent either resumes the reply it was giving or re-asks for something the caller already confirmed. The caller interrupted *because* they had something to say, so either move tells them they weren't heard.

The evidence is concrete. In the test call cited in the *Designing for the Ear* enablement deck, 10 of 23 replies after a barge-in re-asked confirmed details or went off script. The rule from P1 is: yield, treat the interruption as the current turn, and **answer it directly**. That last part is what turns yielding into something useful.

Interruptions also carry reference. "That one." "Yeah, the second." The caller is pointing at the part of the reply they heard. On platform releases that expose it, the agent can see how much of its last reply actually played, which lets it resolve "that one" against what the caller heard rather than what it meant to say.

## Detection

- System instructions are silent on interruption. Most chat-origin scripts are, because chat has no barge-in.
- Instructions tell the agent to "continue where you left off" or "finish your previous answer". In voice, that is the wrong move after barge-in.
- Optimize mode: transcripts where the agent's turn after an interruption repeats its previous reply, or re-asks a value already set in a variable.

## Chat example (before)

```
system:
    instructions: |
        You are the event assistant. Help attendees find and book sessions.
        If you are asked several things, answer each one in turn.
```

(Nothing about interruption, because chat can't be interrupted. In voice, the agent resumes its list after the caller says "that one", or asks "Which session would you like?" again.)

## Voice example (after) — recommended

**Prose rule in system instructions.** It validates everywhere and needs no platform variable:

```
system:
    instructions: |
        You are the event assistant. Help attendees find and book sessions.
        If the caller cuts in while you are speaking, stop. Treat what they just said as the current turn and answer it directly.
        Don't resume or repeat the reply they interrupted, and don't ask again for anything they have already confirmed.
        If they point at something ("that one", "the second"), take it to mean the item you had just said when they cut in.
```

Sounds like:

> **Agent:** There's a keynote at ten, and a hands-on lab at eleven…
> **Caller:** That one. Add it.
> **Agent:** Done. The eleven o'clock lab is on your agenda.

## Voice example — alternatives

**Interruption-aware branch (platform release 262.12+; `[review needed]`).** Recent releases expose two system variables: `@system_variables.last_reply.interrupted` (whether the last reply was cut off) and `@system_variables.last_reply.interrupted_heard_text` (the part the caller actually heard). Put them at the top of the subagent's `reasoning.instructions`:

```
reasoning:
    instructions: ->
        if @system_variables.last_reply.interrupted:
            | The caller cut in. They only heard this much of your last reply: {!@system_variables.last_reply.interrupted_heard_text}
            | Treat what they just said as the current turn and answer it directly. Don't resume your previous reply.
        | Help the caller find and book sessions.
```

**Validator caveat:** the offline AgentScript validator (2.9.8) knows only `@system_variables.user_input`, so it reports `last_reply` as an undefined reference (an **error**, not a warning). Emit this variant only when the target org is confirmed on a supporting release, keep the prose rule above in `system.instructions` as the fallback, and flag the block `[review needed]` in the change log. Don't let a validator error from this variant block the rest of the rewrite.

## Anti-patterns

- **"Continue where you left off."** After barge-in, the caller has moved the conversation. Resuming talks over their intent.
- **Re-asking confirmed details.** If the date is already in `@variables.booking_date`, don't ask for it again because a reply got cut off. Pair with I02 so volunteered values are captured, not re-collected.
- **Apologising for being interrupted.** "Sorry, go ahead" spends a turn on nothing. Answer what they said.
- **Treating barge-in as an error to repair.** It's normal turn-taking (P1). Don't route it through the J01 repair counter.
- **Asking for a sensitivity setting.** There isn't one. Don't put barge-in tuning in Layer E as if it were configurable.

## Where it lives

`system.instructions` (the prose rule, always). Optionally a conditional at the top of each subagent's `reasoning.instructions` (the 262.12+ variant).

## Mis-applications (optimize mode)

- **Pattern: the barge-in rule is present but the agent still re-asks.** Usually the confirmed value isn't held in a variable, so the agent has nothing to remember it by. The fix is I02-style capture, not more instruction text.
- **Pattern: the `last_reply` branch was emitted, and the build fails offline validation.** Expected with the current validator. Confirm the org release, and if it isn't supported, fall back to the prose rule.
- **Pattern: the turns are so long that every reply gets interrupted.** That's a P1 turn-length problem (1–2 sentences, about 20 s). Fix the length before tuning recovery.
