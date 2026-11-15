# Execution Summary Generation Module

This module defines the execution summary that should be generated at the end of every skill run. The summary enables users to compare executions across different devices, CLI versions, and environments, and diagnose inconsistencies.

## Purpose

Generate a comprehensive execution summary documenting:
- Environment configuration (CLI version, Node.js, API versions)
- Working directory and project setup
- Retrieval successes and failures
- Metadata completeness
- Workarounds applied
- Scenario counts by category
- Warnings encountered
- Total execution time

## When to Generate

**At the end of Phase 4** (after all test scenarios and documentation generated), create `EXECUTION_SUMMARY.md` in the output directory.

---

## Summary Template

```markdown
# Execution Summary

**Generated:** <timestamp>  
**Skill Version:** agentforce-escalation-test-generator v6.1  
**Agent:** <agent-name> (<version>)  
**Target Org:** <org-alias> (<org-id>)

---

## Environment

| Component | Value | Notes |
|-----------|-------|-------|
| **SF CLI Version** | <version> | <"Known working" / "Known issues" / "Untested"> |
| **Node.js Version** | <version> | |
| **Org API Version** | <version> | |
| **API Version Override** | <version / None> | <If present: "Unset during execution" / "Left in place"> |
| **Working Directory** | <path> | |
| **sfdx-project.json** | <Found / Created> | <If created: when in execution> |
| **Execution Duration** | <MM:SS> | From Phase 0 to Phase 4 completion |

---

## Pre-Flight Validation

| Check | Status | Details |
|-------|--------|---------|
| **SFDX Project** | ✅ / ❌ | <Found immediately / Created during Phase 0 / Was missing, user corrected> |
| **CLI Version Check** | ✅ / ⚠️ | <No issues / Warning displayed for 2.134.x-2.135.x> |
| **API Override Check** | ✅ / ⚠️ | <None found / Override detected and <unset / left in place>> |
| **Node.js Check** | ✅ | Version <version> |

---

## Phase 1: Agent Selection

| Item | Value |
|------|-------|
| **Org Selected** | <org-alias> |
| **Org Type** | <Sandbox / Production> |
| **Org Username** | <username> |
| **Org ID** | <org-id> |
| **Org Instance** | <instance-url> |
| **Agent Selected** | <agent-name> |
| **Agent Version** | <version> (<Active / Inactive>) |
| **Agent File Path** | <path> |
| **Retrieval Method** | <Standard / Local File Fallback / Metadata-Only> |

---

## Phase 1: Agent Retrieval Details

### Retrieval Attempts

**Attempt 1: Standard AiAuthoringBundle Retrieval**
```bash
sf project retrieve start --metadata "AiAuthoringBundle:<agent-api-name>[_<version>]" -o <org-alias>
```
**Result:** <✅ SUCCESS / ❌ FAILED>

<If failed:>
**Error Message:**
```
<full error message>
```

**Attempt 2: Local File Fallback**
- **Local files found:** <count> file(s)
- **File selected:** <path>
- **File copied to:** <destination>
- **Result:** <✅ SUCCESS / ❌ NO FILES FOUND>

<If metadata-only:>
**Attempt 3: Metadata-Only Generation**
- **User selected:** Metadata-only scenario generation
- **Coverage:** ~60% (routing metadata only, no agent-specific scenarios)

### Final Agent File Status

**Agent file used:** <path>  
**File size:** <size>  
**Source:** <Org retrieval / Local file / N/A (metadata-only)>  
**Validation:** <✅ Valid / ❌ Empty/Corrupted>

---

## Phase 2: Metadata Retrieval

### Connection Blocks Parsed

| Channel | Route Type | Route Target | Found in Org |
|---------|------------|--------------|--------------|
| <channel> | <type> | <target> | <✅ / ❌> |
| <channel> | <type> | <target> | <✅ / ❌> |

### Routing Targets Retrieved

**Flows:**
| Flow API Name | Status | Subflows Discovered | Subflows Retrieved |
|---------------|--------|---------------------|-------------------|
| <FlowName> | ✅ Retrieved | <count> | <count> / <total> |
| <FlowName> | ❌ Failed | N/A | N/A |

**Flow Dependency Tree:**
```
<Main_Flow> (main)
  └─ <Subflow_1> (subflow) ✅
     └─ <Subflow_2> (subflow) ✅
        └─ (no further dependencies)

Total flows retrieved: <count>
```

**Queues:**
| Queue Name | Queue ID | Routing Config | Service Channel | Business Hours |
|------------|----------|----------------|-----------------|----------------|
| <name> | <id> | <✅ / ❌> | <channel-name / ❌> | <hours-name / ❌> |

**Apex Classes:**
| Class Name | Retrieved | Business Logic Extracted |
|------------|-----------|-------------------------|
| <name> | <✅ / ❌> | <Summary> |

### Metadata Completeness

| Metadata Type | Requested | Retrieved | Success Rate |
|---------------|-----------|-----------|--------------|
| Agent File | 1 | <1 / 0> | <100% / 0%> |
| Flows (main) | <count> | <count> | <percentage> |
| Flows (subflows) | <count> | <count> | <percentage> |
| Queues | <count> | <count> | <percentage> |
| Routing Configs | <count> | <count> | <percentage> |
| Service Channels | <count> | <count> | <percentage> |
| Business Hours | <count> | <count> | <percentage> |
| Apex Classes | <count> | <count> | <percentage> |

**Overall Metadata Completeness:** <percentage>

---

## Phase 2: Graceful Degradation

### Unsupported Fields/Objects

| Field/Object | Status | Workaround Applied |
|--------------|--------|--------------------|
| <field> | ❌ Not available | <workaround description> |

### Warnings Issued

1. <Warning message>
2. <Warning message>

---

## Phase 3: Scenario Generation

### Scenario Counts by Category

| Category | Count | Coverage |
|----------|-------|----------|
| **Agent Behavior** | | |
| - User-requested escalation | <count> | <complete / partial> |
| - Agent-initiated escalation | <count> | <complete / partial> |
| - Pre-escalation context gathering | <count> | <complete / partial> |
| - Verification-gated escalation | <count> | <complete / partial> |
| - Cancel/abort paths | <count> | <complete / partial> |
| - Safety probes | 6 | ✅ Complete |
| **Routing Infrastructure** | | |
| - Queue routing (agents available) | <count> | <complete / partial> |
| - Service Channel capacity | <count> | <complete / partial> |
| - Queue presence validation | <count> | <complete / partial> |
| - Flow/Apex availability logic | <count> | <complete / partial> |
| - Fallback behavior | <count> | <complete / partial> |
| - Business hours boundary | <count> | <complete / partial / skipped> |
| - Edge cases | <count> | <complete / partial> |
| **Business Logic** | | |
| - Customer tier routing | <count> | <user-defined / skipped> |
| - SLA enforcement | <count> | <user-defined / skipped> |
| - Compliance routing | <count> | <user-defined / skipped> |
| - Custom requirements | <count> | <user-defined / skipped> |

**Total Scenarios Generated:** <count>

### Coverage Assessment

**Full Coverage (Agent + Routing + Business Logic):** <✅ / ⚠️ Partial / ❌ Metadata-Only>

**Missing Coverage:**
- <Description of missing scenarios and why>
- <Description of missing scenarios and why>

---

## Phase 4: Output Files

| File | Generated | Size | Purpose |
|------|-----------|------|---------|
| TEST_SCENARIOS.md | ✅ | <size> | Complete test scenario list |
| TEST_EXECUTION_GUIDE.md | ✅ | <size> | Step-by-step execution instructions |
| QUICK_REFERENCE.md | ✅ | <size> | Quick lookup guide |
| README.md | ✅ | <size> | Overview and getting started |
| queries/*.soql | ✅ (<count> files) | <total size> | SOQL queries for manual execution |
| results/TEST_LOG.md | ✅ | <size> | Empty log template |
| EXECUTION_SUMMARY.md | ✅ | <size> | This file |

---

## Workarounds Applied

### During Execution

1. **<Workaround name>**
   - **Issue:** <Description>
   - **Solution:** <What was done>
   - **Impact:** <Effect on test coverage or execution>

2. **<Workaround name>**
   - **Issue:** <Description>
   - **Solution:** <What was done>
   - **Impact:** <Effect on test coverage or execution>

---

## Recommendations for Future Runs

### Environment Setup

<If CLI version had issues:>
- ⚠️ **CLI Version:** Consider downgrading to 2.133.4 for more reliable AiAuthoringBundle retrieval
- Command: `npm install -g @salesforce/cli@2.133.4`

<If API override was present:>
- ⚠️ **API Override:** Ensure `org-api-version` is not set before running skill
- Command: `sf config unset org-api-version --global`

<If working directory was created mid-run:>
- ✅ **Project Setup:** Start in existing SFDX project or create one before running skill
- Command: `sf project generate --name escalation-testing && cd escalation-testing`

### Metadata Completeness

<If subflows were missing:>
- ⚠️ **Subflow Dependencies:** Ensure all subflows are retrieved recursively
- This execution <retrieved / did not retrieve> subflows automatically

<If business hours were missing:>
- ℹ️ **Business Hours:** If business hours testing is required, configure BusinessHours records in org

### Comparison with Other Runs

**To compare this execution with another:**
1. Compare "Total Scenarios Generated" counts
2. Check "Metadata Completeness" percentages
3. Review "Workarounds Applied" sections
4. Compare "Agent Retrieval Details" (retrieval method used)
5. Check "Flow Dependency Tree" (are subflows included?)

**Key Metrics for Comparison:**
- Metadata completeness: <percentage>
- Total scenarios: <count>
- Agent retrieval method: <Standard / Local / Metadata-only>
- Subflows retrieved: <count>
- Workarounds applied: <count>

---

## Skill Performance

**Execution Timeline:**
- Phase 0 (Pre-Flight): <duration>
- Phase 1 (Agent Selection & Retrieval): <duration>
- Phase 2 (Metadata Retrieval): <duration>
- Phase 2b (Requirements Gathering): <duration>
- Phase 3 (Scenario Generation): <duration>
- Phase 4 (Output Files): <duration>

**Total Duration:** <MM:SS>

**Bottlenecks:**
<If any phase took unusually long, list it and potential causes>

---

## Skill Version Information

**Skill:** agentforce-escalation-test-generator  
**Version:** 6.1  
**Modular Architecture:** ✅ Enabled  
**Modules Loaded:**
- SOQL_QUERIES.md
- BUSINESS_LOGIC_EXAMPLES.md
- SAFETY_PROBES.md
- GRACEFUL_DEGRADATION.md
- TEST_TEMPLATES.md
- OUTPUT_FORMATS.md
- EXECUTION_SUMMARY.md (this module)

---

## Support Information

**For issues or questions:**
- Skill documentation: See PACKAGE_README.md, QUICKSTART.md, USAGE.md
- Known issues: See CHANGELOG-v4.md
- CLI version issues: Check SF CLI release notes

**To compare executions:**
- Share this EXECUTION_SUMMARY.md file with other users running the skill
- Use comparison metrics in "Recommendations for Future Runs" section

---

**End of Execution Summary**
```

---

## Implementation Notes

### When to Capture Data

**Phase 0:**
- Capture SF CLI version, Node version, API override status
- Record working directory, sfdx-project.json status
- Start execution timer

**Phase 1:**
- Record org selection details
- Capture all retrieval attempts and their results
- Note which retrieval method succeeded (standard / local fallback / metadata-only)

**Phase 2:**
- Track all metadata queries and retrieval commands
- Record successes and failures
- Note subflow discovery and retrieval
- Document graceful degradation workarounds

**Phase 3:**
- Count scenarios by category as they're generated
- Note any skipped categories and reasons

**Phase 4:**
- List all output files generated
- Stop execution timer
- Generate this summary

### Data Storage During Execution

Store execution data in variables throughout the skill run:

```bash
# Example tracking variables
EXEC_START_TIME=$(date +%s)
CLI_VERSION=$(sf --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
API_OVERRIDE=$(sf config list | grep org-api-version || echo "None")
RETRIEVAL_METHOD="Standard"  # Updated if fallback used
FLOWS_RETRIEVED=()
SUBFLOWS_RETRIEVED=()
WORKAROUNDS_APPLIED=()
SCENARIO_COUNTS=()
```

### Template Population

At the end of Phase 4, populate the template with collected data and write to `EXECUTION_SUMMARY.md`.

---

## Benefits of Execution Summary

1. **Debugging:** Quickly identify environment differences causing execution variations
2. **Comparison:** Compare two executions side-by-side to diagnose inconsistencies
3. **Documentation:** Record what was tested and how for audit trails
4. **Reproducibility:** Provide all information needed to reproduce the execution
5. **Troubleshooting:** Help users identify and fix configuration issues

This summary was instrumental in identifying the CLI regression between Ana's and Robbie's executions during cross-device testing.
