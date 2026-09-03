# Contributing

## What this is not

- **Not a paper list.** A citation is not a node. A node is a claim about what a mechanism
  delivers for a named capability, with the evidence and the limits attached.
- **Not a leaderboard.** Scores appear only as evidence for a capability claim, always
  tagged with split and regime. If you find yourself ranking techniques by number, the
  register is being misused.
- **Not an endorsement list.** A refuted or disappointing technique is worth a node —
  see `techniques/recursive-latent-reasoners.md`, kept precisely because the scores are
  real and the explanation is not.

## Adding a node

1. Read `SCHEMA.md`. Copy the closest existing node as a template.
2. Write the frontmatter first. If you cannot fill `split` and `regime` for a number,
   you do not yet have the number — find the primary source or omit the claim.
3. Declare edges **only** on the technique, in `addresses:`. Never add a technique list
   to a capability; the reverse direction is derived.
4. Write `requires:` as tokens from `data/preconditions.yaml`, keeping your sentence in
   the `note:`. Reuse a token before adding one.
5. Type the pair against every technique that already covers the same capability, in
   `interacts:`. The builder's untyped co-coverage report names the pairs still owed.
6. Run `python3 scripts/build_graph.py`. It must exit 0.

## The evidence bar

| Stars | Meaning |
|---|---|
| `*` | argued in a paper; no reproduction |
| `**` | demonstrated once by its authors |
| `***` | reproduced independently |
| `****` | survived an adversarial ablation |

Three stars or more requires `kind: measured`. The validator enforces this.

**Claimed and measured are separate entries.** Where an independent measurement
disagrees with a published claim, both stay on the record. Keeping only the flattering
one is the failure this register exists to prevent.

**A combination is a claim too.** `interacts: rel: composes` says two techniques cover
more together than apart. That is an empirical claim and it carries the same burden as a
score: cite the source that measured the combination. Where none exists, the edge is
`overlaps` — the assumption that the coverage does not add — and the pair stays a
candidate rather than a result.

**Prose is a sentence, not a paragraph.** Each node has four moves — context, problem,
therefore, limit. If a section runs past a short paragraph, the node is probably two nodes.

## Say what put the node in view

Set `provenance.frame` to the instrument that surfaced it — the survey you were reading,
the taxonomy you were stocking from, the run that turned it up. Not why it is *good*;
what caused you to *see* it.

This register is curated, not sampled, and that is the right choice: a sampling frame
keyed to published ARC results would drop `dsl-search`, `hierarchical-task-networks`,
`mcts` and `means-ends-analysis`, which carry no comparable number and are load-bearing
anyway. The cost of curation is a selection effect, and the only honest treatment is to
make it visible: `build_graph.py --provenance` reports the corpus by frame. **Never argue
from the shape of this corpus to the shape of the field** without printing that report
first — and prefer a population you did not select when the claim is about the field.

## Empty cells are contributions

A capability with `status: open` and no incoming edge is a stated research gap. Adding a
well-specified empty capability is as valuable as adding a technique, and the gap report
(`build_graph.py`, run with no arguments) is the register's most useful single output.

## Adoption state stays out

`status` describes field-wide maturity. Whether *your* system has adopted something is
not a fact about the field. Keep that in a private overlay keyed by node `id`.
