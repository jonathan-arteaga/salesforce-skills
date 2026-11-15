# Phase 0: Pre-Flight Environment Validation

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Phase 0: Pre-Flight Environment Validation

Before starting metadata retrieval, validate the execution environment to prevent common issues that cause execution inconsistencies across different machines.

**Step 1: Check Working Directory**

Verify an SFDX project exists in the current directory:

```bash
ls sfdx-project.json
```

**If NOT found:**

```
❌ No sfdx-project.json found in current directory: $(pwd)

This skill requires an SFDX project. You have two options:

Option 1: Navigate to existing SFDX project
  cd /path/to/your/sfdx-project
  
Option 2: Create new SFDX project for testing
  sf project generate --name escalation-testing
  cd escalation-testing

After completing one of these options, re-run the skill.
```

**DO NOT proceed until user confirms they are in an SFDX project directory.**

**Step 2: Check SF CLI Version**

Check the installed SF CLI version and warn about known issues:

```bash
sf --version
```

Extract the version number and display:

```
✅ SF CLI Version: <version>
```

**Known Issues:**
- **SF CLI 2.134.x - 2.135.x:** May have AiAuthoringBundle retrieval regression. Agent file retrieval may fail with "Entity type 'AiAuthoringBundle' is not available in this api version" error.
- **SF CLI 2.133.4:** Confirmed working for AiAuthoringBundle retrieval.

**If version is 2.134.x or 2.135.x, display warning:**

```
⚠️  WARNING: You are using SF CLI version <version>.

Known issue: AiAuthoringBundle retrieval may fail with this CLI version due to a known regression.

If retrieval fails during execution, the skill will offer these fallbacks:
  1. Use local agent file if available
  2. Downgrade CLI to 2.133.4: npm install -g @salesforce/cli@2.133.4
  3. Continue with metadata-only scenario generation (reduced coverage)

Do you want to proceed with this CLI version? (yes/no)
```

**Step 3: Verify Node.js Version (Informational)**

```bash
node --version
```

Display for reference in execution logs:
```
ℹ️  Node.js Version: <version>
```

**Step 4: Display Pre-Flight Summary**

```
✅ Pre-Flight Check Complete

  Working Directory: $(pwd)
  SFDX Project: ✅ Found
  SF CLI Version: <version>
  Node.js Version: <version>
  
Ready to proceed? (yes/no)
```

**If user confirms "yes", proceed to Phase 1. If "no", exit skill.**

---
