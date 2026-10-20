---
id: modeling.commit-or-abstain
kind: capability
name: Commit or Abstain
faculty: modeling
human_source:
  - title: "Metamemory: A Theoretical Framework and New Findings (Nelson & Narens, Psychology of Learning and Motivation 26, 1990)"
    url: https://doi.org/10.1016/S0079-7421(08)60053-5
  - title: "Memory and the feeling-of-knowing experience (Hart, Journal of Educational Psychology 56, 1965)"
    url: https://doi.org/10.1037/h0022263
part_of: [modeling]
completed_by: []
status: open
provenance:
  entered: 2026-10-15
  commit: 65c4542
  frame: kaggle-sweep-2026-09
  note: >-
    candidates 2 and 3 of the twelve the Kaggle Measuring AGI hackathon write-ups suggested,
    merged; kept because a read of the maintainers' own agent records (not public) found the
    same decision failing there, so the selection is that read's, not the hackathon's
---

# Commit or Abstain

**Context.** A hypothesis is held ([`modeling.hypothesis-formation`]) and more evidence
can still be bought, at a price in actions, samples or score.

**Problem.** Holding an account is not the same as knowing whether it is good enough to act
on. The system must judge its own account against the evidence so far and choose: commit
and act on it, abstain (fall back to a safe default or say it cannot answer), or gather
more. Nelson and Narens split this into *monitoring* (how good is what I hold) and
*control* (what I do about it); Hart's feeling-of-knowing judgment is the monitoring half
measured on its own. A system can monitor well and still fail at control: in GAUGE's
three-turn protocol (answer with a confidence, then submit or abstain), Gemini 2.5 Pro
"achieved 94.1% accuracy and ECE of 0.053 ... Its L-Score was 0.0. It never abstained once
across 270 items", while Claude Haiku 4.5, at the lowest accuracy in the sample (78.2%),
"abstained on 25 of 270 items with 84% precision"
([source](https://www.kaggle.com/competitions/kaggle-measuring-agi/writeups/gauge-grading-awareness-of-uncertainty-and-ground)).
The gather-more branch fails both ways too. In LearningBench, "models requesting fewer
examples score higher (ρ = −0.52, p < 10⁻¹⁴). Probe ratios span 37%–96% across models",
and the models that "exhaust 83–96% of the budget, score 0.29–0.35"
([source](https://www.kaggle.com/competitions/kaggle-measuring-agi/writeups/learningbench)).

**Therefore.** Make the commit decision a step of the loop with its own input, a stated
confidence in the held account, and its own outputs: commit, abstain to a default the
system knows is safe, or name the observation that would settle it, which hands the step to
[`exploration.experiment-design`]. Grade the coupling between confidence and the choice,
not the confidence alone: calibration without control is the Gemini row above.

**Limits.** The hackathon numbers above are single hosted-API runs, scored by their authors,
with no human baseline (the hackathon closed 2026-04-16 and published no judging scores).
Three measures from outside it now bear on the cell:

- **A human baseline on monitoring.** Cash et al. ([Memory & Cognition
  2025](https://doi.org/10.3758/s13421-025-01755-4)) compare language models with people on the
  same prediction, Pictionary and trivia tasks: prospective confidence is about human, but
  retrospective confidence is not revised after the model's own failure. The figures behind
  this were read partly from the publisher's summary, not the paper.
- **A third-party measure of the coupling.** AA-Omniscience
  ([2511.13029](https://arxiv.org/abs/2511.13029)) scores correct minus incorrect answers on
  6,000 factual questions, so guessing costs and abstaining does not. In 2025-11 three models
  scored above zero, with a top of 4.8. It is the measure a technique entered here would be
  scored on.
- **Training that works against the cell.** AbstentionBench (20 models, 20 datasets of
  unanswerable, underspecified and false-premise questions) finds that reasoning fine-tuning
  cuts abstention by 24% on average, and that "scaling models is of little use"
  ([2506.09038](https://arxiv.org/abs/2506.09038)).

The abstention literature (selective prediction, reject options) covers one answer to one
question; it says nothing about when an agent should stop gathering evidence and act, and
under action-count scoring (ARC-AGI-3) both too early and too late cost score. The
gather-more branch still has no human-baselined measure.

**Status: open.** No technique in this register addresses it, and the machine-side work
on the gather-or-commit half is thin.
