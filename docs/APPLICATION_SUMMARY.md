# Application-Facing Project Summary

This page provides a concise version of the project suitable for research applications, CV references, or email links.

## One-sentence description

**ETPNav-MID360 studies how an RGB-D-based Vision-and-Language Navigation system can be adapted to sparse LiDAR observations while preserving the original downstream topological planning stack.**

## Short project description

The project starts from ETPNav, a VLN system that uses panoramic RGB-D observations to propose local waypoints and perform topological planning. The research focuses on replacing or adapting the dense depth interface for MID360-style sparse LiDAR geometry without simultaneously redesigning GraphMap, the language-conditioned planner, and execution.

The work has progressed through three main stages:

1. **Explicit geometry:** replacing the learned waypoint proposal with geometry-derived candidates and testing several proposal distributions and suppression strategies.
2. **Failure analysis:** showing that sparse-depth zero-shot input causes a severe waypoint-predictor domain failure, then tracing the failure through intermediate activations rather than immediately retraining the model.
3. **Feature adaptation:** using the failure analysis to motivate a learned sparse-to-dense feature adaptation strategy while keeping the original downstream predictor frozen.

## Contributions

- Reproduced and instrumented the ETPNav / Habitat baseline for controlled R2R-CE experiments.
- Designed multiple MID360-inspired waypoint proposal baselines and documented their failure modes.
- Identified that matching waypoint distance distribution alone does not recover navigation behavior.
- Audited the coupling between local waypoint proposals and GraphMap association.
- Located the complete sparse-depth activation collapse downstream of the depth encoder inside the frozen waypoint predictor.
- Tested and rejected simple channel-wise feature-statistics alignment as an insufficient adaptation strategy.
- Built a staged experimental workflow that separates static mechanism checks from navigation evaluation.

## Current status

Current work investigates learned nonlinear feature adaptation between sparse LiDAR-derived depth representations and the frozen original waypoint predictor. Exact implementation and unpublished results remain private while the research is ongoing.

## Research direction

```text
Habitat / R2R-CE
→ sparse LiDAR adaptation
→ controlled navigation validation
→ Isaac Sim native LiDAR
→ MID360 + IMU localization
→ real robot deployment
```

## Links

- [Main showcase README](../README.md)
- [Detailed research overview](RESEARCH_OVERVIEW.md)
- [Original ETPNav repository](https://github.com/MarSaKi/ETPNav)
- [ETPNav paper](https://arxiv.org/abs/2304.03047)
