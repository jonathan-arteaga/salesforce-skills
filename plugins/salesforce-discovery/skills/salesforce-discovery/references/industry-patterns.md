# Industry & Role Patterns (Design Hypotheses)

These patterns are adaptable discovery hypotheses, not Salesforce-prescribed personalities, legal rules, or claims that Salesforce ships every action. Always test assumptions against customer evidence, offer two materially different voice directions, separate customer-facing autonomy from employee assistance, and never infer traits or vulnerability from protected characteristics. Data 360 profile enrichment is neither authentication nor proof of consent.

## 12 Industry Patterns

| Industry / Example Job | Two Voice Directions to Test | Architecture Control Questions | Signature Recovery Test |
| --- | --- | --- | --- |
| **Retail** (order support, shopping) | Efficient shopping guide; expressive brand concierge | Stock/price truth, order ownership, refund eligibility; suppress upselling during complaints | Refund times out after payment system accepted it |
| **Banking** (disputes, loan info) | Reassuring explainer; precise service specialist | Verified account access, authoritative rates/terms, dispute state; separate info from advice/approval | Customer asks to skip verification because agent remembers them |
| **Insurance** (claim intake, policy summary) | Calm claims navigator; concise coverage explainer | Policy version, effective dates, claim evidence, decision authority; no invented coverage/payouts | User describes a loss with ambiguous coverage |
| **Healthcare** (scheduling, access) | Warm logistical guide; clear appointment coordinator | Identity/proxy authority, EHR scheduling, clinician escalation, minimum PHI; zero clinical judgment | Symptom concern appears mid-scheduling; trigger escalation protocol |
| **Travel & Hospitality** (disruptions) | Resourceful travel coordinator; discreet concierge | Live inventory, fare/rate rules, time zones, party authority, accessibility | Replacement reservation uncertain while original remains active |
| **Manufacturing** (warranty, service) | Methodical technical partner; concise dispatcher | Asset/serial identity, entitlement, approved procedures, tech certs, work-order state | User asks for undocumented hazardous workaround for uptime |
| **Communications** (billing, outage) | Plain-language troubleshooter; transparent billing guide | Billing source, outage evidence, SLA terms, account authority; estimated vs. confirmed restoration | Prior troubleshooting failed while bill dispute stays open |
| **Energy & Utilities** (outages, plans) | Calm status coordinator; accessible plan explainer | Authoritative outage status, effective tariffs, service location, emergency protocol | No restoration estimate exists; customer reports hazardous condition |
| **Education** (admissions, student nav) | Encouraging navigator; practical campus guide | Current deadlines, student/applicant access, guardian authority, financial-aid owner | Parent requests a student's private application outcome |
| **Public Sector** (benefits, permits) | Clear procedural guide; respectful case navigator | Jurisdiction, current criteria, accessibility, evidence rules, official decision/appeal owner | User treats completeness check as a benefits award |
| **B2B Technology** (support, onboarding) | Precise technical peer; patient implementation guide | Product version, tenant isolation, telemetry consent, approved runbooks, incident owner | Customer asks for another tenant's logs to compare issues |
| **Nonprofit** (volunteer, programs) | Welcoming coordinator; practical resource guide | Program capacity, eligibility owner, contact preferences, beneficiary privacy | No service slot available; never invent referrals or aid |

## 7 Cross-Industry Role Patterns

| Role | Personality Direction | Useful Output | Failure to Design Against |
| --- | --- | --- | --- |
| **Service recovery** | Calm advocate; concise, accountable | Verified status and next available remedy | Empty apologies, invented compensation, hiding failures |
| **Discovery & sales** | Curious guide; informative, no pressure | Relevant option tradeoffs | Upselling in distress, fake scarcity, ignoring opt-out |
| **Onboarding navigator** | Patient organizer; encouraging | One actionable next step plus progress | Repeat questions, excess PII, premature approval claims |
| **Employee copilot** | Precise peer; facts vs. suggestions | Evidence-backed summary and editable draft | Acting with staff authority unasked; leaking internal notes |
| **Operations coordinator** | Brief dispatcher; exact state/owner | Exception queue and confirmed assignment | Calling queued "complete"; duplicate work on retries |
| **Coach / educator** | Curious coach; adapts to stated level | Clear explanations and guided practice | Shaming, unfounded grading/diagnosis |
| **Analyst / reviewer** | Skeptical collaborator; calibrated confidence | Findings, evidence, uncertainty, next step | Invented causes, automatic adverse decisions |

## Situation Overlays & Evaluation Rubric

- **Frustration:** Acknowledge the specific failure once; drop flourish; state the next concrete step.
- **Urgency:** Lead with the next safe action and confirmed state; never skip required verification checks.
- **Uncertainty:** Separate known, inferred, pending, and unavailable; never sound certain about unconfirmed outcomes.
- **Vulnerability / sensitive disclosure:** Drop humor and sales prompts; route to the approved specialist path without diagnosing the user.
- **Success & Human Handoff:** Summarize only confirmed effects and returned references. For handoff, pass reason, status, verified facts, pending transaction, and destination ("requested" is not "connected").
- **Channel / locale:** Preserve policy and meaning across channels; validate with native reviewers, not literal translation alone.
- **Measurable evaluation:** Score tone fit, clarity, honesty, customer effort, and handoff usefulness separately (`0` poor / `1` partial / `2` target). Hard failures (unauthorized access, fabricated completion, unsafe advice, bias) can never be averaged away. Compare two persona variants against identical tasks, tools, facts, and permissions; mark unexecuted scenarios `NOT RUN`.
- **Industry-doc conflict check:** Industry overview docs can disagree with platform limits (e.g., utilities Trust Layer overviews describe masking while agent masking docs note masking is disabled for agents). Verify exact execution paths and mark every candidate action `documented candidate`, `discovered in org`, `custom proposed`, or `unavailable`.

## Compact Build Brief Fields (Inline Deliverable)

Include these 6 decisions inside the discovery brief rather than creating a separate schema hierarchy:

- **Job & audience:** Specific task, industry/subsector, customer vs. employee caller, channel, and locale.
- **Character & situation flex:** Two voice directions tested, chosen traits/anti-patterns, and examples across routine, frustrated, urgent, uncertain, success, and handoff states.
- **Evidence, authority & MVP:** Authoritative data/freshness, action availability tags, explain/draft/execute/escalate boundaries decided by the owner, one valuable workflow plus recovery path, and evaluation scenarios (`NOT RUN` until executed).
