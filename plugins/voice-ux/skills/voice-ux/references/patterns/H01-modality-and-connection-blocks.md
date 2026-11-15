---
id: H01
name: modality-and-connection-blocks
category: configuration
severity: high
applies_to: [migrate]
couples_with: [I01, H03]
detection:
  - regex: '^connection messaging:'
    in: [config]
  - structural: "no `connection telephony:` block"
    in: [config]
  - structural: "no `modality voice:` block"
    in: [config]
  - regex: '^\s*additional_parameter__disable_graph_runtime:\s*True\s*$'
    in: [config]
principle_refs: [P4]
---

# Modality and connection blocks

## Why it matters

Chat agents typically have only `connection messaging:` configured. Voice agents need additional config. There are also legacy-runtime flags that quietly drag the agent into the old Bot Builder UI even when everything else is configured for voice.

This pattern handles three concerns, in priority order:

1. **Strip `additional_parameter__disable_graph_runtime: True` if present.** This flag opts the agent into the legacy non-graph runtime, which forces it to open in the legacy Bot Builder rather than the modern Agent Script (NGA) Builder. **This is the single load-bearing change for NGA — verified in isolation testing 2026-05-19.** All other items in this pattern are recommended hygiene, not NGA-vs-legacy switches.
2. **Add `connection telephony:`** — declares telephony channel support.
3. **Add `modality voice:`** — voice settings (`voice_id`, speed, stability, similarity). Couples with H03; note that on the default v3 model only stability is honored, and selecting a non-default model needs the emerging nested format (see H03). The latency/turn-timing config (`additional_configs:` — beepboop, speak-up), STT biasing (`inbound_keywords:`), the filler-word flag (`inbound_filler_words_detection:`), and in-script custom pronunciation (`pronunciation_dict:`) are siblings inside this block; see H06, H05, and H04.
4. **Optionally add `connection customer_web_client:`** for voice-over-web multimodal AND so Agent Builder Preview works correctly. Without it, Preview can return "Something went wrong".
5. **Keep `connection messaging:`** if multi-channel (recommended — leaves the chat-fallback surface available).

This pattern is **deployment-blocking**: missing voice config means the agent doesn't function on voice channels at all. Apply early in Phase 5/7 (Application order step 1).

See also:
- `references/publish-errors/E004-disable-graph-runtime-legacy-builder.md` — full failure mode + fix for the flag
- H03 — voice settings detail

## Detection

Source `config:` block satisfies any of:
- Has `additional_parameter__disable_graph_runtime: True` (immediate rewrite — strip)
- Has only `connection messaging:`, no `connection telephony:` and no `modality voice:`

## Chat example (before)

```yaml
config:
    developer_name: "Customer_Support_Assistant_script"
    agent_label: "Customer Support Assistant"
    agent_type: "AgentforceServiceAgent"
    enable_enhanced_event_logs: True
    additional_parameter__disable_graph_runtime: True   # ← legacy-runtime flag, strip this

connection messaging:
    adaptive_response_allowed: False
```

## Voice example (after) — recommended

**Strip the legacy flag, add telephony connection and voice modality. Keep messaging for fallback. Add customer_web_client so Preview works:**

```yaml
config:
    developer_name: "Customer_Support_Assistant_voice"
    agent_label: "Customer Support Assistant (Voice)"
    agent_type: "AgentforceServiceAgent"
    enable_enhanced_event_logs: True
    # additional_parameter__disable_graph_runtime removed (defaults to False = NGA runtime)

connection messaging:
    adaptive_response_allowed: False

connection telephony:
    adaptive_response_allowed: True

connection customer_web_client:
    adaptive_response_allowed: True

modality voice:
    voice_id: "<voice_id_from_org_voice_library>"
    outbound_speed: 0.9
    outbound_stability: 0.85
    outbound_similarity: 0.85
    additional_configs:
        beepboop_config:
            max_wait_time_ms: 500           # filler audio at ~0.5s, not the 6000ms default (H06)
```

The `additional_configs:` block (beepboop / speak-up timers), `inbound_keywords:`, `inbound_filler_words_detection:`, and `pronunciation_dict:` are authored right here inside `modality voice:` — they are in-script, not Workbench-only. H06 covers the timing block in full; H05 covers `inbound_keywords` and the filler-word flag; H04 covers `pronunciation_dict`.

## Voice example — alternatives

**Telephony-only (most restrictive — minimum to run on voice):**

```yaml
config:
    developer_name: "..."
    agent_label: "..."
    agent_type: "AgentforceServiceAgent"
    enable_enhanced_event_logs: True

connection telephony:
    adaptive_response_allowed: True

modality voice:
    voice_id: "<voice_id>"
    outbound_speed: 0.9
    outbound_stability: 0.85
    outbound_similarity: 0.85
```

This works for NGA at the metadata level. It just lacks the `customer_web_client` surface, so Preview from Agent Builder may return "Something went wrong" — verify before relying.

**Voice-over-web only** (no telephony): use `connection customer_web_client:` alone, no `connection telephony:`. Voice settings still required.

**Multi-channel (chat + voice in one agent)**: keep `connection messaging` and add `connection telephony` + `modality voice`. The agent must handle both channels gracefully — most teams deploy two separate agents instead. Multi-channel coordination in one agent is a larger design problem.

## Anti-patterns

- **Keeping `additional_parameter__disable_graph_runtime: True` "because the source had it".** This flag forces legacy Bot Builder. For voice migrations targeting NGA, always strip. See E004.
- **Adding `modality voice:` without `connection telephony:`.** Voice settings exist but the connection isn't declared — agent won't actually run on voice.
- **Configuring `voice_id` as a placeholder string ("REPLACE_ME") and forgetting to fill it in.** Deploy succeeds but the agent uses the platform default voice. Add to Layer E review checklist.
- **Setting `outbound_speed: 1.5` for "faster calls".** Above 1.1 is rarely intelligible — and on the default v3 model speed has no effect at all. See H03.
- **Hard-coding `voice_id` from one org and deploying to a different org.** Voice IDs are org-scoped. Always verify the ID exists in the target org.
- **Skipping `connection customer_web_client:` "because we're voice-only".** Builder Preview typically uses the customer_web_client surface even for voice-targeted agents. Without it, the developer can't preview their agent in Builder. Cheap to include; expensive to debug "Something went wrong" later.

## Where it lives

`config:` block at the top of the `.agent` file. The `connection` and `modality` declarations are siblings of `config`. After publishing, confirm the settings reached the compiled agent (SKILL.md Phase 8, step 6): a clean publish doesn't prove they did.

## Application order

This pattern is the **first** to apply (step 1 in `README.md` Application order). Other patterns assume the voice connection / modality are present, AND assume the legacy-runtime flag has been stripped. Run this before any others.

## Verification (post-publish)

After publishing, verify NGA via SOQL (this is checked in Phase 8 step 5):

```bash
sf data query --query "SELECT DeveloperName, PlannerType FROM GenAiPlannerDefinition WHERE DeveloperName LIKE '<api_name>_v%' ORDER BY LastModifiedDate DESC LIMIT 1" --target-org <org>
```

Expect `PlannerType = Atlas__ConcurrentMultiAgentOrchestration`. If it's anything else, the legacy flag wasn't fully stripped or there's a different blocker.
