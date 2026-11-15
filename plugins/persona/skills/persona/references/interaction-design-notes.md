---
version: "1.1.0"
date: 2026-09-02
---

## Interaction Design Notes

These guidelines apply across all surfaces — CLI, TUI, web, IDE.

**Output before questions.** Show generated content first, then ask a concise question with short options.

**Batch independent questions.** When multiple questions have no dependency relationship, present together. Examples:
- Context essentials (channel + company + audience + use case) — ask together
- Voice dimensions (Formality, Warmth, Personality Intensity, Reading Level) — ask together; author Reading Level Flex after the baseline is confirmed
- Chatting Style dimensions (Emoji, Formatting, Punctuation, Capitalization) — ask together

Do NOT batch across dependency boundaries. Identity → Personification → Register → Voice → Tone → Delivery → Chatting Style is sequential.

**Short labels, descriptions underneath.** Options scannable in under 2 seconds.

**Multi-select when appropriate.** Phrase book entries to keep, subagents to encode, surfaces to target — allow multiple selections.

**Compact output formats.** Tables for dimensions, lists for phrases, no walls of prose.

**Progress awareness.** Before showing the HUB after a phase/spoke, show a one-line status:
> "Clover: ✓ Identity · ✓ Dimensions · ✓ Phrase book (18) · ✓ Never-say (8) · pending: name, encoding"

**Confidence callouts.** After presenting a drafted persona, highlight 1-2 lowest-confidence dimensions:
> "Least certain: Humor (defaulted) and Emoji (defaulted). Adjust these first if they matter."

### Bounded one-pass output discipline

Write artifacts before composing the response. When `completion_mode = bounded_one_pass`:

1. Prioritize the artifact the user needs to act on—usually the encoded `.agent` file or brownfield proposed file/diff.
2. Write every requested artifact to its canonical path before summarizing.
3. Return a compact artifact index with path, completion status, and key assumptions.
4. Keep prose between requested sections short; do not echo every complete artifact when the surface exposes written files.
5. If the surface does not expose files and the user asked to see an artifact, show the requested artifact while compressing commentary—not the artifact itself.
6. Never omit a requested artifact to save tokens. If an artifact cannot be completed, mark it failed and state the exact missing dependency.
7. Do not present the HUB or ask a routine follow-up at the end of a one-pass run.

---
