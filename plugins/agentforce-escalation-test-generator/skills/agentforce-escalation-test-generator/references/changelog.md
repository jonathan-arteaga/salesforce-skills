# Recent Updates

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Recent Updates

**🆕 Version 6.1 - Fresh Start:**
- Renamed to `agentforce-escalation-test-generator` for clearer value communication
- Removed draft version support (requires published versions only)
- Streamlined for sharing and wider adoption

**Version 6.0 - Output Consistency & Session Management:**
- Enforced template-based HTML dashboard generation (prevents output drift)
- Required persona selection prompt (prevents silent skipping in long sessions)
- Module unload hints to reduce context rot across phases
- Copy-then-Edit pattern for HTML output (Write tool prohibited for dashboard)

**Version 5.0 - Cross-Device Consistency & HTML Dashboard:**
- Pre-flight validation catches environment issues before execution
- Version-aware agent retrieval with fallback chain for CLI regressions
- Recursive subflow dependency resolution for complete metadata
- Optional execution summaries for cross-device comparison and debugging
- HTML dashboard option for interactive test execution
- Built on v4.0's modular architecture (73% token reduction from v3.0)

**Full-Stack Coverage:** This skill generates scenarios for the complete escalation lifecycle:
- **Agent Behavior** — decision-making, topic routing, escalation triggers, safety validation
- **Routing Infrastructure** — Omni-Channel, Service Channel capacity, queue presence, business hours
- **Business Logic** — customer tier routing, SLA enforcement, compliance requirements, custom rules
- **Integration Points** — external systems, Case creation, platform events

**Agent-Derived Test Cases:** Scenarios are derived from your agent's actual structure (escalation subagents, connection blocks, gating variables) rather than hardcoded assumptions. This ensures test cases match your agent's real routing logic.

**Scalability:** Automatically detects your org's availability model (Service Channel-based, queue presence only, both, or custom Flow/Apex logic) and generates scenarios specific to your setup.

**When to Use This Skill:**
- **Development iteration** — validate agent logic changes, verify new escalation paths
- **Pre-release testing** — comprehensive validation before deploying to production
- **Compliance audits** — document routing behavior for business logic and SLA requirements
- **Regression testing** — quarterly validation after Salesforce releases or org configuration changes
- **Troubleshooting** — diagnose escalation failures with targeted scenario reproduction

---

## Version 4.0 Improvements

**Modular Architecture:**
- Main skill file: ~8k tokens (down from ~30k)
- Modules loaded on-demand per phase
- Total token savings: ~73% reduction in initial context consumption

**Module Files:**
- `SOQL_QUERIES.md` — All Phase 2 queries (enhanced with subflow dependency resolution)
- `BUSINESS_LOGIC_EXAMPLES.md` — Requirements gathering guidance
- `TEST_TEMPLATES.md` — All test scenario templates
- `SAFETY_PROBES.md` — Security testing scenarios
- `EXECUTION_SUMMARY.md` — Optional execution tracking and cross-device comparison support
- `OUTPUT_FORMATS.md` — Documentation templates

**Benefits:**
- More context available for org metadata
- Longer conversation history retained
- Reduced risk of context window exhaustion
- Easier to maintain and update individual modules
- Same comprehensive test coverage as v3.0

---

## Migration from v3.0

If you have existing test plans generated with v3.0:
- Test scenarios and coverage are identical
- Only the internal skill structure changed
- No need to regenerate unless org config changed
- Can continue using existing test plans

---
