---
id: modeling.mental-transformation
kind: capability
name: Mental Transformation
faculty: modeling
human_source:
  - title: "Shepard & Metzler, Mental Rotation of Three-Dimensional Objects (Science 171, 1971)"
    url: https://doi.org/10.1126/science.171.3972.701
part_of: [modeling]
completed_by: []
status: open
provenance:
  entered: 2026-10-20
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Mental Transformation

**Context.** A question about a scene can only be answered from another state of it: the
object turned, the room seen from where someone else stands.

**Problem.** People answer such questions by simulating the change and reading the answer off
the result; Shepard and Metzler found the time to judge two drawings the same object grows in
proportion to the angle between them, as if the object were turned in the mind. Multimodal
models do not show the capacity. Across eight spatial benchmarks with published human
baselines, GPT-5 is at human level on metric estimation but below random on 3D mental rotation,
and 50 to 80 points short on perspective taking
([2508.13142](https://arxiv.org/abs/2508.13142)); on CoreCognition, perspective-taking
accuracy falls with model scale ([2410.10855](https://arxiv.org/abs/2410.10855)). Of the
gaps the 2026-10-20 survey read in the priors, it is the clearest one that stays flat.

**Therefore.** Hold a representation that can be transformed, apply the rotation or viewpoint
change to it, and read the answer off the transformed state, rather than answering from what
such scenes usually look like.

**How a technique is graded here.** `direct` if the system computes the transformed state from
its own representation of the scene and answers from it. An answer read off scene priors, or a
transformation applied by an authored geometry engine to a scene description it was handed,
is `incidental`.

**Status: open (entered 2026-10-20).** No technique in the register addresses it. It operates
on the relations [`priors.geometry-and-topology`] names; that cell asks which relations a
representation makes available, this one whether the system can move through them.
