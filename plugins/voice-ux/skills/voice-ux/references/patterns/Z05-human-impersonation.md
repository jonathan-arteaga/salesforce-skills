---
id: Z05
name: human-impersonation
category: lint
severity: high
applies_to: [migrate, optimize]
couples_with: [A09, A10, B02]
detection:
  - regex: '(?i)\byou are (a|an) (real )?(human|person)\b'
    in: [instructions, system.instructions]
  - regex: '(?i)(believe|think|feel like)s? (they|that they|the (caller|customer|user|attendee)) (is|are|\x27re) (talking|speaking) (to|with) (a )?(real )?(human|person)'
    in: [instructions, system.instructions]
  - regex: '(?i)(never|don\x27t|do not) (say|mention|reveal|admit|disclose)[^.]{0,40}\b(AI|bot|automated|virtual|artificial)'
    in: [instructions, system.instructions]
  - regex: '\[(laughs?|chuckles?|giggles?|exhales?|sighs?|inhales?|breathes?|clears throat)\]'
    in: [instructions, system.instructions, response_templates, welcome]
  - regex: '(?i)\b(uhm|umm?|uh|erm)\b'
    in: [instructions, system.instructions, response_templates]
  - structural: "instructions set a human-likeness target (e.g. '80% human-like', 'indistinguishable from a person')"
    in: [instructions, system.instructions]
principle_refs: [P4, P11]
---

# Human impersonation

## Why it matters

Naturalness is the goal; passing as human isn't (A09). Some prompt guides, including internal enablement material, still tell voice agents to be human: "You are a human", "so the caller believes they're talking to a real person", "never say you're an AI unless asked", scripted `uhm`s, `[laughs]`, `[exhales]`, and claimed feelings. On a modern TTS voice those instructions work, which is the problem. The voice amplifies anthropomorphism: the same words that read as a friendly chatbot in text sound like a person on the phone. That breaks AI-disclosure rules in many jurisdictions (B02) and the caller's trust the moment they find out.

This lint runs before pattern application, like Z01–Z04, because these lines usually arrive in the source prompt and quietly undermine A09, A10, and B02 if they survive.

## Detection

Flag any of these in instructions, response templates, or the welcome:
- An identity claim: "You are a human", "you are a real person".
- A belief goal: "so the caller believes they're talking to a real person".
- A disclosure dodge: "never say / don't reveal you're an AI", "only admit it if asked".
- A human-likeness target: "≥80% human-like", "indistinguishable from a person".
- Simulated body sounds or presence: `[laughs]`, `[chuckles]`, `[sighs]`, `[exhales]`, `[clears throat]`; "pretend to type", "say you're grabbing a coffee".
- Scripted disfluency in agent output: `uhm`, `umm`, `erm` written into lines the agent speaks. (Not a hit: `inbound_filler_words_detection`, which is about the *caller's* fillers, H05.)
- Claimed first-person feelings (cross-check A10).

## Where it lives

- Scans `system.instructions`, topic `reasoning.instructions`, response templates, `messages.welcome`, and any persona prompt pasted into them.
- **Auto-fix, then flag.** Rewrite each hit by meaning, and log it as `[review needed]` with the reason, since the source author may have had a client request behind it:
  - Identity claim / belief goal / likeness target → "Speak like a thoughtful person on a relaxed phone call. Sound natural, not human." (A09)
  - Disclosure dodge → the plain-answer rule from A10 and the opening disclosure from B02.
  - Body-sound tags → remove. Warmth goes through the allowed v3 tags instead (`[warm]`, `[reassuring]`, A08).
  - Scripted fillers → remove. Natural rhythm comes from contractions and short sentences (A09).
  - Claimed feelings → A10.
- **Does not block hand-back,** but every hit appears in the audit with its rewrite. If the client insists on keeping a hit, that is a legal and trust decision, not a voice-UX one. Route it to them in writing and leave the `[review needed]` open.
- **A Persona that licenses feelings** (Personification = Anthropomorphic) doesn't switch this off. Feelings are A10's floor-and-flag case; impersonation of a human is never licensed.
