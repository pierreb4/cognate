---
id: priors.agentness
kind: capability
name: Agentness
faculty: prior
human_source:
  - title: "Core knowledge (Spelke), via On the Measure of Intelligence §III.1.2"
    url: https://arxiv.org/abs/1911.01547
  - title: "Gergely & Csibra, Teleological reasoning in infancy: the naive theory of rational action (TiCS, 2003)"
    url: https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(03)00128-1
part_of: [priors]
completed_by: [goal-setting.goal-inference]
status: open
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Agentness

**Context.** A scene contains things that move. Some of them move because they were pushed;
some of them move because they want something.

**Problem.** Chollet lists agentness alongside objectness as a Core Knowledge prior:
recognizing that certain objects are agents, that they have goals, and that they act
efficiently to achieve them. Infants make this split before they have language for it, and
they use it immediately — an object that starts moving on its own, or takes a detour around
an obstacle, is read as goal-directed and its future behaviour is predicted from its
inferred goal rather than from its trajectory. A system without the prior has to model
every mover as physics, which is both wrong and much more expensive.

**Therefore.** Carry a type distinction between things that are moved and things that move
themselves, and predict the second kind by attributing a goal rather than by extrapolating
motion.

**Status: open.** Nothing in the register addresses this. It is also the prior on which
[`goal-setting.goal-inference`] rests: inverse planning has nothing to invert until
something has been identified as an agent.
