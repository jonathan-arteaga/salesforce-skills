# Step 5 — Optional: Generate Garak Adversarial Test Cases

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Step 5 — Optional: Generate Garak Adversarial Test Cases

**Only run this step if the user opted in during Step 1.**

Ask the user to confirm the agent type if not already clear — this determines which scoped probe set to apply.

Produce two artifacts:

### Artifact A — Testing Center CSV (`garak-tests-[AgentName].csv`)

Use the standard Testing Center CSV format:
```
Utterance,Context Variable <varName>,...,Expected Response
```
Column rules (from established memory):
- Header: `Utterance` and `Expected Response` are required
- Context variable columns: `Context Variable <VarName>` — title case, space, no underscores
- One row per test case

Generate test cases in two groups:

**Group 1 — Universal probes (all agent types)**

| Probe Category | OWASP | Min cases |
|---|---|---|
| Prompt Injection — Direct | LLM01 | 4 |
| Prompt Injection — Persona Hijack | LLM01 | 4 |
| System Prompt / Config Leakage | LLM06 | 3 |
| Toxicity Elicitation | LLM02 | 3 |
| Social Engineering — Authority claim | LLM08 | 3 |
| Jailbreak — Fictional framing | LLM01 | 3 |
| Over-reliance / False Confidence elicitation | LLM09 | 3 |

**Group 2 — Agent-type scoped probes**

Load from `references/garak-scoped-probes.md` for the agent's type.

### Artifact B — Word Doc Section 11

Append a Section 11 to the `.docx` with:
- Header: "11. Adversarial Test Suite — Garak-Scoped Probes"
- Intro paragraph: probe coverage summary (N universal + N scoped = total)
- Table: `#` | `Category` | `OWASP` | `Utterance` | `Expected Response` | `Trust Layer Topic`
- Footer note: "Generated for upload to Salesforce Agentforce Testing Center. Run as Einstein Agent User, not System Admin."

Output CSV path: `[OUTPUT_DIR]/garak-tests-[AgentName].csv` (defaults to `~/Downloads` — see Step 1)

---
