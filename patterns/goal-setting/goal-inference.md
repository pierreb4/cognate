---
id: goal-setting.goal-inference
kind: capability
name: Goal Inference
faculty: goal-setting
human_source:
  - title: "Baker, Saxe & Tenenbaum, Action Understanding as Inverse Planning (Cognition, 2009)"
    url: https://www.sciencedirect.com/science/article/pii/S0010027709001607
  - title: "Gergely & Csibra, Teleological reasoning in infancy: the naive theory of rational action (TiCS, 2003)"
    url: https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(03)00128-1
part_of: [goal-setting]
completed_by:
  - goal-setting.subgoal-recognition
  - planning-execution.goal-decomposition
status: open
---

# Goal Inference

**Context.** An agent is dropped into an interactive environment with no instructions, no
reward specification, and no statement of what winning is. Humans do this constantly and
barely notice: shown a novel game screen, a person forms a candidate objective within
seconds and starts acting on it.

**Problem.** Almost every machine method in this register presupposes the objective. A
demonstration pair *is* the goal; a reward function *is* the goal; a verifier *is* the
goal. Strip those away and the question — *what is this environment asking of me* — has no
mechanism attached to it. The human-side literature is comparatively rich: infants read
goals from actions by assuming rational means-ends efficiency, and inverse planning
formalizes that as inference over an agent's utility given its behaviour. But inverse
planning infers *another agent's* goal from observed action; it does not tell a system what
its own goal should be in a world with no other agent in it.

**Therefore.** Treat the goal as an inferred, revisable object with the same standing as a
hypothesis about dynamics — something that can be named, acted on, found wrong, and
replaced — rather than as a fixed input to the system.

**Status: open, and this is the register's largest single hole.** No technique node
currently addresses it. That is not an omission awaiting a literature search; the machine
side is genuinely thin, and it is the precondition for every other node in this directory.
