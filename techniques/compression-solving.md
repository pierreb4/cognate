---
id: technique.compression-solving
kind: technique
name: MDL / Compression-Based Solving
addresses:
  - capability: modeling.per-task-adaptation
    strength: direct
    note: the only training that ever happens is on the single target puzzle — the limiting case of adapting to the instance
  - capability: modeling.hypothesis-formation
    strength: direct
    note: the hypothesis is whatever shortest description reproduces the demonstrations; the objective itself is the commitment
requires:
  - token: differentiable-objective
    note: a differentiable description-length objective over the task
  - token: per-task-compute
    note: inference-time optimization per puzzle
  - token: matched-architecture
    note: an architecture whose inductive biases match the domain's symmetries
cost: medium
evidence:
  - claim: "20% of ARC-AGI-1 evaluation puzzles with a 76K-parameter model and no pretraining"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: uncapped-no-pretraining-single-puzzle-training
    source: https://arxiv.org/abs/2512.06104
    stars: 2
no_absolute_score: false
caveats:
  - "The comparison that matters is not 20% against leaderboard entries but 20% against ZERO pretraining and 76K parameters. Ranked on the percentage axis alone this node reads as weak, which is the wrong reading."
interacts:
  - technique: technique.latent-program-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both reach a hypothesis by optimizing a continuous objective at test time rather than
      by enumerating discrete candidates
  - technique: technique.test-time-training
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      both spend per-task gradient steps on the instance; they differ in what is fitted, not
      in when
---

# MDL / Compression-Based Solving

**What it is.** CompressARC. Take one puzzle, and fit a small network to it alone by
minimizing the description length of that puzzle — no pretraining, no training set, no
transfer. The solution falls out of the compression.

**The cognate.** The oldest formal statement of induction there is: the best account of the
data is the shortest one that reproduces it. Every other node in this register approximates
that with search or with priors baked into weights; this one optimizes it directly.

**Therefore.** Read this node as a control, not as a competitor. It bounds how much of ARC
performance can be attributed to pretraining knowledge, because it has none, and 20% is
where the floor turned out to be.

**The limit.** It is slow, it must be re-run from scratch per puzzle, and its inductive
biases are hand-designed for grid symmetries — the priors did not disappear, they moved
from the data into the architecture.
