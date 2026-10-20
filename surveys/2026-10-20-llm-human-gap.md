# The gap between LLM-based systems and human capacities, by cognate cell

*Survey note, 2026-10-20. Period covered: 2024-01 to 2026-10, with a few older anchors marked as such.*

*A dated snapshot, not a maintained document: it is kept as written, with its links made
local. The nodes and rows it supplied carry `provenance.frame: llm-human-gap-survey-2026-10`,
so `scripts/build_graph.py --provenance` reports how much of the register came through it. The
decisions it names (D1 to D13) were proposals made alongside it; what the register did with each
is at the end, under [Decisions taken](#decisions-taken-2026-10-20).*

## What this covers, and how

**Question.** Where do LLM-based systems (LLMs, multimodal LLMs, LLM agents and the harnesses
around them) stand against human capacities, faculty by faculty? Where has the gap closed, where
does it stay open, and where is it widening? Both inference and training are in scope: how well
a trained system performs, and how efficiently it got there.

**Slices.** Six reading passes, each held to primary sources:

1. the five `priors.*` cells;
2. the five `modeling.*` cells;
3. exploration, goal-setting and planning-execution (four cells);
4. training-time learning efficiency (data, compute, energy, exposures, grounding);
5. continual learning and long-term memory after deployment;
6. cross-cutting work: how the gap is measured, multi-faculty frameworks, robustness, cost.

This note merges the six passes, and a seventh pass re-checked the most load-bearing claims.

**How sources were held.**

- Only primary pages count: arXiv abstract or HTML, journal pages, benchmark owners' result pages
  (arcprize.org, metr.org), and maintained leaderboards.
- Vendor self-reports and press coverage are weak priors. Where they are the only source, the
  number is marked *self-reported* or *secondary* and stays out of the headline findings.
- A dagger (†) marks a claim that was re-opened on its primary on 2026-10-20 in a verification
  pass separate from the reading passes. The check table is in [2026-10-20-llm-human-gap-checks.md](2026-10-20-llm-human-gap-checks.md), 26 rows.
  An unmarked number was read on its primary by one reading pass and not re-checked.
- *Unverified* marks a number that no pass could trace to a primary.

**Stars** follow [`SCHEMA.md`](../SCHEMA.md) and grade the evidence for the gap claim, not the paper:

- `*` argued;
- `**` demonstrated once (one group, or one evaluator running vendors' models);
- `***` reproduced independently (two or more groups in the same direction);
- `****` reproduced under adversarial ablation (none found).

`kind: measured` means a party other than the system's builder obtained the number. ARC Prize
testing a lab's model counts; a paper scoring its own method does not. More than two stars
requires `measured`.

**Reading the cell verdicts.** A cell's `status` and its EMPTY / INDIRECT / covered reading in
[`build_graph.py`](../scripts/build_graph.py)'s gap report describe the *techniques in the register*, graded by the
supplied/acquired test. They do not say whether frontier LLMs "have" a capability. A benchmark
showing a gap does not by itself move a cell. A technique that addresses the cell does, and
where this survey found one, the verdict names it. The gap report at the time of writing reads
9 unmet of 14 cells.

## The answer in one paragraph

**Closed.** Between 2024 and 2026 the gap closed wherever a benchmark poses a bounded problem
with a checkable answer and the system can spend inference compute on it:

- static few-shot abstraction: ARC-AGI-2 went from 3% (2025-05) to 95.0% (GPT-6 Astra,
  2026-09)†, where testers solved 66% of the test pairs they attempted and a secondary estimate
  puts the per-person average at about 53%;
- frontier mathematics;
- literal theory of mind;
- simple rule switching on the Wisconsin Card Sorting Test;
- metric spatial estimation;
- information-seeking questions over an enumerable hypothesis space: a small model with
  Bayesian experimental design beat humans and GPT-5 at Battleship†;
- action-efficient play of ARC-AGI-3's instruction-free games, *when the provider's reasoning
  state is carried between steps*: 99.9%, against 62.7% under ARC Prize's Standard harness
  (2026-09).

**Open.** The gap stays wide wherever a human baseline exists and the task requires one of
these, and on several of them scale has not moved it:

- seeing physics in realistic scenes: 57.5% against 96.4% on IntPhys 2†;
- keeping an object's identity through a swap: at chance;
- mentally rotating objects or taking another's perspective;
- counting what is in the image rather than what a prior expects: 17% on counterfactual images;
- reading an agent's goal from its actions: 40.7% against 88.5%†;
- revising an account after contrary evidence;
- designing experiments with real information value;
- holding the *intended* rule rather than a shortcut: 27% of o3's correct answers against 7%
  of humans'†;
- recognising that a subgoal was achieved;
- writing a once-seen experience into durable memory: zero on the CHC framework's long-term
  storage for both GPT-4 and GPT-5†.

**Widening.** Three gaps grow by construction, because scale is the method:

- data per unit of competence: children reach adult-like language on roughly 10^8 words,
  frontier models train on 10^13 tokens and more, and dataset growth runs at ~2.4x a year;
- compute and energy for learning;
- abstention: reasoning training cuts it by 24%†.

One measured difference is not a matter of degree at all. Children's word learning
*accelerates* with what they already know (kappa ~11-13), while language models show constant
returns (kappa ~1.16)†.

**The profile is jagged, and part of it is an artefact.** The gaps that closed were measured
on 2026 models. Most of the gaps that remain open were last measured, with a human baseline,
on 2024-25 models. Human baselines are typically about eight people. ARC-AGI-3, the largest
mover, scored 54.8% or 99.9% for the same model at the same (high) effort, depending only on the
harness†.

---

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

## Modeling faculty

### `modeling.state-abstraction` — status `partial`, gap report INDIRECT (1 edge)

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Video models do not integrate evidence across frames | REVEAL cross-frame probe: each frame shows ~19% of the scene; share of correct answers kept | 92-97% kept (n = 25 items) | Gemini 2.5 Pro 74% -> 8% (11% kept) (2025 models) | [2602.11244](https://arxiv.org/abs/2602.11244) (v2 2026-09-16) | `**` | one time point |
| Abstraction from pixels lags abstraction from text on the same tasks | ConceptARC, 480 tasks, textual against visual input | 73% pass@1† | o3 (medium + tools) 75.6% textual, 29.2% visual† (2025) | [2510.02125](https://arxiv.org/abs/2510.02125)† | `**` | one model generation |

**Verdict.** Status `partial` and the INDIRECT reading stand.

- Nothing LLM-side emits a stable per-thing index.
- REVEAL widens the gap on the across-frames half, the half the cell is about, and supplies a
  measure with a human ceiling.
- The identity-through-swap result (VET-Bench, under objectness) is the sharper instance.

### `modeling.hypothesis-formation` — status `partial`, gap report covered

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Correct answer, wrong account: models reach right outputs through shortcut rules far more often than humans | ConceptARC; model and human rules hand-classified | ~7% of correct outputs rest on unintended or incorrect rules† | o3: ~27%† (2025) | [2510.02125](https://arxiv.org/abs/2510.02125) v5, 2026-10-16† | `**` | one generation |
| LLM agents guess better at the outset, then fail to refine | RULEARN interactive rule puzzles | 50 people: puzzle success 63.33%; rule found 43.3%, two thirds of it through induction | GPT-4o + IDEA 50.33%; rule right first ~30% vs ~10% for people; ~5% of discoveries through interaction (2024) | [2408.10455](https://arxiv.org/abs/2408.10455) (ACL Findings 2025) | `**` | GPT-4o era, no re-run |
| Instruction-free interactive games: near zero to past the median human in four months, harness-dependent | ARC-AGI-3 semi-private; per-level action efficiency against the median human | every environment beaten by >=2 of ~10 first-time players; 458-person panel† | GPT-5.5 0.43% (2026-05-01); GPT-6 Astra 62.7% Standard, 99.9% Provider Adapter (2026-09-03) | [arc-agi-3 analysis](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis); [astra](https://arcprize.org/blog/astra) | `**` per number | closing steeply |

**Verdict.** Status `partial` stands.

- The evidence splits the cell. *Generating* a first account is at or past human level.
  *Holding the intended account* and *designing tests that could kill one* still show
  human-baselined gaps.
- The ConceptARC rule analysis is the measure the cell's grading rule asks for ("a candidate
  answer is not a candidate account"), now with a human baseline.
- ARC-AGI-3 cannot change a grade: no mechanism is published, and the adapter's state is
  invisible to the testers.

### `modeling.belief-update` — status `open`, gap report covered

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| World-model learning by reward-free exploration: humans ahead everywhere; models keep rules the evidence contradicts | AutumnBench: 43 environments, 129 tasks | 517 participants†; resets and no-ops ~12.5% of actions each | "humans substantially outperform" five frontier models†; models spend <7% on resets and no-ops combined (2025 models) | [2510.19788](https://arxiv.org/abs/2510.19788) (v4 2026-05-07)† | `**` | one snapshot |
| Active concept induction: agents' experiments carry almost no information | ZendoWorld (Zendo-style visual rule game) | 73.3% wins, 19 people; out-of-distribution rule solved by 7 of 10† | best VLM agent 45.5% (Gemini 3.1 Pro preview); 0 of 5 on the out-of-distribution rule† (2026-07) | [2607.08233](https://arxiv.org/abs/2607.08233)† | `**` | one snapshot |
| LLMs plateau after one round of evidence; people keep updating; Bayesian teaching closes part of it | 5-round preference inference | 500 participants improve from round 1 to 5 (p = 0.002) | off-the-shelf LLMs plateau; models tuned on a Bayesian model's predictions agree with it ~80% (2025) | [2503.17523](https://arxiv.org/abs/2503.17523) (Nat Commun) | `**` | closable by training |
| Simple set-shifting is at human level, with the error profile reversed | Wisconsin Card Sorting | 360 participants; more non-perseverative errors (d = -0.868) | at or above human score; o4-mini more perseverative (d = +1.195) (2025) | [2506.16163](https://arxiv.org/abs/2506.16163); [2505.22112](https://arxiv.org/abs/2505.22112) | `**`-`***` on level | closed on score |
| Revision driven by the wrong evidence: models abandon correct answers under pushback | SycEval rebuttals | none | answer changed in 58.19% of cases; right to wrong 14.66% (2025) | [2502.08177](https://arxiv.org/abs/2502.08177) | `**` (the failure itself `***`) | vendors claim reductions (self-reported) |

**Verdict.** Status `open` stands; the gap report reads covered through
`technique.oomdp-identification`.

- The cell's claim that revision is the thin side used to rest on author-scored write-ups with
  no human baseline. It now rests on human-baselined measures: AutumnBench, ZendoWorld and
  RULEARN.
- WCST says the gap is not "cannot switch" but "cannot revise a rich account".
- Bayesian teaching is a candidate technique (decision D4).

### `modeling.per-task-adaptation` — status `covered`, gap report covered

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| ARC-AGI-2: the average human tester is passed | semi-private, pass@2, ARC Prize verified | 66% of attempted test pairs (407 people); "100%" means each task solved by >=2 people; a per-person average of ~53% on the semi-private set is a *secondary* estimate | GPT-6 Astra max 95.0%† (listed 2026-09-02); Claude Opus 5.5 high 93.3%† (2026-09-22); Gemini 4 Argon high 91.3%† (2026-10-13); from 3.0% (2025-05) | [Astra results](https://arcprize.org/results/openai-gpt-6-astra)†; [Opus 5.5](https://arcprize.org/results/anthropic-claude-opus-5-5)†; [2505.11831](https://arxiv.org/abs/2505.11831) | `***` (several vendors' models, one verifier) | closed, 3% -> 95% in 16 months |
| ARC-AGI-1: saturated | H-ARC | 1,729 people, 64.2% on public eval† | Opus 5.5 98.5%† (2026-09) | [2409.01374](https://arxiv.org/abs/2409.01374)† | `***` | closed |
| Matching a human's score from the same materials by a different route | MTOB: Kalamang from one grammar book | one human learner: 51.6 / 57.0 chrF | long-context LLMs reach that score, but "almost all improvements stem from the book's parallel examples rather than its grammatical explanations" | [2309.16575](https://arxiv.org/abs/2309.16575); [2409.19151](https://arxiv.org/abs/2409.19151) (ICLR 2025) | `**` | closed on score, different mechanism |

**Verdict.** Status `covered` stands, and on the cell's flagship measure the human-machine gap
has closed at frontier scale. Three things are not in the cell's current text:

- the route can differ from the human one (MTOB, and the ConceptARC rule analysis);
- ARC Prize 2025's compute-capped track topped out near 24% on the ARC-AGI-2 private set, so the
  crossover is a frontier-scale result ([2601.10904](https://arxiv.org/abs/2601.10904));
- the lifetime data gap underneath per-task adaptation is untouched (see the training section).

### `modeling.commit-or-abstain` — status `open`, gap report EMPTY

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Reasoning training makes abstention worse | AbstentionBench: 20 LLMs, 20 datasets of unanswerable, underspecified and false-premise questions | none | reasoning fine-tuning cuts abstention 24% on average; "scaling models is of little use"† (2025-06) | [2506.09038](https://arxiv.org/abs/2506.09038)† | `**` | widening with reasoning models |
| Guess or abstain on factual recall: nearly all models guessed in 2025 | AA-Omniscience Index (correct minus incorrect), 6,000 questions | none | 3 models above zero, top 4.8† (2025-11); live board 46 (Opus 5.5 max, read 2026-10-20, undated) | [2511.13029](https://arxiv.org/abs/2511.13029)†; [board](https://artificialanalysis.ai/evaluations/omniscience) | `**` | closing on the coupling |
| Prospective confidence about human; retrospective confidence not revised after one's own failure | confidence judgements on prediction, Pictionary and trivia | human participants on the same tasks | about the same as humans prospectively; e.g. predicted 12/20, scored 1, then estimated 16 | Cash et al., [Memory & Cognition 2025](https://doi.org/10.3758/s13421-025-01755-4) | `**` (numbers partly from the publisher's summary) | unknown |
| Calibration on frontier-hard questions | Humanity's Last Exam, stated confidence | none | calibration error 50% at best (GPT-5) | [2501.14249](https://arxiv.org/abs/2501.14249); [lastexam.ai](https://lastexam.ai/) | `**` | closing slowly |

**Verdict.** Status `open` and EMPTY stand: nothing found couples confidence to the
commit/abstain/gather choice with an ablation.

- The cell's Limits paragraph ("every number here is a single hosted-API run ... with no human
  baseline") is out of date. Cash et al. is a human-baselined monitoring measure, and
  AA-Omniscience is a third-party, cross-model coupling measure.
- The gather-more branch still has no human-baselined measure. ARC-AGI-3's action counts are the
  nearest.

---

## Exploration faculty

### `exploration.experiment-design` — status `open`, gap report covered

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| An expected-information-gain question selector beats humans and GPT-5 | Collaborative Battleship (Captain asks, Spotter answers); head-to-head win rate | 42 players | Llama-4-Scout + Monte Carlo Bayesian experimental design: win rate against humans 8% -> 82%, against GPT-5 0% -> 67%, at ~1% of GPT-5's cost; question EIG 94.2% of the noise ceiling† | [2510.20886](https://arxiv.org/abs/2510.20886)† (ICLR 2026) | `**` (the Guess Who? replication is the same authors') | closing |
| Agents' own experiments carry almost no information | ZendoWorld (see belief-update) | 73.3% | 45.5%† | [2607.08233](https://arxiv.org/abs/2607.08233)† | `**` | one snapshot |
| Causal discovery by intervention: accuracy near the best humans, but models do not gain from choosing their own interventions | active blicket task | 306 adults; active beats passive (0.69 vs 0.45 on conjunctive identification) | gpt-5 and deepseek-reasoner match the best humans on disjunctive rules, not on conjunctive ones (2026-06) | [2606.06464](https://arxiv.org/abs/2606.06464) (CogSci 2026) | `**` | closing on accuracy, flat on intervention benefit |
| Where priors are rich, reasoning models out-explore people | Little Alchemy 2, elements found in 500 trials | mean 42 (29,493 players) | o1 177 (2025-05) | [2501.18009](https://arxiv.org/abs/2501.18009) | `**` | machine ahead; knowledge-rich regime |

**Verdict.** The status could go `open` -> `partial`; the gap report already reads covered.

- The cell's sentence "the discriminating-experiment framing has far less machine-side work
  attached" is no longer true. Battleship is an explicit EIG-scored selector, evaluated against
  humans and above them.
- It works because the hypothesis space (ship boards) can be enumerated and sampled: in
  cognate's terms, `solution-in-span`.
- Where the hypothesis space is open (ZendoWorld, AutumnBench), agents still choose
  near-uninformative experiments. This is decision D1.

---

## Goal-setting faculty

### `goal-setting.goal-inference` — status `partial`, gap report INDIRECT (2 edges)

The cell is reading (B): forming one's *own* objective with no instruction. Most of the
literature measures (A): reading *another* agent's goal.

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| (B) ARC-AGI-3 is the only large-scale measure of objective formation, and only as a composite | instruction-free games; the prompt says only "Your goal is to win." | as for hypothesis-formation | Astra 99.9% with the adapter (2026-09-03) | [astra](https://arcprize.org/blog/astra) | `**` composite; `*` for the goal step | closing on the composite; no number isolates the goal step |
| (A) Inferring a goal from observed action lags inferring a belief by ~50 points | MMToM-QA, 600 questions | goal 88.5, belief 97.5 (180 people)† | GPT-4V goal 34.7†; o3-mini-high goal 40.67 / belief 88.67†; AutoToM (inverse planning on GPT-4o) goal 69.33† (2024-01 to 2026-01) | [2401.08743](https://arxiv.org/abs/2401.08743)†; [2502.15676](https://arxiv.org/abs/2502.15676)† | `**` | closing through inverse-planning scaffolds; flat for plain reasoning models |
| (A) Literal theory of mind near human; it breaks under trivial perturbation | classic ToM batteries | 1,907 adults | GPT-4 at or above humans on 3 of 5 test types (2024-05) | [Strachan et al.](https://doi.org/10.1038/s41562-024-01882-z); fragility: [2302.08399](https://arxiv.org/abs/2302.08399), [2412.19726](https://arxiv.org/abs/2412.19726), [2602.10625](https://arxiv.org/abs/2602.10625) | `***` "literal ToM scores do not carry over" | closing on literal ToM; flat on functional ToM |

**Verdict.** Status `partial` and the INDIRECT reading stand.

- ARC-AGI-3 cannot earn `direct`: it is a composite, and the level-completion flag is handed to
  the agent, the same distance-rule clause that caps `technique.test-time-digital-twin`.
- The (A) findings belong to a different cell. Creating one would also resolve this cell's
  declared `human_source` mismatch (decision D6).

### `goal-setting.subgoal-recognition` — status `open`, gap report INDIRECT (1 edge)

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Long-horizon computer use: agents rarely verify or repair | OSWorld 2.0, 108 tasks, 500-step budget | task *time* only (median ~1.6 h); no human success rate | 20.6% binary (Claude Opus 4.8, paper v2 2026-07-13); recovery plus repair <7% of steps; verification 9.8% of activity windows | [2606.29537](https://arxiv.org/abs/2606.29537) | `**` | 31.4% for Claude Opus 5 (2026-07-24) in Epoch's compilation, not re-checked |
| Believing a subgoal was achieved when it was not | Vending-Bench, 2,000-message business simulation | **one** participant | collapses start when the model assumes an expected delivery has arrived (2025-02) | [2502.15840](https://arxiv.org/abs/2502.15840) | `**` | unknown |
| Self-verification collapses where a sound external verifier helps | Game of 24, graph colouring, STRIPS | none | GPT-4 with an external verifier (2024-02) | [2402.08115](https://arxiv.org/abs/2402.08115) | `**` | pre-reasoning models |

**Verdict.** Status `open` and the INDIRECT reading stand.

- Every finding shows the symptom the cell's Problem names: progress not told from noise,
  achievement not checked.
- No benchmark compares humans and machines on recognising an achievement. The measurement
  itself is missing.

---

## Planning-execution faculty

### `planning-execution.goal-decomposition` — status `partial`, gap report covered

| Finding | Measure | Human | Best machine (date) | Source | Stars | Trend |
|---|---|---|---|---|---|---|
| Plain Blocksworld solved; obfuscated and longer problems not | PlanBench, 600 instances, VAL-checked | 39 of 50 gave a valid plan for one instance (78%) | o1-preview 97.8% plain, 52.8% Mystery, 37.3% randomised, 23.63% on 6-20 blocks; flags only 27% of unsolvable instances; $42.12 per 100 instances† (2024-09) | [2409.13373](https://arxiv.org/abs/2409.13373)†; human study [2305.15771](https://arxiv.org/abs/2305.15771) | `**` | no 2025-26 frontier number on the obfuscated set |
| Task length at 50% success grows exponentially | METR time horizon (HCAST, RE-Bench, SWAA; 228 tasks in TH1.1) | human expert time is the axis | doubling every 196 d (2019-2025), 131 d post-2023, 89 d post-2024† (TH1.1); the most capable model measured is at or above the suite's stated 16 h ceiling, with an 80% horizon of ~3-4 h | [METR TH1.1](https://metr.org/blog/2026-1-29-time-horizon-1-1/)†; [time-horizons](https://metr.org/time-horizons/)† | `***` trend | closing; METR stopped updating the page 2026-09-08 |
| Execution of a given plan degrades on one's own errors (self-conditioning) | synthetic retrieve-and-add with an explicit plan | none | GPT-5 thinking 2,176 steps at >=80%; non-thinking models fail at ~4-6 (2025-09) | [2509.09677](https://arxiv.org/abs/2509.09677) (ICLR 2026) | `**` | closing between generations; flat with size |
| Real freelance projects: furthest from parity | Remote Labor Index | 100% by construction | 21.25% (Claude Opus 5.5, 2026-09-22, Epoch's compilation) from 2.5% at the paper (2025-10) | [2510.26787](https://arxiv.org/abs/2510.26787) | `**` | closing from a low base |

**Verdict.** Status `partial` and the covered reading stand.

- The measured progress is in *executing* long tasks. No measure separates decomposition from
  execution.
- The cell's open part, decomposition over learned, noisy representations, has no benchmark of
  its own; ARC-AGI-3 folds it into the composite.

---

## Training and learning: gaps with no cell

All 14 cells are inference-time faculties. The reading passes proposed 26 candidate cells
between them, overlapping heavily. They merge into six, each stated so that a system (with its
training procedure) meets it or does not.

| Merged candidate | Definition (met or not) | Merged from | Strongest finding |
|---|---|---|---|
| `learning.sample-efficiency` | Reaches a stated competence from no more data than a human learner gets for it (language: at most ~10^8 words; interactive play: no more play than the human comparison had). | learning.sample-efficiency, modeling.lifetime-sample-efficiency, modeling.sample-efficient-learning, exploration.acquisition-efficiency (training half); compute and energy budgets as regimes | BabyLM 2024: at 10^8 words the best model is within 2.5 points of the human BLiMP score, but scores 58.4 on EWoK, where chance is 50†. Frontier corpora: 15.6T tokens (Llama 3, 2024-07) and 36T (Qwen3, 2025-05), self-reported. `***` |
| `learning.accelerating-returns` | The gain from each further unit of input rises as competence grows, rather than following a fixed power law (kappa > 1 under Frank's estimator). | learning.accelerating-returns | Children kappa 10.6-13.3 (1,841 children, 5 datasets), against GPT-2-small on child-directed speech at 1.16 (IQR 0.93-1.46)†, [2608.17120](https://arxiv.org/abs/2608.17120), 2026-08-17. `**` |
| `learning.prior-acquisition` | Acquires a core prior (objectness, physics, object categories) from no more egocentric experience than a child of the matching age, with no authored vocabulary. | learning.prior-acquisition-efficiency, learning.prior-acquisition-from-experience, learning.grounded-acquisition | 128 h of video gives >70% on simple-scene physics†, while child-headcam V-JEPA is at chance on IntPhys 2. 200 h of one child's video gives ~70% of an ImageNet model ([2305.15372](https://arxiv.org/abs/2305.15372)). No BabyLM multimodal entry beat its baselines in 2024 or 2025†. `**` |
| `learning.few-exposure-consolidation` | An item met once (or k times) is written to a persistent store the system owns (weights or memory) and is recallable at a stated delay. | learning.few-exposure-retention, memory.few-exposure-consolidation, modeling.long-term-consolidation, modeling.self-assessment-update (in part) | CHC long-term storage 0/10 for GPT-4 and GPT-5†. Weights need ~1000 exposures per fact for full capacity†. SORT: readers 0.64 a week after reading, models fine-tuned on the book "did not improve", the same models 0.95 with the book in context†. `**` |
| `learning.continual-without-forgetting` | After learning new tasks, facts or edits, keeps at least X% of prior held-out performance and its ability to learn more (plasticity). | learning.continual-without-forgetting, learning.sustained-plasticity, learning.targeted-knowledge-update | Learning new facts drops NaturalQuestions F1 by 89% (full fine-tuning), 71% (LoRA), 11% (sparse memory fine-tuning)† ([2510.15103](https://arxiv.org/abs/2510.15103), 2025-10). Plasticity is lost over ~2,000 tasks, and continual backprop keeps it ([Nature 632:768](https://pmc.ncbi.nlm.nih.gov/articles/PMC11338828/), 2024-08). `**`-`***` |
| `learning.cross-episode-improvement` | Over episodes or sessions in deployment, improves from its own experience and keeps the gain. | learning.cross-episode-improvement, memory.cross-session-recall, exploration.acquisition-efficiency (test-time half) | ARC-AGI-3: "Solved the level, didn't learn the game" (2026-05-01) with every environment solved by >=2 untrained people, then 99.9% once provider reasoning state persists (2026-09-03). LoCoMo: humans 87.9 F1, best system 41.4 ([2402.17753](https://arxiv.org/abs/2402.17753), 2024). SEAL acquires and still forgets ([2506.10943](https://arxiv.org/abs/2506.10943)). `**` |

**Not cells.**

- Compute (~10^24 FLOP for a brain lifetime, `*` estimate, against ~5e26 for Grok 4, an Epoch
  estimate) and energy (~3 MWh for a brain to age 18, against ~310 GWh for Grok 4, an Epoch
  estimate) are *budgets*. They belong as the `regime` of `learning.sample-efficiency` rows, not
  as faculties.
- The machine's advantage, experience parallelism, is recorded the same way: AlphaZero reached
  superhuman chess in 9 hours of wall-clock from ~44M self-play games
  ([DeepMind 2018](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/)).
  It is a regime fact, not a faculty humans lack.

**Faculty.** Is a new `learning` faculty warranted? The honest case is that it partly already
exists. The supplied/acquired test in `SCHEMA.md` asks *where a prior came from* for seven
cells, which is a question about learning. A `learning` faculty would make that question
first-class rather than a grading rule.

It is warranted on three conditions:

- each cell is graded on what the *learning procedure* produces, so a technique such as sparse
  memory fine-tuning or continual backprop addresses it;
- each has at least one human-baselined measure;
- it stays separate from `modeling.per-task-adaptation`, which is within an episode.

Four of the six meet all three today: sample-efficiency, prior-acquisition,
few-exposure-consolidation and cross-episode-improvement. Continual-without-forgetting has
techniques but only toy-scale human anchors. Accelerating-returns has one paper.

**What the training side says overall.**

- At a fixed human-scale budget, the gap is closing for form (grammar at 10^8 words; Atari
  above human with 100K steps, BBF [2305.19452](https://arxiv.org/abs/2305.19452) `***`) and flat
  for meaning, world knowledge and grounding.
- At the frontier, data, compute and energy ratios widen by design.
- Consolidation is the one learning gap that the inference side cannot hide. A text in the
  context window is used better than a human uses memory (SORT 0.95 against 0.64), and the same
  text trained into weights is not retrievable at all.

### Inference-side gaps with no cell (brief)

These were proposed by the reading passes and are listed so the choice is explicit. They are
decisions D7-D8, not findings of this section.

| Candidate | One line | Strongest finding | Recommendation |
|---|---|---|---|
| `planning-execution.execution-reliability` | carries out a known plan over many steps without per-step errors compounding | self-conditioning (2,176 vs 4-6 steps); METR 80% horizon ~3-4 h against 50% at >=16 h | enter |
| `goal-setting.goal-attribution` | infers another agent's goal from its actions and adapts to it | MMToM goal 88.5 vs 40.67 (o3-mini-high)† | enter, and move goal-inference's (A) sources to it |
| `modeling.mental-transformation` | simulates a rotation or viewpoint change and reads the answer off the result | GPT-5 below random on 3D mental rotation; perspective taking 50-80 points short | enter |
| `modeling.systematic-recombination` | composes known primitives into a rule never seen in combination | Lake & Baroni: MLC 82.4% vs people 80.7% (2023) | fold into hypothesis-formation |
| `memory.effective-long-context` | accuracy on non-literal, whole-document tasks holds at length L | NoCha: readers 96.9% (claim level) vs GPT-5 68.5% (pair level) | hold (units differ, and no 2026 rows) |
| `modeling.counterfactual-invariance`, `modeling.relevance-filtering` | performance independent of how common the task variant is; irrelevant facts ignored | GSM-NoOp drop of 17.5 points (o1-preview, 2024-10) | hold (no human baseline on the same items) |
| `knowledge.temporal-currency`, `efficiency.processing-speed` | knows its knowledge horizon; elementary speed | under-searched; CHC speed 3/10 flat | hold |

---

## How far the measure can be trusted

**Human baselines are the weakest part of the instrument.**

- A review of 115 human baselines in model evaluations† ([2506.13776](https://arxiv.org/abs/2506.13776),
  2025-06-09) found:
  - a median of 8 baseliners;
  - a power analysis in 2 of 115;
  - a significance test of the AI-human difference in 10 of 115 (8.7%);
  - the same test set as the models in 59%;
  - human data released in 22%;
  - random sampling in none.
- The baselines cited here fit that picture:
  - ARC-AGI-3: about 10 players per environment, from a 458-person panel†. Its action baseline
    was redefined from the second-best human per level to the median player.
  - SimpleBench: 9 participants.
  - Vending-Bench: one participant.
  - SelfAware: two volunteers.
  - REVEAL: 25 items.
- The same name covers different aggregations: the individual average (H-ARC 64.2%), the panel
  union of at least two solvers (ARC-AGI-2's "100%"), a majority of three (IntPhys 2), the median
  completer (ARC-AGI-3) and the 80th percentile (AutumnBench).
- Two "parity" rows built on different aggregations are not comparable, for the same reason two
  scores under different cost caps are not. Decision D9 proposes a `human_baseline` qualifier.

**Contamination.**

- Public benchmarks leak: CoreCognition, WCST, Blocksworld and ConceptARC are all public. A
  fresh, matched copy of GSM8K cost some model families up to 8 points, frontier models of 2024
  little ([2405.00332](https://arxiv.org/abs/2405.00332)).
- Private sets answer this at the price of being unauditable.
- ARC-AGI-3's semi-private games are played through vendor APIs.
- Benchmark keys carry errors too: FrontierMath v2 corrected 42% of its problems, and an expert
  re-check of HLE chemistry and biology found ~29% of answers in conflict with the literature
  (both draft-read, not re-checked).

**Harness dependence.** On ARC-AGI-3, GPT-6 Astra at high effort scores 54.8% when it keeps
only the notes it chooses (Standard harness) and 99.9% when the provider keeps its reasoning
state (Provider Adapter)†. At low effort the scores are 17.5% and 98.0%†
([results page](https://arcprize.org/results/openai-gpt-6-astra)). The gap between the two
harnesses is larger than the gap left under the Standard harness at its best (62.7%).

The general pattern is the same: in-context exploration was fragile unless a harness summarised
the history ([2403.15371](https://arxiv.org/abs/2403.15371)); the VET-Bench fix is an explicit
trajectory state; and TravelPlanner closed when a solver took the search. A gap closed by a
harness is closed for the *system*, not for the model, and cognate's technique side is where that
distinction belongs.

**Different model generations on open and closed gaps.** This is the main limitation of the
survey.

- Closing evidence is on 2026 models: ARC-AGI-2/3, FrontierMath, ClockBench, METR.
- Most human-baselined open gaps were last measured on 2024-25 models: RULEARN (GPT-4o),
  AutumnBench (o3, Claude 4 Sonnet), MMToM-QA (o3-mini), ConceptARC (o3), the PlanBench
  obfuscated set (o1-preview), the Dehaene paradigm (Gemini 1.5), LoCoMo (2024 systems) and
  NoCha (GPT-5).
- So "open" in this note often means "open when last measured". Hypothesis H1 below makes that
  a claim that can lose.

**Machine-only metrics.**

- About half the continual-learning and memory findings have no human figure on the same task;
  they measure a machine against its own earlier self.
- Where a metric changed under a leaderboard (LoCoMo's F1 to an LLM-judge score), the
  human-comparable series stops. Vendor memory scores diverge from independent reruns by up to
  28 points (Redis rerun, 2026-09-21, a competitor's report).

---

## Candidate hypotheses

At most three, in cognate's hypothesis format. Each is argued, one star, until a check runs.

```yaml
id: hypothesis.stale-gaps
kind: hypothesis
name: Open Gaps Are Stale Measurements
claim: >-
  Most human-baselined gaps that read open in 2026-10 were last measured on 2024-25 models,
  and re-measuring them on 2026 frontier systems closes at least half of each gap, except for
  gaps in perception of dynamics and in consolidation into a persistent store.
source: this survey note (2026-10-20), "How far the measure can be trusted"
date: 2026-10-20
status: argued
stars: 1
bears_on: [modeling.hypothesis-formation, modeling.belief-update, exploration.experiment-design, goal-setting.goal-inference, priors.basic-physics]
predicts:
  - claim: >-
      the next published re-run of RULEARN, AutumnBench, ZendoWorld, MMToM-QA (goal questions)
      or the ConceptARC rule analysis on a 2026 frontier model closes at least half of the
      2024-25 human-machine gap on that benchmark
    check: >-
      the benchmark's own results table, same human baseline, model release >= 2026-01;
      gap closed = (new - old) / (human - old)
  - claim: >-
      IntPhys 2 and the SORT fine-tuned-weights arm do NOT close by half when re-run on 2026
      systems
    check: the IntPhys 2 Main split and SORT's parametric-memory arm, same protocol
```

```yaml
id: hypothesis.parity-time-shrinks
kind: hypothesis
name: Time to Human Parity Shrinks per Benchmark Generation
claim: >-
  For a benchmark family re-calibrated against fresh human testing each generation, the time
  from launch to the first verified general model at or above the declared human baseline
  shrinks with each generation: ARC-AGI-1 about 61 months, ARC-AGI-2 about 9-11 months,
  ARC-AGI-3 about 5 months (Provider Adapter harness only).
source: https://arcprize.org/blog/astra
date: 2026-10-20
status: argued
stars: 1
bears_on: [modeling.per-task-adaptation, modeling.hypothesis-formation, hypothesis.bitter-lesson]
predicts:
  - claim: >-
      the next ARC generation has a verified general-model score at or above its own declared
      human baseline within 6 months of launch, under the harness ARC Prize labels Standard
    check: >-
      arcprize.org results pages; launch date against the first verified at-or-above score.
      Parity reached only through a non-Standard harness is recorded as a partial result,
      not a pass
```

```yaml
id: hypothesis.consolidation-flat
kind: hypothesis
name: Consolidation Does Not Arrive with Scale
claim: >-
  Writing a once-seen item into a persistent store is not delivered by scaling pretraining:
  frontier systems' long-term storage stays near zero on a CHC-style battery while their
  total rises, and a book trained into weights stays near chance on order recall while the
  same book in context is above human.
source: https://arxiv.org/abs/2510.18212
date: 2026-10-20
status: argued
stars: 1
bears_on: [learning.few-exposure-consolidation, modeling.per-task-adaptation]
predicts:
  - claim: "the first published CHC rescoring of a 2026 frontier model gives long-term memory storage at most 2/10 and a total above 70%"
    check: >-
      agidefinition.safe.ai or a later version of arXiv 2510.18212, Table 1; record whether
      product memory features were allowed, and if they were, record a split result rather
      than a loss
  - claim: "a SORT-style parametric-memory test on a model of 70B parameters or more stays below the human 0.64 after one reading"
    check: Book-SORT protocol (arXiv 2410.08133), fine-tuned arm, 50-word segments
```

**Considered and not proposed.**

- *The 50%/80% reliability ratio stays flat at ~5x.* METR stopped updating its time-horizon page
  on 2026-09-08, and the ratio rows (from Epoch's copy) were not re-checked, so the check has no
  maintained source.
- *Perturbation robustness has closed.* There is no human baseline on the same items.
- *The data-efficiency gap widens.* True by arithmetic, so it is not a prediction anyone can lose.

---

## Decisions taken (2026-10-20)

Each decision was taken as recommended. The commits that applied them cite this note.

- **Prose and evidence.** The cells' prose now carries the human-baselined measures above; no
  `status`, edge or grade changed through prose alone.
- **D1.** [`technique.bayesian-experimental-design`](../techniques/bayesian-experimental-design.md)
  entered at `direct` on `exploration.experiment-design`, which moved `open` -> `partial`;
  `hypothesis.bitter-lesson`'s refutation paragraph was rewritten to match.
- **D2.** [`technique.latent-video-prediction`](../techniques/latent-video-prediction.md) entered at
  `partial` on `priors.basic-physics` (EMPTY -> INDIRECT, status still `open`), and was examined
  and refused for `priors.objectness`. V-JEPA 2-AC was not read.
- **D3.** Deferred: no multimodal-pretraining node.
- **D4.** [`technique.bayesian-teaching`](../techniques/bayesian-teaching.md) entered at `partial`
  on `modeling.belief-update`.
- **D5.** Deferred: `modeling.commit-or-abstain` stays EMPTY, with AA-Omniscience named in its
  prose as the measure a future technique would be scored on.
- **D6.** [`goal-setting.goal-attribution`](../patterns/goal-setting/goal-attribution.md) entered,
  `open`, with the two (A) human sources moved to it from `goal-setting.goal-inference`.
- **D7.** [`planning-execution.execution-reliability`](../patterns/planning-execution/execution-reliability.md)
  entered, `open`.
- **D8.** [`modeling.mental-transformation`](../patterns/modeling/mental-transformation.md)
  entered, `open`. Systematic recombination is folded into `modeling.hypothesis-formation`'s
  prose, self-assessment update into `modeling.commit-or-abstain`'s, and individuation into a
  `completed_by` edge from `priors.objectness` to `priors.numbers-and-counting`. The five held
  candidates are recorded only in this note.
- **D9.** Evidence rows take an optional `human_baseline` qualifier, and `build_graph.py` warns
  on a row whose claim mentions humans without one.
- **D10.** A `learning` faculty, with four `open` cells: `learning.sample-efficiency`,
  `learning.prior-acquisition`, `learning.few-exposure-consolidation` and
  `learning.cross-episode-improvement`. Continual-without-forgetting and accelerating-returns
  are held.
- **D11.** `hypothesis.consolidation-flat` and `hypothesis.parity-time-shrinks` entered;
  `hypothesis.stale-gaps` is held, and its text is above.
- **D12.** This folder.
- **D13.** The note and every node it touched were re-read for anything outside the public
  record before entering.
