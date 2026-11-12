---
id: technique.world-model-view-search
kind: technique
name: World-Model View Search (MindJourney)
addresses:
  - capability: modeling.mental-transformation
    strength: partial
    note: >-
      for a camera move, the transformed state is computed and read: a learned video model
      renders the view from a new pose out of one reference image, no authored geometry engine
      or handed scene description, and the VLM answers from those views; `partial` because
      the cell names two transformations and only one is computed — the camera moves through a
      still scene, no object is ever turned, and on the object-movement questions accuracy
      falls in 9 of 12 configurations
requires:
  - token: multimodal-model
    note: a frozen vision-language model that proposes moves, scores each rendered view twice, and answers from the kept views; GPT-4o, GPT-4.1, InternVL3-14B and o1
  - token: trained-model
    note: >-
      a controllable video-diffusion world model conditioned on camera pose; either the
      publicly released Stable-Virtual-Camera or the authors' own SWM
  - token: search-procedure
    note: Spatial Beam Search; depth 3, beam 2, exploration and helpfulness thresholds 8, trajectory length up to 8
  - token: dsl-primitives
    note: "an authored action set: 'move forward 0.25 meter, turn left 9 degrees, turn right 9 degrees', each mapped deterministically to a relative camera pose"
  - token: per-task-compute
    note: 16 to 161 seconds per question on the SWM settings in Table 4, plus the VLM's scoring calls
leverage: computation
cost: low
evidence:
  - claim: "SAT-Real top-1 accuracy, baseline -> with the authors' world model: GPT-4o 60.3 -> 70.6, GPT-4.1 74.0 -> 80.6, InternVL3-14B 59.3 -> 66.6, o1 74.6 -> 84.7; perspective-taking 45.0 -> 66.7, 39.4 -> 48.4, 45.4 -> 42.4, 69.7 -> 75.8; object-movement 85.0 -> 56.5, 73.9 -> 78.3, 69.5 -> 60.9, 82.6 -> 82.6 (Table 1; in the o1 row GPT-4o runs the search and o1 only answers)"
    kind: claimed
    split: sat/real-150
    regime: frozen-vlm-plus-swm-finetuned; depth-3-beam-2; one-run-no-variance-reported
    source: https://arxiv.org/abs/2507.12508v2
    date: 2025-11-01
    stars: 2
    requires_beyond: [training-distribution, network-access]
  - claim: "SAT-Real top-1 accuracy, baseline -> with Stable-Virtual-Camera: GPT-4o 60.3 -> 69.3, o1 74.6 -> 77.3; perspective-taking 45.0 -> 57.6, 69.7 -> 63.7; object-movement 85.0 -> 60.9, 82.6 -> 65.2 (Table 1)"
    kind: claimed
    split: sat/real-150
    regime: frozen-vlm-plus-off-the-shelf-svc; depth-3-beam-2; one-run-no-variance-reported
    source: https://arxiv.org/abs/2507.12508v2
    date: 2025-11-01
    stars: 2
    requires_beyond: [network-access]
  - claim: "SAT-Synthesized top-1 accuracy, baseline -> with the authors' world model: GPT-4o 61.0 -> 70.8, GPT-4.1 66.4 -> 75.4, InternVL3-14B 61.4 -> 66.6, o1 72.4 -> 76.8; object-movement 86.8 -> 82.6, 89.0 -> 92.4, 85.9 -> 58.2, 85.9 -> 80.4 (Table 2)"
    kind: claimed
    split: sat/synthesized-random-500-of-4000
    regime: frozen-vlm-plus-swm-finetuned; depth-3-beam-2; one-run-no-variance-reported
    source: https://arxiv.org/abs/2507.12508v2
    date: 2025-11-01
    stars: 2
    requires_beyond: [training-distribution, network-access]
  - claim: "SAT-Synthesized top-1 accuracy, baseline -> with Stable-Virtual-Camera: GPT-4o 61.0 -> 72.3, o1 72.4 -> 78.6; object-movement 86.8 -> 84.8, 85.9 -> 80.4 (Table 2)"
    kind: claimed
    split: sat/synthesized-random-500-of-4000
    regime: frozen-vlm-plus-off-the-shelf-svc; depth-3-beam-2; one-run-no-variance-reported
    source: https://arxiv.org/abs/2507.12508v2
    date: 2025-11-01
    stars: 2
    requires_beyond: [network-access]
no_absolute_score: false
caveats:
  - "The row for this cell is the average WITH the object-movement column. The mechanism moves a camera through a still scene and has no action for moving anything in it. Across the 12 baseline/world-model pairs in Tables 1 and 2, object-movement accuracy falls in 9, is flat in 1 and rises in 2, by as much as 28.5 and 27.7 points (GPT-4o on SAT-Real, InternVL3-14B on SAT-Synthesized). The conclusion's 'robust' reading across all categories does not hold for that column. Mental rotation of an object, the cell's human source, is neither computed nor measured here."
  - "'Without any fine-tuning' is the VLM only. SWM is a fine-tuned model: 'we only finetuned the camera encoder and a newly introduced projector', on 50K Habitat, 10K RealEstate10K and 10K DL3DV-10K clips, on eight H100s over about three days. That is `requires_beyond` on the SWM rows. The SVC rows use a public generator, tested with GPT-4o and o1 only."
  - "The transformed state is a sample, not a state the system holds or can check. 'Because the generator is unaware of the downstream query, it can hallucinate views that are irrelevant—or even contradictory'; regions out of view are filled from what the model has seen (Appendix B.1.4, 'the model may rely on weak priors'), which is the scene-prior reading the cell warns about, entering at the renderer. Limited to one reference image."
  - "Precision. SAT-Real has 150 questions, so one question is 0.67 points and no single delta is much past two standard errors of an unpaired difference (about 5 points at this accuracy; this entry's arithmetic, not the paper's). Tables 1 and 2 report no seeds or intervals on accuracy. SAT-Synthesized is 'a random 500-question subset' of 4,000, seed unstated."
  - "No control separates the views from the search. The ablations vary search depth and score threshold on GPT-4o with SWM; no arm replaces the rendered views with uninformative ones or lets the VLM answer after the same number of scoring calls without them. The paper's average deltas: 7.7 points on SAT-Real reproduces as the unweighted mean of the six rows (7.67); 8.0 on SAT-Synthesized does not (7.65)."
  - "The claim that 'a plain VLM augmented with our world-model search already surpasses the RL-fine-tuned o1' on both splits holds for GPT-4.1 with SWM alone; GPT-4o and InternVL3-14B do not reach the o1 baseline with it."
  - "Unpriced estimate: Table 4 gives 16.27 to 161.48 seconds per question on one VLM-and-SWM setup, split not stated. `cost: low` assumes the GPU rental and the scoring calls of one question come to under a dollar; no row prices it, and SWM's training is excluded as the label requires. The arXiv record gives no venue; the authors' repository states NeurIPS 2025 acceptance (https://github.com/UMass-Embodied-AGI/MindJourney)."
provenance:
  entered: 2026-11-09
  frame: repo-watch-2026-11
  note: >-
    a maintainer's watch of new GitHub repositories and arXiv papers; two rows read by hand on
    2026-11-07 against two cells the gap report listed EMPTY, so it could surface only what
    those cells already ask about
---

# World-Model View Search (MindJourney)

**What it is.** A vision-language model is asked a spatial question about one photograph. Instead
of answering it directly, it searches: three camera primitives (forward 0.25 m, turn left or
right 9 degrees) are chained into candidate trajectories, a video-diffusion world model renders
the view each would reach, and the VLM scores each rendered view twice, for whether to keep
exploring from it and for how much it helps. A beam search keeps the best and an evidence buffer
keeps the most helpful; the VLM then answers from the original image and the buffer. The VLM is
not retrained.

**The cognate.** The person asked what is to the left of the door from where they would stand if
they walked through the room, who pictures the walk and reads off the answer. The paper states
the lack this way: VLMs "perceive 2D images but lack an internal model of 3D dynamics".

**Why `partial`.** The cell's direct case is a system that computes the transformed state from
its own representation of the scene and answers from it, and for a camera move this does: a
learned renderer produces the new view from a single image, with no authored geometry engine and
no handed scene description. The cell also names the object turned, and it takes its human
source from Shepard and Metzler. Nothing here turns an object, and where SAT asks about moving
objects, accuracy falls in most configurations.

**The limit.** The gains are on two splits of one benchmark, in single runs, and depend on how
far the renderer can be trusted from its reference frame: the authors find deeper search hurting
on real outdoor scenes for that reason. Whether answers improve because the views are informative,
or because being asked to look again helps, is not separated.
