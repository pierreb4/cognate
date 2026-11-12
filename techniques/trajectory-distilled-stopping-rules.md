---
id: technique.trajectory-distilled-stopping-rules
kind: technique
name: Trajectory-Distilled Stopping Rules (CONVOLVE)
addresses:
  - capability: modeling.commit-or-abstain
    strength: partial
    note: >-
      ABSTAIN is an action the agent can take at every step of the loop, and a playbook of
      stopping rules distilled from its own earlier rollouts moves when it takes it; `partial`
      because the step has no stated confidence as its input, so the coupling the cell grades
      does not exist to be graded, and only the abstain branch is measured — every held-out item
      is one where abstaining is right, so the commit branch has no number
requires:
  - token: llm-inference
    note: a language model for the rollouts, a reflection model and a curator model; the published runs use Llama-3 and Llama-3.3 at 8B and 70B through hosted providers
  - token: orchestration-layer
    note: >-
      a loop that runs a rollout, has a reflection model analyse it, has a curator model turn the
      reflection into structured add operations on the playbook, and appends the playbook to the
      system prompt on later episodes; fixed sections, an "other" section, an 80,000-token budget
  - token: automatic-verifier
    note: >-
      training reads the benchmark's labels: all 20 training rollouts come from the subset where
      abstaining is correct, and each rollout records whether abstention was timely against a
      benchmark-defined earliest step; the paper does not print the reflection or curator prompts
  - token: training-distribution
    note: >-
      20 rollouts for fitting and 8 for validation, from the same benchmark as the held-out
      items; no weights are fitted, what is learned is text
  - token: interaction-budget
    note: one epoch over the 20 training examples, at most two reflection/update rounds per example, up to 10 environment steps per rollout
leverage: both
cost: low
evidence:
  - claim: "timely abstention recall 26.7 -> 57.4, overall recall (AbsRec@10) 83.2 -> 100.0 and SPL 55.3 -> 78.9 for Llama-3.3-70B with a playbook distilled from its own 20 trajectories; the paper's in-context-learning arm on the same model reaches 55.4 / 97.0 / 77.2, so the playbook adds 2.0 timely-recall points over that arm, about 2 of the 101 items (Table 2)"
    kind: claimed
    split: webshop-abstention-only/held-out-101
    regime: llama-3.3-70b-hosted; 20-training-trajectories; one-epoch; no-weight-update; no-variance-reported
    source: https://arxiv.org/abs/2606.28733v3
    date: 2026-11-06
    stars: 2
    requires_beyond: [network-access]
  - claim: "the playbook carries across model size in one direction: Llama-3.3-70B with a playbook from Llama-3-8B reaches 55.3 timely recall, 99.0 overall; Llama-3-8B with its own playbook moves 6.9 -> 7.9 timely, 92.1 -> 94.1 overall, and with the 70B playbook reaches 12.9 timely, 94.1 overall (Table 2)"
    kind: claimed
    split: webshop-abstention-only/held-out-101
    regime: llama-3-8b-and-llama-3.3-70b-hosted; 20-training-trajectories; one-epoch; no-weight-update; no-variance-reported
    source: https://arxiv.org/abs/2606.28733v3
    date: 2026-11-06
    stars: 2
    requires_beyond: [network-access]
no_absolute_score: false
caveats:
  - "The row for this cell is the recall WITH the missing precision. The 101 held-out items are carved from 'the abstention-only subset of WebShop' (500 examples 'for which abstention is the correct behavior'), so no solvable item is in the set and no over-abstention number exists for the method. An agent that abstained on every task at step 2 would also score 100.0 overall here. The paper's goal is 'to preserve task completion ability' and its appendix says 'preserving normal tool-use behavior on resolvable tasks', and neither has a number behind it. The over-abstention rate the paper defines is reported only for base models (Figure 6), where it reaches 34% by turn 10 for Qwen3-235B-Instruct, so the failure is known to occur at this scale."
  - "No stated confidence, so no monitoring half. The cell separates monitoring from control and grades their coupling. The playbook acts on the control side directly: one learned guideline does say to 'calculate the request's fulfillability score', but no score is emitted, read or checked. Nor does the method name the observation that would settle the question; the third branch, gather more, is only ever ended, never directed."
  - "In-context learning gets nearly all of it. Timely recall 57.4 (playbook) against 55.4 (in-context learning) is two items of 101 in one run; the paper says 'modest additional gains'. v3 does not say what that arm is given (the table caption says 'Trained variants use 20 trajectories', and the arm appears nowhere else but one comparison sentence). So whether the rules add anything beyond an example-based arm is not shown. The 8B model's in-context row lowers overall recall by 11.0 points (92.1 -> 81.1)."
  - "The training examples carry the answer. All 20 are cases where abstaining was right, and the rollout record says whether abstention was timely. What the system produces is a rule about when; that abstaining is the correct outcome on these tasks is supplied."
  - "Timely is benchmark-defined. AbsRec@1 for request-based items, AbsRec@2 for environment-based ones, and the authors say the metric 'may penalize agents that reasonably continue gathering information before abstaining', which is the cell's own gather-more decision. 13 of Table 2's 15 recalls fit k/101 (26.7 = 27, 57.4 = 58, 100.0 = 101; 55.3 and 81.1 do not, 56/101 being 55.4 and 82/101 being 81.2), so it is very likely the 101-item set, which the text implies without saying; the arithmetic is this entry's, not the paper's. One run: no seeds, intervals or significance test. The split is grouped by original WebShop goal, within one domain."
  - "No cross-domain row. v1 had an appendix evaluating on AbstentionBench and TerminalBench (its Table 3, https://arxiv.org/abs/2606.28733v1); v3 (2026-11-06) has no such section or table, and gives no reason, so neither is entered. v3 also changes the in-context-learning row (70B timely 55.1 in v1, 55.4 in v3) and the 8B + 70B overall gain. The arXiv record gives no venue; the authors' repository states NeurIPS 2026 acceptance (https://github.com/lhannnn/agentic-abstention)."
  - "Unpriced estimate: 20 rollouts of up to 10 steps and at most 40 reflection/update rounds is the whole fitting cost, and at run time the playbook is prompt text. `cost: low` rests on that; no row prices it."
provenance:
  entered: 2026-11-09
  frame: repo-watch-2026-11
  note: >-
    a maintainer's watch of new GitHub repositories and arXiv papers; two rows read by hand on
    2026-11-07 against two cells the gap report listed EMPTY, so it could surface only what
    those cells already ask about
---

# Trajectory-Distilled Stopping Rules (CONVOLVE)

**What it is.** An LLM agent does a task over several turns and may at any turn take the action
ABSTAIN. CONVOLVE runs it on 20 tasks where abstaining is the right outcome, has a reflection
model read each rollout for "whether the agent continued acting after the task had become
infeasible, which observations made abstention warranted, and which actions delayed abstention",
and has a curator model turn that into short rules in a structured playbook. The playbook is
appended to the system prompt, with the tools and task text unchanged. No model weight moves.

**The cognate.** The person who has searched long enough to know that this shop does not stock
the thing, and leaves. The failure it treats is the one the benchmark in the same paper
measures: agents usually get there, but late; "Agents usually abstain too late or not at all".

**Why `partial`.** The decision is a real step of the loop and what changes it is produced from
the system's own failures. The cell asks for more than that. It wants a stated confidence as the
step's input and a grade on how the choice follows it, and here nothing is stated; and it wants
commit and abstain both tested, and here only abstain is. The set the numbers come from cannot
tell a system that knows when to stop from one that has learned to stop.

**The limit.** Run the same 101 items with a mix of solvable tasks and the over-abstention rate
would say which of those it is. The paper defines that rate and reports it for base models, not
for the method. Until someone measures it, read the 57.4 as a gain in timing on tasks already
known to be infeasible.
