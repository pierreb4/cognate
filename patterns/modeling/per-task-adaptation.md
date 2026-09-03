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
