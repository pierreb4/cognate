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
status: partial
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
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

**How a technique is graded here.** By the supplied/acquired test (`SCHEMA.md`). A
demonstration pair, a reward function or a verifier IS the objective handed over, so a
system consuming one earns `incidental` at most however well it then pursues it. `direct`
requires the objective to be inferred from observation and to remain revisable — nameable,
actable, and replaceable when found wrong.

**Which capability this is, declared (2026-09-03).** Two different things travel under the
name "goal inference" and this cell is only one of them.

- **(A) reading ANOTHER agent's goal** from its observed behaviour — inverse planning,
  Bayesian theory of mind, inverse RL, ToMnet.
- **(B) forming one's OWN objective** in an environment with no instructions, no reward
  specification and, in the limit, no other agent to read.

**This cell is (B).** The faculty is goal-*setting*; the Context describes a person shown a
novel game screen with nobody to imitate; the Therefore asks for an objective that can be
named, acted on and replaced; and both `completed_by` cells are about pursuing an objective
one already holds. A system that reads another agent's goal does not address this cell
however well it does it — that is a different capability, and it sits closer to
[`priors.agentness`] than to this directory.

**A declared mismatch, not silently fixed.** Both `human_source` rows above are (A):
Baker/Saxe/Tenenbaum infer an observed agent's utility from its trajectory, and Gergely &
Csibra's teleological stance is about interpreting *others'* actions. Keeping them here
asserts that the machinery infants use to read others is the machinery they use to set
their own goals. That is a substantive developmental claim, it may well be true, and this
register has neither made it explicitly nor tested it. Flagged rather than re-cited: which
way to resolve it is a content decision, and the honest state is that the cell's problem
statement and its citations point at two different literatures.

**Status: partial (2026-09-05).** One technique reaches this cell:
[`technique.test-time-digital-twin`] (Twin, arXiv 2608.14490v1) at `partial`. The objective
is an executable predicate the agent writes BEFORE a level's first completion signal, plans
against, and retires when the predicted state is reached without a level boundary — nameable,
actable, replaced when wrong, and never supplied: the agent "is not given object identities,
action semantics, the transition or goal rules, demonstrations, or any privileged simulator
state." The row is a pair, and the node insists on both halves: the first committed goal is
right on 156 of 179 cleared levels (87.2%), and at the action grain the predicate's claims run
at precision 0.214 — "most wins are claimed, and most claims are wrong." `partial` under the
distance rule because two things are handed over that are not the objective: the terminal
level-completion flag that confirms or refutes each hypothesis, and five authored
visual-change heuristics that rank which reachable states get proposed. The two games Twin
does not finish fail exactly here — "accurate dynamics, unresolved goals."

**What was searched, and what was refused (2026-09-05, by hand against the Run 11 gate).**
The gate's satisfiability clause — the objective may be supplied to the scorer, never to the
system — is what a "completion signal only after winning" interface satisfies, and it is why
this literature could enter where the earlier asks returned nothing. Examined and not entered:

- **EMPA** (Tsividis et al., arXiv 2107.12544v1, 2021) is the same shape a Bayesian way round:
  termination rules of the form `WIN IF count(c)==0` inferred from observed Win/Loss status,
  held as "a superset of possible explanations" the planner tries to satisfy, on 90 VGDL games
  against humans. It is a second (B) candidate, not a refusal. Not entered this pass because
  the goal grammar is one authored template, the 90 games are the same lab's own VGDL suite
  (`solution-in-span` by construction), and it is a v1-only preprint whose row needs its own
  reading.
- **WorldCoder** (Tang, Key & Ellis, 2402.12275v3) learns a reward function as code, but "the
  agent receives a goal in natural language" in every environment (mission strings, "win the
  game", ALFWorld instructions). The objective is consumed. Refused; Twin cites it as the
  source of its consistency constraint.
- **Cogito, Ergo Ludo** (2509.25052v1) induces a text "Game Objective" from play on
  Minesweeper, Frozen Lake and Sokoban with +1 at completion and "no explicit game rules", but
  whether the game's identity reaches the agent through the TextArena observation was not
  settled from the primary, and that is the trap the gate names (zero-shot in the weights, not
  the prompt). Unadjudicated, not refused.
- **From Gameplay Traces to Game Mechanics** (2602.00190v1) induces VGDL including a
  TerminationSet, but offline from ten-frame traces with no outcomes in them, with the game's
  name and description supplied above level 0, scored by an LLM judge. Refused on clause 3.
- **Executable World Models** (Rodionov, 2605.05138v2) and **OPINE-World** hold a goal
  predicate in code too; the first was read only far enough to see it reports no baseline,
  the second is known only through Twin's related-work claim that it "fits its predicate
  only after a first level is cleared" — which, if true, is the waiting-for-the-reward shape.
  Neither was adjudicated against its own primary.
- **Inductive general game playing** (Cropper, Evans & Law, 1906.09627) learns a `goal`
  predicate as a rule, but from ground goal facts per state supplied as training examples —
  labels for the graded capability, the supplied/acquired test's `incidental`.

**Still open here.** A `direct` fill would need the objective produced with neither a
terminal flag nor an authored goal-shape prior — the case the cell's Context describes, a
person who names the objective before ever finishing a level. Nothing examined does that.
And the field-level claim the Run 11 STOP branch was written to make — that every available
source of an objective IS the objective — is now false in one instance and should not be
cited.

The nearest miss in the corpus is [`technique.intrinsic-motivation-exploration`], and the
way it misses is instructive: it needs a `reward-channel` for its bonus to be added to, so
it does not infer an objective — it *substitutes a generic drive* for one, and then still
requires the real objective to arrive from outside. Novelty is not an answer to "what is
this environment asking of me"; it is a way of acting well while that question stays open.
