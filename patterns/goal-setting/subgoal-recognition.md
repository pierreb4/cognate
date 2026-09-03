---
id: goal-setting.subgoal-recognition
kind: capability
name: Subgoal Recognition
faculty: goal-setting
human_source:
  - title: "Botvinick, Niv & Barto, Hierarchically organized behavior and its neural foundations: a reinforcement learning perspective (Cognition, 2009)"
    url: https://doi.org/10.1016/j.cognition.2008.08.011
part_of: [goal-setting]
completed_by: []
status: open
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Subgoal Recognition

**Context.** A goal has been decomposed, or a plan is being executed, and the system has
just acted. Something changed.

**Problem.** Knowing *that a subgoal was achieved* is a separate capability from having set
one, and it is the one that closes the execution loop. Without it a system cannot tell
progress from noise, cannot release the resources a finished subtask was holding, and
cannot attribute credit to the action that mattered. Classical planning sidesteps this by
having a human write the termination condition into every operator's effects. Hierarchical
reinforcement learning names the same object — the option's termination function — and then
faces the open problem of discovering it rather than being given it. ARC Prize's ARC-AGI-3
failure list states the machine-side symptom directly: agents "can't convert reward into
corrected actions."

**Therefore.** Make achievement an explicit, checkable predicate over state, and keep it
separate from the reward signal — a subgoal can be achieved with no reward emitted, and
reward can arrive with no subgoal achieved.

**Status: open.** The only incoming edge is `incidental`, from
[`technique.hierarchical-task-networks`], where the achievement test exists but was written
by hand. Recognition of an achievement the system was not told to look for has no member.
