---
id: learning.sample-efficiency
kind: capability
name: Sample Efficiency
faculty: learning
human_source:
  - title: "Frank, Children, but not language models, show accelerating returns in word learning (arXiv 2608.17120, 2026)"
    url: https://arxiv.org/abs/2608.17120
part_of: [learning]
completed_by: []
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

# Sample Efficiency

**Context.** A system is trained, and its competence is then measured against a person's.

**Problem.** Matching a person's competence says nothing about how much input it took. A child
reaches adult-like language on roughly 10^8 words; frontier models train on 10^13 tokens and
more, a ratio of about 10^5 that widens as training sets grow. At a human-scale budget the
gap closes for form and stays open for meaning: in BabyLM 2024, the best model trained on
10^8 words is within 2.5 points of the human score on BLiMP's grammar items but scores 58.4 on
EWoK's world knowledge, where chance is 50 ([2412.05149](https://arxiv.org/abs/2412.05149)).
In interactive play the budget can be met: BBF is above human on Atari with 100K environment
steps ([2305.19452](https://arxiv.org/abs/2305.19452)). One difference is not of degree.
Children's word learning accelerates with what they already know (kappa 10.6 to 13.3 across
1,841 children in five datasets), while a language model trained on child-directed speech
shows about constant returns (kappa 1.16) ([2608.17120](https://arxiv.org/abs/2608.17120)).
That is one preprint, so it is carried as a predicate on this cell rather than a cell of its
own until it is replicated.

**Therefore.** State the competence and the budget together: a system meets this cell when it
reaches a stated competence from no more data than a human learner gets for it (for language,
at most about 10^8 words; for interactive play, no more play than the human comparison had).

**How a technique is graded here.** On what the learning procedure produces from the stated
budget. A result bought with more data than the human comparison had does not address the
cell, however good. Compute and energy are not cells: a row records them as its `regime`.

**Status: open (entered 2026-10-20).** No technique in the register addresses it. The
candidates are the BabyLM entries and sample-efficient reinforcement learners such as BBF;
none has been read as a technique.
