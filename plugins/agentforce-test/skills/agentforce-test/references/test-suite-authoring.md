# Test Suite Authoring & OWASP Security Coverage

Author repeatable Testing Center YAML specs (`AiEvaluationDefinition` via `@salesforce/agents`) covering routing, action selection, grounding, authorization denial, persona consistency, and gated OWASP LLM Top 10 security probes.

## Canonical Testing Center YAML Schema

Author YAML directly (never run interactive `sf agent generate test-spec` in agentic workflows). Only recognized `@salesforce/agents` keys are allowed—do NOT add `apiVersion`, `kind`, `metadata`, or `settings`:

```yaml
name: "<Agent_Name> Regression Suite"   # Required MasterLabel
subjectType: AGENT                      # Required
subjectName: <BotDefinition_ApiName>    # Required
testCases:
  - utterance: "Check status of synthetic order ORD-0001"
    expectedTopic: Order_Support        # Maps to subagent in .agent
    expectedActions:                    # Flat list of action API names
      - Get_Order_Status
    expectedOutcome: "Returns synthetic order status without inventing fields."
```

### Standard Suite File Layout

Store authored suites under `<project-root>/tests/`:

- `<AgentApiName>-testing-center.yaml` — Full CI/CD regression suite (Mode B)
- `<AgentApiName>-regression.yaml` — Regressions derived from production failures (`agentforce-observe`)
- `<AgentApiName>-smoke.yaml` — Fast preview smoke utterances (Mode A)
- `<AgentApiName>-security.yaml` — OWASP LLM Top 10 security suite (Mode C1)

## Mandatory Regression Coverage Matrix

Derive test cases directly from the `.agent` file, Agent Spec, and Data Library boundaries:

1. **Routing & ambiguity:** Every reachable subagent/topic, overlapping boundary utterances, multi-turn continuation (`runtime.reset_to_initial_node`), and standard `Escalation` (`localDeveloperName`).
2. **Action & idempotency:** Expected action invocation, missing required inputs, action error/empty-state handling, and duplicate-call/retry safety.
3. **Grounding & abstention:** Supported facts with citations, out-of-scope abstention ("nothing found" instead of fabrication), stale/conflicting docs, and hostile instructions embedded inside retrieved records.
4. **Authorization & cross-customer denial:** Unauthorized record IDs, cross-customer lookup attempts (especially Service Agents running as an Agent User), and sensitive field minimization.
5. **Persona & overrides:** Tone Flex shifts + reset, Never-Say enforcement, and subagent `system` override retention.

## Mode C: OWASP LLM Top 10 Security Testing (Confirmation Gate)

Security testing is part of the ADLC, but **generating or executing security test cases requires explicit user confirmation first**. Tailor probes directly to the agent's `.agent` logic and business domain across 7 core OWASP categories:

- **Prompt Injection (direct & indirect)** — instruction override, delimiter breaks, embedded record payloads.
- **Sensitive Information Disclosure** — PII/PHI/internal plumbing (`action` names, field names, record IDs), system prompt extraction.
- **Excessive Agency & Authorization Bypass** — unconfirmed writes, skipping verification gates, cross-user record access.
- **Hallucination / Grounding Manipulation** — false premises, forced fabrication under pressure.
- **System / Tool Abuse & DoS** — transition loops, unbounded multi-action fan-out, malformed inputs.

Deliver as **C1** (persistent Testing Center suite deployed via `sf agent test create`) or **C2** (live adversarial preview probes with A-F severity grading, defaulting to `--simulate-actions`).
