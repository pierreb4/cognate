---
id: technique.theory-based-rl
kind: technique
name: Theory-Based Reinforcement Learning (EMPA)
addresses:
  - capability: goal-setting.goal-inference
    strength: partial
    note: >-
      the objective is a termination rule `WIN|LOSE IF count(c)==0` held as "a superset of
      possible explanations, which the planner tries to simultaneously satisfy", inferred per
      game from the observed Win/Loss/Continue status by an indicator likelihood, set as the
      planner's goal, differentiated into subgoal and goal-gradient rewards, and refuted when a
      class count reaches zero without a terminal — nameable, actable, replaceable; `partial`
      and not `direct` under the distance rule because two things are handed over: the
      terminal status channel, and a one-production goal grammar that IS the hypothesis space
      of objectives — see caveats
requires:
  - token: expert-authored-library
    note: >-
      the VGDL ontology the models are written in — sprite dynamic types, 14 interaction
      types, the identity and type of the avatar, its projectile and the walls — all
      supplied; the authors say the last three "could be learned ... at the cost of expanding
      the hypothesis space"
  - token: state-representation
    note: >-
      a symbolic, fully observed state — "objects and their locations as well as interactions
      that occur between objects", with the nature of each collision event given
  - token: value-signal
    note: >-
      the environment's Win/Loss/Continue status, observed every step and informative only at
      steps where some class count is zero — the sparse signal strictly UPSTREAM of the
      objective the system produces; the distance-rule token for this cell, shared with
      `test-time-digital-twin`
  - token: goal-grammar
    note: >-
      one authored production over class names, `{WIN|LOSE} IF count(c)==0`, is the whole
      hypothesis space of objectives: "We restrict our scope to games that are won or lost
      when counts of particular objects on the screen reach zero" — a family, not the answer,
      so a cap and not the supplied/acquired test's `incidental`
  - token: deterministic-environment
    note: >-
      interaction outcomes are deterministic and uniform by class — the interaction rules are
      kept as a single MAP hypothesis "because the interactions are deterministic"; object
      motion may be random and is modelled as a dynamic type
  - token: per-task-compute
    note: >-
      up to 1M agent steps and "a total time budget of 24 hours for playing each game";
      long-term planning budget of 1,000 imagined states, doubling on failure
  - token: solution-in-span
    note: >-
      the game's true win and loss conditions must be count-to-zero rules over the given
      classes; true by construction on the authors' own 90 games, an assumption anywhere else
leverage: knowledge
cost: high
evidence:
  - claim: "learning efficiency within 0.1x-10x of the mean human on 79 of 90 games, better on roughly two-thirds and worse on roughly a third (Figure 3); no number in the paper isolates termination-rule identification from dynamics learning, exploration or planning"
    kind: claimed
    split: empa-vgdl-90
    regime: 10-seeds-per-game; up-to-1M-agent-steps; 24h-cpu-per-game; symbolic-object-input; color-only
    source: https://doi.org/10.1098/rsta.2024.0529
    date: 2026-05-14
    stars: 1
  - claim: "DDQN more than 100x less efficient than humans on 67 of 90 games, more than 1,000x on 45, more than 10,000x on 22, and Rainbow no better on average; Bait all five levels in fewer than 1,000 steps, Zelda within 500, Zelda 1 within 2,000"
    kind: claimed
    split: empa-vgdl-90
    regime: 10-seeds-per-game; up-to-1M-agent-steps; 24h-cpu-per-game; symbolic-object-input; color-only
    source: https://doi.org/10.1098/rsta.2024.0529
    date: 2026-05-14
    stars: 2
no_absolute_score: false
caveats:
  - "There is NO number for this cell. The ablations remove exploration, subgoals, goal gradients and IW pruning, never the termination learner, so goal identification cannot be separated from dynamics learning even by subtraction; the efficiency ratio folds all four together. The only goal-identification evidence is qualitative (Extended Data Figure 1E of the preprint: 'now touching the door wins the level'). A reader carrying 79/90 has read the headline of a different capability."
  - "Two supplied things cap the grade, and the second is heavier than Twin's. (1) The Win/Loss/Continue status, observed every step: 'the only states that are informative about termination rules for any hypothesis are ones where count(cj)==0 for some class cj' — sparse, terminal, upstream; `value-signal`. (2) The goal grammar is ONE production, and the games were written to fit it: 'We restrict our scope to games that are won or lost when counts of particular objects on the screen reach zero.' Twin's heuristics rank candidate states for a free-form predicate; EMPA's template is the space of predicates. Same clause of the distance rule, less distance."
  - "Own-lab suite, all 90 games in view during design, no held-out. 27 base games — 17 GVGAI, '10 in a similar style that we designed with particular learning challenges in mind' — times 1-4 author-made variants. The journal version says the human data and game videos are 'available for download' at github.com/tsividis/Theory-based-RL; the repository's README as read on 2026-09-05 lists four simplified two-level demo games and no versioned 90-game set. The suite is playable in a browser (pedrotsividis.com/vgdl-games) without source. `solution-in-span` by construction."
  - "The human row is not a cold goal-inference baseline. Participants were told 'each game had several levels, and that they needed to complete a level in order to go to the next level' — the objective's shape, handed. They played in real time (the game stepped without a keypress) against a turn-based model with a no-op; the metric is agent steps. Color-only mode with randomized colours is the strongest part of the protocol: no semantic priming for either party."
  - "Determinism, full observability, handed identities. 'we assume that the state-space is fully observed'; interactions kept as one MAP rule 'because the interactions are deterministic'; the avatar, its type, its projectile and the walls are given. The Loss half of the objective (avatar count to zero) is written over a given identity. The Discussion names 'causal determinism and uniformity' as the assumptions that buy the speed."
  - "Two primaries. The rows cite the journal version (Phil. Trans. R. Soc. A 384:20240529, 2026-05-14, CC-BY, changed title), whose main text was read and carries the same 79/90, 0.1-10x and DDQN numbers as the preprint; the mechanism quotations above are from the preprint's Methods (arXiv 2107.12544v1, 2021-07-27), which the journal's electronic supplement was not read to re-verify. The journal adds Rainbow as a baseline and a section on five Atari games (Breakout, Carnival, Freeway, Pong, Space Invaders) where the objective is score, not a termination rule — outside this cell — and where the authors report the theory's predictions drifting to 'a mean error as high as 40 pixels per moving object after just 10 action steps on Pong'."
  - "Unresolved from the primary: whether an UNCONFIRMED Win rule in the 'superset' enters the goal reward (RG is 'effectively ∞ for Win states'), i.e. whether the planner will drive a class to zero as a hypothesized win before either polarity has been observed. One SI game, Survive Zombies ('survive for 500 game steps'), is not obviously a count-to-zero rule and the paper does not say how it is expressed."
  - "Edges OWED, not declared. The VGDL model is a printable program scored by likelihood — `modeling.hypothesis-formation` by the exhibitable-commitment rule, undeclarable until typed against the nine techniques at direct/partial there; contact goals for every unobserved class pair are an EIG proxy that overlaps `technique.oomdp-identification` on `exploration.experiment-design`; subgoals and goal gradients derived from the termination rule are `planning-execution.goal-decomposition`. This node enters for the cell it was examined against, as Twin did."
interacts: []
provenance:
  entered: 2026-09-05
  commit: b163844
  frame: hand-search-run-11-gate
  note: >-
    listed as 'a second (B) candidate, not a refusal' in the goal-inference node's hand search
    against the Run 11 gate; entered after its own reading of the preprint and the 2026
    journal version
---

# Theory-Based Reinforcement Learning (EMPA)

**What it is.** A Bayesian learner holds the unknown game as a VGDL program — sprite
dynamics, pairwise interaction rules, and a termination set — and scores candidates by whether
they reproduce every observed frame, including the frame's Win/Loss/Continue status. The
termination set is where this register looks: rules of the form `WIN IF count(c)==0`, kept as
"a superset of possible explanations, which the planner tries to simultaneously satisfy".
Nothing in that superset is refuted until some class count actually reaches zero, so the
exploration module makes reaching zero an epistemic goal in its own right, and the planner
turns whichever rules survive into a goal, a subgoal reward on the class count, and a spatial
gradient toward whatever the model says can destroy that class. A count hitting zero without
a terminal kills the rule; a Win confirms it.

**The cognate.** The person at a novel screen who guesses "I am probably meant to clear
those" and starts clearing them, ready to be wrong. The objective has the standing the cell
asks for — printable, planned against, refuted by play — and the paper shows the signature of
a live hypothesis rather than a lookup: EMPA "doesn't know that games almost always have
exactly one win condition, so after finding one way to win a game it may continue to explore
new ways of winning". The paper itself frames the termination set as "the agent's ultimate
goals".

**Why `partial`.** Two things are handed over and neither is the objective. The status
channel is the sparse terminal signal the distance rule caps on, exactly as for Twin. The
second is heavier than Twin's: not a ranking prior over candidate states but the hypothesis
space of objectives itself, one authored production over class names, and a suite written to
fit it — "We restrict our scope to games that are won or lost when counts of particular
objects on the screen reach zero." The system still performs the producing step, which class
and which polarity, and that keeps it off `incidental`; the size of the step is what keeps it
well short of `direct`.

**The limit.** There is no number for the cell. The headline — human-order learning
efficiency on 79 of 90 games — folds dynamics learning, exploration, planning and goal
identification into one ratio, and no ablation removes or oracles the termination learner.
The suite is the authors' own, was in view throughout design, and is not released as a fixed
versioned set; the human row was told the shape of the objective. What EMPA demonstrates for
this cell is the mechanism, and the mechanism is honest about what it consumes; what it does
not demonstrate is how much of the 79 the objective-finding step earned.
