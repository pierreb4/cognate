---
id: learning.few-exposure-consolidation
kind: capability
name: Few-Exposure Consolidation
faculty: learning
human_source:
  - title: "McClelland, McNaughton & O'Reilly, Why there are complementary learning systems in the hippocampus and neocortex (Psychological Review 102, 1995)"
    url: https://doi.org/10.1037/0033-295X.102.3.419
  - title: "Pink et al., Assessing Episodic Memory in LLMs with Sequence Order Recall Tasks (arXiv 2410.08133, 2024): human readers a week after reading"
    url: https://arxiv.org/abs/2410.08133
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

# Few-Exposure Consolidation

**Context.** A system meets an item once, or a few times: a fact, an event, a book it read.
Later, with the item gone from its input, it is asked about it.

**Problem.** People write a once-seen experience into a lasting store; in the complementary
learning systems account, a fast hippocampal store holds it and slowly teaches the neocortex.
Machines either hold the item in context, where it is used well and lost at the end of the
session, or train it into weights, where one exposure barely registers. Three measures show
the gap. On the CHC-based definition of AGI, GPT-4 and GPT-5 both score 0 of 10 on long-term
memory storage while GPT-5's total rises to 57% ([2510.18212](https://arxiv.org/abs/2510.18212)).
Language models need each fact visited about 1,000 times in training to store it at full
capacity ([2404.05405](https://arxiv.org/abs/2404.05405)). And on SORT, 155 readers recall the
order of a book's segments at 0.64 about a week after reading it; a model with the book in
context scores 0.95 (Mixtral-8x22B), but fine-tuning models on the book (Llama3-8B,
Mistral-7B) "did not improve SORT performance" ([2410.08133](https://arxiv.org/abs/2410.08133)).
A text in the context window is used better than a person uses memory, and the same text
trained into weights is not retrievable.

**Therefore.** Write an item met once, or k times, into a persistent store the system owns
(its weights or a memory it maintains), so that it is recallable at a stated delay.

**How a technique is graded here.** On recall at a stated delay with the item out of context.
Holding the item in the context window, or retrieving it from a store a person wrote, is not
consolidation and is `incidental` at most.

**Status: open (entered 2026-10-20).** No technique in the register addresses it. Sparse
memory fine-tuning is a candidate: learning new facts that way costs 11% of held-out
NaturalQuestions F1, against 89% for full fine-tuning and 71% for LoRA
([2510.15103](https://arxiv.org/abs/2510.15103)); it has not been read as a technique, and
its row measures forgetting, not recall of the new item at a delay.
