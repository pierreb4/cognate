---
id: technique.mcts
kind: technique
name: Monte-Carlo Tree Search
addresses:
  - capability: exploration.experiment-design
    strength: incidental
    note: UCB trades exploration against exploitation by VISIT COUNT and value variance — coverage of the tree, never discrimination between hypotheses about the environment
  - capability: planning-execution.goal-decomposition
    strength: incidental
    note: produces a sequence of actions toward a goal without ever naming an intermediate one; nothing in the tree is a subgoal
requires:
  - token: resettable-simulator
    note: a simulator you can roll forward and reset — the binding precondition
  - token: value-signal
    note: a terminal or heuristic value signal
  - token: per-task-compute
    note: many simulations per decision
cost: medium
evidence: []
no_absolute_score: true
caveats:
  - "The precondition does the work. MCTS is available exactly when a resettable forward model exists; for an agent that must learn the environment's rules from interaction, the model MCTS needs is the thing that is missing."
  - "Its demonstrated results are in games with exact simulators (see the survey, https://dblp.org/rec/journals/tciaig/BrownePWLCRTPSC12.html). Those carry no split or regime on any benchmark in this register, so no percentage is entered."
interacts:
  - technique: technique.means-ends-analysis
    rel: overlaps
    scope: planning-execution.goal-decomposition
    note: >-
      both turn a goal into an action sequence; sampled rollouts versus derived sub-goals,
      and only means-ends leaves the decomposition inspectable
---

# Monte-Carlo Tree Search

**What it is.** Build a search tree asymmetrically: descend by an upper-confidence rule to
a promising leaf, expand it, roll out to an estimate, and back the value up the path.
Repeat until the budget is spent, then take the most-visited child.

**Why it appears here as a cautionary node.** The README uses MCTS as the worked example of
the reverse direction — *I have a technique; what does it bear on?* — and the honest answer
is narrower than its reputation suggests. Both of its edges are `incidental`. MCTS is a
superb *action selector* given a model; it contributes nothing to acquiring one.

**Therefore.** Ask for the simulator first. If the environment is unknown and must be
inferred from interaction, MCTS is downstream of the actual problem, and adopting it will
move the gap rather than close it.

**The exploration confusion.** MCTS is routinely cited as an exploration method, and it is
— over its own tree. [`exploration.experiment-design`] asks for something different: an
action chosen because its outcome discriminates between live hypotheses about the world.
UCB's exploration term has no hypothesis set to read.
