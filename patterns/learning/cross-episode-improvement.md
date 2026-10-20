---
id: learning.cross-episode-improvement
kind: capability
name: Cross-Episode Improvement
faculty: learning
human_source:
  - title: "ARC Prize, ARC-AGI-3 human dataset (2026-04-14): 458 first-time players, every environment beaten by at least two"
    url: https://arcprize.org/blog/arc-agi-3-human-dataset
part_of: [learning]
completed_by: []
status: open
provenance:
  entered: 2026-10-20
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Cross-Episode Improvement

**Context.** A deployed system meets the same environment, or the same user, across several
episodes or sessions.

**Problem.** People get better at a game by playing it and keep what they learned; on
ARC-AGI-3 every environment was beaten by at least two of about ten first-time players. In
May 2026 ARC Prize's replay audit named the machine failure "solved the level, didn't learn
the game" ([source](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)). Four
months later GPT-6 Astra reached 99.9% once a Provider Adapter carried the provider's
reasoning state between requests, against 62.7% under the Standard harness, which carries only
the notes the model chooses to keep ([source](https://arcprize.org/blog/astra)): what was kept
between steps decided the score. On LoCoMo's long multi-session conversations, people score
87.9 F1 and the best system 41.4 ([2402.17753](https://arxiv.org/abs/2402.17753), 2024).
SEAL, which writes its own fine-tuning data, acquires new knowledge and still forgets earlier
updates ([2506.10943](https://arxiv.org/abs/2506.10943)).

**Therefore.** Over episodes or sessions in deployment, improve from the system's own
experience and keep the gain.

**How a technique is graded here.** On the gain carried from one episode to a later one, with
the experience coming from the system's own play. Within one episode the capability is
[`modeling.per-task-adaptation`], not this.

**Status: open (entered 2026-10-20).** No technique in the register addresses it. The
candidates are self-editing fine-tuning (SEAL) and the ARC-AGI-3 harnesses that carry state
between steps; the harnesses publish no mechanism, so none can be graded.
