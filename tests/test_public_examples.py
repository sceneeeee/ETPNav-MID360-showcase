import importlib.util
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_sparse_depth_demo_is_deterministic():
    demo = load_module("sparse_demo", ROOT / "examples" / "sparse_depth_projection_demo.py")
    depth_a = demo.make_synthetic_depth()
    depth_b = demo.make_synthetic_depth()
    np.testing.assert_allclose(depth_a, depth_b)

    sparse, mask = demo.sparsify_depth(depth_a, demo.SparsifyConfig())
    assert sparse.shape == depth_a.shape
    assert mask.shape == depth_a.shape
    assert mask.dtype == bool
    assert np.count_nonzero(sparse) == int(mask.sum())


def test_result_table_formatter():
    summary = load_module("summary", ROOT / "analysis" / "summarize_results.py")
    rows = [
        summary.ResultRow("Baseline", 0.8, 0.7, 2.9, 0.8, 0.71, 0.65),
        summary.ResultRow("Variant", 0.5, 0.4, 4.2, 0.6, 0.58, 0.39),
    ]
    table = summary.to_markdown(rows)
    assert "Baseline" in table
    assert "Variant" in table
    assert "SR ↑" in table
