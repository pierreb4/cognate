---
id: goal-setting.goal-attribution
kind: capability
name: Goal Attribution
faculty: goal-setting
human_source:
  - title: "Baker, Saxe & Tenenbaum, Action Understanding as Inverse Planning (Cognition, 2009)"
    url: https://www.sciencedirect.com/science/article/pii/S0010027709001607
  - title: "Gergely & Csibra, Teleological reasoning in infancy: the naive theory of rational action (TiCS, 2003)"
    url: https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(03)00128-1
part_of: [goal-setting]
completed_by: []
status: open
provenance:
  entered: 2026-10-20
  commit: c6ca7db
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Goal Attribution

**Context.** Another agent is acting in view: a person, a character, a sprite that moves on
its own. Its goal is not stated.

**Problem.** Reading what the other agent wants from what it does, and acting on that reading
in context, is the capability [`goal-setting.goal-inference`] declared it is *not*: that cell
is forming one's own objective, reading (B); this is reading another's, reading (A). Infants
read goals from actions by assuming the agent acts efficiently toward them, and inverse
planning formalises that as inference over the agent's utility given its behaviour. The
machine gap is large and measured against people. On MMToM-QA's goal questions people score
88.5, GPT-4V 34.7, o3-mini-high 40.67, and AutoToM, which runs inverse planning over GPT-4o,
69.33 ([2401.08743](https://arxiv.org/abs/2401.08743);
[2502.15676](https://arxiv.org/abs/2502.15676)). Plain reasoning models infer a goal from
observed action about 50 points worse than they infer a belief (o3-mini-high 88.67 on belief,
against 97.5 for people). Literal theory-of-mind batteries are near human: GPT-4 is at or above
1,907 adults on three of five test types ([Strachan et al.,
2024](https://doi.org/10.1038/s41562-024-01882-z)). But the scores break under trivial
perturbations of the stories, a finding reproduced by several groups
([2302.08399](https://arxiv.org/abs/2302.08399);
[2412.19726](https://arxiv.org/abs/2412.19726);
[2602.10625](https://arxiv.org/abs/2602.10625)).

**Therefore.** Hold the other agent's goal as an inferred object, revised as its actions come
in, and let it change what the system does. Answering a question about the goal is not the
whole capability.

**How a technique is graded here.** The attribution must be produced from the observed
behaviour. A system told the other agent's goal, or handed a label for it, earns `incidental`.
It rests on [`priors.agentness`]: there is nothing to attribute a goal to until something has
been identified as an agent.

**Status: open (entered 2026-10-20).** No technique in the register addresses it. The inverse
planning scaffolds (AutoToM, and BIP-ALM at 73.3 on the same goal questions) are the nearest
candidates, and none has been read as a technique.
