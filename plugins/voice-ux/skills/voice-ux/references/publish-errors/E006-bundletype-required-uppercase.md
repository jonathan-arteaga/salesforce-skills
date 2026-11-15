---
id: E006
name: bundletype-required-uppercase
match:
  regex: "Required field is missing: bundleType"
severity: blocking
auto_fix: true
---

# bundleType missing or wrong case

## Symptom

```
Error (MetadataTransferError): Metadata API request failed: Error: Required field is missing: bundleType
```

The publish trace shows:

```
✔ Validate Bundle
✔ Publish Agent
✔ Retrieve Metadata        (or — Skipped with --skip-retrieve)
✘ Deploy Metadata          ← fails here
```

`Validate Bundle` and `Publish Agent` both pass; the agent record IS created in the org. The error is on the final `Deploy Metadata` step that re-deploys the bundle XML back to the local DX project.

## Root cause

`<bundleType>` is a required field on the `AiAuthoringBundle` metadata type, AND its value is case-sensitive. The org-side metadata API accepts only `AGENT` (uppercase). Mixed-case (`Agent`, `agent`) fails.

The error message is misleading — it says "missing" even when the field is present, if the value is the wrong case. Treat "missing" and "wrong case" as the same root cause for this check.

## Canonical fix

Edit `force-app/main/default/aiAuthoringBundles/<name>/<name>.bundle-meta.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AiAuthoringBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <bundleType>AGENT</bundleType>
</AiAuthoringBundle>
```

Required:
- Root element `AiAuthoringBundle` (mixed-case "Ai", not "AI").
- `<bundleType>AGENT</bundleType>` — **uppercase, no exceptions**.

Re-run publish. The Deploy Metadata step now succeeds.

## Why no auto-detection earlier

The offline `@agentscript/agentforce` validator validates the `.agent` source, not the bundle XML. Server-side `sf agent validate authoring-bundle` validates the agent script too, not the bundle XML for the deploy-back step. The case error only surfaces on the final deploy.

The skill should:
1. Generate `.bundle-meta.xml` correctly in Phase 7 (uppercase by default) — see SKILL.md Phase 7 step 1.
2. Lint any user-edited bundle XML before Phase 8 publish.

## Bonus: prefer `--skip-retrieve` on publish

The post-publish retrieve+deploy back to local project has had recurring bugs (this E006, plus E005 for `target` undefined errors). The agent itself publishes fine; the local sync is the bit that breaks.

Default Phase 8 publish command:

```bash
sf agent publish authoring-bundle --api-name <name> --target-org <org> --skip-retrieve
```

Use `--skip-retrieve` unless you specifically need the platform-generated supporting metadata pulled into your DX project. Most voice-migration workflows don't — the source `.agent` is canonical.

If you do need the local sync, run a standalone retrieve after publish:

```bash
sf project retrieve start --metadata AiAuthoringBundle:<name> --target-org <org>
```
