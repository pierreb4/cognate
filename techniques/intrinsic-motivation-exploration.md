---
id: technique.intrinsic-motivation-exploration
kind: technique
name: Intrinsic-Motivation Exploration
addresses:
  - capability: exploration.experiment-design
    strength: incidental
    note: delivers coverage of unvisited states, which is the thing that capability explicitly distinguishes itself FROM
requires:
  - token: reward-channel
    note: a reward channel the intrinsic bonus can be added to
  - token: novelty-estimator
    note: a novelty estimator — a count, a density model, or a fixed random target network
  - token: interaction-budget
    note: enough interaction budget for the bonus to shape behaviour
leverage: both
cost: medium
evidence:
  - claim: "Random network distillation reaches state-of-the-art on Montezuma's Revenge and better than average human performance without demonstrations or access to underlying game state"
    kind: claimed
    split: atari/montezumas-revenge
    regime: not-applicable
    source: https://arxiv.org/abs/1810.12894
    date: 2018-10
    stars: 2
    requires_beyond: [trained-model, weight-gradients]
no_absolute_score: false
caveats:
  - "The RND row is an Atari hard-exploration result. Nothing here has been measured on any ARC split, and the register does not carry a transfer argument in place of a measurement."
  - "Count-based bonuses and novelty search belong to the same family and are described in the prose without evidence rows, because no primary source was checked for them here."
interacts:
  - technique: technique.mcts
    rel: supplies
    scope: value-signal
    note: >-
      the novelty bonus is a value for a reached state where the environment gives none,
      which is exactly MCTS's binding second precondition
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Intrinsic-Motivation Exploration

**What it is.** Add a bonus to the reward for reaching states the agent has not reached
before. The family differs only in how novelty is estimated: visit counts and their
density-model generalizations, novelty search over behaviour descriptors, and random
network distillation — the prediction error of a network trained to match a fixed randomly
initialized one, which is high exactly where observations are unfamiliar.

**The cognate.** Curiosity, in its coverage-shaped form. It is the machine mechanism most
often named when a cognitive account of exploration is wanted, and it is genuinely the
state of the art for hard-exploration environments with sparse reward.

**Why the edge is `incidental` and not `direct`.** [`exploration.experiment-design`] is
written specifically to separate these two things. A novelty bonus answers *where have I
not been*; an experiment answers *what outcome would tell me which of my hypotheses is
wrong*. An intrinsic-motivation agent will happily spend its whole budget in a region where
every live hypothesis predicts the same thing, and will report that budget as progress.

**The limit.** The bonus is defined over observations, not over beliefs. Nothing in the
family reads a hypothesis set, which is why the capability it most resembles is the one it
leaves open.
