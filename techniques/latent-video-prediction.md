---
id: technique.latent-video-prediction
kind: technique
name: Latent Video Prediction (V-JEPA)
addresses:
  - capability: priors.basic-physics
    strength: partial
    note: >-
      dynamics are inferred from observed motion, with no physics engine and no authored
      object vocabulary, and read off as surprise when a video violates them — the cell's
      `direct` criterion, acquired rather than handed over; `partial` because it holds only in
      simple scenes (IntPhys 98%) and is near chance in realistic ones (IntPhys 2, 57.51 against
      96.44 for people), and because the model is not action-conditioned, so nothing in it
      separates what the environment does from what an action did
requires:
  - token: trained-model
    note: a video encoder and predictor pretrained by prediction in latent space before deployment
  - token: training-distribution
    note: >-
      a large unlabelled corpus of natural video (HowTo100M, Kinetics-710 and SSv2 in the rows
      below); 128 hours of unique video suffice on simple scenes
leverage: computation
cost: low
evidence:
  - claim: "V-JEPA: 98% pairwise accuracy (95% CI 95-99) on IntPhys, zero-shot from the surprise of its latent prediction, with no physics engine and no object vocabulary"
    kind: claimed
    split: intphys-2018/dev
    regime: zero-shot-surprise-pretrained-on-howto100m-k710-ssv2
    source: https://arxiv.org/abs/2502.11831
    stars: 2
    date: 2025-02-17
  - claim: "trained on 128 h of unique video (0.1% of HowTo100M), V-JEPA keeps pairwise accuracy above 70% on every IntPhys property"
    kind: claimed
    split: intphys-2018/dev
    regime: zero-shot-surprise-pretrained-on-128h-unique-video
    source: https://arxiv.org/abs/2502.11831
    stars: 2
    date: 2025-02-17
  - claim: "V-JEPA 2-h 57.51 on IntPhys 2 Main against 96.44 for human annotators; the best multimodal LLM, Gemini 2.5 Flash, 55.63 and GPT-4o 53.75 — every model near chance in realistic scenes"
    kind: claimed
    split: intphys-2/main
    regime: zero-shot-surprise-best-of-~12-hyperparameter-runs
    source: https://arxiv.org/abs/2506.09849
    stars: 2
    date: 2025-06-11
    human_baseline:
      n: 3
      population: annotators, three per video, each rating at most 96 videos
      aggregation: majority-of-3
      same_items: true
      source: https://arxiv.org/abs/2506.09849
      note: a majority vote of three inflates the human figure over an individual's; Held-Out split 92.44
no_absolute_score: false
caveats:
  - "Do NOT cite the IntPhys row alone. The IntPhys 2 authors call IntPhys saturated, and the same model family is near chance on IntPhys 2's realistic scenes; that row is the binding one. V-JEPA and IntPhys 2 come from the same lab (Meta FAIR), so neither row is an independent measurement. An independent group reports the same near-chance reading on IntPhys 2 (V-JEPA 2-H 0.52), and the same architecture trained on 472 hours of one child's headcam video (SAYCam) at chance, 0.50 (https://arxiv.org/abs/2512.06232)."
  - "Not action-conditioned. The cell asks to separate what the environment does on its own from what the agent's action did; a model that predicts passive video has no action to separate. Its action-conditioned variant, V-JEPA 2-AC, fits that wording but was not read, so whether it needs a node of its own is open."
  - "ADJUDICATED AND REFUSED for `priors.objectness` (2026-10-20, from the survey's reading of arXiv 2502.11831, re-checked on the primary, and of IntPhys 2). Of Chollet's three commitments, influence-via-contact is weak where it is tested (GRASP 66%, InfLevel-lab 62%), persistence shows as a surprise signature on simple scenes and collapses on IntPhys 2, which tests permanence among its properties, and nothing in the output individuates things: the model emits a surprise score, not an index of persisting objects. The cell asks for identity across time as a first-class output, so no edge is written."
provenance:
  entered: 2026-10-20
  commit: ed471a4
  frame: llm-human-gap-survey-2026-10
  note: >-
    surfaced by the 2026-10-20 survey of the gap between LLM-based systems and human
    capacities (surveys/2026-10-20-llm-human-gap.md): six reading passes held to primary
    sources and a re-check pass, organised by this register's own cells, so it could surface
    only what those cells already ask about and the cells it proposed
---

# Latent Video Prediction (V-JEPA)

**What it is.** Pretrain a video encoder by predicting the representation of masked parts of
a clip from the rest, in latent space rather than pixels, on unlabelled natural video. At test
time, show it a pair of videos, one physically possible and one not, and read its surprise:
the prediction error is higher on the impossible one.

**The cognate.** [`priors.basic-physics`] asks for dynamics inferred from observed motion,
not supplied by an engine or hand-written rules. This is that, and nothing in the training
target names an object, a force or a law: permanence, continuity and shape constancy show up
as surprise at their violation, from 128 hours of video upward.

**Therefore.** A violation-of-expectation signature can be acquired from passive video alone,
which moves the cell from EMPTY to INDIRECT: the first technique in the register that
acquires a physical prior rather than consuming one.

**The limit.** Only in simple scenes. On IntPhys 2's realistic scenes it is at 57.51 against
96.44 for people, no better than the multimodal LLMs, and the same holds when an independent
group re-runs it. It also predicts passive video, so the cell's own question, what the
environment did as opposed to what the agent did, is not yet asked of it. The cell stays
`open`.
