# Phase 9 — Stakeholder HTML artifact (optional)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 9 — Stakeholder HTML artifact (optional)

After the bundle (Phase 6) or the `.agent` file (Phase 7) exists, optionally offer to generate a single self-contained interactive HTML page that communicates the migration/optimization to a team — PMs, developers, QA, and executives at once. **Offered, never automatic.** It's a communication layer built *from* the bundle and the sample conversation; it introduces no new design decisions.

When the developer opts in:

1. Read `references/stakeholder-html-artifact.md` for the reusable patterns and the bundle→HTML mapping. **Treat it as inspiration, not a strict template** — pull the patterns that fit this project, drop the ones that don't. Don't force a fixed structure.
2. Build the page from the existing artifacts: Layer B + inline audit → before/after compare-cards; summary categories → filter chips; Layer A + Layer D → journey tabs; sample conversation → conversation trees; Layer E + config deltas → the dark config-delta table.
3. Keep it self-contained: one `.html` file, inline CSS/JS, vanilla JS, no build step, no CDN frameworks (Google Fonts link is fine).
4. Write to `artifacts/voice-ux/<api_name>-voice-summary.html`. Offer to open it and iterate on stakeholder feedback.

This is a stakeholder-communication aid, not a canonical artifact — the bundle and `.agent` file remain the sources of truth.
