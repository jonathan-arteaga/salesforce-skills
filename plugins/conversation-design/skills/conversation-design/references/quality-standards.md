# Quality Standards

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Quality Standards

A well-formed conversation-design draft:

- **Three scenarios, one of each type** — no second happy path, no two error states; the cap is the cap. If a fourth scenario is critical, it earns its place in the team's expansion of this draft, not in this skill's output.
- **Turn count within bounds** — 4 ≤ turns ≤ 8 per scenario. Outliers either need to split or aren't ready to design.
- **`actions[]` and `components[]` are honest** — populated only when the upstream files (`actions.yaml`, Concept Design markdown, or Style Guide draft) exist. Empty arrays when grounding is missing; never a fabricated ID or slug. The reason for empty arrays surfaces in `global_notes`.
- **Voice is honest about its source** — persona-grounded when persona exists, generic + flagged when it doesn't. Never fabricate persona signals.
- **Notes are useful, not ceremonial** — every scenario lists at least one open question / voice flag / decision deferred *that's actually open*. Empty notes is acceptable when the scenario is genuinely unambiguous; padding notes with filler is worse than leaving them empty.
- **`draft: true` everywhere by default** — the skill never writes `draft: false`. Only the team / an AXS pass flips a scenario to shipped.
- **Error state is plausible, not catastrophic** — model a real break the team is likely to encounter, not a worst-case enumeration of every failure mode.
- **Fallback exits gracefully** — every fallback scenario ends with a clear exit (escalation offered, deferral stated, alternative suggested), not a deadend.
- **Channel-intrinsic prosody cues** — voice / multimodal scenarios populate `prosody_cues[]` from a small canonical set; chat-channel scenarios leave it empty.

---
