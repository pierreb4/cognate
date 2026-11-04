<!-- Part 5 of 5 of 2026-10-20-llm-human-gap.md, moved there word for word on 2026-11-04. -->
[← 2026-10-20-llm-human-gap.md](2026-10-20-llm-human-gap.md) · [← part 4](2026-10-20-llm-human-gap-part-4.md) · part 5 of 5

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
