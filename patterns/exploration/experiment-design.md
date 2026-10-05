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
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
---

# Experiment Design

**Context.** A hypothesis is held ([`modeling.hypothesis-formation`]) and actions are
available. Actions cost something — turns, tokens, samples, or score.

**Problem.** Most exploration methods answer *"where have I not been?"* — novelty,
count-based bonuses, random network distillation. That is coverage, not experiment.
An experiment is an action chosen because its **outcome discriminates between the
hypotheses currently held**. Coverage-driven exploration will happily spend its budget
in regions where every live hypothesis predicts the same thing, learning nothing. The
hypotheses worth splitting are not always about mechanics: where the dynamics are learned
and the objective is not, they are goal hypotheses ([`goal-setting.goal-inference`];
[`technique.test-time-digital-twin`] reports exactly that split).

**Therefore.** Score candidate actions by expected information gain with respect to the
live hypothesis set, not by novelty of the state they reach — as a step of the loop that
can refuse an action, not as a tool the policy may call, since a ranker the policy may
call is one it may ignore.

**Known failure.** "Inefficient exploration" is the first of four failure modes ARC Prize
names for ARC-AGI-3 agents. Under RHAE scoring — `(human_actions / agent_actions)²` —
undiscriminating exploration is not merely slow, it is *quadratically* penalized, which
makes this pattern load-bearing for score rather than only for learning. The pattern
binds the agent's designer too: a design change whose plausible effect is below what the
evaluation can detect is an experiment every live hypothesis predicts alike, and the same
remedy applies — price the discrimination before the run, and refuse it when it fails.

**Status: open.** This is a genuinely thin cell. Most published exploration machinery
addresses coverage; the discriminating-experiment framing has far less machine-side
work attached to it than the human-side literature would suggest.
