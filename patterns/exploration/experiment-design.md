---
id: exploration.experiment-design
kind: capability
name: Experiment Design
faculty: exploration
human_source:
  - title: "Intrinsic motivation and the exploration/exploitation tradeoff"
    url: https://oecs.mit.edu/
part_of: [exploration]
completed_by: []
status: open
---

# Experiment Design

**Context.** A hypothesis is held ([`modeling.hypothesis-formation`]) and actions are
available. Actions cost something — turns, tokens, samples, or score.

**Problem.** Most exploration methods answer *"where have I not been?"* — novelty,
count-based bonuses, random network distillation. That is coverage, not experiment.
An experiment is an action chosen because its **outcome discriminates between the
hypotheses currently held**. Coverage-driven exploration will happily spend its budget
in regions where every live hypothesis predicts the same thing, learning nothing.

**Therefore.** Score candidate actions by expected information gain with respect to the
live hypothesis set, not by novelty of the state they reach.

**Known failure.** "Inefficient exploration" is the first of four failure modes ARC Prize
names for ARC-AGI-3 agents. Under RHAE scoring — `(human_actions / agent_actions)²` —
undiscriminating exploration is not merely slow, it is *quadratically* penalized, which
makes this pattern load-bearing for score rather than only for learning.

**Status: open.** This is a genuinely thin cell. Most published exploration machinery
addresses coverage; the discriminating-experiment framing has far less machine-side
work attached to it than the human-side literature would suggest.
