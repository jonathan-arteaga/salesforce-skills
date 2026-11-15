# Dialect discipline

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Dialect discipline

The skill reads `engagement.language` from the hub config (one of `en-GB`, `en-AU`, `en-US`, or a locale the hub explicitly supports) and uses that dialect throughout **every artefact it drafts** — classification descriptions, global instructions, decision-point `after_text`, variant deltas, markdown export. There is no silent fallback to US English; the chosen region's dialect is load-bearing.

Why this matters: in standalone mode without an explicit locale, generation drifts toward US English even for AU / GB engagements. That produces an inconsistent agent (persona says one dialect, routing descriptions say another), which reviewers correctly reject. Making the dialect a first-class input prevents the drift.

**Dialect is behaviour, not UI.** Nothing is rendered on the page as a `en-GB` chip or a visible region tag; the dialect only shapes the text content the skill produces. Reviewers see the content in their chosen dialect; the skill does not advertise which dialect was selected.

**Fallbacks.**
- `engagement.language` set → use it.
- Hub mode without `engagement.language` → ask once at Step 1 (engagement context), persist to config.
- Standalone mode → ask once at Step 1 (modes), persist to a `./_local/engagement.language` file so re-runs resolve to the same dialect.

Downstream skills (`conversation-design`, `persona`, `voice-ux`, `agentforce-generate`) are expected to resolve the same dialect from the same source. The skill does not re-check their outputs for dialect drift at write-time; the Validate flow (Step 12) checks the drafted content before confirmation.

**Constraints over the framework.** Engagements with novel modalities (voice + multimodal handoff), regulated industries, or unusual integration topologies may push past the 3–6 subagent default. The skill flags exceptions in `notes` rather than silently breaking the rule.

---
