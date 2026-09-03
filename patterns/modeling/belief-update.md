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
loop; without it, hypothesis formation and experimentation both become decoration. The
ARC-AGI-3 failure list names this twice — agents "can't convert reward into corrected
actions" and "can't form a theory, test it, update it."

**Therefore.** Make the update operation explicit and cheap enough to run every step.
The representation choice made in [`modeling.hypothesis-formation`] determines what is
even possible here: weights admit gradient updates but no retraction; explicit programs
admit retraction but need a search to replace them.

**Status: open.** Note the asymmetry — the machine-side literature on *scoring* candidate
programs is vast, while the literature on *revising a committed account* is thin. That
asymmetry is the gap.
