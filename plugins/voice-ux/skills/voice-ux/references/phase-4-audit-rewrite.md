# Phase 4 — Audit + Rewrite

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 4 — Audit + Rewrite

Run the audit per `references/audit-rubric.md` AND `references/patterns/`. The rubric is the **abstract** contract (principle-by-principle coverage); the patterns folder is the **operational** source (concrete chat-example + voice-example + alternatives per detected pattern).

**Pattern loading is lazy:** Phase 2 extraction loads only `references/patterns/README.md` (the index) and walks each pattern's frontmatter `detection:` rules against the source. For each hit, Phase 4 loads the full pattern body to apply it. Patterns that don't hit don't load — keeps token cost in check.

For each row in the rubric / each hit pattern, produce one of:

- `[changed]` — voice principle violated or absent, rewrite applied
- `[ok]` — principle already respected (counts in summary, not surfaced inline)
- `[review needed]` — voice principle violated AND original logic shows intentionality signal; preserve original, flag conflict
- `[consider]` *(optimize mode only)* — principle present but applied weakly; suggestion, no rewrite, no preservation
- `[out-of-scope]` — pattern detected that source library doesn't cover

### Conflict policy (mode-dependent; load-bearing, do not override)

**Persona precedence when a Persona is supplied:** Preserve its exact Never-Say entries, immutable spans/response shape, Lexicon meaning, explicit Guardrails, Identity, Register, Tone boundaries, and Tone Flex semantics. Voice adaptation may shorten, chunk, or expand spoken variants only inside that contract. Any proposed character change is `[review needed]`; never silently rewrite it. Persona Tone Flex continues to own situational word choice and response patterns. P5/A08 maps the same triggers and resets to prosody without redefining them.

**Voice floors the Persona can't lower.** Two rules hold even against a supplied Persona, and each conflict is surfaced, never resolved silently:
- **A10, no first-person feelings.** If the Persona licenses feelings (Personification = Anthropomorphic), apply A10 and log `[review needed]` with the reason: a human-sounding voice amplifies anthropomorphism far beyond the same words in text.
- **B02/Z05, AI disclosure and no human impersonation.** A brand preference to hide the AI, or an instruction to pass as human, is `[review needed]` and goes to legal.

**Welcome ownership.** The Persona owns the welcome's wording and register. This skill owns its spoken structure (system/agent split, 5–7s budget, disclosure placement, CTA last). Re-chunking or shortening is fine; a change in meaning is `[review needed]` (B01).

The existing Script remains authoritative for business logic, action contracts, routing, and source-carried compliance. A conflict between Script compliance/immutable content and `persona.md` is `[review needed]` and blocks that span until the user resolves source authority.

**Strong intentionality signals** (preserve in BOTH modes):
- Explicit compliance/regulatory language ("PCI", "GDPR consent", "must record", "required by")
- Comment marking the directive as fixed
- Bundled question that asks for items legally bound together

**Weak intentionality signals** (preserve in MIGRATE only; flag in OPTIMIZE):
- Repeated assertion of the same rule across multiple turns
- Pattern repeated across topics

**No intentionality signal:** rewrite as `[changed]` in both modes.

The bar shift: in migrate mode, "the designer probably knew what they were doing" is the working assumption. In optimize mode, "the designer wants my opinion" is the working assumption.

### Optimize-mode-specific check class

Optimize mode adds **mis-application checks** (see `audit-rubric.md` for the full table): principle is present but applied wrong. Examples:
- P10-mis-1: Repair tier 2 prompt is identical/near-identical to tier 1 → `[consider]`
- P11-mis-1: Phrasebook has fewer than 3 tokens per function → `[consider]`
- P2-mis-1: Grounding policy treats phone/email/money as low-stakes → `[changed]`
- T-opening-mis-1: Two-voice opening system and agent layers don't sound clearly different → `[changed]`

Run mis-application checks in migrate mode too — they usually return `[ok]` (the principle isn't there to be mis-applied), but they catch half-migrated scripts.
