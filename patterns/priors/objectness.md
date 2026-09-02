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

**Note on scope.** ARC-AGI-3's environment-design constraints add **basic physics**
(gravity, momentum, bouncing) and **agentness** as priors alongside this one — a widening
of the 2019 four-prior list that is easy to miss because the two lists are published in
different documents.
