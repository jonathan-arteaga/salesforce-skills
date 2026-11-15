# Deploy, Publish, and Activate

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Deploy, Publish, and Activate

1. Read [CLI for Agents](salesforce-cli-for-agents.md),
   [Metadata & Lifecycle](agent-metadata-and-lifecycle.md), and
   [Deploy](deploy-reference.md).
2. Compile locally and validate against the target org. Deploy the bundle and
   dependencies, then run live preview with realistic coverage and inspect
   traces. Do not proceed through a blocking result.
3. Present the exact target org and version state. Obtain explicit user approval
   before publishing or activating.
4. Publish, activate, and verify the user-facing agent only after approval.
5. **Voice agents — wiring a telephony channel is a separate, opt-in step; never
   auto-wire it.** Attaching a phone number creates real routing infrastructure
   (flows, a queue, an active `MessagingChannel`) and consumes a provisioned
   number, so do it only when the user **explicitly asks** and has supplied a
   **provisioned phone number** (confirm it exists — do not assume or invent
   one). If either is missing, stop and say what's needed. When both hold, attach
   it headless via the CLI — do not send the user to Agent Builder. Follow
   [Headless Telephony CLI](voice-telephony-cli.md).
