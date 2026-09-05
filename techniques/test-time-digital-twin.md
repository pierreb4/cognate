---
id: technique.test-time-digital-twin
kind: technique
name: Test-Time Digital Twin (Twin)
addresses:
  - capability: goal-setting.goal-inference
    strength: partial
    note: >-
      the objective is an explicit executable artifact, `goal_reached(grid) -> bool`, written
      by the agent BEFORE the level's first completion signal from a ranked reachable state,
      planned against, and retired when the predicted state is reached without a level
      boundary — nameable, actable, replaceable; `partial` and not `direct` under the
      distance rule because two things are handed over: the terminal level-completion flag
      that confirms or refutes each hypothesis, and five authored visual-change heuristics
      that rank which reachable states are worth proposing as goals — see caveats
requires:
  - token: llm-inference
    note: a frontier code model driving a coding agent (GPT-5.6 Sol through OpenAI Codex)
  - token: network-access
    note: the model is a hosted service reached during play; web search is disabled but the model call is not local
  - token: orchestration-layer
    note: >-
      a harness holding the full transition log across agent restarts and enforcing two hard
      constraints — no scored action until the twin replays every logged transition, no goal
      test until the predicate rejects every logged frame
  - token: value-signal
    note: >-
      the environment's terminal level-completion flag, and nothing denser — the sparse signal
      strictly UPSTREAM of the nameable objective the system produces; the distance-rule token
      for this cell
  - token: novelty-estimator
    note: >-
      five fixed visual-change heuristics (color_gone, color_new, local_burst, big_change, and a
      most-different-state frontier fallback) rank reachable states as goal candidates; the
      paper calls the branch "Go-Explore-style novelty search" — an authored prior over what a
      goal looks like, generic across games but supplied, not acquired
  - token: deterministic-environment
    note: replay validation is a hard precondition for action and "assumes deterministic dynamics representable by the twin"
  - token: per-task-compute
    note: about 224k processed tokens per scored action; 2.60B tokens and 91.4 h of inference across the 25 games
  - token: interaction-budget
    demand: 0.61
    unit: actions-per-human-baseline-action
    measured_on: arc-agi-3/public-25-games
    source: https://arxiv.org/abs/2608.14490v1
    note: >-
      mean ratio of agent to first-time-human action counts over the 23 games Twin fully
      clears (Figure 3); the two uncleared games (sp80, sc25) are not in the ratio
leverage: both
cost: high
evidence:
  - claim: "the first committed goal hypothesis is correct BEFORE that level's first completion signal on 156 of 179 cleared levels (87.2%); graded per scored action instead, the predicate's claims reach recall 138/179 = 0.771 at precision 138/646 = 0.214 (Table 11: 138 right claims, 508 wrong claims, 41 missed wins, 10,870 correctly quiet)"
    kind: claimed
    split: arc-agi-3/public-25-games
    regime: gpt-5.6-sol-via-codex; 2.60B-processed-tokens-and-91.4h-over-25-runs; one-run-per-game
    source: https://arxiv.org/abs/2608.14490v1
    date: 2026-08-14
    stars: 2
  - claim: "93.3 action-efficiency score, 23 of 25 games and 179 of 183 levels cleared, against the same base model in off-the-shelf Codex with the validate-explore-plan loop removed at 61.1 (13 games, 148 levels), Prime Agent 78.3 on the same base model, OPINE-World 78.4 (Claude Opus 4.8), EWM 63.8 (GPT-5.5), and direct play 7.8"
    kind: claimed
    split: arc-agi-3/public-25-games
    regime: gpt-5.6-sol-via-codex; 2.60B-processed-tokens-and-91.4h-over-25-runs; one-run-per-game
    source: https://arxiv.org/abs/2608.14490v1
    date: 2026-08-14
    stars: 2
no_absolute_score: false
caveats:
  - "The row for this cell is the 87.2% / 0.214 PAIR, not either number alone. Per level, the first committed goal is right on 156 of 179; per scored action, 508 of 646 goal claims are wrong and the authors say so: 'Most wins are claimed, and most claims are wrong' and 'the twins learn how the world moves more reliably than they learn what winning in it means' (Appendix J). A reader who carries only 87.2 has read the headline."
  - "'Before any reward' is per LEVEL, not per game. Twin, log and agent context persist across a game's levels and 'a level boundary ... becomes the first reward example', so from level 2 onward the predicate is proposed with earlier boundaries as positive examples. The 179 verdicts are not 179 cold inferences; the paper does not stratify the 87.2% by level index."
  - "Two supplied things cap the grade. (1) The terminal level-completion flag is the only positive supervision the objective ever gets — a sparse scalar strictly upstream of the nameable predicate, which is the distance rule's `partial` case, carried as `value-signal`. (2) Candidate goal states are ranked by five authored visual-change heuristics; the paper says they 'do not encode game-specific objects, actions, or goals', and that is true, but they are a designer's prior over what a goal looks like and the coding agent infers a predicate FROM the state they select. Neither is the objective itself, so neither is the supplied/acquired test's `incidental`; both are handed."
  - "Public 25-game set only, one scored run per game, no semi-private or hidden-eval number. The contamination guard covers the base model (Feb 2026 cutoff against a March 2026 game release), web access and deny-listed sources; it cannot cover harness design, which was done with the 25 public games available. The comparison systems were run on different base models except the Codex ablation and Prime Agent ('the Codex ablation and Prime Agent's Sol configuration are the only entries sharing Twin's base model'), so only the 93.3 vs 61.1 vs 78.3 triple is model-matched."
  - "The human row is the score's normalization, 'not a measured system'. The 0.61x action ratio is over the 23 cleared games; two games (sp80 at 92.3% dynamics accuracy, 'goal-limited'; sc25 with 'costly timer-driven tests') are unfinished and the authors name them as 'accurate dynamics, unresolved goals' — the cell's own failure mode, not a dynamics failure."
  - "Scope limits stated by the authors: deterministic dynamics, one-frame state ('mechanics driven by long temporal context ... are beyond this scope'), small discrete grids where cell equality is decidable, fixed search budgets (depth 14 / 30,000 nodes for goal discovery) so 'a goal beyond the horizon goes unfound'. The hosted model exposes no seed, so token sequences are not reproducible; the audit trail (hash-committed prediction before every action, all 25 runs replayable at the project site) is what stands in for it."
  - "Edges OWED, not declared. The twin is an executable program replayed against the log, which is `direct` on `modeling.hypothesis-formation` by that cell's exhibitable-commitment rule, but declaring it means typing the pair against eight techniques already at direct/partial there; `modeling.belief-update` (counterexample-guided repair) and `exploration.experiment-design` (the 'live wall' picks what the next action should teach, but by one held hypothesis, not by information gain over a set) have no written strength ladder to grade against. This node enters for the cell it was examined against."
interacts: []
provenance:
  entered: 2026-09-05
  commit: pending
  frame: hand-search-run-11-gate
  note: >-
    found by a hand literature search against the pre-committed Run 11 gate (stance c,
    LLM and program-induction agents in unfamiliar games), not by launching the run; the
    gate's satisfiability clause — objective to the scorer, never to the system — is what the
    paper's 'completion signal only after winning' interface satisfies
---

# Test-Time Digital Twin (Twin)

**What it is.** A coding agent writes the unknown game as a Python program at test time —
`step(grid, action) -> grid` and `goal_reached(grid) -> bool` — starting from an identity
stub, and a harness refuses every scored action until the program replays the whole
interaction log. Dynamics get a label from every action. The goal gets a positive label only
when the environment reports a completed level, so at the start of a game the predicate
rejects every state and the planner has no target. Twin's move is to manufacture one: search
the validated twin for reachable states that look like progress, have the agent write a
tentative `goal_reached` describing the top candidate's salient change, filter it against
every logged frame (all certified non-goals, because the engine replaces the winning frame),
then spend real actions on the cheapest route to it. A level boundary confirms the
hypothesis; arriving without one retires it for good.

**The cognate.** The person shown a novel game screen who forms a candidate objective within
seconds and starts acting on it. The objective here has exactly the standing the cell asks
for: it is a named artifact something downstream acts on, and it is found wrong and replaced
by the ordinary course of play. The paper names the asymmetry the cell is built on — "the
dynamics can be verified against every interaction, whereas goal reachability must be
established through exploration" — and reports that the first committed goal is right on
87.2% of cleared levels.

**Why `partial`.** Two things are handed over, and neither is the objective. The terminal
completion flag is the sparse signal the distance rule caps on: the system does the producing
step from "a level ended here" to "winning is X", and that is the whole reason this node can
exist where a reward *function* could not. The five visual-change heuristics are the second:
a designer's prior over what goals look like, generic but supplied. And the measurement the
authors themselves put last is the one to carry: at the action grain the predicate's
precision is 0.214. Most wins are claimed; most claims are wrong.

**The limit.** The unfinished games are the cell's own failure mode — "accurate dynamics,
unresolved goals" — and the number is on the public set, one run per game, under a harness
built with those games in view. Whether the propose-and-test loop transfers off a 64x64
deterministic grid where cell equality is free is untested; the authors say so.
