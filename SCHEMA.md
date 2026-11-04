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
faculty: exploration            # exploration | modeling | goal-setting | planning-execution | prior | learning
human_source:                   # where the concept is characterized in cognitive science
  - title: Curiosity and Exploration
    url: https://oecs.mit.edu/pub/...
part_of:     [exploration]          # the larger context this serves ("up" in Alexander)
completed_by: [exploration.novelty-memory]   # patterns that finish this one ("down")
status: open | partial | covered    # FIELD-WIDE maturity, not any project's adoption
```

Capabilities never list techniques. That edge is derived.

**The `learning` faculty (2026-10-20).** The other five faculties are inference-time: what a
trained system does with a task in front of it. `learning` holds what a system's learning
procedure produces across its lifetime — how much data it needed, what priors it acquired,
what it kept from one exposure, what it carried from one episode to the next — and a technique
addresses a `learning` cell through that procedure. It stays apart from
`modeling.per-task-adaptation`, which is adaptation within one episode: the frontier closed
per-task adaptation over 2024-26 while the data gap to human learners widened, and one faculty
holding both would hide that. Compute and energy budgets are not cells; they are the `regime`
of a `learning.sample-efficiency` row.

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
    human_baseline:             # optional; expected whenever the claim compares with humans
      n: 42                     # people in the baseline
      population: human players' recorded games, first exposure
      aggregation: individual-mean   # | panel-union | majority-of-<k> | median-of-completers | percentile-<k>
      same_items: true          # the people saw the items the machine was scored on
      source: https://arxiv.org/abs/2510.20886
      note: optional, one line
no_absolute_score: false        # true if the work publishes only relative claims
caveats:
  - one line, with a source
interacts:                      # technique <-> technique, declared once (see below)
  - technique: technique.other
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: one line on why
```

### `human_baseline:` — a human figure is an axis too

`split` and `regime` exist so that two numbers on different axes are never ranked together.
A human baseline has the same problem. One name covers an individual's average (H-ARC's
64.2%), the union of a panel where a task counts as solved once two people solve it
(ARC-AGI-2's "100%"), a majority vote of three annotators (IntPhys 2), the median player who
completed a level (ARC-AGI-3) and an 80th-percentile person (AutumnBench). A review of 115
human baselines in model evaluations found a median of 8 people and a significance test in
8.7% of them ([arXiv 2506.13776](https://arxiv.org/abs/2506.13776)). A row that says "above
human" and carries none of this cannot be compared with another that says the same.

So an evidence row whose claim compares with people carries `human_baseline:` with `n`,
`population`, `aggregation` (one of `individual-mean`, `panel-union`, `majority-of-<k>`,
`median-of-completers`, `percentile-<k>`, with `k` a number), `same_items` and `source`, and
optionally a `note`. Two human-comparison rows with different `aggregation` are not ranked
against each other, for the same reason two `regime`s are not. The field is optional so that
existing rows stay valid: `build_graph.py` warns, and does not fail, on a row whose `claim`
mentions humans without it, and fails on a `human_baseline` that is malformed.

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
`composes` measures what the source measures: tasks solved on the named split by the
combination against each member alone. It does not require either arm to reach `direct` or
`partial` on the scope — a member `incidental` there (a bare output predictor on
hypothesis-formation) still adds solved tasks, and that is the claim. The combination's
GRADE on the scope stays the best member's `addresses` strength; `grade_combination.py`
reads `addresses` and never `composes`. An operator applied to a substrate (test-time
training on a transductive model) is `composes` too, on the row that measures the gain.

Symmetric relations are declared **once**, on the alphabetically-first technique id; the
reverse is derived, the same discipline `addresses:` follows. `subsumes` and `supplies`
are declared on the source and derive as `subsumed_by` / `supplied_by`.

Two techniques that address the same capability at `direct` or `partial` strength with no
declared interaction appear in the builder's **untyped co-coverage** report. That is a
to-do list: until the pair is typed, no combination containing both can be graded.

### The supplied / acquired test

Seven capabilities — the five `priors`, `modeling.state-abstraction` and
`goal-setting.goal-inference` — name a thing a system must *have* before the rest of the
register's machinery can run: objects, physics, agents, geometry, number, a stable
identity across frames, an objective. For those cells the grading question is not whether
the system HAS the thing. It is **where the thing came from.** Since 2026-10-20 that
question is also a cell of its own, `learning.prior-acquisition`, which asks how much
experience the acquiring took against a child's; the grading rule below is unchanged.

- **`direct` / `partial`** — the system ACQUIRES it from what it observes.
- **`incidental`** — the system is HANDED it, as an authored primitive, a hand-written
  vocabulary, a demonstration pair that *is* the objective, a fixed input the paper's own
  future-work section admits it does not derive, **or a supervised training target that IS
  the graded capability** (track ids for identity, instance masks for objectness). The
  capability is consumed, not produced.

**The distance rule.** Training supervision does not disqualify by being supervision; what
matters is how far the supplied artifact sits from the graded capability. If the supplied
artifact IS the capability, the grade is `incidental` — a tracker trained on annotated
track ids has identity transferred from a human, however good its numbers. If it is
strictly UPSTREAM and the system performs the step that produces the capability, the grade
caps at `partial` and the dependency is named as a precondition token rather than
rejecting the technique. `technique.counterfactual-probe-segmentation` trains against
SeaRAFT optical flow — correspondence, one level below the persisting index — and carries
`correspondence-estimator`. `technique.temporal-feature-similarity-slots` predicts affinity
in a frozen DINO feature space and carries `frozen-self-supervised-features`. Neither is
handed the thing it is graded on; both are capped for what they are handed.

The gap report has three states, and `incidental` edges count as hits: a cell reads EMPTY
when NO technique addresses it at any strength, INDIRECT when it has edges but none at
`direct`, and is otherwise covered (`gap_report` in `scripts/build_graph.py`). So a cell
whose every candidate is a consumer reads INDIRECT with its edge count, not EMPTY — the two
served priors below are the case — and only a cell nobody has tried reads EMPTY.
`technique.dsl-search` is the worked case, capped at `incidental` on two served priors
because it "supplies the prior as authored primitives (rotate, reflect, connect, fill)
rather than acquiring it".

This is the second cell-family whose grading rule was being applied uniformly and written
nowhere; `modeling.hypothesis-formation` carries the other one (*exhibitable commitment*)
in its own node. Both look like instances of a single ladder — does the technique PRODUCE
the capability or CONSUME it — but two families is not enough to declare one, and
`SCHEMA.md` still defines `direct | partial | incidental` for the remaining cells nowhere.

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

A frame is declared by use: there is no list of frames, and every node a frame brings in
carries the same `frame` and the same `note`, because `--provenance` prints one note per frame.
When the instrument is a dated literature survey, the survey is kept in `surveys/` (never
parsed) and the note names its file, so a reader can open what the instrument was reading.

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



---

*Split on 2026-11-04 so each file reads whole: what follows moved word for word to 1 part beside this file, each heading below linking to its place. Line numbers cited before that day are the whole file's: `git show 9af47e1:SCHEMA.md`.*

### `cost:` — the per-task inference price band

→ [part 2](SCHEMA-part-2.md#cost--the-per-task-inference-price-band)

#### `cost:` ages

→ [part 2](SCHEMA-part-2.md#cost-ages)

### `kind: hypothesis`

→ [part 2](SCHEMA-part-2.md#kind-hypothesis)

### `arrival:` on a capability

→ [part 2](SCHEMA-part-2.md#arrival-on-a-capability)

### `requires_beyond:` — the result cost more than the mechanism

→ [part 2](SCHEMA-part-2.md#requires_beyond--the-result-cost-more-than-the-mechanism)

### Quantities: `limit` and `demand`

→ [part 2](SCHEMA-part-2.md#quantities-limit-and-demand)

### Rules the validator enforces

→ [part 2](SCHEMA-part-2.md#rules-the-validator-enforces)

## `kind: bundle`

→ [part 2](SCHEMA-part-2.md#kind-bundle)
