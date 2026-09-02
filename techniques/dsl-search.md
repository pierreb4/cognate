---
id: technique.dsl-search
kind: technique
name: Hand-Crafted DSL + Search
addresses:
  - capability: modeling.hypothesis-formation
    strength: direct
    note: the hypothesis is a program in a named, readable language — inspectable, executable, and refutable by a single demonstration pair
  - capability: priors.geometry-and-topology
    strength: incidental
    note: supplies the prior as authored primitives (rotate, reflect, connect, fill) rather than acquiring it
  - capability: priors.numbers-and-counting
    strength: incidental
    note: same — counting and ordering exist because someone wrote the primitive, not because the system learned to count
requires:
  - a human who will author and maintain the primitive set
  - a search or synthesis procedure over compositions of those primitives
  - tasks whose solutions actually lie in the span of the chosen primitives
cost: low
evidence: []
no_absolute_score: true
caveats:
  - "arc-dsl publishes a solver for every ARC-AGI-1 training task but reports no benchmark percentage; any number attached to it is someone else's search procedure and must be sourced separately (https://github.com/michaelhodel/arc-dsl)."
related: [technique.brute-force-program-search, technique.latent-program-search]
---

# Hand-Crafted DSL + Search

**What it is.** Author a domain-specific language of primitives — Hodel's `arc-dsl` is
the reference artifact, ~160 primitives with a hand-written solver for each ARC-AGI-1
training task — then search compositions of those primitives for one consistent with the
demonstrations.

**The cognate.** A DSL is a *prior, made legible*. Everything the system can hypothesize
is something a person decided was a natural operation on the domain. That is its strength
against learned representations, where the same commitments exist but cannot be read off.

**Therefore.** Reach for it when you want the hypothesis space to be auditable and the
failure mode to be diagnosable — an unsolved task tells you exactly which primitive is
missing.

**Why there are no evidence rows.** `arc-dsl` states no score, and the register does not
borrow one. The published percentages attributed to "DSL search" belong to particular
search procedures over particular DSLs and are entered on those nodes, not this one.

**The limit.** Coverage is bounded by the author's imagination, and the search cost grows
with expressiveness — the two pressures run against each other, which is the whole reason
learned program spaces are attempted at all.
