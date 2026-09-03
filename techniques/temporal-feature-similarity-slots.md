---
id: technique.temporal-feature-similarity-slots
kind: technique
name: Temporal Feature-Similarity Slots (VideoSAUR)
addresses:
  - capability: modeling.state-abstraction
    strength: partial
    note: >-
      slots are an explicit addressable set that downstream code can name, and the reported
      metric is a single clustering over the whole video, so a mid-clip identity swap is
      charged against the score — identity acquired from a target (next-frame patch
      affinity) in which no id, mask or count appears; `partial` and not `direct` because
      the paper never stratifies by occlusion and the margin over an identity-perfect
      trivial control is under 2x — see caveats
requires:
  - token: trained-model
    note: a slot encoder-decoder trained before deployment
  - token: weight-gradients
    note: the slot model is trained, not prompted
  - token: training-distribution
    note: an unlabelled video corpus of the target domain
  - token: frozen-self-supervised-features
    note: >-
      a frozen DINO ViT-B/16 supplies both the input features and the prediction target —
      the partition is acquired, the feature space it is drawn in is supplied
leverage: computation
cost: high
evidence:
  - claim: "whole-video FG-ARI 28.9 ± 0.4 on FULL-LENGTH YouTube-VIS 2021 validation videos, against an identity-perfect trivial control (Block Pattern, a fixed spatial grid) at 15.1 and STEVE at 15.0 ± 0.7; the 6-frame / 12-frame / full-length series is 39.5 / 35.8 / 28.9, 5 seeds, frozen DINO ViT-B/16"
    kind: claimed
    split: youtube-vis-2021/validation-full-length
    regime: 18h-1xA100-40GB-per-100k-step-run
    source: https://arxiv.org/html/2306.04829v2
    date: 2023-12-08
    stars: 2
no_absolute_score: false
caveats:
  - "Do NOT cite the headline for this cell. MOVi-E 73.9 whole-video FG-ARI sits against 78.4 IMAGE FG-ARI for the same model on the same 5 seeds (Tables 1 and A.1): the whole-video matching costs 4.5 points, so ~94% of 73.9 is per-frame segmentation quality and only the remainder is identity. The full-length YT-VIS row is carried instead because a single clustering over an entire real video cannot be re-read as frame-averaged quality."
  - "The Block Pattern control is what makes the row interpretable, and it also refuses a tempting inference. It is a fixed spatial grid: its cross-frame index is perfect by construction while it knows nothing about objects. So a small video-vs-image FG-ARI gap does NOT prove identity — Block Pattern's gap on MOVi-E (-5.9) is LARGER than VideoSAUR's (-4.5). Identity is evidenced by the margin over that control (28.9 vs 15.1, widening with clip length: 1.65x at 6 frames, 1.91x at full), not by the gap."
  - "MOVi-C is excluded, not merely uncited. `configs/videosaur/movi_c.yml` sets NUM_SLOTS 11 = the generator's max_num_objects 10 plus background, i.e. the object count is read off the answer key. MOVi-E at NUM_SLOTS 15 survives only because 15 matches no ground-truth statistic — movi_def_worker.py generates 11-23 objects, mean 17 — and it is a supporting row, with the caveat that 15 over-provisions ~36% of scenes."
  - "The DAVIS 34.0 and YouTube-VIS-2019 41.3 mBO transfer figures must NOT be entered. The paper takes each at the 'optimal number of slots' from an evaluation-time sweep against the target set's own ground truth — the object count re-entering through the back door, one level less visibly than MOVi-C."
  - "Occlusion is never measured, only attributed. The 39.5 -> 28.9 decay is stratified by DURATION, and both mentions of occlusion in v2 are prose explaining that decay. `modeling.state-abstraction` asks for identity surviving occlusion or feature change as a MEASUREMENT; on this evidence `direct` is unavailable, and that is the binding reason for `partial`, ahead of the frozen-backbone dependency."
  - "Not adjudicated for `priors.objectness`, deliberately. Cohesion and persistence both look acquired here and influence-via-contact does not, which would make it the mirror image of `technique.counterfactual-probe-segmentation`. The run that admitted this node examined only the state-abstraction cell, and an unexamined second claim is exactly what was withdrawn before entry in the run before it."
provenance:
  entered: 2026-09-03
  commit: PENDING
  frame: exploration-harness
  note: >-
    admitted by exploration-harness run wf_8808d2a6-f62, the state-abstraction cell asked
    alone in the video frame; the earlier three-cell run returned an image specimen and
    never reached this sub-literature
---

# Temporal Feature-Similarity Slots (VideoSAUR)

**What it is.** Train a slot encoder-decoder on unlabelled video with one target: from the
slots at frame *t*, predict for each patch the affinity distribution between that patch's
frozen DINO feature and every patch feature at frame *t+1*. No object, instance, count or
id appears anywhere in that target — it is a matrix product over an unlabelled clip.

**The cognate.** The cheapest way to lower that loss is a partition into units whose future
affinity pattern is jointly predictable, and a patch's future affinity is settled by which
thing it belongs to and where that thing went. Identity is squeezed out of correspondence
structure. Two properties then carry the cell: the abstraction is **externalised** — slots
are an addressable K-vector set, so downstream code can name slot 3 and get the same thing
next frame, which is precisely what a method holding identity implicitly in weights cannot
hand over — and the score is a **whole-video** clustering, so a mid-clip swap is charged.

**Therefore.** Cross-frame identity does not have to be annotated. Supervising one level
BELOW the answer — on next-frame feature affinity, a quantity no annotator ever touches —
is enough to make a stable index fall out. That is the same move as
[`technique.counterfactual-probe-segmentation`] one axis over: poke for cohesion, predict
for persistence.

**The limit, and it is not the one the paper advertises.** The advertised limit is the
frozen backbone. The real one is that **occlusion is never measured**. The cell asks for an
index that survives occlusion and feature change; what is reported is a decay with clip
length, narrated as occlusion-driven. And the margin that does carry the row — 28.9 against
a fixed grid's 15.1 — is under 2x. This is a thin fill honestly recorded, not a solved cell.
