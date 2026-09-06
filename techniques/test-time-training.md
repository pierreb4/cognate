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
  - token: trained-model
    note: >-
      a pretrained parametric model whose weights are adapted per task — every row here
      fine-tunes one (an 8B language model in Akyürek et al.; NVARC adds heavy synthetic
      pretraining, which is where `training-distribution` enters at the row level, not the
      mechanism's)
  - token: weight-gradients
    note: gradient access to the weights (rules out closed API-only models)
  - token: per-task-compute
    note: per-task inference compute
  - token: augmentation-scheme
    note: an augmentation scheme that preserves task semantics
leverage: computation
cost: low
evidence:
  - claim: "53.0% on ARC-AGI-1 public eval; 61.9% ensembled with BARC's program synthesizer"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: ~12h-per-100-tasks-1xA100
    source: https://arxiv.org/abs/2411.07279v2
    date: 2025-03-25
    stars: 2
  - claim: "53.5% — winning Kaggle 2024 entry"
    kind: measured
    split: arc-agi-1/kaggle-private-2024
    regime: kaggle-2024-compute-limit
    source: https://github.com/da-fr/arc-prize-2024
    stars: 3
    date: 2024
  - claim: "16.53% (ARChitects, 2D masked-diffusion LM + self-refinement)"
    kind: measured
    split: arc-agi-2/kaggle-private-2025
    regime: kaggle-2025-cost-cap-~$0.20/task
    source: https://arcprize.org/blog/arc-prize-2025-results-analysis
    stars: 3
    date: 2025-12-05
  - claim: "24.03% (NVARC — TTT plus heavy synthetic pretraining data)"
    kind: measured
    split: arc-agi-2/kaggle-private-2025
    regime: kaggle-2025-cost-cap-~$0.20/task
    source: https://arcprize.org/blog/arc-prize-2025-results-analysis
    stars: 3
    date: 2025-12-05
  - claim: "33.89% on the ARC-AGI-2 Kaggle 2026 PUBLIC leaderboard, provisional until the private rerun after the 2026-11-02 deadline (results 2026-12-04): the open 'Failed in AIMO' notebook and its forks, ranks 9-20 at the read date, run the ARChitects/NVARC recipe — a Qwen-family ~4B model fine-tuned per task with LoRA on augmented demonstrations inside the scored kernel, a depth-first decoder, and product-of-experts reranking across augmentations"
    kind: measured
    split: arc-agi-2/kaggle-public-2026
    regime: kaggle-2026-4xL4-12h-offline
    source: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard
    stars: 2
    date: 2026-09-06
no_absolute_score: false
caveats:
  - "The 61.9% is NOT this technique alone: it is an acknowledged joint submission with the BARC team (arXiv 2411.02272), TTT applied inside BARC's pipeline with their induction model used as-is. Attribute the ensembled figure to the pair, never to TTT (https://arxiv.org/html/2411.07279v2)."
  - "The published latest version disagrees with itself on that number: the abstract says 61.9%, Table 1's cell says 62.8%, and the v1 table said 61.875%. Only 61.875% is expressible on the paper's own denominator (247.5/400; 0.628 x 400 = 251.2 is not a half-task multiple). Cite 61.9% from the abstract and expect the table to differ."
  - "Do not read this paper's 42.2% -> 73.5% solved-set statistic as complementarity. The authors' own gloss is the opposite: TTT 'significantly improves the neural model's ability to learn systematic reasoning patterns SIMILAR TO those captured by program synthesis models' — convergence, not disjointness. The complementarity finding it is often confused with belongs to arXiv 2411.02272 and is held on the `composes` edge between `technique.llm-sampling-program-synthesis` and `technique.transductive-output-prediction`."
  - "ARC-AGI-2 training data contains ARC-AGI-1 eval data; any system trained on AGI-2 train and scored on AGI-1 eval is inflated (flagged in the TRM README)."
  - "The 2024 and 2025 numbers are under different cost regimes and different benchmarks — they do not form a trend line."
  - "The 2026 row is a PUBLIC leaderboard number, read 2026-09-06 with the Kaggle CLI, and it is `measured` at two stars deliberately: Kaggle scores it on the hidden set, so it is not self-reported, but the private result lands only after the 2026-11-02 deadline (https://arcprize.org/competitions/2026), and the entries at the same score are reruns of one public notebook (https://www.kaggle.com/code/koushikrudra/failed-in-aimo), not an independent reproduction of the method. The regime is read from that notebook's own code — `global_end_time = time.time() + 12 * 3600 - 600` and a comment stating L4 22GB x4, offline — because the Kaggle rules page is rendered client-side and was not fetched."
  - "The top of the 2026 ARC-AGI-2 public board is NOT this row and is not attributable to any technique: rabbithole 73.33 and nvbanana 72.08 (PUBLIC LB, provisional, read 2026-09-06, https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard) publish no method. nvbanana is the NVARC team, whose 2025 winner was 'A synthetic-data-driven ensemble of an improved Architects-style test-time-trained model and TRM-based components that reaches ~24% on ARC-AGI-2 under contest constraints' (https://arcprize.org/blog/arc-prize-2025-results-analysis) — a prior about the team, not a description of the 2026 entry. For scale, the same post gives the 2025 Kaggle private SOTA: 'The top Kaggle score winner reached a new SOTA on the ARC-AGI-2 private dataset of 24% for $0.20/task.'"
interacts:
  - technique: technique.transductive-output-prediction
    rel: composes
    scope: modeling.per-task-adaptation
    note: >-
      TTT is an operator applied to a transductive model, and the pair is a measured
      combination: arXiv 2411.02272 Table 2 fine-tunes one direct output predictor per task
      and reports the operator's gain on the same model, same split, same budget. The
      substrate alone is amortized adaptation (`partial` here); with the operator the fit is
      per instance
    evidence:
      - claim: "29.125% -> 39.25% on the 400-task ARC-AGI-1 public validation set from adding test-time training to the same transductive model, no reranking in either arm (Table 2, ARC-Potpourri, 'Transduction (no TTT, no reranking)' vs 'Transduction (TTT, no reranking)'); with reranking in both arms 35.25% -> 43.00%"
        kind: claimed
        split: arc-agi-1/public-eval
        regime: uncapped-2-tries-beam-20
        source: https://arxiv.org/abs/2411.02272v4
        date: 2024-11
        stars: 2
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
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
