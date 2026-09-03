---
id: priors.objectness
kind: capability
name: Objectness
faculty: prior
human_source:
  - title: "Core knowledge (Spelke), via On the Measure of Intelligence §III.1.2"
    url: https://arxiv.org/abs/1911.01547
part_of: [priors]
completed_by: [modeling.state-abstraction]
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

# Objectness

**Context.** A grid, an image, or a scene arrives as an undifferentiated array. Every
downstream faculty — modeling, planning, goal inference — presupposes that the array has
already been carved into persisting things.

**Problem.** Chollet specifies this prior as three commitments: **cohesion** (parts move
together), **persistence** (a thing occluded or unchanged is still the same thing), and
**influence via contact** (things affect each other by touching). Systems routinely
implement the first and omit the other two, then fail when a thing is re-coloured or
briefly hidden and identity is silently lost.

**Therefore.** Treat object *identity across time* as a first-class output, not a
by-product of per-frame segmentation.

**How a technique is graded here.** By the supplied/acquired test (`SCHEMA.md`). Being
given a segmenter, an object vocabulary or a hand-written primitive set is consumption,
not coverage — this is the ground on which DOORMAX was refused this cell, its own future-
work section conceding the object vocabulary is an input. `direct` requires cohesion,
persistence AND influence-via-contact to be acquired from observation; implementing
cohesion alone and losing identity on a recolour is the documented failure, not a partial
pass.

**Note on scope.** ARC-AGI-3's environment-design constraints add **basic physics**
(gravity, momentum, bouncing) and **agentness** as priors alongside this one — a widening
of the 2019 four-prior list that is easy to miss because the two lists are published in
different documents.
