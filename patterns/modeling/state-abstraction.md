---
id: modeling.state-abstraction
kind: capability
name: State Abstraction and Object Individuation
faculty: modeling
human_source:
  - title: "Scholl & Pylyshyn, Tracking Multiple Items Through Occlusion: Clues to Visual Objecthood (Cognitive Psychology, 1999)"
    url: https://perception.yale.edu/papers/99-Scholl-Pylyshyn-CogPsych.pdf
  - title: "Core knowledge (Spelke & Kinzler, Developmental Science 2007)"
    url: https://onlinelibrary.wiley.com/doi/10.1111/j.1467-7687.2007.00569.x
part_of: [modeling]
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

# State Abstraction and Object Individuation

**Context.** Observations arrive as a stream of frames or grids. [`priors.objectness`]
supplies the commitment that each frame contains persisting things; this pattern is about
what has to be true *across* frames.

**Problem.** A per-frame segmenter produces a fresh, anonymous set of regions every step.
Nothing in that output says *this* blob is the same thing as *that* blob one step ago. Human
vision solves the correspondence problem with a small set of pre-attentive indices that
stick to items through occlusion and through changes in their features — the object stays
the same object when it changes colour or disappears behind something. Every capability
downstream assumes this has happened: a difference function
([`technique.means-ends-analysis`]) needs a state whose parts are named, and a belief update
needs to know which thing the evidence was about.

**Therefore.** Emit identity, not just segmentation — a stable index per thing, maintained
across frames, that survives feature change and occlusion — and let the planner and the
hypothesis space be written over those indices rather than over raw arrays.

**How a technique is graded here.** By the supplied/acquired test (`SCHEMA.md`). A
classical planner handed a factored state, or a learned method holding the abstraction
implicitly in weights where nothing downstream can name a thing, earns `incidental`.
`direct` requires identity to be an emitted output — a stable index per thing, derived
from the observation stream and surviving occlusion and feature change.

**Status: open.** No technique in the register addresses this. The classical planners assume
the abstraction is handed to them; the learned methods hold it implicitly in weights where
nothing downstream can name a thing. This is where the gap on
[`planning-execution.goal-decomposition`] lands after it moves down a layer.
