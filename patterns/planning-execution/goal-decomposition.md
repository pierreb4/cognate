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
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
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

**What the language-model results measure.** On PlanBench, o1-preview finds a valid plan for
97.8% of plain Blocksworld instances, 52.8% of the same problems with the predicates
obfuscated (Mystery Blocksworld), and 23.63% of problems with 6 to 20 blocks
([2409.13373](https://arxiv.org/abs/2409.13373)). Surface familiarity, not decomposition,
closed the plain case. METR's time horizon, the length of task a model completes half the
time, doubled every 196 days over 2019-2025, every 131 days since 2023 and every 89 days
since 2024 (Time Horizon 1.1, [METR](https://metr.org/blog/2026-1-29-time-horizon-1-1/)), and
the most capable model measured is at the suite's stated ceiling of 16 hours. That progress is
in *executing* long tasks; no measure found separates decomposition from execution.
