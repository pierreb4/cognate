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
  - claim: "on a population this register did not select, the top of the leaderboard should pass from purpose-built systems to general models"
    check: >-
      arcprize.org/leaderboard, grouping by its own SYSTEM TYPE column and reading the
      top score per split per year. The external check exists because the three above
      are computed over a corpus we curated; run build_graph.py --provenance first and
      read that frame before reading them.
history:
  - as_of: '2026-09-03'
    status: argued
    source: https://github.com/pierreb4/cognate
    note: >-
      first reading against this register's own rows rather than against the essay. Of 16
      dated ARC rows, 12 are `leverage: computation`, 4 are `both`, none are knowledge-side,
      and the highest score on every split is computation-side. (Was 15 rows before the
      Berman ARC-AGI-2 row was dated on 2026-09-03; the row it gained is `both`, so the
      computation share fell from 12/15 to 12/16.) NOT counted as support: the corpus was
      seeded from ARC-Prize-adjacent work, which is LLM-heavy, so the ratio measures what
      was collected as much as what won.
  - as_of: '2026-09-03'
    status: argued
    source: https://github.com/pierreb4/cognate
    note: >-
      the frame is now MEASURED rather than gestured at. `build_graph.py --provenance`:
      62% of the corpus (18 of 29 nodes, 11 of the 16 techniques) entered through one
      instrument — the ARC Prize 2025 report's refinement-loop taxonomy — and 34% more
      through four catalogue works chosen to exercise the format. A taxonomy of ARC
      entries in 2024-25 is LLM-heavy by construction, so a computation-side lean in the
      three checks above is PREDICTED BY THE FRAME and cannot corroborate this node.
      Those checks stay, scoped as claims about the register; they are not evidence about
      the field. Deliberately NOT fixed by a sampling rule: this is a curated pattern
      language, and a frame keyed to published results would drop 7 of 16 techniques —
      including dsl-search, HTN and means-ends-analysis, three of the six the arc-agi-3
      profile admits. Declaring the frame is the cheaper and more honest instrument.
  - as_of: '2026-09-03'
    status: argued
    source: https://arcprize.org/leaderboard
    note: >-
      FIRST READING ON A POPULATION WE DID NOT SELECT, and the first that can bear on the
      field rather than on us. The ARC Prize leaderboard maintains its own SYSTEM TYPE
      column (CoT / Base LLM / Custom / Refinement / CoT+Synthesis), so the typology is
      not ours either. The top of both splits has passed from `Custom` purpose-built
      systems to `CoT` general models: ARC-AGI-1 goes Icecuber 17.0% (Custom, 2023-11) ->
      ARChitects 56.0% (Custom, 2024-11) -> o3 preview 75.7% (CoT+Synthesis, 2024-12) ->
      Claude Fable 5 98.5% (CoT, 2026-06); on ARC-AGI-2 the best `Custom` entry is NVARC
      at 27.6% against GPT-5.6 Sol at 92.5% (CoT, 2026-07). Directionally this supports
      the node. TWO CAVEATS THAT STOP IT BECOMING A THIRD STAR. (1) Budget confound,
      partly answered: `Custom` entries run under the Kaggle cap (~$0.20/task) while CoT
      entries do not, so the raw comparison confounds leverage with spend — but DeepSeek
      V4 Flash 0731 (CoT) reaches 61.4% on ARC-AGI-2 at $0.042/task, a fifth of the cap,
      so the gap is not bought by budget. (2) That iso-cost pair is NOT split-matched:
      NVARC's 27.6% is the 2025 Kaggle private set and DeepSeek's 61.4% is semi-private,
      which the leaderboard shows in one column. Indicative, not matched. The leaderboard
      is also itself selected — verified submissions only, and its own note says "Only
      systems which required less than $10,000 to run are shown."
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
collected in a way that would produce that lean whether or not the hypothesis is true —
`build_graph.py --provenance` now puts a number on it: 62% of the register entered through
a taxonomy of ARC entries, which is LLM-heavy by construction. So the internal checks are
claims about the register, and the leaderboard reading in `history` is the first one that
bears on the field. The
one row here carrying four stars is a computation-side technique being *refuted* — the ARC
Prize ablation showing that a plain transformer lands within ~5pp of HRM and that the
puzzle-identifier embedding is load-bearing. Scale winning on average and a scaling story
failing under ablation are both real, and the register should be able to hold them at once.

**What would refute it, in this corpus.** A capability whose best coverage is knowledge-side
and stays that way while compute grows around it. `exploration.experiment-design` is the
live candidate: its only `direct` member is knowledge-side, and no computation-side technique
in the register addresses it above `incidental`.
