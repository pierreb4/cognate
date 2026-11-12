---
id: technique.optional-world-model-tooling
kind: technique
name: Optional World-Model Tooling (the seal)
addresses:
  - capability: modeling.hypothesis-formation
    strength: partial
    note: >-
      when the agent writes `world_model.py` and its replay test passes, the account is an
      executable program (`initial_state`, `do_move`, `render`) that the harness steps against
      every executed move and that stops the batch at the first misprediction, so the
      commitment is exhibited, not merely exhibitable; `partial` because writing it is the
      agent's option: with no passing model the batch runs unchecked and there is no account to
      name, so the cell's "at any moment" holds only part of the time, and the rows measure
      score, not whether the account is right
requires:
  - token: llm-inference
    note: >-
      a code-writing language model; the published runs serve an expert-pruned, distilled
      Qwen3.8-Flash-Next locally, which is a property of the RESULT, not the mechanism — see
      `requires_beyond` on the evidence rows
  - token: orchestration-layer
    note: >-
      a harness with one persistent Python kernel per level and files that survive levels; it
      tests the model silently on a call's first move, checks every executed move against it
      once it passes, stops a batch at a mismatch (`WorldModelStop`) or after a move the model
      declines (`Unknown`), and says in the next prompt whether the actions ran checked
  - token: search-procedure
    note: >-
      after a call whose last test passed and which played no moves, a breadth-first search
      over the model (130 s and 2 GiB) whose targets are a win or a boundary: a move the model
      answers with `Unknown`, one whose code raises, or a click state that does not render
  - token: deterministic-environment
    note: >-
      the test replays the level's history from `initial_state()` and compares every frame, so
      a model is only checkable where the same moves give the same frames; −1 wildcards, loose
      energy and a pixel tolerance are the stated outs
  - token: per-task-compute
    note: >-
      the submitted run's budget is the tokens one RTX PRO 6000 generates in 9 hours over 110
      games; the search runs outside a call's time limit, at most 12 at once on the machine
leverage: both
cost: low
evidence:
  - claim: "offered as an option (the submitted level), the world model scores 2.7 ± 2.1 points above the same agent offered none (no prompt section, no test, no search), 3.5 ± 2.0 above a mandatory one (a passing test required before any sequence of actions, a few single moves per level until then) and 4.2 ± 2.0 above none with the file tools removed too; 95% intervals from one OLS fit with HC3 errors over 108 runs that draw seven settings at once, read at 8:40 of a simulated 9-hour run; the three alternatives cannot be told apart (mandatory against none −0.8 ± 2.4)"
    kind: claimed
    split: arc-agi-3/public-21-of-25-plus-11-own-games-weighted
    regime: kaggle-2026-single-rtx-6000-9h-clock-simulated-on-b200-qwen-3.8-flash-next-nvfp4-joint205-u800; 108-runs; one-play-per-game
    source: https://tufalabs.github.io/arc-writeups/supplementary/arc3_ablations/arc3_ablations.html
    date: 2026-11-09
    stars: 2
    requires_beyond: [trained-model, weight-gradients]
  - claim: "the option pays late and acts less: runs offered no world model lead for the first hours, by up to 2.7 points about two hours in; the optional level passes none at about 6 simulated hours and leads it by 3.8 at 10 hours; a mandatory model trails optional by about 7 points at three hours and 2.4 at ten; over a run, agents without a world model take about 41,000 and 45,000 actions against 23,000 optional and 16,000 mandatory"
    kind: claimed
    split: arc-agi-3/public-21-of-25-plus-11-own-games-weighted
    regime: kaggle-2026-single-rtx-6000-9h-clock-simulated-on-b200-qwen-3.8-flash-next-nvfp4-joint205-u800; 108-runs; one-play-per-game
    source: https://tufalabs.github.io/arc-writeups/supplementary/arc3_ablations/arc3_ablations.html
    date: 2026-11-09
    stars: 2
    requires_beyond: [trained-model, weight-gradients]
no_absolute_score: false
caveats:
  - "Not a leaderboard figure. The sweep plays 21 of the 25 public ARC-AGI-3 games (ar25, ft09, lp85 and m0r0 left out as scoring near 100 whatever the settings) and 11 of the authors' own re-arc-3 games, scored against optimal solves at three times their baseline actions (ball_bounce at nine). Game weights were fitted so that an earlier version of the agent reads its two leaderboard scores; the authors: 'every game is public or our own, so it is not a leaderboard score. The differences between settings are what this note reports.' The same page puts the configuration with every setting submitted at 67.5 ± 2.3, and the one run that drew all seven submitted levels scored 62.0."
  - "The sign depends on when the run is read. The clock is a model of the Kaggle machine, fitted on an earlier agent before the submitted throughput stack and drafter and not refitted; the authors: the world model's differences 'change sign about three to four hours before the read', and 'At 4:40, where a 5-hour limit would be read, the three are within about a point of each other.' Read the first row as a 9-hour result on a modelled clock; under a 5-hour budget the same sweep shows no difference."
  - "The option is a bundle. The `none` arm removes the prompt section, the test and the search together, and the optional arm also seeds `world_model.py` with a working model of a different, simpler game so the contract is in view. So the rows do not separate holding an account from the breadth-first search that uses it, nor from the example file. 'No world model' means not offered, not impossible: in 12 of those levels' 1,728 games the agent called the test anyway. The table reads main effects averaged over the other six settings; adding every pairwise interaction does not improve the fit significantly (33 terms, p = 0.08), and the strongest pair is the world model with the board image (p = 0.024, not surviving correction for 21 pairs)."
  - "Optional against mandatory is the finding that separates this node from `technique.test-time-digital-twin`, which refuses every scored action until its program replays the whole log. Tufa's mandatory arm is not the twin (it allows a few single moves per level before a pass, on another model and harness), and the twin's 93.3 is on the public 25-game split with GPT-5.6 Sol, so nothing here ranks the two. The pair is typed `overlaps` on hypothesis-formation, the conservative edge; a harness cannot hold both policies at once, but a combination can hold either kind of account."
  - "Source standing. The supplementary pages say of themselves 'This material was written by AI agents and human reviewed'; the sweep code (`jeroen-arc3-experiments`) is not released and is 'available from Tufa Labs on request'; one play per game per run, the fit explaining 33% of the variance between runs. A null parameter drawn beside the seven comes out at p = 0.74, and batch terms are jointly insignificant (p = 0.55). The agent itself is released, MIT-0: `arc3/packages/seal` in https://github.com/Tufalabs/arc-prize-2026 (the world model in `model.py` and `py_model.py`, the search in `search.py` and `planner.py`), specified in https://tufalabs.github.io/arc-writeups/supplementary/harness_arc3/harness_arc3.html."
  - "The entry's score is not this node's. The selected submission, version 1 of the same agent, scored 70.24 on the ARC-AGI-3 Kaggle public board (submission 57853115), and version 3 scored 70.92 and 67.56 in two runs after the code deadline (arc3_ablations, Caveats): two runs of one configuration 3.36 apart. The authors credit their largest gains elsewhere: 'Our largest practical performance improvements came from adopting newer, more capable open-source models, rather than from our additional harness- or environment-specific post-training' (https://tufalabs.github.io/arc-writeups/supplementary/rl_training/rl_training.html). An entry row belongs with the Duck-lineage rows on `technique.refinement-harness`, and is not entered here."
  - "Edges still OWED, not declared. `modeling.commit-or-abstain`: `Unknown(reason)` declines a claim about a move never observed, and a batch stops after it, but the declined move is still played, and the step-back audit after 300,000 tokens without a clear has no measurable effect (−0.1 ± 1.6, about 27 audits in a 32-game run). `exploration.experiment-design`: the search targets an `Unknown` boundary as well as a win, so it seeks the edge of the model, with no ablation of its own. `learning.sample-efficiency`: the action counts in the second row, with no human ratio. Each would change a gap-report line and its cell's Status, so none is entered with this node."
  - "Unpriced estimate: one RTX PRO 6000 for 9 hours over 110 games is the competition's own budget, a few GPU-minutes a game; `cost: low` rests on that, and no row prices it in dollars."
interacts:
  - technique: technique.solver-trace-distillation
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both check a named candidate against the evidence before acting on it; the seal's account
      is a program the agent writes at test time when it chooses to, the distilled trace's is
      drawn from a candidate space installed at training — both `partial`, for different caps
  - technique: technique.test-time-digital-twin
    rel: overlaps
    scope: modeling.hypothesis-formation
    note: >-
      both hold the game's dynamics as Python the next frame can refute; the twin makes the
      program compulsory before any scored action, the seal leaves it to the agent and
      measures that compulsion costing points (mandatory −3.5 ± 2.0 against optional), which is
      why one is `direct` and the other `partial`
provenance:
  entered: 2026-11-12
  commit: e06a285
  frame: competition-release-watch-2026-11
  note: >-
    a maintainer's watch of repositories made public by ARC Prize 2026 teams; the second-placed
    ARC-AGI-3 team's code and supplementary pages, read by hand on 2026-11-10 against this
    register's cells, so it surfaces what a top entry chose to publish and the cells already
    asked about
---

# Optional World-Model Tooling (the seal)

**What it is.** An agent plays an unknown game from a Python kernel, and may, if it wants,
write the game's rules as a program in `world_model.py`: an initial state, a move function
that raises `Unknown` for any move whose effect it has never seen, and a renderer whose −1
cells match anything. The harness replays the level's history through the program on the
first move of every call. Once it passes, every real move is checked against it and a batch
stops at the first misprediction; a call that plays no moves gets a breadth-first search over
the program, aimed at a win or at the nearest move the program cannot answer. Without a
passing program the agent plays unchecked, and the prompt tells it which it was.

**The cognate.** The player who plays most games by feel and reaches for pencil and paper only
when one resists: the rules get written down when writing them down pays, and then they are
held to every move. Tufa's own sweep is the case for the option. Offered the tool, the agent
plays fewer actions and ends higher; made to use it, the agent starts slowest and never
catches up within the run.

**Why `partial`.** When the program exists it is as exhibited as a commitment gets: a single
executable account, checked on every move, whose failure stops play. But the cell asks for a
commitment at any moment, and here there is one only while the agent has chosen to keep a
passing model. The rows are score differences between harness settings; none says how often
the model was written, or how often it was right.

**The limit.** The difference is on the authors' simulated clock, over public and self-made
games, and it changes sign hours before the read: under a 5-hour budget the three settings
are within a point. And the option comes bundled with the search that uses it, so whether
the account or the search over it carries the 2.7 points is not separated.
