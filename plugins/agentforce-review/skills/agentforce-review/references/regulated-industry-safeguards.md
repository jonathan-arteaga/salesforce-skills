# Regulated-Industry Agent Safeguards (P1-P8)

Focused engineering compliance and guardrail review for Healthcare, Life Sciences, Financial Services, Insurance, and Pharma agents (HIPAA, GxP, SOX, PCI lenses). Engineering patterns only—confirm legal obligations with the customer's compliance owner.

## Step 0: Scope & Applicability Gates (Run First)

1. **Read `system.instructions` first:** Classify every guardrail by enforcement tier—**Tier 1** deterministic (`run`, `set`, `if`, `transition to`, `available when`), **Tier 2** global `system.instructions`, **Tier 3** topic pipe-text (`| ...`, weakest).
2. **Enumerate write surfaces:** Inspect all `flow://` targets (`recordCreates`, `recordUpdates`, `recordDeletes`) and `apex://` `@InvocableMethod` classes (DML). Mark **P1** and **P7** `N/A` if the agent is strictly read-only.
3. **Channel & telemetry gates:** No voice channel -> **P5** voice sub-check `N/A`. No Data Cloud/STDM access -> use local preview/test trace fallback for **P6** (note reduced confidence; do not auto-GAP).

## Pattern Catalog (P1-P8)

| Pattern | Rule & Check | Key Nuance / Mitigation |
| --- | --- | --- |
| **P1 Confirmation Gate** | Every write action requires preview + explicit user confirmation before invocation. | Check write surfaces only; directly callable write in 1 turn -> finding. |
| **P2 Grounded Output Only** | Surface only action-returned values; safe empty states; never invent IDs, balances, or clinical data. | Correctly lives at Tier 2 (`system:`); watch for echoing unverified conversation input. |
| **P3 Enforcement Strength** | Hard-mandatory gates belong at Tier 1 (deterministic), never Tier 3 pipe-text alone. | **Carve-out:** Inherently probabilistic detection (crisis/intent) is NOT a FAIL—split probabilistic classification from a deterministic `after_reasoning` or action gate and note residual risk. |
| **P4 Least-Privilege Scoping** | Scope queries to entitled records (`with sharing`, `OwnerId`, verified `currentRecordId`). | **Verify as the running user, never System Administrator** (admins bypass sharing). |
| **P5 Sensitive Identifiers** | Mask/segment sensitive IDs; voice must never read full account/case/PII strings aloud. | Voice sub-check applies only when voice/telephony is enabled. |
| **P6 Audit & Traceability** | Regulated actions must be trace-verified (`ACTION_STEP` + I/O match displayed values) via `agentforce-observe`. | Without STDM, fall back to preview/test suite traces and document reduced confidence. |
| **P7 Resolve-Before-Act** | Resolve ambiguous names/numbers to one exact ID before writes; 0 -> stop, 2+ -> pick-list and stop. | Write surfaces only; multi-match must never auto-select. |
| **P8 Safety-Classifier Pitfall** | Platform content-safety classifiers can false-positive on benign clinical/pharma terms (`PHARMACY`, `SCREENING`). | **Residual risk note only (never a code FAIL).** Do NOT instruction-patch; tune Einstein Trust Layer moderation or escalate to Salesforce with trace evidence. |

## Adversarial Verify-Before-Report & Verdicts

Before filing any `PARTIAL` or `GAP`, inspect both global `system:` and deterministic blocks to avoid false positives. Assign verdicts (`PASS`, `PARTIAL`, `GAP`, `N/A`) with `file:line` evidence and severity (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`). Lower severity when Einstein Trust Layer covers the risk or a write is benign/reversible. Produce a standalone Markdown report (`regulated-industry-review-<AgentName>-<Date>.md`) or fold into [config-permission-review.md](config-permission-review.md) JSON when invoked as a supplemental section.
