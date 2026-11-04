<!-- Part 2 of 5 of 2026-10-20-llm-human-gap.md, moved there word for word on 2026-11-04. -->
[← 2026-10-20-llm-human-gap.md](2026-10-20-llm-human-gap.md) · [← part 1](2026-10-20-llm-human-gap.md) · part 2 of 5 · [part 3 →](2026-10-20-llm-human-gap-part-3.md)

## Prior faculty

### `priors.objectness` — status `partial`, gap report INDIRECT (1 edge)

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| MLLMs trail humans on object permanence, and low-level concepts scale worse than high-level ones | CoreCognition, 1,503 items, 12 concepts, 230 models | permanence 88.10; overall 86.98 (MTurk) | permanence InternVL3-78B 74.14; overall o1 74.91 (2024-10), GPT-5 84.37 in an independent re-run (2025-08) | [2410.10855](https://arxiv.org/abs/2410.10855) (ICML 2025); re-run [2508.13142](https://arxiv.org/abs/2508.13142) | `***` permanence below human; `**` scaling | closing on the aggregate, flat on the low-level items |
| Identity through motion: swapping identical objects puts frontier VLMs at chance | VET-Bench, 3-cup shell game, chance 0.33 | none measured | Gemini-3-Pro 0.34; SGCoT over 90%† using Molmo2's tracker (2026-03) | [2603.08436](https://arxiv.org/abs/2603.08436)† | `**` | flat at chance; the fix is an explicit trajectory state |
| Video-LLMs lose identity, state and continuity across occlusion | TOC-Bench, 2,323 QA pairs | 89.3% | GPT-5.5 47.1% (2026-05); the deficit is in counting, ordering and state change, not re-identification | [2605.09904](https://arxiv.org/abs/2605.09904) | `**` | one snapshot |
| Permanence acquired from raw video, with no object vocabulary, in simple scenes only | IntPhys (pairwise surprise), GRASP, InfLevel-lab | permanence error 12.5% (IntPhys private test) | V-JEPA IntPhys 98% (95-99)†, GRASP 66%†, InfLevel 62%† (2025-02) | [2502.11831](https://arxiv.org/abs/2502.11831)† | `**` | technique result; collapses on IntPhys 2 (see basic-physics) |

**Verdict.** Status `partial` and the INDIRECT reading stand.

- The working fix for identity (SGCoT) consumes a tracker trained on track supervision, so it
  grades `incidental` here.
- Latent video prediction (V-JEPA) is the first candidate for *acquired* persistence the
  register has not examined. Contact evidence is weak (GRASP 66%, InfLevel 62%), so the likely
  outcome is a recorded refusal, as for VideoSAUR.

### `priors.basic-physics` — status `open`, gap report EMPTY

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Intuitive physics in complex scenes: every model near chance | IntPhys 2, violation of expectation; Main 1,012 videos, Held-Out 344 | Main 96.44, Held-Out 92.44† (3 annotators, majority vote) | V-JEPA 2-h 57.51, Gemini 2.5 Flash 55.63, GPT-4o 53.75 (2025-06)† | [2506.09849](https://arxiv.org/abs/2506.09849)† | `***`: near-chance reproduced by an independent group ([2512.06232](https://arxiv.org/abs/2512.06232)) and by GRASP | flat (2024 and 2025 models all 50-58%) |
| Physical question answering: about half human accuracy | PhysBench, 10,002 items, chance 25% | 95.87% | GPT-4o 49.49% (2025-01) | [2501.16411](https://arxiv.org/abs/2501.16411) | `**` | no newer independent run |
| Video generators: visual realism does not imply physics, and scale gives case-based generalisation | Physics-IQ; controlled 2D mechanics sweep | none (Physics-IQ's 100 is take-to-take physical variance) | VideoPoet 29.5 on Physics-IQ (2025-01); scaling fixes in-distribution, not out-of-distribution (2024-11) | [2501.09038](https://arxiv.org/abs/2501.09038); [2411.02385](https://arxiv.org/abs/2411.02385) | `***` direction (two groups) | flat with scale |
| Data needed to acquire violation-of-expectation physics | V-JEPA data ablation; child-headcam pretraining | infants show permanence effects by about 3-4 months | 128 h of unique video keeps >70% on every IntPhys property†; 472 h of child headcam (SAYCam) is at chance on IntPhys 2 | [2502.11831](https://arxiv.org/abs/2502.11831)†; [2512.06232](https://arxiv.org/abs/2512.06232) | `**` | unknown |

**Verdict.** Status `open` stands, but the EMPTY reading is now arguable.

- MLLMs are not candidates.
- Latent video prediction infers dynamics from observed motion with no physics engine, which is
  the cell's `direct` criterion, but only in simple scenes. Entered as a technique at `partial`,
  it would move the cell to INDIRECT, and its evidence line must carry the IntPhys 2 result
  (57.5 against 96.4). This is decision D2 in the proposals.

### `priors.geometry-and-topology` — status `partial`, gap report INDIRECT (1 edge)

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Metric spatial estimation is at human level; perspective taking, mental rotation and deformation are far below | GPT-5 against published human baselines on 8 benchmarks | VSI-Bench 79.2; MMSI 97.2; MindCube-Tiny 94.55; SpatialViz 82.46 | GPT-5: 55.03, 41.80, 56.30, 51.27; below random on 3D mental rotation (2025-08 to 2025-12) | [2508.13142](https://arxiv.org/abs/2508.13142) | `***` VSI-Bench gap (independent re-run); `**` by category | closing on VSI-Bench (Gemini-1.5 Pro 45.4 in 2024-12); flat on rotation and perspective |
| Dehaene's geometric odd-one-out: VLMs below unschooled adults | 43 concepts in 7 classes | Western adults 85.10%, Munduruku 65.34% | DINOv2 48.89%; best VLM 37.78% (2025-05); Gemini 1.5 Pro weak at random rotations (2025-03) | [2505.13281](https://arxiv.org/abs/2505.13281); [2503.03840](https://arxiv.org/abs/2503.03840) | `***` direction (two groups) | no 2026 model tested |
| Topology: a relation is recognised but not acted on | MindTopo, 13 task types | 97.40% | GPT-5.5 54.13 (reasoning 57.74, planning 48.33) (2026) | [mind-topo.github.io](https://mind-topo.github.io/), project page only, *no paper* | `*` | one snapshot |
| A jagged item that closed: reading analog clocks | ClockBench, 720 questions | average 90.7%, best 95% | Gemini 4 Argon High 83.3% (board read 2026-10-20, rows undated); about 13% at launch (2025-09, secondary) | [clockbench.ai](https://clockbench.ai/) | `**` | closing fast |

**Verdict.** Status `partial` and the INDIRECT reading stand.

- Frontier MLLMs *acquire* metric relations, which `technique.dsl-search` (authored primitives,
  `incidental`) cannot claim. A node for multimodal pretraining could earn `partial` here, but it
  would have to carry the failures on rotation, perspective and topology.
- Nothing found induces a symmetry group it was not told about, so the cell's "no node"
  sentence still holds.

### `priors.numbers-and-counting` — status `open`, gap report INDIRECT (1 edge)

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Counting in real cluttered scenes: under half exact, collapsing with numerosity | CountQA, 1,528 questions, exact match | none | Gemini 2.5 Pro 42.93; 13.9 above 50 objects (2025-08) | [2508.06585](https://arxiv.org/abs/2508.06585) | `**` | unknown |
| VLMs count from priors, not from the image | VLMBias, counterfactual images (a 5-legged dog) | 45-96% time-limited, by domain | mean 17.05; best o4-mini 20.25; 100% on unmodified images (2025-05 to 2026-04) | [2505.23941](https://arxiv.org/abs/2505.23941) | `**` | flat (reasoning models gain 2-4 points) |
| Numerosity is decodable in the vision encoder and lost in the language readout | probes over 7 VLMs | subitizing and Weber-law signatures | architecture explains far more variance (partial omega^2 0.325) than visual conditions (2026-08) | [2608.15425](https://arxiv.org/abs/2608.15425); BlindTest [2407.06581](https://arxiv.org/abs/2407.06581) | `**` | n/a (mechanism) |

**Verdict.** Status `open` and the INDIRECT reading stand.

- MLLM counting is acquired, not authored, but it fails the cell's own commitment: it is not
  grounded in individuated items.
- The repeated finding that the encoder holds the count and the readout loses it supports the
  cell's claim that counting is a commitment about the front end.

### `priors.agentness` — status `open`, gap report EMPTY

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Intuitive psychology from animations: no MLLM matched humans | help/hinder and cost-reward stimuli; regression on mean human judgements | individual against human mean R^2 0.858 (help/hinder) | best R^2 0.038 (Otter); Claude-3 coefficient -0.25 (2023-24 models) | [2311.16093](https://arxiv.org/abs/2311.16093) (Nat Mach Intell 2025-01) | `**` | unknown for 2026 models |
| Static intentionality items: above the human baseline | CoreCognition intentionality, multiple-choice VQA | 81.98% | o1 87.54 (2024-25) | [2410.10855](https://arxiv.org/abs/2410.10855) | `**` | closed on this format, which can be answered from scene priors |
| Infant-paradigm agency benchmarks (BIB, AGENT) have never been run on a frontier MLLM | violation of expectation after familiarisation | infant looking-time effects | none located; a Bayesian ToM model with "agent" as a primitive reaches ~99% on BIB (2022) | [2102.11938](https://arxiv.org/abs/2102.11938); [AGENT](https://proceedings.mlr.press/v139/shu21a/shu21a.pdf) | n/a (an absence) | n/a |

**Verdict.** Status `open` and the EMPTY reading stand.

- Every result found is either handed the agent or measures goal inference after the agent has
  been identified. Nothing individuates agents from behaviour.
- The cheapest high-value measurement in the whole survey is BIB or AGENT run on 2026 video
  MLLMs.

---

