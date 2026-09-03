---
id: technique.counterfactual-probe-segmentation
kind: technique
name: Counterfactual-Probe Segmentation (SpelkeNet)
addresses:
  - capability: priors.objectness
    strength: partial
    note: >-
      the partition is produced by poking the scene inside a learned video predictor and
      reading which regions move together — cohesion and influence-via-contact acquired
      from unlabelled video, with no segmentation labels and no authored object vocabulary;
      `partial` and not `direct` because persistence, the second of the cell's three
      commitments, is absent — see caveats
requires:
  - token: trained-model
    note: a large autoregressive video predictor, trained before deployment
  - token: weight-gradients
    note: the predictor is trained, not prompted
  - token: training-distribution
    note: a large unlabelled video corpus — here ~7k hours plus 3D and video datasets
  - token: correspondence-estimator
    note: >-
      training targets are optical-flow fields from SeaRAFT, a separately trained
      supervised flow network — the acquisition routes through a supplied instrument
leverage: computation
cost: extreme
evidence:
  - claim: "unprompted automatic segmentation on SpelkeBench: AP 0.35 / AR 0.46 / mIoU 0.57 / F1 0.38, against self-supervised discovery baselines CutLER 0.41/0.32/0.42/0.34 and ProMerge 0.42/0.34/0.43/0.36"
    kind: claimed
    split: spelkebench/500-images
    regime: 64xH100-14d-pretrain-then-inference-only
    source: https://arxiv.org/html/2507.16038v1
    date: 2025-07-21
    stars: 2
no_absolute_score: false
caveats:
  - "Grade this on the UNPROMPTED frame only. The paper's headline — SpelkeNet 0.5411 AR over supervised SAM2 0.4816 — is Table 1, where each prompt is 'generated using the centroid' of a ground-truth segment: the benchmark hands over how many objects there are and where each one is, and the system supplies only the extent. In Table 2, with no seed, the differential reverses (SpelkeNet AR 0.46 vs SAM2 0.62). A test asking whether the system produced the partition cannot be settled in a frame that supplies the count and the location (https://arxiv.org/html/2507.16038v1)."
  - "Does NOT address `modeling.state-abstraction`. SpelkeNet emits a single-image mask; there is no cross-frame index and no measurement of identity through occlusion or feature change anywhere in the paper. That cell's own text names this specimen as the failure it was written for — 'a per-frame segmenter produces a fresh, anonymous set of regions every step'."
  - "Persistence is the missing one of Chollet's three commitments. Cohesion (regions that move together under a poke) and influence-via-contact (motion propagating across contact) are both acquired here; persistence is not tested, which is exactly the omission `priors.objectness` was written to flag."
  - "Superseded within its own lineage before entry: PSI (arXiv:2509.09737, same lab, v1 10 Sep 2025) reports 0.65 mIoU / 0.54 AR on the same auto-segmentation benchmark against SpelkeNet's 0.57 / 0.46, by folding extracted structure back into training. PSI's prose and table disagree on that figure (0.57 vs 0.65) and this register has not adjudicated it. Written on SpelkeNet because it introduces the benchmark and its numbers verify cleanly; revisit when PSI's inconsistency resolves."
  - "The paper's downstream transfer arm is partly in-family: 3DEditBench and the LRAS-3D editor are the same authors on the same backbone. Three independently authored editors (LightningDrag, DiffusionHandles, DiffusionAsShader) do move the same way under a pure segment swap, on smaller margins; cite those three, not the benchmark."
provenance:
  entered: 2026-09-03
  commit: 6346d73
  frame: exploration-harness
  note: >-
    admitted by exploration-harness run wf_b93ef41d-166, the item-3 re-ask with the
    arc-agi-3 admissibility screen dropped; this literature was structurally invisible to
    the earlier run because it is gradient-trained
---

# Counterfactual-Probe Segmentation (SpelkeNet)

**What it is.** Train a large autoregressive predictor on unlabelled video, then segment
without ever training a segmenter: apply a virtual "poke" to a location, sample what the
predictor thinks happens next, and keep the region whose motion is correlated with the
poke. The object is whatever moves together when you push it.

**The cognate.** This is the register's first entry against a Core Knowledge prior that
**acquires** it rather than consuming it. Every other candidate for this cell arrives
holding an authored vocabulary — [`technique.dsl-search`]'s primitives, DOORMAX's object
types — and is capped at `incidental` by the supplied/acquired test. Here the grouping
comes out of a prediction objective that never names an object, which is why it clears
`partial` where they do not.

**Therefore.** Where you can afford a pretrained video predictor, objectness need not be
authored. That is a claim about what is possible, not about what is cheap: the regime is
64 H100s for roughly 14 days, and the register holds it at two stars.

**The limit.** Two, and they are different in kind. The acquisition is not clean —
training targets come from SeaRAFT, a supervised flow network, so correspondence is
supplied even though the vocabulary is not. And the output is a per-image mask: nothing
here carries a thing from one frame to the next, so [`modeling.state-abstraction`] stays
empty and the cell's third commitment, persistence, remains untested.
