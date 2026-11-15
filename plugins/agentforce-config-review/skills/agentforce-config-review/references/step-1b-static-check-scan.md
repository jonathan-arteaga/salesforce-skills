# Step 1b — Run the Static Check Scan

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Step 1b — Run the Static Check Scan

**Run `references/static-checks.md` against the retrieved metadata before writing any finding.** The catalog is 61 rules decidable mechanically — a grep, a set difference, a graph property, or a count — with no org access and no judgement required.

Record each rule as PASS, FAIL (with the file and line that proves it), N/A (with a reason), or NOT ASSESSED (with what was missing). A rule you did not check is not a PASS.

Why this ordering: drafting prose first and scanning second produces a review shaped by whatever you noticed first. Scanning first produces one shaped by evidence, and makes the review reproducible — a second reviewer running the catalog should reach the same findings.

**Findings from the scan file into the dimensions**, exactly as action schema findings do. The catalog tags every rule with its destination dimension. `AF-COST` is the sole exception and files into Dimension 9 (Cost & Consumption Efficiency).

**Token cost:** the catalog is a reference file, so it costs nothing until read. Read it once at this step, record results as compact PASS/FAIL lines, and do not re-read it while drafting. The scan results are what you carry forward, not the catalog.

**A clean scan is not a passing dimension.** The catalog covers the mechanical floor only. D3 has just three mechanical guardrail rules, and the most severe guardrail failure mode — an injection guardrail broad enough to block the agent's own primary workflow — cannot be detected mechanically at all. Continue to the full dimension analysis in every case.

Start with the five cheapest high-yield rules: `AF-SEC-01` (empty subagent description), `AF-PER-02` (unreplaced placeholder text), `AF-VAR-11` (masking explicitly disabled), `AF-REL-01` (deprecated parameter now a hard error), `AF-ARCH-07` (transition to an undefined state).

---
