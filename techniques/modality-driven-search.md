---
id: technique.modality-driven-search
kind: technique
name: Modality-Driven Search
addresses:
  - capability: modeling.hypothesis-formation
    strength: partial
    note: text, image and code are treated as parallel search operators over one task, so the representation is a search dimension rather than a fixed design choice
  - capability: modeling.per-task-adaptation
    strength: incidental
    note: all the adaptation is inference-time routing between representations, with no per-task fitting
requires:
  - token: multimodal-model
    note: a model that accepts and emits more than one modality
  - token: candidate-arbiter
    note: a judge that can compare candidates produced in different representations
  - token: parallel-inference-budget
    note: parallel inference budget
leverage: computation
cost: high
evidence:
  - claim: "72.9% on ARC-AGI-2 semi-private using text, image and code as parallel search operators plus a judge"
    kind: claimed
    split: arc-agi-2/semi-private
    regime: $38.99-per-task
    source: https://arxiv.org/abs/2606.31543
    date: 2026-06
    stars: 2
no_absolute_score: false
caveats:
  - "UNVERIFIED SOURCE: the arXiv identifier above was reported to this register second-hand and has not been fetched and confirmed here. Treat the row as provisional until the identifier is checked against arxiv.org."
interacts:
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      parallel candidates judged against a single account narrowed by refutation; the first
      needs a judge it can trust, the second needs no judge at all
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
---

# Modality-Driven Search

**What it is.** Rather than picking a representation for the task, run several — a natural
language description, a rendered image, an executable program — as parallel operators in
one search, and let a judge choose among what they produce.

**The cognate.** It generalizes the finding on
[`technique.induction-transduction-ensemble`]. If two representations solve disjoint task
sets, the representation is not a design decision to be made once; it is a dimension the
search should be moving along.

**Therefore.** Where you already run an ensemble, consider making the representation an
explicit search operator with a judge over it, rather than a fixed pair of models with a
combination rule.

**Read the caveat first.** This node carries the register's highest reported number and its
weakest sourcing. The percentage came in with a citation that has not been independently
resolved, and until it is, the row is provisional — which is exactly the situation the
`caveats` field exists for.
