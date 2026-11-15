# Observe guidance

- Check tracing enablement, Standard Data Model version (documented minimum 1.130), selected data space, permissions, and ingestion delay before treating no rows as no sessions. A failed probe does not establish that tracing is disabled.
- Trace collection can contain PII, PHI, payment data, prompts, and action results. Minimize exports and apply authorized Data 360 access/masking controls; do not assume Einstein Trust Layer LLM masking sanitizes stored traces.
- Changing the tracing data space does not migrate older data. Trace queries and reports must state the space, time window, agent/version filters, and missing evidence.
- For read-only investigation, use existing evidence. Deploying a helper, running live actions, changing alerts, enabling tracing, or editing/publishing an agent requires scope already authorized by the user. Missing traces do not authorize those fallbacks.

## Sources checked 2026-11-15

- [Set Up Agentforce Session Tracing](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_setup.htm&release=264.0.0&type=5)
- [Agentforce Session Tracing](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace.htm&release=264.0.0&type=5)
