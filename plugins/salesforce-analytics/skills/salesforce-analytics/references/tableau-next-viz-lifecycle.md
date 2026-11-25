# Tableau Next Visualizations, Dashboards & Asset Lifecycle

Distilled authoring, editing, sharing, promotion, and destructive-operation rules for Tableau Next MCP workflows.

## Narrative-First & Chart Authoring (G8)

- **Dashboards**: Design the full narrative before creating widgets — KPIs (top/left F/Z path) -> trends -> breakdowns -> correlations — with business-friendly labels and chart-type diversity.
- **Single standalone viz**: State the analytical intent (question answered + why the chart type fits field roles) without inventing an unrequested dashboard.
- **Single-tool surface**: All chart types use `create_visualization` (specialized `create_*_viz` tools do not exist). Never build a chart before G7 confirms non-empty rows.

| Analytical Pattern | `marks.panes.type` | `layout` | Key Encoding Notes |
| --- | --- | --- | --- |
| Trend / Multi-series | `Line` | `Vizql` | Date (`DateTruncMonth`) on columns, measure on rows (+ Color dim; optional `forecasts`) |
| Ranking / Comparative | `Bar` | `Vizql` | Dim on columns, measure on rows, `sortIntent: "MeasureDescending"` |
| Two-dim Breakdown | `Bar` | `Vizql` | `stack: {isAutomatic: false, isStacked: true}` + Color on second dim |
| Composition (< 5 vals) | `Donut` | `Radial` | Measure on `Angle` encoding (NEVER `rows`/`columns`); dim on `Color` |
| Correlation / Hotspot | `Circle` / `Square` | `Vizql` | Scatter: X/Y measures + Color dim; Heatmap: two dims + measure on Color |
| Detailed Table | `Text` | `Table` | Dims in `groups`, measures in `rows` |

## Viewing & Editing Dashboards Safely

- **View existing assets**: Show a chart with `get_visualization` (`minorVersion: -1`, do not chain `render_visualization`). Show a dashboard with `render_dashboard` (`addVisualization=true`, `addSdm=true`, `showDraft=true`, `minorVersion=-1`) — `get_dashboard` is metadata-only and does not render.
- **Atomic draft edits**: `edit_dashboard` batches `upsert_*_widget` + `place_widget_on_page` into an **unsaved draft** by default (`autosave` unset/false). NEVER call `save_dashboard` automatically — wait for explicit user confirmation AFTER they inspect the draft, even if the initial prompt said "save it". Avoid `&` in stored text labels (encodes to `&amp;`).
- **Response wrapper quirk**: Several lifecycle tools (`edit_dashboard`, deletes) double-wrap responses as `{"defaultExc": "<stringified JSON>", "responseCode": N}`. Branch on `responseCode === 204` before calling `JSON.parse(defaultExc)` because 204 returns an empty string.

## Asset Sharing Permission Matrix

Resolve recipients via `search_users_and_groups` (`usersAndGroupsQueryInput`, min 2 chars; paginate `nextUserOffset` and `nextGroupOffset` independently). Pass top-level args (no `body` wrapper) with `applicationDomain: "Tableau"`:

| `setupObjectType` | Production Allowed `accessType` | Personal Org Notes |
| --- | --- | --- |
| `analyticsvisualization` | `viewer` only | Direct writes return `ACCESS_DENIED` (share via workspace) |
| `analyticsdashboard` | `viewer` only | Direct writes return `ACCESS_DENIED` (share via workspace) |
| `analyticsworkspace` | `viewer`, `editor`, `owner` | `viewer`, `editor` only (no `owner`); groups cannot be `owner` |
| `semanticmodel` | `viewer`, `editor`, `owner` | Direct writes return `ACCESS_DENIED`; groups cannot be `owner` |

- `commenter` and `manager` are never valid `accessType` values.
- For `update_asset_share` or `remove_asset_share`, call `list_asset_shares` first (`limit` defaults to 10; `"ASC"` is case-sensitive) and pass the listed shadow `userOrGroupId` (`update_asset_share` does not remap add-time IDs).

## Destructive Gates, Workspaces & Promotion

- **Mandatory confirmation**: Confirm explicitly before `delete_visualization`, `delete_dashboard`, `delete_semantic_model`, `delete_workspace`, `delete_alert` (preview `alertSummary`, `userConfirmed=true`), `delete_analytics_utterances`, `upsert_user` (admin-only role provisioning; never fall back to share tools), or share/promotion writes. Preflight viz/dashboard deletes with `list_asset_dependencies`.
- **Clean widget removal**: Deleting a viz placed on a dashboard leaves a broken widget; remove both definition and placements in one `edit_dashboard` op via `remove_widget_from_dashboard` (not `remove_widget_from_page`).
- **Workspace association**: `add_workspace_asset` / `remove_workspace_asset` take flat top-level args; `delete_workspace` cascade-deletes only `assetUsageType: "Created"` assets (not `"Referenced"`).
- **Reuse & Promotion**: Reuse copies prod -> Personal Org; Promotion exports Personal Org package -> wait for `packageExportStatus: Ready` -> open PR via `create_promotion_pull_request`.
