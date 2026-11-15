# Phase 4b — Vocal identity and casting

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 4b — Vocal identity and casting

Runs after the audit, before the bundle is written, because the casting sides use the rewritten lines. Three steps, recorded in `artifacts/voice-ux/[agent-name]-vocal-identity.md` (template: `templates/vocal-identity-brief.md`):

1. **Vocal Identity brief (H08).** Interpret the Persona for the ear: derivation trace, audience and listening conditions, perceived identity (gender presentation as elicited in Phase 3, age band, accent per locale, pitch zone, voice quality, tempo), perceptual target and must-not-sound-like, expressive range and forbidden effects, the two-voice relation, locale variants, and the name block. No voice IDs or settings. Without a Persona, label the brief `inferred`.
2. **Casting (H09).** Hard filters (locale, model fit, exists in the target org, no static catalog), a shortlist of three from a dated snapshot of the target org's library, casting sides generated from this agent, an audition, and a decision record with a runner-up.
   - The audition channel is recorded. A real phone call is recommended; Builder Preview is acceptable when no number is provisioned, with the caveat that phone rendering may differ.
   - The listener tier is recorded. Minimum one listener; three to five independent listeners recommended for go-live or brand-critical agents.
   - The skill prepares everything up to the listening. Picking the voice in the org library and the listening sign-off are human steps; the skill can't hear the result. Until sign-off, the `voice_id` stays `[review needed]`.
3. **Light tuning (H03).** Model choice, stability band (v3 default 0.5), speed on Flash only, similarity ≥0.75, resting and shift tags on v3 (A08), pauses through punctuation. One parameter at a time, re-auditioning the same casting sides.

**Optimize mode:** write the brief, then audit the voice that's already live against it with the casting sides. Recommend a recast only when the voice clearly mismatches the brief or has a defect.
