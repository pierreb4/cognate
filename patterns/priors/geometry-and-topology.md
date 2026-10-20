---
id: priors.geometry-and-topology
kind: capability
name: Elementary Geometry and Topology
faculty: prior
human_source:
  - title: "Core knowledge (Spelke), via On the Measure of Intelligence §III.1.2"
    url: https://arxiv.org/abs/1911.01547
  - title: "Spelke, Lee & Izard, Beyond Core Knowledge: Natural Geometry (Cognitive Science, 2010)"
    url: https://pubmed.ncbi.nlm.nih.gov/20625445/
part_of: [priors]
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

# Elementary Geometry and Topology

**Context.** Two shapes are the same shape rotated. A region is inside another region. A
line continues behind an occluder. None of this is stated in the input.

**Problem.** Chollet's fourth Core Knowledge prior covers lines, connectedness,
containment, symmetry, rotation, reflection, scaling, and distance comparison. Human
geometric competence is itself two evolutionarily old systems — one for navigable layouts,
one for small movable forms — and neither captures all of distance, angle and direction,
which is why "elementary geometry" is not one uniform ability even in people. For a machine
the practical consequence is that the operations are cheap to write and expensive to
*learn*, so nearly every system acquires them by having them written.

**Therefore.** State which geometric relations your representation makes available, and
treat that list as a prior you have chosen, not as a neutral encoding.

**How a technique is graded here.** By the supplied/acquired test (`SCHEMA.md`), and this
cell is one of the two worked cases: `technique.dsl-search` sits at `incidental` because
rotate, reflect, connect and fill were written by a person.

**Status: partial.** Better served than the other priors here, but served in one way: the
incoming edge is `incidental`, from [`technique.dsl-search`], where the relations are
authored primitives. A system that induces the symmetry group of a domain it was not told
about has no node.

**What the multimodal models show, against people.** The prior splits. Across eight spatial
benchmarks with published human baselines, GPT-5 is at human level on metric estimation, below
random on 3D mental rotation, and 50 to 80 points short on perspective taking
([2508.13142](https://arxiv.org/abs/2508.13142)). On Dehaene's geometric odd-one-out test (43
concepts), vision-language models fall below unschooled adults: the best scores 37.78%, against
65.34% for Munduruku adults and 85.10% for Western adults
([2505.13281](https://arxiv.org/abs/2505.13281); [2503.03840](https://arxiv.org/abs/2503.03840)).
Metric relations are acquired by these models, which an authored DSL cannot claim, but no
node grades multimodal pretraining here: nothing in it is separable from the model.
