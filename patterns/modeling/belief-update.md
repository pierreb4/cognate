---
id: modeling.belief-update
kind: capability
name: Belief Update
faculty: modeling
human_source:
  - title: "Bayesian Models of Cognition (Griffiths, Chater & Tenenbaum, MIT Press 2024)"
    url: https://mitpress.mit.edu/9780262049412/
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

**Status: open.** Note the asymmetry — the machine-side literature on *scoring* candidate
programs is vast, while the literature on *revising a committed account* is thin. That
asymmetry is the gap.
