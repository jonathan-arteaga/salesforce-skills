# Industry and role patterns for agent design

Read only the selected rows and the composition workflow. These are adaptable design hypotheses, not mandatory industry personalities, legal requirements, or claims that Salesforce supplies every proposed action. Checked 2026-11-15. Source IDs below distinguish documented product capabilities from our design synthesis.

Contents: [Compose](#compose-the-design) · [Roles](#role-patterns--usable-across-industries) · [Industries](#industry-patterns) · [Situations](#situation-overlays) · [Examples](#example-contrasts-synthetic-not-approved-policy) · [Evaluation](#build-brief-and-measurable-evaluation) · [Sources](#sources-and-evidence-boundaries)

## Compose the design

1. Identify the job, audience, industry/subsector, brand, locale, channel, and current situation. Separate customer-facing autonomy from employee assistance. An employee's access does not authorize customer self-service.
2. Choose one role pattern and one industry context below. Offer two materially different personality directions with sample replies; label assumptions. Do not infer personality, vulnerability, literacy, or preferences from protected traits. Ask only for missing decisions that materially change the result.
3. Draft a stable character contract and situational calibrations. Adapt tone to explicit context (confusion, time pressure, service failure), not demographic stereotypes or unverified sentiment scores. Preserve policy and action outcomes across tone variants. Never pretend to be human or a credentialed specialist.
4. Give the architecture owner a separate list of policy decisions, authoritative data, action boundaries, human handoff needs, and prerequisites. Persona owns words and stance, not control design or script encoding. A design brief is not a second persona-handoff schema; use the existing semantic handoff for implementation.
5. Check existing Salesforce templates/actions before proposing custom work. Record exact source, target support, licenses, data model, channel, and execution identity. Mark each action documented candidate / discovered in org / custom proposed / unavailable. Never invent an API name from a marketing label.
6. Design the success path and a service-recovery path together. Produce examples for missing evidence, denied requests, uncertain action outcomes, and unavailable handoff. Make customer effort and verified resolution primary; containment and sales conversion alone are insufficient.
7. Hand off: persona → character/calibration; conversation-design → dialogue/repair; agent-architecture → actions/control/authority; voice-ux → spoken delivery; agentforce-generate → implementation; agentforce-test → runtime scenarios. Data 360 identity/profile enrichment is neither authentication nor proof of consent.

## Role patterns — usable across industries

| Role | Personality direction | Useful output | Failure to design against |
| --- | --- | --- | --- |
| Service recovery | Calm advocate; concise, accountable | Explain verified status and next available remedy | Apologies without action, invented compensation, hiding failed transactions |
| Discovery and sales | Curious guide; informative without pressure | Compare relevant options and surface tradeoffs | Upselling during distress, invented scarcity, ignoring opt-out |
| Onboarding navigator | Patient organizer; encouraging without patronizing | One actionable next step plus progress | Repeated questions, unnecessary personal data, declaring approval too early |
| Employee copilot | Precise peer; distinguish facts and suggestions | Evidence-backed summary and editable draft | Acting with the employee's authority without intent; leaking internal notes |
| Operations coordinator | Brief dispatcher; exact about state and ownership | Exception queue and confirmed assignment | Treating queued as completed; duplicate work after retries |
| Coach or educator | Curious coach; adjust to stated experience | Explanations and practice with feedback | Shaming, unfounded grading/diagnosis, substituting advice for decisions |
| Analyst or reviewer | Skeptical collaborator; calibrated confidence | Findings, evidence, uncertainty, proposed next step | Invented explanations, unsupported causal claims, automatic adverse decisions |

## Industry patterns

Voice directions below are our starting hypotheses. Product anchors support use-case discovery, not the personality recommendations or deployability.

| Industry / example job | Two directions worth testing | Context and control questions for architecture | Signature recovery test | Anchor |
| --- | --- | --- | --- | --- |
| Retail / order support and product discovery | Efficient shopping guide; expressive brand concierge | Current stock, prices, order ownership, refund eligibility; suppress selling during complaint resolution | Refund times out after payment system accepted it | R, U |
| Banking / disputed charge or loan information | Reassuring explainer; precise service specialist | Verified account access, authoritative rates/terms, dispute state; separate product information from approval or personalized financial advice | Customer asks to skip verification because the agent remembers them | F |
| Insurance / claim intake or employee policy summary | Calm claims navigator; concise coverage explainer | Policy version, effective dates, claim evidence, decision authority; no invented coverage or payout promise | User describes a loss but coverage is ambiguous | F |
| Healthcare / scheduling and access navigation | Warm logistical guide; clear appointment coordinator | Identity/proxy authority, scheduling system, clinician escalation, minimum necessary data; keep administrative role separate from clinical judgment | Symptom concern appears during appointment scheduling; switch to approved escalation protocol | H |
| Travel and hospitality / disruption recovery | Resourceful travel coordinator; discreet concierge | Live inventory, fare/rate conditions, time zones, party authorization, accessibility preferences | A replacement reservation is uncertain while original booking remains active | T |
| Manufacturing / warranty or service coordination | Methodical technical partner; concise service dispatcher | Asset/serial identity, entitlement, approved procedures, technician qualifications, work-order state | User requests an undocumented hazardous workaround to restore uptime | M |
| Communications / billing or connectivity support | Plain-language troubleshooter; transparent billing guide | Billing source, outage evidence, service-level terms, account authority; distinguish estimated from confirmed restoration | Prior troubleshooting failed and a bill dispute is still open | C |
| Energy and utilities / outage and plan navigation | Calm status coordinator; accessible plan explainer | Authoritative outage status, effective tariffs, service location and approved emergency protocol | No restoration estimate exists; customer reports a potentially dangerous condition | E, U |
| Education / admissions and student navigation | Encouraging navigator; practical campus guide | Current deadlines, applicant/student access, guardian authority, financial-aid decision owner | Parent asks for a student's private application outcome | D |
| Public sector / benefits or permit navigation | Clear procedural guide; respectful case navigator | Jurisdiction, current criteria, accessibility, evidence requirements, official decision and appeal owner | User interprets an application completeness check as a benefits award | P |
| B2B technology / troubleshooting and onboarding | Precise technical peer; patient implementation guide | Product version, tenant isolation, telemetry consent, approved runbooks, incident ownership | Customer requests another tenant's logs to compare an issue | U |
| Nonprofit / volunteer and program navigation | Welcoming coordinator; practical resource guide | Program capacity, eligibility decision owner, contact preferences, beneficiary privacy | No service slot is available; avoid inventing a referral or guaranteed aid | U |

## Situation overlays

- Frustration: acknowledge the specific failure once; reduce flourish; say what can happen next.
- Urgency: lead with the next safe action and confirmed state; do not accelerate past required checks.
- Uncertainty: distinguish known, inferred, pending, and unavailable. Avoid turning a confident voice into a guarantee.
- Vulnerability or sensitive disclosure: avoid humor and sales prompts; use the organization's approved specialist route. Do not diagnose the person from wording.
- Success: summarize only confirmed effects, any remaining step, and a reference if the system returned one.
- Human handoff: identify reason, status, necessary verified facts, outstanding transaction, and destination. “Requested” is not “connected.” If unavailable, give the actual supported alternative.
- Channel or locale change: preserve meaning and policy; adapt length and turn-taking. Validate with native-language reviewers and channel tests, not literal translation alone.

## Example contrasts (synthetic, not approved policy)

User: “This is the third time I've asked. Just fix it.”

- Retail recovery: “You've already spent time on this. I'll check the order's current refund status before we try anything else.” Requires an authorized status action.
- Banking: “Let's check the dispute's status. First, we'll complete the required account verification.” Never treat familiarity as verification.
- Healthcare scheduling: “Let's focus on the appointment. Which location were you trying to book?” Use only when administrative clarification is appropriate; urgent clinical concerns need the approved escalation path.
- Manufacturing: “Let's confirm the asset and the last recorded fault so we don't repeat a failed step.” Do not request unsafe troubleshooting.

These differ in vocabulary and next step, not in willingness to bypass policy. Test alternatives against the same facts and outcomes.

## Build brief and measurable evaluation

Use this compact table inside the existing deliverable, not a new mandatory file hierarchy:

| Field | Required decision |
| --- | --- |
| Job and audience | Specific task, industry/subsector, customer or employee, channel and locale |
| Character | Two directions considered; chosen traits and anti-patterns; stakeholder assumptions |
| Situation flex | Routine, frustrated, uncertain, urgent, successful, handoff examples |
| Evidence and capability | Source IDs, candidate templates/actions, target availability, authoritative data and freshness |
| Authority | What the agent can explain, recommend, draft, execute, or must hand off; owner decides |
| Minimum viable workflow | One valuable job, one recovery path, dependencies and next implementation step |
| Evaluation | Synthetic scenario, expected tone, expected permitted action, disallowed result, observed trace, status |

Score tone fit, clarity, honesty, customer effort, and handoff usefulness separately (0 poor / 1 partial / 2 meets agreed target). Hard failures—unauthorized access, fabricated completion, unsafe advice, discriminatory treatment—cannot be averaged away by a good personality score. Compare two persona variants using identical tasks, tools, facts, and action permissions. Include repeat-contact and downstream correction/reopening alongside satisfaction and successful completion. Mark all unexecuted scenarios NOT RUN; a drafted script is not runtime evidence.

## Sources and evidence boundaries

- **V — Persona design:** https://www.salesforce.com/agentforce/personas/ — context, expression dimensions, calibration, and example-driven design. Our role and industry combinations are synthesis, not Salesforce presets.
- **U — Use-case catalog:** https://www.salesforce.com/agentforce/use-cases/ — inspiration across service, sales, recruiting, supplier onboarding, and operations; marketing examples are not installation instructions.
- **R — Retail:** https://www.salesforce.com/retail/artificial-intelligence/ — shopping and service use-case inspiration; verify actual Commerce/Service actions separately.
- **F — Financial services:** https://help.salesforce.com/s/articleView?id=ind.fsc_agents_overview.htm&language=en_US&type=5 — distinct banking, loan, advisor, and insurance assistance contexts; check each template's setup and data model.
- **H — Health:** https://help.salesforce.com/s/articleView?id=sf.hc_admin_health_einstein.htm&language=en_US&type=5 and https://help.salesforce.com/s/articleView?id=ind.hc_admin_agentforce_cc_voice_setup.htm&language=en_US&type=5 — healthcare template families and voice scheduling prerequisites; not authorization for clinical advice.
- **M — Manufacturing:** https://help.salesforce.com/s/articleView?id=ind.mfg_gen_ai_agentforce_templates_in_manufacturing_cloud.htm&language=en_US&type=5 — template/action catalog for asset service, inventory, sales, and channel work.
- **C — Communications:** https://help.salesforce.com/s/articleView?id=ind.comms_agentforce_for_communications_cloud.htm&language=en_US&type=5 — billing, service-level insights, and quoting capabilities with differing dependencies.
- **D — Education:** https://help.salesforce.com/s/articleView?id=sfdo.ec_set_up_agentforce_for_education_cloud.htm&language=en_US&type=5 — education agent prerequisites; school policy and record-access rules require local evidence.
- **P — Public sector:** https://help.salesforce.com/s/articleView?id=ind.psc_agentforce_for_public_sector_solutions.htm&language=en_US&type=5 — public-sector feature discovery; jurisdiction and decision rights remain implementation-specific.
- **T — Travel/hospitality:** https://www.salesforce.com/travel-hospitality-transportation/hospitality/ and https://www.salesforce.com/customer-stories/engine/agentic-service/ — reservation and recovery use cases; customer-story outcomes are not performance guarantees.
- **E — Utilities:** https://help.salesforce.com/s/articleView?id=release-notes.rn_energy_and_utilities_cloud.htm&language=en_US&release=262&type=5 — tariff comparison and connection workflows; proposed outage persona is a design hypothesis, not a verified packaged agent.

Industry documentation can disagree with platform-wide guidance. For example, broad utilities Trust Layer wording describes masking while the agent masking limitations page says it is disabled for agents. Do not promise masking from an industry overview; verify the exact execution path and current limitations. Regulatory and clinical rules are not established by this playbook; obtain the organization's approved policies and qualified owners.
