# Deep references (cited by task guides)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Deep references (cited by task guides)

The task guides point *down* to these for verified payloads and tool shapes.
A narrow lookup — "how do I / what is / what's the exact ___" — is a
**direct-dispatch** only when the list below names that file. Viz,
dashboard-widget, ingest, and greenfield-build lookups are **not**
direct-dispatch: first-hop to the matching `references/tasks/*.md` guide
(the guide then cites the deep ref). In particular, chart-type /
`create_visualization` payload questions first-hop to `tasks/create-viz.md`;
**`viz-authoring.md` is not a first hop.**

Direct-dispatch lookups:

- "how do I handle a huge/wide CSV with cryptic columns" → `large-flat-file-handling.md`
- "how do I figure out grain / measures vs. dimensions [before modeling]" → `data-understanding.md`
- "what's the input shape / suffix rule for `add_semantic_model_*`" → `sdm-tool-reference.md`
- "how do I bind SDM fields in one `create_semantic_model` call" → `sdm-tool-reference.md`
- "how do I add or update a semantic-model parameter" → `tasks/edit-sdm.md`
  (shapes in `sdm-tool-reference.md` Parameters)
- "how do I add a HardJoin / Union / CustomSQL logical view" → `tasks/edit-sdm.md`
  (shapes in `sdm-tool-reference.md`)
- "how do I safely delete a calc / metric / data object / logical view / relationship" →
  `sdm-tool-reference.md`
- "what depends on this viz / dashboard" / before deleting a viz or dashboard →
  `dashboard-authoring.md`
- "how do I show / open / view a dashboard" (inline render, not metadata) →
  `dashboard-authoring.md` (§8 `render_dashboard`)
- "why did my query return zero rows" / "empty vs. does-not-exist" → `empty-source-handling.md`
- "how do I write a `run_semantic_query` body" → `semantic-query-and-enrichment.md`
- "how do I make my model AI-ready" (checklist; not "backfill it now") → `ai-readiness.md`
- "how should I design the narrative/layout before charting" → `dashboard-design-principles.md`

Not a first hop (cited only from the matching task guide):

- "which chart type / what `create_visualization` payload" → `tasks/create-viz.md`
  (NOT `viz-authoring.md`)
- "how do I add/move/remove a widget on an **existing** dashboard" →
  `tasks/edit-dashboard.md` (NOT `edit-dashboard.md` the deep ref, and NOT
  `dashboard-authoring.md`)
- "how do I create a dashboard / lay out a **new** dashboard" →
  `tasks/build-dashboard.md` (NOT `dashboard-authoring.md`)
- "how do I ingest a CSV / Excel / existing connection into a DLO/DMO" → `tasks/ingest-flat-file.md`
  (NOT `ingest-and-metric-gotchas.md`)
- "how do I create or update a data transform" → `tasks/create-data-transform.md`
  (NOT `data-transform-gotchas.md`)
- "walk me through building a model end to end" → `tasks/build-end-to-end.md`
  (NOT `build-workflow.md`)
- "how do I share / unshare / list who has access" → `tasks/share-asset.md`
  (NOT `sharing-and-promotion.md`)
- "how do I reuse a prod asset or promote a Personal Org asset" →
  `tasks/promote-or-reuse.md` (NOT `sharing-and-promotion.md`)
- "how do I provision / list Tableau Next users / check licenses" →
  `tasks/provision-user.md` (NOT `admin-users.md`)
- "how do I create / update / list / delete a data alert" → `tasks/manage-alert.md`
  (NOT `alerts.md`)
- "how do I list verified questions / score agent SQL" →
  `tasks/review-verified-questions.md` (NOT `verified-questions.md`)

What each deep reference covers (and which guide cites it) is in
**`references/deep-reference-index.md`**.
