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
minimality: argued
does_not_give:
  - a discriminating experiment selector — see the gap note below
  - transfer of a learned account across environments
---

# Theory / Test / Update

**The requirement.** "My agent must form a theory, test it, and update it." This is the
single most-cited capability gap for interactive agents, named verbatim in ARC Prize's
ARC-AGI-3 failure analysis.

**The minimum, as currently stocked.** Two of the three legs have credible members:
an explicit, optimizable hypothesis ([`technique.latent-program-search`]) and a planner
that can act on a committed account ([`technique.means-ends-analysis`]).

**The bundle does not close.** The middle leg — [`exploration.experiment-design`] — has
no member. Every candidate the register currently holds selects actions by *novelty of
the state reached*, not by *how far the outcome would discriminate between live
hypotheses*. A coverage-driven explorer will spend its whole budget in regions where all
live hypotheses agree.

**This is the point of the bundle form.** A table would have shown three rows with
entries in two of them and let the eye slide past. Stated as a bundle with a declared
`satisfies` set, the missing leg is the deliverable: an unfilled `load_bearing_for` slot
is a research gap with a specification attached.

**`minimality: argued`, not `tested`.** No ablation has shown each member is necessary.
Under the schema, promoting this to `tested` requires citing one.
