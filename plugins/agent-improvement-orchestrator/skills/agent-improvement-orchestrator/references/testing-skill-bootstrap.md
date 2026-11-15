# Testing Skill Bootstrap

Triggered when pre-flight check #3 fails (no testing skill found). Loaded on demand from
`Phase: Pre-Flight Checks → Check 3` — the common case is that a testing skill already exists, so
this flow only runs the first time an agent is onboarded.

This is an interactive, conversational flow. Walk the user through creating a testing skill:

## Step 1: Confirm Org and Agent

```
"I'll help you create a testing skill for $AGENT_NAME on org $ORG_USERNAME. First, let me read the agent's configuration to understand what it does."
```

## Step 2: Read Agent Configuration

```bash
sf project retrieve start -m AIAuthoringBundle:$AGENT_NAME -o $ORG_USERNAME --json
```

Read the agent file and summarize:
- Agent description and role
- Topics it handles
- Actions available
- Key instructions and guardrails

Present summary to user.

## Step 3: Persona Development

Ask the user conversationally:

> "Now let's build your test personas. What are you most worried about with this agent? What scenarios do you want to make sure it handles well?"

Guide through these areas (don't ask all at once):
1. **Happy path** — common questions it should answer well
2. **Edge cases** — tricky scenarios, overlapping topics
3. **Clarification** — when should it ask vs answer directly
4. **Guardrails** — what should it refuse
5. **Context retention** — session continuity across turns
6. **Adversarial** — prompt injection, jailbreak
7. **Error recovery** — known problem scenarios
8. **Escalation** — when to hand off to human

Synthesize responses into structured personas with:
- Name and description
- 5-10 test questions with expected behaviors
- Evaluation criteria (PASS vs FAIL)

Iterate with user until they're satisfied.

## Step 4: Generate Testing Skill

Create `.agents/skills/<agent-name>-testing/SKILL.md` with:
- Configuration (org, bundle, mode)
- `sf agent preview` usage instructions (start/send/end)
- All personas as tables
- Parallel execution instructions (3 sub-agent streams)
- Evaluation table format
- `test-results.json` schema

Also create:
- `personas.md` — full persona definitions
- `test-results.json` — empty template

## Step 5: Offer First Run

> "Your testing skill is ready! Want to run the tests now to establish a baseline?"

If yes, delegate to the testing skill immediately.

After bootstrap completes, save `TESTING_SKILL_PATH` and `TESTING_SKILL_DIR` (its containing directory), then continue pre-flight from check #4.
