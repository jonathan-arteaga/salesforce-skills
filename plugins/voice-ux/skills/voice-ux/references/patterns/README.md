# Pattern catalog

Per-file index of chat→voice migration patterns. Each pattern has a chat example, a recommended voice example, and at least one alternative.

This catalog is the **operational** source of truth used by the audit (Phase 4) and rewrite (Phase 5). The principle reference (`../voice-ux-principles.md`) is the **theoretical** source — patterns cite back to it.

## How the skill uses this catalog

1. **Phase 2 — extraction:** Skill loads only this `README.md` (cheap). Walks each pattern's `detection` block, scanning the source `.agent` and sample. Records hits.
2. **Phase 4 — audit:** Skill loads the body of each *hit* pattern (full content) and applies it. Patterns it didn't hit don't load.
3. **Phase 5 — rewrite:** Skill applies patterns in the order in `## Application order` below.
4. **Phase 6 — hand-back:** Findings cite both the pattern ID (e.g., `A01`) and the principle / telephony-pattern ID (e.g., `P9-end-focus`, `T-translate-6`).

Optional Phase 7/8 (`.agent` generation + publish-with-self-healing) consume the same catalog.

## Categories

| Code | Category | Patterns |
|---|---|---|
| A | system-instructions | A01–A12 |
| B | welcome-and-static | B01–B04 |
| C | display-formatting | C01–C05 |
| D | input-collection (spell-confirm) | D01–D09 |
| E | output-presentation | E01–E04 |
| F | crisis-and-safety | F01–F03 |
| G | latency-masking | G01–G03 |
| H | configuration | H01–H09 |
| I | variables | I01–I02 |
| J | flow-control | J01 |
| Z | lint (pre-emptive, run before pattern application) | Z01–Z08 |

## Pattern index

| ID | Name | Severity | Modes | Couples with |
|---|---|---|---|---|
| A01 | numbered-list-rule | high | migrate, optimize | E01, C02 |
| A02 | confirmation-rule | medium | migrate, optimize | — |
| A03 | numeric-input-as-yes-no | low | migrate | — |
| A04 | one-question-per-turn | high | migrate, optimize | E02 |
| A05 | congratulatory-language-ban | medium | migrate, optimize | — |
| A06 | currency-spoken-form | high | migrate, optimize | I01 |
| A07 | slot-selection-collapse | medium | migrate | E01 |
| A08 | tone-tags-and-expressivity | medium | migrate, optimize | H03, A09 |
| A09 | contractions-and-cadence | medium | migrate, optimize | A08, A10, B02 |
| A10 | agent-self-reference | medium | migrate, optimize | B02, A09 |
| A11 | no-unscripted-commitments | high | migrate, optimize | G02, A10 |
| A12 | times-and-dates-spoken-form | medium | migrate, optimize | I01, A06, D03 |
| B01 | welcome-length | high | migrate, optimize | B02 |
| B02 | welcome-ai-disclosure | high | migrate, optimize | B01, A10 |
| B03 | error-message-voice-readable | medium | migrate, optimize | C01, C03 |
| B04 | pre-chat-variable-interpolation | high | migrate | H02 |
| C01 | html-tags-in-spoken-content | high | migrate | — |
| C02 | markdown-in-spoken-content | high | migrate | — |
| C03 | interface-verbs | high | migrate, optimize | — |
| C04 | url-read-aloud | high | migrate, optimize | E03 |
| C05 | chat-ui-references | high | migrate | — |
| D01 | postcode-collection | high | migrate, optimize | — |
| D02 | name-spell-back | high | migrate | — |
| D03 | date-of-birth | high | migrate, optimize | I01 |
| D04 | phone-number | high | migrate, optimize | D06 |
| D05 | email-address | medium | migrate | D07, D08 |
| D06 | reference-numbers | medium | migrate | D07 |
| D07 | hard-to-capture-identifiers | medium | migrate, optimize | D02, D04, D05, D06, D08 |
| D08 | type-dont-say-capture-handoff | medium | migrate, optimize | D05, D07 |
| D09 | pii-masking-in-prose | high | migrate, optimize | D04, D06, E02 |
| E01 | slot-list-presentation | high | migrate, optimize | A01 |
| E02 | summary-readback | high | migrate, optimize | A04 |
| E03 | long-static-messages | high | migrate, optimize | C04 |
| E04 | speciality-list-enumeration | medium | migrate, optimize | — |
| F01 | crisis-flow-no-hangup | high | migrate, optimize | — |
| F02 | red-flag-symptom-checklist | high | migrate, optimize | — |
| F03 | sensitive-flag-redaction | high | migrate, optimize | F01 |
| G01 | progress-message-required | high | migrate, optimize | — |
| G02 | pre-action-narration | medium | migrate, optimize | G03 |
| G03 | live-lookup-narration | medium | migrate, optimize | G01, G02 |
| H01 | modality-and-connection-blocks | high | migrate | I01, H03 |
| H02 | strip-pre-chat-seeding | high | migrate | B04 |
| H03 | voice-settings | high | migrate | H01, A08 |
| H04 | pronunciation-dictionary | medium | migrate, optimize | — |
| H05 | key-term-prompting | medium | migrate, optimize | — |
| H06 | voice-latency-and-turn-timing | high | migrate, optimize | H01, H03, G01 |
| H07 | barge-in-recovery (experimental) | medium | migrate, optimize | A04, I02 |
| H08 | vocal-identity-brief | high | migrate, optimize | H09, H03, A08 |
| H09 | casting-and-audition | high | migrate, optimize | H08, H03, H04 |
| I01 | spoken-format-companion-variables | high | migrate | A06 |
| I02 | volunteered-slot-capture | high | migrate, optimize | I01, J01 |
| J01 | escalation-budget | high | migrate, optimize | I02 |
| Z01 | description-length-cap (≤255 chars) | high | migrate, optimize | — |
| Z02 | subagent-deprecation (auto-rewrite topic→subagent) | high | migrate, optimize | — |
| Z03 | duplicate-keys (surface, no auto-fix) | high | migrate, optimize | — |
| Z04 | em-dash-in-spoken-prose (auto-fix) | medium | migrate, optimize | A09 |
| Z05 | human-impersonation (auto-fix + flag) | high | migrate, optimize | A09, A10, B02 |
| Z06 | nothing-after-transition (auto-fix; blocks until fixed) | high | migrate, optimize | J01 |
| Z07 | empty-check-none-and-blank (auto-fix) | medium | migrate, optimize | I01, I02, B04 |
| Z08 | no-silent-generative-turn (auto-fix + flag; blocks until fixed) | high | migrate, optimize | D08, H06 |

## Application order

When generating the voice agent (Phase 5 or optional Phase 7), apply patterns in this order so later passes don't overwrite earlier ones:

0. **Pre-emptive lints (Z-class)** — Z01 (description length cap), Z02 (auto-rewrite `topic`→`subagent`), Z03 (surface duplicate keys for developer resolution), Z04 (rewrite em-dashes in spoken prose), Z05 (rewrite human-impersonation instructions and flag each), Z06 (move work that follows a `transition` above it), Z07 (empty checks test both `None` and `""`), Z08 (replace "output nothing" instructions with a holding line). Run BEFORE pattern application. Z01 catches an error class the offline validator doesn't enforce but the org-side compiler does. Z02/Z03/Z06 catch warnings the offline validator emits — Z02 and Z06 auto-fix, Z03 blocks hand-back until resolved. Z07 and Z08 catch runtime failures no validator sees. See SKILL.md Phase 7.2.
1. **Configuration** — H01 (strip `additional_parameter__disable_graph_runtime`, add `connection`/`modality voice:`), H02 (strip pre-chat seeding), H08 → H09 → H03 (vocal identity brief, casting, then light tuning of the chosen voice; the brief and casting record are a side artifact, only the resulting `voice_id` and settings land in the `.agent`), H06 (`additional_configs` latency/turn timing), H05 (`inbound_keywords` STT bias).
2. **Variables** — I01 (add spoken-format companions), I02 (volunteered-slot capture action + slot set).
3. **System instructions (global)** — A01–A12, B01–B04, H07 (barge-in recovery rule), D09 (never-say-in-full PII rule). (A08 tone tags, A09 contractions/cadence, and A10 self-reference are global register rules; A08 is gated to the v3 model set in step 1 — see H03.)
4. **Per-topic system instructions** — A01–A05 reapplied at topic scope.
5. **Per-topic reasoning instructions** — D, E, F, G categories. Within D, consult D07 (the hard-identifier decision ladder) *before* the field-specific D02/D04/D05/D06, and design any D08 type-don't-say handoff where the capture turn lives. G03 (live-lookup narration) applies to read/lookup turns here; G01 action-level progress messages come at step 6.
6. **Action definitions** — G01 (`progress_indicator_message`).
7. **Flow-control guarantees** — J01 (unclear-turn flag + deterministic `after_reasoning` increment and escalation guard + handover subagent). Applied after instructions and actions exist, so the guard's `transition to` target and the flag's `setVariables` action are already present.
8. **Strip chat-isms (final pass)** — C01–C05 over every user-visible string.
9. **Final Z-class re-lint** — Z01 sanity check in case patterns introduced new long descriptions; Z03 re-check in case an Edit introduced a new duplicate key; Z04 re-check in case a pattern introduced a spoken em-dash; Z05 re-check in case a rewrite reintroduced a body-sound tag or filler. Z06/Z07 re-check over every block the skill wrote (J01 guards, I01/I02 checks, after-speech `run` lines); Z08 re-check in case a D08 wait was written as a silent turn. (Z02 is one-shot — once `topic` is gone it can't reappear.)

Patterns with `applies_after:` frontmatter override the default order locally.

## CRITICAL: Per-topic action declarations are NOT duplicates

Each `topic`'s `actions:` block is **scoped** — actions referenced in that topic's `reasoning.instructions` MUST be declared in that topic's `actions:` block. If two topics both call `Validate_Postal_Code`, the action MUST be declared in BOTH topics' `actions:` blocks. Do NOT deduplicate during voice migration. Removing a "duplicate" action declaration breaks publish.

## Coupling

Patterns that cite each other in `couples_with:` should be presented as a group in the findings report. Example: A01 (numbered-list-rule) almost always couples with E01 (slot-list-presentation) — finding one without the other is a bug. Phase 4 surfaces them together: "you have 8 findings clustered around list presentation — apply as a set, or walk through?"

## Adding a pattern

See `_schema.md` for the file format and contribution flow. Every new pattern must include:
- A chat example from a real or representative `.agent` source (never invented).
- A recommended voice example with concrete spoken words.
- At least one alternative.
- A fixture in `tests/fixtures/` exercising the pattern.
