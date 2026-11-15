# Step 3 — Score Each Dimension

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 3 — Score Each Dimension
- Step 4 — Build Priority Remediation Summary
- Step 4b — Generate KPI / Success Criteria
  - How to generate
  - FDE callout — include in every document
  - KPI table columns
- Step 4a — Serialize Findings to JSON

## Step 3 — Score Each Dimension

**SCORING SCALE IS ALWAYS 1–10. Never use 1–5. Never output a score of 0. If you catch yourself writing "/5" or "out of 5", correct it to "/10" before proceeding.**

Score each dimension 1–10. Use these thresholds:

| Score | Meaning | Display colour |
|---|---|---|
| 8–10 | Well configured, minor gaps only | Green |
| 6–7 | Functional with notable gaps | Amber |
| 4–5 | Significant gaps, at-risk for go-live | Orange |
| 1–3 | Critical failures, not go-live ready | Red |

Compute **Composite Configuration Health Score** = average of 7 dimension scores, rounded to 1 decimal.

**FDE score disclaimer — include in Section 8 of every document:**

> **These scores are AI-generated based on the metadata provided and should be treated as a starting point, not a final assessment. The FDE must review each dimension score before sharing this document with the customer and adjust ratings based on:**
> - Direct inspection of the live org (planner, action, and Trust Layer configuration)
> - Any metadata not included in the retrieved package (genAiPlanners, genAiFunctions, genAiPlugins)
> - Customer context, deployment constraints, or compensating controls not visible in the metadata
>
> Scores marked `[INFERRED]` are based on bot dialog structure only and require planner validation before they can be confirmed.

---

## Step 4 — Build Priority Remediation Summary

Select all CRITICAL findings plus HIGH findings that represent go-live blockers.
Order by: CRITICAL first, then HIGH, within each by business impact.

For each item: `#` | `Area` | `Finding` | `Severity`

---

## Step 4b — Generate KPI / Success Criteria

Produce a suggested KPI table for Section 10 of the document. This section has two purposes:
1. Give the customer a concrete measurement framework to evaluate the agent post-launch.
2. Flag a clear FDE ownership boundary — suggested KPIs are derived from industry standards; customer-specific targets must be set by the FDE with the customer before go-live.

### How to generate

1. Select the baseline KPI set for the agent type from the table in **Agent-Type KPI Defaults** below.
2. Annotate each KPI with: a suggested industry benchmark, why it matters for this specific agent, and any configuration gaps that will prevent it from being measurable (e.g., `citationsEnabled: false` means hallucination rate cannot be tracked without external tooling).
3. Add any KPIs implied by the agent's specific use case (e.g., `Verification Abandonment Rate` for an agent with an OTP gate; `Points Enquiry Deflection Rate` for an agent with a loyalty topic).
4. Include the FDE callout block verbatim (see below).

### FDE callout — include in every document

> **FDE Review Required — Customer-Specific Targets Not Set**
> The KPIs below are derived from industry standards for this agent type. Suggested benchmarks are starting points only. Before go-live, the FDE must work with the customer to:
> - Validate or replace benchmarks against the customer's existing human-agent baseline
> - Add any business-specific KPIs (e.g., loyalty redemption rate, no-show dispute resolution time)
> - Confirm which KPIs are measurable given the current configuration (some require Trust Layer, CSAT triggers, or external analytics tooling)
> - Set a review cadence (recommended: weekly for the first 30 days, monthly thereafter)

### KPI table columns

`#` | `KPI` | `Category` | `Suggested Benchmark` | `Why It Matters` | `Measurable Now?`

**Measurable Now?** values: `Yes` / `No — requires [what]` / `Partial`

---

## Step 4a — Serialize Findings to JSON

**Run this immediately after completing Step 4, before spawning the doc builder.**

Write all findings to `[OUTPUT_DIR]/review-findings-[AgentName].json` (defaults to `~/Downloads` — see Step 1) using the Bash tool with a Python one-liner. Structure:

```json
{
  "agent_name": "...",
  "agent_type": "...",
  "platform": "Salesforce Agentforce",
  "customer": "...",
  "use_case": "...",
  "languages": "...",
  "review_date": "...",
  "prepared_by": "...",
  "composite_score": 0.0,
  "exec_summary": ["para1", "para2", "para3"],
  "sections": [
    {
      "number": 1,
      "title": "Persona, Tone & Topic Scope",
      "score": 0,
      "passes": [{"label": "...", "text": "..."}],
      "findings": [{"severity": "HIGH", "label": "...", "text": "..."}],
      "fixes": ["..."]
    }
  ],
  "remediation": [
    {"number": 1, "area": "...", "finding": "...", "severity": "CRITICAL"}
  ],
  "scores": [
    {"dimension": "Persona, Tone & Topic Scope", "score": 0, "rationale": "..."}
  ],
  "kpis": [
    {
      "number": 1,
      "kpi": "Containment Rate",
      "category": "Deflection",
      "benchmark": ">=70% for mature service agents",
      "why": "...",
      "measurable": "Yes | No — requires [what] | Partial"
    }
  ],
  "cost": {
    "status": "CRITICAL_WASTE | HIGH_WASTE | EFFICIENT | NOT_RUN",
    "not_run_reason": "Pricing model not established — confirm Flex Credits vs per-conversation and re-run",
    "pricing_model": "flex_credits | per_conversation",
    "rate_assumed": "20 credits/action production (voice 30); rate card 2026-02-03",
    "modeled_paths": [
      {"path": "...", "billable_actions": 5, "credits": 100, "usd": 0.50}
    ],
    "forecast_volume_per_day": 2000,
    "findings": [
      {"severity": "CRITICAL | HIGH | MEDIUM", "rule_id": "AF-COST-01", "label": "...", "text": "..."}
    ]
  },
  "static_scan": {
    "rules_total": 61,
    "pass": 0,
    "fail": 0,
    "na": 0,
    "not_assessed": 0,
    "failed_rule_ids": ["AF-SEC-01", "AF-ARCH-07"]
  },
  "permissions": {
    "status": "CRITICAL_GAPS | HIGH_GAPS | NO_GAPS_CONFIRMED | NOT_RUN",
    "not_run_reason": "Action schema metadata not available — retrieve GenAiFunction/GenAiPlugin and re-run",
    "running_user": "...",
    "permission_sets": ["...", "..."],
    "psl_licenses": ["..."],
    "findings": [
      {
        "severity": "CRITICAL | HIGH | MEDIUM",
        "check": "B — Apex Class Access | C — Object CRUD | D — FLS | E — Named Credential | F — Hygiene",
        "label": "...",
        "text": "..."
      }
    ]
  }
}
```

Write the JSON with Python so quoting and special characters are handled correctly:

```python
import json, pathlib
data = { ... }  # fill with findings
out_dir = pathlib.Path('[OUTPUT_DIR]').expanduser()  # [OUTPUT_DIR] defaults to ~/Downloads — see Step 1
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / 'review-findings-[AgentName].json').write_text(json.dumps(data, indent=2))
```

**Only proceed to Step 6 after confirming the file was written successfully.**

---
