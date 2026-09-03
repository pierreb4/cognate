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
status: partial
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

**Status: partial.** One technique reaches this cell:
[`technique.temporal-feature-similarity-slots`] (VideoSAUR) at `partial` — slots are an
addressable set a caller can name, scored by a single clustering over a whole real video,
learned from a target in which no id, mask or count appears. It is a thin fill and the node
says so: occlusion is never measured, only attributed to a decay with clip length, and the
margin over an identity-perfect trivial control (a fixed spatial grid) is under 2x. The
classical planners still assume the abstraction is handed to them, and the other learned
methods still hold it implicitly in weights where nothing downstream can name a thing.

**What was searched, and the shape of what was not found.** The cell was asked alone across
the object-centric video, multi-object-tracking, developmental-psychology and
video-world-model literatures. The negative that survived is structural, and worth more than
the count of candidates: **the field splits acquisition from individuation.** The
point-tracking literature acquires correspondence with no identity annotation and measures
it through occlusion directly — OmniMotion (arXiv 2306.05422v2) reports occlusion accuracy
85.3 on TAP-Vid-DAVIS from a per-video fit with no training set — but it emits a per-POINT
index and never groups points into things; its own limitations concede "duplicated objects
in canonical space", and there is no object-level metric in the paper or its supplement. The
tracking and video-instance-segmentation literatures individuate, but the identity is the
training label. Each half is done well by a literature that does not do the other half.
VideoSAUR is admitted here because it is one of the few places the two halves meet at all —
not because it does either half decisively.
