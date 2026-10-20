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

**Status: open (2026-10-20: EMPTY -> INDIRECT).** One technique reaches this cell,
[`technique.latent-video-prediction`] (V-JEPA) at `partial`: it acquires a
violation-of-expectation signature from unlabelled video with no physics engine, which is the
`direct` criterion, but only in simple scenes, and it predicts passive video, so it never
separates what the environment did from what an action did. The status stays `open` because
its realistic-scene result is near chance (below). Note also that the register's ARC-facing
techniques were built for the static benchmarks, where this prior is not exercised at all —
their scores carry no information about it. ARC-AGI-3 exercises it, but only as part of a
composite score.

**The measured state of the field.** Against people, every model tested is near chance in
realistic scenes. On IntPhys 2's Main split (violation of expectation over permanence,
immutability, spatiotemporal continuity and solidity) people score 96.44, the best model,
V-JEPA 2-h, 57.51, and the best multimodal LLM, Gemini 2.5 Flash, 55.63
([2506.09849](https://arxiv.org/abs/2506.09849)). On PhysBench's physical question answering,
GPT-4o scores 49.49% against 95.87% for people
([2501.16411](https://arxiv.org/abs/2501.16411)).
