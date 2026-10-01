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
  - claim: "27.89 RHAE on the ARC-AGI-3 Kaggle 2026 PUBLIC leaderboard, provisional until the private rerun after the 2026-11-02 deadline (rank 3 at the 2026-10-01 07:28 UTC read; a tentative Milestone #2 winner): Daniel Franzen's fork of the Duck harness — the same coding agent playing through a Python tool, on Qwen3.8-Flash-Next (Intel AutoRound W4A16, with a quantized multi-token-prediction draft for speculative decoding) served in-kernel by an SGLang fork, a larger context trimmed in large blocks so the kept prefix stays cached, a priority scheduler that moves compute to the games making progress, larger board and difference images, animation frames, an UNDO action, and the Duck's structured world-model mechanism disabled; the published notebook shows 27.89"
    kind: measured
    split: arc-agi-3/kaggle-public-2026
    regime: kaggle-2026-single-rtx-6000-9h-offline-in-kernel-qwen-3.8-flash-next-w4a16
    source: https://github.com/da-fr/arc-agi-3-solution/blob/10882e332d883af3e61616df8c8a17d03a328a75/WRITEUP.md
    stars: 2
    date: 2026-09-30
  - claim: "23.84 RHAE on the ARC-AGI-3 Kaggle 2026 PUBLIC leaderboard, provisional until the private rerun after the 2026-11-02 deadline (rank 5 at the 2026-10-01 07:28 UTC read; a tentative Milestone #2 winner): Lord Han Solo's Duck harness on the Tufa ARC-AGI Framework, on a mixed NVFP4/FP8 Qwen3.8-Flash-Next with its multi-token-prediction head, served in-kernel by a vLLM build (e975732). No write-up: the method is the published notebook and its attached source bundle, which Tong Hui Kang's comparison (see caveats) reads as a rewritten tool-agent and system prompt, Python modules kept for the whole game, history trimmed at about 126k tokens and a per-game time cap; this notebook version shows 23.84"
    kind: measured
    split: arc-agi-3/kaggle-public-2026
    regime: kaggle-2026-single-rtx-6000-9h-offline-in-kernel-qwen-3.8-flash-next-nvfp4-fp8
    source: https://www.kaggle.com/code/lordhansolo/arc-agi-3-milestone-2?scriptVersionId=353922905
    stars: 2
    date: 2026-09-30
  - claim: "22.53 RHAE on the ARC-AGI-3 Kaggle 2026 PUBLIC leaderboard, provisional until the private rerun after the 2026-11-02 deadline (rank 6 at the 2026-10-01 07:28 UTC read; a tentative Milestone #2 winner): rellik13's Duck harness with Wang's sandbox and prompt design, on Qwen3.8-Flash-Next (Intel AutoRound, with the RadixArk NVFP4 speculative-decoding head) served in-kernel by SGLang (the Pennyroyal build). The last step, from 14.49, changed only memory: an FP8 KV cache, history trims raised from 36,864→26,624 to 57,344→45,056 tokens and 16 games at once, with prompts, harness logic, model and sampling unchanged; the published notebook shows 22.53"
    kind: measured
    split: arc-agi-3/kaggle-public-2026
    regime: kaggle-2026-single-rtx-6000-9h-offline-in-kernel-qwen-3.8-flash-next-w4a16
    source: https://github.com/LohitSiriki/arc-agi-3-milestone2-solution/blob/af105202327dcf35bd670a50b2558adab12e8dd3/WRITEUP.md
    stars: 2
    date: 2026-09-30
  - claim: "20.00 RHAE on the ARC-AGI-3 Kaggle 2026 PUBLIC leaderboard, provisional until the private rerun after the 2026-11-02 deadline (rank 8 at the 2026-10-01 07:28 UTC read; not among the three tentative Milestone #2 winners): face-of-agi's Duck harness on the RadixArk NVFP4 Qwen3.8-Flash-Next, served in-kernel by a vLLM build (8e685d198) with no speculative decoding and an int4 KV cache. No write-up: the method is the published notebook and its attached source bundle, which this register reads as Tufa Labs' Duck tool agent itself (subclassed; its code unchanged but for a history hook), a Python interpreter kept for the whole game, an append-only context compacted by a model-written summary at a 130,816-token window per game, and a token-budget scheduler keeping up to 31 games in play behind a KV-cache admission gate. The weights are not stock: the routed experts are GPTQ re-quantized onto the same NVFP4 grid with Hessians from MoE activations captured on the team's own recorded ARC-AGI-3 gameplay (experts with under 64 calibration rows keep the checkpoint's), and 64 of each layer's 512 routed experts (12.5%) are pruned at load by a mask ranked on recorded routing; this version's public output records both loaded. So the 20.00 is harness plus ARC-calibrated weights, not orchestration alone, and the bundle has no score with and without them; this notebook version shows 20.00"
    kind: measured
    split: arc-agi-3/kaggle-public-2026
    regime: kaggle-2026-single-rtx-6000-9h-offline-in-kernel-qwen-3.8-flash-next-nvfp4-arc-calibrated-gptq-experts-64-of-512-pruned
    source: https://www.kaggle.com/code/richardcsaky/arc-agi-3-milestone-2-submission?scriptVersionId=353985307
    stars: 2
    date: 2026-09-30
no_absolute_score: false
caveats:
  - "The harness's score is inseparable from the underlying frontier models. It is a measurement of orchestration ON a given model generation, and it moves when that generation moves."
  - "AIMO3 (olympiad math, not ARC): the 3rd-place team lists 'Two-Step Self-Correction: A prompt that forced a draft-then-finalize sequence' under what was tried and did not work, and the only refinement in its pipeline is execution feedback — Python as 'a verification and search tool' inside the sampling loop — not a model-only reconsider step (https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/writeups/3rd-place-solution-for-the-aimo3-competition). No AIMO3 write-up read for this register shows an ablated gain from model-only self-refinement."
  - "NeuroGolf 2026 is the KNOWN-RULE regime — ONNX code golf over the 400 ARC-AGI-1 public TRAINING tasks with the answers given, so not an induction result — and every top harness was a loop of frontier-LLM agents over an exact local verifier with per-task attempt memory and a shared cookbook of verified tricks. The 1st-place team quantifies rewrite against polish: 'architectural rewrites averaged +0.5 boost per task whereas optimzing existing graphs averaged only +0.05 per task' (https://www.kaggle.com/competitions/neurogolf-2026/writeups/1st-place-kaggle-agent), and at the 7900-point plateau a single ChatGPT Pro call asked for +0.5 on one task 'achieved target 33% of the time', +0.3 'at 50% of the time' (https://www.kaggle.com/competitions/neurogolf-2026/discussion/726799). Read these as hit rates for refining a program whose rule is already known, not for inducing one."
  - "The Duck row runs OUTSIDE this node's `requires`: no network and the model in-kernel on one GPU — 'Because evaluation on the semi-private/private test set on Kaggle is constrained to a single GPU, we are restricted to use small open-source models and small token throughput.' (https://tufalabs.ai/research/duck-harness/) — so `network-access` is a property of the Poetiq row, not of the family. The organizer's milestone post records the design finding against authored tooling: 'Tufa Labs noted that, counterintuitively, hand-crafted tools actually hurt the model; letting it improvise worked better.' and that it was the only winner with the 'agent-writes-code' approach (https://arcprize.org/blog/arc-prize-2026-milestone-1). Spread is of the order of the score: on the 25 public games with 20 tries each Tufa reports 'Our mean score across all public games is 1.6002 +/- 0.4475.', and the readable re-release of the milestone notebook says of its 1.21 that 'we haven't had the same lucky result with this one' (https://www.kaggle.com/code/jeroencottaar/tufa-labs-duck-harness-june-30-milestone-winner). The top of the same board at the read date — Daniel Franzen 7.63, mostik.ai 7.51, Third Intelligence 6.43 (PUBLIC LB, provisional) — publishes no method and is evidence for no node."
  - "Re-read of the same board 2026-09-17 (`kaggle competitions leaderboard arc-prize-2026-arc-agi-3`, PUBLIC LB, provisional): Tufa Labs 18.81, Daniel Franzen 11.59, NVARC3 11.04, Lord Han Solo 9.81, Tong Hui Kang 8.72. The 4.71 row stays at its read date because nothing public ties Tufa's 18.81 to the Duck as described: Tufa's newest ARC-AGI-3 post is still the 2026-07-01 Milestone #1 write-up (https://tufalabs.ai/research/), `Tufalabs/duck-harness` was last committed 2026-07-01, and `jeroencottaar`'s newest Kaggle notebook was last run 2026-07-01. The lineage has spread past Tufa — public competition notebooks on 09-16/17 are Duck forks on Qwen 3.8 (`wuliao0/duck-qwen3-8-anim-base`, `yuriimuktarov/arc3-duck-qwen38-*`) — but none is tied to a board row. Of places 2-5, none has published a method for this competition: Franzen's newest Kaggle notebook is the ARC Prize 2025 solution, NVARC's public repo is the ARC-AGI-2 solution (https://github.com/1ytic/NVARC) and the team name alone does not establish the same members, Lord Han Solo is untraceable, and Tong Hui Kang's public `tonghuikang/arc3` (last push 2026-07-22) links an autoresearch training-metrics dashboard (validation loss on held-out base games) with no score attached. Evidence for no node; re-read at the Milestone #2 deadline (2026-09-30)."
  - "Re-read of the same board 2026-09-30 07:27 UTC, the morning of the Milestone #2 deadline (`kaggle competitions leaderboard arc-prize-2026-arc-agi-3`, PUBLIC LB, provisional): Tufa Labs 45.33, Yi-Chia Chen 40.80, Daniel Franzen 26.55, the last dance 24.54, Lord Han Solo 23.84; 20th place is 9.07. The milestone will not surface the top two. Tufa Labs 'will not be sharing our solution on September 30 for the second milestone prize, since we worry it may not be possible to beat the best of 4000 copies of that solution', and adds 'We still plan to release our final solution when the competition ends' (https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/discussion/742801). In the declarations thread Yi-Chia Chen declines, and Daniel Franzen, Lord Han Solo and Tong Hui Kang will publish only if they place top 3 among the teams willing to share (https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/discussion/742935). The same Tufa post gives the lineage from the author's side, 'all high-scoring public notebooks now building on this harness', but the best public notebook states 5.75 (`shiiin9/affectify-arc-duck-plus-ours`, a Duck fork that allots thinking turns across games by a weighted lottery), so no public notebook ties to any row in the top 13 (13th place is 11.04). The 4.71 row stays at its read date: Tufa's newest ARC post is still the 2026-07-01 Milestone #1 write-up (https://tufalabs.ai/research/) and `Tufalabs/duck-harness` was last committed 2026-07-01. The organizer had no Milestone #2 post at the read (https://arcprize.org/blog/arc-prize-2026-milestone-2 returned 404). Evidence for no node; second pass after the deadline (2026-09-30 23:59 UTC)."
  - "Second re-read, after the Milestone #2 deadline, 2026-10-01 07:28 UTC (`kaggle competitions leaderboard arc-prize-2026-arc-agi-3 --download`, PUBLIC LB, provisional): Tufa Labs 50.65, Yi-Chia Chen 40.97, Daniel Franzen 27.89, the last dance 24.54, Lord Han Solo 23.84, rellik13 22.53; 20th place is 9.26. Three of the top six have now published, and each notebook carries the public score of its board row: Franzen 27.89 (https://www.kaggle.com/code/dfranzen/arc-agi-3-milestone-2-solution, write-up https://github.com/da-fr/arc-agi-3-solution/blob/main/WRITEUP.md), Lord Han Solo 23.84 (https://www.kaggle.com/code/lordhansolo/arc-agi-3-milestone-2, no write-up) and rellik13 22.53 (https://www.kaggle.com/code/sirikilohit/arc-agi-3-duck-18-1gc-submit, write-up https://github.com/LohitSiriki/arc-agi-3-milestone2-solution/blob/main/WRITEUP.md; the team's last submission is stamped 2026-10-01 00:02:30, after the deadline). Tong Hui Kang, unpublished, calls them the winners 'tentative, to be confirmed by the organizers' and reports that 'All three run Tufa Labs' Duck harness on the Tufa ARC-AGI Framework (TAAF) and serve Qwen3.8-Flash-Next'; the rows of his comparison are serving (quantization, speculative decoding, server, KV cache), context management, per-game compute budget, level handover, prompts and harness patches (https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/discussion/744792). So the best published method is this node's Duck lineage with serving and context work, and both write-ups credit context over added structure: rellik13's 'The last jump, 14.49 to 22.53, changed no prompts' (an FP8 KV cache, the freed memory spent on longer history), and Franzen's 'The largest improvement in this area came from disabling the structured world-model mechanism entirely' (the model-written notes, dropped in favour of a larger rolling context). Neither is a controlled ablation: Franzen calls his findings 'practical experiment results rather than a complete controlled ablation study', and rellik13 reports 'The same notebook submitted three times scored 5.02, 5.50 and 6.42'. face-of-agi, 8th, has also published, its notebook carrying the 20.00 of its board row (https://www.kaggle.com/code/richardcsaky/arc-agi-3-milestone-2-submission), with no write-up and its solver in an attached public dataset. Tufa Labs and Yi-Chia Chen are unpublished, and the organizer's Milestone #2 page still returned 404 at 07:32 UTC. The 4.71 row stays at its read date. The four published rows are entered as evidence at two stars, each one submission demonstrated by its authors; Lord Han Solo's method is read from his published code by a third party, not described by him, and face-of-agi's is read from its published code by this register. The face-of-agi row is not orchestration alone: its routed experts are re-quantized and pruned on the team's own recorded ARC-AGI-3 gameplay before the run, though frozen during play (see the row). Like the 4.71 row, all four run outside this node's `requires`: no network, the model in-kernel."
  - "Third re-read, the same day, 2026-10-01 11:55 UTC (`kaggle competitions leaderboard arc-prize-2026-arc-agi-3 --download`, PUBLIC LB, provisional): scores from 9-hour reruns keep landing after the deadline, and the board has moved under the four published rows without changing their scores. Daniel Franzen 27.89 is now 16th, Lord Han Solo 23.84 48th, rellik13 22.53 51st and face-of-agi 20.00 64th (at 10:13 UTC they were 9th, 30th, 33rd and 42nd), and 20th place is 27.58, up from 9.26 at 07:28 UTC. Two teams whose every submission predates the deadline now score above Franzen: Mathemortician 28.32 (last submission 2026-09-30 23:13:34) and GYUYOUNG PARK09 28.13 (2026-09-30 23:30:31). For a team whose last submission is after the deadline, the board alone cannot say which of its scores predates it. So the ranks in the four Milestone #2 rows are those of the 07:28 UTC read, and the winners remain 'tentative, to be confirmed by the organizers': the organizer's Milestone #2 page still returned 404 at 11:55 UTC. Evidence for no node; re-read at the organizer's confirmation."
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
