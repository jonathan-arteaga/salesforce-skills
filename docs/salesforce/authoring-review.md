# Agent authoring review — 2026-11-15

## Scope and result

Reviewed current Salesforce persona guidance, Agent Script overview, Blocks, instructions, patterns, overrides, and lifecycle reference. Fetched full relevant pages through Salesforce Docs MCP and official websites. Updated the shared agent guidance consumed by 18 skills, added an instruction-design worksheet to agentforce-generate, and strengthened capability discovery guidance packaged with all 43 Salesforce skills. Existing persona ownership and Agent Script compiler workflows remain intact.

| Capability | Library disposition | Evidence needed before use |
| --- | --- | --- |
| Persona and contextual voice | Existing persona workflow; clearer handoff and example-driven review | Approved sample responses and behavioral evaluation |
| New Builder / Agent Script / DX | Existing generation workflow; preferred new-build path when supported | Target compiler, metadata validation, org preview |
| Global instructions and subagent overrides | Explicit replacement semantics and lost-policy review | Contradiction and override test cases |
| Mandatory action ordering | Script gates plus backing action authorization | Trusted evidence, denied access and duplicate-call tests |
| Lifecycle hooks | Repeat-safe guidance; no guaranteed cleanup assumption | Target traces including transitions and failures |
| Runtime restart/resume | Documented option; not enabled by default in library | Two-turn target trace |
| Memory / profile / uploaded files | Documented options, conditional adoption | Support, consent, data scope and isolation tests |
| Citations / groundedness / streaming | Explicit quality and channel decisions | Grounded-answer and client rendering tests |
| Other Salesforce / Data 360 capabilities | Existing dated domain guides plus live capability check | Current task-specific docs and org evidence; not exhaustively re-certified in this pass |

## Documentation discrepancies

The Blocks reference uses config.developer_name while the introductory Agent Script example still uses agent_name. Blocks documents optional reset_to_initial_node with resume as default, whereas Flow of Control broadly describes returning to start_agent each turn. Lifecycle reference timing also requires care when reading the high-level prompt construction walkthrough. Do not silently choose an overview example over the target compiler and observed runtime. Record the actual version and trace that resolve the question.

Official upstream repository inspected at commit 788b83fb9f5effb4f1548e3090df415704d3ec64 (2026-11-13). Its latest Salesforce Development 2.8.0 release explicitly identifies standalone skills that require plugin infrastructure. This review does not blindly import that plugin or claim a full upstream diff audit. Source: https://github.com/forcedotcom/sf-skills/commit/788b83fb9f5effb4f1548e3090df415704d3ec64

Product source links are maintained in agent.md and manifest.json. Persona source: https://www.salesforce.com/agentforce/personas/

## Validation

Local marketplace generation/check and packaged Markdown references passed. Metadata validation passed for 82 packaged skills (76 unique). Existing suites passed: root 33, persona 164, architecture 604, Data 360 407; total 1,208. No agent implementation was generated or deployed in this change; no target org, runtime feature availability, live action behavior, or production readiness has been validated.

Independent offline forward test: a refund-agent design preserved persona/control separation, rejected self-asserted verification, required backing authorization, reconciled timeouts before retries, handled replacement overrides, and stated validation limits. The test also found and prompted fixes for an arbitrary 3–6-subagent design default and adjacent prompt markers in an existing example. This was a design test, not compiled or org-executed Agent Script.

## Repository migration

Public publication authorized by the owner on 2026-11-15. Salesforce-only export excludes personal packages and private writing profiles. Source cleanup follows verified destination publication.
