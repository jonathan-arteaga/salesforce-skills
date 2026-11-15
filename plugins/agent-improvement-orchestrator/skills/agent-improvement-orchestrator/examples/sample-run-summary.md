## Acme_Support_Agent — Improved ✓ · 6.5 → 9.0 · tests 67% → 89% · 0 regressions

> Sample / illustrative deliverable. No real org, customer, or PII.

Reviewed the agent, found 4 issues, fixed the 3 priority ones in a single iteration, and
re-tested with no regressions. One LOW issue (no Refunds topic) was deferred.

### What improved   (evidence)
- Stopped inventing discounts (D2-H1, HIGH)              review D3-Guardrails · test P2-Q2 ↑
- Stays in role under jailbreak (D2-M1, MEDIUM)          review D3-Guardrails · test P3-Q1 ↑
- Retries Knowledge fetch before failing (D3-M1, MEDIUM) review D4-Knowledge
→ Score 6.5 → 9.0, pass rate 67% → 89% (6/9 → 8/9). Deferred: D1-L1 (no Refunds topic, LOW).

### Evidence
- Before: review-Acme_Support_Agent-2026-05-30.docx (6.5) · report-baseline.html (67%)
- After:  review-Acme_Support_Agent-2026-05-30-v2.docx (9.0) · report-iter1.html (89%)
- Changes: commit a1b2c3d
- All artifacts: see `outputs[]` in loop-state-Acme_Support_Agent__00Dxx0000000000EAA.json

Run: dev@acme-support.example.com · /Users/dev/projects/acme-support · iter 1/3 · full_ownership · 2026-05-30T15:05:00Z
