# Consumed JSON Contracts

This skill **does not own** the findings JSON, `test-results.json`, or the persona rubric — they are produced by the delegated `/agentforce-config-review` skill, the project testing skill, and `persona`. To avoid silently breaking when a delegated skill changes its output (or a different skill is swapped in), the orchestrator depends on only the minimal fields below and **validates their presence** the moment a sub-agent returns. Treat extra fields as opaque; treat a missing required field as a hard stop — *except* the persona rubric, which degrades gracefully (see below).

These contracts are validated at the validation step of REVIEW, PLAN (skip path), TEST, RE-REVIEW, and the persona SCORE return.

## Findings JSON (from `/agentforce-config-review`)

The review skill emits **snake_case** keys, and findings are **nested inside `sections[]`** — there is no top-level `findings[]`. Required fields the orchestrator reads:

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `composite_score` | number (0–10) | REVIEW, RE-REVIEW | The headline score and delta |
| `sections[]` | array | PLAN, RE-REVIEW | One object per scorecard dimension |
| `sections[].number` | integer (1–7) | Finding IDs | The `D<n>` dimension in the Finding ID |
| `sections[].title` | string | reports | Dimension name |
| `sections[].findings[]` | array | PLAN, RE-REVIEW | The findings for that dimension (may be empty) |
| `sections[].findings[].severity` | `"HIGH"`\|`"MEDIUM"`\|`"LOW"` | PLAN (filter), Finding IDs | Drives what gets fixed |
| `sections[].findings[].label` | string | reports, reconciliation | Short human-readable name (the finding "title") |
| `sections[].findings[].text` | string | reports | Body text (the finding "detail") |

Field mapping to this skill's internal model: `composite_score → compositeScore`, `sections[].number → D<n>` (the dimension in the Finding ID), `findings[].label → title`, `findings[].text → detail`. To enumerate every finding, **flatten `sections[].findings[]` across all sections** (carrying each section's `number` as the dimension).

Optional/tolerated (read if present, never required): `remediation[]` (`{number, area, finding, severity}` — a pre-prioritized roadmap; useful as a cross-check on PLAN ranking), `scores[]` (`{dimension, score, rationale}` — the scorecard), `exec_summary`, `kpis`, and any others — passed through to reports unmodified.

**Validation on read:** assert `composite_score` is a number and `sections` is a non-empty array whose entries have a `number` and a `findings` array (findings entries each have `severity`). The canonical required set is: `composite_score`, `sections`, `sections[].number`, `sections[].findings`, `sections[].findings[].severity`. If any is missing → stop with: *"Config review output is missing required fields (`<name the missing ones from: composite_score, sections, sections[].number, sections[].findings, sections[].findings[].severity>`). The review skill may have changed its format; cannot plan against it."*

## `test-results.json` (from the project testing skill)

Required fields:

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `passRate` | number (0–1) | EVALUATE | Compared against baseline |
| `passed` | integer | EVALUATE, reports | Numerator |
| `total` | integer | EVALUATE, reports | Denominator |
| `lastUpdated` | ISO timestamp | pre-flight Check 5 | Baseline freshness |

Optional/tolerated: `personas[]`, per-question detail, etc.

**Validation on read:** assert `passRate` is a number in `[0,1]` and `passed`/`total` are integers with `passed <= total`. If not → stop with: *"Test results are missing or inconsistent (`<detail>`). Cannot evaluate against baseline."*

## Persona rubric (from `persona` SCORE)

**This is a delegation-return contract, not a file contract.** The persona skill writes its
evaluation to `persona/<agent>/evaluation.md` as prose plus a percentage — there is no JSON to parse.
So, exactly as REVIEW reads `composite_score` and TEST reads `passRate` from a sub-agent's result,
the orchestrator captures the rubric from the **returned result** of the SCORE delegation. Required
return values:

| Value | Type | Used by | Notes |
|-------|------|---------|-------|
| total score | integer (0–100) | Persona Rubric (resolution + reporting) | The headline persona number |
| band | string | reports | One of: production-ready / strong foundation / needs revision / significant gaps |
| evaluation path | string | `outputs[]`, evidence | Relative path to `evaluation.md` |

**Validation on read:** assert the total is an integer in `[0,100]`. If it's missing or out of range,
**do not stop the loop** — record that the rubric was unavailable, treat the persona finding as
*unresolved* (per **Persona Rubric**), and continue. The rubric is supplementary; a missing score
must never block reconciliation of the non-persona findings or the run summary.

> **Schema drift note:** these are the only fields the orchestrator depends on. If a delegated skill renames or removes one, fix the mapping here in one place rather than scattering field names through the phases.
