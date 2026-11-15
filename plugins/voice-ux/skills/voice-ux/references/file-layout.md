# File layout

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## File layout

```
voice-ux/
├── SKILL.md                              # This file
├── references/
│   ├── voice-ux-principles.md            # 14 principles (P1–P14) + mis-applications
│   ├── telephony-patterns.md             # T-translate, T-grounding, T-repair, T-latency, T-phrasebook, T-opening + mis-applications
│   ├── audit-rubric.md                   # Coverage contract, mis-application checks, mode-dependent conflict policy, mode-detection signals
│   ├── stakeholder-html-artifact.md      # Patterns for the optional interactive HTML summary (Phase 9) — inspiration, not a template
│   ├── patterns/                         # Per-file pattern catalog — concrete chat→voice patterns with worked examples
│   │   ├── README.md                     # Index, application order, coupling rules
│   │   ├── _schema.md                    # Frontmatter spec + body section requirements + lint rules
│   │   ├── A01-numbered-list-rule.md
│   │   ├── A02-confirmation-rule.md
│   │   ├── A03-numeric-input-as-yes-no.md
│   │   ├── A04-one-question-per-turn.md
│   │   ├── A05-congratulatory-language-ban.md
│   │   ├── A06-currency-spoken-form.md
│   │   ├── A07-slot-selection-collapse.md
│   │   ├── A08-tone-tags-and-expressivity.md
│   │   ├── A09-contractions-and-cadence.md
│   │   ├── A10-agent-self-reference.md
│   │   ├── B01-welcome-length.md
│   │   ├── B02-welcome-ai-disclosure.md
│   │   ├── B03-error-message-voice-readable.md
│   │   ├── B04-pre-chat-variable-interpolation.md
│   │   ├── C01-html-tags-in-spoken-content.md
│   │   ├── C02-markdown-in-spoken-content.md
│   │   ├── C03-interface-verbs.md
│   │   ├── C04-url-read-aloud.md
│   │   ├── C05-chat-ui-references.md
│   │   ├── D01-postcode-collection.md
│   │   ├── D02-name-spell-back.md
│   │   ├── D03-date-of-birth.md
│   │   ├── D04-phone-number.md
│   │   ├── D05-email-address.md
│   │   ├── D06-reference-numbers.md
│   │   ├── D07-hard-to-capture-identifiers.md
│   │   ├── D08-type-dont-say-capture-handoff.md
│   │   ├── D09-pii-masking-in-prose.md
│   │   ├── E01-slot-list-presentation.md
│   │   ├── E02-summary-readback.md
│   │   ├── E03-long-static-messages.md
│   │   ├── E04-speciality-list-enumeration.md
│   │   ├── F01-crisis-flow-no-hangup.md
│   │   ├── F02-red-flag-symptom-checklist.md
│   │   ├── F03-sensitive-flag-redaction.md
│   │   ├── G01-progress-message-required.md
│   │   ├── G02-pre-action-narration.md
│   │   ├── G03-live-lookup-narration.md
│   │   ├── H01-modality-and-connection-blocks.md
│   │   ├── H02-strip-pre-chat-seeding.md
│   │   ├── H03-voice-settings.md
│   │   ├── H04-pronunciation-dictionary.md
│   │   ├── H05-key-term-prompting.md
│   │   ├── H06-voice-latency-and-turn-timing.md
│   │   ├── H07-barge-in-recovery.md
│   │   ├── H08-vocal-identity-brief.md
│   │   ├── H09-casting-and-audition.md
│   │   ├── I01-spoken-format-companion-variables.md
│   │   ├── I02-volunteered-slot-capture.md
│   │   ├── J01-escalation-budget.md
│   │   ├── Z01-description-length-cap.md
│   │   ├── Z02-subagent-deprecation.md
│   │   ├── Z03-duplicate-keys.md
│   │   ├── Z04-em-dash-in-spoken-prose.md
│   │   └── Z05-human-impersonation.md
│   └── publish-errors/                   # Known sf agent publish errors and canonical fixes (for optional Phase 8)
│       ├── README.md
│       ├── E001-locale-restricted-picklist.md
│       ├── E002-invocation-target-restricted-picklist.md
│       ├── E003-bundle-meta-filename.md
│       ├── E004-disable-graph-runtime-legacy-builder.md
│       └── E005-cli-retrieve-undefined-target.md
└── templates/
    ├── rewrite-bundle.md                 # Output skeleton — Phase 5 bundle (Layers A–E, mode-aware)
    ├── pronunciation-dictionary.md       # Output skeleton — generated when H04 detected (Phase 7)
    ├── key-term-prompting.md             # Output skeleton — generated when H05 detected (Phase 7)
    ├── vocal-identity-brief.md           # Output skeleton — brief, casting sides, audition, decision record (Phase 4b)
    └── v1-review-checklist.md            # Output skeleton — V1 review items, annotated per migration (Phase 7)
```
