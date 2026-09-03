# Schema

One node per file. YAML frontmatter is the source of truth; the prose below it is for
humans and is never parsed. `scripts/build_graph.py` validates every field and emits
`data/graph.json`.

Edges are declared **once**, on the technique. `build_graph.py` derives the reverse
edge onto the capability, so the forward and reverse directions cannot disagree.

## Common fields

```yaml
id:    exploration.frontier-seeking   # dotted, stable, never reused after deletion
kind:  capability | technique | bundle
name:  Frontier Seeking               # human-readable, title case
```

## `kind: capability`

A named cognitive requirement, stated so that a system either meets it or does not.

```yaml
faculty: exploration            # exploration | modeling | goal-setting | planning-execution | prior
human_source:                   # where the concept is characterized in cognitive science
  - title: Curiosity and Exploration
    url: https://oecs.mit.edu/pub/...
part_of:     [exploration]          # the larger context this serves ("up" in Alexander)
completed_by: [exploration.novelty-memory]   # patterns that finish this one ("down")
status: open | partial | covered    # FIELD-WIDE maturity, not any project's adoption
```

Capabilities never list techniques. That edge is derived.

## `kind: technique`

A named machine mechanism.

```yaml
addresses:                      # the forward edge — the only place it is written
  - capability: modeling.per-task-adaptation
    strength: direct | partial | incidental
    note: one line on what it actually delivers
requires:                       # preconditions, as tokens from data/preconditions.yaml
  - token: weight-gradients
    note: gradient access to the weights (rules out closed API-only models)
  - token: per-task-compute
    note: per-task inference compute
leverage: knowledge | computation | both   # REQUIRED — see below
cost: low | medium | high | extreme
evidence:
  - claim: "53.0% on ARC-AGI-1 public eval"
    kind: claimed | measured        # measured = independently reproduced
    split: arc-agi-1/public-eval    # REQUIRED — the exact set
    regime: uncapped                # REQUIRED — cost cap, compute budget, or 'uncapped'
    source: https://arxiv.org/abs/2411.07279
    stars: 3
    date: 2024-11-11            # YYYY, YYYY-MM or YYYY-MM-DD — partial is honest where that
                                # is all the source supports (an arXiv id fixes the month of
                                # v1 and no more); a trend view can still order by it
no_absolute_score: false        # true if the work publishes only relative claims
caveats:
  - one line, with a source
interacts:                      # technique <-> technique, declared once (see below)
  - technique: technique.other
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: one line on why
```

### `requires:` is a token, not a sentence

A precondition written as prose cannot be screened. Every entry cites a `token` from
`data/preconditions.yaml` — the closed vocabulary — and keeps the original sentence in
`note:`. That is what lets a project state what it can supply and have the register
answer *which techniques are admissible here at all* mechanically.

Tokens carry a `kind`: `artifact` (you must build or hold it), `resource` (compute or
budget), `environment` (a property of the deployment, not yours to choose), `human`
(ongoing labour), `assumption` (a domain-fit claim that can only be checked, never
supplied — a screen reports these, it does not fail on them).

Adding a token is a real edit to the vocabulary: reuse before you extend, and never add
one that names a single technique's implementation detail.

### `interacts:` — the technique-to-technique edge

`addresses:` says what a technique gives you. `interacts:` says what it gives you *that
another one does not* — the question a combination must answer before anyone builds it.

| `rel` | Direction | `scope` | Means |
|---|---|---|---|
| `overlaps` | symmetric | capability | both address it; assume coverage does **not** add |
| `composes` | symmetric | capability | coverage measurably adds — requires `evidence:` |
| `subsumes` | source → target | capability | source is strictly stronger there and contains the target's mechanism; the target is removable |
| `supplies` | source → target | precondition token | the source produces something the target requires — the synergy case |
| `conflicts` | symmetric | either | the two cannot co-exist in one system |

`overlaps` is the default for co-coverage, and it is the conservative one: it says a
combination holding both is no better covered than one holding either. Upgrading a pair
to `composes` is a claim about a measured combination and needs a source, exactly as an
evidence entry does. If you cannot cite one, the honest edge is `overlaps`.

Symmetric relations are declared **once**, on the alphabetically-first technique id; the
reverse is derived, the same discipline `addresses:` follows. `subsumes` and `supplies`
are declared on the source and derive as `subsumed_by` / `supplied_by`.

Two techniques that address the same capability at `direct` or `partial` strength with no
declared interaction appear in the builder's **untyped co-coverage** report. That is a
to-do list: until the pair is typed, no combination containing both can be graded.

### `provenance:` — what put the node in view

```yaml
provenance:
  entered: 2026-09-02          # when it entered the corpus
  commit: 6f81060              # the commit that added it
  frame: arc-prize-2025-taxonomy   # THE INSTRUMENT that surfaced it
  note: >-                     # one line on what that instrument was reading
```

Optional, and it describes the register rather than the field, so it never affects a
grade. It exists because a curated pattern language is evidence about its authors before
it is evidence about anything else: `frame` names the instrument a node came through, so
`build_graph.py --provenance` can report how much of the corpus one instrument supplied.
Any distributional reading of this corpus — see `hypotheses/` — must state that number
before it states its own. A frame holding most of the corpus is the corpus's blind spot,
and the register would rather print that than pretend to be a sample.

### `leverage:` — which side of the bitter lesson a technique sits on

- `knowledge` — performance is bounded by human-authored content; more compute alone does
  little
- `computation` — performance improves with compute or data without new authored content
- `both` — needs authored content *and* scales with compute

It is **declared, never derived**. An earlier attempt to infer it from `requires` tokens got
`evolutionary-program-synthesis` wrong, because that node's tokens and its evidence
disagreed — the same disagreement `requires_beyond` now records. A technique whose side you
cannot state is one you do not understand well enough to grade, so the validator requires it.

`--trend [split]` orders dated evidence by this axis, and `--profile` cross-tabulates it
against admissibility. That is what turns a much-cited essay into a query over the corpus.

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
