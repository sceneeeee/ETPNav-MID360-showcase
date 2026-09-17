# Public Code Examples

The code in this directory is intentionally **publication-safe**. It is included to make the showcase more concrete and reproducible without releasing the active research implementation.

## Included

- `sparse_depth_projection_demo.py`
  - creates a deterministic synthetic depth panorama;
  - applies a simple sparse angular sampling pattern;
  - reports basic sampling statistics;
  - demonstrates the public high-level idea behind sparse-depth controlled experiments.

## Not included

This repository does **not** contain:

- the active learned adapter implementation;
- current training losses or recipes;
- exact held-out split definitions;
- private Stage 5 experiment code;
- checkpoints, caches, or restricted Matterport3D assets;
- a full Livox MID360 sensor model.

The sparse-depth demo is a pedagogical proxy, not a claim of physical Livox scan fidelity.

## Run

```bash
python -m pip install -r requirements-public.txt
python examples/sparse_depth_projection_demo.py
pytest -q
```

A small generic result-table utility is also available at:

```bash
python analysis/summarize_results.py results.csv
```

with CSV columns:

```text
method,sr,spl,ne,os,ndtw,sdtw
```
