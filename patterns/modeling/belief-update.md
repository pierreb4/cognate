---
id: modeling.belief-update
kind: capability
name: Belief Update
faculty: modeling
human_source:
  - title: "Bayesian Models of Cognition (Griffiths, Chater & Tenenbaum, MIT Press 2024)"
    url: https://mitpress.mit.edu/9780262049412/
  - title: "A behavioral analysis of degree of reinforcement and ease of shifting to new responses in a Weigl-type card-sorting problem (Grant & Berg, Journal of Experimental Psychology 38, 1948): the Wisconsin Card Sorting Test"
    url: https://doi.org/10.1037/h0059831
  - title: "The Unity and Diversity of Executive Functions (Miyake et al., Cognitive Psychology 41, 2000): shifting as a separable function"
    url: https://doi.org/10.1006/cogp.1999.0734
part_of: [modeling]
completed_by: []
status: open
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
---

# Belief Update

**Context.** A hypothesis is held and an experiment has returned an outcome.

**Problem.** Revising a held account in light of evidence is the step that closes the
loop; without it, hypothesis formation and experimentation both become decoration. ARC
Prize's ARC-AGI-3 replay audit names this as its third failure mode, "solved the level,
didn't learn the game": "even if a model beat a level, that reward did not translate into
further success", and "without an explicit check on why the prior level was won, models will
carry their misconception into the next level" ([source](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)).

**Therefore.** Make the update operation explicit and cheap enough to run every step.
The representation choice made in [`modeling.hypothesis-formation`] determines what is
even possible here: weights admit gradient updates but no retraction; explicit programs
admit retraction but need a search to replace them.

**It fails in two directions.** Holding on too long is perseveration, what the Wisconsin
Card Sorting Test measures in people when the sorting rule changes unannounced; letting go
too soon throws away an account that was right. Miyake et al. find shifting separable from
updating and inhibition, so neither direction predicts the other. Turn Bench, a Kaggle
Measuring AGI write-up, builds both into one hidden-rule game, and the same model fails
them in opposite ways: "Opus collapses on reversal (42%) while Haiku leads (80%), yet on
cycling, Opus leads (86%) and Haiku trails (73%)", and on Resistance, where no matchup
holds and staying put is optimal, the best switchers of the standard variant "collapse
(Haiku 45%, DeepSeek 47%)"
([source](https://www.kaggle.com/competitions/kaggle-measuring-agi/writeups/new-writeup-1775940834879)).
LearningBench gives holding on a cheap signature in action logs: "43 runs show ≥10
consecutive identical actions", in a set where failed runs spent 4.3× the tokens of solved
ones ([source](https://www.kaggle.com/competitions/kaggle-measuring-agi/writeups/learningbench)).
A repeat count alone cannot tell the two apart, since repeating one action is correct play
wherever the mechanic is a cycle; reading it needs a game where the same repeats are wrong
(see the variant pair in Turn Bench's design). Whether a system lets go depends on what it
would have to replace the account with: Haiku "pivots 98% of the time in urgent ... but
only 8% in super", the variant with the more complex replacement plan. That condition is
reported once and measured nowhere else. All of these numbers are single author-scored
runs with no human baseline.

**Status: open.** Note the asymmetry — the machine-side literature on *scoring* candidate
programs is vast, while the literature on *revising a committed account* is thin. That
asymmetry is the gap.
