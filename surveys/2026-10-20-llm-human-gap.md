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



---

*Split on 2026-11-04 so each file reads whole: what follows moved word for word to 4 parts beside this file, each heading below linking to its place. Line numbers cited before that day are the whole file's: `git show 9af47e1:surveys/2026-10-20-llm-human-gap.md`.*

## Prior faculty

→ [part 2](2026-10-20-llm-human-gap-part-2.md#prior-faculty)

### `priors.objectness` — status `partial`, gap report INDIRECT (1 edge)

→ [part 2](2026-10-20-llm-human-gap-part-2.md#priorsobjectness--status-partial-gap-report-indirect-1-edge)

### `priors.basic-physics` — status `open`, gap report EMPTY

→ [part 2](2026-10-20-llm-human-gap-part-2.md#priorsbasic-physics--status-open-gap-report-empty)

### `priors.geometry-and-topology` — status `partial`, gap report INDIRECT (1 edge)

→ [part 2](2026-10-20-llm-human-gap-part-2.md#priorsgeometry-and-topology--status-partial-gap-report-indirect-1-edge)

### `priors.numbers-and-counting` — status `open`, gap report INDIRECT (1 edge)

→ [part 2](2026-10-20-llm-human-gap-part-2.md#priorsnumbers-and-counting--status-open-gap-report-indirect-1-edge)

### `priors.agentness` — status `open`, gap report EMPTY

→ [part 2](2026-10-20-llm-human-gap-part-2.md#priorsagentness--status-open-gap-report-empty)

## Modeling faculty

→ [part 3](2026-10-20-llm-human-gap-part-3.md#modeling-faculty)

### `modeling.state-abstraction` — status `partial`, gap report INDIRECT (1 edge)

→ [part 3](2026-10-20-llm-human-gap-part-3.md#modelingstate-abstraction--status-partial-gap-report-indirect-1-edge)

### `modeling.hypothesis-formation` — status `partial`, gap report covered

→ [part 3](2026-10-20-llm-human-gap-part-3.md#modelinghypothesis-formation--status-partial-gap-report-covered)

### `modeling.belief-update` — status `open`, gap report covered

→ [part 3](2026-10-20-llm-human-gap-part-3.md#modelingbelief-update--status-open-gap-report-covered)

### `modeling.per-task-adaptation` — status `covered`, gap report covered

→ [part 3](2026-10-20-llm-human-gap-part-3.md#modelingper-task-adaptation--status-covered-gap-report-covered)

### `modeling.commit-or-abstain` — status `open`, gap report EMPTY

→ [part 3](2026-10-20-llm-human-gap-part-3.md#modelingcommit-or-abstain--status-open-gap-report-empty)

## Exploration faculty

→ [part 3](2026-10-20-llm-human-gap-part-3.md#exploration-faculty)

### `exploration.experiment-design` — status `open`, gap report covered

→ [part 3](2026-10-20-llm-human-gap-part-3.md#explorationexperiment-design--status-open-gap-report-covered)

## Goal-setting faculty

→ [part 3](2026-10-20-llm-human-gap-part-3.md#goal-setting-faculty)

### `goal-setting.goal-inference` — status `partial`, gap report INDIRECT (2 edges)

→ [part 3](2026-10-20-llm-human-gap-part-3.md#goal-settinggoal-inference--status-partial-gap-report-indirect-2-edges)

### `goal-setting.subgoal-recognition` — status `open`, gap report INDIRECT (1 edge)

→ [part 3](2026-10-20-llm-human-gap-part-3.md#goal-settingsubgoal-recognition--status-open-gap-report-indirect-1-edge)

## Planning-execution faculty

→ [part 4](2026-10-20-llm-human-gap-part-4.md#planning-execution-faculty)

### `planning-execution.goal-decomposition` — status `partial`, gap report covered

→ [part 4](2026-10-20-llm-human-gap-part-4.md#planning-executiongoal-decomposition--status-partial-gap-report-covered)

## Training and learning: gaps with no cell

→ [part 4](2026-10-20-llm-human-gap-part-4.md#training-and-learning-gaps-with-no-cell)

### Inference-side gaps with no cell (brief)

→ [part 4](2026-10-20-llm-human-gap-part-4.md#inference-side-gaps-with-no-cell-brief)

## How far the measure can be trusted

→ [part 4](2026-10-20-llm-human-gap-part-4.md#how-far-the-measure-can-be-trusted)

## Candidate hypotheses

→ [part 5](2026-10-20-llm-human-gap-part-5.md#candidate-hypotheses)

## Decisions taken (2026-10-20)

→ [part 5](2026-10-20-llm-human-gap-part-5.md#decisions-taken-2026-10-20)
