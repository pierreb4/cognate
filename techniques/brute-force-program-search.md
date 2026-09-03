---
id: technique.brute-force-program-search
kind: technique
name: Brute-Force DAG Search
addresses:
  - capability: modeling.hypothesis-formation
    strength: incidental
    note: enumerates compositions rather than committing to an account; nothing downstream can be told what the system currently believes
requires:
  - token: dsl-primitives
    note: a small closed set of primitive operations
  - token: compiled-implementation
    note: a fast, typically compiled, implementation
  - token: per-task-compute
    note: a compute budget that scales with the composition depth you want
leverage: both
cost: medium
evidence:
  - claim: "20% on the ARC-AGI-1 2020 Kaggle private leaderboard"
    kind: measured
    split: arc-agi-1/kaggle-private-2020
    regime: kaggle-2020-compute-limit
    source: https://github.com/top-quarks/ARC-solution
    stars: 3
    date: 2020
no_absolute_score: false
caveats:
  - "The 20% is under the 2020 Kaggle compute limit on the 2020 private set; it is not on the same axis as any later leaderboard or uncapped result."
interacts:
  - technique: technique.dsl-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both enumerate compositions of a fixed primitive set; running both buys coverage only
      where the two primitive sets differ
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Brute-Force DAG Search

**What it is.** icecuber's 2020 Kaggle winner. 142 unary grid operations, greedily
composed into a directed acyclic graph of intermediate grids, with the output assembled
from pieces of that graph. No learning of any kind.

**Why it stays in the register.** It is the honest floor. Any technique that invokes
learning, pretraining, or reasoning should be asked what it buys over 142 hand-written
operations and a fast loop — a comparison that is rarely made because the two are usually
reported under incompatible regimes.

**Why `incidental` on hypothesis formation.** Enumeration is not commitment. The system
never holds a specific falsifiable account, so there is nothing for an experiment to
discriminate and nothing for a belief update to revise. It reaches an answer without ever
having had a theory.

**The limit.** It scales with the primitive set and the depth, and both are capped by the
compute budget rather than by any insight — which is why the approach plateaued rather
than being refuted.
