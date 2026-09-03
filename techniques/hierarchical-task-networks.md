---
id: technique.hierarchical-task-networks
kind: technique
name: Hierarchical Task Networks (HTN)
addresses:
  - capability: planning-execution.goal-decomposition
    strength: direct
    note: decomposition is the primitive operation — a method names how a task breaks into subtasks, so the hierarchy is data rather than something the planner must discover
  - capability: goal-setting.subgoal-recognition
    strength: incidental
    note: a subtask counts as achieved when its decomposition's primitives have executed and their effects hold; the achievement test is authored by hand, never inferred
requires:
  - token: expert-authored-library
    note: a library of methods written by a domain expert
  - token: operator-preconditions
    note: operators with explicit preconditions and effects
  - token: state-representation
    note: a state representation those preconditions can be evaluated against
leverage: knowledge
cost: low
evidence: []
no_absolute_score: true
caveats:
  - "SHOP2 (https://arxiv.org/abs/1106.4869) won an award at the 2002 International Planning Competition; no percentage is entered here because planning-competition results carry no split or regime comparable to anything else in this register."
  - "The method library is the system. HTN performance is a statement about the expert who wrote the methods, and is not transferable to a domain where no one has written them."
interacts:
  - technique: technique.means-ends-analysis
    rel: overlaps
    scope: planning-execution.goal-decomposition
    note: >-
      both decompose a goal through operator preconditions; HTN reads a human's method
      library where means-ends derives the split from a difference function
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Hierarchical Task Networks (HTN)

**What it is.** Instead of searching for a plan, expand one. A *method* says that this task
can be accomplished by this ordered set of subtasks under these conditions; planning is the
recursive application of methods until only primitive operators remain. SHOP2 is the
canonical implementation.

**The cognate.** Where [`technique.means-ends-analysis`] *derives* subgoals from unmet
preconditions, HTN *is handed* them. That difference is the whole trade: MEA needs only a
difference function and will flail without a good one; HTN needs no search heuristic at all
and will do nothing outside its library.

**Therefore.** Choose HTN when the decomposition is known and stable and the value is in
executing it reliably. Choose MEA when the decomposition is what you are trying to find.

**The limit, and why it matters here.** HTN answers "how is this goal decomposed" by
assuming someone already answered it. The open problem named on
[`planning-execution.goal-decomposition`] — decomposition over learned, noisy
representations — is precisely the part HTN moves out of the planner and into the author.
