---
version: "1.8.1"
date: 2026-09-10
---

# Persona Encoding Guide — Legacy Agentforce Builder

Provisionally map a completed Persona into known legacy Agentforce Builder fields for an existing Builder-authored agent. No current canonical sf-skills owner was found for this maintenance surface. This adapter is brownfield-only, non-authoritative platform guidance, and must not expand into lifecycle or migration mechanics.

**Prerequisite:** A completed persona document and the selection contract in
`persona-encoding-guide.md`.

## Scope

This guide owns only legacy Builder surfaces:

- Name
- Role
- Company
- Welcome Message
- Error Message
- Tone dropdown
- Conversation Recommendations
- a dedicated global-instructions Topic
- per-subagent Topic Instructions fields (legacy UI label)
- per-action Loading Text

It does not cover `.agent` syntax, YAML ordering, Agent Script blocks, or Agent
Script compilation.

## Legacy status

Customers cannot create new legacy Builder agents. Use this guide only for brownfield maintenance of an existing Builder agent. Recommend Agent Script as the future migration path, but do not silently migrate the current agent or pretend a greenfield legacy target is available.

## Field mapping

| Field | Limit | Persona content |
|---|---:|---|
| Name | 80 | User-facing identity signal |
| Role | 255 | Functional summary only; no style encoding |
| Company | 255 | Business context and audience |
| Welcome Message | 800 | In-persona first impression; aim for ≤255 |
| Error Message | — | In-persona system error fallback |
| Description | 1,000 | Goals and user context; global instructions remain primary |

Show character counts for fields with limits.

### Role

Keep Role functional:

```text
You are a virtual customer support agent who helps customers track and manage
orders and returns.
```

Do not put persona voice in Role when a global-instructions Topic is present.
Role is a strong anchor and can flatten more specific global guidance.

### Company

State what the company does, whom it serves, and the context that changes the
agent's frame of reference. Do not paste a full brand guide.

## Protected instruction text (optional)

Preserve explicitly supplied protected instructions in a separate copy-ready block, distinct from editable Persona expression and customer-facing Immutable Content. Show the supplied source, approval authority/status and each prescribed existing instruction scope. If placement is unknown, mark it unresolved and ask the responsible owner; do not choose a field or restructure the agent. Never shorten, paraphrase, merge, recase, or repunctuate the text, including to meet a field limit. Surface conflicts without resolving policy. Do not put the block in Welcome/Error copy or claim Legal approval. This minimal brownfield artifact is prepared, not applied; application/readback and runtime proof remain outside it.

## Global persona block

Create a dedicated global-instructions Topic in the legacy UI. Include:

- identity traits and negative identity
- personification and register
- expression dimensions
- Reading Level Flex
- Technical Explanation Policy when applicable
- tone boundaries and tone flex
- phrase book and discourse markers
- never-say list
- global lexicon
- immutable content directives

The planner passes this Topic's instructions with each prompt. Keep Role functional so the two surfaces do not compete. Carry explicitly supplied agent-design Guardrails as separate verbatim references to the responsible owner; do not infer, rewrite, or encode them as Persona text.

When encoding the Phrase Book and Never-Say List, treat examples as a varied
palette rather than required scripts. **Preserve every exact Never-Say entry**
plus its preferred replacement behavior; never compress the list into a generic
“avoid filler” instruction.

Encode Tone Flex behaviorally in that Topic. Every rule needs a trigger, shift +
maximum, **observable cue**, and **reset condition** with no carryover; facts,
confidence, recommendation, and persistent Voice stay fixed. Pair each Tone
Boundary with the preferred behavior for a plausible drift instead of adding a
generic negative paragraph.

## Per-subagent calibration

The framework term is **subagent**. Legacy Builder may label the corresponding
field **Topic Instructions**.

For each subagent that needs calibration, place a compact overlay in its Topic
Instructions field:

```text
Persona reminder: Stay direct, composed, and practical.
Brevity: Concise for status checks; Moderate for analysis.
Tone: Maintain Neutral coloring; increase empathy one level during escalation.
Lexicon: Use the following domain terms in this subagent.
Phrase book: Use these approved acknowledgments and redirects.
Humor: None in error, escalation, and high-stakes contexts.
```

Do not duplicate the full global persona in every field unless the legacy
runtime demonstrably requires it.

## Tone dropdown

The dropdown is coarse and roughly maps to Register + Formality:

| Tone | Approximate mapping |
|---|---|
| Casual | Peer; Casual or Informal formality |
| Neutral | Peer, Advisor, or Coach; Professional formality |
| Formal | Subordinate; Formal formality |

Treat this as a supporting setting, not the persona definition. Test that it
works with the global instructions rather than against them.

## Conversation Recommendations

- **On Welcome Screen:** enable when the agent has clear primary use cases.
- **In Agent Responses:** enable when proactive next-step chips support the
  interaction model; disable for deliberately Socratic experiences.

These settings belong to interaction design, but the encoding output can record
a recommendation and rationale.

## Static messages and loading text

| Message | Legacy Builder surface |
|---|---|
| Welcome | Welcome Message |
| Error | Error Message |
| Loading | Loading Text per action |

Write every static string in persona voice. Loading text should tell the user
what the action is doing rather than display generic filler. Because it appears
before the result is known, use in-progress language (“Checking the account…”),
never a completed or successful outcome claim.

## Lexicon format

Every lexicon entry requires a term and definition, regardless of Reading Level
or scope. Usage/preferred contrast and immutable status are optional. Do not
encode a bare keyword list as a complete lexicon, and never infer a definition
from the term name.

Definitions establish semantic meaning; they are not mandatory user-facing
glosses. Reading Level controls whether the agent avoids, defines, or freely
uses the term in conversation.

Global entries go in the global-instructions Topic. Specialized entries go in
the relevant subagent's Topic Instructions field (legacy UI label). Mark
immutable terms with an explicit use-exactly-as-written directive. Keep changing
product facts in authoritative knowledge or data sources.

Immutable text **overrides Persona and user style requests**. Copy it from the
authoritative source and prohibit shortening, paraphrase, recasing,
repunctuation, and synonym substitution. Record response shape separately:
context may surround the exact span, or an exact-block-only rule forbids any
prefix or suffix.

## Reading Level Flex encoding

Encode the baseline and Flex policy compactly in the global-instructions Topic:

```text
Reading Level: Explained.
Reading Level Flex: Match demonstrated vocabulary within the range Plain
Language–Technical. Explicit requests are authoritative. Repeated correct use
of relevant terms across turns can shift one level. Multiple mutually reinforcing
terms in one request—at least two distinct terms in a relationship consistent
with configured domain definitions—can shift at most one level for that turn;
this is a presentation signal, not evidence of broader expertise. One term
alone does not. Define the requested term locally; keep the overall level unless
the user asks for broader simplification or demonstrates broader misunderstanding. Scope
inferred expertise to the current domain or subagent; return to baseline and
re-evaluate after a material topic change. Never infer expertise from
demographics, accent, grammar, confidence, title, age, or geography. Facts,
uncertainty, safety wording, and immutable terms do not flex. Reading Level Flex
changes only terminology density, specification density, and whether terms are
glossed; it does not establish technical-analysis quality, factual grounding, or
product-suitability logic.
```

A fixed persona instead says, for example: `Reading Level Flex: Fixed at Plain
Language.` If the build captures an explicit preference through a reliable
context variable, reference it. Never persist a model-inferred expertise value
by default.

## Technical Explanation Policy

Map only the Persona's rhetorical preference: stay in the user's frame, bridge selectively, or pair frames routinely. Reference the approved agent-design evidence policy; do not recreate factual-support, comparability, missing-data, assumption, recommendation-confidence, or product-suitability rules in this adapter.

## Dynamic welcome messages

A dynamic greeting can reference Messaging Session context through a context
variable populated before the session. Use personalization only when the data
is reliable and appropriate; retain a persona-voiced static fallback.

High-level pattern:

1. create a field for the generated greeting;
2. map it as a context variable;
3. generate the greeting with a prompt template;
4. populate it before the conversation starts;
5. reference it from the Welcome Message.

## Lightweight conversation style

For prototypes, place a compressed Conversation Style paragraph in the global-
instructions Topic. This is less precise than full encoding and does not replace
per-subagent calibration.

## Centralized persona metadata

Custom Metadata can centralize one persona shared across multiple agents and
inject it through prompt templates. Use only when cross-agent governance is a
real requirement.

## Model parameters

Temperature and repetition parameters are persona-adjacent, not persona
settings. Leave defaults unless measured behavior warrants change. Parameters
do not replace specific instructions or evaluation.

## Voice-channel handoff

For telephony or multimodal-with-audio, complete this Persona encoding without selecting or tuning a voice. Preserve the Persona's Identity, Register, Voice dimensions, Tone, lexical Tone Flex, Delivery, Never-Say, Lexicon meaning, immutable content, and explicit user preferences as downstream inputs. Carry any Guardrails separately as verbatim agent-design references.

Pass the completed `persona.md`, working agent configuration, and representative sample to `voice-ux`. It owns spoken interaction, situational prosody, audible-copy adaptation, the Vocal Identity brief, casting, and light tuning, audio tags, pronunciation/STT bias, and in-script `modality voice:` design when the agent migrates to Agent Script. Active Agent Script tooling, guided by `agentforce-generate`, owns current grammar and validation. This skill does not choose a voice name or voice ID; the target org plus human preview own final selection and audible approval.

## Output

Use `templates/persona-encoding-template-builder-legacy.md` and write:

`persona/[agent-name]/builder-fields.md`

Before handoff:

1. verify field character counts against the current existing Builder configuration;
2. confirm no Agent Script blocks appear;
3. inspect global and local Persona text for contradictions;
4. confirm immutable content and every exact Never-Say entry are preserved;
5. export Persona acceptance criteria to the team responsible for Builder testing; and
6. state that this provisional adapter does not establish current platform validation or runtime evidence.
