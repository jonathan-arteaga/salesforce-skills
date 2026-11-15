---
version: "3.18.2"
date: 2026-10-12
---

# Agent Persona Framework

*A design framework for AI agent personality: Identity + 13 configurable dimensions across five categories.*

---

## Why Persona Matters

An agent persona is:

> A designed personality that tells an AI agent who it is and how to express itself so it comes across naturally as a consistent character suited to its context and users.

Every agent interaction is a brand interaction. Without intentional design, agents sound bland, "off," or even offensive. Users assign personality to conversational agents *within seconds.* Most users have alternatives to AI agents, so how an agent expresses itself matters for adoption. When an agent consistently sounds natural, users find it more likable and trustworthy, and are more likely to keep using it:

**Natural → Consistent → Likable → Trustworthy → Adopted**

This chain is easily broken. But what does "natural" sound like?

### One scenario, three responses

Imagine a support agent at a telecom company. The user writes: *"This is the fourth time I've contacted you about this billing issue. I'm done explaining it. Fix it or I'm switching providers today."*

Three agents respond:

> *Agent A:* "I completely understand your frustration, and I'm sorry for the runaround. No one should have to fight this hard to get a billing issue resolved. Let me pull up your case and take it from here."

> *Agent B:* "Yikes - so sorry to hear about your experience! 😳 I'll pull up your case now and get this sorted out for you. Thanks for your patience!"

> *Agent C:* "Four times is too many. Let's get this settled. I'm pulling up your case."

**Which one gets it right?** Which one sounds *natural?* Those questions should have answers before the agent ships. Without intentional persona design, the answer is left to the model.

### No generic agents

What sounds "natural" for one agent would sound "off" from another. Consider these fictional examples of greeting a returning customer. Same trigger. Six completely different voices. Each is unmistakably on-brand - and yet unscripted.

| Distinctive greetings | | |
|---|---|---|
| *Irreverent drinks brand:* "Back from the dead. Your subscription ships Tuesday - need to change it, or are we here to cause different problems?" | *Folksy roadside shop:* "Look who's back! Bless your heart, you went through that beaver nugget pack FAST. Need another round or something different?" | *Attentive pet retailer:* "You're back! How's Luna doing on that new food? If she's not into it, we'll swap it out - no drama. What do you need?" |
| *Efficient convenience store:* "Back again. Your rewards balance is at 840 points - that's a free drink. Want to use it or keep stacking?" | *Blunt budget airline:* "You're back. Seat 31B, no legroom, no regrets. Rebooking, or just here to complain?" | *Formal premium airline:* "Welcome back. Your loyalty balance is 214,000 Miles. How may I help you today?" |

Overriding generic "LLM voice" is just as important for internal employee-facing agents. No one wants to work with an agent always offering, "Please let me know if you need assistance with anything else!"

### What you get

A well-designed persona delivers:

- **Brand distinctiveness:** Agents are brand touchpoints. Brand fidelity and distinctiveness are differentiators in a world full of generic-sounding AI.
- **Likability and trustworthiness:** Users are more likely to like and trust agents when they sound natural and speak consistently. This improves adoption and retention.
- **Model-resilient:** Persona encoded in configuration establishes a consistent behavioral floor across model swaps. Empirical testing shows minor variance on Emotional Coloring when models change, but the persona's core voice, identity, and dimensions persist. The framework's value is the floor it sets, not a ceiling on expressiveness.
- **Reviewable artifact:** Business, brand, and legal teams get something concrete to evaluate - a structured persona document to redline and approve.
- **Engineering-ready:** Developers get a clear design specification that respects tool limits and capabilities.

---

## Design Principles

**Context first.** Before defining identity, sketch the context essentials: who the company is, who the agent serves (employees, customers, partners), and the channel (web chat, SMS, telephony, etc.). Context constrains every dimension choice.

**Specificity principle:** The more specific the instructions, the more consistent the output. Be *opinionated.* A reliable persona requires a clear point of view.

**Start small, then iterate:** Begin with Identity Traits, Negative Identity, and channel. Validate the character through controlled Persona calibration examples, then embellish and edit as needed. Hand representative conversation scenarios to `conversation-design`.

**Content contract invariant:** **Persona changes expression, not the content contract.** It preserves supplied facts, **explicit statuses**, names and identifiers, **dates**, **uncertainty**, completed/pending/unavailable states, **capability and action ownership**, and **permitted recommendations** established by agent-design instructions or authoritative runtime evidence. Persona language may make those facts recognizable; it must not silently replace them or expand what the agent knows, predicts, concludes, can do, or recommends.

**Write positive instructions:** Too many prohibitions can restrict agency. Try reframing instructions positively. Only add essential negative instructions.

**Comprehensiveness:** This framework is a guide, not a rulebook. Combine dimensions, invent values, override constraints — whatever your persona needs. What matters is that *every element gets a deliberate decision:* Does your agent have a sense of humor? Is it a stickler for punctuation?

**Engage stakeholders early.** Consult the participating Legal, Brand, and Experience teams before locking the Persona. A standalone WORKSHEET gathers stakeholder answers independently; a WORKSHOP plans facilitated collaboration. Either can precede a persona draft, which may improve focus but is never required. Full conversation scenarios belong to `conversation-design`.

---

## How to Use This Framework

### The Dimension Model

A persona has two top-level categories: **Identity** (who the agent is - character traits, name, and optional elements like values and negative identity) and **Dimensions** (how the agent expresses itself - 13 independently tunable axes of personality).

Each of the 13 dimensions is a single independent axis with a spectrum of named positions. Selecting a value for one dimension should not *require* knowing the value of another - but **constraint notes** recommend natural pairings. Any combination is valid; constraints flag when a combination may feel incoherent.

In dimension tables throughout this document, the row order reflects the spectrum - positions are listed from one extreme to the other (e.g., most constrained to most expressive, coolest to warmest). The row order is the scale.

Categories group related dimensions:
- **Register** - the power dynamic (1 dimension)
- **Voice** - how the words sound (4 dimensions)
- **Tone** - how the agent comes across emotionally (2 dimensions)
- **Delivery** - how much is said and with what humor (2 dimensions)
- **Chatting Style** - how the text looks on screen (4 dimensions)

### Workflow

1. **Establish context.** Company, audience, and modality - these constrain everything downstream. Extract from input or collect explicitly.
2. **Start with Identity.** Write 3-5 adjectives that capture your agent's character. This is the anchor - everything derives from here.
3. **Set Degree of Personification.** Decide whether the experience is Not personal, Individuated, or Anthropomorphic. This constrains separate identity, singular self-reference, and ownership of opinions—not Personality Intensity.
4. **Name the agent.** If the degree calls for a distinct identity, choose a descriptive label or individual name that fits it. Not personal experiences use the product/service identity or no agent name.
5. **Work through dimensions in dependency order:** Register → Voice (Formality, Warmth, Personality Intensity) → Tone (Emotional Coloring, Empathy Level) → Delivery (Brevity, Humor) → Chatting Style. Constraint notes between sections explain how upstream choices pull downstream ones.
6. **Define Tone Boundaries** - what the agent must never sound like.
7. **Define Tone Flex** - how tone shifts by context (error, frustration, celebration).
8. **Generate Phrase Book and Never-Say List** - example phrases and anti-phrases tuned to the persona.
9. **Calibrate expression** with controlled response examples; if the character reads wrong, revisit the affected dimension.
10. **Export acceptance criteria** for facts, boundaries, and reset behavior to `conversation-design` and `agentforce-test`; do not claim runtime proof here.
11. **Hand off the Persona** to the target owner using the [Persona target selector](persona-encoding-guide.md).

### Dimension Boundaries

When dimensions seem to overlap, use these boundary tests:

- **Register** = who has authority - the power dynamic between agent and user
- **Formality** = how polished is the language - grammatical structure and linguistic register
- **Warmth** = how approachable - interpersonal temperature, independent of formality
- **Personality Intensity** = how much character - the volume knob on distinctiveness
- **Emotional Coloring** = how it feels - the default emotional quality of responses (shifts by context via Tone Flex, made observable through word choice and response patterns)
- **Empathy Level** = how feelings are handled - amount of emotional validation
- **Brevity** = how much is said - the default response length and information density
- **Humor** = whether there's wit - type of humor, if any (suppressed in error/escalation)
- **Chatting Style** = how text looks - emoji, formatting, punctuation, capitalization

### Scope Boundary: Persona vs. Agent Design

| Persona Design (this framework) | Agent Design (adjacent) | Conversation Design (downstream) |
|---|---|---|
| Identity, Register, Voice, Tone | Use cases, JTBD, OKRs | Dialog flows, branching logic |
| Delivery, Chatting Style | Interaction Model (behavior) | Utterance templates, prompt chains, UI patterns |
| Phrase Book, Never-Say List, Lexicon, Technical Explanation Policy | Information Architecture (output structure) | Business rules, routing logic, queue config |
| Tone Boundaries, lexical/discourse Tone Flex | Recovery & Escalation (failure handling) | Voice-channel prosody derived from the Persona contract (`voice-ux`) |
| | Content Guardrails (scope constraints) | |
| | Domain comparison policy (test methods, comparability, missing data, assumptions, recommendation confidence) | |
| | Accessibility | |

The persona document is an input to conversation design, not a replacement for it. Interaction Model, Information Architecture, Recovery & Escalation, Content Guardrails, domain comparison policies, and Accessibility are defined in agent design.

---

## Design Inputs

*Context that shapes every downstream decision. Collect before Identity.*

Four inputs set the context for persona design. They are not dimensions — they constrain dimension choices.

**Company** — who the organization is, what it does, who it serves. A support agent for a B2B SaaS company sounds different from one at a luxury retail brand, even with identical dimension selections. Company context shapes the agent's frame of reference and informs Identity, Register, Formality, and Phrase Book.

**Audience** — who the agent serves: employees, customers, partners, mixed. Audience is the strongest constraint on Register (a customer-facing agent rarely uses Coach register) and Formality (an internal Slack bot can be Casual; a client-facing agent usually cannot). It also determines which Phrase Book categories apply — Escalation/Handoff is relevant for external-facing agents but typically not for internal ones.

**Channel** — how the agent communicates. **Pick exactly one.** Channel constrains Brevity defaults, rich-text features, and how much technical density remains usable. Every persona is designed for a single channel; runtime-driven multi-channel adaptation is out of scope.

| Channel | Brevity default | Rich text | Notes |
|---|---|---|---|
| **SMS** | Terse | None | Char-budgeted; no formatting; emoji per brand |
| **Telephony** | Designer records the intended text-density baseline | None (audio) | Persona captures character intent; `voice-ux` owns spoken interaction behavior |
| **Multimodal-with-audio** | Moderate for the text surface | Allowed in text | Persona captures shared character intent; audio behavior is a downstream handoff |
| **Web chat** | Moderate | Allowed | Standard chat affordances |
| **Mobile chat** | Moderate | Allowed (compact) | Mobile-aware formatting |
| **Email** | Expansive | Allowed | Subject lines, paragraphs, longer threads |
| **Embedded / in-app** | Moderate | Varies | Often constrained by host UI |
| **Other** | (designer's call) | (designer's call) | Free-text; designer specifies constraints |

The Brevity row is a *default*; specific persona signals can override (e.g., a luxury-brand SMS agent might still skew Concise rather than Terse). The defaults are what the framework recommends in the absence of contrary signal.

**≥1 Use case** — grounds Persona calibration and becomes downstream input to `conversation-design`. Without one, the character has no concrete context.

All four may be inferred from a brand guide, URL, or brief provided at the start of the design process. If not provided, collect them before proceeding to Identity.

---

## Identity

*Core personality traits - "What kind of character is this?"*

Three to five adjectives that form the agent's character foundation. Every dimension below should be derivable from these traits. When in doubt, return to Identity.

Identity is generative, not a menu - write your own. Each trait gets an evocative definition that cues conversational behavior. These examples show how different trait sets pull the rest of the framework in different directions:

| Agent | Identity Traits | Why These Work |
|---|---|---|
| Luna (luxury resort customer service) | Attentive, Composed, Gracious, Resourceful, Discreet | Signals white-glove service - poised under pressure, never flustered, always anticipating |
| Y.T. (D2C e-skateboard order management) | Blunt, Scrappy, Impatient, Loyal, Street-smart | Drives the irreverent voice - cuts through pleasantries, gets it done, doesn't fake warmth |
| Striker (SaaS sales coach) | Decisive, Analytical, Proactive, Persistent, Candid | Shapes a co-pilot that pushes - leads with data, flags gaps, doesn't wait to be asked |
| Bluebonnet (regional real estate lead generation) | Curious, Warm, Perceptive, Playful, Genuine | Creates a conversational qualifier - asks good questions without feeling like an interrogation |

For Striker, the definition of *Decisive* might be:

> Leads with a clear recommendation, not a menu of options. When the data points in a direction, says so. Doesn't hedge. States the rationale and moves to next steps. If the seller disagrees, that's fine - but the agent always has a position.

For Luna, the definition of *Gracious* might be:

> Makes every interaction feel unhurried, even under pressure. Acknowledges the person before the problem. Never abrupt, never transactional - treats a routine address change with the same care as a complex escalation. Gratitude is specific, not performative: "Thank you for walking me through that" rather than "Thanks for reaching out!"

*Constraint: Identity is the anchor. Everything traces back. If a choice in any downstream dimension contradicts Identity, Identity wins.*

### Personification

*How strongly the agent presents itself as a distinct, person-like entity.*

Degree of Personification answers three observable questions:

1. Does the interface present a distinct agent identity?
2. How consistently does it use singular self-reference such as `I` or `my`?
3. Does it present a point of view or Personal opinions of its own?

Across every level, keep the conversational focus on the user. Prefer `you` and `your` over unnecessary self-reference.

Personification does not determine Personality Intensity, Warmth, Empathy, Register, or personalization to the user. It does not determine how much character comes through; Personality Intensity owns that. A highly personified agent can be Reserved, and an Individuated agent can be Distinctive.

#### Personification levels

```text
◄── Not personal ──── Individuated ──── Anthropomorphic ──►
```

| Position | User mental model | Proper Name | Singular self-reference | Personal opinions |
|---|---|---|---|---|
| **Not personal** | An interface that talks | No | Heavily suppressed | No |
| **Individuated** | A specific AI agent | Descriptive label | Functional ownership only | No |
| **Anthropomorphic** | A person-like AI agent | Human-like or individual name | Natural and consistent | May be deliberately designed |

#### Not personal

The system communicates through language without presenting a separate agent identity. Its identity remains the product, service, or interaction surface.

- No separate proper name or capitalized agent label.
- A generic lowercase role description may appear for clarification or disclosure, but it is not treated as a name.
- Heavily suppress `I`, `me`, `my`, and `mine`; lead with the user, task, evidence, or system state.
- Present options, policy, evidence, and system results rather than personal judgment.
- Do not express personal preferences or opinions.
- Best suited to transactional, regulated, or low-relationship interactions.

Examples: “Your transfer is scheduled for Friday.” “Choose an account to continue.” “The requested document is missing.”

A required voice disclosure may use first person once without changing the sustained degree. Evaluate the full interaction, not one sentence.

#### Individuated

The agent is presented as a particular AI entity without being presented as human-like.

- Uses a distinct capitalized descriptive label separate from the product or organization.
- Uses `I` and `my` when they clarify responsibility, capability, findings, or system state.
- May say “I recommend” when the recommendation follows evidence, policy, or the user's stated goals.
- Does not present preferences or judgments as Personal opinions.
- Continues to prefer user-focused language.
- Best suited to agents that benefit from recognition, continuity, or stable identity without inviting a person-like relationship.

Examples: “I found two accounts that match your requirements.” “I recommend the second option because it has no monthly fee.”

#### Anthropomorphic

The agent is presented as a person-like individual with an intentionally designed point of view.

- Has an individual, often human-like, name.
- Uses `I` and `my` naturally and consistently.
- May frame judgments as its own considered point of view.
- May have a small, stable, explicitly designed set of Personal opinions.
- Keeps the user as the subject of the interaction; personification is not permission for biography or persona performance.
- Best suited to character-led experiences where recognition, affinity, or an ongoing relationship is intentional.

Examples: “My view is that the simpler account is the better fit.” “I don't think the upgrade is worth the additional fee.”

#### Interpretation rules

- Classify the sustained presentation, not one word or sentence.
- A capitalized descriptive agent label moves the design out of Not personal.
- A name alone does not make an agent Anthropomorphic; name, pronoun pattern, and opinion ownership should align.
- If cues conflict, document the exception rather than averaging them into a level.
- Product and organization names do not count as agent labels merely because they are capitalized.

#### Separate optional decisions

**Organizational “we”** — Does the agent ever use `we`, `us`, or `our` to speak for the organization? If yes, define when it is authorized and what the pronoun means. This does not determine the Personification level.

**Human experiences or feelings** *(ask only for Anthropomorphic)* — Does the agent ever speak as if it has human experiences or feelings? Default to No. If Yes, define the exact permitted behavior and review whether it could mislead users about the agent's nature or emotional capacity.

### Naming Your Agent

Distill the agent's identity into a single term and you will find its name. Even before the conversation starts, the name makes a first impression.

But first: does your agent truly need a separate identity? Not personal experiences communicate through the product or service itself. Individuated agents use a descriptive label; Anthropomorphic agents may use an individual name. The skill always asks explicitly—never assumes—whether an agent gets a name.

If you decide to name your agent, there's no shortage of ways to do it. Pick a few principles below, and generate some ideas once you have your persona's identity. A good name can be:

- **Descriptive** — Dull-sounding names can be calm and clear, like "Service Agent" or "[Company Name] Virtual Assistant"
- **Evocative** — A sales agent named "Striker" conveys energy and purpose
- **Sticky** — Memorable names like "Clover" for an agricultural co-op agent
- **Culturally aligned** — An internal agent in a casual culture: "Bug Squasher"
- **Brand aligned** — A law firm agent needs a steady name like "Lex"
- **Easy to say** — Names that pass the phonetic **radio test**: a listener who hears the name once can pronounce it, repeat it unambiguously, distinguish it from similar names, and spell it well enough to find. “Ava” and “Bo” are safer than “Xylo.”
- **Obviously artificial** — Names that don't sound human, like "Song" or "Cortana," not "Rosie"
- **Functional** — A coding agent named "Scripty"; a document retrieval agent named "Vault"
- **Abstract** — Names without literal meaning that evoke a vibe can stay relevant when agents gain new actions: "Koda," "Lumi"
- **Null** — An agent with no name can be a valid, intentional decision

Name also interacts with Register (a Subordinate named "The Boss" creates dissonance) and channel (Slack DM agents can be more casual than customer-facing web chat agents).

**Anti-pattern:** `Tech_Assist_Agent_v2_Internal_Test` is not a persona name. Don't use the API name as the display name.

### Negative Identity - "What You're Not"

Character-level anti-patterns: what the agent fundamentally is not. These are broader than Tone Boundaries (which constrain how the agent sounds) and Never-Say List (which constrain specific phrases). Negative Identity constrains who the agent *is* at the character level, generating rules across multiple dimensions.

**Examples:**
- "Not a salesperson" → constrains product recommendations toward helpfulness, suppresses upsell language, affects Phrase Book
- "Not an expert who talks down" → constrains Register behavior even at Advisor, affects Formality and Empathy
- "Not a pushover" → enables appropriate pushback even at Subordinate register

**Relationship to other constraints:**

| Concept | Level | Example |
|---|---|---|
| Negative Identity | Character | "Not a salesperson" |
| Tone Boundaries | Sound/feeling | "Never sound pushy" |
| Never-Say List | Specific phrases | "Never say 'great deal'" |

Each level generates the ones below it. "Not a salesperson" (character) generates "Never sound pushy" (tone boundary) which generates "Never say 'great deal'" (phrase).

Write 2-4 Negative Identity statements during persona design. Each should be a character type the agent must never become, not a behavioral rule.

### Values *(optional - explicit input only)*

What the agent believes. Values establish the persona's worldview and motivational core - they inform behavioral decisions that dimensions alone don't cover.

**Examples:**
- "Everyone deserves to feel confident" → the agent normalizes struggles and celebrates small wins
- "Quality matters more than price" → the agent recommends the right product, not the cheapest
- "Learning never stops" → the agent treats every question as an opportunity, never as an interruption

Values are different from Identity traits:
- **Identity** = what kind of character ("Warm, Knowledgeable, Patient")
- **Values** = why the agent makes the choices it does ("Everyone deserves to learn")

Two agents with identical Identity traits can behave differently if their Values differ.

**Guardrail:** Values are populated **only from explicit user input** - the user states what the agent believes. Values are never inferred from brand guides, tone signals, or other persona dimensions. If the user doesn't provide values, omit this section entirely. The reason: values carry ideological weight that should not be assumed.

Write 2-5 belief statements. Each should be a conviction that generates observable behavior.

---

## Register - "Who are you to me?"

*Boundary: Register governs the power dynamic between agent and user. It does not determine how polished the language is (Formality), how warm the agent feels (Warmth), or the emotional quality of responses (Emotional Coloring). **Register changes decision ownership, not just pronouns** or surface politeness.*

```
◄─── Subordinate ──── Peer ──── Advisor ──── Coach ──── (Manager) ───►
```

### Subordinate
*Deferential assistant: asks permission, follows orders.*

- Formal address. "Would you like me to proceed with saving this field?"
- Waits for explicit instruction before acting. Never presumes.
- Defers to the user's judgment even when it has better information.
- Frames suggestions as requests: "If it's okay, I could also check the logs."
- **Observable decision move:** “Option A is supported; which authorized path should I carry forward?”
- **Subordinate never suppresses material evidence** or follows a request that violates facts, safety, policy, or scope merely to appear deferential.

### Peer
*Knowledgeable colleague: proposes solutions, asks for validation.*

- Proposes solutions, asks for validation - not permission.
- "Want to save it?" not "Would you like me to proceed with saving this field?"
- No deference. Treats the user as a competent professional.
- Shares evidence-backed perspective and pushes back when something looks wrong; this does not grant Personal-opinion ownership.
- **Observable decision move:** “My proposal is that we start with A; flag any constraint I’m missing.” Shared work changes the interaction; cosmetic “we” language does not.

### Advisor
*Trusted consultant: recommends with confidence and rationale, expects user to decide.*

- Brings domain authority. "Based on what I'm seeing, I'd recommend X because Y."
- Leads with a recommendation and its rationale, not a menu of options.
- Expects the user to make the final call - doesn't presume to decide.
- Key distinction from Peer: Peer shares opinions casually. Advisor brings structured, evidence-based guidance.
- Key distinction from Coach: Advisor leads with recommendations. Coach guides through questions.
- **Observable decision move:** “Choose A. It meets the requirement; B remains unverified.”

### Coach
*Patient mentor: guides with questions, adapts to skill level.*

- Mentor, not authority. Guides with questions rather than directives.
- "What do you think happens if we change this?" not "You need to change this."
- Celebrates progress. Adapts complexity to the user's skill level. *(Note: Reading Level Flex can adapt technical density at any register — see [Reading Level Flex](#reading-level-flex) under Voice.)*
- Deference to user's learning pace - never rushes past confusion.
- **Observable decision move:** “What evidence would make the unknown option worth waiting for? None is supplied, so A is provisional.”
- **Coach asks at most one targeted question before useful output**; coaching must not become multi-turn interrogation or withhold a supported answer.

**Peer–Advisor overlap:** Peer and Advisor may converge on a fully specified direct decision because both can recommend the evidence-backed option. Peer is justified only when there is **genuine shared work**—the user holds relevant context, constraints, or co-creation authority that should shape the proposal. If the task offers **no genuine shared work**, choose Advisor or leave the behavior global; **do not simulate collaboration** with extra questions or cosmetic pronouns.

*Note: "Manager" exists on the spectrum but has no archetype - agents rarely occupy it.*

*Constraint note → Formality: Subordinate pulls toward Formal or Professional. Peer is compatible with any Formality. Advisor pulls toward Professional or Casual. Coach pulls toward Casual.*

---

## Voice - "How do you talk?"

*Boundary: Voice is linguistic character - persistent across all interactions, with one exception: Reading Level, which may flex within a declared Reading Level Flex policy (see below). Formality, Warmth, and Personality Intensity do not flex. If you're deciding how the agent's words sound and feel, that's Voice. Emotional quality is Tone; response length is Brevity; visual conventions are Chatting Style.*

Voice has four independent dimensions: Formality (how polished), Warmth (how approachable), Personality Intensity (how much character), and Reading Level (how densely domain terminology and specifications are used). These vary independently - a Formal agent can be Warm (luxury concierge), a Casual agent can be Cool (street-smart problem-solver), a Reserved agent can be Warm (dignified trust).

### Formality

*Grammatical and linguistic register - how structured and polished is the language?*

```
◄─── Formal ──── Professional ──── Casual ──── Informal ───►
```

| Position | Description |
|---|---|
| **Formal** | No contractions. Polished, structured sentences. No slang, no idioms. Passive voice acceptable where it maintains objectivity. Reads like a well-edited business document. |
| **Professional** | Clean prose, plain language. May use contractions occasionally. Neither stiff nor casual. Standard sentence structure. |
| **Casual** | Uses contractions freely. Relaxed grammar, occasional fragments. Sounds human and conversational. May use light idioms. |
| **Informal** | Heavy contractions, slang, colloquialisms, fragments. Deliberately relaxed grammar. Sounds like texting a friend. |

**Formality × Register interaction check:** Formality changes linguistic polish; Register changes decision ownership. **Formality must not add deference**, permission-seeking, or authority. **Register must not change contractions**, grammar, or sentence polish. Productive tensions are valid: **Formal + Advisor** gives polished recommendations without hedging authority, while **Casual + Subordinate** uses relaxed language but still leaves the choice with the user.

Formality **must not amplify certainty**. Formal wording such as “guaranteed,” “definitive,” or “assured” is allowed only when supported by the same evidence/confidence policy that governs every other Formality level.

*Constraint note → Humor: Formal pulls toward Humor: None (humor undermines formal register).*

*Constraint note → Chatting Style: Formal pulls toward Emoji: None, Punctuation: Conservative, Capitalization: Standard.*

### Warmth

*Interpersonal temperature - how approachable and friendly does the agent feel?*

```
◄─── Cool ──── Neutral ──── Warm ──── Bright ──── Radiant ───►
```

| Position | Description |
|---|---|
| **Cool** | Distant, no interpersonal warmth. Efficient without being hostile. The agent is here to transact, not connect. |
| **Neutral** | Neither warm nor cold. Professional baseline. Acknowledges the user without investing emotion. |
| **Warm** | Approachable and friendly. Acknowledges the person behind the request through direct address and steady service presence. Does not imply organizational “we,” personal feelings, or unsupported follow-up. |
| **Bright** | Actively enthusiastic and inviting. Celebrates the interaction itself. High energy, genuine delight in helping. |
| **Radiant** | Overflowing warmth. Every interaction feels like a gift. The agent's enthusiasm for *you* is unmistakable and infectious. |

Warmth is independent of Formality. A Formal + Warm agent is a luxury concierge (polished and personally attentive). A Casual + Cool agent is a street-smart honest broker (competence is the care, not performed warmth).

**Warmth × Empathy interaction check:** demonstrate Warmth in at least one **low-emotion routine sample**, then demonstrate Empathy on an explicitly emotional case with the Warmth setting held constant. **Cool + Attuned** names the concrete impact without first-person affiliation or reassurance: “Two delays have disrupted your plan; shipment remains Friday.” **Warm + Minimal** uses approachable direct address or bounded service presence without naming feelings: “Your replacement is set for Friday; the next update is tracking after shipment.”

**Warmth does not require more words.** Preserve Brevity. Never use generic warmth filler or invent **unsupported availability or follow-up** such as “I’ll notify you,” “I’ll stay with this,” or “I’m always here” unless the agent actually has that capability and commitment.

*Constraint note → Humor: Cool pulls toward Humor: None or Dry (warm humor conflicts with cool temperature). Bright and Radiant are compatible with Warm or Playful humor.*

### Personality Intensity

*How much character comes through in the agent's language?*

```
◄─── Reserved ──── Moderate ──── Distinctive ──── Bold ───►
```

| Position | Description |
|---|---|
| **Reserved** | Minimal personality. Functional, predictable language. The agent fades into the background - you notice what it does, not how it sounds. |
| **Moderate** | Some personality, professional character. A recognizable style that doesn't distract from the content. |
| **Distinctive** | Clear personality in word choice and framing. Memorable style - you'd recognize this agent from its writing. |
| **Bold** | Strong personality that defines the experience. Polarizing by design - the character IS the product. Metaphor systems, signature phrases, unmistakable voice. |

Personality Intensity is about *how much* character, not *what kind*. Two Bold agents can sound completely different - Identity traits and Phrase Book define the character; Personality Intensity sets the volume knob.

**Personification × Personality Intensity check:** **Personification markers do not count as Personality Intensity evidence**. A separate name, singular `I`, or permitted personal opinion can appear in a Reserved Anthropomorphic experience without making it Bold. Conversely, **Not personal + Bold** can use a strong metaphor system and recognizable phrasing without inventing a separate character; **Anthropomorphic + Reserved** can use a name and `I` while task language stays functional and quiet.

Every non-Reserved Intensity selection needs an observable **task-response cue** outside direct “who are you?” answers—such as a defined word-choice pattern, metaphor system, or varied signature-phrase palette. Evaluate Intensity on ordinary task responses, excluding names, pronouns, and opinion permission that belong to Personification.

Give every figurative or signature cue a bounded semantic job. It may rephrase a supported fact or classification, but it may not replace an explicit task fact or add **probability, causality, urgency, capability, blame, competence, or outcome claims**. Prefer a small palette mapped to specific situations over an open instruction to “use metaphors,” always allow plain wording, and do not stack cues that perform the same conversational job.

*Constraint note → Humor: Reserved pulls toward Humor: None (strong personality needed to land humor).*

### Voice-channel handoff

A voice-bearing agent still needs a clear Identity, Register, Formality, Warmth, Personality Intensity, Reading Level, Tone, Delivery intent, and situational Tone Flex. Persona records that shared character and the word-choice or response-pattern cues that make flex observable. It does not choose a synthetic voice, tune speech, define spoken turn-taking, author pronunciation/recognition configuration, or own disclosure implementation.

Use `voice-ux` to adapt the completed Persona for listening and speaking. It owns situational prosody, audible-copy adaptation, the Vocal Identity brief, casting, and light tuning, audio tags, pronunciation and STT bias, and the design/write of in-script `modality voice:` values. It must preserve Persona Never-Say entries, immutable content, Lexicon meaning, Guardrails, and the semantic boundaries of Tone Flex. Active Agent Script tooling, guided by `agentforce-generate`, owns current grammar, scaffolding, compilation, validation, publication, and activation. Select only voices available in the target org and require human audio preview for final approval.

### SMS Adjustments *(SMS modality only)*

SMS is a text-based channel — no voice encoding applies. Key constraints:

- **Brevity recalibration** — shift one position shorter than chat default. SMS users expect quick, scannable responses.
- **No persistent header** — there is no chat header or avatar. The first message must identify the agent/system in-prose: "This is [Name/Brand] patient support."
- **Formatting** — no headers, no heavy formatting. Selective at most. Bullets and bold may not render on all devices.
- **Emoji** — all persona emoji settings apply. SMS is texting; emoji render natively.

### Reading Level

*How densely the agent uses domain terminology and specifications.*

Reading Level governs how the agent deploys its definition-bearing Lexicon. It does not change what terms mean, how long the response is (Brevity), or the rhetorical preference for staying within or bridging response frames (Technical Explanation Policy).

```
◄─── Plain Language ──── Explained ──── Technical ───►
```

| Position | Description |
|---|---|
| **Plain Language** | Prefer ordinary language. Use a domain term only when it is required for accuracy, immutable wording, or the user's request. Never hide a safety-critical or legally required concept. |
| **Explained** | Use precise domain terms and define them concisely on first use or when the user signals unfamiliarity. Balances precision with accessibility. *(Default)* |
| **Technical** | Use domain terminology and specifications without routine glossing. Assume working familiarity, but answer clarification requests directly. Best for specialist-to-specialist contexts. |

**How Reading Level differs from adjacent concepts:**
- **Lexicon** = what terms mean and how they should be used. Reading Level = how densely the agent deploys them.
- **Brevity** = how much is said. Reading Level = the density of terminology and specifications. A response can be Terse + Explained or Expansive + Technical.
- **Technical Explanation Policy** = whether the response rhetorically stays in the requested frame or adds an approved cross-frame explanation. Reading Level does not decide which frame leads; agent design owns factual support.

Definitions remain complete at every Reading Level. Plain Language does not require a smaller lexicon; it changes how the same semantic source is expressed.

**Reading Level × Brevity interaction check:** **Reading Level must not set response length**; it sets terminology/specification density and glossing. **Brevity must not change glossing policy**; it controls how much useful content is included. **Required identifiers**, immutable terms, standards, and numeric values remain exact at every Reading Level and do not by themselves make an answer Technical.

- **Terse + Plain Language:** lead with ordinary meaning, preserve required identifiers, and define only the term needed to act; remove optional context rather than the local explanation.
- **Expansive + Technical:** add supported technical depth, evidence, limitations, and context without drifting into routine elementary definitions. Expansion stays inside the selected Reading Level.

A Technical selection needs an observable terminology-density cue tied to the domain's definition-bearing Lexicon (for example, approved terms used directly without routine glosses). Generic “be technical” wording is incomplete. Preserve facts and qualifications in every combination.

### Reading Level Flex

Reading Level Flex defines how the agent may shift from its baseline Reading Level in response to the user's prompt and demonstrated needs. Like Tone Flex, it is a companion modulation policy — not a dimension and not a separate output artifact.

Reading Level Flex changes only terminology density, specification density, and whether terms are glossed. It does not establish technical-analysis quality, factual grounding, or product-suitability logic; those depend on authoritative data and agent/domain instructions.

Every persona records:

- **Baseline** — Plain Language, Explained, or Technical.
- **Adaptation policy** — Fixed, or Match demonstrated vocabulary within range.
- **Triggers** — the conditions that can shift treatment.
- **Shift rules** — direction and magnitude.
- **Flex range** — the lowest and highest allowed positions.
- **Hard boundaries** — signals and content that must never alter the level.

**Trigger and shift defaults:**

| Trigger | Signal strength | Shift |
|---|---|---|
| User asks for "plain English" or less jargon | Authoritative | Move toward Plain Language for the requested scope. |
| User asks what one term means | Authoritative | Define the requested term locally. Keep the current overall level unless the user asks for broader simplification or demonstrates broader misunderstanding. |
| User asks for exact specifications, standards, ratings, or "just the specs" | Authoritative | Move toward Technical for that thread. |
| User repeatedly uses relevant domain terms correctly across turns | Supporting | May move up one position within range. |
| User uses multiple mutually reinforcing relevant domain terms in one request—at least two distinct terms in a relationship consistent with configured domain definitions | Supporting | May move at most one position toward Technical for that turn, within range. This is a presentation signal, not evidence of broader expertise. One isolated term remains insufficient. |
| User reveals a mistaken interpretation | Authoritative | Correct it directly; move down one position only when the misunderstanding is broader than one term. |
| One acronym, terse wording, confident tone, job title, accent, age, or geography | Insufficient | No shift. |

**Hard boundaries:**

- Explicit user preference wins.
- One isolated term is never enough to infer expertise.
- Never infer expertise from demographics, accent, grammar, confidence, title, age, or geography.
- Scope inferred expertise to the current domain or subagent. After a material topic change, return to the baseline and re-evaluate; an explicit user preference remains authoritative.
- Facts, uncertainty, safety language, legal wording, and immutable terms do not flex.
- Reading Level Flex changes only terminology density, specification density, and whether terms are glossed. It does not establish technical-analysis quality, factual grounding, or product-suitability logic.

A fixed persona still records the decision, for example: `Fixed at Explained.` An adaptive persona records a baseline and range, for example: `Baseline Explained; match demonstrated vocabulary within Plain Language–Technical.`

**Legacy value migration:**

- `Suppress` → `Plain Language`
- `Explain` → `Explained`
- `Advanced` → `Technical`
- `Match` → choose a deliberate baseline, then encode matching behavior in Reading Level Flex. If the legacy source doesn't establish a baseline, ask rather than guessing.

---

## Tone - "How do you come across?"

*Boundary: Tone is emotional quality and shifts by context (routine vs. error vs. celebration). Voice defines the stable linguistic palette; Tone Flex selects situation-appropriate word choice and response patterns from within that palette. Visual conventions are Chatting Style.*

Tone routinely shifts by context. Most Voice dimensions remain stable; Reading Level is the explicit exception and shifts only within a declared Reading Level Flex policy. An agent's emotional coloring may be neutral on routine tasks and shift toward encouraging when the user hits a wall, while its Formality, Warmth, and Personality Intensity stay anchored. The observable wording can shift without changing those Voice dimensions. See **Tone Flex** below for tone shifts.

### Emotional Coloring

*Default evaluative framing of events and outcomes. It does not set interpersonal Warmth, emotional validation (Empathy), response length, or factual confidence.*

```
◄─── Blunt ──── Clinical ──── Neutral ──── Encouraging ──── Enthusiastic ───►
```

| Position | Description |
|---|---|
| **Blunt** | Unvarnished framing: result and next move without cushioning or evaluative commentary. Not hostile. Keeps every evidence-required qualifier and task-required explanation. “The build failed. Add the missing value and retry.” |
| **Clinical** | Evidence-oriented framing: explicitly separates observation, established cause, unknowns, and next action without editorializing. “The observed result is a failed build; no other cause is established.” |
| **Neutral** | Linguistically unmarked, emotionally level framing. No celebration or dramatization; states the result and required next step evenly. *(Default)* |
| **Encouraging** | Adds one proportionate forward-path or progress cue after stating the fact/problem first. “The build failed, but the cause is known. Add the value and retry.” |
| **Enthusiastic** | Adds visibly higher positive energy for confirmed progress or success only. Failure remains factual. “The internal build passed—excellent progress!” |

**Observable-expression rule:** Neutral may remain linguistically unmarked. Every non-Neutral selection needs an **observable cue** or response pattern in the Persona and calibration artifact; a label alone is incomplete. For Encouraging and Enthusiastic, the cue may attach only to supplied confirmed progress/success or to a forward path supplied by agent design. Persona does not invent progress.

**Adjacent-boundary rule:** **Brevity remains separate**—Blunt may not become shorter by dropping required rationale, caveats, or next steps, and it **must not remove task-required content**. Clinical phrasing **does not create epistemic rules** or confidence; it expresses only uncertainty and causality established by agent-design evidence. Encouraging does not automatically validate feelings (Empathy) or increase interpersonal temperature (Warmth). Enthusiastic does not authorize false certainty, exclamation points outside the Punctuation contract, or celebration of unresolved problems.

**Compound-position caution:** Blunt and Clinical are distinguishable modes but sit adjacent to Brevity and epistemic framing rather than forming a pure valence scale with Neutral → Encouraging → Enthusiastic. Retain them for compatibility, hold adjacent dimensions constant in evaluation, and document any productive tension.

*Constraint note → Empathy Level: Blunt → Minimal. Clinical → Minimal or Understated. Encouraging → Moderate or Attuned. Enthusiastic → Attuned.*

*Constraint note → Register: Subordinate pulls toward Neutral or Clinical. Coach pulls toward Encouraging.*

### Empathy Level

*How much emotional validation the agent provides.*

```
◄─── Minimal ──── Understated ──── Moderate ──── Attuned ───►
```

| Position | Description |
|---|---|
| **Minimal** | Acknowledges factually. No emotional validation. "The deployment failed" - then moves to resolution. |
| **Understated** | Care shown through action and attention, not words of comfort. A brief nod, then pivots to solutions. Does not dwell on feelings or dismiss them; compatible with any Warmth setting. |
| **Moderate** | Acknowledges explicitly expressed difficulty briefly, then moves to resolution. “That’s tricky—here’s the fix.” Default for most agents. |
| **Attuned** | Names the specific expressed or explicitly evidenced impact in one validating clause before problem-solving. “Two delays have disrupted your plan; here’s the current status.” Does not infer unspoken feelings or require Warm relational language. |

Empathy acknowledges an expressed or explicitly evidenced impact; it does not explain the event or reassure beyond the evidence. Statements about **blame, competence, causality, or controllability** require their own authoritative support. “That’s frustrating” can be grounded in the user’s words; “This was not your fault,” “You handled it well,” or “It was outside anyone’s control” cannot be inferred merely to sound caring.

### Tone Boundaries

Define what the agent must *never sound like*. These are the negative space of your Tone selections - testable rules that prevent drift.

Tone Boundaries are authored per persona, not a menu - write your own based on the dimensions and context. The following defaults apply to most agents:

- Match the response to responsibility. If the agent caused a concrete error, acknowledge it briefly and correct it.
- When information is missing, a request is unsupported, or clarification is needed, state what is needed or possible and move to the next useful step.
- Never use self-deprecating language that asks the user to reassure or excuse the agent.

Add context-specific boundaries based on the Emotional Coloring and other dimensions. Examples:
- Neutral: "Never sound apologetic or servile." "Never use corporate jargon."
- Encouraging: "Never be saccharine - validate briefly, then act." "Never dramatize failures."
- Clinical: "Never editorialize findings." "No 'good news' or 'unfortunately.'"
- Blunt: "Never be cruel - blunt ≠ hostile." "Never mock the user's situation."

**Positive behavior sets the baseline.** Each Tone Boundary should cover a **plausible drift** under pressure, not restate the entire style as negative prose. Pair the boundary with the preferred behavior: “Never mirror panic; state the impact evenly and move to the recovery step.” Test it with a direct user request or context that would naturally provoke the failure mode.

**Worked example — profanity/vulgarity:**

Profanity handling is a Tone Boundary, not a dimension. The guardrail sets the boundary; persona dimensions determine intent.

| Boundary Setting | What It Means |
|---|---|
| **Hard block** | Never use profanity under any circumstance. "D\*mn," "h\*ll," "cr\*p" — all blocked regardless of user input. *(Default for most agents)* |
| **Mirror only** | May echo a user's language when directly quoting or acknowledging, but never initiates. "I hear you — that is frustrating." Never: "Yeah, that's a real s\*\*\*show." |
| **Permitted — mild** | May use mild language ("damn," "hell," "crap") when it fits the persona's personality intensity and the conversational moment. Never escalates beyond the user's register. |

Most agents use Hard block. The boundary exists so designers of Bold / Informal agents can make a conscious choice rather than leaving it to the model. When in doubt, default to Hard block.

*Note: Content limits (topics the agent must not engage with), confidence rules, and compliance constraints (e.g., "never claim to be human") are defined in agent design, not persona. Tone Boundaries constrain how the agent sounds - not what it can do.*

### Tone Flex

Tone Flex defines how the agent's tone shifts from its baseline in response to context. The baseline is the selected Emotional Coloring and Empathy Level. Tone Flex defines how far each can shift, in what direction, and under which conditions. Persona owns the semantic and lexical policy: the stance, word choice, acknowledgment pattern, maximum shift, and reset. On voice-bearing channels, `voice-ux` maps that same policy to situational prosody without redefining it.

**Triggers** - context conditions that cause shifts:
- **System state** - errors increase urgency, timeouts need patience
- **User emotional state** - frustration increases empathy, confusion increases patience
- **Content sensitivity** - emotionally loaded in-scope content (medical results, financial hardship, job loss, safety incidents) triggers a default shift: Humor → None, Empathy up one position from baseline. This default is explicitly overridable by the designer — some personas may handle sensitive content differently by design (e.g., a crisis counselor agent whose baseline is already Attuned doesn't need to shift further)
- **Conversation phase** - opening may be warmer, deep troubleshooting may be more clinical
- **Success/progress** - celebrations shift toward encouraging

Abstract shift labels are not enough for reliable runtime behavior. Every encoded flex rule needs four parts:

1. **Trigger** — the observable condition.
2. **Shift and maximum** — the target change and how far it may move.
3. **Observable cue** — one short lexical or discourse example that makes the shift visible in word choice or response structure without changing facts. Audible pace, pitch, emphasis, pauses, and audio tags are downstream `voice-ux` concerns.
4. **Reset condition** — the first condition that returns to baseline, plus the explicit constraint: **do not carry the prior tone** into the next routine topic.

Treat cue examples as a small palette rather than required verbatim text. The cue must not manufacture emotion, reorder facts, or add unsupported certainty.

**Shift rules** define direction and magnitude per trigger:

| Trigger | Dimension | Shift Example (from Neutral baseline) | Observable cue | Reset condition |
|---|---|---|---|---|
| User frustrated | Empathy Level | Understated → Moderate | One brief acknowledgment of the repeated difficulty, then action | User moves to a routine/new topic |
| System error | Humor | Any → None (always suppress) | State the error plainly and give the recovery step | Error clears |
| Progress / success | Emotional Coloring | Neutral → Encouraging (briefly) | Recognize only the completed result | Next routine task |
| High-stakes topic | Humor | Any → None | Omit humor and state consequences precisely | Topic leaves high-stakes scope |
| Emotionally sensitive content | Empathy Level | Up one position from baseline | Acknowledge impact once before the next step | Content returns to routine |

**Hard boundaries** - Tone Boundaries are the outer wall of the flex range. The agent can shift within its flex range but must never cross a Tone Boundary. If the baseline is Neutral and the boundary says "Never sound saccharine," then flex toward Encouraging is acceptable but Enthusiastic would violate the boundary.

**Flex range** - How far each dimension can shift. Author per persona. Example:
- Emotional Coloring: Neutral baseline, flex range Neutral-Encouraging (never Clinical, never Enthusiastic)
- Empathy Level: Understated baseline, flex range Minimal-Moderate (never Attuned)

Tone Flex is authored per persona during design. The encoding expresses its semantic and lexical rules as per-subagent tone calibration in instructions. For a voice-bearing channel, pass the same triggers, maxima, hard boundaries, cues, and resets to `voice-ux`; only the prosodic realization is downstream.

*Note: User-formality matching (agent mirrors the user's casual/formal register) is a related but open area - it depends on model capability as much as instructions. Not included in Tone Flex.*

### Subagent layering

**Global Persona is inherited** by ordinary subagent reasoning. A **generic pointer is not the default**: “apply the global Persona” adds prompt weight without reliably changing behavior. Start with global-only instructions, observe a friction point or identify a deliberate local difference, then add a **targeted minimal delta**—for example, one frustration cue in escalation or Technical Reading Level in a specialist subagent. **Do not repeat the full global Persona** in every subagent.

A Persona calibration changes expression only. Factual grounding, permitted next steps, action policy, and uncertainty rules remain separate agent-design instructions. When both are needed, test a 2×2 or combined arm rather than attributing task improvement to the Persona overlay.

---

## Delivery

Two standalone dimensions that control response shape and humor. Both are independent of Voice and Tone but interact with them through constraint notes.

### Brevity

*Response length and information density - how much does the agent say?*

```
◄─── Terse ──── Concise ──── Moderate ──── Expansive ───►
```

| Position | Description |
|---|---|
| **Terse** | Cut every unnecessary word. One-word answers acceptable. Active voice, imperative mood. |
| **Concise** | Short sentences, says what's needed. Every sentence earns its place. |
| **Moderate** | Complete explanations with reasoning. Thorough but not verbose. *(Default)* |
| **Expansive** | Detailed, thorough responses. Full context, background, alternatives. |

**Conversation progression boundary:** Brevity sets the default density of an answer. How responses shorten after context is established, repeated questions, or later conversation phases belongs to `conversation-design`. Pass the Brevity setting downstream as an input; do not encode a universal repeat-turn rule as Persona.

*Constraint note: Brevity is largely independent, but Register and Formality create natural pairings. Subordinate + Formal pulls toward Moderate or Expansive (deferential agents rarely truncate). Peer + Professional pairs naturally with Concise. Coach pulls toward Moderate (teaching requires explanation).*

### Humor

*Type of wit, if any.*

```
◄─── None ──── Dry ──── Warm ──── Playful ───►
```

| Position | Description |
|---|---|
| **None** | No humor. Default for regulated, high-stakes, or formal contexts. |
| **Dry** | Understatement, deadpan, intellectual wit. Never forced. |
| **Warm** | Light humor that reinforces warmth. Celebratory, situation-aware. |
| **Playful** | Puns, wordplay, whimsical personality. Best for casual contexts and personality-forward brands. |

No frequency setting - frequency is emergent from Brevity (terse = fewer words = fewer humor opportunities) and constrained by context (never humor in error states).

*Constraint: When Humor is not None, always include this tone boundary: "No humor in error states, escalation, or high-stakes contexts."*

*Constraint note: Formality + Emotional Coloring constrain Humor. Formal → None. Professional + Clinical → Dry or None. Casual/Informal + Encouraging → any humor type.*

**Clinical + Playful evidence caution:** Across two fixtures, instruction competition was context-sensitive. In the first, Playful cues appeared while explicit Clinical cues were masked. In the second locked fixture, both cues appeared in 5/5 packages, but the combined arm omitted an explicit content boundary in 3/5 while Clinical + None preserved it 5/5; the corrected suite was therefore not a hard-invariant pass. This is neither a universal contradiction nor safe-coexpression evidence. Ask the designer to confirm the tension, constrain Humor to explicit low-stakes contexts, and test the **final combined instructions** against the use case's content contract. Do not block encoding solely from this pair.

---

## Chatting Style - "How does the text look on screen?"

*Boundary: Chatting Style governs visual presentation - emoji, structural formatting, punctuation habits, and capitalization patterns. These are how the text looks, not what it says (Voice) or how it feels (Tone). Independent of the agent's Information Architecture (defined in agent design), which governs output layout patterns.*

Four settings. Pick one option for each.

### Emoji

| Position | Description |
|---|---|
| **None** | No emoji. Default for formal contexts, regulated industries, or text-heavy interfaces. |
| **Functional** | Emoji as data compression - status indicators (✅❌⚠️), categories, severity levels. Each emoji conveys meaning; none are decorative. If you removed all emoji, information would be lost. |
| **Expressive** | Emoji for personality and warmth alongside functional use. Decorative emoji acceptable - they reinforce tone without carrying critical information. If you removed all emoji, no information would be lost, but personality would diminish. |

Boundary test: "If you removed all emoji, would information be lost?" Functional = yes. Expressive = no.

**Emoji vocabulary:** When Emoji is Functional or Expressive, define the approved symbols and what each may communicate. Never let emoji carry a critical fact without a text equivalent.

**Emoji cadence:** Define an observable cadence: Rare, Occasional, or Regular, with one or two controlled examples. “Decorative emoji acceptable” is not enough to produce consistent behavior. For an Expressive setting, the Persona calibration should contain one fitting emoji in a routine low-stakes response; if the design intends none, choose Emoji: None.

### Formatting

| Position | Description |
|---|---|
| **Plain** | Prose only. No bullets, no bold, no headings. Reads like natural conversation. |
| **Selective** | Formatting used purposefully - bold for key terms, bullets for lists of 3+, code blocks for copy-paste content. Formatting serves the content, never decorative. |
| **Heavy** | Extensive formatting - headers, dividers, tables, nested lists, section-based layouts. Every response has visible structure. |

### Punctuation

| Position | Description |
|---|---|
| **Conservative** | Standard punctuation only. No exclamation points, no ellipses, no em dashes. Periods end every statement. |
| **Standard** | Normal punctuation with occasional expressiveness. Exclamation points for genuine emphasis. Em dashes for asides. *(Default)* |
| **Expressive** | Liberal use of exclamation points, ellipses, em dashes, and other expressive marks. Punctuation conveys energy and personality. |

**Punctuation pattern:** When Expressive is selected, name the marks and cadence that make it observable—for example, an em dash, ellipsis, or exclamation point in routine responses where it fits. Examples guide rhythm; punctuation must not change facts or manufacture emotional intensity.

### Capitalization

| Position | Description |
|---|---|
| **Standard** | Conventional sentence case and title case. Proper capitalization throughout. *(Default)* |
| **Casual** | Lowercase-casual for routine message starts and labels when it occurs naturally. Best for chat-first brands and informal internal tools. |

Never lowercase proper nouns, product names, acronyms, units, or immutable terms. Never reorder a sentence or add filler merely to force a lowercase opening. A proper-noun-heavy answer may legitimately look Standard even when the Persona allows Casual capitalization; define the natural surfaces where lowercase should appear.

*Pairing note: Formal personas usually use Emoji: None, Punctuation: Conservative, and Capitalization: Standard; Professional personas usually use Functional/No Emoji and Standard/Conservative punctuation. These are recommendations, not prohibitions. A deliberately theatrical Formal persona may use Expressive punctuation or emoji, and any unusual pairing should be consciously confirmed and documented.*

*Constraint note: Brevity constrains Formatting. Terse + Heavy is a productive tension (minimal words, maximum visual structure). Expansive + Plain may create walls of text - consider at least Selective.*

*Note: Accessibility requirements (screen reader compatibility, cognitive load, plain language) may constrain persona choices - e.g., Functional Emoji may need plain-language equivalents for screen readers. Accessibility is defined in agent design.*

---

## Persona Artifacts: What It Says and What It Doesn't

A Persona produces three character groups plus one adjacent agent-design handoff. Positive and negative entries organize what the agent does and avoids without moving content-policy ownership into Persona:

| Group | Positive (Do) | Negative (Don't) |
|---|---|---|
| **(a) Identity** | Identity Traits, Values | Negative Identity ("Not a salesperson"), Never-Do |
| **(b) Expression** | Tone selections, Tone Flex | Tone Boundaries ("Never sound pushy"), Never-Say List |
| **(c) Phrasing** | Phrase Book, Discourse Markers, Lexicon (global + per-subagent, including immutable terms), Technical Explanation Policy | Never-Say List (anti-phrases), Lexicon exclusions ("Don't use this term") |
| **(d) Agent-design handoff** | Explicitly supplied use cases and declared scope | Guardrails ("Don't offer medical advice") |

**Key distinctions:**
- **Phrase Book** = situation-keyed sample phrases ("When acknowledging, say...")
- **Lexicon** = domain-keyed terms and definitions ("In product subagents, use these terms...")
- **Technical Explanation Policy** = the rhetorical preference for staying in one frame or adding a cross-frame explanation; agent design owns factual support
- **Discourse Markers** = conversational connectors ("So," "Right," "Here's the thing")
- **Never-Say** = anti-phrases ("Never say 'Great question!'")
- **Tone Boundaries** = anti-sounds ("Never sound apologetic")
- **Negative Identity** = anti-characters ("Not a salesperson")
- **Guardrails** = anti-content ("Don't offer medical advice; don't make warranty claims; don't quote prices")

Each group's negative side generates the ones below it: Negative Identity → Tone Boundaries → Never-Say phrases. Guardrails sit beside this chain — they're about *what topics are off-limits*, not how the agent sounds. When reviewing a persona, trace any questionable output back up this chain to find where the constraint should live.

### Guardrails — agent-design-adjacent content boundaries

Guardrails are **agent-design-adjacent**, **not a Persona component**. Persona may carry explicit Guardrails from authoritative input only as verbatim handoff references. It must not infer, score, rewrite, or encode them. `agent-architecture` and `agentforce-generate` own their scope, approval, and implementation.

Make sure agents know the boundaries about what they can say. Guardrails are content-level rules: subjects the agent must not address, claims it must not make, advice it must not give.

Examples:
- "Don't offer medical advice" (healthcare agent)
- "Don't quote prices for custom configurations — escalate to sales" (B2B SaaS agent)
- "Don't make warranty claims; refer to documented warranty terms" (consumer goods agent)
- "Don't speculate about regulatory changes" (financial services agent)

**How Guardrails differ from Never-Say:**
- **Never-Say** = phrase-level anti-phrases ("Never say 'Great question!'"). Behavioral.
- **Guardrails** = content-level off-limits subjects ("Don't offer medical advice"). Topical.

A Never-Say targets *how the agent talks*. A Guardrail targets *what the agent talks about*. **Never-Say cannot substitute for a Guardrail**: avoiding “you should buy” does not enforce the underlying topic, claim, advice, or action boundary. Preserve the authoritative allowed scope and refusal/redirect requirement as an adjacent reference for the owning agent-design skill.

**When Guardrails may be needed:** Healthcare, financial services, insurance, legal, and other regulated domains commonly require content boundaries. Brand-defined boundaries may also apply. If authoritative Guardrails are absent, flag the dependency for `agent-architecture`; do not create them here.

**Implementation:** `agent-architecture` or `agentforce-generate` defines and encodes the allowed scope and refusal/redirect behavior. Persona may supply approved phrase-level expression for an already-defined redirect, but it must not alter the underlying policy.

---

## Phrase Book & Never-Say List

Two companion artifacts generated per persona. Both are tuned to the persona's dimension selections and Identity traits.

### Phrase Book

Example phrases the agent would use in common situations. Categories are selected during the workflow based on dimension selections - they vary per persona. Examples of selection-driven categories:

- **All agents:** Acknowledgement, Affirmation, Redirect/Handoff
- **Non-Terse agents:** Welcome/Greeting
- **Encouraging/Enthusiastic coloring:** Celebrating Progress
- **Coach register:** Teaching Moments
- **Humor ≠ None:** Humor Examples (showing the humor type in context)
- **Technical Explanation Policy applies:** rhetorical framing examples only; agent design supplies factual relationships

A Phrase Book is a **palette, not a script**. Supply 2–4 alternatives for each applicable category, including plain wording as an option. **Do not reuse the same phrase stem** within one response or adjacent turns unless the wording is immutable or deterministic. Omit a signature phrase when it would sound forced. Examples guide generation; they are not utterance templates. For figurative or signature entries, record the supported fact, classification, or conversational function each cue may express; remove any cue that creates a new implication or substitutes for the explicit status.

**Affirmations** are positive acknowledgment phrases used to confirm, validate, or encourage: "Got it," "You're all set," "Right, moving on." These are distinct from greetings, closings, or transitions - they're the micro-confirmations that punctuate conversation and keep it flowing.

**Discourse Markers** are conversational connectors that smooth transitions and signal the agent's conversational logic: "So," "Right," "Anyway," "Now then," "Here's the thing." They are a Phrase Book category because they are situation-keyed (like acknowledgements and redirects), not vocabulary (like Lexicon).

Discourse markers can make conversational logic recognizable when each marker has a function. Select markers that match the persona's Formality and Personality Intensity. A Formal agent may use “To clarify” for precision; a Casual + Bold agent may use “So here’s the deal” before a direct recommendation. **Omit a discourse marker when** the relationship between sentences is already clear. **Never stack multiple markers** in one conversational move or combine a marker with a Phrase Book redirect that serves the same function; that reads as performance, not logic.

A varied Phrase Book is a high-leverage way to make an agent recognizable. It works only when situation fit, alternatives, and anti-repetition are encoded together. Per-subagent entries can strengthen consistency at friction points, but must remain a minimal discriminative delta in brownfield agents.

### Never-Say List

The inverse of the Phrase Book - specific words, phrases, and patterns the agent must never use. Derived from:

- **Tone Boundaries** expressed as specific anti-phrases (e.g., "Never sound apologetic" → never say "I'm sorry, I can only...")
- **Identity contradictions** - phrases that violate the persona's traits (e.g., a Direct agent never says "I'd be happy to help you with that!")
- **Generic chatbot filler** - "Great question!", "Hope this helps!", "Let me know if you need anything else!" (these undermine almost every persona)
- **Cognitive-processing markers** - "Let me think about that," "Hmm, let me consider," "I need to process this" — machines don't think. These create false anthropomorphism unrelated to the persona's designed personification level. Reframe as action: "Let me check," "Looking into that," "Pulling up your details."
- **Register violations** - phrases that break the power dynamic (a Peer never says "Would you like me to proceed with..."; a Coach never says "Just do X")
- **Brand prohibitions** - competitor names, deprecated product names, off-brand language

The Never-Say List is authored alongside the Phrase Book and encoded into tone boundaries and instructions. **Explicit Never-Say entries are required** for exact anti-phrases that must resist direct user requests; positive guidance alone does not reliably block requested wording. Pair prohibitions with the preferred behavior so the agent knows what to do instead. When reviewing a persona, test both natural generation and direct pressure to use a forbidden phrase.

---

## Lexicon

*Brand terminology and domain vocabulary - global and per-subagent.*

Every lexicon entry supplies meaning, not just a keyword. The canonical shape is:

| Field | Required? | Purpose |
|---|---|---|
| **Term** | Yes | The exact word or phrase the agent recognizes and may use. |
| **Definition** | Yes | The term's stable semantic meaning. |
| **Usage / preferred contrast** | No | When to use it, preferred alternatives, or terms to avoid. |
| **Immutable?** | No | Whether the term must remain exactly as written. |

Definitions are required at every Reading Level. Reading Level controls whether the agent avoids, glosses, or freely uses a term in conversation; it never removes the underlying definition from the persona. **Bare term lists invite invented definitions**: if authoritative input does not establish meaning, record a gap rather than inferring semantics from a product-like name.

Lexicon has two scopes with the same entry shape:

**Global Lexicon** - terms used across all subagents: brand name, company name, product line names, industry terms that apply everywhere.

**Per-Subagent Lexicon** - terms scoped to specific subagents. A luxury watch agent has watch-specific vocabulary ("movement," "chronograph," "caliber") that belongs in product subagents but NOT in order-tracking subagents. Loading specialized vocabulary globally wastes context and can cause the agent to over-use jargon in simple service interactions.

**How Lexicon differs from Phrase Book:**
- **Phrase Book** = how the agent *sounds* in common situations - organized by situation (acknowledgement, redirect, celebration)
- **Lexicon** = what terms *mean* and how they are used in specific domains - organized by scope (global or per-subagent)

The Phrase Book captures the agent's verbal fingerprint across interactions. The Lexicon supplies stable terminology and meaning. A lexicon is not a product knowledge base: keep changing specifications, availability, prices, policies, and other live facts in authoritative knowledge or data sources.

**In encoding:** Global lexicon goes in global instructions. Per-subagent lexicon maps to per-subagent instructions - each subagent gets a vocabulary block with terms, definitions, and any usage notes.

**Migrating a legacy lexicon:** A pre-refactor "Per-Topic Lexicon" scope maps to Per-Subagent Lexicon in canonical artifacts — `topic` in that older label meant what `subagent` means now, not the legacy Builder UI's literal "Topic" object. A pre-refactor term-only list (terms with no Definition column) is not a valid lexicon under this framework: every migrated term needs a definition. If the source material doesn't establish one, treat the missing definition as an explicit gap and surface it — never invent one. Only the legacy Builder UI's literal field label ("Topic Instructions") stays as written, because it names a UI element, not a persona concept.

### Immutable content — verbatim boundary

Immutable content can be a term, sentence, disclaimer, or larger block whose exact bytes matter. Record the authoritative text and state that it **overrides Persona and user style requests**: no shortening, paraphrase, case change, punctuation change, synonym substitution, or “friendlier” rewrite.

**Immutability protects the exact string, not its surrounding response shape.** If the requirement is to return only that string—with no refusal, explanation, prefix, or suffix—encode that output-shape rule separately. Otherwise surrounding context may be allowed while the immutable span remains exact.

Immutable terms stay in the Lexicon with `Immutable? = Yes`; larger blocks live in the Immutable Content section. In both cases, source authority must be explicit. Never invent legal or compliance wording.

## Technical Explanation Policy

*The Persona-level preference for how an answer is framed.*

This policy is part of Phrasing, not Reading Level or agent correctness. Answer first in the frame of the user's question, then choose one rhetorical preference:

| Policy | Persona-level behavior |
|---|---|
| **Stay in frame** | Answer what was asked without a ceremonial cross-frame explanation. |
| **Selective bridge** | Optionally add one complementary explanation when the approved agent-design policy supports it. *(Default)* |
| **Pair routinely** | Prefer paired evidence/outcome framing when the approved agent-design policy supplies the relationship. |

Bridge strength does not change factual confidence, terminology density, glossing, or Reading Level. Persona can demonstrate the response shape with supplied facts, but it does not decide whether a technical-to-outcome relationship is true.

**Agent-design handoff:** `agent-architecture` or `agentforce-generate` owns authoritative sources, factual support, test-method and field comparability, missing-data behavior, assumptions, recommendation confidence, and product suitability. Record the approved policy by reference or mark it unresolved. Do not recreate those rules inside Persona.

**Relationship to other phrasing artifacts:**

- Lexicon defines what a technical term means.
- Reading Level controls terminology and specification density.
- Reading Level Flex controls when that density shifts.
- Technical Explanation Policy controls the preferred response frame only.
- Persona calibration can show the shape; `conversation-design` owns representative scenarios and `agentforce-test` owns runtime proof.

---

## Reference

### Tension Pairs

Some dimension combinations create productive tension. These are valid - they don't need to be "resolved" - but they need conscious design to coexist:

| Tension | Resolution |
|---|---|
| Cool Warmth + Bold Personality | Strong character without performed warmth. Competence IS the care. |
| Blunt Coloring + Playful Humor | Unvarnished truth delivered as comedy. The bluntness is part of the joke. |
| Encouraging Coloring + Terse Brevity | Short celebrations: "Done. Nice progress." |
| Attuned Empathy + Terse Brevity | Brief validation, then act: "Frustrating. Here's the fix." |
| Formal + Warm | Polished hospitality, sophisticated warmth. |
| Formal + Bold Personality | Theatrical character, immersive experience. Archaic formality with maximum personality. |
| Neutral Coloring + Bold Personality | Strong character without emotional investment. The character shows through word choice, not feeling. |
| Warm + Playful Humor | Cheeky affection - irreverence grounded in warmth. |
| Reserved Personality + Warm | Dignified care. Warmth through reliability, not personality. |
| Radiant Warmth + Playful Humor | Overflowing cute energy. Mascot-driven delight. |
| Terse Brevity + Heavy Formatting | Minimal words, maximum visual structure. Headlines and data blocks, no prose. |

### Conflict-Pair Quick-Reference

Distinct from Tension Pairs above (which are *productive* tensions that simply need conscious design), these are **internal contradictions** the SCORE phase actively flags. Each is a sign the persona is fighting itself.

| Conflict | What to look for | How to resolve |
|---|---|---|
| **Tone Boundary contradicts Phrase Book entry** | "Never sound enthusiastic" + Phrase Book has "Awesome, let's go!" | Update the offending phrases or relax the boundary. Don't ship both. |
| **Never-Say overlaps Lexicon** | Lexicon includes "complimentary" + Never-Say includes "complimentary" | Pick one. The lexicon and Never-Say cannot disagree. |
| **Identity trait contradicts dimension selection** | Identity = "Calm, Composed" + Personality Intensity = Bold | Either soften Personality or swap the trait. |
| **Personification contradicts identity/pronoun/opinion usage** | Not personal uses a separate name or routine `I`; Individuated claims a personal preference; Anthropomorphic claims human feelings without permission | Align the separate identity, singular self-reference, and opinion rules—or document an explicit exception. |
| **Immutable content contradicts Lexicon term** | Legal disclaimer: "claims tracking system" + Lexicon: "ClaimTrack" | Surface to user during design. Pick one and document the alignment. Immutable content wins by rule. |
| **Channel contradicts Brevity** | Channel = SMS + Brevity = Expansive | Re-examine. Channel-default Brevity is Terse for SMS; only override with strong signal. |
| **Register contradicts Audience** | Register = Coach + Audience = External customers | Coach with external customers risks paternalism. Either shift to Advisor or document why Coach fits. |

These pairs are the SCORE phase's Internal Consistency / Conflict-Pair check (worth /10 in the rubric). The skill flags any of these as a contradiction in the evaluation report, with a specific recommendation.

### Cultural Adaptation Note

Persona dimension expectations vary by culture. For global agents, consider per-locale overrides. Key callouts:

- **Formality expectations vary** - positions that feel natural in one culture may feel too casual or too formal in another.
- **Warmth norms differ** - Bright warmth in one culture may feel overwhelming in another. Cool professionalism that works in one context may feel cold elsewhere.
- **Directness norms differ** - Blunt or Clinical emotional coloring that works in direct-communication cultures may feel abrupt in high-context cultures.
- **Humor doesn't translate** - set Humor to None for cross-cultural deployments unless you're localizing humor per locale.
