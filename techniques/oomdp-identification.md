---
id: technique.oomdp-identification
kind: technique
name: Object-Oriented MDP Identification (DOORMAX)
addresses:
  - capability: exploration.experiment-design
    strength: direct
    note: >-
      the exploration bonus attaches to a prediction that is still unknown, never to a state
      that is merely unvisited — an action whose outcome every live prediction already agrees
      on returns nothing and is not taken
  - capability: modeling.belief-update
    strength: direct
    note: >-
      one contradicting transition falsifies a condition-effect prediction outright; under
      determinism the retraction is derived from the error rather than proposed and retried
  - capability: modeling.hypothesis-formation
    strength: partial
    note: >-
      the account is a set of condition-effect predictions per (action, attribute, effect type)
      that can be printed and pointed at — but it is stated in an object vocabulary the
      mechanism is given, not one it forms
requires:
  - token: expert-authored-library
    note: the object classes, attributes and relations, which the paper states are not learned
  - token: state-representation
    note: attributes and relations the conditions can be evaluated against
  - token: deterministic-environment
    note: falsification-on-a-single-counterexample depends on it; a stochastic outcome refutes nothing
  - token: interaction-budget
    note: identification is paid in environment actions taken before the policy is optimal
cost: medium
evidence:
  - claim: "529 steps before an optimal policy on Taxi 5x5, against 1676 for factored Rmax"
    kind: claimed
    split: taxi-5x5
    regime: 100-repetitions-averaged-six-probe-start-states
    source: https://carlosdiuk.github.io/papers/OORL.pdf
    stars: 2
    date: 2008-07-05
  - claim: "821 steps on Taxi 10x10 — 14.4x the state space for 1.55x the steps, against 11.85x for factored Rmax"
    kind: claimed
    split: taxi-10x10
    regime: 100-repetitions-averaged-six-probe-start-states
    source: https://carlosdiuk.github.io/papers/OORL.pdf
    stars: 2
    date: 2008-07-05
  - claim: "494 actions to learn the dynamics of Pitfall screen 1, after which the optimal policy it executes takes 94"
    kind: claimed
    split: pitfall-screen-1
    regime: single-run-deterministic-transitions
    source: https://carlosdiuk.github.io/papers/OORL.pdf
    stars: 2
    date: 2008-07-05
no_absolute_score: false
caveats:
  - "The object classes, attributes and relations are an INPUT. The paper's own future work asks that 'algorithms could also learn the object definitions and classes automatically, as well' — so this mechanism consumes objectness and state abstraction, it does not deliver them."
  - "Read in the unit an action-charged deployment actually spends — identification actions per optimal-completion action — the one case where the paper reports both terms is Pitfall: 494 against 94, a factor of 5.26. A regime that cuts an agent off at a small multiple of a human action count cannot pay that out of the same budget it is scored on."
  - "The 1.55x scaling is measured across more instances of ALREADY-KNOWN classes: the 10x10 Taxi varies size, not mechanics. The paper is silent on the cost of a new class, condition or effect type, which is the axis a benchmark of unseen games moves along."
  - "Across that same 14.4x state-space step, per-step time rose 21.16x (13.88ms to 293.72ms) and the advantage over factored Rmax fell from 3.14x to 1.04x."
interacts:
  - technique: technique.intrinsic-motivation-exploration
    rel: subsumes
    scope: exploration.experiment-design
    note: >-
      optimism about what cannot yet be predicted contains count-based novelty as the special
      case where "not yet predictable" is read as "not yet visited"; the two coincide only
      while every unvisited state is also unexplained
  - technique: technique.refinement-harness
    rel: overlaps
    scope: modeling.belief-update
    note: >-
      both revise in light of a failure, one by falsifying a prediction the evidence
      contradicts and one by re-prompting with the failure attached
---

# Object-Oriented MDP Identification (DOORMAX)

**What it is.** Represent the world as typed objects with attributes and relations, and keep,
for every (action, attribute, effect-type) triple, the set of conditions still consistent with
what has been seen. A single contradicting transition removes one. Act so as to resolve what is
still unknown; when nothing is unknown, stop exploring and plan.

**The cognate.** Experiment design, in the sense the register means it: the quantity being
maximised is the agent's own remaining ignorance, not the world's unvisitedness. This is the
first member the register holds for [`exploration.experiment-design`] that scores an action by
how far its outcome would discriminate between live accounts, which is precisely what a
novelty-driven explorer cannot do — and it is why the bundle
[`bundle.theory-test-update`] previously had an empty leg.

**Therefore.** Where the environment is deterministic and an object vocabulary can be authored,
falsification is cheap and exact: no ensemble is needed to estimate disagreement, because under
determinism a prediction is either still live or dead.

**The limit, and it is severe.** The object vocabulary is supplied. The paper says so itself in
its future work, so the mechanism answers none of the three capabilities that would give it that
vocabulary — objectness, state abstraction, goal inference. And the identification is paid in
actions: 494 on Pitfall against a 94-action optimal path. In a deployment that charges for
exploration out of the same budget it scores, that ratio is the whole question, and this
mechanism does not answer it either.
