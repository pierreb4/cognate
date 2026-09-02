---
id: technique.latent-program-search
kind: technique
name: Latent Program Search (LPN)
addresses:
  - capability: modeling.hypothesis-formation
    strength: direct
    note: the hypothesis is an explicit latent, searchable by gradient, without a hand-written DSL
requires:
  - a learned latent space over programs
  - test-time gradient search
cost: medium
evidence:
  - claim: "Test-time search doubles out-of-distribution performance relative to no search"
    kind: claimed
    split: not-applicable
    regime: uncapped
    source: https://arxiv.org/abs/2411.08706
    stars: 1
no_absolute_score: true
caveats:
  - "Frequently cited as though it carried an ARC percentage. It does not. Any ARC number attributed to LPN is someone else's reimplementation and must be sourced separately."
related: [technique.test-time-training]
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
