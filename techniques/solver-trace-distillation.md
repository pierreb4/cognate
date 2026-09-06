---
id: technique.solver-trace-distillation
kind: technique
name: Solver-Trace Distillation
addresses:
  - capability: modeling.hypothesis-formation
    strength: partial
    note: >-
      the trace commits to a named candidate transformation — an 8-rule bit sequence, an
      anchor digit mapping — and checks it against the examples before answering, so a
      commitment exists to be exhibited and refuted; capped at partial because the space of
      candidates and the order they are tried are authored by the solver writer and installed
      at training time: the model performs the check, it did not form the space
  - capability: modeling.belief-update
    strength: incidental
    note: >-
      a rejected candidate is replaced by the next catalog neighbour in a fixed
      Hamming-distance order; the content of the failure never steers the next candidate, so
      the repair is a rendered solver step, not a revision of a held account
  - capability: modeling.per-task-adaptation
    strength: incidental
    note: >-
      nothing is fitted at inference — one greedy pass, no tools, no weight update; the
      adaptation to the task family is amortized into a LoRA adapter before deployment
requires:
  - token: trained-model
    note: >-
      a small open model fine-tuned on the rendered traces — Nemotron-3-Nano-30B with a
      rank-32 LoRA in every published instance
  - token: weight-gradients
    note: the adapter is trained by supervised fine-tuning; gradient access at training time
  - token: training-distribution
    note: >-
      the load-bearing precondition: a generator for the task family that the solver writer
      can reverse-engineer and sample from — the winners rendered 27M to 890M tokens of
      traces from programmatic problem generators matched to the seven fixed puzzle
      families, and the 2nd-place write-up is titled as a solution that reverse-engineers
      the data-generation process; ARC's per-task novelty removes exactly this
  - token: expert-authored-library
    note: >-
      a human writes and maintains the deterministic solver whose execution becomes the
      trace, one per task family — the 2nd-place write-up calls trace design the more
      human-intensive part
  - token: automatic-verifier
    note: >-
      needed at trace-authoring time, not at inference — the solver checks each candidate
      against the examples so that the check, and the failed candidates before the fix, can
      be rendered into the trace the model imitates
  - token: solution-in-span
    note: >-
      the model's ceiling is the solver's ceiling within the token budget — 93.16% of
      train.csv for the 1st-place solvers against 92.00% for the trained model; a task the
      solver cannot state, the model cannot solve
leverage: knowledge
cost: low
evidence:
  - claim: "0.920 on the private leaderboard, 1st place (NullSira): cryptarithm through a memorized signature catalog plus bounded in-trace DFS, bit manipulation through nearest-neighbour repair against a memorized rule-sequence catalog with up to 32 candidates verified in-trace; LoRA rank 32 SFT on 220,000 solver-rendered traces (890.1M tokens), about 119h on one RTX PRO 6000"
    kind: measured
    split: nemotron-reasoning/kaggle-private-2026
    regime: single-greedy-pass-7680-tokens-lora-rank-32-no-tools
    source: https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/leaderboard
    stars: 3
    date: 2026-06-15
  - claim: "0.908 on the private leaderboard, 2nd place (vli): the bit-manipulation generator reverse-engineered into a grammar of 21 atoms and six binary operations, rendered as a corner-region and shift-inference trace verified bit-by-bit; 57,600 synthetic traces (159M tokens), plain cross-entropy LoRA SFT, 11h on 4x A100"
    kind: measured
    split: nemotron-reasoning/kaggle-private-2026
    regime: single-greedy-pass-7680-tokens-lora-rank-32-no-tools
    source: https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/leaderboard
    stars: 3
    date: 2026-06-15
  - claim: "0.900 on the private leaderboard, 3rd place (YS-L): SFT on deterministic solver traces designed so the answer is reached step by step with no hidden deduction, a multiplication-pattern lookup table (3,678 signatures) memorized in a first recall-drill stage before the procedure that consumes it is trained; 72,377 traces (299M tokens), 25.2h plus 32.7h on one RTX PRO 6000"
    kind: measured
    split: nemotron-reasoning/kaggle-private-2026
    regime: single-greedy-pass-7680-tokens-lora-rank-32-no-tools
    source: https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/leaderboard
    stars: 3
    date: 2026-06-15
  - claim: "two-stage memorize-then-execute ablation (3rd place): at 12K cryptarithm samples direct training solved 0/11 held-out cryptarithm problems against 7/11 for two-stage; on the full data mix, direct training solved 12/17 with private LB 0.888 against 16/17 and 0.900 for two-stage (post-competition ablation, same mix, stage-1 adapter initialization the only difference)"
    kind: claimed
    split: nemotron-reasoning/kaggle-private-2026
    regime: single-greedy-pass-7680-tokens-lora-rank-32-no-tools
    source: https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/writeups/3rd-place-solution
    stars: 2
    date: 2026-06-19
no_absolute_score: false
caveats:
  - "The headline does not transfer to ARC as a capability claim: the seven puzzle generators are fixed and shared between train and test — 'public and hidden splits share generators, so held-out data proxies test accuracy' (https://arxiv.org/abs/2606.21884) — and the memorized catalogs are generator-specific. The 1st-place write-up says of its own solver-coverage table that 'The solver design and rule extraction were done after looking at the full train.csv, so this table essentially includes leakage' (https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/writeups/1st-place-solution). What transfers is the method — memory/compute split, in-trace verification, nearest-valid repair — not the number."
  - "RL and distillation from larger models were bet against and beaten by plain cross-entropy SFT: the Open Progress Prize winner lists both under what he was betting against — 'I know reinforcement learning approaches are not necessary when you know what the optimal policy should be' (https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/689915); the 2nd-place write-up reports 'Complex training schemes did not beat simple cross-entropy loss' after trying focal loss, token loss reweighting and multi-stage schedules (https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/writeups/2nd-place-solution); Patel's RL from verifiable rewards on the cryptarithm sub-task stayed inside the same 0.01-0.07 band as every trace design (https://arxiv.org/abs/2606.21884). The competition's own rules listed reinforcement learning as an allowed approach and offered a Best RL Method award."
  - "The non-learnable-search boundary: what distills is a forward-computable procedure, not a search — 'When a procedure's only solution is search over information-free structure, no faithful forward chain-of-thought exists to imitate' and 'What distills is memorization and verification, not search' (https://arxiv.org/abs/2606.21884). The winners' move was to precompute the search's combinatorial core into a catalog the adapter memorizes and to reduce the trace to recall plus bounded verification; a task whose search cannot be precomputed is outside this technique."
  - "Leaderboard placings at the top are within noise: the 1st-place write-up reports that 'generation with temperature=0.0 was still not fully deterministic, so scores varied across repeated submissions' and that 'The best unselected submission scored 0.932 on Private LB' (https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/writeups/1st-place-solution); the private board is computed on approximately 50% of the test data (https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/leaderboard). Read the three measured rows as one result at about 0.90-0.92, not as a ranking of three mechanisms."
  - "`cost: low` is the inference cost — one greedy pass of at most 7,680 tokens on a 30B model with 3.5B active parameters. The authoring cost is a human-written solver per task family and 11h to about 170h of adapter training per entry; that cost is what `expert-authored-library` and `training-distribution` name."
interacts:
  - technique: technique.test-time-digital-twin
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a Python twin replayed against a growing transition log and repaired at test time against
      a solver replay from weights whose repair is a fixed neighbourhood walk; the twin's
      commitment is exhibited per action, the trace's once per task
provenance:
  entered: 2026-09-06
  commit: pending
  frame: kaggle-sweep-2026-09
  note: >-
    Kaggle competitions ending 2026-03..09 swept for ARC-relevant results; entered from the
    NVIDIA Nemotron reasoning challenge write-ups
---

# Solver-Trace Distillation

**What it is.** Write a deterministic solver for the task family. Render its execution as a
reasoning trace — parse, enumerate candidates, check each against the examples, show the
ones that fail, repair the survivor toward the nearest valid entry in a precomputed catalog,
apply it to the query. Fine-tune a small open model on those traces (the Nemotron winners:
LoRA rank 32 on Nemotron-3-Nano-30B, one greedy pass, no tools at inference). Optionally
split training in two: a first stage of recall drills that installs the lookup tables in the
adapter, then the procedure that consumes them.

**The cognate.** Worked-example and drill learning. Tables before procedural fluency —
the 3rd-place write-up's stage 1 is rote recall of a multiplication-pattern table, and only
then does stage 2 train the solve procedure, 0/11 to 7/11 on held-out cryptarithm at the same
sample count. And chunking: a search that cannot fit in the token budget is cut down to a
catalog of recallable entries plus a bounded check, which is the 1st-place write-up's own
phrase for the design variable — deciding what the model should memorize through synthetic
traces and what it should compute inside the trace.

**Where it stops.** The hypothesis space is the solver writer's. The trace names a
candidate and refutes it against the examples, which is a real commitment by the
[`modeling.hypothesis-formation`] rule, but the candidates, their order, and the repair
neighbourhood were authored and installed, so the cell is capped at `partial`. Nothing is
fitted at inference — `incidental` on [`modeling.per-task-adaptation`] — and the repair
walks a fixed neighbourhood rather than reading why the candidate failed, so
[`modeling.belief-update`] is `incidental` too. The binding precondition is
`training-distribution`: the winners reverse-engineered seven fixed generators shared
between train and test, and ARC's per-task novelty forbids exactly that. What is not
forward-computable does not distill at all (Patel, arXiv 2606.21884).

**Reading the numbers.** Three measured rows at 0.920 / 0.908 / 0.900 are one result, not a
ranking: the 1st-place team reports its best unselected submission at 0.932 and
non-deterministic scoring at temperature 0, and the private board is half the test set.
The claimed row is the one ablation in the set — the two-stage schedule against direct
training on the same mix — and it is the part of this node most likely to carry to another
task family. None of the numbers is an ARC number.
