---
id: modeling.per-task-adaptation
kind: capability
name: Per-Task Adaptation
faculty: modeling
human_source:
  - title: "Learning-to-learn / rapid within-task skill acquisition"
    url: https://arxiv.org/abs/1604.00289
part_of: [modeling]
completed_by: []
status: covered
provenance:
  entered: 2026-09-02
  commit: fb41fa3
  frame: catalogue-survey-seed
  note: >-
    chosen to make both traversal directions real, from the four catalogue works the README
    names (Minsky; Hassabis et al.; Kotseruba & Tsotsos; Wray, Kirk & Laird) - selected to
    exercise the format, not sampled from a field
---

# Per-Task Adaptation

**Context.** A novel task arrives with a handful of demonstrations and no further supervision.

**Problem.** A fixed model applies fixed competence. Chollet's definition makes
*skill-acquisition efficiency* the thing being measured, which means the ability to get
better at this specific task, from this specific evidence, within this specific episode.

**Therefore.** Spend inference-time compute on adapting to the instance, whether by
fitting weights, searching a latent, or accumulating an in-context account.

**Status: covered.** This is the best-served cell in the register — the 2024 and 2025
leaderboards are largely a contest between ways of doing it. Marked `covered` for field
maturity, which says nothing about whether any given system has adopted it.

**The 2026 crossover.** On the cell's flagship measure, frontier general models now pass the
human testers. ARC Prize verifies GPT-6 Astra (max effort) at 95.0% on the ARC-AGI-2
semi-private set ([results page](https://arcprize.org/results/openai-gpt-6-astra), listed
2026-09-02) and Claude Opus 5.5 (high effort) at 93.3%
([results page](https://arcprize.org/results/anthropic-claude-opus-5-5), 2026-09-22). The
testers who calibrated ARC-AGI-2 solved 66% of the test pairs they attempted
([2505.11831](https://arxiv.org/abs/2505.11831)). Two limits go with it. The crossover is a
frontier-scale result: ARC Prize 2025's compute-capped track topped out near 24% on the
ARC-AGI-2 private set ([2601.10904](https://arxiv.org/abs/2601.10904)). And a matched score
can come by a different route: on MTOB, long-context models reach a human learner's score
for translating Kalamang from one grammar book, but "almost all improvements stem from the
book's parallel examples rather than its grammatical explanations"
([2409.19151](https://arxiv.org/abs/2409.19151)).
