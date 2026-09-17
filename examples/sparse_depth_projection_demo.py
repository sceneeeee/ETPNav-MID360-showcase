"""Publication-safe toy demo for sparse depth projection.

This file intentionally does NOT reproduce the active research implementation,
a Livox MID360 sensor model, or any unpublished training pipeline.

It demonstrates only the public high-level idea used in the showcase:
start with a dense depth panorama, keep a configurable subset of angular rays,
and preserve the nearest valid return for each sampled column.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class SparsifyConfig:
    horizontal_stride: int = 8
    vertical_stride: int = 4
    min_depth_m: float = 0.1
    max_depth_m: float = 10.0


def make_synthetic_depth(height: int = 32, width: int = 128) -> np.ndarray:
    """Create a deterministic synthetic depth panorama in metres."""
    y = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    x = np.linspace(-np.pi, np.pi, width, dtype=np.float32)[None, :]

    wall = 3.0 + 0.4 * np.cos(2.0 * x)
    floor_shape = 0.8 * np.abs(y)
    depth = wall + floor_shape

    # Add a closer synthetic obstacle.
    h0, h1 = height // 3, 2 * height // 3
    w0, w1 = width // 2 - width // 16, width // 2 + width // 16
    depth[h0:h1, w0:w1] = 1.5
    return depth.astype(np.float32)


def sparsify_depth(depth: np.ndarray, config: SparsifyConfig) -> Tuple[np.ndarray, np.ndarray]:
    """Return a sparse depth image and boolean sampling mask.

    The sampling pattern is intentionally simple and deterministic. It is a
    pedagogical proxy for sparse angular sampling, not a Livox scan simulator.
    """
    if depth.ndim != 2:
        raise ValueError("depth must be a 2D array")
    if config.horizontal_stride <= 0 or config.vertical_stride <= 0:
        raise ValueError("strides must be positive")
    if config.min_depth_m < 0 or config.max_depth_m <= config.min_depth_m:
        raise ValueError("invalid depth range")

    valid = (
        np.isfinite(depth)
        & (depth >= config.min_depth_m)
        & (depth <= config.max_depth_m)
    )

    mask = np.zeros_like(depth, dtype=bool)
    mask[:: config.vertical_stride, :: config.horizontal_stride] = True
    mask &= valid

    sparse = np.zeros_like(depth, dtype=np.float32)
    sparse[mask] = depth[mask]
    return sparse, mask


def summarize(depth: np.ndarray, sparse: np.ndarray, mask: np.ndarray) -> dict:
    valid_dense = np.count_nonzero(np.isfinite(depth) & (depth > 0))
    sampled = int(mask.sum())
    return {
        "dense_valid_pixels": int(valid_dense),
        "sampled_pixels": sampled,
        "sampling_ratio": 0.0 if valid_dense == 0 else sampled / valid_dense,
        "mean_sampled_depth_m": 0.0 if sampled == 0 else float(sparse[mask].mean()),
    }


def main() -> None:
    depth = make_synthetic_depth()
    sparse, mask = sparsify_depth(depth, SparsifyConfig())
    stats = summarize(depth, sparse, mask)

    print("Synthetic sparse-depth demo")
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
