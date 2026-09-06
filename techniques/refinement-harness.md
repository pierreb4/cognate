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
cost: high
evidence:
  - claim: "54% on ARC-AGI-2 semi-private, ARC Prize verified, orchestrating frontier models with no training"
    kind: measured
    split: arc-agi-2/semi-private
    regime: $30.57-per-task
    source: https://poetiq.ai/posts/arcagi_verified/
    stars: 3
    date: 2025-12-05
  - claim: "4.71 RHAE on the ARC-AGI-3 Kaggle 2026 PUBLIC leaderboard, provisional until the private rerun after the 2026-11-02 deadline (rank 11 of the board at the read date): Tufa Labs' Duck harness — a coding agent in a Python REPL where every game observation is a Python variable, a Qwen 3.6 27B FP8 served in-kernel, image plus text views of the grid, and a context kept short by evicting the oldest messages; the same lineage won Milestone #1 on 2026-06-30 at 1.21"
    kind: measured
    split: arc-agi-3/kaggle-public-2026
    regime: kaggle-2026-single-rtx-6000-9h-offline-in-kernel-qwen-3.6-27b-fp8
    source: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard
    stars: 2
    date: 2026-09-06
no_absolute_score: false
caveats:
  - "The harness's score is inseparable from the underlying frontier models. It is a measurement of orchestration ON a given model generation, and it moves when that generation moves."
  - "AIMO3 (olympiad math, not ARC): the 3rd-place team lists 'Two-Step Self-Correction: A prompt that forced a draft-then-finalize sequence' under what was tried and did not work, and the only refinement in its pipeline is execution feedback — Python as 'a verification and search tool' inside the sampling loop — not a model-only reconsider step (https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/writeups/3rd-place-solution-for-the-aimo3-competition). No AIMO3 write-up read for this register shows an ablated gain from model-only self-refinement."
  - "NeuroGolf 2026 is the KNOWN-RULE regime — ONNX code golf over the 400 ARC-AGI-1 public TRAINING tasks with the answers given, so not an induction result — and every top harness was a loop of frontier-LLM agents over an exact local verifier with per-task attempt memory and a shared cookbook of verified tricks. The 1st-place team quantifies rewrite against polish: 'architectural rewrites averaged +0.5 boost per task whereas optimzing existing graphs averaged only +0.05 per task' (https://www.kaggle.com/competitions/neurogolf-2026/writeups/1st-place-kaggle-agent), and at the 7900-point plateau a single ChatGPT Pro call asked for +0.5 on one task 'achieved target 33% of the time', +0.3 'at 50% of the time' (https://www.kaggle.com/competitions/neurogolf-2026/discussion/726799). Read these as hit rates for refining a program whose rule is already known, not for inducing one."
  - "The Duck row runs OUTSIDE this node's `requires`: no network and the model in-kernel on one GPU — 'Because evaluation on the semi-private/private test set on Kaggle is constrained to a single GPU, we are restricted to use small open-source models and small token throughput.' (https://tufalabs.ai/research/duck-harness/) — so `network-access` is a property of the Poetiq row, not of the family. The organizer's milestone post records the design finding against authored tooling: 'Tufa Labs noted that, counterintuitively, hand-crafted tools actually hurt the model; letting it improvise worked better.' and that it was the only winner with the 'agent-writes-code' approach (https://arcprize.org/blog/arc-prize-2026-milestone-1). Spread is of the order of the score: on the 25 public games with 20 tries each Tufa reports 'Our mean score across all public games is 1.6002 +/- 0.4475.', and the readable re-release of the milestone notebook says of its 1.21 that 'we haven't had the same lucky result with this one' (https://www.kaggle.com/code/jeroencottaar/tufa-labs-duck-harness-june-30-milestone-winner). The top of the same board at the read date — Daniel Franzen 7.63, mostik.ai 7.51, Third Intelligence 6.43 (PUBLIC LB, provisional) — publishes no method and is evidence for no node."
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
  - technique: technique.transductive-output-prediction
    rel: overlaps
    scope: modeling.per-task-adaptation
    note: >-
      neither touches weights at inference; the harness accumulates attempts across calls
      under a verifier, the transductive model conditions once and cannot be told it was wrong
provenance:
  entered: 2026-09-02
  commit: 6f81060
  frame: arc-prize-2025-taxonomy
  note: >-
    stocked from the ARC Prize 2025 report's refinement-loop taxonomy (technique side) and
    Chollet's Core Knowledge prior list plus ARC-AGI-3's added priors (capability side)
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
