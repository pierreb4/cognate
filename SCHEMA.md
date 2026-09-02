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
requires:                       # preconditions a user must be able to supply
  - gradient access to the weights
  - per-task inference compute
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
related: [technique.other]
```

### Rules the validator enforces

1. Every `evidence` entry has `split`, `regime`, `source`, `stars`.
2. `stars` is 1–4 and may not exceed 2 unless `kind: measured`.
3. `no_absolute_score: true` forbids any `evidence.claim` containing a `%`.
4. A `claimed` and a `measured` entry for the same split must both be present if the
   two disagree — you may not keep only the flattering one.
5. Every `addresses.capability` and every `part_of` / `completed_by` id must resolve.
6. An evidence entry without `date` is a **warning**, not an error — but a trend view
   silently drops it, so add one when you have it.

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
