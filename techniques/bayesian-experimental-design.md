---
id: technique.bayesian-experimental-design
kind: technique
name: Bayesian Experimental Design (Monte Carlo EIG Question Selection)
addresses:
  - capability: exploration.experiment-design
    strength: direct
    note: >-
      each candidate question is scored by its expected information gain over a sampled set of
      hypotheses (possible ship boards) and the best is asked, so a question every live
      hypothesis answers alike scores zero and is not chosen — the cell's quantity, computed
      explicitly; it holds only where the hypothesis space can be enumerated and sampled
requires:
  - token: solution-in-span
    note: >-
      the hypothesis space is enumerable and sampleable (the set of possible ship boards);
      where it is open, nothing here says how to sample it
  - token: llm-inference
    note: the language model the selector runs on (Llama-4-Scout in the row below), which asks the questions and takes the shots
  - token: per-task-compute
    note: Monte Carlo samples of the hypothesis space for every question scored
leverage: both
cost: low
evidence:
  - claim: "Llama-4-Scout with Monte Carlo Bayesian experimental design: win rate against human captains 8% -> 82% and against GPT-5 0% -> 67%, at ~1% of GPT-5's cost; its questions reach 94.2% of the expected-information-gain noise ceiling"
    kind: claimed
    split: collaborative-battleship/battleshipqa
    regime: llama-4-scout-plus-monte-carlo-bed-~1pct-of-gpt-5-cost
    source: https://arxiv.org/abs/2510.20886
    stars: 2
    date: 2025-10-23
    human_baseline:
      n: 42
      population: human players in the BattleshipQA dataset; their recorded games, not live play
      aggregation: individual-mean
      same_items: true
      source: https://arxiv.org/abs/2510.20886
      note: the win rate is head-to-head against recorded human games, and the authors note that people are not Bayes-optimal question askers
no_absolute_score: false
caveats:
  - "The precondition does the work. Ship boards can be enumerated and sampled, so expected information gain can be computed by Monte Carlo; this is `solution-in-span` in the register's terms. Where the hypothesis space is open the result does not carry: in ZendoWorld 'VLM-based agents propose near-uninformative experiments', and the best agent wins 45.5% against 73.3% for people (https://arxiv.org/abs/2607.08233)."
  - "The authors report the gain replicates on Guess Who? (+28.3 to 42.4 points); the replication is theirs, so it does not count toward a third star."
  - "The hypothesis space is the designer's, made sampleable for the game, and the language model works inside it. That is why `leverage` is `both` rather than `computation`."
interacts:
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: exploration.experiment-design
    note: >-
      both choose the action whose outcome splits the live hypotheses; DOORMAX reads the split
      off condition-effect predictions that are still unknown, this computes expected
      information gain over sampled hypotheses, and both need the hypothesis space handed to
      them in a form they can enumerate, so holding both does not buy two selectors
provenance:
  entered: 2026-10-20
  commit: a382939
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Bayesian Experimental Design (Monte Carlo EIG Question Selection)

**What it is.** Hold a set of hypotheses about the hidden state, sampled from the space of
possibilities. For each candidate question, estimate by Monte Carlo how much its answer would
shrink that set (its expected information gain), ask the best one, condition the samples on
the answer, and repeat. In Collaborative Battleship the selector runs on Llama-4-Scout, which
asks the questions and takes the shots.

**The cognate.** [`exploration.experiment-design`] in its textbook form: the action is chosen
because its outcome discriminates between the hypotheses held, and the quantity is computed,
not prompted for. It is the first member of that cell measured against people: a small model
with the selector beats human captains and GPT-5, at about 1% of GPT-5's cost.

**Therefore.** Where the hypotheses can be enumerated and sampled, do not leave it to a
language model to judge which question is informative; compute it.

**The limit.** Everything rests on the enumerable space. Battleship's boards are a closed,
sampleable set; an environment whose rules are unknown is not, and there agents still choose
near-uninformative experiments. The cell's open part is that case, which is why it reads
`partial` and not `covered`.
