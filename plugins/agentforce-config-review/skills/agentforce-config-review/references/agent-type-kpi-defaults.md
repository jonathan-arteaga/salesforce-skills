# Agent-Type KPI Defaults

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Agent-Type KPI Defaults

Use these as the starting point for Step 4b. Supplement with use-case-specific KPIs derived from the agent's topic list.

> **Note:** The full KPI table has 6 columns: `#` | `KPI` | `Category` | `Suggested Benchmark` | `Why It Matters` | `Measurable Now?`. The defaults below show only the first 4 columns — `Why It Matters` and `Measurable Now?` are populated at runtime based on the specific agent's configuration and any gaps identified during the review.

### Service Agent (consumer-facing)

| # | KPI | Category | Suggested Benchmark |
|---|---|---|---|
| 1 | Containment Rate | Deflection | ≥70% at 90 days (Salesforce State of Service benchmark) |
| 2 | First Contact Resolution (FCR) | Quality | ≥65% for handled conversations |
| 3 | Average Handle Time (AHT) | Efficiency | Establish baseline vs. human agent AHT in week 1 |
| 4 | CSAT / Agent Rating | Satisfaction | ≥4.0/5.0 (Salesforce benchmark for AI-assisted service) |
| 5 | Escalation Rate | Deflection | ≤20% of conversations escalate to human |
| 6 | Unresolved / Abandoned Rate | Quality | ≤10% — conversations where user disengaged without resolution |
| 7 | Ticket Deflection Rate | Efficiency | ≥50% — conversations resolved without ticket creation |
| 8 | Verification Completion Rate | Security | ≥85% of OTP flows completed successfully (if agent uses OTP gate) |
| 9 | Topic Mis-Routing Rate | Accuracy | ≤5% — conversations routed to wrong topic or re-routed mid-session |
| 10 | Hallucination / Incorrect Answer Rate | Trust | ≤2% (requires external QA sampling if Trust Layer absent) |

### SDR / Sales Agent

| # | KPI | Category | Suggested Benchmark |
|---|---|---|---|
| 1 | Meeting Booked Rate | Pipeline | ≥15% of qualified conversations result in calendar booking |
| 2 | Sequence Opt-Out Rate | Compliance | ≤3% — monitor for messaging tone or compliance issues |
| 3 | Response Rate | Engagement | ≥40% reply rate for outbound sequences |
| 4 | Containment Rate | Deflection | ≥60% — queries handled without human SDR involvement |
| 5 | Bilingual Handling Rate | Quality | 100% of non-English inbound replied in matching language |

### Field Service Agent

| # | KPI | Category | Suggested Benchmark |
|---|---|---|---|
| 1 | Appointment Self-Service Rate | Deflection | ≥60% of scheduling requests handled without dispatcher |
| 2 | SLA Commitment Violation Rate | Compliance | 0% — agent must never quote arrival times without system data |
| 3 | Work Order Write-Back Success Rate | Integration | ≥99% — work order updates logged without error |

### Employee Agent

| # | KPI | Category | Suggested Benchmark |
|---|---|---|---|
| 1 | Self-Service Resolution Rate | Deflection | ≥60% of HR/IT queries resolved without human escalation |
| 2 | Audit Trail Completeness | Compliance | 100% — every Finance/HR action logged |
| 3 | PII Exposure Incidents | Security | 0 — measure via field-level minimization + Trust Layer audit trail; **not** masking, which is disabled for agents |

### AgentScript Agent

| # | KPI | Category | Suggested Benchmark |
|---|---|---|---|
| 1 | Script Completion Rate | Quality | ≥85% — conversations that reach a terminal step (resolved or transferred) without abandonment |
| 2 | Dead-End Rate | Quality | ≤2% — conversations that reach a step with no valid next path |
| 3 | Wrong-Branch Rate | Accuracy | ≤5% — conversations where conditional logic sent the user to the wrong branch |
| 4 | Transfer Success Rate | Integration | ≥98% — transfer steps that successfully hand off to a human queue |
| 5 | Script Bypass Attempt Rate | Security | Track — conversations where users attempted to skip or circumvent script steps |
| 6 | Average Steps to Resolution | Efficiency | Establish baseline; target reduction of ≥20% vs. v1 after first 30 days |
| 7 | Step Error / Exception Rate | Reliability | ≤1% — steps that threw an error or timed out |

---
