---
id: planning-execution.execution-reliability
kind: capability
name: Execution Reliability
faculty: planning-execution
human_source:
  - title: "Norman, Categorization of action slips (Psychological Review 88, 1981)"
    url: https://doi.org/10.1037/0033-295X.88.1.1
part_of: [planning-execution]
completed_by: [goal-setting.subgoal-recognition]
status: open
provenance:
  entered: 2026-10-20
  commit: c6ca7db
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Execution Reliability

**Context.** A plan is known, given or derived ([`planning-execution.goal-decomposition`]),
and it takes many steps to carry out. Each step is easy on its own.

**Problem.** Long-task capability and long-task reliability come apart. A system that can do
each step can still fail the task, because per-step errors compound, and the errors it has
already made sit in its own context and change what it does next. People slip too, and
Norman's classification of action slips is the human-side account of how a known intention
goes wrong in execution. Two machine measures show the gap. In a synthetic task with an
explicit plan, per-step accuracy falls once the context holds the model's own earlier errors,
and scale does not remove this self-conditioning; GPT-5 with thinking holds 80% accuracy for
2,176 steps, while non-thinking models fail at about 4 to 6
([2509.09677](https://arxiv.org/abs/2509.09677), ICLR 2026). And METR reports the most capable
model it measured at a 50% time horizon at or beyond its suite's 16-hour ceiling, but an 80%
horizon of about 3 to 4 hours ([time horizons](https://metr.org/time-horizons/);
[frontier risk report](https://metr.org/blog/2026-05-19-frontier-risk-report/)): the length of task a
model completes reliably is a fraction of the length it completes at all.

**Therefore.** Carry out a known plan over many steps without per-step errors compounding,
including when the system's own earlier errors are in its context: check each step's result
against what the plan predicted, and keep a failed step from becoming the premise of the next.

**How a technique is graded here.** On the step that keeps errors from compounding, not on
the plan. A technique that only shortens the plan, or that succeeds because the task is short,
does not address the cell.

**Status: open (entered 2026-10-20).** No technique in the register addresses it, and no
benchmark found measures people and machines on the same long execution. It is completed by
[`goal-setting.subgoal-recognition`]: knowing that a step was achieved is how a slip is
caught.
