# Salesforce Skills

Salesforce and Agentforce skill marketplace: **43 skills**. Includes Data 360, Apex, Flow, LWC, integrations, access, analytics, agent design/testing, grounding, Prompt Builder and Agent API workflows.

## Install

```sh
codex plugin marketplace add jonathan-arteaga/salesforce-skills
codex plugin add data360-ingestion-modeling@salesforce-skills
```

The marketplace name is `salesforce-skills`, separate from the personal `skills` marketplace. Packages remain available on demand. After verifying the new repository is accessible, replace previously enabled Salesforce packages from the old marketplace with the corresponding packages here; avoid enabling two copies of the same skill. No installed host profiles are changed by the export.

See [Salesforce guidance](docs/salesforce/README.md), [practitioner evidence](docs/salesforce/practitioner-insights.md), and [validation evidence](tests/results/2026-11-15-salesforce-expansion.md). The separate [Docs MCP package](integrations/salesforce-docs-mcp/README.md) is included. Older reports describe the combined repository at the time of their audit.

## Validate

```sh
python3 -m pip install -r requirements-validation.txt
python3 scripts/package_marketplace.py --check
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

CI also runs the persona, architecture-analysis and Data 360 analysis suites. These are offline checks; live org behavior requires authorized sandbox validation. Edit canonical references and run `python3 scripts/package_marketplace.py` to regenerate consumers.

## Provenance

Extracted from `jonathan-arteaga/arteaga-ai-skills` at baseline `68c6c18a4bc3cf7f2ef0e24109f3b2140b864e00` with split-aware packaging infrastructure. Per-file checksums in [migration-manifest.json](migration-manifest.json) cover every preserved plugin file. This snapshot intentionally excludes personal writing profiles, personal packages and unrelated Git history. Public publication authorized by the repository owner on 2026-11-15. Original per-file checksums describe the extraction baseline; subsequent reviewed changes are tracked in Git. Third-party license files remain with their packages.

## Design agents for the job and context

Use `persona` for character and calibration, `conversation-design` for interactions, `agent-architecture` for authority and workflows, and `agentforce-generate` for Agent Script implementation. The [industry and role playbook](plugins/persona/skills/persona/references/industry-patterns.md) combines 12 industry contexts, seven roles, situation-specific behavior, and measurable evaluation. These are adaptable starting points, not stereotypes or preconfigured deployable agents.
