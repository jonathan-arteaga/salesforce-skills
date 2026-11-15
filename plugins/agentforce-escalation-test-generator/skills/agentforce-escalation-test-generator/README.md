# Agentforce Escalation Testing Skill

A Codex skill for generating comprehensive test scenarios for Agentforce agent escalation and fallback logic. This skill produces detailed, metadata-driven test plans designed for manual execution by humans.

## Overview

This skill helps teams create thorough test plans for Agentforce agent behavior under realistic escalation scenarios:

- **No agents available** — Does fallback logic execute correctly?
- **Agents at capacity** — Does overflow routing work?
- **Business hours boundaries** — Are off-hours requests handled properly?
- **Concurrent requests** — Does routing scale under load?
- **External integrations** — Do third-party systems get notified?

All test scenarios are **metadata-driven**, **org-specific**, and designed for **manual execution**.

## Features

✅ **Metadata-first** — Scenarios derived from your org's actual routing configuration  
✅ **No browser automation** — Test plans include SOQL queries and manual steps  
✅ **Security-first** — Never commits credentials, blocks production orgs  
✅ **Availability-method-aware** — Adapts to Flow, Apex, or native Omni-Channel  
✅ **Comprehensive edge cases** — 20-30 scenarios including common and edge cases  
✅ **Team-ready** — Designed for sharing across development teams  
✅ **Manual execution guides** — Step-by-step instructions for human testers

## Installation

Install the personal Salesforce plugin in Codex.

## Usage

In any Codex conversation:

```
$agentforce-escalation-test-generator
```

or describe your need:

```
I want to generate test scenarios for my Agentforce agent's escalation behavior
```

The skill will:
1. Fetch routing metadata from your org
2. Guide you through configuration questions
3. Generate 20-30 comprehensive test scenarios
4. Create detailed documentation for manual execution
5. Provide verification queries and pass/fail criteria

See [USAGE.md](SKILL.md) for detailed examples.

## Test Scenario Categories

The skill generates scenarios across multiple categories:

| Category | Examples | When Applicable |
|----------|----------|-----------------|
| **Core Scenarios** | Agents available, No agents available, Status lifecycle | Always |
| **Availability Method** | Flow-based checks, Apex-based checks, Native presence | Based on org config |
| **Edge Cases** | Capacity overflow, Empty queues, Nested groups | Based on org config |
| **Business Hours** | Inside hours, Outside hours, Timezone boundaries | If BusinessHours configured |
| **Skills Routing** | Skills match, Skills mismatch | If skills configured |
| **Concurrency** | Multiple simultaneous escalations | Always |
| **Integration** | External callouts, Platform events | If applicable |
| **Channel-Specific** | Messaging, Chat, Voice | Based on channels found |

## Generated Documentation

When the skill completes, you'll have:

```
escalation-testing-<agent-name>/
├── README.md                      # Overview of the test plan
├── TEST_SCENARIOS_DETAILED.md     # 20-30 detailed scenarios with steps
├── QUICK_REFERENCE.md             # One-page summary table
├── EDGE_CASES.md                  # Edge case scenarios explained
├── MANUAL_TEST_GUIDE.md           # How to execute tests manually
├── .env.example                   # Org configuration template
├── queries/                       # Pre-built SOQL queries
│   ├── check-agent-presence.soql
│   ├── verify-routing.soql
│   ├── check-session-status.soql
│   ├── verify-no-cases.soql
│   └── check-capacity.soql
└── results/
    └── test-log-template.md       # Fill this out as you test
```

## Security

This skill follows strict security practices:

- **Never commits credentials** — `.env` is git-ignored
- **Production org protection** — Blocks execution against production orgs
- **Read-only metadata access** — Only queries org configuration
- **No destructive operations** — Generates documentation only
- **Human execution** — All tests require manual human involvement

## Prerequisites

- **Salesforce CLI** (`sf` command) installed and authenticated
- **Non-production org** with Agentforce + Omni-Channel configured
- **User permissions** — Omni-Channel Supervisor or equivalent

## What Makes This Different

This skill focuses on **generating comprehensive test plans**, not executing them:

- ✅ Creates 20-30 scenarios tailored to your org
- ✅ Includes edge cases based on your configuration
- ✅ Provides verification queries for each scenario
- ✅ Gives step-by-step manual execution instructions
- ✅ Generates pass/fail criteria
- ✅ Includes troubleshooting guidance

Why manual execution?
- Setting agent presence requires UI interaction
- Triggering escalations may need conversational context
- Verifying fallback messages requires human judgment
- Edge case timing requires manual state manipulation

## Example Workflow

### 1. Generate Test Plan

```bash
# In Codex
$agentforce-escalation-test-generator
```

Provide your org alias and answer configuration questions.

### 2. Review Generated Scenarios

```bash
cd escalation-testing-your-agent
cat TEST_SCENARIOS_DETAILED.md
```

### 3. Execute Tests Manually

Follow the instructions in `MANUAL_TEST_GUIDE.md`:
1. Set agent presence states using Omni-Channel widget
2. Trigger escalations in your messaging channel
3. Run verification queries to check results
4. Record outcomes in `results/test-log-template.md`

### 4. Track Results

```bash
# Fill out the test log as you test
nano results/test-log-template.md

# Review your results
cat results/test-log-template.md
```

## Team Workflow

### Daily Testing
Review and execute 2-3 core scenarios after each deployment.

### Pre-Release Validation
Execute all generated scenarios before releasing to production.

### Regression Tracking
Keep `test-log-template.md` in version control to track test history over time.

## Customization

The generated test plan can be customized:

- **Add scenarios** — Edit `TEST_SCENARIOS_DETAILED.md` to add custom scenarios
- **Modify acceptance criteria** — Update expected outcomes for your use case
- **Add queries** — Create additional `.soql` files in the `queries/` directory
- **Customize test data** — Update `.env.example` with your org-specific values

## Troubleshooting

### Skill doesn't appear in Codex
- Run `bash verify-install.sh` from the installed skill package
- Restart Codex

### SF CLI authentication errors
```bash
sf org login web --alias your-sandbox
```

### No metadata found
- Verify Agentforce and Omni-Channel are configured in your org
- Ensure your user has Omni-Channel Supervisor permissions
- Check API access is enabled

### Tests fail with "production org" error
This is intentional! The skill blocks production orgs. Use a sandbox or scratch org.

## Contributing

To improve this skill:

1. **Add new scenario types** — Edit `SKILL.md` with new edge cases
2. **Enhance metadata discovery** — Add queries to Phase 1
3. **Improve documentation templates** — Update Phase 4 generation logic
4. **Add acceptance criteria options** — Expand Phase 2 questions

## Support

For issues or questions:

1. Check [USAGE.md](SKILL.md) for detailed examples
2. Review [QUICKSTART.md](SKILL.md) for fast onboarding
3. Check SF CLI authentication: `sf org display`
4. Review the error output in Codex.

## License

This skill is provided as-is for internal team use. Adapt and customize as needed.

---

**Built for Codex** — Designed for teams building Agentforce agents at scale.
