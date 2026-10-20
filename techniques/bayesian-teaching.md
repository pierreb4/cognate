---
id: technique.bayesian-teaching
kind: technique
name: Bayesian Teaching
addresses:
  - capability: modeling.belief-update
    strength: partial
    note: >-
      a language model fine-tuned on a normative Bayesian updater's predictions keeps revising
      its estimate across rounds of evidence, where off-the-shelf models plateau after the
      first; `partial` because the updater it imitates is authored for the task family, and
      what is revised is a preference estimate over a fixed space, not a rich account of an
      environment
requires:
  - token: weight-gradients
    note: the language model is fine-tuned, so its weights must be open to training
  - token: training-distribution
    note: >-
      an authored normative Bayesian updater for the task family, and the interactions to
      generate its predictions on as fine-tuning targets
leverage: both
cost: low
evidence:
  - claim: "fine-tuned on a normative Bayesian assistant's predictions in a 5-round flight-recommendation task, 7-9B open models agree with it ~80% of the time and carry the behaviour to tasks they were not trained on, where off-the-shelf LLMs plateau after one round"
    kind: claimed
    split: flight-recommendation-5-round/simulated-users
    regime: fine-tuned-7-9b-open-models
    source: https://arxiv.org/abs/2503.17523
    stars: 2
    date: 2025-03-21
no_absolute_score: false
caveats:
  - "The per-model accuracies are in the paper's figures only, so the row carries the agreement rate and not an accuracy."
  - "The human comparison is in the learning curve, not the level: 500 people, on 48 of the 624 simulated users, improve significantly from round 1 to round 5 (p = 0.002), where off-the-shelf models stop after one. The models tested are a 2024-25 generation (Gemini 1.5 Pro, GPT-4.1 Mini, Gemma 2, Llama 3, Qwen 2.5)."
  - "Knowledge-side content distilled by gradients: the normative model is written by a person for one task family, so the gain is bounded by that model, and a new family needs a new one. That is why `leverage` is `both`."
interacts:
  - technique: technique.evolutionary-program-synthesis
    rel: overlaps
    scope: modeling.belief-update
    note: >-
      both revise in light of evidence; one mutates a failing program given its trace, the
      other updates an estimate the way a distilled Bayesian model would, and neither holds a
      rich account that it retracts
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.belief-update
    note: >-
      both revise a held estimate with each new observation; DOORMAX retracts a falsified
      condition outright under determinism, this shifts a probability the way an authored
      Bayesian model would, and each needs its hypothesis space written by a person
  - technique: technique.refinement-harness
    rel: overlaps
    scope: modeling.belief-update
    note: >-
      both carry evidence from one attempt into the next; the harness re-prompts with the
      failure attached, this has the update rule trained into the weights
provenance:
  entered: 2026-10-20
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Bayesian Teaching

**What it is.** Write a normative Bayesian model of the task: here, an assistant that infers
a user's flight preferences from the choices they make over five rounds. Fine-tune a language
model on that model's predictions, so it learns to update the way the Bayesian model does.

**The cognate.** [`modeling.belief-update`] asks that evidence revise what is held. Off the
shelf, language models in this task "often plateau after a single interaction", while people
keep improving from round 1 to round 5. Trained on the normative updater's outputs, the model
keeps updating, and the behaviour carries to tasks it was not trained on.

**Therefore.** Where a correct update rule can be written down, it can be taught to a model
by imitation rather than prompted for.

**The limit.** The rule is authored, one task family at a time, and the space it updates over
is fixed. The cell's open part, revising a rich account of an environment after contrary
evidence, is not what this measures, so the cell's status does not move.
