<!-- Part 4 of 5 of 2026-10-20-llm-human-gap.md, moved there word for word on 2026-11-04. -->
[← 2026-10-20-llm-human-gap.md](2026-10-20-llm-human-gap.md) · [← part 3](2026-10-20-llm-human-gap-part-3.md) · part 4 of 5 · [part 5 →](2026-10-20-llm-human-gap-part-5.md)

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
| `learning.few-exposure-consolidation` | An item met once (or k times) is written to a persistent store the system owns (weights or memory) and is recallable at a stated delay. | learning.few-exposure-retention, memory.few-exposure-consolidation, modeling.long-term-consolidation, modeling.self-assessment-update (in part) | CHC long-term storage 0/10 for GPT-4 and GPT-5†. Weights need ~1000 exposures per fact for full capacity†. SORT: readers 0.64 a week after reading, models fine-tuned on the book "did not improve", the same models 0.95 with the book in context† [corrected on entry from the check table, row 18: not the same models; Mixtral-8x22B scored 0.95 in context, and the fine-tuned models were Llama3-8B and Mistral-7B]. `**` |
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

