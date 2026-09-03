---
id: technique.recursive-latent-reasoners
kind: technique
name: Recursive Latent Reasoners (HRM / TRM)
addresses:
  - capability: modeling.per-task-adaptation
    strength: partial
    note: the outer refinement loop, not the recursion, appears to carry the result
  - capability: modeling.hypothesis-formation
    strength: incidental
    note: >-
      the refinement loop revises a candidate output grid, never an account of the rule
      producing it; as with test-time-training the commitment is held in weights and a
      latent, so nothing downstream can be told what the system currently believes
requires:
  - token: training-distribution
    note: training on the target task distribution
  - token: trained-model
    note: the recurrent model itself, trained before deployment
  - token: task-identifier-embedding
    note: a puzzle identifier embedding (see caveats — this turns out to be load-bearing)
leverage: computation
cost: low
evidence:
  - claim: "HRM: 40.3% on ARC-AGI-1"
    kind: claimed
    split: arc-agi-1/semi-private
    regime: uncapped
    source: https://arxiv.org/abs/2506.21734
    date: 2025-06
    stars: 1
  - claim: "HRM: 32% ARC-AGI-1, 2% ARC-AGI-2 under ARC Prize verification"
    kind: measured
    split: arc-agi-1/semi-private + arc-agi-2/semi-private
    regime: uncapped
    source: https://arcprize.org/blog/hrm-analysis
    stars: 4
    date: 2025-08-15
  - claim: "TRM: 45% ARC-AGI-1, 8% ARC-AGI-2 claimed; 40% and 6.2% measured"
    kind: measured
    split: arc-agi-1/semi-private + arc-agi-2/semi-private
    regime: uncapped
    source: https://arxiv.org/abs/2510.04871
    date: 2025-10
    stars: 3
no_absolute_score: false
caveats:
  - "ARC Prize ablation: a plain transformer lands within ~5pp of HRM; the outer refinement loop is worth +13pp; training on eval tasks recovers 31 of 41 points. The 'hierarchical reasoning' explanation is unsupported. (https://arcprize.org/blog/hrm-analysis)"
  - "Independent critique: blank or randomized puzzle-ID embeddings drop accuracy to zero, and the recursion saturates at step 1. (https://arxiv.org/abs/2512.11847)"
  - "The exact eval split behind TRM's 40% / 6.2% is not independently confirmed."
interacts:
  - technique: technique.refinement-harness
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      adaptation held in a recurrent pass against adaptation held in an orchestration loop;
      neither touches weights at test time and neither can name what it adapted
  - technique: technique.test-time-training
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      both adapt to the instance without naming a hypothesis; recurrence depth versus fitted
      weights
---

# Recursive Latent Reasoners (HRM / TRM)

**What it is.** A very small network (HRM ~27M, TRM ~7M) that recurses over a latent
state at two timescales, with adaptive halting, wrapped in an outer refinement loop.

**Why it is in the register despite the caveats.** The scores are real and the parameter
counts are startling. What is *not* supported is the story: three independent parties
converge on the finding that the recursion is not doing the work. This node exists as
much to record that separation as to recommend the technique.

**The lesson this node carries.** A capability claim and an architecture claim are
different claims. Cite this node before attributing any result to a named architectural
mechanism that has not survived an ablation. It is the register's worked example of
[schema rule 4](../SCHEMA.md): the claimed and measured entries must both be kept.
