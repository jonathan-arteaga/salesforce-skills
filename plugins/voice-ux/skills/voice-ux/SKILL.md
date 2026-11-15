---
name: |-
  voice-ux
description: |-
  Adapt an existing Agent Script for voice casting, voice tuning, prosody, audio tags, pronunciation, STT bias, and `modality voice:`. Return a voice brief and authorized script changes. Use persona for character and linguistic style.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.

For industry-specific agents, cross-industry ideation, or role/personality choices, read the selected patterns in [industry and role design](references/shared/industry-patterns.md). Use them within this skill’s ownership; distinguish documented capabilities from proposed designs.


# Voice UX for Agent Script

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## What this skill does

Read [`references/overview-and-session.md`](references/overview-and-session.md) when explaining the skill, its audiences, or what a typical session asks.

## How to Use

Read [`references/how-to-use.md`](references/how-to-use.md) when explaining migrate versus optimize mode or what the bundle contains.

## Prerequisites

This skill has three required inputs at intake — without all three, it refuses to proceed:

1. **The source Agent Script** (`.agent` file, YAML, or text instructions).
2. **A sample conversation** showing the main use case (turn-by-turn transcript). Real production logs, hand-written mockups, or the developer's best guess are all acceptable — but the developer is responsible for representativeness.
3. **`agentforce-generate`**, which provides Agent Script syntax and CLI guidance. Resolve it in Phase 0.

**Optional authoritative input:** a completed Persona from the `persona` skill: `persona-handoff.json`, `persona.md`, or both. When supplied, it is the character contract for the voice adaptation. Preserve its exact Never-Say entries, immutable content and response shape, Lexicon meaning, explicit Guardrails, and the semantic boundaries of Tone Flex. Existing Agent Script business logic and compliance constraints remain authoritative for behavior. Any conflict between those sources is `[review needed]`, never a silent choice.

<b>The boundary with </b>**`persona`****, in one line:** `persona` decides who the agent is and what it would say. This skill decides what that character sounds like on a phone line and how it behaves in spoken time. That covers the Vocal Identity brief, casting, light tuning, prosody, phrasebook adaptation, pronunciation/STT and `modality voice:`.

Persona's character contract (Never-Say, immutable content, Lexicon, Guardrails, Tone Flex semantics) is the boundary this skill works within. It may shorten, chunk, re-voice and add audible variants. It never redefines the character. Conflicts are marked `[review needed]`.

**Why agentforce-generate is required (not optional):** the audit and rewrite both depend on knowing what `.agent` syntax will compile. Phase 5 produces directives that are written *into* an `.agent` structure; Phase 7 renders them into a deployable file; Phase 8 publishes. Even the planning bundle is shaped by Agent Script grammar — without the companion skill, the rewrite drifts into instructions the platform won't accept.

If `agentforce-generate` is missing from every supported location, the skill refuses to proceed at **Phase 0 (dependency gate)**. In SF Pi, check the managed effective tree through `/sf-skills` before suggesting any generic installation. A managed copy is already installed even when it is manual-only.

**Recommended companions (not required, but called out where relevant):**

- `agentforce-test` (sf-skills) — post-deploy test specs (`AiEvaluationDefinition`). The V1 review checklist includes a pilot-testing section; this skill is what runs those.
- `agentforce-observe` (sf-skills) — production session traces. Useful in **optimize** mode when the source script is already in production and trace data is available — the audit can ground itself in real conversations rather than instructions alone.
- `persona` — character design. If extraction reveals that the source has no coherent character contract, recommend running `persona` BEFORE Phase 4. When a completed Persona (`persona-handoff.json` and/or `persona.md`) is available, accept it as the optional authoritative input rather than redesigning the character here.

## Phase 0 — Dependency gate (runs before anything else)

Resolve the `agentforce-generate` skill before drafting. Start with the skill location provided by the host or the sibling `../agentforce-generate/SKILL.md` beside this skill in the Salesforce plugin. For marketplace installs, select the installed `agentforce-generate:agentforce-generate` entrypoint from the host skill list or its individual package under the same marketplace cache. For loose Codex installs, check the project and user `.agents/skills/agentforce-generate/` directories. If using SF Pi, prefer its managed effective tree (`~/.pi/agent/sf-skills/effective/skills/agentforce-generate/SKILL.md`) over the source checkout.

Read the dependency's entrypoint and the sections relevant to the requested workflow. If the dependency is unavailable, explain what is missing and point the user to the personal Salesforce plugin or the maintained Salesforce skills collection. Pause the workflow; do not install a duplicate or claim the dependency was checked without filesystem or attachment access.

For a shell-based check, set `VOICE_UX_SKILL_DIR` to this skill’s actual directory. If the host exposes the dependency directly, use that copy.

```bash
# agentforce-generate-resolver-v1
AGENTFORCE_GENERATE_SKILL=""
for candidate in \
    "${VOICE_UX_SKILL_DIR:+$VOICE_UX_SKILL_DIR/../agentforce-generate/SKILL.md}" \
    "$HOME/.pi/agent/sf-skills/effective/skills/agentforce-generate/SKILL.md" \
    "$HOME/.agents/skills/agentforce-generate/SKILL.md" \
    "$PWD/.agents/skills/agentforce-generate/SKILL.md"
do
    if [ -f "$candidate" ]; then
        AGENTFORCE_GENERATE_SKILL="$candidate"
        break
    fi
done

if [ -z "$AGENTFORCE_GENERATE_SKILL" ]; then
    exit 1
fi
printf '%s\n' "$AGENTFORCE_GENERATE_SKILL"
```

### Re-check on resumption

If a previous turn ended at this gate and the user reports they have now installed it ("done", "installed", "try again"), **re-run the filesystem check** before proceeding. Do not take their word for it. If the check still fails, stop again with the same message.

## Long-running phase conventions — verbose progress required

Several phases routinely take more than 5 minutes on real migrations. During those, **emit at least one progress line every 60 seconds**. Don't go silent.

| Phase | Typical duration | Progress signals to emit |
| --- | --- | --- |
| Phase 4 (audit) | 3–8 min | "Loading 14 principles…", "Checking pattern A01…", "5 of 60 patterns checked, 3 hits so far…" |
| Phase 5 (Layer A–E write) | 5–15 min | "Drafting Layer A turn structure…", "Layer B copy edits, 12 of 30 strings done…" |
| Phase 7 (`.agent` generate with self-heal) | 10–30 min | "Iteration 3 of 14 — 2 errors remaining, fixing…", "Z01 lint pass: 31 over-length descriptions truncated", "H01 NGA flag stripped" |
| Phase 8 (publish with self-heal) | 2–10 min | "Publish failed on E007 — diagnosing…", "Retrying with stripped inputs…", "Schema drift detected, surfacing 3 fix options" |

Format: one short sentence, ending with what's coming next so the user can pick up cold. No internal-deliberation narration. No "let me think about" / "I'm going to". State results, not intent.

If a phase stalls (e.g., publish self-heal hits an unknown error), surface the blocker immediately — don't keep emitting progress lines while stuck.

## When to Use This Skill

Read [`references/when-to-use.md`](references/when-to-use.md) when deciding whether a request belongs to this skill.

## Reference Material

The skill consults these local reference sets at runtime. Do not regenerate from external sources — read these.

- `references/voice-ux-principles.md` — 14 voice UX principles (P1–P14) with citation IDs, voice-vs-text contrasts, migration heuristics, and **common mis-applications for optimize mode**. Source of `why:` lines in audit.
- `references/telephony-patterns.md` — operational decision tables: 8 chat→voice translation rules (T-translate-1..8), grounding policy by field type (T-grounding), repair tier ladder (T-repair-tier-1..3), latency budget (T-latency), spoken-function phrasebook scaffold (T-phrasebook), and two-voice opening (T-opening). Each table has mis-application notes for optimize mode.
- `references/audit-rubric.md` — coverage contract mapping each principle and pattern to a check. Includes both presence checks (used in both modes) and **mis-application checks (optimize mode)**. Documents mode-dependent conflict thresholds.
- `templates/vocal-identity-brief.md` — skeleton for the vocal identity file (brief, casting sides, audition, decision record, light-tuning log). Used in Phase 4b.
- `references/patterns/` — **per-file pattern catalog** (patterns across 10 categories: A system-instructions, B welcome-and-static, C display-formatting, D input-collection / spell-confirm, E output-presentation, F crisis-and-safety, G latency-masking, H configuration, I variables, J flow-control — plus Z-class pre-emptive lints). Each file has frontmatter (id, severity, applies\_to, couples\_with, detection rules), a chat example, a recommended voice example, alternatives, anti-patterns, and (where relevant) optimize-mode mis-applications. Phase 2 extraction loads only `references/patterns/README.md` (cheap index); Phase 4 audit loads only the bodies of patterns whose detection hit.
- `references/publish-errors/` — catalog of known `sf agent publish authoring-bundle` errors with canonical fixes. Optional Phase 8 (publish-with-self-healing) consumes this.
- `references/stakeholder-html-artifact.md` — patterns for the optional interactive HTML summary (Phase 9): before/after compare-cards, filter chips, journey tabs, conversation trees, dark config-delta table, and the bundle→HTML mapping. Inspiration, not a strict template.

## Phase 1 — Artifact Intake

Consult [`references/phases-1-3-intake-and-mode.md`](references/phases-1-3-intake-and-mode.md) before Phase 1. Covers: Phase 2 — Automated Extraction (mode detection); Phase 3 — Mode Confirmation + Gap-fill Diagnostic.

## Phase 4 — Audit + Rewrite

Consult [`references/phase-4-audit-rewrite.md`](references/phase-4-audit-rewrite.md) before Phase 4.

## Phase 4b — Vocal identity and casting

Consult [`references/phase-4b-vocal-identity-and-casting.md`](references/phase-4b-vocal-identity-and-casting.md) before Phase 4b.

## Phase 5 — Write Output

Consult [`references/phase-5-write-output.md`](references/phase-5-write-output.md) before Phase 5.

## Phase 6 — Hand-back

After writing, summarize for the developer:

- Mode used and why
- Persona source path/hash and handoff status when supplied, or `inferred from Script/sample`
- Casting: chosen voice and runner-up, audition channel, listener tier, and whether sign-off is still pending (path to the vocal identity file)
- Counts: changed / review needed / consider / out-of-scope / ok per category
- Top 3 review-needed and consider items with one-line context
- Layer E item count (work still owed to platform/runtime owner)
- Path to the migration/optimization bundle

Do not re-summarize the rewrite content — they can read it.

After hand-back, ask whether to proceed to optional Phase 7 (`.agent` generation) or stop. Stopping after Phase 6 is the default — the bundle is independently usable as a planning / handoff artifact.

## Phase 7 — Generate `.agent` file (optional, with mandatory self-heal)

Consult [`references/phase-7-generate-agent.md`](references/phase-7-generate-agent.md) before Phase 7 or 7.7. Covers: Phase 7.7 — Org-side dry-run validate (optional, recommended).

## Phase 8 — Publish with self-healing (optional)

Consult [`references/phase-8-publish.md`](references/phase-8-publish.md) before Phase 8.

## Phase 9 — Stakeholder HTML artifact (optional)

Consult [`references/phase-9-stakeholder-html.md`](references/phase-9-stakeholder-html.md) before Phase 9.

## What this skill does NOT do

Read [`references/scope-boundaries.md`](references/scope-boundaries.md) when a request may be out of scope, or to route neighbouring work.

## Verification (for skill maintenance)

Read [`references/maintenance-verification.md`](references/maintenance-verification.md) only when maintaining this skill.

## File layout

Read [`references/file-layout.md`](references/file-layout.md) when you need the location of a script, template, or reference.
