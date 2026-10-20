---
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
bears_on:
  - modeling.per-task-adaptation
  - modeling.hypothesis-formation
  - hypothesis.bitter-lesson
predicts:
  - claim: >-
      the next ARC generation has a verified general-model score at or above its own declared
      human baseline within 6 months of launch, under the harness ARC Prize labels Standard
    check: >-
      arcprize.org results pages; launch date against the first verified at-or-above score.
      Parity reached only through a non-Standard harness is recorded as a partial result,
      not a pass
provenance:
  entered: 2026-10-20
  commit: 6ee3761
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Time to Human Parity Shrinks per Benchmark Generation

**The claim.** Each ARC generation was built to reopen a large gap between people and
machines, and each lost it faster than the last: ARC-AGI-1 from its 2019-11 release to 2024-12,
ARC-AGI-2 from 2025-03-24 to between 2025-12 and 2026-02, ARC-AGI-3 from 2026-03-25 to
GPT-6 Astra's 99.9% on 2026-09-03.

**Why it is held as a hypothesis and not as a reading.** Three numbers are a pattern, not a
rate, and each rests on a choice the register now asks rows to state. "Parity" depends on which
human figure is meant: the ARC-AGI-2 date is 2025-12 against a per-person average of about 53%
on the semi-private set, which is a secondary estimate, and 2026-02 against the 66% of
attempted test pairs the calibration testers solved (arXiv 2505.11831). The human figures are
not one aggregation either: an individual's average, a panel's union, the median player who
completed a level. That is the problem `human_baseline:` names (`SCHEMA.md`). And ARC-AGI-3's
parity holds only with the Provider Adapter, which carries the provider's reasoning state
between requests; under ARC Prize's Standard harness the same model scores 62.7%.

**What would refute it.** The next ARC generation going more than six months without a
verified general model at or above its declared human baseline under the Standard harness.
Parity reached only through another harness counts as partial, so a fourth number that
shrinks only by changing the harness does not support the claim.

**Where it stops.** It is about one benchmark family whose makers re-test people each
generation. It says nothing about capabilities no ARC generation measures, and the survey
that proposed it found the gaps that stay open mostly outside ARC.
