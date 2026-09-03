---
id: technique.induction-transduction-ensemble
kind: technique
name: Induction / Transduction Ensembling
addresses:
  - capability: modeling.hypothesis-formation
    strength: partial
    note: shows the representation choice is not a detail — induced programs and directly predicted outputs succeed on different tasks
requires:
  - token: trained-model
    note: two models trained on the same task distribution with different output types
  - token: training-distribution
    note: a synthetic task generator large enough to train both
  - token: candidate-arbiter
    note: a rule for combining or selecting between the two
leverage: computation
cost: high
evidence:
  - claim: "56.75% combined on ARC-AGI-1 validation; 38.0% induction alone, 43.0% transduction alone"
    kind: claimed
    split: arc-agi-1/validation
    regime: uncapped
    source: https://arxiv.org/abs/2411.02272
    date: 2024-11
    stars: 2
no_absolute_score: false
caveats:
  - "The headline is not the combined number. It is that the two approaches solve substantially DISJOINT task sets — the ensemble gain comes from non-overlap, not from either method being better."
interacts:
  - technique: technique.llm-sampling-program-synthesis
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      the induction arm is program synthesis with a trained generator in place of a prompted
      one
  - technique: technique.modality-driven-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both run one task through two representations and arbitrate; the gain is claimed from
      non-overlap of the solved sets in each case
---

# Induction / Transduction Ensembling

**What it is.** Train two models on the same synthetic task distribution: an *inductive*
one that emits a program, and a *transductive* one that emits the output grid directly.
Run both.

**Why it is a node and not a footnote.** [`modeling.hypothesis-formation`] names the
representation choice as the branch point of the whole faculty. This work is the direct
measurement of that claim: the two representations do not merely differ in strength, they
succeed on different tasks. A per-task property decides which one can work, and no one can
yet say in advance which.

**Therefore.** Do not treat "program vs. direct prediction" as an implementation
preference to be settled once. Where budget allows, run both and let the disjointness pay.

**The limit.** Nothing here predicts *which* representation a given task needs. The
ensemble buys the union by paying for both — a coverage result, not an understanding
result.
