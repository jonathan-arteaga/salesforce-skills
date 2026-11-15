---
name: |-
  tableau-next-asset-create
description: |-
  Use Tableau Next tools to profile data, query models, or build analytics assets. Return findings or validated assets within the requested scope. Use crm-analytics-wave-generate for Wave.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# Tableau Next SDM Authoring — Router

Use the Tableau Next MCP tools for asset operations. If unavailable, return a scoped plan or analyze supplied data. Keep read-only queries separate from authorized writes and sharing.

Build semantic data models that actually return data, then enrich, query, and<br />visualize them. This skill encodes the failures that produce empty or<br />confidently-wrong dashboards in Tableau Next — building on **empty** source<br />objects, leaving objects **unjoined**, inventing field **apiNames**, summing an<br />ID, inflating a snapshot by its date count — and carries through to enriching,<br />querying, and visualizing the model.

This file is a **router**. It does two things: assert the one universal<br />precondition (G1), then dispatch your intent to the right task guide. The<br />guardrails that overlap between steps live in exactly one place —<br />**`references/shared-gates.md`** (gates G1–G8) — and each task guide opens with<br />the gates it must assert. Read the gate file once; every guide points back to it.

<b>The MCP tools are exposed under a </b>**`tableau-next-*`**<b> server</b>.<br />Every tool name in this skill — router and reference/task files alike — is written<br />**bare** (e.g. `add_semantic_model_relationship`) for readability; invoke each one<br />under whatever name your client exposes for that server's tool. Match the advertised<br />name — do not hand-construct it. (Single statement: `references/shared-gates.md`.)

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## G1 — Precondition (assert once, here, before dispatching)

Every step of this skill drives a Tableau Next MCP server; without one connected<br />there is nothing to call. Before dispatching to any guide, confirm the available<br />tools include one prefixed `mcp__tableau-next-*__` (e.g.<br />`mcp__tableau-next-pilot-production__browse_data_assets`,<br />`mcp__tableau-next-self-service__create_semantic_model`). Server names vary — match<br />the `tableau-next` stem, not an exact name.

**If NO such tool is present, STOP.** Do not attempt the workflow, do not describe<br />payloads as if you had run them, and never fabricate tool calls, results, or IDs.<br />Tell the user the skill requires a connected Tableau Next MCP server (e.g.<br />`tableau-next-pilot-*`, `tableau-next-self-service`) and ask them to connect one<br />and re-invoke. Every entry point inherits this — a standalone "add a metric" with<br />no server must still STOP. Full statement: `references/shared-gates.md` G1.

## Dispatch — route your intent to a task guide

Classify on **what the user wants to do**, then read that guide. Each guide's<br />header names the gates it asserts (from `references/shared-gates.md`).

Question phrasing does not exempt an intent from classification. "How do I<br />profile X" → `profile-dataset.md`. "What payload do I use for<br />`create_visualization`" / "which chart type for a stacked bar" →<br />`create-viz.md` (**not** `viz-authoring.md` — that file is cited by the<br />guide, it is not a first hop). "Before I build, how should I design the<br />layout" → `dashboard-design-principles.md` (load this skill; do not answer<br />from general dashboard knowledge). Only an explicit disclaimer of<br />*authoring* ("don't build/create anything") sends advice / review / ideation<br />to the No-dispatch rule. A disclaimer that still asks for a number, table,<br />or interpretation ("don't build or change any model — just get the count<br />from existing Tableau Next data") is a query/analyze intent: route to<br />`query-model.md` / `analyze-data.md`. The question mark is never the test.

| User intent | Route to |
| --- | --- |
| "analyze this CSV" / "build a dashboard from these files" / nothing modeled yet | `references/tasks/build-end-to-end.md` |
| "ingest this CSV / Excel into a DLO/DMO" or ingest from an existing Snowflake / Databricks / BigQuery / Redshift connection (ingest only, no downstream ask) | `references/tasks/ingest-flat-file.md` |
| "create / update a data transform" / derived DLO or DMO via Data Cloud SQL | `references/tasks/create-data-transform.md` |
| "profile / discover / check this data" (read-only) | `references/tasks/profile-dataset.md` |
| add a **raw** object / dimension / measure / join / **logical view** / **parameter** to my model | `references/tasks/edit-sdm.md` |
| add a **calculated** dimension / measure / **metric** to my model | `references/tasks/enrich-model.md` |
| "is my model AI-ready" / "backfill readiness metadata" / validate a model | `references/tasks/ai-readiness-audit.md` |
| count / total / scalar ("how many orders", "what is total revenue") or named-model structured `run_semantic_query` or raw DLO/DMO `run_query` | `references/tasks/query-model.md` |
| interpreted breakdown / ranking / trend / comparison without asking to author | `references/tasks/analyze-data.md` |
| delete a calc / metric / data object / logical view / relationship (component, not the whole SDM) | `references/sdm-tool-reference.md` |
| "create a viz / chart" OR which-chart-type / `create_visualization` payload (no existing chart; not "just advise") | `references/tasks/create-viz.md` (then that guide cites `viz-authoring.md` — do **not** skip to it) |
| "edit / add a filter / forecast / sort / field to **this** chart" (an existing viz) | `references/tasks/edit-viz.md` |
| "show / view / display my existing chart/visualization" (no edit) | Call `get_visualization` directly (`minorVersion: -1`) — renders inline; do NOT chain `render_visualization` |
| "show / view / display / open my existing dashboard" (no edit) | Call `render_dashboard` (`addVisualization=true`, `addSdm=true`, `showDraft=true`, `minorVersion=-1`) — details in `references/dashboard-authoring.md` §8. Do **not** use `get_dashboard` (metadata-only, does not render) |
| "create a dashboard" / design a dashboard layout / add a global filter (no existing dashboard to edit) | `references/tasks/build-dashboard.md` |
| "edit an existing dashboard" / add-move-remove a widget / add-rename-delete a page on a dashboard that already exists | `references/tasks/edit-dashboard.md` |
| "how should I design the narrative/layout before charting" (no existing dashboard to review) | `references/dashboard-design-principles.md` |
| share / revoke / list who has access (user or group on a dashboard, viz, workspace, or SDM) | `references/tasks/share-asset.md` |
| reuse a prod asset in a Personal Org **or** promote a Personal Org asset / open a promotion PR | `references/tasks/promote-or-reuse.md` |
| provision / list Tableau Next users / check licenses (org **role**, not asset ACL) | `references/tasks/provision-user.md` |
| "alert me when" / change that alert / list or delete my alerts (ongoing monitor) | `references/tasks/manage-alert.md` |
| list / classify verified questions **or** score agent SQL against expected SQL | `references/tasks/review-verified-questions.md` |

**Destructive / lifecycle operations** — component and whole-asset deletes,<br />workspace asset association, share/reuse/promotion mutations, `upsert_user`,<br />`delete_alert`, `delete_analytics_utterances`, `edit_dashboard` drafts, and<br />double-wrapped `defaultExc` responses: read<br />**`references/destructive-operations.md`** before calling any of them. Always<br />get explicit user confirmation before `delete_visualization` /<br />`delete_dashboard` / `delete_semantic_model` / `delete_workspace`, and never<br />call `save_dashboard` or `upsert_user` without the user's explicit go-ahead.

**Disambiguation:**

- **calculated vs. raw** — a calc dimension/measure/metric routes to<br />`enrich-model.md`; a plain object/dimension/measure/join/**logical view**<br />routes to `edit-sdm.md`.
- **analyze vs query vs greenfield** — figures (counts, totals, scalars;<br />"how many orders", "what is total revenue") → `query-model.md`<br />(`run_semantic_query`; discover the SDM with `list_semantic_models` if<br />unnamed), **including** when the user says not to build or change a model.<br />Interpreted breakdowns, rankings, trends, comparisons →<br />`analyze-data.md` (`analyze_data`; do not pin `targetEntityNameOrId` /<br />`targetEntityType` unless the user named an SDM). Named already-built model +<br />structured table / explicit `run_semantic_query` → `query-model.md`. Raw SQL<br />against a DLO/DMO (`run_query`) when no SDM covers the data, or the user<br />asked for SQL, also → `query-model.md` (that guide prefers<br />`run_semantic_query` when an SDM exists). Nothing modeled yet / CSV /<br />"build a dashboard" → `build-end-to-end.md`. Ingest from an existing<br />database connection (not a local file) still → `ingest-flat-file.md`.<br />Derived table / Data Cloud SQL transform → `create-data-transform.md`, not<br />ingest and not `enrich-model.md`. Metadata discovery (list SDMs, fields,<br />relationships) is `list_*` / `get_*`, not `analyze_data`.
- **create vs. edit a viz** — a request that names or clearly references an<br />**existing** chart ("add a forecast to my monthly sales chart", "filter this<br />chart to West") routes to `edit-viz.md`; a request with no existing chart in<br />play ("create a bar chart of sales by category", "which chart type and what<br />`create_visualization` payload for a stacked bar") routes to `create-viz.md`.<br />Do not skip to `viz-authoring.md`.
- **create vs. edit a dashboard** — a request that names or clearly references an<br />**existing** dashboard ("add a KPI widget to my sales dashboard", "move this<br />chart to the top", "add a details page to the pipeline dashboard") routes to<br />`edit-dashboard.md`; a request with no existing dashboard in play ("create a<br />dashboard for regional sales", "design a dashboard layout for these metrics")<br />routes to `build-dashboard.md`. Do not skip to `dashboard-authoring.md`.
- **show vs get vs edit a dashboard** — "show / open / view my Sales<br />dashboard" (including naming or id'ing one to see it), no edit → `render_dashboard`<br />(`dashboard-authoring.md` §8). Widget JSON / PATCH or `edit_dashboard` prep on<br />an **existing** dashboard → `get_dashboard` then `edit-dashboard.md`. "Review<br />this dashboard, don't modify it" stays No-dispatch.
- **Fast-path** — if a suitable **already-built, populated, joined** model is<br />available (named, or discovered via `list_semantic_models`) and the user wants<br />figures or a structured table, this skill's build steps are not the entry<br />point: route to `query-model.md` (`run_semantic_query`). An interpretive<br />question (breakdown, ranking, trend, comparison) → `analyze-data.md`.
- **Greenfield** — "analyze account engagement / build a dashboard" where no<br />model exists yet is a *build* intent (the trigger is "the user wants insight<br />from data that isn't modeled yet," not the literal phrase "semantic model") →<br />`build-end-to-end.md`.
- **share vs workspace membership** — granting a user/group `accessType` on an<br />asset routes to `share-asset.md`. Putting an asset in a workspace<br />(`add_workspace_asset`) is not a share.
- **revoke share vs delete the asset** — "unshare Alice" / "remove her access"<br />→ `share-asset.md`. Deleting the dashboard/model/workspace itself stays on<br />the destructive tools above.
- **reuse / promote vs create** — copying or packaging an **existing** asset<br />routes to `promote-or-reuse.md`. Building a new SDM from data still goes to<br />`build-end-to-end.md` / `edit-sdm.md`.
- **share vs provision a user** — "share this dashboard with Alice" /<br />viewer-vs-editor on an asset → `share-asset.md` (`search_users_and_groups`).<br />"Add Alice as Analyst" / list Tableau Next users / check seats →<br />`provision-user.md` (`get_users` / `upsert_user`). Granting a **role** is<br />not granting `accessType` on an asset.
- **analyze vs alert** — one-off "why did EMEA sales drop" /<br />breakdown/trend/comparison → `analyze-data.md`. "Alert me when bookings<br />drop 10% week over week" / change or list my alerts → `manage-alert.md`.<br />Do not pin an SDM on either path.
- **query vs score SQL** — "what is total revenue" → `query-model.md`.<br />"Does this agent SQL match the expected SQL" →<br />`review-verified-questions.md` (`run_regression_evaluator`; persists<br />nothing).
- **AI-ready vs verified questions** — backfill descriptions / `agentEnabled`<br />/ prefs → `ai-readiness-audit.md`. List/classify AVQ or score golden Q&A →<br />`review-verified-questions.md`.
- **insights (analyze vs metric-card payload)** — "generate insights on EMEA<br />sales" / interpretive "what should I focus on" → `analyze-data.md`. The<br />dashboard metric-card live value/trend/status payload is<br />`generate_insight_bundle` / `render_metric` for the MCP app renderer<br />(`insight-bundle.md`) via `app.callServerTool()`. The model does **not**<br />call those tools on a user chat turn and does **not** first-hop to<br />`insight-bundle.md`.

## No-dispatch rule (decline — do NOT route into an authoring guide)

The surface verbs above ("create a viz", "edit sdm", "create metric",<br />"create/update dashboard", "share", "promote", "reuse", "provision",<br />"alert", "classify") collide word-for-word<br />with work this skill is **not**<br />for. Classify on **build-vs-advise/review/ideate/edit-prose**, not the surface<br />verb. Decline (or hand off) these — do not dispatch:

- **Advice, no build** — "which chart type, stacked vs grouped? don't create<br />anything" → advise; do not route to `create-viz.md`.
- **Prose edit on an existing model** — decline any request whose *only* change<br />is the wording of an existing description/label, no matter the verb used<br />("rewrite", "update", "fix", "correct", "improve", "reword" all count — the verb<br />is not the test). The test is: **does this add/change a field, join, metric, or<br />grain? If not — pure copy-editing — decline.** E.g. "rewrite the description on<br />my existing model" or "fix the typo in this field's description" → decline. This<br />is the sharpest near-miss: `edit-sdm.md` / `ai-readiness-audit.md` literally wrap<br />`update_semantic_model_dimension/_measure` as sparse description updates, so it<br />is tempting — but a prose-only edit is not authoring the model. (Backfilling<br />*missing* readiness metadata as part of making a model AI-ready IS in scope<br />and must echo `isVisible` + `dataObjectFieldName` — see G5; rewording existing<br />prose for style, accuracy, or typos is not.)
- **Ideation, no data** — "brainstorm KPIs I could track later, no changes now" →<br />ideate; do not route to `enrich-model.md`.
- **Review** — "review my dashboard layout, don't modify it" / "someone on my<br />team built this, what's confusing" → review; do not route to<br />`build-dashboard.md`. Designing the narrative *before* you drop charts is<br />the opposite intent — that **does** dispatch (to<br />`dashboard-design-principles.md`).
- **Share advice, no grant** — "who should I share this with / viewer vs<br />editor? don't actually share" → advise; do not route to `share-asset.md`.
- **Provision advice, no mutate** — "who should I add as Analyst? don't<br />provision anyone" → advise; do not route to `provision-user.md`.
- **Alert advice, no monitor** — "should I alert on this KPI? don't create<br />one" → advise; do not route to `manage-alert.md`.

A "don't build / don't change anything" disclaimer does **not** by itself<br />mean No-dispatch. Count / total / scalar ("how many orders") and named-model<br />structured query still route to `query-model.md`; interpreted breakdown /<br />ranking / trend / comparison still route to `analyze-data.md`. Those are<br />in-scope redirects, not declines.

Also out of scope: debugging a broken MCP server (→ Columbo / standard<br />debugging); writing application code / managing AI Suite infra.

## Deep references (cited by task guides)

Read [`references/deep-references-index.md`](references/deep-references-index.md) when a task guide cites a deep reference and you need its path.
