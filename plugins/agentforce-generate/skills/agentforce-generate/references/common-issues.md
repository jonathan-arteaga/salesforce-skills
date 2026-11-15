# Common Issues Quick Reference

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Common Issues Quick Reference

**`Internal Error, try again later` during publish:**
Server-side compile failure. The 500 doesn't tell you which check failed — walk all four causes in order before asking the user what's wrong. Do NOT stop at cause 1.

1. **Agent type mismatch on `access.default_agent_user`.** Employee agents normally omit `access.default_agent_user`; service agents MUST have it (and the user must hold an Einstein Agent license). See [Design & Agent Spec](agent-design-and-spec-creation.md), Section 3. Re-run the query — do not invent the username.
2. **Action definition missing `outputs:` block.** If any action has `target:` and `inputs:` but no `outputs:`, the server-side compiler can't generate return bindings. CLI `validate` and LSP both PASS — only publish fails. See [Known Issues](known-issues.md), Issue 15.
3. **Other structural drift in the `.agent` file.** Diff against a known-good bundle in the same org:
   `sf project retrieve start --metadata "AiAuthoringBundle:<known-working-agent>" --output-dir /tmp/diff-bundle --json`
   Compare keyword-by-keyword. Look for missing required-but-undocumented fields, block-ordering drift, or DSL keywords your bundle uses that aren't in the working one.
4. **Genuine transient backend error.** If 1–3 are clean and the response `requestId` differs across retries, wait 60 s and retry once.

**`Unable to access Salesforce Agent APIs...` during preview:**
`default_agent_user` lacks permissions. See [Agent User Setup & Permissions](agent-user-setup.md). Do NOT publish as fix — `--use-live-actions` does not require published agent.

**Permission error referencing different username than configured:**
Same fix as above — error references org's default running user, but root cause is Einstein Agent User permissions.

**Agent fails with permission error even though current subagent's actions work:**
Planner validates ALL actions across ALL subagents at startup. One missing permission fails entire agent.

**Apex action returns empty results in live preview but works in simulated:**
`WITH USER_MODE` enforces object and field permissions; access violations can raise query exceptions. Zero rows can instead reflect record sharing, filters, or absent data. Inspect the actual error and action result before diagnosing. See [Agent User Setup & Permissions](agent-user-setup.md), Section 6.2.

**Agent published, ADL indexed (`retrieverId` populated), but every grounded question returns empty `knowledgeSummary` / "I don't have that information":**
The Einstein Agent User lacks Data Cloud access. Two things to check, in order:
1. **Permset/PSL not assigned.** Run the verification queries from [Agent User Setup, Step 3b.3](agent-user-setup.md). If no Data Cloud permset/PSL appears, run the discovery-then-assign procedure (priority: `GenieDataPlatformStarterPsl` PSL → `GenieUserEnhancedSecurity` PS → `DataCloudUser` PS → `DataCloudArchitect` PS).
2. **Data Space scope not granted on the permset.** Currently no API. Setup → Permission Sets → click the assigned permset → "Data Cloud Data Space Management" under Apps → Edit → add the ADL's data space (usually `default`) → Save. See [Agent User Setup, Step 3b.4](agent-user-setup.md).
