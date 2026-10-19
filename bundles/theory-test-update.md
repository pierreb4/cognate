---
id: bundle.theory-test-update
kind: bundle
name: Theory / Test / Update
satisfies:
  - modeling.hypothesis-formation
  - exploration.experiment-design
  - modeling.belief-update
  - planning-execution.goal-decomposition
members:
  - technique: technique.means-ends-analysis
    load_bearing_for: [planning-execution.goal-decomposition]
  - technique: technique.oomdp-identification
    load_bearing_for: [modeling.hypothesis-formation, exploration.experiment-design, modeling.belief-update]
minimality: argued
does_not_give:
  - the object vocabulary its hypotheses and its experiment selector are stated in — supplied, never inferred
  - an experiment budget any action-charged deployment can afford — the one published ratio is 494 identification actions against a 94-action optimal path
  - transfer of a learned account across environments
---

# Theory / Test / Update

**The requirement.** "My agent must form a theory, test it, and update it." This is the
loop ARC Prize's ARC-AGI-3 replay audit says the environments demand — "forming a working
theory, testing it, updating it when the evidence disagrees" — and the one it reports frontier
models failing at, at a different step in each model ([source](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)).

**The minimum, as currently stocked.** Two members: [`technique.oomdp-identification`],
which forms the account, tests it and revises it, and a planner that can act on a committed
account ([`technique.means-ends-analysis`]).

**Why acting on the theory is in `satisfies`.** The identifier alone covers forming, testing
and updating `direct`. But the audit scores the loop by play, and a theory that nothing acts
on scores nothing, so the requirement includes reaching a goal from the committed account:
`planning-execution.goal-decomposition`. That makes the planner load-bearing, not
decoration. Without that fourth capability the bundle would have one member, and a bundle
of one says nothing about how techniques combine.

**Why latent-program-search left.** It held the hypothesis leg while it was the only `direct`
holder: an explicit, optimizable hypothesis. Once the identifier's conditions were graded
`direct` on hypothesis formation too (formed from an authored vocabulary, as a DSL search forms
programs from authored primitives), the two `overlap` there, and an overlap adds no coverage.
`grade_combination.py` then reports the latent search REMOVABLE. Dropping it costs no coverage.
It also takes three preconditions off the build: a learned latent space, weight gradients, and
the per-task compute the gradient search spends. An inference-only deployment cannot supply the
first two. What it gave that the identifier does not
is a hypothesis that needs no authored vocabulary. That is the first line of `does_not_give`,
and it now applies to the theory leg as well as the test leg.

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
