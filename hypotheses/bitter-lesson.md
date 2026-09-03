---
id: hypothesis.bitter-lesson
kind: hypothesis
name: The Bitter Lesson
claim: >-
  General methods that leverage computation are ultimately the most effective, and by a
  large margin; the human knowledge we build into a system gives short-term gains and then
  becomes the thing that limits it.
source: http://www.incompleteideas.net/IncIdeas/BitterLesson.html
date: 2019-03-13
status: argued
stars: 1
bears_on:
  - all
predicts:
  - claim: "on any one split, later results are dominated by techniques with `leverage: computation`"
    check: build_graph.py --trend <split>
  - claim: "a capability now marked `arrival: engineered` should over time acquire a sourced `emerges_from` carrier"
    check: the gap report's arrival annotations, read across revisions
  - claim: "knowledge-side techniques should show a shrinking margin as compute grows, not a growing one"
    check: build_graph.py --trend, comparing same-split rows by leverage
history:
  - as_of: '2026-09-03'
    status: argued
    source: https://github.com/pierreb4/cognate
    note: >-
      first reading against this register's own rows rather than against the essay. Of 15
      dated ARC rows, 12 are `leverage: computation` and the highest score on every split is
      computation-side. NOT counted as support: the corpus was seeded from ARC-Prize-adjacent
      work, which is LLM-heavy, so the ratio measures what was collected as much as what
      won. A selection-corrected reading needs a sampling rule for what enters the register.
---

# The Bitter Lesson

**Why it is a node and not an axiom.** It is cited constantly, and the register's own rule
is that stars grade the evidence rather than the idea. This is an argued essay with no
reproduction attached: one star. Holding it as a node means it can be checked against the
corpus, dated, and moved — and it means an empty cell can be attributed to it explicitly
rather than by a reader's assumption.

**What it changes here.** Without it, `EMPTY` in the gap report is ambiguous between *nobody
has built a mechanism for this* and *this arrives as a byproduct of scaling something else,
so building a mechanism is the wrong move*. Those call for opposite actions. The `arrival:`
field on a capability forces the distinction, and requires a named carrier when the answer
is emergence — because "it might emerge" with no carrier is not a claim anyone can lose.

**The honest current reading.** The trend view leans computation-side, and the corpus was
collected in a way that would produce that lean whether or not the hypothesis is true. The
one row here carrying four stars is a computation-side technique being *refuted* — the ARC
Prize ablation showing that a plain transformer lands within ~5pp of HRM and that the
puzzle-identifier embedding is load-bearing. Scale winning on average and a scaling story
failing under ablation are both real, and the register should be able to hold them at once.

**What would refute it, in this corpus.** A capability whose best coverage is knowledge-side
and stays that way while compute grows around it. `exploration.experiment-design` is the
live candidate: its only `direct` member is knowledge-side, and no computation-side technique
in the register addresses it above `incidental`.
