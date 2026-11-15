---
version: "1.2.0"
date: 2026-09-03
---

# [Agent Name] — Provisional Legacy Builder Persona Mapping

**Target:** Existing legacy Agentforce Builder agent only
**Authority note:** Provisional Persona-field adapter; current platform behavior requires separate validation
**Channel:** [web chat / mobile chat / SMS / email / telephony / multimodal-with-audio / embedded / other]
**Date:** [date]
**Source persona:** [agent-name]-persona.md

## Encoding Invariants

- Preserve every approved exact Never-Say entry as an explicit prohibition with
  its preferred replacement behavior; never reduce the list to a generic “avoid
  filler” rule.
- Preserve immutable content and its declared surrounding response shape.
- Persona changes expression only; export the acceptance criteria below to the team responsible for legacy Builder validation.

## Agent Configuration Fields

| Field | Limit | Value | Chars |
|---|---:|---|---:|
| **Name** | 80 | [agent name] | [count] |
| **Role** | 255 | [functional summary only; no persona style] | [count] |
| **Company** | 255 | [company context] | [count] |
| **Welcome Message** | 800 | [persona welcome; aim ≤255] | [count] |
| **Error Message** | — | [persona error] | — |

## Builder Settings

| Setting | Recommendation | Rationale |
|---|---|---|
| **Tone** | [Casual / Neutral / Formal] | [Register + Formality mapping] |
| **Conversation Recs on Welcome** | [On / Off] | [rationale] |
| **Conversation Recs in Responses** | [On / Off] | [rationale] |

## Global Persona Block

*Place in a dedicated global-instructions Topic in the legacy UI.*

```text
[Identity, dimensions, Reading Level Flex, rhetorical Technical Explanation preference (when applicable), Phrase Book, Tone Boundaries, Tone Flex, Never-Say List, Global Lexicon, and Immutable content directives. Keep agent-design Guardrails as verbatim handoff references rather than Persona text.]
```

## Immutable Terms

| Term | Type | Usage |
|---|---|---|
| [term] | [brand / legal] | [use-exactly-as-written rule] |

## Protected Instruction Text *(optional)*

*Include only explicitly supplied blocks. This copy-ready payload is prepared, not applied. These are internal instructions, not words to speak to the customer. Omit when none is supplied.*

- **Block ID:** [PI-01]
- **Source:** [supplied reference or unknown]
- **Approval authority / status:** [supplied or unknown]
- **Supplied instruction placement(s):** [existing scope(s) or unresolved; do not invent]

```text
[Complete exact supplied instruction block; keep metadata outside it.]
```

*Do not trim a protected block to fit a field limit. Report the limit conflict or unresolved placement for the responsible owner. Do not rewrite, redistribute or silently deduplicate prescribed placements.*

## Per-Subagent Persona Instructions

*Legacy Builder UI label: Topic Instructions.*

**[Subagent Name / legacy Topic label]:**

```text
Persona reminder: [global identity reminder]
Brevity: [subagent calibration]
Tone: [tone-flex shift]
Reading Level: [baseline + fixed/adaptive Flex policy]
Technical explanation: [subagent-specific bridge guidance, if any]
Lexicon: [subagent terms and definitions]
Phrase book: [relevant situational phrases]
Humor: [context guidance]
```

## Loading Text

| Action | Loading Text |
|---|---|
| [action name] | [in-character loading text] |
| Generic fallback | [in-character loading text] |

## Downstream acceptance handoff

- Preserve supplied facts, statuses, uncertainty, and permitted recommendations.
- Preserve action, routing, and capability ownership from the existing agent.
- Preserve exact Never-Say and immutable content.
- Hand these criteria to the team responsible for legacy Builder testing; do not claim runtime proof in this artifact.

## Character-Count Review

- [ ] Name ≤80
- [ ] Role ≤255 and functional only
- [ ] Company ≤255
- [ ] Welcome ≤800 (aim ≤255)
- [ ] No Agent Script blocks or syntax appear in this output
