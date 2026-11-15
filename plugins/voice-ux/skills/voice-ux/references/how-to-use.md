# How to Use

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## How to Use

This skill takes an Agentforce Agent Script and applies voice UX expertise to it. Two modes:

- **Migrate mode** — source is a text-based Script. Output is a voice-optimized rewrite.
- **Optimize mode** — source is an existing voice Script. Output is an improved voice Script with weak applications of voice principles flagged and (where unambiguous) fixed.

Mode is auto-detected from extraction signals (text-shaped vs. voice-shaped patterns in the source) and confirmed with the developer. The output bundle is the same shape in both modes; the audit content differs.

**What it produces:**
- A migration/optimization bundle (`artifacts/voice-ux/[agent-name]-voice-{migration,optimization}.md`) with five labeled layers (instructions, copy, phrasebook, opening, out-of-script notes) plus inline audit
- Optionally (Phase 9): a self-contained interactive HTML summary (`artifacts/voice-ux/<api_name>-voice-summary.html`) for communicating the changes to stakeholders

- A vocal identity file (`artifacts/voice-ux/[agent-name]-vocal-identity.md`): the Vocal Identity brief, casting sides, audition scores, and the casting decision with a runner-up (Phase 4b)

**What it does not do:** Build voice agents from scratch. Design the agent's character or lexical Tone Flex policy. Run runtime QA. Configure external carrier, IVR, TTS-vendor, or ASR-vendor setup. In-script `modality voice:` design remains in scope. It does not generate non-English copy.
