# Step 4: Draft subagents

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 4: Draft subagents
- Step 4.5: Pattern selection
- Step 5: Classification descriptions
- Step 6: Routing clarity test
- Step 6.5: Routing contract capture
- Step 7: Scope per subagent
- Step 8: Action definition
- Step 8.5: Integration map (optional, FDE-leaning)
- Step 8.6: Voice / channel variant capture (Channel customisation mode only)
- Step 8.7: Decision-points capture (Script comparison mode only)
- Step 9: Platform dependency banner (optional)
- Step 9.5: Instruction override capture

### Step 4: Draft subagents

Cluster MVP capabilities into proposed subagents. For each:

```yaml
id: [kebab-case slug]
name: [name in persona voice]
stage: [lifecycle / domain / intent / hybrid]
color: [hex from a curated palette — the page renders subagent stripes from this]
owner: fde | customer | joint | external
capabilities: [capability IDs from capabilities.yaml]
what_it_does: [one paragraph — reviewer-facing, what this subagent handles]
why_it_exists: [one paragraph — the rationale, grounded in capability data and (if available) transcript insights]
```

If persona is absent, name subagents functionally and flag for voice pass.

**When a baseline `.agent` is loaded** (Redesign / Channel-customisation / Script-comparison): seed the subagents array from the baseline's topics. Preserve baseline IDs verbatim so downstream references (decision-points, variants) resolve cleanly.

**For Redesign mode** (or Redesign combined with anything else), additionally capture per subagent:

- `risk` — `Low` (mostly preserved) / `Medium` (substantial rework) / `High` (mostly new)
- `carries_forward` — string or null. What from the existing agent carries into this subagent.
- `changes_from_today` — string or `{ lead, points }` object. What's different from today.

**Auto-draft from baseline** — when a baseline `.agent` is present, draft the continuity paragraph from the baseline text instead of asking the user blind. Present per subagent:

> "**[Subagent name]** — here's my continuity draft based on the baseline:
>
> - **Continuity risk:** Medium *(substantial rework — capture flow replaced, rendering rewritten for spoken prose; core routing preserved)*
> - **Carries forward:** [drafted paragraph derived from baseline scope + preserved capabilities]
> - **Changes from today:** [drafted bullets derived from delta between baseline and target design]
>
> 1. **Looks right, continue**
> 2. **Adjust the risk level** — say which and why
> 3. **Edit the paragraph or bullets** — I'll incorporate
> 4. **This subagent is genuinely new** — no carries-forward, drop the block"

The user confirms rather than composes. When no baseline is loaded (Redesign without export, verbal description path), fall back to asking blind.

**For all engagements**, additionally capture per subagent:

- `intents_owned` — array of `{ id, name, sessions?, verdict?, note? }`. If `_local/data/transcripts/intents.json` is loaded, populate `sessions` and `verdict` from it; otherwise leave those fields out and just capture intent name + ID.
- `failure_triage` — array of `{ status: "fixed" | "needs_work" | "deferred", text, addressed_by? }`. Derive from `_local/data/transcripts/coverage.json` if present (intents marked `Covered poorly` / `Missed` become triage entries with `status: "needs_work"`; the redesign's planned address shows up in `addressed_by`). Else omit.
- `open_questions` — array of strings. What's not yet decided about this subagent — surfaces to reviewers.

### Step 4.5: Pattern selection

Before drafting classification descriptions, surface which **founding patterns** (if any) the drafted subagents are leaning on. The pattern library lives in [`references/patterns/`](patterns/README.md) — currently `deterministic-router`, `identity-ladder`, `verification-facade`, `escalation-reason-key`, `business-topic-slot`. Each pattern has a shape contract, a when-to-use rule, and cross-skill resolution notes so downstream skills (`conversation-design`, `voice-ux`, `agentforce-generate`) can wire against the same contract.

Walk the subagent list and, per subagent, pick zero or more patterns. For each pick, capture:

```yaml
patterns:
  - name: <pattern-slug>                 # e.g. "identity-ladder"
    rationale: <one-sentence why>        # grounded in a capability, deliverable, or evidence
pattern_contract:                        # optional; keyed by pattern slug
  identity-ladder: { factors: [...], escape_hatches: [...] }   # shape from the pattern file
```

When the design has settled a pattern's contract, record it under `pattern_contract.<pattern-slug>` using the contract shape in that pattern's file. Leave it out while the contract is still open.

**Rules:**
- Reference only patterns included in `references/patterns/`. Describe an unsupported design as a proposal; do not claim an existing pattern or upstream approval.
- Picking a pattern is a commitment: downstream skills will resolve the contract shape and expect the fields it names. Only pick what the design actually uses.
- No patterns is a valid answer. Not every subagent fits one, and padding with unnecessary patterns dilutes the signal for reviewers.

Patterns picked here are rendered on the architecture page beside the subagent name so reviewers (and downstream skill authors) can see the shape the design is leaning on.

### Step 5: Classification descriptions

For each subagent, draft the **classification description** — the "when to route here" instruction that the master agent reads at runtime. Plain user-language, not config-language.

**Good:** *"Use this subagent when the student is exploring properties without a specific one in mind — looking at options, comparing locations, or asking what's available."*

**Bad:** *"Property browsing intent classifier — handles GET requests for property data."*

### Step 6: Routing clarity test

Compare classification descriptions pairwise. If two subagents' descriptions overlap on the same user input, flag for sharper boundaries:

```
⚠ ROUTING OVERLAP
────────────────────────────────────────────────
Subagent A: "Discovery"  — handles students exploring
Subagent B: "Booking"    — handles students ready to book

Overlap: "I'd like to see what's available for September"
could route to either.

Recommended: tighten one boundary, or merge if the
distinction won't survive in practice.
────────────────────────────────────────────────
```

Surface this before locking the structure.

**This is a design-review check.** It catches overlaps on paper. Runtime routing diagnostics — detecting ambiguous actual-user utterances against the deployed classifications — are owned by `agentforce-generate` `references/agent-audit-diagnostics-instructions-routing.md` and `agentforce-test` (ambiguous-utterance tests). This step does not simulate runtime routing; it validates that the drafted classifications don't overlap on obvious inputs.

### Step 6.5: Routing contract capture

For each handoff between subagents — and from `start_agent` into any subagent — capture the routing contract. This closes a historical gap: routing was described in prose on each subagent but never named with a stable shape, which meant two reviewers could read the same subagent and disagree on which conditions actually fire the handoff.

Per handoff, capture three categories of fields:

```yaml
routing_contract:
  from: <subagent-id-or-start_agent>
  to: <subagent-id>
  mechanism: invariant | judgment | filtered   # how the route is chosen (see below)
  reason: <one sentence — why this mechanism>
  invariant_fields:                      # fields that MUST be present on handoff
    - { name, type, source }
  judgment_fields:                       # fields the master agent decides on (not deterministic)
    - { name, decision_statement }
  filtered_fields:                       # fields explicitly excluded from the handoff payload
    - { name, reason }                   # typically PII or large context the receiver doesn't need
```

`mechanism` names how the route is chosen: `invariant` (a deterministic transition that always fires when its condition holds), `judgment` (the router or subagent decides from the conversation), or `filtered` (the route is only offered when state allows it). `agentforce-generate` maps each one to Agent Script.

**Where it is written.** A handoff between subagents is stored on the source subagent as `handoff_triggers[].routing_contract` (with `to` matching that trigger's `target`). The `start_agent` entry into a subagent is stored on the receiving subagent as `entry_route`, with an extra `condition` field describing when it fires.

**Why three categories.** `invariant` names the contract (what the receiver can rely on). `judgment` names the honest-uncertainty surface (what the master agent is deciding, not just forwarding). `filtered` names the quiet decision not to pass something that was available (PII hygiene, context budget) — making the omission auditable instead of invisible.

**For `start_agent` entry.** When the entry uses the [`deterministic-router`](patterns/deterministic-router.md) pattern, its design contract lines up with these categories — `stage_variables` are invariant, `ordered_transitions` are the judgment layer, `escape_hatches` short-circuit before judgment fires. These are design terms; `agentforce-generate` maps them to Agent Script variables, conditional transitions, and `available when` filters.

**For Redesign / Script-comparison with a baseline `.agent`.** Draft the contract from the baseline's existing transition fields and ask the user to confirm each category. The baseline is authoritative; the skill is codifying what's already there, not inventing new fields.

### Step 7: Scope per subagent

For each, capture:
- **In-scope capabilities** — capability IDs (already on each subagent from Step 4)
- **Out-of-scope** — what the subagent does *not* handle, with handoff target (another subagent or human)
- **Required context** — what the master agent must hand in (auth state, prior conversation, user metadata). The physical shape of those stage variables and the valid runtime surface for them is owned by `agentforce-generate` `assets/agent-spec-template.md` (Variables and Deterministic Controls). This step captures the design intent — which values each subagent genuinely needs — not the platform shape.
- **Handoff triggers** — explicit conditions that route out (e.g. *"if the student asks about billing, hand off to Account subagent"*)

### Step 8: Action definition

For each MVP capability inside each subagent, define the action(s) that deliver it.

**Action `type`** (the design semantic — what's preserved vs new):

- `preserved` — exists in the current agent, carrying forward unchanged. Redesign-only.
- `modified` — exists today, being updated. Redesign-only.
- `new` — net new for this build.
- `stretch` — potentially in scope, not committed to MVP. Renders in the page distinctly so reviewers know it's speculative.

**Action `impl_type`** — the canonical enumeration of action implementation types (Flow / Apex / Prompt Template / MCP / Headless / Knowledge / etc.) and the per-shape defaults are owned by `agentforce-generate` `references/actions-reference.md` and the Salesforce Agent Script Reference: Actions page. This skill captures the implementation **preference** (what the team wants the FDE to use) and defers to the canonical source for the valid values and the shape-to-type mapping. Use whatever string the team names; the canonical skill will validate at build-time.

**Per action, capture:**

```yaml
- id: [kebab-case action ID]
  capability_id: [P3, P5, etc. — references capabilities.yaml]
  name: [the action name as it'll appear in Agentforce Builder]
  type: preserved | modified | new | stretch
  impl_type: [team-named preference — resolved against canonical actions-reference at build]
  purpose: [one sentence — what this action does]
  inputs:
    - { name, type, source: prior_turn | user_input | session_context | external_system, required: true|false }
  outputs:
    - { name, type: structured | text | enum, consumed_by: [next_capability_ids] }
  dependencies:
    upstream_actions: [action IDs]
    auth_state: anonymous | authenticated | staff
    prerequisite_data: [...]
  build_owner: fde | admin | platform | external
```

Confirm the implementation preference with the team — it is sometimes constrained by the platform team's build posture (e.g. *"we use Flows for everything to keep admin-buildable"*).

**Build owner is required.** Surfacing this prevents capabilities sliding from MVP because nobody owned them. If a capability has no owner, flag it and either reassign or demote to Phase 2 / Stretch.

### Step 8.5: Integration map (optional, FDE-leaning)

External systems the agent depends on. Captured on a third tab on the architecture page (Integration), hidden by default — the tab only appears when one or more integrations are recorded. **Designed to disappear when the future Technical Spec skill ships** and takes over integration ownership; until then, FDEs need a home for this content.

**Skip the entire step in customer mode** (`engagement.customerMode === true`) — integration plumbing isn't customer-facing.

**Skip if `engagement.type === "concept"`** — concept-fidelity engagements aren't ready for integration mapping.

Otherwise, ask once at the start of the step:

> "Want to capture the integration map now? It's the external systems the agent depends on (named credentials, APIs, data sources) — useful for handoff to the FDE and for flagging blockers. You can skip and come back later via 'refresh integrations' if it's not ready yet.
>
> 1. **Yes, walk me through it** — I'll guide capture per integration
> 2. **Skip** — I'll mark integrations as 'pending FDE input' on the page"

**If the user picks 1**, walk through each integration the actions reference. Sources to scan first: `actions.yaml` entries with `dependencies.upstream_actions` pointing outside the agent, `inputs[].source: external_system`, `dependencies.prerequisite_data` mentioning external sources.

For each integration, capture:

```yaml
- id: [kebab-case ID, e.g. "salesforce-orders-api"]
  name: [display name, e.g. "Salesforce Orders API"]
  type: api | named_credential | mcp_server | knowledge_source | data_cloud | external_system | other
  purpose: [one sentence — what the agent uses this for]
  used_by:
    actions: [action IDs that call this integration]
    subagents: [subagent IDs whose actions depend on this — derived from actions.subagents]
  ownership: fde | customer | joint | external
  blocks_e2e_testing: true | false   # is this on the critical path for end-to-end testing?
  blocker_reason: [if blocks_e2e_testing: true, one-line reason]
  auth: [auth approach — named credential, OAuth flow, API key, etc.]
  data_classification: [PII / regulated / public / internal — drives compliance review]
  notes: [open questions, environment-specific quirks, etc.]
```

**If the user picks 2 (skip)**, write `architecture.integrations = []` and a `architecture.integrations_pending: true` flag. The page renders the Integration tab with a single "FDE input pending" panel and a re-run hint.

**Re-run handling.** If `architecture.integrations` already exists from a prior run, ask:

> "Existing integration map: [N] integrations. What would you like to do?
>
> 1. **Refine** — walk through and edit
> 2. **Add new** — keep existing, add more
> 3. **Replace** — discard and re-capture from scratch"

**Why this is in the architecture skill (for now).** The integration map is build-detail and belongs philosophically with the Technical Spec deliverable. That skill doesn't exist yet. Until it does, FDEs run an architecture skill that excludes their build content — which means integration data gets captured in private notes that never make it into the engagement state. Putting integrations here as an optional, hidden-by-default tab is a pragmatic bridge: FDEs have a home for the work, the customer-facing page stays clean (Integration tab hidden in customer mode), and when Technical Spec ships, the data migrates cleanly via shared action IDs.

**Integrations are channel-agnostic.** A voice channel doesn't get a separate integration list from chat — instead, any per-channel integration difference (e.g. Vonage/telephony for voice, Web Messaging for chat) is captured inline in the integration's `notes` field. This keeps the map single-source and stops it forking across channels.

### Step 8.6: Voice / channel variant capture (Channel customisation mode only)

> **Scope.** This step captures the **channel-variant overlay** (what differs per channel at the design level) and **voice open questions** (investigations that must close before a variant can lock). The voice-specific *rewrites* — ASR-safe capture ladders, repair tiers, spoken-prose rendering of structured outputs — belong in `voice-ux`. Voice latency trade-offs belong in `agentforce-generate` `references/voice-latency-heuristics.md`. This step draws from the baseline and names the deltas; the rewrites and latency judgements happen in those downstream skills.

For each subagent — and again per action inside it — draft a `<channel>_variant` block from the baseline text + channel defaults matrix (Step 1.7), then confirm with the user.

**Per subagent:**

> "**[Subagent name]** — here's my draft voice variant:
>
> - **Severity:** major *(baseline capture flow uses chat error strings + strict validation; voice needs echo-and-repair + tiered recovery)*
> - **Summary:** Capture path replaced (phone-first ladder); rendering rewritten for spoken prose; multi-article handled by index selection.
> - **Deltas:**
>   - Capture path replaced — caller-phone lookup → account-phone lookup → full tracking number with sender-name confirmation.
>   - Single-article rendering — Markdown card replaced with spoken prose by milestone status.
>   - Failure repair ladder — Tier 1 open repair → Tier 2 chunked dictation → Tier 3 state-preserving handoff.
>
> 1. **Looks right, continue**
> 2. **Adjust the severity** — say why
> 3. **Edit the summary or deltas** — I'll incorporate
> 4. **Add a voice open question** — for anything that needs investigation before it can be locked
> 5. **Skip this subagent** — no meaningful variant needed"

**YAML shape** (per subagent — single-channel case):

```yaml
voice_variant:
  severity: minor | major   # minor = channel tweaks only; major = capture/rendering/repair rewritten
  summary: <one-line summary of the variant>
  deltas:
    - <delta>
    - <delta>
```

**Multi-channel case** (Step 1.7 picked more than one target channel):

```yaml
variants:
  voice: { severity, summary, deltas: [...] }
  multimodal: { severity, summary, deltas: [...] }
```

**Voice open questions** — when the user picks option 4, capture under `voice_open_questions[]` on the subagent (AusPost pattern — inline, not a separate file):

```yaml
voice_open_questions:
  - title: <short question>
    context: <why this is unresolved>
    prompt: <the investigation to run>
    if_yes: <what changes if the investigation confirms>
    if_no: <what changes if it doesn't>
    owner: <who owns the investigation>
```

**Per action** — same confirmation pattern, additionally covers:

```yaml
voice_variant:
  severity: minor | major
  progress_message: <conversational voice replacement for the chat progress message>
  modifications:
    - <output rendering change>
    - <URL policy change>
    - <response-length shaping>
```

**Drafting strategy** — the skill drafts variants for every subagent and action automatically (not just the ones the user flags), then accepts "skip this subagent" as a valid answer. Reasoning: forcing the user to name which subagents need a variant first requires the same domain knowledge the skill is trying to codify.

### Step 8.7: Decision-points capture (Script comparison mode only)

The skill walks the baseline `.agent` sequentially — config block, global instructions, then each subagent's `before_reasoning` + `reasoning` blocks, then each action — and drafts before/after recommendation cards against the checked deliverables (Step 1.6).

**Confirmation happens section-by-section** — not per-record (too much friction) and not silent-then-summary (too easy to miss). Per section, present a compact table with bulk-accept:

> "**Section 1 of 6: Config + language + welcome** — 4 recommendations drafted.
>
> | # | Title | Scope | Cites |
> |---|---|---|---|
> | 1 | Production-clean agent naming | script | Persona §8 |
> | 2 | Drop 'Full' from welcome message | script | Persona §7, §8 |
> | 3 | Swap primary locale to en_AU | script | engagement config |
> | 4 | Add Welcome / AI Disclosure to global phrase book | script | Persona §9 |
>
> 1. **Accept all 4 and continue to next section**
> 2. **Open [#]** — I'll show the before/after and let you edit
> 3. **Reject [#]** — mark as skipped, no card written
> 4. **Add a recommendation I missed** — describe what
>
> Or say 'accept all remaining sections' to bulk-accept everything and I'll flag any pending ones."

**Per-card shape:**

```yaml
- id: <kebab-case-id>
  iteration: <int>                # review order — assigned in scan order (top of .agent down)
  requirement_ref: <string>       # persona §N, R-ID, CD scenario turn — resolvable by LinkifiedText
  subagent: <string>              # can be a path e.g. "customer_verification.reasoning"
  title: <string>
  change_scope: script | flow | ivr | knowledge | integration | site
  before_text: |
    <verbatim from baseline .agent>
  after_text: |
    <AXS-recommended replacement>
  recommendation: <rationale + FDE ask>
  pending: <optional — what's blocking finalisation, e.g. "Des confirming balance read-back format">
  decision: <optional — will-implement | wont-implement | needs-discussion>
```

**Change scope defaults** — the skill assigns `change_scope` based on where the edit lands: text inside the `.agent` = `script`; changes to a Flow's decision logic = `flow`; changes to Vonage/IVR routing = `ivr`; Knowledge Library article edits = `knowledge`; named-credential / integration edits = `integration`; changes to the AXS hub itself = `site`. User can override at the "Open [#]" step.

**Rationale ref auto-population** — pulled from where the recommendation cites: persona section anchor (§N), requirement ID (R-ID), CD scenario turn (`hp-golden Turn 11`), or a workshop decision label supplied at Step 1.6. Resolved at render time by the hub-side LinkifiedText.

**After the walk-through**, write `decision-points.yaml` and then ask what the user wants to do next:

> "Drafted [N] recommendations. Written to `_local/data/decision-points.yaml`.
>
> The proposed `.agent` file and the developer worklist are separate, explicit next steps. What would you like to do?
>
> 1. **Refine yaml first** *(recommended)*
> 2. **Hand the approved changes to `agentforce-generate` for a proposed `.agent`** — it produces the candidate source and validates it; the result stays labelled "proposed, not validated" until it compiles
> 3. **Create a developer worklist from approved changes** *(only when `designing-agentforce-labs:agentscript-change-worklist` is installed)* — invoke that Labs skill for recommendations already marked `will-implement`; it will ground them against current source and package the implementation handoff"

Offer option 2 only when at least one recommendation is marked `will-implement`. Offer option 3 only when recommendations are approved **and** the Labs worklist skill is available; do not prompt to install Labs as part of the core workflow. Without Labs, retain the approved `decision-points.yaml` as the developer handoff and explain that an optional worklist can be generated later. The handoff is opt-in; never invoke it automatically. If no decisions are approved yet, tell the user to settle them before generating a worklist. `designing-agentforce-labs:agentscript-change-worklist` can also be invoked independently with approved changes from another source, so Agent Architecture is not a prerequisite.

**Gated handoffs:** the proposed `.agent` never generates automatically, and this skill does not write it. The user reviews `decision-points.yaml` first, adjusts any card, then explicitly asks for the proposed file, which `agentforce-generate` produces. The worklist also requires an explicit request and includes only approved `will-implement` decisions. These gates prevent unvalidated recommendations from appearing as implementation-ready changes.

### Step 9: Platform dependency banner (optional)

Some engagements have a single biggest external dependency that's worth surfacing as a page-level banner above the architecture (the Scape engagement has the property data layer schema + Data Cloud / Apex split). If applicable, capture:

```yaml
title: [one-line summary]
body: [paragraph — what this is, what depends on it, what it blocks]
```

The page renders this as a yellow warning banner so reviewers don't read the architecture as solving a problem that's actually upstream of the agent.

If no platform dependency exists, omit. Don't fabricate one.

### Step 9.5: Instruction override capture

Per subagent, capture any **instruction overrides** that live on that subagent's `system:` block in Agent Script and intentionally diverge from the global instructions. The register makes overrides reviewable instead of silently stacking up.

```yaml
instruction_override:                   # stored on the subagent it applies to
  summary: <one-line>
  overrides_rule: <global-rule-ref>     # which global rule this diverges from
  reason: <why this subagent needs the divergence>
  must_restate:                         # global invariants the override must carry
    - <e.g. AI disclosure>
  risk_if_omitted: <what breaks if an invariant is dropped>
```

A subagent `system` block replaces the global instructions for that subagent, so `must_restate` lists every global invariant (identity, disclosure, safety, never-say) the override still has to carry. `agentforce-generate` `references/instruction-resolution.md` owns how the override is written.

**When to capture.** Any time a subagent's `system.instructions` text contradicts or narrows a rule in global instructions. Examples: a verification subagent that uses stricter language than the global persona (`"Confirm each digit back to the caller before advancing"`); a compliance subagent that overrides the global "never read URLs aloud" with a jurisdictionally required disclosure URL readback.

**When NOT to capture.** Additive, non-conflicting detail belongs in the subagent's instructions without a register entry — that's just normal subagent-specific guidance. The register is for conflicts.

**Why this matters.** Overrides tend to accumulate silently in production agents until the agent's actual behaviour has drifted from what the design doc describes. A deliberate register makes the drift legible and gives reviewers a surface to challenge each override on.
