---
id: learning.prior-acquisition
kind: capability
name: Prior Acquisition
faculty: learning
human_source:
  - title: "Core knowledge (Spelke & Kinzler, Developmental Science 2007)"
    url: https://onlinelibrary.wiley.com/doi/10.1111/j.1467-7687.2007.00569.x
part_of: [learning]
completed_by:
  - priors.objectness
  - priors.basic-physics
  - priors.agentness
  - priors.geometry-and-topology
  - priors.numbers-and-counting
  - modeling.state-abstraction
  - goal-setting.goal-inference
status: open
provenance:
  entered: 2026-10-20
  commit: 92f4379
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Prior Acquisition

**Context.** The seven cells the supplied/acquired test governs (`SCHEMA.md`) each name a
thing a system must have before the rest can run: objects, physics, agents, geometry, number,
identity across frames, an objective. Those cells grade *whether* the thing was acquired or
handed over.

**Problem.** They do not ask what the acquiring cost. Infants show object-permanence effects
by about three to four months of age. The machine results do not yet settle what a machine
needs for the same. A latent video predictor trained on 128 hours of unique video keeps above 70%
on every IntPhys property ([2502.11831](https://arxiv.org/abs/2502.11831)), on simple scenes
only; the same architecture trained on 472 hours of one child's headcam video is at chance on
IntPhys 2's realistic scenes, as is every model trained on internet-scale video
([2512.06232](https://arxiv.org/abs/2512.06232)). About 200 hours of one child's video gives
a vision model about 70% of an ImageNet-trained model's downstream performance
([2305.15372](https://arxiv.org/abs/2305.15372)). And in BabyLM 2024 no multimodal entry
beat the baselines ([2412.05149](https://arxiv.org/abs/2412.05149)).

**Therefore.** Acquire a core prior from no more egocentric experience than a child of the
matching age has had, with no authored vocabulary, and say how much experience it took.

**How a technique is graded here.** The prior must be acquired by the supplied/acquired test,
and the experience it was acquired from must be stated and at most a child's. A technique
`direct` or `partial` on one of the seven cells, with a training budget far above a child's,
does not address this cell.

**Status: open (entered 2026-10-20).** No technique in the register addresses it.
[`technique.latent-video-prediction`] is the nearest candidate: its 128-hour row is within an
order of magnitude of an infant's visual experience, on simple scenes only. It is completed by
the seven cells it asks about, since each states which prior is to be acquired.

Task-specific reinforcement learning on games is no candidate by this cell's rule, its
experience being far above a child's, and one controlled report reads its limit as a priors
problem. In Tufa Labs' ARC Prize 2026 work, PPO and DPPO, evaluated on the 25 public
ARC-AGI-3 games with the training seeds, moved an expert-pruned Qwen3.8-Flash-Next from
45.5% to between 44.2% and 45.9% (four updates, paired p 0.61 to 0.92), while a Qwen3.8-27B
trained with PPO gained 12.7 points (9.4 to 22.1%, 95% interval [8.27, 17.5]) on 43
generated games held out from its training and earlier used to validate a 9B model. The two
arms differ in model family and setup as well as size. The authors "read Flash-Next's
failure as coming less from a bad strategy than from not having the right priors or
committing to the wrong hypothesis, which is hard to fix with task-specific post-training",
and call the Flash-Next results "not proof that further RL cannot work"
([source](https://tufalabs.github.io/arc-writeups/supplementary/rl_training/rl_training.html),
2026-11-09).
