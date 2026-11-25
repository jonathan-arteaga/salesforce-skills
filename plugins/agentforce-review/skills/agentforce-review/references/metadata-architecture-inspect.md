# Deployed Metadata Architecture Inspection

Extract a deterministic design-time architecture snapshot (`<agent>_<ver>_metadata_tree.json` and `<agent>_<ver>_architecture.md` with Mermaid graphs) from declared Salesforce metadata (`BotDefinition`, `GenAiPlanner*`, `GenAiPlugin*`, `GenAiFunction*`, `Flow`, `ApexClass`, `GenAiPromptTemplate`). Reads declared metadata only; route runtime traces to `agentforce-observe`.

## Agent Discovery (When Unspecified)

Never invent an agent API name. Query `BotDefinition` read-only first:

```bash
sf data query --query "SELECT DeveloperName, MasterLabel FROM BotDefinition ORDER BY DeveloperName" [--target-org <alias>] --json
```

Zero rows -> report no agents and stop. Single match -> state which agent was selected and preset `ARG_AGENT=<DeveloperName>`. Multiple matches -> list `DeveloperName` and `MasterLabel` and ask the user to choose.

## Pipeline Architecture & Invariants

- **SOQL-first fan-out (30-45s typical, <=60s target):** Resolves `BotDefinition`/`BotVersion`, retrieves `GenAiPlannerBundle`, fans out 6 parallel Tooling SOQL channels, batches Data API SOQL for Flow/Apex bodies, and uses Metadata API retrieve only for `GenAiPromptTemplate` and NGA external plugins.
- **Classic ReAct & NGA normalization:** Normalizes both classic (`ReactAiPlannerV1`) and NGA (`ConcurrentMultiAgentOrchestration`) planners into one deterministic tree; ID-prefix routing resolves 15/18-char targets and records unknown prefixes in `_unresolved[]` (`STATUS=PARTIAL_OK` on partial failures).
- **Caching & cycles:** Tree cache hashes bundled `assets/` (`soql/`, `cli/`, `mermaid/`); bypass with `--force`. Channel probe cache has 7-day TTL (`--reprobe` refreshes after releases). Per-branch cycle detection (`MAX_BFS_DEPTH=20`) prevents infinite recursion while preserving shared utility flows.
- **Prerequisites:** Authenticated `sf` CLI supporting `sf org auth show-access-token` and Python 3.10+.

## Pipeline invocation

Run inline once `ARG_AGENT` (or `--agent` in `AGENT_ARCH_FLAGS`) is known. Keep raw user prose out of shell commands.

```bash
set -euo pipefail
[ -n "${ZSH_VERSION:-}" ] && setopt KSH_ARRAYS

_skill=agentforce-review
for _c in "${SKILL_ROOT:-}" "<SKILL_DIR>" \
          "${VIBES_SKILLS_DIR:+$VIBES_SKILLS_DIR/$_skill}" \
          "$PWD/.agents/skills/$_skill" "$HOME/.agents/skills/$_skill" \
          "${PLUGIN_ROOT:-$HOME/.vibe/skills}/$_skill"; do
  [ -n "$_c" ] || continue
  for _r in "$_c" "$_c/artifacts"; do
    [ -f "$_r/scripts/main.py" ] && { SKILL_ROOT="$_r"; break 2; }
  done
done
[ -f "${SKILL_ROOT:-}/scripts/main.py" ] || { echo "$_skill: scripts not found — set SKILL_ROOT to this skill's directory" >&2; exit 1; }

ARG_ORG="${ARG_ORG:-}"
ARG_AGENT="${ARG_AGENT:-}"
ARG_VERSION="${ARG_VERSION:-}"
ARG_FORCE="${ARG_FORCE:-}"
ARG_REPROBE="${ARG_REPROBE:-}"
ARG_PARALLELISM="${ARG_PARALLELISM:-}"
ARG_MAX_MERMAID="${ARG_MAX_MERMAID:-}"

[ -n "${ZSH_VERSION:-}" ] && setopt SH_WORD_SPLIT
set -f
# shellcheck disable=SC2206
_args=(${AGENT_ARCH_FLAGS:-})
set +f
i=0
while [ $i -lt ${#_args[@]} ]; do
  tok="${_args[$i]}"
  case "$tok" in
    --org=*) ARG_ORG="${tok#--org=}" ;;
    --org) i=$((i+1)); ARG_ORG="${_args[$i]:-}" ;;
    --agent=*) ARG_AGENT="${tok#--agent=}" ;;
    --agent) i=$((i+1)); ARG_AGENT="${_args[$i]:-}" ;;
    --version=*) ARG_VERSION="${tok#--version=}" ;;
    --version) i=$((i+1)); ARG_VERSION="${_args[$i]:-}" ;;
    --parallelism=*) ARG_PARALLELISM="${tok#--parallelism=}" ;;
    --parallelism) i=$((i+1)); ARG_PARALLELISM="${_args[$i]:-}" ;;
    --max-mermaid-nodes=*) ARG_MAX_MERMAID="${tok#--max-mermaid-nodes=}" ;;
    --max-mermaid-nodes) i=$((i+1)); ARG_MAX_MERMAID="${_args[$i]:-}" ;;
    --force) ARG_FORCE="1" ;;
    --reprobe) ARG_REPROBE="1" ;;
  esac
  i=$((i+1))
done

if [ -z "$ARG_ORG" ] && command -v sf >/dev/null 2>&1; then
  _cfg="$(sf config get target-org --json 2>/dev/null || true)"
  _cfg="$(printf '%s\n' "$_cfg" | sed -n 's/.*"value"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' || true)"
  ARG_ORG="${_cfg%%$'\n'*}"
fi

if [ -z "$ARG_ORG" ] || [ -z "$ARG_AGENT" ]; then
  cat >&2 <<'USAGE'
Which agent should I document, and in which org?
Required: --agent <BotDefinition.DeveloperName> and --org <alias> (or default target-org).
Optional: --version <vN> --force --reprobe --parallelism <N> --max-mermaid-nodes <N>
USAGE
  exit 2
fi

WORK_DIR="/tmp/agentforce-review-$(date +%s)-$RANDOM"
mkdir -p "$WORK_DIR"
python3 "$SKILL_ROOT/scripts/_shared/fs_guard.py" "$ARG_AGENT" agent_api_name api_name || exit 1
python3 "$SKILL_ROOT/scripts/_shared/fs_guard.py" "$ARG_ORG" org_alias not_empty || exit 1
python3 "$SKILL_ROOT/scripts/_shared/fs_guard.py" "$WORK_DIR" WORK_DIR symlink || exit 1
python3 "$SKILL_ROOT/scripts/_shared/fs_guard.py" "$WORK_DIR" WORK_DIR owned || exit 1
if [ -n "$ARG_VERSION" ]; then
  python3 "$SKILL_ROOT/scripts/_shared/fs_guard.py" "$ARG_VERSION" agent_version api_name || exit 1
fi

_main_args=(--org-alias "$ARG_ORG" --agent "$ARG_AGENT" --work-dir "$WORK_DIR")
[ -n "$ARG_VERSION" ] && _main_args+=(--version "$ARG_VERSION")
[ -n "$ARG_FORCE" ] && _main_args+=(--force)
[ -n "$ARG_REPROBE" ] && _main_args+=(--reprobe)
[ -n "$ARG_PARALLELISM" ] && _main_args+=(--parallelism "$ARG_PARALLELISM")
[ -n "$ARG_MAX_MERMAID" ] && _main_args+=(--max-mermaid-nodes "$ARG_MAX_MERMAID")

set +e
python3 "$SKILL_ROOT/scripts/main.py" "${_main_args[@]}"
_rc=$?
set -e

WORK_DIR="$WORK_DIR" python3 "$SKILL_ROOT/scripts/emit_result.py"
exit "$_rc"
```
