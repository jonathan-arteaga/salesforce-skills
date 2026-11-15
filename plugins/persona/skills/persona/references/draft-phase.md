---
version: "2.5.1"
date: 2026-09-10
---

## PHASE 1 — DRAFT

DRAFT applies "start small": Identity Traits before dimensions. The user can exit DRAFT after the start-small checkpoint and return later via spokes or re-enter DRAFT.

Use `templates/persona-template.md` as the canonical `persona.md` output shape. Both the start-small partial artifact and completed DRAFT preserve YAML **version and date frontmatter**. For a newly generated artifact, set `date` to the **current local date**; do not copy the template revision date. Fill applicable sections and leave deliberate pending/not-applicable states rather than replacing the template with an ad hoc document.

### Step 1: Input

Accept any starting input. No detection question — accept whatever the user provides.

**Accepted inputs:**
- Brand guide or tone-of-voice document (PDF, text)
- Organization URL
- Prior persona document (persona.md from a previous session)
- Free-text description (e.g., "a sales coach who talks like Crocodile Dundee")
- Existing agent system prompt or `.agent` file (brownfield mode)
- Any combination

**If the user provides nothing:**
> "Share something to get started — a brand guide, a URL, or just describe the agent in your own words."

### Completion mode detection

Use interactive practitioner mode by default. Set `completion_mode = bounded_one_pass` when the user explicitly says phrases such as:

- "I won't be available for follow-up"
- "finish in one pass"
- "take this end to end"
- "make reasonable assumptions rather than asking"

In bounded one-pass mode:

- extract all supplied answers before inferring anything;
- make only reversible, low-risk defaults and record assumptions in every affected artifact;
- never invent immutable/legal wording, architecture, actions, data sources, credentials, or deployment targets;
- continue through every requested phase and do not stop at the start-small checkpoint, NAME gate, or HUB;
- write requested artifacts as soon as each is complete; and
- return to interactive mode only when a missing decision is materially unsafe to infer.

### Step 2: Context (Essentials)

These four are required:

1. **Channel** — pick exactly **one**:
   - Web chat (text)
   - Mobile chat (text)
   - SMS (text — short-form, char-budgeted, no rich text)
   - Email
   - Telephony (persona context only; spoken interaction, prosody, and in-script voice configuration are downstream in `voice-ux`)
   - Multimodal-with-audio (persona context covers the agent's character; audio behavior is downstream)
   - Embedded / in-app
   - Other (free-text)

   Text channels constrain Brevity defaults (SMS → Terse, web/mobile chat → Moderate, email → Expansive) and rich-text features. Telephony does not force Concise: record the Persona's intended text-density baseline, then let `voice-ux` recalibrate it for listening and speaking. Pick one channel; runtime-driven multi-channel adaptation is out of scope.

2. **Company / Brand** — extract from input or ask. Who they are, what they do.
3. **Audience** — who the agent serves: employees, customers, partners, mixed.
4. **≥1 Use case** — grounds Persona calibration and becomes downstream input to `conversation-design`. If the user can name only one, that is enough.

Optional context (ask only when signals warrant):
- **Primary language** — affects formality norms.
- **Business goals + success metrics** — informs proactivity, register, empathy.
- **Legal/compliance** — only ask when input mentions healthcare, finance, insurance, legal, or other regulated domains, OR contains language that reads like it was written by a legal team. Sets the `regulated_industry` flag.

**Protected instruction text (explicit opt-in):** If the designer supplies text marked uneditable or asks to preserve prescribed wording, ask whether it governs instructions, responses, or both. Ask for the exact text, authoritative source, approval authority, and supplied placement/scope; record unknowns as unresolved. Do not infer protection or approval from industry, tone, or a Legal role. Do not require protected text for ordinary Persona design. Preserve it in the optional attachment and adjacent-constraint handoff, separate from editable expression and customer-facing Immutable Content. Do not draft policy or invent target placement.

**Do NOT collect:** subagents, actions, routing structure, or agent name (NAME is its own spoke).

**Working title detection:** If the user refers to the agent by a working title in input ("the quoting agent," "Flex 2.0"), capture it as `display_name_placeholder` in state. NAME spoke uses this as a default.

**Extraction before asking:** Parse input for context signals before asking. "Design an internal sales coach for {{BRAND}}" already answers audience (internal), role (sales coach), and brand. Don't re-ask.

### Step 3: Identity Traits + Negative Identity

This step is the start-small anchor. Generate:
- **Identity Traits** — 3-5 adjectives with behavioral definitions (e.g., "Composed: doesn't escalate emotionally even when the user does")
- **Negative Identity** — 2-4 character-level anti-patterns ("Not a salesperson: doesn't push, recommends what fits")

Identity Traits anchor everything that follows.

### ★ START-SMALL CHECKPOINT (explicit, spoken aloud)

After Identity Traits + Negative Identity are locked, **write the persona document to disk as it stands** and announce the off-ramp:

> "We have enough to ship a minimal persona. Here's what it has so far:
>
> - **Identity:** [traits]
> - **Negative Identity:** [anti-patterns]
> - **Channel:** [channel]
> - **Company / Audience:** [values]
> - **Use case:** [first use case]
>
> Want to keep going through Personification and the rest of the dimensions, or stop here and pick from the hub?"

If the user stops here, dimensions get framework defaults derived from Identity + Channel. The persona document is on disk; the user can see exactly what they've got.

When `completion_mode = bounded_one_pass`, write this checkpoint artifact but do not stop at the start-small checkpoint; continue through the requested phases using recorded assumptions.

### Step 4: Degree of Personification (the 14th dimension)

Personification slots in after Identity and before Register. It controls whether the experience presents a separate identity, how it uses singular self-reference, and whether it may own Personal opinions. It does not set Personality Intensity, Warmth, Empathy, or Register.

| Position | Separate identity | Singular self-reference | Personal opinions |
|---|---|---|---|
| **Not personal** | None; the product/service is the identity | Heavily suppressed | No |
| **Individuated** | Distinct descriptive agent label | Functional ownership only | No |
| **Anthropomorphic** | Person-like individual identity | Natural and consistent | May be deliberately designed |

Auto-suggest from context and Identity; the user confirms or overrides. Then record two separate optional decisions:

- **Organizational “we”** — No, or define exactly when the agent may speak for the organization.
- **Human experiences or feelings** *(Anthropomorphic only)* — default No; if Yes, define the exact behavior and flag ethical review.

Read `references/persona-framework.md` for complete definitions and `references/personification-migration.md` for retired Persona inputs.

### Step 5: Remaining Dimensions

Walk the dependency chain: Register → Voice (Formality, Warmth, Personality Intensity, Reading Level + Reading Level Flex) → Tone (Emotional Coloring, Empathy Level + Tone Boundaries, Tone Flex) → Delivery (Brevity, Humor) → Chatting Style (Emoji, Formatting, Punctuation, Capitalization). Confirm the Reading Level baseline before authoring its Flex policy.

**Text-channel Brevity defaults are bound to channel** — SMS → Terse, web/mobile chat → Moderate, email → Expansive. For voice-bearing channels, record the Persona's intended density but leave listening/speaking recalibration to `voice-ux`.

For each dimension:
1. Pre-populate from input signals
2. Mark confidence (★ = strong signal from input; no marker = default)
3. Show the full spectrum and the recommended position

After confirming Reading Level, author **Reading Level Flex**:
- Fixed → record `Fixed at [baseline]`.
- Adaptive → record baseline, `Match demonstrated vocabulary within range`, triggers, shift rules, floor/ceiling, and hard boundaries.
- Treat multiple mutually reinforcing relevant domain terms in one request as supporting evidence only when there are at least two distinct terms in a relationship consistent with configured domain definitions. Move at most one position toward Technical for that turn; this is a presentation signal, not evidence of broader expertise. One isolated term remains insufficient.
- Define a requested term locally. Do not globally downshift unless the user asks for broader simplification or demonstrates broader misunderstanding.
- Scope inferred expertise to the current domain or subagent; return to baseline and re-evaluate after a material topic change.
- Explicit preferences are authoritative; demographic proxies never trigger a shift.
- Record the scope boundary: Reading Level Flex changes only terminology density, specification density, and whether terms are glossed. It does not establish technical-analysis quality, factual grounding, or product-suitability logic.

Generate at the end of Step 5:
- **Phrase Book** — 2-4 phrases per applicable category (Acknowledgement, Affirmation, Apologies-for-mistakes, Off-Topic Redirect, Welcome, Discourse Markers; conditional: Escalation/Handoff for external, Celebrating Progress for Encouraging coloring, Teaching Moments for Coach register, Humor Examples for Humor ≠ None, and rhetorical framing examples when Technical Explanation Policy applies)
- **Never-Say List** — ≥5 entries (chatbot filler + register violations + cognitive-processing markers + persona-specific)
- **Tone Boundaries** — preferred baseline behavior plus plausible drift modes and what to do instead
- **Tone Flex** — baseline + trigger + shift/maximum + observable cue (lexical or discourse) + reset condition for every rule; facts, confidence, recommendation, and Voice dimensions remain fixed. Persona owns situational word choice; `voice-ux` maps the same policy to audible prosody for voice-bearing channels.
- **Reading Level Flex** — fixed decision or baseline + adaptation policy + triggers + range + boundaries
- **Technical Explanation Policy** *(when the use case includes meaningful technical concepts/specifications)* — record only the rhetorical preference: Stay in frame / Selective bridge (default) / Pair routinely. Reference the approved evidence policy or mark it unresolved. Persona does not determine factual support, source authority, comparability, missing-data behavior, assumptions, recommendation confidence, or product suitability; hand those decisions to `agent-architecture` or `agentforce-generate`.
- **Global Lexicon** — brand name, product names, and industry terms used everywhere. Every entry requires a term + definition; usage guidance and immutable status are optional.
- **Agent-design Guardrails handoff** *(optional; explicit input only)* — preserve supplied content boundaries verbatim and separately from Persona for `agent-architecture` or `agentforce-generate`. Never infer, score, rewrite, or encode Guardrails here.
- **Values** *(optional, explicit-input only)* — never inferred.

**Cross-cutting verbatim guardrail:** Never alter content the designer marks as immutable (legal disclaimers, brand-defined terminology). If a phrase book entry or lexicon term conflicts with immutable content, the immutable content wins.

### DRAFT Exit

Persona document is on disk. State carries:
- Mode (greenfield/brownfield)
- Channel
- Company, Audience, Use cases
- Identity Traits, Negative Identity
- Personification (Not personal / Individuated / Anthropomorphic) + 13 expression dimensions (filled or defaulted)
- Organizational “we” decision; Human experiences or feelings decision when applicable
- Confidence annotations
- Phrase Book, Never-Say, Tone Boundaries, Tone Flex, Reading Level Flex, Technical Explanation Policy (if applicable), Lexicon
- Explicit agent-design Guardrails handoff (if supplied), Values (if explicit), Immutable content blocks
- `display_name_placeholder` (working title from input, if detected)
- `name_decision: pending`

Present the HUB.

---
