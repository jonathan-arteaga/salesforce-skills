# Conversation Design (Bounded Starter Draft)

Produce a strictly bounded three-scenario starter brief (`conversation-design.json` plus optional customer-clean Markdown export) that teams or Agentic Experience Specialists (AXS) expand into corpus-grade conversation designs.

## Prerequisites & Fidelity Gates

- **Capability cut required:** Require a prioritized capability list (`capabilities.yaml` or normalized inline list) before drafting. Warn if `signoff.status: pending`, but proceed as draft.
- **Do not overwrite shipped work:** On re-run, if any existing scenario has `draft: false`, preserve shipped scenarios intact and only refine explicitly selected draft scenarios.
- **Fidelity mode:**
  - `design-fidelity` *(default)*: Persona, capability cut, and optional architecture are available.
  - `concept-fidelity`: Early sketch with capability outline only; looser concept narratives clearly labeled as early fidelity.
- **Persona handling:** If `persona.md` is absent, draft in a clean neutral voice and flag every scenario for a persona pass—never fabricate persona claims.

## Three-Scenario & Turn-Cap Contract

Every run produces **exactly three scenarios**, each marked `draft: true` and capped at **4-8 turns**:

1. **Happy Path:** Top-priority capability completing end-to-end with zero errors.
2. **Error State:** A realistic system or user error mid-flow (timeout, auth failure, invalid input, lookup empty state, or unbuilt capability) with clear recovery.
3. **Fallback:** An out-of-scope request, escalation trigger, or dead-end boundary exiting gracefully with a concrete next step.

Draft, preview, and confirm **one scenario at a time**—do not dump all three unreviewed at once. Surface the recommended capability, error subtype, and fallback subtype before drafting so the user can override them early.

## Turn-by-Turn Principles (CD1-CD6)

Audit every drafted turn against six core conversation design principles:

| ID | Principle | Check |
| --- | --- | --- |
| **CD1** | **One Breath Test** | Each agent turn reads smoothly aloud in a single breath without dense clauses. |
| **CD2** | **Tapering** | Repeat prompts and confirmations shorten progressively across turns. |
| **CD3** | **No Dead Ends** | Every error and fallback names why and offers a concrete path forward (human handoff, alternate action, or channel shift). |
| **CD4** | **End-Focus** | Place the question or call-to-action at the very end of the turn; strip front-loaded preamble. |
| **CD5** | **Persona-Voiced Turns** | Wording reflects the supplied persona contract without drifting into robotic templates. |
| **CD6** | **Cooperative Principle** | Responses stay truthful, concise, relevant, and unambiguous (Grice's Maxims). |

## Honest Field Gating

- **`actions[]`:** Populate ONLY when `actions.yaml` from architecture design exists. Never invent action IDs; note implied missing actions in `notes` for an architecture revisit.
- **`components[]`:** Populate ONLY when an upstream visual spec or style guide defines component slugs. Otherwise leave empty and state why in `global_notes`.
- **`prosody_cues[]` & Voice Rewrite:** Populate only for `voice` or `multimodal` channels using conservative cues grounded in [voice-ux.md](voice-ux.md). Pre-launch regression testing belongs in `agentforce-test`, not conversation design.
