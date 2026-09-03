---
id: technique.refinement-harness
kind: technique
name: Refinement Harness
addresses:
  - capability: modeling.per-task-adaptation
    strength: direct
    note: all adaptation is inference-time orchestration of a frozen model — no weights are touched
  - capability: modeling.belief-update
    strength: partial
    note: a verifier's result is fed back as the input to the next attempt; the revision is textual and unstructured
requires:
  - token: llm-inference
    note: one or more frontier models
  - token: network-access
    note: those models are reached by API
  - token: automatic-verifier
    note: an automatic verifier over candidate answers
  - token: orchestration-layer
    note: an orchestration layer holding the attempt history
leverage: computation
cost: medium
evidence:
  - claim: "54% on ARC-AGI-2 semi-private, ARC Prize verified, orchestrating frontier models with no training"
    kind: measured
    split: arc-agi-2/semi-private
    regime: $30.57-per-task
    source: https://poetiq.ai/posts/arcagi_verified/
    stars: 3
    date: 2025-12-05
no_absolute_score: false
caveats:
  - "The harness's score is inseparable from the underlying frontier models. It is a measurement of orchestration ON a given model generation, and it moves when that generation moves."
interacts:
  - technique: technique.test-time-training
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      adaptation with no weight update against adaptation that is nothing but weight updates;
      the cost profiles differ far more than the coverage does
  - technique: technique.llm-sampling-program-synthesis
    rel: subsumes
    scope: modeling.belief-update
    note: >-
      a verifier plus attempt history contains independent sampling as the case where the
      history is discarded between attempts
  - technique: technique.modality-driven-search
    rel: subsumes
    scope: modeling.per-task-adaptation
    note: >-
      both are inference-time orchestration of frozen models; parallel candidates plus a
      judge is one configuration of a refinement loop
---

# Refinement Harness

**What it is.** No training and no new model — a control loop that calls frontier models,
verifies their answers, and feeds the failures back as context for the next attempt. The
ARC Prize 2025 taxonomy classes this as the test-time chain-of-thought-with-verifier-
feedback branch of the general refinement-loop family.

**Why it matters to the register.** It is the cheapest existence proof that a large part
of the remaining benchmark headroom is a *harness* problem rather than a model problem —
54% at $30.57/task without touching any weights, against evolutionary methods an order of
magnitude more expensive for lower scores.

**Therefore.** Before building a training pipeline, establish what a verifier plus a loop
gets you on the same model. That number is the real baseline for any training claim.

**The limit.** It inherits the model's ceiling and its blind spots. A refinement loop over
a model that cannot represent the task at all refines nothing, and the loop has no way to
tell that case from a hard one.
