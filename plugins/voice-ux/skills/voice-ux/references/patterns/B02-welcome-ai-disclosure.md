---
id: B02
name: welcome-ai-disclosure
category: welcome-and-static
severity: high
applies_to: [migrate, optimize]
couples_with: [B01, A10]
detection:
  - structural: "welcome lacks any of: 'AI', 'virtual assistant', 'automated', 'bot'"
    in: [welcome]
principle_refs: [P4]
pattern_refs: [T-opening]
---

# Welcome AI disclosure

## Why it matters

Voice channels have no UI label, avatar, or "Bot" badge — the only way the user knows they're speaking to an AI is the agent telling them. Most jurisdictions now require AI disclosure on voice channels (EU AI Act, FTC guidance, several US states, UK ICO guidance for healthcare and financial services). It's also a trust requirement: callers expect to know if they're being recorded and if they're talking to a machine.

In chat the disclosure can be implicit (the chat window says "Virtual assistant"). In voice it must be in the spoken opening.

Bring legal in early. Disclosure and consent requirements — recording/transcription, AI disclosure, and whether consent is opt-in or opt-out — vary by country, region, state, and language, and they change what has to be said (and sometimes in which layer). Get the requirements confirmed before writing the opening, not after.

**Disclosure is a floor, not a Persona preference.** A brand card may ask for the AI to stay invisible ("never say 'as an AI'"). Persona can record that preference, but this skill doesn't honour it below the floor: the caller hears that they're talking to an AI, either in the IVR/system layer or in the agent layer, depending on what the jurisdiction requires. A Persona or brand instruction that would remove disclosure is `[review needed]` and goes to legal. Instructions that try to make the caller believe they're talking to a person are caught by Z05.

## Detection

Source `messages.welcome` (or equivalent) does NOT contain any of:
- "AI" / "AI assistant"
- "virtual assistant"
- "automated assistant" / "automated service"
- "bot"
- "this call may be recorded and transcribed" (implies, but doesn't state, automated)

If none are present, the disclosure is missing.

## Chat example (before)

```
"Hi, I'm the Northwind Customer Experience assistant. How can I help you today?"
```

(No disclosure that "assistant" means AI rather than a human service rep.)

## Voice example (after) — recommended

**Disclosure in the system layer (preferred — couples with B01):**

> System layer: "Thanks for calling Northwind Customer Experience. This call may be recorded and transcribed for quality and training. You will be speaking with our AI voice assistant. For our full privacy terms, visit northwind dot com."
>
> [600–900ms pause]
>
> Agent layer: "Hi, I'm [Agent Name], Northwind's AI assistant. I can help with your orders, deliveries, and returns. How can I help you today?"

**Disclosure in agent layer (single-layer welcome):**

> "Hi, you're through to Northwind. I'm [Agent Name], a virtual assistant. I can help with orders, deliveries, and returns. How can I help you today?"

## Voice example — alternatives

**"AI assistant" wording:** more direct, slightly less warm.
> "Hi, this is the Northwind AI assistant."

**"Automated service":** more formal, financial-services register.
> "You've reached Northwind's automated service line."

Pick the wording that matches the persona register (Layer C). Don't mix — pick one and use it consistently.

## Anti-patterns

- **Disclosure buried mid-sentence.** "Hi, welcome to Northwind, where we offer a wide range of products and our AI assistant can help with your order today." The disclosure is there but lost in the prose.
- **Disclosure only on first turn but not when the user explicitly asks "am I talking to a bot?".** Some compliance regimes require an in-conversation disclosure on demand. Add a global rule: "If the caller asks whether they're speaking to a person or a machine, voice 'I'm an automated assistant. I can help with [X], or put you through to a person if you'd prefer.'"
- **Sole reliance on a pre-connect disclosure with no agent-side re-affirmation.** If the *only* AI disclosure plays in the IVR / carrier-side announcement before the call connects, a caller who started speaking may miss it. The IVR / carrier-side split (see T-opening, B01) is sound *because* the agent layer re-affirms identity to an engaged listener — the agent-layer self-ID ("Hi, I'm [Agent Name], Northwind's AI assistant") re-discloses to someone now paying attention. Keep that agent-side self-ID; don't let the pre-connect announcement carry the disclosure alone. Verify the arrangement with legal — some regulators are stricter than others.
- **"Don't self-identify unless asked."** Some enablement material recommends not volunteering AI status and only confirming it on demand. For the opening, that's the wrong default. Disclosing once at the start (IVR layer or welcome) is the norm and often the law: EU AI Act transparency rules, several US state bot laws. After the opening there's no need to repeat it unprompted (A10). On demand, answer plainly.
- **A "before" example that penalises "I'm an AI agent".** When reviewing a welcome, don't mark the disclosure as the verbose part. Trim the capability list or the pleasantries; keep the disclosure.
- **Implying agency the agent doesn't have.** "I'm your Northwind agent" reads ambiguous — could be human or AI. Pick a word that's unambiguously machine.

## Where it lives

`messages.welcome` (agent layer) and the system-layer content (IVR / carrier config or prepended welcome). The disclosure may also appear in a separate `system.disclosure` field if the runtime supports it.

**Relationship to A10 (agent self-reference).** B02 owns the *required opening disclosure* and the hard compliance requirement. A10 governs the surrounding self-reference conduct — how the agent answers "are you a bot?" on demand, the ban on claimed first-person emotion, and the rule against re-announcing AI status unprompted mid-call. They couple: A10 does **not** remove this opening disclosure, and the on-demand wording in both must stay consistent (use the client / Legal-approved phrasing where provided).

**Revisit on every market expansion.** The disclosure/consent set is not write-once. Whenever the engagement adds a new market, region, state, language, or demographic, re-check the recording, AI-disclosure, and opt-in vs. opt-out requirements with legal and update both layers accordingly — the IVR / system-layer disclosures and the agent-layer self-ID.

## Mis-applications (optimize mode)

- **Pattern: disclosure present but the wording reads as marketing not disclosure.** "Welcome to our AI-powered booking experience!" — uses the word AI but in a promotional register. Compliance audit may not accept this. Reword to direct disclosure ("you're speaking with our automated assistant").
- **Pattern: disclosure on call open but the agent later says "let me check with my team" or similar.** Implies a human team behind the AI. Fix by removing first-person plural references that imply colleagues.
