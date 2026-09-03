---
id: technique.evolutionary-program-synthesis
kind: technique
name: Evolutionary Program Synthesis
addresses:
  - capability: modeling.hypothesis-formation
    strength: direct
    note: the population holds many specific, executable accounts at once, each refutable against the demonstrations
  - capability: modeling.belief-update
    strength: partial
    note: a failing candidate is mutated in light of its own execution trace — revision, not just rejection; but the revision is proposed, not derived from the error
requires:
  - token: per-candidate-executor
    note: an executor giving per-candidate feedback on the demonstration pairs
  - token: mutation-operator
    note: a mutation or recombination operator over the program representation
  - token: per-task-compute
    note: a per-task budget large enough for many generations
cost: extreme
evidence:
  - claim: "29.4% on ARC-AGI-2 semi-private, evolving natural-language program descriptions"
    kind: claimed
    split: arc-agi-2/semi-private
    regime: $3,648-per-task
    source: https://jeremyberman.substack.com
    stars: 2
    requires_beyond: [llm-inference]
  - claim: "26.0% on ARC-AGI-2 semi-private, growing a reusable library of solved sub-programs"
    kind: claimed
    split: arc-agi-2/semi-private
    regime: $476-per-task
    source: https://github.com/epang080516/arc_agi
    stars: 2
    requires_beyond: [llm-inference]
  - claim: "SOAR: 52% of the ARC-AGI-1 public set, evolutionary search plus hindsight fine-tuning on the system's own search traces"
    kind: claimed
    split: arc-agi-1/public-eval
    regime: uncapped
    source: https://arxiv.org/abs/2507.14172
    stars: 2
    requires_beyond: [llm-inference, weight-gradients]
no_absolute_score: false
caveats:
  - "The two ARC-AGI-2 rows sit at $3,648 and $476 per task — a 7.7x cost difference for 3.4 points. Ranking them by percentage alone inverts the useful comparison."
  - "SOAR words its split as 'the public test set'; read it as the ARC-AGI-1 public evaluation set and not as a held-out leaderboard number."
  - "ARC-AGI-2 training data contains ARC-AGI-1 eval data; any system fine-tuned on AGI-2 train and scored on AGI-1 eval is inflated."
interacts:
  - technique: technique.oomdp-identification
    rel: overlaps
    scope: modeling.belief-update
    note: >-
      one retracts a prediction the evidence contradicts, the other mutates a candidate that
      scored badly; both revise under feedback, and the register does not yet hold a measured
      combination of the two
  - technique: technique.llm-sampling-program-synthesis
    rel: subsumes
    scope: modeling.belief-update
    note: >-
      mutating a failing candidate in light of its trace contains rejection sampling as the
      special case where the mutation ignores the trace
  - technique: technique.refinement-harness
    rel: overlaps
    scope: modeling.belief-update
    note: >-
      both close the revision gap by feeding a failure back into the next attempt; one
      mutates a population, the other re-prompts
---

# Evolutionary Program Synthesis

**What it is.** Keep a population of candidate solutions, score each against the
demonstration pairs, and mutate or recombine the survivors — the DreamCoder shape, with a
language model as the mutation operator. The population may be symbolic programs (Pang,
which also grows a reusable library) or natural-language descriptions (Berman). SOAR adds
a second loop: fine-tune the model on its own successful search traces, so later search is
drawn from a better proposal distribution.

**The cognate.** This is the register's nearest thing to *revising a committed account*.
Unlike independent sampling, a candidate here inherits from one that was tried and found
wrong, which is why it earns `partial` on [`modeling.belief-update`] where sampling earns
only `incidental`.

**Therefore.** Use it when execution feedback is cheap and per-task budget is not the
binding constraint. The cost rows are the caveat: at $3,648/task this is a demonstration
of what is reachable, not a deployable method.

**The limit.** The mutation is *proposed* by a model, not *derived* from the error. Nothing
in the loop identifies which part of a candidate was responsible for the failure, so the
revision step is still search wearing the shape of inference.
