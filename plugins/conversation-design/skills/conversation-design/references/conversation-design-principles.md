# Conversation design principles reference

The 6 principles the conversation-design skill audits scenarios against. Use as the citation source for each scenario's `notes` field and the `design_decisions_pending` block.

**Source lineage:** Conversation Design Institute (CDI) sample-dialog-first design and persona-led voice; Google Conversation Design Guidelines (Grice's cooperative principle, no-dead-ends); Cathy Pearl, *Designing Voice User Interfaces* (error typology); Nielsen Norman Group (voice vs tone, error-message principles); Salesforce Agentforce architecture (topic boundaries, classification descriptions). Synthesised for early-fidelity scenario design — not a substitute for the full corpus-grade pass an AXS leads.

**Citation prefix:** **CD** (e.g., `CD1-one-breath`, `CD3-no-dead-ends`).

The rubric is *load-bearing*: every scenario the skill writes must surface at least one citation per scenario in `notes`, naming the principles the scenario honours and any it intentionally violates. Uncited scenarios are treated as drafts, not preview-ready.

---

## CD1 — One Breath Test

**Summary:** Every agent turn must be speakable in a single breath. In voice this is literal — a turn longer than ~7s spoken (~100 words) cannot be uttered without a pause that may be parsed as turn-end. In chat this is figurative — a turn longer than ~3 short paragraphs is read in chunks, and the user loses the thread.

**Why it matters:** Long turns starve the conversation of feedback. The user can't course-correct mid-stream; the agent can't tell whether it's been understood. Both modalities suffer, voice acutely.

**How the skill applies it:**
- Cap any single agent turn at ~3 sentences for chat, ~7s spoken for voice.
- Where a turn would exceed that, split — either into two turns with a beat between, or by deferring the longer content (e.g. a list of options) to a follow-up turn.
- Surface in `notes`: *"Turn 3 split — original violated CD1; recovery turn 4 picks up after user acknowledgement."*

**Common mis-applications:**
- Long turns chunked into short visible lines but still uttered as a single utterance at runtime — the chunking is cosmetic, not functional.
- Welcome / opening turns front-loaded with policy ("I'm an AI agent, your conversation may be recorded, …") that defeats the breath test before the conversation starts.

**Lineage:** CDI's "One Breath Test"; Pearl's chunking principle for voice.

---

## CD2 — Tapering

**Summary:** Verbosity reduces as the user demonstrates competence. Early turns over-explain and offer scaffolding; later turns shorten as the user finds rhythm. By the third or fourth user turn, the agent should be matching brevity, not over-instructing.

**Why it matters:** Constant explicit scaffolding ("To check your balance, just say 'balance'") feels patronising once the user has shown they understand the interaction. Tapering signals that the agent is *paying attention* to the user, not running a script.

**How the skill applies it:**
- Compare agent verbosity across turns 1, 3, 5. If turn 5 isn't shorter than turn 1, the scenario isn't tapering.
- Acknowledgments shorten across the scenario (turn 1: "Got it — let me check that for you"; turn 5: "Got it.").
- Scaffolding cues drop as the user demonstrates understanding.

**Common mis-applications:**
- Tapering in the agent's verbosity but not in the agent's *register* — the agent stays formal even after the user has switched casual.
- Tapering applied so aggressively that error recovery turns become curt and feel cold.

**Lineage:** CDI's tapering principle; Pearl's adjacency-pair acknowledgment economy.

---

## CD3 — No Dead Ends

**Summary:** Every fallback offers a next move. The agent never terminates a conversation with "I can't help" without offering an alternative — escalation, deferred capability, channel switch, or graceful close with a way back in.

**Why it matters:** A dead end teaches users that the agent is unreliable. They'll either churn or escalate at every future ambiguity. A well-designed fallback is *more important* than a well-designed happy path; it's where trust is made or lost.

**How the skill applies it:**
- Every fallback scenario must end with an offer: human handoff, a related capability the agent *can* do, a channel-switch suggestion, or a graceful "come back when X is ready" with the path back.
- Out-of-scope refusals must name *why* and *what's next*, not just refuse.
- Surface in `notes`: *"Fallback offers human handoff (CD3); user has a path forward."*

**Common mis-applications:**
- Fallback ends with "Is there anything else I can help with?" — that's a turn-taking move, not a next move. The user already knows the agent can't help; they need a route, not a re-prompt.
- Escalation is named but the handoff path drops state, forcing the user to restart.

**Lineage:** Google CDG's no-dead-ends principle; CDI's refusal-as-design; Pearl's modality-shift escalation tier.

---

## CD4 — End-Focus

**Summary:** Critical information lands at turn-end. Questions are always at turn-end. When offering a choice, present the options first, then the ask. In voice this is non-negotiable — spoken language is ephemeral and the recency effect dominates. In chat, end-focus still holds because users skim.

**Why it matters:** Users remember the last thing they heard or read. Burying the question or the critical confirmation in the middle of a turn means it gets missed.

**How the skill applies it:**
- Reverse turns where the question precedes the context. *"What date works for you? I have slots Tuesday, Wednesday, Friday."* → *"I have slots Tuesday, Wednesday, Friday — what works?"*
- Critical confirmation data (time, location, amount) goes last in the turn, not first.
- Surface in `notes`: *"Turn 4 — confirmation reordered to end-focus on the appointment time, not the SMS confirmation."*

**Common mis-applications:**
- End-focus respected for questions but critical confirmation data buried mid-turn ("I've booked your 3pm at Highgate, and I've sent you a text" — the user remembers "text" and forgets the time).
- Multi-clause turns where the recency effect lands on the wrong piece.

**Lineage:** Google CDG's recency-effect principle; Pearl on turn-final placement; NN/g's scanning research.

---

## CD5 — Persona-Voiced Turns

**Summary:** Every agent turn draws from the persona's phrase book / never-say lists. The agent voice isn't generic-friendly default; it's the persona's voice applied to this scenario's content. When persona is absent at draft time, voice is functional and explicitly flagged for re-voicing.

**Why it matters:** Generic-friendly voice reads as a stock chatbot. Persona-voiced turns read as a *character* the user is interacting with — that's the entire point of persona work, and the conversation design is where it becomes visible.

**How the skill applies it:**
- When persona is present: each agent turn references the persona's phrase book for acknowledgments, refusal language, and tone-flex moments.
- Reference the persona section briefly in scenario `notes` for traceability (e.g. *"Agent voice draws from persona §3 — Voice. Re-tune for error voice that doesn't blame the user."*).
- When persona is absent: write functional turns and add a top-level scenario note flagging every agent turn for re-voicing once persona lands. **Do not invent a persona.**

**Common mis-applications:**
- Persona present but only reflected in turn 1; subsequent turns drift into generic-friendly voice.
- Persona's never-say list ignored — the scenario uses phrasing the persona explicitly forbids.
- Persona's tone-flex rules ignored — voice stays the same on error turns where the persona explicitly softens.

**Lineage:** Persona skill (`persona`); CDI's persona-led voice; NN/g's voice (persistent) vs tone (contextual) distinction.

---

## CD6 — Cooperative Principle (Grice's Maxims)

**Summary:** Each agent turn satisfies the four maxims: **quantity** (as informative as needed, no more), **quality** (only assert what's grounded), **relation** (relevant to the user's last move), and **manner** (clear, ordered, unambiguous). Turns that violate any of the four feel "off" even when the content is technically correct.

**Why it matters:** Conversational AI failures are usually maxim violations, not factual errors. Over-informing on quantity (data dumping), asserting on quality (hallucinating policy, inventing a price), drifting on relation (responding to a different question than asked), and ordering on manner (confusing flow) are the friction patterns users describe as "the bot didn't get me".

**How the skill applies it:**
- **Quantity** — turns answer the user's question, not adjacent questions. No premature offers of related capabilities.
- **Quality** — when the agent doesn't know, it says so. Refusals are designed (CD3); fabrication is forbidden.
- **Relation** — every agent turn is reactive to the user's last turn, not pre-scripted independent of it.
- **Manner** — one ask per turn; options ordered the way a person would volunteer them, not the way the database orders them.

**Common mis-applications:**
- **Quantity** violation — agent answers the question and then offers three related capabilities the user didn't ask for. Reads as a sales pitch.
- **Quality** violation — agent invents a price, policy, or claim the persona's never-say list explicitly forbids.
- **Relation** violation — user asks a follow-up, agent re-runs the original flow from the top.
- **Manner** violation — bundled questions ("What's your name and date of birth?"), data-schema field order ("DOB before name").

**Lineage:** Grice (1975) cooperative principle; Google CDG's maxim-based design; Pearl's adjacency-pair structure.

---

## How the audit cites principles

Each scenario's `notes` field must include at least one principle citation. Format:

```
notes:
  - "Turn 3 — split per CD1 (one breath test); recovery turn 4 picks up after acknowledgement."
  - "Voice draws from persona §3 (CD5)."
  - "Fallback offers human handoff (CD3) and preserves collected fields (CD3 + CD6-relation)."
  - "[review needed] CD2 — tapering not yet applied; persona's tone-flex needs another pass."
```

**Citation tags:**

| Tag | Meaning |
|---|---|
| `CD<N>` | Principle honoured. Surfaces as a justification line. |
| `[review needed] CD<N>` | Principle violated AND intentionality signal present (engagement constraint, persona override). Preserve original; flag conflict for AXS. |
| `[consider] CD<N>` | Principle present but applied weakly. Suggestion only — no rewrite. |
| `[out-of-scope] <signal>` | Pattern detected that this rubric doesn't cover (e.g. multi-intent mid-flow, emotional de-escalation, multilingual handoff). Flag, do not invent. |

**Coverage contract:** the skill must visit every principle for every scenario and return one of: `ok` (counts in summary, not surfaced), `changed` (rewrite applied, surfaced as citation), `review needed`, `consider`, or `out-of-scope`. Silent skips are not allowed — uncovered principles weaken the audit.

---

## Gaps not covered by CD1–CD6

This rubric does not cover (the skill should not invent scenarios that depend on these patterns; flag as `[out-of-scope]`):

- **Multi-intent / context-switching mid-conversation** — the user changes goal mid-flow.
- **Emotional de-escalation** — the user is angry, distressed, or in crisis.
- **Multi-turn cascading error recovery** — a corrected field invalidates downstream collected fields.
- **Multilingual / accent-clash handling** — speaker switches language or accent mid-conversation.
- **Agent-to-agent skill transfer at runtime** — master-agent re-routing visible to the user.

These are AXS-led design decisions. The starter draft flags them and stops; the AXS pass designs them.
