---
id: priors.basic-physics
kind: capability
name: Basic Physics
faculty: prior
human_source:
  - title: "Core knowledge (Spelke & Kinzler, Developmental Science 2007)"
    url: https://onlinelibrary.wiley.com/doi/10.1111/j.1467-7687.2007.00569.x
  - title: "Building Machines That Learn and Think Like People (§4.1.1, intuitive physics)"
    url: https://arxiv.org/abs/1604.00289
part_of: [priors]
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

# Basic Physics

**Context.** An environment where things fall, carry momentum, collide and bounce, and
cannot pass through each other.

**Problem.** This prior is not in Chollet's 2019 four-prior list. It appears later, in
ARC-AGI-3's environment-design constraints, which widen the set to include basic physics
alongside agentness — a widening that is easy to miss because the two lists live in
different documents. The move matters: a static grid benchmark can be solved with
objectness and geometry alone, but an interactive environment adds *dynamics that continue
without the agent acting*, and a system whose entire model is "my action, then the next
observation" has no place to put them.

**Therefore.** Separate what the environment does on its own from what the agent's action
did, and model the first as continuing state rather than as noise in the transition.

**How a technique is graded here.** By the supplied/acquired test (`SCHEMA.md`). A physics
engine, or hand-coded gravity and bounce rules, is consumption. `direct` requires the
dynamics to be inferred from observed motion.

**Status: open.** No technique addresses this. Note also that the register's ARC-facing
techniques were built for the static benchmarks, where this prior is not exercised at all —
their scores carry no information about it.
