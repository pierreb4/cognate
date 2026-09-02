---
id: technique.means-ends-analysis
kind: technique
name: Means-Ends Analysis (GPS / STRIPS)
addresses:
  - capability: planning-execution.goal-decomposition
    strength: direct
    note: recursively reduces the difference between current and goal state by selecting an operator that reduces it
requires:
  - operators expressed as (preconditions, effects)
  - a computable difference function between states
  - a state representation the difference function can read
cost: low
evidence:
  - claim: "Foundational method of the General Problem Solver; the operator/precondition/effect formulation is the basis of all subsequent classical planning"
    kind: measured
    split: not-applicable
    regime: not-applicable
    source: https://en.wikipedia.org/wiki/General_Problem_Solver
    stars: 4
no_absolute_score: true
caveats:
  - "Its classical failure is the difference function: MEA is only as good as the state abstraction it is handed, and on raw perceptual input the difference function is the actual open problem."
related: [technique.hierarchical-task-networks]
---

# Means-Ends Analysis (GPS / STRIPS)

**What it is.** Newell & Simon, 1959. Represent actions as `(preconditions, effects)`.
Compute the difference between where you are and where you want to be. Select an
operator that reduces that difference. Recurse on its unmet preconditions.

**Why a 1959 method is in a 2026 register.** Because this is the register's argument in
miniature. MEA was derived from protocol analysis of *humans solving problems out loud* —
it is a cognate in the strict sense, a machine mechanism with documented human descent.
Teams building interactive agents reliably rediscover it after a reactive-controller
phase fails, having spent the intervening time on the detour.

**The honest limit.** MEA does not solve perception. Handed a good state abstraction it
is close to free; handed raw pixels it does nothing, because the difference function has
nothing to read. When a project's gap "moves down a layer" from planning to perception
after adopting MEA, that is not a failure of the technique — it is MEA working and
exposing where the real gap was.
