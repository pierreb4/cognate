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
leverage: computation
cost: medium
evidence:
  - claim: "20% of ARC-AGI-1 evaluation puzzles with a 76K-parameter model and no pretraining"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: uncapped-no-pretraining-single-puzzle-training
    source: https://arxiv.org/abs/2512.06104
    date: 2025-12
    stars: 2
no_absolute_score: false
caveats:
  - "The comparison that matters is not 20% against leaderboard entries but 20% against ZERO pretraining and 76K parameters. Ranked on the percentage axis alone this node reads as weak, which is the wrong reading."
interacts:
  - technique: technique.dsl-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      one account per task in both; the DSL's reachable set is a human's guess at the domain
      and the description-length objective's is the architecture's, so they fail on different
      tasks for the same reason
  - technique: technique.evolutionary-program-synthesis
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a single account driven to a minimum against a population held at once; compression
      cannot report its second-best hypothesis, which is what makes an evolutionary pool
      useful
  - technique: technique.induction-transduction-ensemble
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      one objective against two representations arbitrated; compression has no second arm
      that could disagree with the first
  - technique: technique.llm-sampling-program-synthesis
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both commit to an account the demonstrations can refute; the prior sits in the
      objective in one and in a pretrained model's weights in the other
  - technique: technique.modality-driven-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a single representation optimized against several generated and judged; running both
      buys candidate diversity, not a second kind of account
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a shortest description scored globally against condition-effect rules killed locally,
      one counterexample at a time; neither reads the other's account
  - technique: technique.recursive-latent-reasoners
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      fitting to the instance at inference in both; gradient steps on the one puzzle against
      recurrent depth plus a puzzle identifier
  - technique: technique.refinement-harness
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      the register's sharpest contrast on this capability: everything is fitted to the
      instance in one and nothing is, in the other
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
