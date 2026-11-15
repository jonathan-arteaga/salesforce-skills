# HUB

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## HUB

After every DRAFT-phase or post-DRAFT spoke exit, present the HUB. Standalone WORKSHEET and WORKSHOP requests end with the requested artifact instead. **Not a flat menu** — the suggested next step is rendered as a labeled primary recommendation with rationale, above the rest.

```
HUB

  Suggested next:
  → [SUGGESTED] — [one-line rationale grounded in current state]

  Or do something else:
    Phases:
      → REFINE              [state-aware annotation, e.g., "re-run; iterate on dialog"]
      → SCORE               ["how good is it?"]
      → ENCODE              [gating note if name_decision pending]
    Spokes:
      ⊙ NAME                [annotation: "name_decision pending" or "current: [name]"]
      ⊙ FILL OUT            [annotation: what's empty, e.g., "Lexicon empty"]
      ⊙ ADJUST              [annotation: gated reason if not available]
      ⊙ CHECKLIST           ["what's filled in?"]
      ⊙ WORKSHEET           ["stakeholder questions"]
      ⊙ WORKSHOP            ["facilitated session plan"]
  Exit:
    → I'm done
```

**Suggestion logic:**
- Just exited DRAFT → suggest REFINE
- Just exited REFINE → suggest SCORE
- Just exited SCORE with passing score → suggest ENCODE
- Just exited SCORE with failing score → suggest FILL OUT or ADJUST (whichever has the largest surfaced gaps)
- `name_decision: pending` and ENCODE was attempted → suggest NAME, then resume ENCODE
- After every post-DRAFT phase/spoke → user can always pick anything, including the one just exited

---
