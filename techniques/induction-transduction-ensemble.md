---
id: technique.induction-transduction-ensemble
kind: technique
name: Induction / Transduction Ensembling
addresses:
  - capability: modeling.hypothesis-formation
    strength: partial
    note: shows the representation choice is not a detail — induced programs and directly predicted outputs succeed on different tasks
requires:
  - two models trained on the same task distribution with different output types
  - a synthetic task generator large enough to train both
  - a rule for combining or selecting between the two
cost: high
evidence:
  - claim: "56.75% combined on ARC-AGI-1 validation; 38.0% induction alone, 43.0% transduction alone"
    kind: claimed
    split: arc-agi-1/validation
    regime: uncapped
    source: https://arxiv.org/abs/2411.02272
    stars: 2
no_absolute_score: false
caveats:
  - "The headline is not the combined number. It is that the two approaches solve substantially DISJOINT task sets — the ensemble gain comes from non-overlap, not from either method being better."
related: [technique.llm-sampling-program-synthesis, technique.test-time-training]
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
