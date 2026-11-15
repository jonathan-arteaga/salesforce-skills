# When to Use This Skill

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## When to Use This Skill

- **Migrate:** Migrating a working text-based Agentforce Agent Script to voice (telephony or voice-over-web). Auditing a chat-based agent for voice UX issues without committing to a full rewrite.
- **Optimize:** Reviewing an existing voice Agent Script for voice UX quality. Catching mis-applied voice principles (repair tier 2 identical to tier 1, phrasebook with too few tokens, grounding policy treating phone numbers as low-stakes). Preparing a voice script for stakeholder review or handoff.

**Scope boundary:** This skill adapts what the agent says and how it behaves for listening and speaking. It preserves the Persona character contract while making copy speakable, casting and tuning a voice for the character, and mapping Persona Tone Flex to situational prosody. It does not redesign identity, linguistic Voice, Tone Flex semantics, topic structure, actions, routing, or business logic. If a request such as “make it warmer” is ambiguous, ask one disambiguation question: words/stance belong to `persona`; audible delivery belongs here; if both, finish Persona first. It does design and write in-script `modality voice:` values. External carrier, IVR, TTS-vendor, and ASR-vendor setup remains a Layer E handoff.
