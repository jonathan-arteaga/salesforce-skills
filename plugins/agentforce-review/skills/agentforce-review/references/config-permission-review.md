# Configuration & Permissions Health Review

Conduct a structured, evidence-backed Agentforce configuration review across 7 core dimensions plus 2 supplemental dimensions (D8 Permissions & Identity, D9 Cost & Consumption), producing verified findings JSON and an optional stakeholder report (`.md` or `.docx`).

## The 9 Review Dimensions

| Dim | Focus | Key Checks |
| --- | --- | --- |
| **D1** | Persona, Tone & Topic Scope | Clear role, non-overlapping subagent/topic routing descriptions, consistent voice |
| **D2** | Instructions, Actions & Fallback | Deterministic gates vs. pipe-text, dead ends, action output handling, retry/fallback clarity |
| **D3** | Guardrails, Safety & Responsible AI | Escalation triggers, verbal abuse/crisis, competitor/opt-out rules, Einstein Trust Layer topics |
| **D4** | Variable Typing & Data Integrity | Typed state, lifecycle resets, `isPII` flags, no cross-turn leakage |
| **D5** | Knowledge Grounding & Hallucination | Data Library/retriever readiness, static prefilter awareness, explicit empty states, citations |
| **D6** | Data Residency & AI Governance | Zero retention + field minimization (LLM masking is disabled for agents), transcript PII hygiene |
| **D7** | CRM Integration, Logging & Errors | Case/activity/VoiceCall logging, Flow fault paths, idempotency, unreachable steps |
| **D8** | Permissions, Identity & Access *(supplemental)* | **REQUIRED for Service & SDR agents:** running user, Apex access, CRUD, FLS, Named Credentials, Permission Sets |
| **D9** | Cost & Consumption *(supplemental)* | Establish exact pricing model before quoting numbers; report arithmetic (LLM passes/action fan-out), not adjectives |

## Mandatory Execution Gates

- **D8 gate (Service & SDR agents):** Never skip D8 because the running user wasn't pre-supplied. If connected to an org, query the running user and run sub-sections A-F (Running User, Apex Access, Object CRUD, FLS, Named/External Credentials, Permission Set Hygiene). If offline, set `permissions.status = "NOT_RUN"` with `not_run_reason` and surface it in the scorecard. For Employee, Field Service, or Agent Script agents without a dedicated Agent User, mark `NOT_RUN` with explicit rationale.
- **Voice agent triage (`isVoiceAgent: true`):**
  1. Run a silent `PASS`/`CHECK`/`N/A` metadata triage first; promote only `CHECK` items to findings.
  2. Emit **D8a** as a compact binary table (`PASS`/`FAIL`/`N/A`), escalating failures into D2 (timeouts/retries), D3 (consent/PCI), or D7 (logging).
  3. Split D7 voice checks into `[METADATA]` vs. `[REQUIRES LIVE TEST CALL]`—never mark live-call items `PASS` from config alone; mark them `[UNVERIFIED]`.
  4. Inspect actual Real-Time Streaming call recording settings and Flow overrides before assessing notice/consent—never auto-mark recording N/A.
- **Regulated industries:** Automatically fold in [regulated-industry-safeguards.md](regulated-industry-safeguards.md) as a supplemental section (excluded from composite score; full severity promoted to Priority Remediation).

## Severity Scale & Output Contract

- **CRITICAL:** Go-live blocker (brand, legal, compliance, cross-customer data exposure).
- **HIGH:** Major operational or quality risk; fix before launch where possible.
- **MEDIUM:** Recommended improvement with remediation plan.
- **LOW:** Minor optimization.

Complete and verify the findings JSON before rendering any summary or Word document (`agentforce-review-<AgentName>-<Date>.docx`). Keep scores as structured review indicators, never deployment certifications. Route permission fixes to `salesforce-security-access` and `.agent` edits to `agentforce-build`.
