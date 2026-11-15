# Step 8: Present Complete Test Plan to User

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Step 8: Present Complete Test Plan to User
  - Phase 4: Generate Documentation
  - Phase 4 Summary: Files Generated

## Step 8: Present Complete Test Plan to User

After all scenarios are generated, present summary:

```
Test plan generated for [Agent Name] (version [N]):

Total Scenarios: [count]

By Category:
  - Agent Behavior: [count] (includes [N] safety probes)
  - Routing Infrastructure: [count] ([N] core, [N] availability, [N] business hours, [N] edge cases)
  - Business Logic: [count] custom rules

By Priority:
  - P0 (Critical): [count]
  - P1 (High): [count]
  - P2 (Medium): [count]
  - P3 (Low): [count]

Estimated test duration: [guidance based on scenario count]

Configuration Summary:
  - Queues tested: [list]
  - Availability model: [detected model]
  - Business hours: [count] configurations
  - Custom business rules: [count]

Ready to generate documentation? (yes/no)
```

---

### Phase 4: Generate Documentation

For a generated project that will be maintained with agents, copy `templates/AGENTS.md.template` to its root as `AGENTS.md`. Adapt its file list to the chosen output format. The template is output material, not instructions governing the skill library. Do not create a separate CLAUDE.md copy.

**📄 Load Modules:**
- `modules/OUTPUT_FORMATS.md`
- `modules/EXECUTION_SUMMARY.md`

**Step 0: Choose output format and options**

Before generating any files, ask the user their preferred documentation format and options.

**Option 1 - Markdown (.md files):**
- Edit-friendly, version control, works in VS Code/GitHub/any text editor
- Best if you plan to edit docs manually or check into git

**Option 2 - HTML dashboard (test-dashboard.html):**
- Interactive, filterable, pass/fail dropdowns per scenario
- Click-to-copy SOQL queries, live progress bar
- Opens in any browser by double-clicking
- No Python, no server, no internet required
- Best if you want a visual interface during testing

Ask: **"Which format would you like? (1 for Markdown, 2 for HTML)"**

After format selection, ask: **"Would you like to include an execution summary (EXECUTION_SUMMARY.md)? This contains environment details, CLI versions, metadata completeness, and debugging info useful for cross-device comparison. (yes/no)"**

---

**If user chooses 1 (Markdown):** Generate the standard file set below.

**If user chooses 2 (HTML):** Generate ONLY the following files in the output directory:
- `test-dashboard.html` — fully self-contained interactive dashboard (all content + CSS + JS inline, zero external dependencies)
- `queries/` directory — SOQL files (same as markdown path, useful regardless of format)
- `README.md` — lightweight overview with instructions for opening the dashboard
- `AGENTS.md` — only when this output will be maintained with agents; use the template above
- `EXECUTION_SUMMARY.md` — Only if user requested it in Step 0

Do NOT generate the individual `.md` scenario/guide/log files when HTML is chosen — the dashboard replaces them.

**How to generate the HTML dashboard:**

**CRITICAL: You MUST use the template file. DO NOT generate HTML from scratch.**

**Step 1: Read the template file**
```
Read file: templates/test-dashboard.html
```
This template is a complete, self-contained HTML dashboard with all styling, JavaScript, and structure already built. Your job is ONLY to populate the data sections.

**Step 2: Locate the data sections in the template**

The template has THREE main data sections to populate (all are JavaScript variables in the `<script>` tag):

**Section A: SCENARIOS array** - Starts with `var SCENARIOS = [` around line 482
- This is an array of scenario objects
- Each object has: id, priority, category, name, body

**Section B: GUIDE_CONTENT string** - Starts with `var GUIDE_CONTENT = \`# Test Execution Guide` around line 1249
- This is a single multi-line template literal (backtick string)
- Contains markdown-formatted execution instructions

**Section C: REFERENCE_CONTENT string** - Starts with `var REFERENCE_CONTENT = \`# Quick Reference` around line 1360
- This is a single multi-line template literal (backtick string)
- Contains markdown-formatted quick reference

**Step 3: Generate your scenario data in the EXACT format**

Each scenario object MUST match this structure:
```javascript
{
  id: 'S1',                    // String: scenario ID (e.g., 'S1', 'A1', 'R1', 'BUG1')
  priority: 'p0',              // String: 'p0', 'p1', 'p2', or 'p3' (lowercase)
  category: 'safety',          // String: 'safety', 'agent', 'routing', 'hours', 'logic', 'bugs', or 'edge'
  name: 'Safety Probe — ...',  // String: scenario name
  body: `Markdown content`     // String: full scenario content in markdown format
}
```

**CRITICAL formatting rules for scenario.body:**
- Use backticks for the body string (template literal)
- Preserve all markdown formatting (headers, lists, code blocks)
- Escape backticks in SOQL queries: use \\\` instead of \`
- Include all sections: Objective, Preconditions, Test Utterances, Expected Outcome, Verification, Pass Criteria

**Step 4: Build your SCENARIOS array**

Create a complete JavaScript array with ALL your generated scenarios:
```javascript
var SCENARIOS = [
  {
    id: 'S1',
    priority: 'p0',
    category: 'safety',
    name: 'Safety Probe — Escalation Bypass Attempt',
    body: `**Objective:** ...
    
**Preconditions:**
- ...

**Test Utterances:**
- ...

**Expected Outcome:**
- ...`
  },
  {
    id: 'S2',
    // ... next scenario
  }
  // ... all scenarios
];
```

**Step 5: Generate execution guide content**

Build the GUIDE_CONTENT string with these sections (adapt to this specific org):
- Pre-Test Setup (including queue names, agent names, capacity settings for THIS org)
- Setting Agent Presence States
- Triggering Escalations (with THIS org's deployment URL if known)
- Running Verification Queries (with THIS org's alias)
- Business Hours Schedule (with THIS org's actual business hours from Phase 2)
- Debugging Failed Scenarios (with THIS org's specific bugs/issues identified)

Format as a markdown string in backticks with proper escaping.

**Step 6: Generate quick reference content**

Build the REFERENCE_CONTENT string with these sections (org-specific):
- Org details (name, queue names, channel names)
- Execution Order (actual scenario IDs generated)
- Key Verification Queries (with THIS org's queue/channel names)
- Key Config Reference (THIS org's actual values)
- Known Bugs (actual bugs identified in Phase 2)

Format as a markdown string in backticks with proper escaping.

**Step 7: Update metadata in the HTML**

The template contains placeholder data that must be replaced with the actual org and agent data from this test run. Find and update these sections:

**In the topbar section (look for `<div class="topbar">`)**:
- **Title:** Update the agent name in the title
  - Template example: `🧪 Robbie Escalation Agent — Test Dashboard`
  - Replace with: `🧪 [Agent-Name-From-Phase-1] — Test Dashboard`

- **Metadata line:** Update version, status, org name, and generation date
  - Template example: `v2 (Inactive) &nbsp;·&nbsp; storm-52b2c4fd995495 &nbsp;·&nbsp; Generated 2026-05-26`
  - Replace with: `v[version-from-Phase-1] ([status-from-Phase-1]) &nbsp;·&nbsp; [org-name-from-Phase-1] &nbsp;·&nbsp; Generated [today's-date]`

**In the JavaScript section (look for `var STORAGE_KEY`)**:
- **Storage key:** Create a unique key for this agent and version
  - Template example: `var STORAGE_KEY = 'escalation-test-Robbie_Escalation_Agent-v2';`
  - Replace with: `var STORAGE_KEY = 'escalation-test-[Agent_Name_underscored]-v[version]';`
  - Use underscores instead of spaces in agent name

**In the export function (look for `function exportLog()`)**:
- **Export title:** Update agent name and version in the markdown export
  - Template example: `Test Execution Log — Robbie_Escalation_Agent v2`
  - Replace with: `Test Execution Log — [Agent_Name_underscored] v[version]`

- **Org line:** Update org identifier
  - Template example: `**Org:** storm-52b2c4fd995495`
  - Replace with: `**Org:** [org-alias-or-name-from-Phase-1]`

**In the progress section (look for progress bar initialization)**:
- **Initial count displays:** Update the total scenario count
  - Template has hardcoded numbers like `0 / 31 tested` and `31 untested`
  - Replace `31` with `[actual-scenario-count]` (the length of your SCENARIOS array)
  - Note: The JavaScript variable `var total = SCENARIOS.length;` will automatically calculate this at runtime, but the initial HTML display should show the correct count

**All values come from data collected in Phases 0-3:**
- Agent name: from Phase 1 (agent selection)
- Version: from Phase 1 (version selection)
- Status: from Phase 1 (Active/Inactive)
- Org name: from Phase 1 (org display command)
- Date: current date (YYYY-MM-DD format)
- Scenario count: number of scenarios generated in Phase 3

**Step 8: Copy template to output directory (DO THIS FIRST)**

**CRITICAL: Do NOT edit the template file itself. Copy it to the output directory, then edit the copy.**

```bash
cp templates/test-dashboard.html <output-dir>/test-dashboard.html
```

This ensures the template is never modified and the output always starts from the exact template structure.

**Step 9: Edit ONLY the data sections in the copied file**

Use the Edit tool on `<output-dir>/test-dashboard.html` (NOT on `templates/test-dashboard.html`).

**NEVER use the Write tool to recreate the HTML file from scratch. Only Edit the specific sections below.**

Make these edits in order:

1. Find the line starting with `var SCENARIOS = [` and the matching closing `];` 
   - Replace EVERYTHING between (including the array brackets) with your generated SCENARIOS array

2. Find the line starting with `var GUIDE_CONTENT = \`` and the matching closing backtick + `;`
   - Replace the content between the backticks with your GUIDE_CONTENT

3. Find the line starting with `var REFERENCE_CONTENT = \`` and the matching closing backtick + `;`
   - Replace the content between the backticks with your REFERENCE_CONTENT

4. Apply the metadata updates from Step 7 (topbar title, topbar meta line, STORAGE_KEY, exportLog title/org, progress count)

All edits use the Edit tool on the output file. The Write tool is never used for the HTML file.

**Step 10: Verification checklist**

After writing, verify:
- [ ] File size is substantial (should be 60-80KB, not 20-30KB)
- [ ] Contains the sidebar HTML structure (`<div class="sidebar">`)
- [ ] Contains three page divs: `page-scenarios`, `page-guide`, `page-reference`
- [ ] SCENARIOS array has all your scenarios
- [ ] GUIDE_CONTENT is populated (not empty)
- [ ] REFERENCE_CONTENT is populated (not empty)
- [ ] All metadata updated with org-specific values

**If any of these checks fail, DO NOT PROCEED. Re-read the template and try again.**

**HTML dashboard requirements (MUST follow for safety and compatibility):**
- Zero external resources — no CDN links, no Google Fonts, no remote scripts or stylesheets
- No fetch or XMLHttpRequest calls — all content embedded as JS variables at generation time
- Avoid dynamic code execution — use textContent and DOM methods for safety
- Works from file:// URLs — double-click to open, no local server needed
- All interactivity via plain JavaScript — no frameworks (no React, no Vue, no jQuery)
- localStorage for pass/fail persistence — keys namespaced to agent name + version to avoid collisions across test runs
- Clipboard API for copy-to-clipboard with silent fallback (no alerts)
- Export button generates a downloadable TEST_LOG.md from current localStorage state

**HTML dashboard structure:**
1. Header — agent name, version, org, generated date, progress bar (live from localStorage)
2. Filter bar — priority buttons (All/P0/P1/P2/P3), category buttons, real-time search box
3. Scenario cards — one per scenario, collapsed by default, click to expand
   - Each card shows: ID, name, priority badge (color-coded), category, status dropdown
   - Expanded view shows: full scenario body with SOQL copy buttons
   - Status dropdown options: Untested / Pass / Fail / Blocked / Needs Review
   - Status saves to localStorage on change, card border updates to reflect status
4. Side panel tabs — Execution Guide, Quick Reference (rendered from embedded content)
5. Export button — downloads filled TEST_LOG.md based on current localStorage state

---

**For Markdown format (option 1):**

Create the following files in a new project directory named: `escalation-test-[agent-name]-[date]`

Use the templates from OUTPUT_FORMATS.md to generate:

1. **TEST_SCENARIOS.md** — Consolidated file containing ALL test scenarios
2. **QUICK_REFERENCE.md** — One-page quick lookup for rapid testing
3. **TEST_EXECUTION_GUIDE.md** — Comprehensive step-by-step instructions
4. **queries/** directory — Pre-built SOQL files for verification
5. **results/TEST_LOG.md** — Test execution log template
6. **README.md** — Project overview and quick start
7. **AGENTS.md** — When maintained with agents, copied and adapted from `templates/AGENTS.md.template`
7. **EXECUTION_SUMMARY.md** — Only if user requested it in Step 0

Follow the exact structure and format from OUTPUT_FORMATS.md for each file.

If execution summary is included, use the template from EXECUTION_SUMMARY.md module to generate it with all data collected during Phases 0-4.

---

### Phase 4 Summary: Files Generated

**If Markdown format chosen:**

```
Documentation generated:
  📁 escalation-test-[agent-name]-[date]/
     📄 README.md
     📄 TEST_SCENARIOS.md ([N] scenarios)
     📄 QUICK_REFERENCE.md
     📄 TEST_EXECUTION_GUIDE.md
     [📄 EXECUTION_SUMMARY.md (if requested)]
     📁 queries/ ([N] SOQL files)
        📄 check-agent-presence.soql
        📄 verify-routing.soql
        📄 check-session-status.soql
        [... availability-model-specific queries ...]
        [... business-hours-specific queries ...]
        [... custom-business-logic queries ...]
     📁 results/
        📄 TEST_LOG.md (template)

Next Steps:
1. Review TEST_SCENARIOS.md to understand all test cases
2. Read TEST_EXECUTION_GUIDE.md for detailed instructions
[3. Check EXECUTION_SUMMARY.md for environment details (if generated)]
[N]. Start with P0 scenarios (smoke test: R1, R2, S1)
[N]. Log results in results/TEST_LOG.md

Ready to start testing!
```

**If HTML format chosen:**

```
Documentation generated:
  📁 escalation-test-[agent-name]-[date]/
     📄 README.md (instructions for opening dashboard)
     📄 test-dashboard.html (interactive dashboard, [N] scenarios)
     [📄 EXECUTION_SUMMARY.md (if requested)]
     📁 queries/ ([N] SOQL files)
        📄 check-agent-presence.soql
        📄 verify-routing.soql
        📄 check-session-status.soql
        [... availability-model-specific queries ...]
        [... business-hours-specific queries ...]
        [... custom-business-logic queries ...]

Next Steps:
1. Double-click test-dashboard.html to open in your browser
2. Review all scenarios in the interactive dashboard
3. Use filters (priority, category, search) to focus testing
4. Mark pass/fail for each scenario (auto-saves to browser storage)
5. Export TEST_LOG.md when testing is complete
[6. Check EXECUTION_SUMMARY.md for environment details (if generated)]

Ready to start testing!
```

---
