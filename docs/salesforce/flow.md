# Flow guidance

- Use before-save for supported updates to the triggering record; use after-save when the action needs saved IDs, related-record changes, or other unsupported before-save operations. Recheck element support against the chosen flow type.
- Keep record operations outside loops, collect changes for bulk execution, use selective entry conditions, guard against recursive updates, and design fault handling without swallowing failures.
- Inspect the actual Flow run context. System context with sharing still bypasses CRUD/FLS; system context without sharing also bypasses record sharing. Agent action context does not automatically make a privileged Flow customer-safe.
- Use available, documented authoring tools or retrieved/project Flow metadata. A particular MCP generation pipeline is a connector workflow, not the only Salesforce-supported way to create Flow XML. Validate as Draft and test bulk, negative, fault, and recursion cases before authorized activation.

## Sources checked 2026-11-15

- [Before-Save Record-Triggered Flows](https://help.salesforce.com/s/articleView?id=platform.flow_concepts_trigger_record.htm&release=264.0.0&type=5)
- [Decide Between Before-Save and After-Save Record-Triggered Flows](https://help.salesforce.com/s/articleView?id=platform.automate_flow_build_get_started_record_triggered_before_or_after_save.htm&release=264.0.0&type=5)
- [Agent Execution Context and Data Access by Type](https://help.salesforce.com/s/articleView?id=ai.agent_execution_data.htm&release=264.0.0&type=5)
- [Flow Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_visual_workflow.htm)
