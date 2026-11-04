<!-- Part 3 of 5 of 2026-10-20-llm-human-gap.md, moved there word for word on 2026-11-04. -->
[← 2026-10-20-llm-human-gap.md](2026-10-20-llm-human-gap.md) · [← part 2](2026-10-20-llm-human-gap-part-2.md) · part 3 of 5 · [part 4 →](2026-10-20-llm-human-gap-part-4.md)

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

