# Research Overview

This document provides a more detailed, publication-safe overview of the ETPNav-MID360 project.

It focuses on the research logic, experimental progression, and observed failure modes. Current training implementation, checkpoints, exact held-out protocols, and unpublished Stage 5 results remain private.

---

## 1. Problem formulation

ETPNav relies on a learned waypoint predictor operating on panoramic RGB-D observations. The project studies whether this interface can be adapted to sparse LiDAR observations without redesigning the downstream GraphMap and language-conditioned planner.

A useful abstraction is:

```text
sensor observation
      ↓
waypoint interface
      ↓
GraphMap
      ↓
language / topological planner
      ↓
execution
```

The central experimental strategy is to change one boundary at a time and keep downstream components frozen whenever possible.

---

## 2. Baseline reproduction

The first step was to reproduce and instrument the original ETPNav pipeline under Habitat / R2R-CE conditions.

A fixed 20-episode `val_unseen` development panel was then used for rapid controlled comparisons. This panel is intended for mechanism studies only and is not an official benchmark claim.

Baseline on that panel:

| Method | SR | SPL | NE | OS | nDTW | SDTW |
|---|---:|---:|---:|---:|---:|---:|
| Original ETPNav | 0.800 | 0.698 | 2.922 | 0.800 | 0.714 | 0.651 |

---

## 3. Explicit geometry route

### 3.1 Geometry V0

The first replacement strategy used explicit geometry instead of the original learned waypoint proposal.

```text
12-view depth
→ metric reconstruction
→ local point cloud
→ MID360-like sparsification
→ traversability / geometry
→ waypoint candidates
→ frozen GraphMap / planner
```

The first version showed a strong long-range bias, with many candidates pushed toward the maximum proposal radius.

Result on the development panel:

| Method | SR | SPL | NE | OS | nDTW | SDTW |
|---|---:|---:|---:|---:|---:|---:|
| Geometry V0 | 0.500 | 0.321 | 5.055 | 0.500 | 0.448 | 0.305 |

This suggested that geometric feasibility alone was not enough to reproduce the waypoint prior learned by ETPNav.

### 3.2 Bounded NMS

The proposal map can be viewed as:

```text
angle × distance
```

These dimensions have different topology:

- angle is circular;
- distance is bounded.

A geometry-specific bounded NMS correction improved the result:

| Method | SR | SPL | NE | OS | nDTW | SDTW |
|---|---:|---:|---:|---:|---:|---:|
| Geometry + bounded NMS | 0.550 | 0.364 | 4.526 | 0.600 | 0.467 | 0.356 |

The original ETPNav NMS implementation was not modified.

### 3.3 MRU distance-distribution ablation

The next hypothesis was that the geometry proposal failed mainly because candidates were too far away.

A middle-distance radial utility moved proposals back toward intermediate ranges, but navigation performance did not recover:

| Method | SR | SPL | NE | OS | nDTW | SDTW |
|---|---:|---:|---:|---:|---:|---:|
| MRU | 0.450 | 0.365 | 4.730 | 0.550 | 0.534 | 0.351 |

This was an important negative result:

> Matching the average waypoint-distance distribution is not sufficient to recover navigation behavior.

### 3.4 G-Min coverage experiment

G-Min removed a single preferred radial score and instead emphasized angular and radial coverage.

Result:

| Method | SR | SPL | NE | OS | nDTW | SDTW |
|---|---:|---:|---:|---:|---:|---:|
| G-Min | 0.500 | 0.428 | 4.274 | 0.650 | 0.582 | 0.399 |

Although SR did not exceed the bounded-NMS variant, several path-quality metrics improved.

---

## 4. Proposal–GraphMap interface analysis

A key observation from the geometry experiments was that increasing raw candidate diversity does not necessarily increase the action diversity seen by the graph planner.

For one audited configuration:

```text
595 raw candidates
→ 411 new ghost nodes
→ 25 existing-ghost merges
→ 159 visited-node absorptions
```

Very short-range candidates were particularly likely to be absorbed into already visited nodes.

This supports the hypothesis that:

> The proposal representation and GraphMap topology are coupled, so local geometric diversity alone is not a sufficient interface objective.

This does not imply that GraphMap is incorrect; it means that a replacement front-end must produce candidates that remain meaningful after graph association.

---

## 5. Sparse-depth zero-shot experiment

The second major route kept the original learned waypoint predictor frozen and changed only the sensor input.

```text
Dense depth
→ metric point cloud
→ deterministic MID360-like angular sparsification
→ nearest-return projection
→ sparse depth
→ frozen original waypoint predictor
```

The MID360-like input is an engineering abstraction used for controlled testing. It does not model the complete Livox sampling process, motion distortion, or all sensor noise characteristics.

Development-panel result:

| Method | SR | SPL | NE | OS | nDTW | SDTW |
|---|---:|---:|---:|---:|---:|---:|
| Sparse depth zero-shot | 0.000 | 0.000 | 9.108 | 0.000 | 0.281 | 0.000 |

The waypoint output collapsed toward a fixed short-range distance pattern.

---

## 6. Failure forensics

The next step was not retraining. Instead, the frozen network was instrumented to identify where the failure first became complete.

The important observation was:

```text
Sparse depth
→ frozen depth encoder
→ partial activation remains
→ downstream predictor
→ classifier activation collapses
→ effectively bias-driven waypoint logits
```

This changed the interpretation of the problem.

The failure was not simply:

```text
sparse input → no useful representation
```

Instead, the evidence suggested:

```text
sparse input
→ partially structured representation
→ distribution shift inside frozen predictor
→ decision-stage collapse
```

That distinction is important because it points toward interface adaptation rather than immediately replacing the entire perception stack.

---

## 7. Fixed feature-statistics alignment

A simple channel-wise mean/std alignment experiment was used to test whether first- and second-order feature statistics explained most of the domain shift.

Conceptually:

```text
F_sparse
→ normalize with sparse statistics
→ rescale with dense statistics
→ frozen waypoint predictor
```

On held-out static observations, this did not restore downstream classifier activity or waypoint diversity.

This provided another useful negative result:

> Simple global feature-statistics alignment is insufficient for the sparse-depth domain gap observed here.

---

## 8. Current research direction

The current direction is learned feature adaptation between the frozen sparse-depth representation and the frozen original waypoint predictor.

Only the high-level boundary is disclosed publicly:

```text
Sparse geometry
→ frozen depth representation
→ lightweight learned adaptation
→ frozen original waypoint predictor
→ GraphMap / planner
```

The main mechanism questions are:

1. Does the adapted representation move toward the dense feature domain?
2. Does predictor activity recover from collapse?
3. Does waypoint angular/radial diversity recover?
4. If static mechanism checks pass, does navigation improve under controlled evaluation?

The exact implementation, training recipe, data split protocol, checkpoints, and current unpublished results are intentionally omitted from this public repository.

---

## 9. Experimental principles

Several principles guide the work:

- isolate one hypothesis at a time;
- separate static mechanism experiments from navigation evaluation;
- keep original downstream modules frozen unless an experiment explicitly studies them;
- use fixed development episodes for controlled ablations;
- do not interpret development-panel results as official benchmark scores;
- preserve negative results when they change the research direction;
- avoid modifying evaluation conditions after seeing held-out outcomes.

These constraints are meant to make failure analysis more interpretable and reduce the chance that multiple simultaneous changes hide the actual cause of improvement or degradation.

---

## 10. Planned transfer path

The intended progression is:

```text
Habitat / R2R-CE
→ full validation
→ Isaac Sim native LiDAR
→ MID360 + IMU localization
→ real robot
```

The real-system architecture is expected to keep responsibilities separated:

```text
MID360 + IMU
→ localization / FAST-LIO2

RGB + LiDAR-derived geometry
→ VLN waypoint interface

high-level waypoint
→ Nav2 / MPPI
→ local control and safety
```

This keeps semantic decision making, state estimation, and low-level execution from being unnecessarily entangled.

---

## 11. What remains private

The public repository intentionally excludes:

- active research branches;
- current training implementation;
- exact training and held-out protocols;
- unpublished Stage 5 results;
- checkpoints and caches;
- private issue / PR discussions;
- restricted datasets and Matterport3D assets.

Additional technical detail can be shared selectively when appropriate for research collaboration or application review.
