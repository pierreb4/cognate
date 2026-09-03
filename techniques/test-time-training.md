---
id: technique.test-time-training
kind: technique
name: Test-Time Training
addresses:
  - capability: modeling.per-task-adaptation
    strength: direct
    note: fits parameters to the specific task instance at inference, from its own demonstrations
  - capability: modeling.hypothesis-formation
    strength: incidental
    note: the hypothesis is held in weights and cannot be named, inspected, or refuted
requires:
  - token: weight-gradients
    note: gradient access to the weights (rules out closed API-only models)
  - token: per-task-compute
    note: per-task inference compute
  - token: augmentation-scheme
    note: an augmentation scheme that preserves task semantics
cost: high
evidence:
  - claim: "53.0% on ARC-AGI-1 public eval (61.9% ensembled)"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: uncapped
    source: https://arxiv.org/abs/2411.07279
    stars: 2
  - claim: "53.5% — winning Kaggle 2024 entry"
    kind: measured
    split: arc-agi-1/kaggle-private-2024
    regime: kaggle-2024-compute-limit
    source: https://github.com/da-fr/arc-prize-2024
    stars: 3
  - claim: "16.53% (ARChitects, 2D masked-diffusion LM + self-refinement)"
    kind: measured
    split: arc-agi-2/kaggle-private-2025
    regime: kaggle-2025-cost-cap-~$0.20/task
    source: https://arcprize.org/blog/arc-prize-2025-results-analysis
    stars: 3
  - claim: "24.03% (NVARC — TTT plus heavy synthetic pretraining data)"
    kind: measured
    split: arc-agi-2/kaggle-private-2025
    regime: kaggle-2025-cost-cap-~$0.20/task
    source: https://arcprize.org/blog/arc-prize-2025-results-analysis
    stars: 3
no_absolute_score: false
caveats:
  - "ARC-AGI-2 training data contains ARC-AGI-1 eval data; any system trained on AGI-2 train and scored on AGI-1 eval is inflated (flagged in the TRM README)."
  - "The 2024 and 2025 numbers are under different cost regimes and different benchmarks — they do not form a trend line."
---

# Test-Time Training

**What it is.** Rather than asking a fixed model to answer, fit the model *to this task*
at inference: generate augmented variants of the task's own demonstration pairs, take a
small number of gradient steps (typically LoRA), then predict.

**The cognate.** This is the machine counterpart of within-task skill acquisition —
adapting to a novel problem by practising on it — and it is the technique family that
most directly attacks Chollet's *skill-acquisition efficiency* definition rather than
his *knowledge coverage* bound. That is why it dominated the 2024 leaderboard.

**Where it stops.** The adapted hypothesis lives in weights. Nothing downstream can read
it, contradict it, or design an experiment against it, which is why it scores only
`incidental` on [`modeling.hypothesis-formation`]. TTT gets you a system that has
adapted, not a system that can say what it now believes.

**Reading the numbers.** The four evidence rows span two benchmarks and three cost
regimes. The 2025 rows are under a roughly $0.20/task Kaggle cap; the 2024 rows are not
comparable to them, and neither is comparable to uncapped verified-leaderboard results.
