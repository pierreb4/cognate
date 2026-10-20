---
id: priors.objectness
kind: capability
name: Objectness
faculty: prior
human_source:
  - title: "Core knowledge (Spelke), via On the Measure of Intelligence §III.1.2"
    url: https://arxiv.org/abs/1911.01547
part_of: [priors]
completed_by:
  - modeling.state-abstraction
  - priors.numbers-and-counting   # through individuation: only separated things can be counted
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

**Also examined and refused.** [`technique.temporal-feature-similarity-slots`] (VideoSAUR)
was the obvious second candidate — it groups an unlabelled video into slots with no authored
vocabulary, and it serves [`modeling.state-abstraction`]. It gets no edge here. Only cohesion
is acquired: influence-via-contact is absent from the paper entirely, and persistence is
disclaimed by its own authors ("we do not have any memory module to handle object occlusions
and reidentification"). Cohesion alone is precisely the documented failure above. The two
acquired-objectness candidates fail on opposite commitments, which is the more interesting
fact: poking buys cohesion and contact but not permanence, and predicting buys cohesion but
neither of the others.

[`technique.latent-video-prediction`] (V-JEPA) was examined the same way on 2026-10-20 and
refused. It is the first candidate for *acquired* persistence: its surprise at an object
vanishing behind an occluder is learned from unlabelled video. But the signature holds on
simple scenes and collapses on IntPhys 2, which tests permanence among its properties;
contact is weak where it is tested (GRASP 66%, InfLevel-lab 62%); and the model emits a
surprise score, not an index of persisting things, so identity across time is never an
output. It serves [`priors.basic-physics`] at `partial` instead.

**What the multimodal models show, against people.** On CoreCognition's object-permanence
items people score 88.10 and the best model 74.14 (InternVL3-78B), and low-level concepts
such as permanence improve less with scale than high-level ones
([2410.10855](https://arxiv.org/abs/2410.10855)). On TOC-Bench, which asks about identity,
state and continuity across occlusion in video, people score 89.3% and GPT-5.5 47.1%
([2605.09904](https://arxiv.org/abs/2605.09904)). Neither result is a technique, so neither
moves the grade; they say the persistence commitment is the one current models lack.

**Individuation, between this cell and counting.** Separating a scene into discrete items is
the step [`priors.numbers-and-counting`] depends on: the exact number system counts only
things already separated into things. It was proposed as a cell of its own (individuation)
and is held instead as the `completed_by` edge from this cell to counting (2026-10-20). The
evidence for keeping it there is on the counting side: multimodal models count what a prior
expects rather than the items in the image.

**Note on scope.** ARC-AGI-3's environment-design constraints add **basic physics**
(gravity, momentum, bouncing) and **agentness** as priors alongside this one — a widening
of the 2019 four-prior list that is easy to miss because the two lists are published in
different documents.
