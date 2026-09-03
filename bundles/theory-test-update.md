---
id: bundle.theory-test-update
kind: bundle
name: Theory / Test / Update
satisfies:
  - modeling.hypothesis-formation
  - exploration.experiment-design
  - modeling.belief-update
members:
  - technique: technique.latent-program-search
    load_bearing_for: [modeling.hypothesis-formation]
  - technique: technique.means-ends-analysis
    load_bearing_for: [planning-execution.goal-decomposition]
  - technique: technique.oomdp-identification
    load_bearing_for: [exploration.experiment-design, modeling.belief-update]
minimality: argued
does_not_give:
  - the object vocabulary its own experiment selector is stated in — supplied, never inferred
  - an experiment budget any action-charged deployment can afford — the one published ratio is 494 identification actions against a 94-action optimal path
  - transfer of a learned account across environments
---

# Theory / Test / Update

**The requirement.** "My agent must form a theory, test it, and update it." This is the
single most-cited capability gap for interactive agents, named verbatim in ARC Prize's
ARC-AGI-3 failure analysis.

**The minimum, as currently stocked.** Two of the three legs have credible members:
an explicit, optimizable hypothesis ([`technique.latent-program-search`]) and a planner
that can act on a committed account ([`technique.means-ends-analysis`]).

**The middle leg now has a member, and it arrived with a price tag.**
[`technique.oomdp-identification`] selects actions by what its live predictions still
disagree about rather than by novelty of the state reached, which is exactly what the slot
specified. It also carries the first published number for what that costs: 494
identification actions on a Pitfall screen whose optimal traversal is 94. Where exploration
is charged out of the same budget it is scored on, the leg is filled and the bundle is
still not affordable — a different finding from an empty cell, and a more useful one.

**This is the point of the bundle form.** A table would have shown three rows with
entries in two of them and let the eye slide past. Stated as a bundle with a declared
`satisfies` set, the missing leg was a specification; what came back to fill it also
reported its own cost in the unit the deployment spends, which is what the specification
was for.

**`minimality: argued`, not `tested`.** No ablation has shown each member is necessary.
Under the schema, promoting this to `tested` requires citing one.
