---
id: profile.arc-agi-3-llm-ship
kind: profile
name: ARC-AGI-3 (ARC Prize 2026, Kaggle) — in-kernel LLM ship lineage
source:
  - title: ARC-AGI-3 — interactive reasoning benchmark
    url: https://arcprize.org/arc-agi/3/
  - title: ARC Prize 2026 (Kaggle code competition)
    url: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3
  - title: ARC-AGI-3 technical report (scoring, aggregation, action cutoff)
    url: https://arxiv.org/abs/2603.24621
supplies:
  # level: full | partial | none   — what the deployment can actually provide.
  # binding: competition | project — a competition rule cannot be relaxed; a project
  #   constraint is a choice, and marking it as one keeps it re-openable.
  - token: dsl-primitives
    level: full
    binding: project
    note: the agent authors its own primitives over the 64x64 / 16-colour grid
  - token: search-procedure
    level: full
    binding: project
  - token: expert-authored-library
    level: full
    binding: project
    note: one maintainer, authoring by playtest
  - token: operator-preconditions
    level: full
    binding: project
  - token: state-representation
    level: full
    binding: project
  - token: state-difference-function
    level: full
    binding: project
  - token: candidate-arbiter
    level: full
    binding: project
  - token: mutation-operator
    level: full
    binding: project
  - token: orchestration-layer
    level: full
    binding: project
  - token: novelty-estimator
    level: full
    binding: project
  - token: augmentation-scheme
    level: full
    binding: project
    note: grid symmetries are available, though nothing here can consume them
  - token: per-task-compute
    level: full
    binding: competition
    note: in-process engine, no per-game cost cap beyond the notebook's wall clock
  - token: parallel-inference-budget
    level: full
    binding: competition
  - token: deterministic-environment
    level: full
    binding: competition
    note: seeded games and a deterministic engine, so one counterexample settles a prediction

  - token: resettable-simulator
    level: partial
    binding: competition
    note: >-
      RESET restarts the current level and the engine is seeded and deterministic, but there
      is no restore to an arbitrary state and no forward model is given -- a rollout is
      replayed from a level boundary at the cost of its whole prefix. Where a game offers the
      undo action, a one-step counterfactual is cheaper than a replay; it is offered per game,
      not guaranteed
  - token: value-signal
    level: partial
    binding: competition
    note: terminal only (level complete / game over); no heuristic value for a reached state
  - token: reward-channel
    level: partial
    binding: competition
    note: the same terminal signal, and nothing denser to add a bonus to
  - token: interaction-budget
    level: partial
    binding: competition
    limit: 5
    unit: actions-per-human-baseline-action
    as_of: '2026-04-17'
    checked: '2026-09-03'
    source: https://arxiv.org/abs/2603.24621
    note: >-
      v2 section 4.3 imposes "an action budget of five times the human-baseline median
      action count per level", justified there by the cost of evaluating frontier models
      rather than as a property of the task. Scoring in v2 is S = min(1.15, h/a)^2 per level,
      aggregated as the MINIMUM of the weighted completion fraction and the weighted average
      of level scores, with w_l = l over at least six levels. So exploration is charged twice:
      quadratically in the score, and against a budget that ends the level when it runs out.
    history:
      - as_of: '2026-03-24'
        limit: 5
        unit: actions-per-human-baseline-action
        source: https://arxiv.org/html/2603.24621v1
        note: >-
          v1 stated the same 5x figure as a hard cutoff in the scoring section ("we set a hard
          cutoff of 5x human performance per level"), capped a level at 1.0 rather than 1.15,
          and aggregated as sum_l l*S_l / (n(n+1)/2) with no completion-fraction term. The
          budget survived the revision; the cap and the aggregation did not. A screen run
          against v1 was run against a different rule, which is why this row is kept.
  - token: per-candidate-executor
    level: partial
    binding: competition
    note: >-
      the environment is the only executor and the scored rerun gives one trajectory per
      game; a candidate can be replayed only by resetting and re-spending actions
  - token: automatic-verifier
    level: partial
    binding: competition
    note: >-
      the only ground truth is level completion, and consulting it costs the actions that
      the score is computed from

  - token: network-access
    level: none
    binding: competition
    note: no internet during evaluation
  - token: llm-inference
    level: full
    binding: project
    note: >-
      a 27B language model (Qwen3.6-27B, fp8) served in-kernel by vLLM from an attached model
      dataset on the RTX PRO 6000; no network, so nothing is called — the model is co-located
  - token: compiled-implementation
    level: partial
    binding: project
    note: >-
      wheels are installed offline from an attached wheelhouse dataset and the image carries a
      compiler; nothing scored is compiled today
  - token: weight-gradients
    level: partial
    binding: project
    note: >-
      adapters (LoRA) are trained OFF-kernel on Colab and shipped as a dataset; no training
      runs inside the scored kernel
  - token: trained-model
    level: partial
    binding: project
    note: >-
      the served base plus optional adapters; nothing is fitted to the hidden games
  - token: training-distribution
    level: partial
    binding: project
    note: >-
      self-generated replay from the public games; the hidden evaluation games stay unseen
  - token: differentiable-objective
    level: none
    binding: project
  - token: learned-latent-space
    level: none
    binding: project
  - token: multimodal-model
    level: partial
    binding: project
    note: >-
      a vision-language model of the same family can be served the same way and has been
      staged; the shipped build reads the grid as text, so the token is available, not used
  - token: task-identifier-embedding
    level: none
    binding: project
    note: the evaluation games are unseen, so no per-task identifier could be fitted anyway

own_splits:
  # a cost measured somewhere else is indicative here, never a verdict; the screen says so
  - arc-agi-3/public-preview
  - arc-agi-3/hidden-eval
requires_capabilities:
  - capability: goal-setting.goal-inference
    criticality: required
    why: the games ship with no instructions; nothing states what winning is
  - capability: exploration.experiment-design
    criticality: required
    why: mechanics must be learned by acting, and every action is charged to the score
  - capability: modeling.hypothesis-formation
    criticality: required
    why: the rules of each game are the object to be inferred
  - capability: modeling.belief-update
    criticality: required
    why: a first reading of the mechanics is usually wrong and must be revised in play
  - capability: modeling.state-abstraction
    criticality: required
    why: a 64x64x16 frame must become objects before any rule can be stated over it
  - capability: planning-execution.goal-decomposition
    criticality: required
    why: levels need multi-step routes, and the score falls with the square of actions taken
  - capability: priors.objectness
    criticality: required
    why: the grids are read as sprites and regions, not pixels
  - capability: priors.agentness
    criticality: useful
    why: several games contain autonomous movers whose behaviour must be predicted
  - capability: modeling.per-task-adaptation
    criticality: useful
    why: each game is its own task, seen once
  - capability: priors.geometry-and-topology
    criticality: useful
    why: routes, containment and adjacency are the vocabulary of most mechanics
  - capability: priors.numbers-and-counting
    criticality: useful
    why: counters, inventories and repetition appear as mechanics
---

# ARC-AGI-3 (ARC Prize 2026)

**What a profile is.** A statement of what a deployment can supply and what it needs —
never what its team has adopted. This profile is the in-kernel LLM lineage of the same
competition entry: a language model served locally inside the scored Kaggle kernel, driven
by a harness that reads the game as text. The stdlib-only single-file lineage is
`profile.arc-agi-3`; the competition tokens are identical, the project tokens differ.

**Why the split between `competition` and `project` matters.** The competition rows are
unchanged from the stdlib profile: no network, terminal-only reward, an interaction budget
that is a wall. What this lineage chose to supply is a model and off-kernel gradients; what
it still does not supply is any in-kernel training, a learned latent space, or an identifier
for games it has never seen. A screen against this profile therefore reports which techniques
the model unlocks — and which are blocked by the benchmark either way.

**The interesting preconditions here are the `partial` ones.** Interaction, verification
and simulation are all *available but charged*: the scoring rule squares the action count,
so exploration, hypothesis testing and candidate replay are paid for in the same currency
as the answer. A technique whose `requires` are all satisfied at `partial` is not thereby
admissible — it is admissible *at a price the score can see*, which is the distinction a
prose precondition list could never make.

**And `interaction-budget` is a wall, not only a price.** The five-times-human action budget
ends the run on a level, and the levels after it are weighted more heavily and go unattempted.
So a mechanism's exploration cost has to be read against *h*, the human action baseline, and
one whose published identification cost exceeds 5h is not expensive here — it is inadmissible.
That is now arithmetic the screen does rather than a caveat a reader has to carry.

**Which is why the number is dated.** The figure has kept its value across a revision of the
technical report but not its standing: v1 stated it as a hard cutoff inside the scoring rules,
v2 as an evaluation budget on the leaderboard, justified by the API cost of running frontier
models. The scoring around it moved further — the per-level cap went from 1.0 to 1.15 and the
aggregation gained a completion-fraction term. A screen is only as current as the version it
was run against, so every quantity here carries the version it came from and the date someone
last read it, and the superseded row stays in `history` rather than being overwritten.
