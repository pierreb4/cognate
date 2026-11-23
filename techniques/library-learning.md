---
id: technique.library-learning
kind: technique
name: Library Learning (Wake-Sleep Abstraction)
addresses:
  - capability: modeling.hypothesis-formation
    strength: direct
    note: each solved task is held as one executable program over the current library, refutable by its examples; the library makes deeper compositions short enough to reach
  - capability: learning.cross-episode-improvement
    strength: incidental
    note: >-
      the mechanism carries an explicit library, abstracted from its own solutions, from task
      to task, and a frozen library lifts search on held-out tasks; but every published run
      learns on a provided train split, the shape this cell excludes for task RL, so it would
      grade higher only when run on a deployed system's own stream
requires:
  - token: dsl-primitives
    note: a base language whose programs have a countable description length to compress
  - token: search-procedure
    note: an enumerative or model-guided search that finds programs for the wake phase
  - token: per-candidate-executor
    note: programs run against each task's examples, so a found program is checked for free
  - token: training-distribution
    note: a corpus of related tasks sharing structure, varied enough for reuse to exist
  - token: per-task-compute
    note: search per task in every wake phase, repeated over many cycles
  - token: solution-in-span
    note: solutions lie in the span of the base language; abstraction shortens them, it does not widen the span
leverage: both
cost: low
evidence:
  - claim: "SyGuS 2017 text editing: 3.7% solved before learning, 79.6% after, trained on 128 generated tasks"
    kind: claimed
    split: sygus-2017/text-editing-108-problems
    regime: 10-min-search-per-task
    source: https://arxiv.org/abs/2006.08381
    stars: 2
    date: 2020-06
    requires_beyond: [trained-model]
  - claim: "84.3% on the same 108 problems under the competition's conditions, against 82.4% for CVC4, the competition's best"
    kind: claimed
    split: sygus-2017/text-editing-108-problems
    regime: 1h-and-8-CPUs-per-problem
    source: https://arxiv.org/abs/2006.08381
    stars: 2
    date: 2020-06
    requires_beyond: [trained-model]
  - claim: "93% of 60 physics laws and identities learned after 8 wake/sleep cycles, from map, fold and arithmetic only (solved set, not held out)"
    kind: claimed
    split: dreamcoder/physics-laws-60
    regime: 8-wake-sleep-cycles
    source: https://arxiv.org/abs/2006.08381
    stars: 2
    date: 2020-06
    requires_beyond: [trained-model]
  - claim: "LOGO graphics and towers: no ablation (no recognizer, no abstraction) or baseline exceeds 60% of held-out tasks; the full system nearly 100%"
    kind: claimed
    split: dreamcoder/logo-graphics-and-towers-held-out
    regime: 20-wake-sleep-cycles
    source: https://arxiv.org/abs/2006.08381
    stars: 2
    date: 2020-06
    requires_beyond: [trained-model]
  - claim: "LILO mean test solve rate 77.07 / 96.76 / 48.95% (REGEX / CLEVR / LOGO, 3 seeds); LLM solver alone 76.13 / 88.67 / 32.13; LLM solver plus enumeration 76.60 / 96.44 / 37.84; language-guided DreamCoder 43.93 / 94.50 / 28.53"
    kind: claimed
    split: lilo/regex-clevr-logo-test-online
    regime: codex-4-prompts-x-4-samples-per-task-plus-enumeration-96-CPU
    source: https://arxiv.org/abs/2310.19791
    stars: 2
    date: 2023-10
    requires_beyond: [llm-inference]
  - claim: "Stitch abstractions handed unnamed to the LLM solver: mean change -22.93 / -2.91 / -11.11 points against the LLM solver alone; adding AutoDoc names recovers +9.73 / +2.27 / +0.00"
    kind: claimed
    split: lilo/regex-clevr-logo-test-online
    regime: codex-4-prompts-x-4-samples-per-task
    source: https://arxiv.org/abs/2310.19791
    stars: 2
    date: 2023-10
    requires_beyond: [llm-inference]
  - claim: "Frozen final library, enumeration only, no language: LILO's library +42.27 / +63.43 / +40.24 points over the base DSL, DreamCoder's +19.60 / +62.46 / +29.73"
    kind: claimed
    split: lilo/regex-clevr-logo-test-offline
    regime: fixed-enumeration-budget-per-domain
    source: https://arxiv.org/abs/2310.19791
    stars: 2
    date: 2023-10
    requires_beyond: [llm-inference]
  - claim: "Stitch: 3-4 orders of magnitude faster and 2 orders less memory than DreamCoder's compressor, at comparable or better compression"
    kind: claimed
    split: dreamcoder-library-learning-corpora/5-domains
    regime: stitch-1-thread-vs-dreamcoder-8-CPUs
    source: https://arxiv.org/abs/2211.16605
    stars: 2
    date: 2022-11
no_absolute_score: false
caveats:
  - "Against an LLM proposer plus enumeration, LILO's full loop adds +0.47 / +0.32 / +11.11 points (Table 1 means) with LILO stds of 14.14 / 3.12 / 22.15 over 3 seeds: the library's own contribution is within run spread (https://arxiv.org/abs/2310.19791)."
  - "LILO without enumeration, library named by AutoDoc, stays below the bare LLM solver on all three domains (62.93 / 88.03 / 21.02 against 76.13 / 88.67 / 32.13) (https://arxiv.org/abs/2310.19791)."
  - "LILO's prose gives -30.60 for the REGEX unnamed-library drop, which equals the max-column difference, and +43.24 for offline LOGO; Table 1's means give -22.93 and +40.24, and the rows use the means (https://arxiv.org/abs/2310.19791)."
  - "For the library's share: DreamCoder's Memorize baselines keep whole solutions without compressing, and the full system 'always solves the most held-out tasks' (https://arxiv.org/abs/2006.08381); offline, LILO's in-loop library beats one derived post hoc from the LLM solver plus enumeration, 64.27 / 92.56 / 41.14 against 55.67 / 89.00 / 27.63 (https://arxiv.org/abs/2310.19791)."
  - "DreamCoder attributes its gain to library and recognizer together and says the recognizer yields deeper libraries; the split between them is only in Fig. 6, not stated as numbers (https://arxiv.org/abs/2006.08381)."
  - "Compute: training to convergence typically takes about a day on 20-100 CPUs, growing a functional programming library from 1959 Lisp primitives roughly five days on 64 CPUs, and the origami library approximately a year of total CPU time (https://arxiv.org/abs/2006.08381)."
  - "Stitch is scored on corpus compressivity, time and memory, never on tasks solved; it matches syntax only and cannot learn higher-order abstractions, so on the list domain it 'sometimes loses out' to DreamCoder (https://arxiv.org/abs/2211.16605)."
  - "LILO's three domains are all language-annotated and Stitch is the compressor in every library arm, including its DreamCoder baseline (https://arxiv.org/abs/2310.19791)."
interacts:
  - technique: technique.dsl-search
    rel: supplies
    scope: dsl-primitives
    note: >-
      the learned library is a primitive set a plain enumerator can search; LILO's offline
      runs search a frozen library with no language and beat the base DSL on all three domains
  - technique: technique.llm-sampling-program-synthesis
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      LILO measures the pair: against an LLM proposer plus enumeration the library adds
      +0.47 / +0.32 / +11.11 points within its 3-seed spread, so the edge stays overlaps
  - technique: technique.modality-driven-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both search for a program account; one widens the space by representation, the other
      shortens deep programs by abstraction, and no source measures the two together
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both hold an explicit, refutable account over a vocabulary; the library grows its
      vocabulary from its own solutions, the identifier never does
  - technique: technique.optional-world-model-tooling
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a program held for every solved task against one written at the agent's option —
      `direct` against `partial`
  - technique: technique.solver-trace-distillation
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both start from an authored space; distillation memorizes a fixed solver's catalog,
      library learning extends the space itself from what it solved
  - technique: technique.test-time-digital-twin
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both hold the account as a program; the twin is free code repaired against one
      environment's log, the library a reusable vocabulary built across many tasks
provenance:
  entered: 2026-11-23
  frame: claude-x-dreamcoder-map-2026-11
  note: >-
    surfaced by a cross-project map of LLM-agent work against the DreamCoder class of
    library learners (wake search, sleep abstraction, sleep dreaming), which found no node
    for library learning in this register
---

# Library Learning (Wake-Sleep Abstraction)

**Context.** DreamCoder, then Stitch and LILO. A system meets many related tasks in one
domain, each solvable by a program in a base language. It alternates a wake phase that
searches for programs with a sleep phase that refactors shared structure out of the found
programs into named functions, so later programs in the grown library are shorter and easier
to find. DreamCoder adds a recognizer trained on replays and dreamed tasks; Stitch makes the
abstraction step fast; LILO proposes programs with an LLM and names the abstractions with
it (AutoDoc).

**Problem.** The register's program-synthesis nodes search each task in a space that does
not grow from what was solved; one evolutionary run (Pang) keeps solved sub-programs, but no
node grades a mechanism that refactors them into a reusable language. What one task taught
is otherwise lost to the next unless it lives in weights.
`learning.cross-episode-improvement` had no technique at all.

**Therefore.** Reach for it where programs execute cheaply, have a countable length, and
many tasks share structure: the library is the carried knowledge, inspectable and usable by
a plain enumerator (LILO's offline rows). Pair it with a strong proposer and test whether the
library adds anything beyond it: in LILO's comparison the margin is small and noisy.

**The limit.** The gains are measured on curated, related task corpora with a base language
chosen to fit. LILO says much of DreamCoder's search goes to rediscovering abstractions
programmers already know, which an LLM proposer supplies; unnamed abstractions hurt its LLM
solver, and the full loop's margin over LLM plus enumeration sits inside three-seed spread.
Stitch's evaluation scores compression and speed, not tasks solved, and the pure symbolic
loop costs CPU-days to CPU-years.
