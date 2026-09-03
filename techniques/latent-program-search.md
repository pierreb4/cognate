---
id: technique.latent-program-search
kind: technique
name: Latent Program Search (LPN)
addresses:
  - capability: modeling.hypothesis-formation
    strength: direct
    note: the hypothesis is an explicit latent, searchable by gradient, without a hand-written DSL
requires:
  - token: learned-latent-space
    note: a learned latent space over programs
  - token: weight-gradients
    note: test-time gradient search
  - token: per-task-compute
    note: the search budget that gradient search spends per task
leverage: computation
cost: medium
evidence:
  - claim: "Test-time search doubles out-of-distribution performance relative to no search"
    kind: claimed
    split: not-applicable
    regime: uncapped
    source: https://arxiv.org/abs/2411.08706
    date: 2024-11
    stars: 1
no_absolute_score: true
caveats:
  - "Frequently cited as though it carried an ARC percentage. It does not. Any ARC number attributed to LPN is someone else's reimplementation and must be sourced separately."
interacts:
  - technique: technique.llm-sampling-program-synthesis
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      a latent searched by gradient against programs sampled from a model; the latent is
      cheaper to search and cannot be read, which is the trade the register keeps recording
  - technique: technique.modality-driven-search
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      one continuous space searched against several discrete ones compared; no capability is
      covered twice by holding both
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      an optimized latent against an accumulated rule set; the second can say what it
      believes and the first cannot, at equal coverage of this capability
  - technique: technique.test-time-training
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both run gradient descent per task to reach an instance-specific account; only the
      latent one can be read back, which is why the two differ by two strength steps here
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
---

# Latent Program Search (LPN)

**What it is.** Learn a latent space in which points decode to programs, then search that
space by gradient at test time. It sits between DSL search (explicit, hand-built,
enumerable) and test-time training (implicit, in weights, uninspectable): the hypothesis
is explicit enough to be optimized, without anyone having to author a DSL.

**The cognate.** This is the closest published counterpart to *forming a hypothesis in a
space you learned rather than one you were given* — the thing that makes
[`modeling.hypothesis-formation`] more than program enumeration.

**Why the `no_absolute_score` flag.** The paper publishes a relative claim only. It is
included at one star, and the flag is the point: an entry with no comparable number is
more useful stated as such than quietly omitted, because omission is what lets a
borrowed number circulate.
