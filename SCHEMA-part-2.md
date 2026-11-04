<!-- Part 2 of 2 of SCHEMA.md, moved there word for word on 2026-11-04. -->
[← SCHEMA.md](SCHEMA.md) · [← part 1](SCHEMA.md) · part 2 of 2

### `cost:` — the per-task inference price band

`cost:` is what one task costs to RUN with the technique, in USD per task, at the price the
node's best published number was bought for. Four bands, upper bound inclusive:

| band | per task |
|---|---|
| `low` | up to $1 |
| `medium` | $1 to $10 |
| `high` | $10 to $100 |
| `extreme` | above $100 |

Training, pretraining and authoring spend are NOT in it — they are named in `requires:`
(`trained-model`, `training-distribution`, `expert-authored-library`) and, when a result cost
more than the mechanism, in `requires_beyond:`. A one-value label cannot carry two currencies,
and the 2026-09-06 audit found it carrying neither consistently: a `cost: medium` node held a
`$30.57-per-task` row and a `cost: extreme` node held `$3.97-per-task`.

The label is checked against the rows. Any evidence row whose `regime:` prices the run in
dollars per task (`$30.40-per-task`, `kaggle-2025-cost-cap-~$0.20/task`) is parsed, and the
label must equal the band of the DEAREST such row — cheaper rows may sit below it and say so
in their own `regime:`, but the label answers "what must I be prepared to pay for the best
number here". Where no row is priced in $/task the label is the author's estimate from the
regime strings and is not checked; a node that wants its label enforced prices a row.
`grade_combination.py` reads the label as the combination's heaviest member tier.

#### `cost:` ages

The band is nominal. It records what a task cost in the dollars of the row's `date:`, and
nothing rewrites it later — a measured row is a primary fact, and a label that drifted on a
schedule would stop being checkable against the row that justifies it. But compute gets
cheaper, so a 2023 `high` and a 2026 `high` are not the same claim, and a reader comparing
them is comparing two vintages without being told.

The register's answer is to deflate at QUERY time and never in the data.
`build_graph.py --as-of <date>` re-reads every priced row in the dollars of that date and
prints the nominal price beside the deflated one, with the band each implies, so a label
moved by ageing alone is visible. The series live in `data/deflators.yaml`, each a dated,
sourced claim held to the same standard as an evidence row: a rate quoted from a blog citing
a primary does not enter.

Three currencies age at three rates, so one rate would be wrong for two of them. A row's
currency is read off its `regime:` string:

| currency | example `regime:` | what moves |
|---|---|---|
| `api-usd-per-task` | `$30.57-per-task` | the price of the CAPABILITY: vendor cuts, and cheaper models reaching the same threshold. The fast curve |
| `gpu-hour` | `~12h-per-100-tasks-1xA100` | the price of an hour of that class. The register stores the hours, which do not change |
| `fixed-cap` | `kaggle-2025-cost-cap-~$0.20/task` | nothing. A cap is a rule, not a price, and is never deflated. What changes is what it BUYS, which the regime string already records |

A cap still witnesses a band, because it bounds what was paid: `test-time-training` reads
`cost: low` on the strength of a ~$0.20/task cap.

**A series holds BASES, because the sources disagree and the disagreement is the finding.**
One basis per primary or per vendor, each naming the span it actually measured
(`covers_from` / `covers_to`). `status: contested` makes the view print a RANGE across
bases and never a point estimate, and a date outside a basis's span prints EXTRAPOLATED.
Both API primaries banked here stop before 2026 while the corpus holds 2026 rows, so every
current re-pricing is extrapolated and says so. Two points a year apart ARE a rate, and the
view reads between and beyond them log-linearly; it never invents a basis the sources do not
support.

A series may also decline to deflate at all. `competition-cost-cap` does so because a cap is
nominal by construction. `gpu-hour-price` does so because the 2026-09-06 fetch found no
single index to deflate BY: over 2024 to 2026 one vendor cut A100 by a third and H100 by 44%
while leaving L4 unchanged to the cent, another vendor's on-demand LIST PRICES ROSE on every
class checked, and on one day the same chip spans about 2.5x across vendors. Its points are
banked as evidence of that spread and read by hand. A series with no fetched primary is
`status: unbanked`, holds no points, and prints NOT BANKED — the honest state, enforced in
both directions.

### `kind: hypothesis`

A dated, sourced, falsifiable claim **about the register's own contents** — held as a node so
it can be checked and moved rather than assumed. `predicts:` is required: each entry pairs a
`claim` with the `check` that would test it against the corpus. A hypothesis with nothing to
predict cannot earn its place, and `status: argued` may not exceed two stars, exactly as an
argued technique claim may not.

### `arrival:` on a capability

```yaml
arrival: engineered | emergent-claimed | emergent-demonstrated | contested
emerges_from: [technique.x]    # REQUIRED unless `engineered` — the named carrier
arrival_source: https://...    # REQUIRED unless `engineered`
arrival_date: '2026-01'
```

`EMPTY` in the gap report used to be ambiguous between *nobody has built a mechanism for
this* and *this arrives as a byproduct of scaling something else*. Those call for opposite
actions, so the field forces the choice, and the gap report prints it.

Anything but `engineered` must name a carrier. "It might emerge" with no technique attached
is a claim that can never lose, and would become the field that launders every empty cell.

### `requires_beyond:` — the result cost more than the mechanism

A technique's `requires:` describes the *family*. A published result is one *instance* of
it, and the instance often needed more than the family does. Genetic programming does not
require a language model; every published evolutionary-synthesis result on ARC does.

```yaml
evidence:
  - claim: "SOAR: 52% of the ARC-AGI-1 public set, evolutionary search plus hindsight fine-tuning"
    ...
    requires_beyond: [llm-inference, weight-gradients]   # what THIS result needed
```

The screen then separates two questions a single admissibility verdict used to blur: *can
this deployment run the mechanism* and *can it reproduce the number*. Where they differ it
says so — "the MECHANISM is admissible, but 3 of 3 published results are not" — and a
combination's evidence floor counts only results this deployment could actually reproduce.

Without this the register quietly overstates what a constrained deployment can reach. It
was found by trying to classify techniques as knowledge-side or scale-side and getting the
wrong answer for a node whose tokens and whose evidence disagreed.

### Quantities: `limit` and `demand`

A precondition is usually yes/no. Some are a *budget*, and there the interesting question is
not whether the deployment has any but whether it has enough. A token in
`data/preconditions.yaml` may declare a `unit:`; only such a token can carry a number.

```yaml
# on a technique, in `requires:` — what the mechanism is published to cost
  - token: interaction-budget
    demand: 5.26
    unit: actions-per-human-baseline-action
    measured_on: pitfall-screen-1        # the split it was measured on
    source: https://...

# on a profile, in `supplies:` — what the deployment allows
  - token: interaction-budget
    limit: 5
    unit: actions-per-human-baseline-action
    as_of: '2026-04-17'                  # the version of the rule this is
    checked: '2026-09-03'                # when someone last read the source
    source: https://...
    history:                             # superseded values, never deleted
      - as_of: '2026-03-24'
        limit: 5
        source: https://...
        note: what changed, and what did not
```

The screen compares the two only when the units match, and reports `OVER BUDGET` — a
bucket of its own, distinct from `BLOCKED`, because a mechanism refuted by arithmetic is a
different object from one that cannot run at all.

**Three disciplines, and they are the point of the feature.**

*Vintage.* `as_of` is which version of the rule this is; `checked` is when a human last
read the source. A benchmark's scoring rules change, and a screen run against last
quarter's budget is not wrong so much as undated. Superseded values go in `history` with a
note saying what changed — deleting them would erase the reason an older verdict differed.

*Frame.* `measured_on` names the split the cost was measured on. A profile may list
`own_splits:`; a demand measured anywhere else is printed as **indicative, not a verdict**.
Comparing a cost measured on one domain against a budget set for another is the same error
the evidence schema already forbids for scores, and the screen says so on every line rather
than quietly doing the arithmetic.

*Contingency.* Where an over-budget technique would have covered a capability better than
anything admissible, the screen prints that under `CONTINGENT ON A BUDGET QUESTION` with the
margin. Coverage that turns on a number should be visible as such, not rounded to zero.

### Rules the validator enforces

1. Every `evidence` entry has `split`, `regime`, `source`, `stars`.
2. `stars` is 1–4 and may not exceed 2 unless `kind: measured`.
3. `no_absolute_score: true` forbids any `evidence.claim` containing a `%`.
4. A `claimed` and a `measured` entry for the same split must both be present if the
   two disagree — you may not keep only the flattering one.
5. Every `addresses.capability` and every `part_of` / `completed_by` id must resolve.
6. An evidence entry without `date` is a **warning**, not an error — but a trend view
   silently drops it, so add one when you have it.
7. Every `requires.token` resolves in `data/preconditions.yaml`; a bare prose entry is
   an error.
8. `interacts.rel` is one of the five above, the target is another technique, and the
   pair is declared exactly once.
9. A symmetric relation declared on the second id is an error — declare it on the first.
10. `subsumes` requires the source's `strength` on `scope` to be strictly greater than
    the target's. `supplies` requires `scope` to be a token the target actually
    `requires`. `composes` requires `evidence:`.
11. Every technique declares `leverage`. A capability's `arrival`, if not `engineered`,
    names `emerges_from`, `arrival_source` and `arrival_date`. A hypothesis carries
    `claim`, `source`, `date`, `status`, `stars` and a non-empty `predicts`.
12. `date` is `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. A missing date on a scored entry warns; a
    `not-applicable` split is exempt. A `source` that is a bare domain warns — it does not
    cite the result.
13. A `limit` or `demand` may only sit on a token that declares a `unit`, must state that
    same unit, and must be a positive number. A `limit` needs `as_of`, `checked` and
    `source`; a `demand` needs `measured_on` and `source`; a `history` entry needs
    `as_of`, `source` and `note`.
14. `cost` is one of `low | medium | high | extreme`, and if any evidence row's `regime`
    prices the run in $/task the label equals the band of the dearest such row.
15. Each deflator series in `data/deflators.yaml` names a currency `build_graph.py` can
    read off a `regime`, and one currency has one series. An `unbanked` series holds no
    points; `contested` needs at least two bases, because one source is not a disagreement;
    every basis carries `source`, `covers_from`, `covers_to` and a `note`, and a deflating
    one holds at least two dated points. Every point cites a declared basis and carries
    `as_of`, a positive `value` and a `source`. Deflation never moves a `cost:` label:
    rule 14 checks the label in the nominal dollars of each row's `date:`, and the band
    `--as-of` implies is printed beside it, never written back (`refinement-harness` reads
    `medium` at 2026-09 on ageing alone and stays labelled `high`).
16. Profiles that name the same `competition:` carry identical `binding: competition`
    rows: the same tokens, each row equal field for field. Two lineages of one entry copy
    the competition's rules, and a re-read that edits one copy alone is an error.
17. An evidence row whose `claim` contains "human" and has no `human_baseline` is a
    **warning**. A `human_baseline` that is present must carry a positive integer `n`, a
    `population`, an `aggregation` from the list above, a boolean `same_items` and a
    `source`, and no other field than an optional `note`.

## `kind: bundle`

A minimal set of techniques that jointly satisfy a cluster of capabilities. Bundles are
the forward-direction answer: *given this requirement, what is the least I must build?*

```yaml
satisfies: [modeling.hypothesis-formation, exploration.experiment-design]
members:
  - technique: technique.mcts
    load_bearing_for: [exploration.experiment-design]
minimality: argued | tested     # 'tested' requires an ablation showing each member matters
does_not_give:                  # honest negative space
  - transfer across environments
```

`minimality: tested` without a cited ablation is a validation error.
