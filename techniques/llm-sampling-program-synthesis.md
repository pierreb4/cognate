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
no_absolute_score: false
caveats:
  - "A widely-circulated 43% figure attributed to the semi-private set has no primary source pairing that number with that set; it is not entered here."
  - "The result is a sample-budget result. Read it against the regime field, not against cost-capped leaderboard entries."
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
