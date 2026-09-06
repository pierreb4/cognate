---
id: hypothesis.cost-decay
kind: hypothesis
name: Costs Age
claim: >-
  A price in this register decays after the date it was measured, and not at one rate: the
  dollars to reach a fixed capability through a vendor API fall fast, an accelerator-hour
  falls slowly or not at all and not in one direction across vendors, and a competition cost
  cap does not fall by construction. So a `cost:` band read years later overstates what the
  same result would cost today, two bands of different vintages are not comparable without a
  deflator, and one deflator for all three currencies would be wrong for two of them.
source: https://github.com/pierreb4/cognate/blob/main/data/deflators.yaml
date: 2026-09-06
status: argued
stars: 1
bears_on:
  - all
predicts:
  - claim: >-
      re-priced at today's date, some priced rows fall into a cheaper band than their node's
      label — and the labels that move are api-usd-per-task rows, not gpu-hour ones
    check: build_graph.py --as-of <today>, comparing the printed band against the node's `cost:`
  - claim: >-
      the same capability level appears later in the corpus at a lower price, on rows the
      register did not select for price
    check: >-
      build_graph.py --trend <split>, reading `regime:` prices in date order within one split
  - claim: >-
      a technique whose only cost witness is a competition cap keeps its band as the cap is
      re-issued, while an api-priced neighbour's band falls under it
    check: the `cost:` labels of test-time-training against refinement-harness, across revisions
  - claim: >-
      if this is right, `leverage: computation` techniques become admissible under a fixed
      budget over time without any change to the technique
    check: >-
      build_graph.py --profile <id> at a fixed budget, re-run after banking a deflator; the
      OVER BUDGET list should shrink from the computation side first
history:
  - as_of: '2026-09-06'
    status: argued
    source: https://epoch.ai/data-insights/llm-inference-price-trends
    note: >-
      first fetch, and it split the claim in two. The API half is SOURCED and contested
      between primaries: Epoch AI (2025-03-12) reports prices at a fixed benchmark threshold
      declining 9x to 900x per year with a median of 50x, across six benchmarks; Gundlach,
      Lynch, Mertens & Thompson (MIT FutureTech, arXiv 2511.23455 v2, 2026-03-23) report 5x
      to 10x per year at fixed benchmark performance and say so against Epoch directly. Both
      end before 2026, so every current re-pricing is extrapolated. The GPU half is PARTLY
      REFUTED as stated: there is no single accelerator-hour index to deflate by. Over
      2024-07 to 2026-09 AWS cut A100 40GB $4.10 -> $2.74 and H100 80GB $12.29 -> $6.88 while
      leaving L4 at $0.8048 unchanged to the cent; Lambda's on-demand LIST prices rose on
      every class checked (A100 80GB $1.79 -> $2.79); RunPod Secure fell mildly. On
      2026-09-06 an H100 80GB hour spans about 2.5x across vendors. "GPU compute keeps
      getting cheaper" is true of one vendor's large parts and false of another's list, so
      `gpu-hour-price` is banked as evidence and declines to deflate. A widely repeated
      "200x per year since January 2024" is not on the Epoch page (grep of the raw capture)
      and is not carried.
  - as_of: '2026-09-06'
    status: argued
    source: https://github.com/pierreb4/cognate
    note: >-
      entered with the deflator mechanism and NO banked series, which is the point: the claim
      is stated and checkable before any number is fetched, so the fetch cannot be steered by
      the answer it is wanted for. `--as-of 2026-09` currently re-prices 0 of 10 priced rows.
      The corpus holds 4 api-usd-per-task rows (2025-09 to 2026-06), 4 gpu-hour rows (2023-12
      to 2026-09) and 2 fixed-cap rows, so the first prediction is testable on 4 rows only —
      too few to settle it, enough to falsify it if the bands do not move.
provenance:
  entered: 2026-09-06
  frame: kaggle-sweep-2026-09
  note: >-
    raised by Pierre reading the cost-band fix: the bands are checkable against the rows now,
    but a row's dollars age and the label does not say from when
---

# Costs Age

**The claim.** `cost:` is nominal. A `high` from 2023 and a `high` from 2026 are different
claims about the world, and the register prints them in the same column.

**Why it is held as a hypothesis and not as a rule.** The decay is real but its rate is
contested and differs by currency, and this register's own corpus is far too small to
measure it: four rows priced in API dollars, four in hardware-hours, two caps. Holding the
claim as a node means the rate must be fetched from a primary and banked in
`data/deflators.yaml` with a date and a source, exactly as an evidence row is — rather than
a constant being assumed inside a script where nobody can see its vintage.

**What would refute it.** `--as-of` moving no band on the API-priced rows; or the gpu-hour
rows moving as fast as the API rows, which would mean the three-currency split is
unnecessary and one rate would do.

**Where it stops.** A deflator says what a run would cost today at the same capability. It
says nothing about whether the technique is worth running, and it must never be used to
edit a row: the register's ability to say "this is what was actually paid, on this date"
is the thing that makes the question askable at all.
