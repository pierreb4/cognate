---
id: planning-execution.goal-decomposition
kind: capability
name: Goal Decomposition
faculty: planning-execution
human_source:
  - title: "Newell & Simon, Human Problem Solving — protocol analysis of subgoaling"
    url: https://en.wikipedia.org/wiki/General_Problem_Solver
part_of: [planning-execution]
completed_by: []
status: partial
---

# Goal Decomposition

**Context.** A goal is known, or has been inferred, and is not reachable by a single action.

**Problem.** Breaking a goal into subgoals whose achievement composes. The published
open-problem lists single this out: a living survey names *sub-exponential hierarchical
decomposition* as something "no current architecture implements."

**Therefore.** Represent actions with explicit preconditions and effects so that an unmet
precondition becomes a subgoal automatically, rather than requiring a separately authored
task hierarchy.

**Status: partial.** Classical methods ([`technique.means-ends-analysis`], HTN) solve this
given a good state abstraction, which is exactly what perception does not hand you. The
open part is decomposition over learned, noisy representations.
