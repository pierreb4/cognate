---
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
bears_on:
  - learning.few-exposure-consolidation
  - modeling.per-task-adaptation
predicts:
  - claim: "the first published CHC rescoring of a 2026 frontier model gives long-term memory storage at most 2/10 and a total above 70%"
    check: >-
      agidefinition.safe.ai or a later version of arXiv 2510.18212, Table 1; record whether
      product memory features were allowed, and if they were, record a split result rather
      than a loss
  - claim: "a SORT-style parametric-memory test on a model of 70B parameters or more stays below the human 0.64 after one reading"
    check: Book-SORT protocol (arXiv 2410.08133), fine-tuned arm, 50-word segments
provenance:
  entered: 2026-10-20
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Consolidation Does Not Arrive with Scale

**The claim.** Of the learning gaps, consolidation is the one the inference side cannot hide.
On the CHC-based definition of AGI, GPT-4 scores 27% and GPT-5 57%, and both score 0 of 10 on
long-term memory storage (arXiv 2510.18212, Table 1). On SORT, a model with a book in context
recalls the order of its segments at 0.95, above the 0.64 of people a week after reading, while
models fine-tuned on the book do not improve (arXiv 2410.08133). The capability that rose is
using what is in front of the model; the one that stayed at zero is keeping what is not.

**Why it is held as a hypothesis.** Two batteries and two model generations are not a trend.
The CHC scoring has been applied to two models, by its own authors; SORT's fine-tuned arm was
run on 7-8B models. Holding the claim as a node means the next scoring of a 2026 model can
move it, either way.

**What would refute it.** A 2026 frontier model scoring above 2 of 10 on CHC long-term storage
without product memory features, or a model of 70B parameters or more reaching people's 0.64 on
SORT's fine-tuned arm after one reading. A product memory feature that lifts the CHC score is
recorded as a split result, not a refutation: it is a store the system was handed, which is
the `incidental` case of [`learning.few-exposure-consolidation`].

**Where it stops.** It says scaling pretraining does not deliver consolidation. It does not
say no mechanism can: sparse memory fine-tuning and other targeted updates are the candidates
the cell names, and a technique that passes its check would address the cell without touching
this claim.
