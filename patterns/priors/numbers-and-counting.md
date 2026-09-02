---
id: priors.numbers-and-counting
kind: capability
name: Numbers and Counting
faculty: prior
human_source:
  - title: "Core knowledge (Spelke), via On the Measure of Intelligence §III.1.2"
    url: https://arxiv.org/abs/1911.01547
  - title: "Feigenson, Dehaene & Spelke, Core systems of number (TiCS, 2004)"
    url: https://pubmed.ncbi.nlm.nih.gov/15242690/
part_of: [priors]
completed_by: []
status: open
---

# Numbers and Counting

**Context.** A task turns on *how many* — three of one colour and four of another, the
largest group, the odd one out, a shape repeated n times.

**Problem.** Chollet lists this prior as elementary arithmetic and comparison over small
quantities: counting, ordering, sorting, and one-to-one correspondence. The human system is
two systems, not one — an exact representation of small sets of individuals, and an
approximate magnitude system for large ones — and the exact one is parasitic on object
individuation: you can only count things that have been separated into things. That
dependency is usually invisible in machine implementations because the counting primitive
is handed a segmentation.

**Therefore.** Do not treat counting as arithmetic bolted on after perception. It is a
commitment about what the perceptual front end must emit — discrete, individuated items —
and it fails silently when the front end emits regions instead.

**Status: open.** The only incoming edges are `incidental`, from
[`technique.dsl-search`], where counting exists because a person wrote the primitive. That
supplies the prior; it does not acquire it.
