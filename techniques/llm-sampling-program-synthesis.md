---
id: technique.llm-sampling-program-synthesis
kind: technique
name: Program Synthesis by LLM Sampling
addresses:
  - capability: modeling.hypothesis-formation
    strength: direct
    note: each sample is a named, executable program — a specific account that the demonstration pairs can refute
  - capability: modeling.belief-update
    strength: incidental
    note: rejection against the demonstrations filters the pool; no sample is ever revised in light of why it failed
requires:
  - token: llm-inference
    note: a frontier model with strong code generation
  - token: per-candidate-executor
    note: an executor that can run candidate programs against the demonstration pairs
  - token: per-task-compute
    note: a per-task sample budget in the thousands
leverage: computation
cost: high
evidence:
  - claim: "50% on ARC-AGI-1 public eval with GPT-4o, ~8k Python programs sampled per task"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: uncapped-~8k-samples-per-task
    source: https://blog.redwoodresearch.org/p/getting-50-sota-on-arc-agi-with-gpt
    stars: 2
    date: 2024-06-17
  - claim: "38.00% on the ARC-AGI-1 public validation set with a Llama-3.1-8B-instruct generator fine-tuned on 400k synthetic problems — 20k samples per task, filtered on the demonstration pairs, majority vote over execution results (BARC induction model, Table 2, ARC-Potpourri)"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: uncapped-20k-samples-per-task
    source: https://arxiv.org/abs/2411.02272v4
    date: 2024-11
    stars: 2
    requires_beyond: [trained-model, training-distribution, weight-gradients]
  - claim: "4% on the ARC Prize 2024 Kaggle private test set with the same generator at 384 samples per task; 14% on the public validation set at that budget (Table 3)"
    kind: claimed
    split: arc-agi-1/kaggle-private-2024
    regime: kaggle-2024-compute-limit-384-samples-per-task
    source: https://arxiv.org/abs/2411.02272v4
    date: 2024-11
    stars: 2
    requires_beyond: [trained-model, training-distribution, weight-gradients]
no_absolute_score: false
caveats:
  - "A widely-circulated 43% figure attributed to the semi-private set has no primary source pairing that number with that set; it is not entered here."
  - "The result is a sample-budget result. Read it against the regime field, not against cost-capped leaderboard entries."
  - "The 38.00% and 4% rows are a fine-tuned 8B generator, not a prompted frontier model. They sit on this node because the paper places them here itself — 'Comparable to our induction model, but instead of fine-tuning, it uses prompting' (§7) — and `requires_beyond` records what the fine-tuning cost. 4% against 14% at the same 384-sample budget, and 38.00% at 20k, is the sample-hunger of the mechanism measured on one model (Figure 8, near-monotone in samples)."
  - "A bound on the `candidate-arbiter` precondition from AIMO3 (olympiad math, 50 private problems — NOT ARC): the host's tool-free sampling puts gpt-oss-120b at pass@20 ≈ 45.5 and pass@100 ≈ 49/50 on the private set, while the best majority-vote-over-8 score in the independent ablation is 42/50; the paper names the gap 'selection loss: the correct answer appears in the N =8 pool but is outvoted by a more common wrong one' (arXiv 2603.27844 §9, https://arxiv.org/abs/2603.27844, citing the host post https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/679559). It bears on this node because the executor only filters; the moment no sample reproduces every demonstration pair the arbiter is a vote, and the selector, not the generator, is the bottleneck once the answer is in the pool."
  - "Under a wall-clock cap more samples per task scored lower: gpt-oss-20b at N=8 reached 31.0 on the AIMO3 public leaderboard against 26 at N=32 — 'per-attempt time shrinks, p̂ drops from 0.61 to 0.52, score drops from 31.0 to 26' (Table 3, https://arxiv.org/abs/2603.27844); the 3rd-place team reports the same direction going from 8 to 16 solver runs, 'leading to an overall increase in errors' (https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/writeups/3rd-place-solution-for-the-aimo3-competition). Sample budgets in this node's regime fields are token budgets, not wall-clock ones; do not read them across."
  - "Prompt-diversity mixers did not decorrelate errors: pairwise error correlation between attempts was already negative at T=1.0 (mean ρ̂ = −0.122 for N ≥ 7) and every mixed-strategy configuration scored at or below the single-prompt baseline — 'More diversity = worse performance' (Table 1, §4.2, https://arxiv.org/abs/2603.27844). Diversity-by-prompt is not a substitute for a selector."
  - "Entropy-weighted voting, used by every top AIMO3 entry, has no ablated gain over plain majority in the one ablation that isolates it: the Qwen3.5-35B-A3B table lists 'Entropy voting' at 8/10, equal to the 8/10 baseline (Table 4, https://arxiv.org/abs/2603.27844). Treat the weighting as unproven."
interacts:
  - technique: technique.modality-driven-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      modality-driven search contains this as its code arm; it scores lower here because
      arbitrating across representations does not itself commit to a named account
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a sampled program against an identified rule set; the sample is drawn from a prior over
      human code, the rule from the transitions actually observed
  - technique: technique.evolutionary-program-synthesis
    rel: supplies
    scope: mutation-operator
    note: >-
      a language model asked to revise a failing program IS a mutation operator over the
      program representation, which is the precondition the evolutionary family names and
      does not otherwise supply
  - technique: technique.test-time-digital-twin
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      the nearest kin in the register: a Python program an executor refutes, in both;
      thousands of independent draws against demonstration pairs in one, a single program
      replayed against every logged transition and repaired in the other — repair is a
      belief-update distinction, and on this cell the committed object is the same kind
  - technique: technique.transductive-output-prediction
    rel: composes
    scope: modeling.hypothesis-formation
    note: >-
      the register's one measured representation-union: a fine-tuned program generator
      (this node's 38.00% row) and a direct output predictor (43.00%, with TTT and
      reranking stacked) solve substantially disjoint task sets, and the induction-first /
      transduction-fallback rule (eq. 5: sample programs, keep those that reproduce every
      demonstration pair, fall back to the predictor only when none does) reaches 56.75%.
      What adds is tasks solved, not this cell's grade — the transductive arm is
      `incidental` here by the exhibitable-commitment rule, so the pair's coverage of
      hypothesis-formation stays at this node's `direct`; nothing here predicts which
      representation a given task needs
    evidence:
      - claim: "56.75% ensemble vs 38.00% induction alone vs 43.00% transduction alone (TTT + reranking), ARC-AGI-1 public validation, 2 tries (Table 2, ARC-Potpourri); 37.50% vs 30.50% vs 19.25% with no TTT anywhere (Table 2, ARC-Heavy); 19% vs 4% vs 18% on the Kaggle 2024 private set at 384 samples / beam 3, no TTT (Table 3)"
        kind: claimed
        split: arc-agi-1/public-eval
        regime: uncapped-2-tries
        source: https://arxiv.org/abs/2411.02272v4
        date: 2024-11
        stars: 2
      - claim: "the disjointness is stable across random seeds — solved sets correlate within a class and not across it (Figure 5B, 5C); 26.50% ensemble vs 18.78% / 15.25% at the 100k-problem scale (Table 1)"
        kind: claimed
        split: arc-agi-1/public-eval
        regime: 100k-synthetic-problems
        source: https://arxiv.org/abs/2411.02272v4
        date: 2024-11
        stars: 2
  - technique: technique.solver-trace-distillation
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      thousands of independent programs filtered by an executor against one scripted enumeration
      with in-trace checks; the sampled program is a fresh account each draw, the distilled trace
      re-emits an authored one
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Program Synthesis by LLM Sampling

**What it is.** Ask a frontier model for a Python program that maps the input grids to the
output grids, thousands of times per task, and keep any sample that reproduces every
demonstration pair.

**The cognate.** Generate-and-test, with the generator carrying the prior instead of the
DSL. The model's pretraining supplies what a DSL author would otherwise have to enumerate;
the executor supplies the refutation that pure generation lacks.

**Therefore.** When you have an executable checker, spend inference compute on breadth of
candidates rather than depth of reasoning on one. The checker is what makes breadth safe.

**The limit.** The pool is drawn independently — a failed sample teaches the next sample
nothing. That gap between *filtering* a pool and *revising* an account is exactly what the
evolutionary and refinement families were built to close, and it is why this node scores
only `incidental` on [`modeling.belief-update`].
