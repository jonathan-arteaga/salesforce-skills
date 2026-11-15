# Phase 7 — Generate `.agent` file (optional, with mandatory self-heal)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Phase 7 — Generate `.agent` file (optional, with mandatory self-heal)
  - Phase 7.0 — Validator setup gate
  - Phase 7.1 — Generation strategy
  - Phase 7.2 — Z-class pre-emptive lints
  - Phase 7.3 — Pattern application
  - Phase 7.4 — Iteration tracking
  - Phase 7.5 — Final lint pass + side artifact generation
  - Phase 7.6 — What guarantee Phase 7 provides
  - Output
- Phase 7.7 — Org-side dry-run validate (optional, recommended)
  - When to run it
  - What it catches that Phase 7 doesn't
  - Workflow
  - Why it's optional
  - Cost

## Phase 7 — Generate `.agent` file (optional, with mandatory self-heal)

If the developer wants a deployable `.agent` rather than just the planning bundle.

**Hard rule: the developer never sees a draft with offline-detectable publish-blocking errors OR offline-detectable Z-class warnings that haven't been cleared.** Phase 7 keeps iterating until the file is clean of errors AND of all Z-class warnings — Z01, Z02 and Z04 auto-fix, Z05 auto-fixes and flags each hit `[review needed]`, Z06 and Z07 auto-fix, Z08 auto-fixes and blocks until the replacement line is in, Z03 blocks hand-back until the developer resolves it manually. Other deprecation or advisory warnings the skill hasn't categorised are surfaced in hand-back but don't block. The rule applies to source-carried warnings too — the output is cleaner than the input. The 1800-error first draft and the 8-warning hand-off from real-world testing are both failure modes this prevents.

### Phase 7.0 — Validator setup gate

Before any generation:

1. **Verify the offline validator is set up.** Check that `~/dev/agentscript/packages/agentforce/dist/index.js` exists (or the user's chosen path). If not, run the user through `references/offline-validator-setup.md` and pause until they confirm setup.
2. **Verify the validator script exists** in the working project (e.g., `validate-agent.mjs`).
3. **Version-staying-current check (informational):** compare local clone tag against upstream. If older than 30 days OR a new tag is available, voice a soft prompt to update. Don't block.

If the validator is missing, do NOT proceed by skipping validation. Without validation Phase 7's quality guarantee is void. Either set up the validator or stop at Phase 6 (planning bundle still useful).

### Phase 7.1 — Generation strategy

Strategy: **start from a clean copy of the source `.agent`, apply changes as small `Edit` batches, validate after every batch, never let errors accumulate.**

NOT this: write the file from scratch in one big `Write`. The from-scratch path produced a 1800-error blowup on its first run. The surgical-edits-from-clean-copy path produced 0 errors in 14 iterations on the same task.

Steps:
1. **Copy** source `.agent` → `artifacts/voice-ux/<api_name>.agent`. Original untouched. (Caller can diff later.)
2. **Validate baseline.** Run `node validate-agent.mjs artifacts/voice-ux/<api_name>.agent`. Expect 0 errors. Source-carried warnings (deprecation, duplicate keys) are recorded in the iteration table but are NOT considered "tolerated" — Phase 7.2 will clear or surface every Z-class warning before hand-back. If baseline shows errors, the source itself was broken — escalate to user before continuing.
3. **Apply Z-class pre-emptive lints first** (see Phase 7.2).
4. **Apply patterns in Application order** as small batches (see Phase 7.3).
5. **Validate after every batch.** If errors appear, do NOT proceed — diagnose and fix that batch first.
6. **Cap at 20 iterations.** Beyond that, stop and surface remaining issues with a clear "I couldn't get this fully clean" hand-back.

### Phase 7.2 — Z-class pre-emptive lints

These run BEFORE pattern application. Z01 and Z02 catch error classes the offline validator either doesn't enforce (Z01) or only flags as warnings (Z02) — but both produce broken or stale output if ignored. Z03 catches a warning the offline validator does emit but cannot safely auto-fix. Z04 catches spoken em-dashes, which no validator flags but TTS renders unpredictably. Z05 catches instructions that make the agent pass as human, which no validator flags either. Z06–Z08 catch script that compiles and then misbehaves on a call: work after a `transition` that never runs (the validator only warns `unreachable-code`), empty checks that miss `None` or `""`, and generative stages told to output nothing.

| ID | Check | Auto-fix | Block hand-back? |
|---|---|---|---|
| Z01 | Any `description: "..."` field >255 chars | Auto-truncate to ≤240 chars at sentence boundary, suffix `…` if needed | Yes — auto-fixed before hand-back |
| Z02 | Any `^topic\s+\w+:` block declaration (deprecated keyword), plus all `@topic.<Name>` reference-path occurrences | Auto-rewrite both: `topic <name>:` → `subagent <name>:` and `@topic.<Name>` → `@subagent.<Name>` | Yes — auto-fixed before hand-back |
| Z03 | Validator warning matching `Duplicate key '<key>'` | None — surfaces location + both values for developer choice | Yes — fail loop until developer resolves |
| Z04 | Any `—` in a `\|` instruction line or spoken string (welcome, error, progress message, speak-up message, filler sentence) | Rewrite by meaning: full stop, commas, or ellipsis; add a no-dashes line to global instructions | No — auto-fixed before hand-back |
| Z05 | Human impersonation: "you are a human", "so they believe it's a real person", disclosure dodges, human-likeness targets, body-sound tags (`[laughs]`, `[exhales]`), scripted fillers (`uhm`) | Rewrite per A09 ("sound natural, not human") / A10 / B02; log each hit `[review needed]` with the rationale | No — auto-fixed and flagged; a client who insists on keeping a hit decides in writing |
| Z06 | A `set`, `run`, `if` or `\|` line after a `transition to` in the same block, or any `unreachable-code` validator warning | Move the work above the transition | Yes — auto-fixed and re-validated before hand-back |
| Z07 | An emptiness check on a string that tests only `== ""` or only `is None` | Test both: `is None or == ""` (or `is not None and != ""`) | No — auto-fixed before hand-back |
| Z08 | An instruction telling a generative stage to output nothing or stay silent | Replace with a short holding line, plus speak-up timers (H06) for the wait; move logic-only work out of the reasoning pass | Yes — until the replacement is in; flag `[review needed]` if the silent turn was load-bearing |

**Z01 specifically:** the org-side metadata API rejects descriptions over 255 chars on any of these locations: `config.description`, variable descriptions, action descriptions, transition descriptions. The error message is misleading — it picks ONE specific over-length field, hiding however many others were also over. Auto-truncate ALL over-length descriptions before generation, not just one at a time.

**Z02 and Z03 detail:** see the per-pattern docs (`references/patterns/Z02-subagent-deprecation.md`, `references/patterns/Z03-duplicate-keys.md`). Z02 rewrites both `^topic\s+\w+:` block declarations AND `@topic.<Name>` references in a single coordinated batch — both must flip together. Z03 surfaces duplicate-key warnings with line/value context for the developer to resolve; no auto-fix because picking the wrong dup silently breaks runtime.

### Phase 7.3 — Pattern application

Apply patterns in the canonical Application order from `references/patterns/README.md` (H → I → A → per-topic A → D/E/F/G → action progress messages → final C strip).

**H01 in particular** is mandatory and front-loaded — it's the NGA-runtime gate. If source has `additional_parameter__disable_graph_runtime: True`, strip it as the FIRST edit. See `references/publish-errors/E004` and the H01 pattern doc.

**Write the in-script voice-channel config (H06, H05).** The latency/turn-timing block and the STT bias list are authored in the `.agent`, not deferred to a human. When H06 applies, write `modality voice: → additional_configs:` with the recommended defaults: `beepboop_config.max_wait_time_ms: 500` and `speak_up_config` (10000ms timers + a phrasebook pursuit line). When H05 applies, write `inbound_keywords: → keywords:` from the predicted term list, and set `inbound_filler_words_detection` deliberately (often `True` for telephony; see H05). When H03/H04 apply, emit the flat `voice_id` from the casting record (H09) + the light-tuned delivery settings and any `pronunciation_dict` (including the agent name and brand from the H08 name block), but flag that on the default v3 model only `outbound_stability` applies; speed/similarity/custom-pronunciation are Flash-only. Surface **each written value as `[review needed]`** so a developer can tune it against a real call. Map Persona Tone Flex to P5/A08 situational prosody without changing its triggers, semantic shift, maximum, hard boundary, or reset. Keep every value inside compiler ranges (see H06 / `T-config`); an out-of-range value fails validation in 7.5. Active Agent Script tooling validates syntax, the target org supplies valid voice IDs, and a human listening sign-off (H09) approves the audible result.

Within each pattern category, batch by location not by pattern (so a single `Edit` doesn't span dozens of unrelated places). Validate after each batch.

**Use `Edit` for surgical changes.** Use `Write` only when overwriting an entire section is cleaner AND you can predict the new section is parser-safe (no embedded multi-line quoted strings with em-dashes — that bit us).

### Phase 7.4 — Iteration tracking

Maintain an internal table to surface to the developer at hand-back time:

```
Iteration | Errors | Warnings | Info | Notes
--------- | ------ | -------- | ---- | -----
0 (clean) | 0      | 8        | 0    | baseline (7× Z02 topic deprecation, 1× Z03 dup-key)
1         | 0      | 1        | 0    | Z02 rewrite: topic→subagent (block decls + @-refs)
2         | 0      | 0        | 0    | Z03 resolved by developer (kept later occurrence)
3         | 0      | 0        | 0    | H01 + welcome + connection blocks
4         | 0      | 0        | 3    | I01 _spoken vars (unused-info expected)
…
N         | 0      | 0        | 1    | final
```

Targets: errors must reach 0; Z-class warnings must reach 0 (auto-fixed by Z01/Z02/Z06 or developer-resolved for Z03); other warnings are surfaced in hand-back.

The table is honest about what happened. If iteration N had errors that took 3 retries to fix, show that.

### Phase 7.5 — Final lint pass + side artifact generation

Once the loop is clean:

1. Run a final lint: Z01 retroactively in case any added content went over, and Z06–Z08 over every block the skill wrote (J01 guards, I01/I02 checks, after-speech `run` lines, D08 waits).
2. Generate side artifacts:
   - `pronunciation-dictionary.md` per `templates/pronunciation-dictionary.md` if H04 detected
   - `key-term-prompting.md` per `templates/key-term-prompting.md` if H05 detected
   - `v1-review-checklist.md` per `templates/v1-review-checklist.md` (always)
   - `vocal-identity.md` per `templates/vocal-identity-brief.md` (always; written in Phase 4b, updated here if light tuning changed)
3. **Generate `.bundle-meta.xml`** alongside the `.agent` file in `force-app/main/default/aiAuthoringBundles/<api_name>/`. Required content (see E006 for case-sensitivity):

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <AiAuthoringBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <bundleType>AGENT</bundleType>
   </AiAuthoringBundle>
   ```

4. **Sample dialog (optional sub-step):** generate 5–7 turns of voice dialog using the new agent's instructions, replaying a representative scenario from the provided sample. Use as a quick sanity check before publish. Iterate on developer feedback.

### Phase 7.6 — What guarantee Phase 7 provides

**Strong guarantee:** the file passes the offline `@agentscript/agentforce` validator with 0 errors AND 0 Z-class warnings (Z01 description length, Z02 `topic`→`subagent`, Z03 duplicate keys, Z06 unreachable code all cleared or explicitly resolved by the developer) before being shown to the developer. Non-Z-class warnings, if any, are listed in the hand-back so the developer is aware.

**NOT guaranteed:** that the file passes server-side `sf agent validate authoring-bundle` against an arbitrary org. Server-side validation catches schema drift (target Apex / Flow / Prompt Template signatures), missing dependencies, and other org-specific concerns the offline validator can't see. That's Phase 7.7 (org-side dry-run, recommended) and Phase 8 (publish with self-heal).

Be honest with the developer at hand-back: "Offline-clean. Server-side and org-specific concerns will be caught in Phase 7.7 / 8 if you continue."

### Output

```
artifacts/voice-ux/<api_name>.agent
artifacts/voice-ux/<api_name>-pronunciation-dictionary.md   (if H04)
artifacts/voice-ux/<api_name>-key-term-prompting.md         (if H05)
artifacts/voice-ux/<api_name>-v1-review-checklist.md
artifacts/voice-ux/<api_name>-vocal-identity.md
force-app/main/default/aiAuthoringBundles/<api_name>/<api_name>.agent
force-app/main/default/aiAuthoringBundles/<api_name>/<api_name>.bundle-meta.xml
```

The bundle copy is what Phase 8 consumes. The `artifacts/voice-ux/` copy is the canonical source for diffing and review.

**Critical: per-topic action declarations are NOT duplicates.** Each topic's `actions:` block is scoped — actions referenced in that topic's `reasoning.instructions` MUST be declared in that topic's `actions:` block. If two topics both call `Validate_Postal_Code`, declare it in BOTH. Removing a "duplicate" breaks publish. (See `references/patterns/README.md`.)

## Phase 7.7 — Org-side dry-run validate (optional, recommended)

Optional intermediate phase between Phase 7 (offline-clean) and Phase 8 (publish). Runs the **server-side** validator without creating any agent record in the org:

```bash
sf agent validate authoring-bundle --api-name <api_name> --target-org <org>
```

This is read-only on the org side. No `BotDefinition` record is created. No metadata is deployed. The command compiles the `.agent` against the target org's schemas (flows, prompt templates, Apex action targets, locale picklists, restricted-picklist constraints) and returns either success or a list of compile errors with locations.

### When to run it

After Phase 7 (offline-clean), before Phase 8 (publish). Cheap insurance.

### What it catches that Phase 7 doesn't

- **Schema drift** between the `.agent` and target org's flows / prompt templates / Apex (E007 catalog entry)
- **Missing target dependencies** — referenced Apex / Flow / Prompt Template doesn't exist in the target org (E002)
- **Locale picklist constraints** (E001)
- **Description length and other org-side validation** that the offline parser doesn't enforce

### Workflow

1. Confirm target org via `AskUserQuestion` (show `sf org display --target-org <alias>`).
2. Run `sf agent validate authoring-bundle --api-name <name> --target-org <org> --json`.
3. On success: surface "Server-side compile passed. Ready for Phase 8 publish."
4. On failure: surface error list, match against `references/publish-errors/` (same catalog used in Phase 8 self-heal). For each match, surface the canonical fix and the developer's options. Loop: developer chooses fix → apply → re-run dry-run → repeat. Cap at 5 iterations of dry-run before recommending stopping and re-examining the source.

### Why it's optional

Some teams skip this and go straight to Phase 8 publish — the publish step does the same validation and reports the same errors. The difference is that publish creates partial state in the org (a BotDefinition record and one or more BotVersions) even when the deploy back fails, leaving cleanup work. Phase 7.7 fails clean: no org state created.

### Cost

~5–30 seconds depending on org size and network. Negligible compared to the alternative (debugging from a half-published agent).
