---
version: "1.1.0"
date: 2026-09-01
---

# Reading Level Characterization Scenarios

This fixture records stable prompts and grounded product facts for before/after
Persona skill checks. It does not prescribe the future wording.

## Grounded facts

Use only these facts in generated responses:

- Ridge Shell uses a 3-layer waterproof-breathable construction.
- The face fabric is 75 denier.
- Denier is the yarn-weight measure used for the face fabric.
- The verified hydrostatic-head rating is 20,000 mm.
- Hydrostatic head measures resistance to water pressure and is reported in millimeters.
- Pit zips provide mechanical ventilation.
- The manufacturer positions it for sustained rain and alpine use.
- Store pickup requires an order ID and photo ID.

Do not invent breathability numbers, weight, price, warranty terms, durability
guarantees, or store-pickup requirements beyond the two listed items.

## Prompts

1. **Novice:** “Will this keep me dry on an all-day hike?”
2. **Expert:** “Give me the membrane construction, denier, hydrostatic-head rating, and venting.”
3. **Ambiguous:** “How technical is this shell?”
4. **One isolated term:** “Is the denier good?”
5. **Repeated jargon:** “Compare the 3-layer build and 75D face fabric. Does the 20K hydrostatic head make sense for sustained alpine rain?”
6. **Explicit downshift:** “Plain English, please.”
7. **Explicit upshift:** “Just give me the specs.”
8. **Technical question:** “What is the hydrostatic-head rating?”
9. **Outcome question:** “What difference will this make when I’m above treeline in bad weather?”
10. **Challenge:** “A 20K rating means it can never leak, right?”
11. **Compound first-turn expertise:** “Compare the 3-layer laminate, 75D face, 20K hydrostatic head, and pit-zipped mechanical ventilation for sustained alpine rain.”
12. **Term-local clarification:** After demonstrated shell expertise: “What does hydrostatic head mean?” Define only that term; keep the rest of the response at the demonstrated level.
13. **Material domain change:** After a technical shell discussion: “Switching topics: what do I need for store pickup?” Return to the Reading Level baseline and re-evaluate in the new domain.
14. **Missing-data bridge:** “The breathability number isn't listed. Does that mean the Ridge breathes poorly?” State that missing data is not evidence; do not infer the outcome.

## Baseline observations to record during implementation

- terminology/specification density;
- whether terms are defined;
- whether facts remain invariant;
- whether unsupported specifications appear;
- whether the response leads with evidence or outcome;
- whether it bridges to the opposite frame;
- whether one isolated term triggers over-adaptation;
- whether multiple mutually reinforcing terms trigger a bounded first-turn upshift;
- whether a term-local clarification preserves the demonstrated level elsewhere;
- whether inferred expertise resets after a material domain or subagent change;
- whether a missing-data bridge states the limitation instead of inferring an outcome.
