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
status: partial
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

**Known failure.** The failure ARC Prize reports for frontier models on ARC-AGI-3 is
precisely the absence of this loop — agents "can't form a theory, test it, update it"
([source](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)). Note the
failure is reported as a *loop* failure; a system can generate plausible hypotheses and
still fail here if nothing downstream can kill one.

**Related.** Completed by [`exploration.experiment-design`] and [`modeling.belief-update`].
Its representation choice constrains which techniques can address the other two.
