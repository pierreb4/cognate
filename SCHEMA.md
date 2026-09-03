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
cost: low | medium | high | extreme
evidence:
  - claim: "53.0% on ARC-AGI-1 public eval"
    kind: claimed | measured        # measured = independently reproduced
    split: arc-agi-1/public-eval    # REQUIRED — the exact set
    regime: uncapped                # REQUIRED — cost cap, compute budget, or 'uncapped'
    source: https://arxiv.org/abs/2411.07279
    stars: 3
    date: 2024-11-11            # when the claim was made or measured (ISO); enables trend views
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
