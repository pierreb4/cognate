---
id: modeling.hypothesis-formation
kind: capability
name: Hypothesis Formation
faculty: modeling
human_source:
  - title: "Building Machines That Learn and Think Like People (§4.1, model-building)"
    url: https://arxiv.org/abs/1604.00289
  - title: "Society of Mind — frames and difference-engines"
    url: https://archive.org/details/marvin-minsky-the-society-of-mind
part_of: [modeling]
completed_by:
  - exploration.experiment-design
  - modeling.belief-update
  - modeling.commit-or-abstain
status: partial
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
---

# Hypothesis Formation

**Context.** A system is placed in an environment whose rules it was not told. It can
observe and it can act. Before it can act *well*, it must hold a candidate account of
what governs the environment.

**Problem.** Generating a candidate is not the same as searching a space of candidates.
A system that enumerates programs is doing search; a system that forms a hypothesis has
committed to a *specific*, falsifiable account and can say what would refute it. The
second is what makes the next two patterns — [`exploration.experiment-design`] and
[`modeling.belief-update`] — possible at all. Without commitment there is nothing to
design an experiment against and nothing to update.

**Therefore.** Represent the candidate account explicitly and separately from the policy
that acts on it, so that it can be named, tested, and discarded. The representation
choice is the branch point: symbolic program, natural-language description, learned
latent, or weights.

**Known failure.** ARC Prize's replay audit of GPT-5.5 and Opus 4.7 on ARC-AGI-3 (0.43% and
0.18% on the semi-private set, May 2026) names what the environments demand — "encountering
an unfamiliar environment, forming a working theory, testing it, updating it when the
evidence disagrees, and carrying forward what was learned" — and reports three failure modes
against it: "true local effect, false world model", "wrong level of abstraction from
training data", and "solved the level, didn't learn the game"
([source](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)). The loop fails at a different step in each
model: "Opus compressed its observations into a confident-but-wrong theory. GPT-5.5 had
difficulty compressing at all." A system can generate plausible hypotheses and still fail
here if nothing downstream can kill one. Dated to one model generation: on 2026-09-03 the
same auditors report GPT-6 Astra at 62.7% on the semi-private set in their Standard harness,
which only carries forward notes, and 99.9% with a Provider Adapter that "preserves opaque
reasoning state between requests" ([source](https://arcprize.org/blog/astra)); no mechanism
is published for either, so nothing here is graded from it. The interactive rule puzzles of
RULEARN show which step fails against people: agents guess the first rule better than
people do (about 30% against about 10%) but refine it worse, so puzzle success is 50.33% for
the best agent setup against 63.33% for 50 people
([2408.10455](https://arxiv.org/abs/2408.10455)).

**How a technique is graded here.** The test is *exhibitable commitment*: can the system,
at any moment, produce one specific account that something downstream could act on and
refute? `direct` if the account is the system's working object — a program, a description,
a searchable latent. The limiting case is [`technique.test-time-digital-twin`], which
hash-commits its prediction before every scored action, so the commitment is not merely
exhibitable but exhibited — and the same paper reports that its GOAL hypotheses are mostly
wrong at the action grain, which is this cell met while [`goal-setting.goal-inference`] is
not. `incidental` if the system reaches answers without ever holding one:
[`technique.test-time-training`] keeps it in weights where it cannot be named, and
[`technique.brute-force-program-search`] holds a lattice of compositions instead of a
current belief. Note that the second case is the one that fixes the rule — brute-force
emits perfectly readable symbolic programs, so the test is **not** whether the
representation is nameable, it is whether a commitment exists to be named. A candidate
*answer* is not a candidate *account*: a system that emits an output and no rule cannot
tell anything downstream what it believes governs the environment, whatever form its
output takes. The distinction now has a human-baselined measure: in a hand classification of
ConceptARC rules, about 27% of o3's correct outputs rest on unintended or incorrect rules,
against about 7% of humans' correct outputs ([2510.02125](https://arxiv.org/abs/2510.02125)
v5, 2026-10-16). A right answer reached through the wrong account is common, and more common
in the machine.

**Related.** Completed by [`exploration.experiment-design`] and [`modeling.belief-update`].
Its representation choice constrains which techniques can address the other two.
