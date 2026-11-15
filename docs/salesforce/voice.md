# Voice guidance

- Determine the telephony architecture and enabled settings before evaluating recording. Supported Real-Time Streaming configurations can record agent calls; inspect Record Voice Calls with Agents and per-agent Flow overrides. Check participant notice/consent and each recorded call leg; never automatically mark recording N/A.
- Verify language/persona availability in the target release and builder, including beta status. Current voice guidance describes monolingual agents using the configured default language; text Allowed Languages is not evidence of multilingual voice.
- Validate interruption, silence, recognition failures, latency, escalation, and recording behavior with real test calls in an authorized environment. Static metadata cannot prove those outcomes.

## Sources checked 2026-11-15

- [Turn on Voice Call Recording and Transcription When Using Real-Time Streaming](https://help.salesforce.com/s/articleView?id=ai.agent_record_voice_calls_realtime_streaming.htm&release=264.0.0&type=5)
- [Agentforce Voice Considerations](https://help.salesforce.com/s/articleView?id=ai.agentforce_voice_considerations.htm&release=264.0.0&type=5)
