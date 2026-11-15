---
id: E007
name: action-schema-drift
match:
  regex: "property [^ ]+ was not found in the available list of properties"
severity: blocking
auto_fix: false
---

# Action target schema drift

## Symptom

```
An error occurred when processing the Generative AI Function Definition entity
with name <Action_Name>_<id>. In the generated or retrieved LightningType
schema, the property <input_or_output_name> was not found in the available
list of properties: [<list of what's actually there>]
```

The publish trace shows:

```
✔ Validate Bundle
✘ Publish Agent     ← fails here
```

## Root cause

The `.agent` file declares an action with inputs/outputs that don't match the actual schema of the target metadata in the publish org. Common causes:

- **Prompt template (`generatePromptResponse://`)** in the org has fewer / different `<apiName>` parameters than the `.agent` declares
- **Flow (`flow://`)** in the org has fewer / different `isInput=true` / `isOutput=true` variables than the `.agent` declares
- **Apex (`apex://`)** invocable class has fewer / different `@InvocableVariable` declarations than the `.agent` declares

The `.agent` was likely authored against a different org's metadata (a source / dev / production org with richer signatures), then deployed to a target org that hasn't kept up. This is the most common publish failure when migrating an `.agent` between orgs.

## Why no auto-fix

Each fix path has business-logic implications:
- Stripping silently loses functionality (e.g., specialty filtering, sub-specialty refinement)
- Updating the target may regress other consumers of that flow / template / Apex
- Re-authoring takes engineering judgment about which side is canonical

Always a deliberate developer decision. Surface options; don't apply silently.

## Fix taxonomy — three options to surface to the developer

### Option 1: Strip `.agent` to match target schema (lossy but fast)

Edit the action call sites and definition to remove the inputs/outputs that the target doesn't have. Document explicitly which features are lost.

For prompt templates / flows / Apex — same shape:

```yaml
# Before (.agent declares 5 inputs)
find_closest_consultant_names: @actions.Get_Closest_Consultant_Name_s
    with "Input:NearbyHospitals" = @variables.Hospitals_available_within_specific_distance
    with "Input:ConsultantName" = ...
    with "Input:speciality" = ...
    with "Input:hospitalName" = ...
    with "Input:subSpeciality" = @variables.search_sub_speciality

# After (target only accepts 2 inputs)
find_closest_consultant_names: @actions.Get_Closest_Consultant_Name_s
    with "Input:NearbyHospitals" = @variables.Hospitals_available_within_specific_distance
    with "Input:ConsultantName" = ...
```

Also strip the dropped inputs from the action `inputs:` definition block.

**What's lost:** specialty and sub-specialty filtering by name. Caller can still filter by hospital list. Document this in the migration bundle.

### Option 2: Update target metadata to match `.agent` (correct fix when target is owned by same team)

For prompt templates: edit `genAiPromptTemplates/<n>.genAiPromptTemplate-meta.xml`, add the missing `<apiName>` entries to `<inputParameters>` / `<outputParameters>`, redeploy.

For flows: edit `flows/<n>.flow-meta.xml`, add missing variables with `isInput=true` or `isOutput=true`.

For Apex: edit `<n>.cls`, add missing `@InvocableVariable` declarations on Request / Response classes, redeploy.

Then re-publish the agent.

**Out of skill scope to do automatically** — could regress other consumers. Flag to developer; let them decide.

### Option 3: Re-author the `.agent` action against current target schema (when neither side is canonical)

Treat the target org's signature as truth. Rewrite the `.agent` action to match. Update both call sites and the action definition block. Document the design choice in the migration bundle.

Use this when the dev / source org schemas have drifted apart and there's no clear "right" version.

## Inspecting target schemas

Retrieve the target metadata to see what's actually there:

```bash
# Prompt template
sf project retrieve start --metadata GenAiPromptTemplate:<n> --target-org <org>
grep -oE '<apiName>[^<]+</apiName>' force-app/main/default/genAiPromptTemplates/<n>.genAiPromptTemplate-meta.xml

# Flow
sf project retrieve start --metadata Flow:<n> --target-org <org>
# Then parse the .flow-meta.xml for variables with isInput=true / isOutput=true

# Apex
sf project retrieve start --metadata ApexClass:<n> --target-org <org>
grep -E '@InvocableVariable' force-app/main/default/classes/<n>.cls
```

## Where in Phase 8 self-heal this surfaces

In the self-heal loop, on a publish failure:
1. Capture stderr.
2. Match against this catalog (E007 regex).
3. On match: surface the three options above, with the org's actual schema attached so the developer can see the delta.
4. Pause. `auto_fix: false` — wait for developer choice.
5. Apply the chosen fix.
6. Re-publish.

The skill should NOT default to Option 1 (strip) silently. Always ask. Stripping is the fastest path to a clean publish but it's also the one that quietly loses functionality.

## Worked examples (Nuffield run, 2026-05-19)

Two cases, both Option 1 (strip — lossy but the user explicitly chose to preserve aivoice's leaner schemas):

### Case A — `Get_Closest_Consultant_Name_s` (prompt template)

Target had: `Input:NearbyHospitals`, `Input:ConsultantName`.
`.agent` declared: + `Input:speciality`, `Input:hospitalName`, `Input:subSpeciality`.
Fix: stripped 3 inputs. Lost specialty/sub-specialty filtering by name.

### Case B — `Agent_Find_Consultants_By_Speciality` (flow)

Target had: `PostalCode`, `Radius`, `daysOffSet`, `speciality`.
`.agent` declared: + `selectedHospital`, `gmcCode`, `subSpeciality`, `returnSlots`.
Fix: stripped 4 inputs. Lost hospital filtering and slot-vs-name distinction.

Both cases: documented as `[review needed]` in the migration bundle so the team knows the deployed agent doesn't match the source-of-truth `.agent` exactly.
