# What this skill does

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## What this skill does

This skill takes an Agentforce agent — chat or voice — and applies voice UX expertise to it. The output is a voice-optimized rewrite with every change cited to a specific voice UX principle, plus (optionally) a deployable `.agent` file and publish to your org.

It works for two audiences:
- **Developers** building or refining a voice agent — drives the audit, generates the `.agent` file, walks you through deploy and publish.
- **PMs and conversation designers** driving a voice migration without writing `.agent` files themselves — produces a planning bundle you can review with stakeholders and hand to a developer.

Both audiences need the same three inputs (see Prerequisites below). The flow is the same; only Phases 7–8 (`.agent` generation + publish) require running developer commands. If you stop at Phase 6, the planning bundle is independently useful as a handoff artifact.

**Typical session: 15–30 minutes.** You'll be asked:
1. For your script and sample conversation (Phase 1).
2. To confirm the mode the skill inferred (Phase 3).
3. A few short questions about your voice channel — channel type, crossmodal handoff channels, IVR/carrier-side announcement — and about the voice itself: gender presentation, age, accent, who's calling (Phase 3).
4. Whether to continue to a deployable `.agent` file (Phase 6 → 7, optional).
5. Whether to publish to your org (Phase 7 → 8, optional, requires explicit confirmation).

**What you'll get back:** a layered bundle (rewritten LLM instructions, user-facing copy, spoken-function phrasebook, opening sequence, out-of-script handoff notes), a vocal identity file (brief, casting sides, audition record), an inline audit citing each change, and, if you opt in, a compiled `.agent` file, a published draft agent, and an optional interactive HTML summary.
