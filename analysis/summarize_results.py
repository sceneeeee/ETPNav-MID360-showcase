"""Small utility for summarizing controlled VLN result tables.

This script is deliberately generic and operates on CSV files supplied by the
user. It contains no private episode IDs, dataset paths, checkpoints, or active
research logic.

Expected columns:
method,sr,spl,ne,os,ndtw,sdtw
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class ResultRow:
    method: str
    sr: float
    spl: float
    ne: float
    os: float
    ndtw: float
    sdtw: float


def load_results(path: Path) -> List[ResultRow]:
    rows: List[ResultRow] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"method", "sr", "spl", "ne", "os", "ndtw", "sdtw"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain columns: {sorted(required)}")

        for item in reader:
            rows.append(
                ResultRow(
                    method=item["method"],
                    sr=float(item["sr"]),
                    spl=float(item["spl"]),
                    ne=float(item["ne"]),
                    os=float(item["os"]),
                    ndtw=float(item["ndtw"]),
                    sdtw=float(item["sdtw"]),
                )
            )
    return rows


def to_markdown(rows: Iterable[ResultRow]) -> str:
    rows = list(rows)
    header = "| Method | SR ↑ | SPL ↑ | NE ↓ | OS ↑ | nDTW ↑ | SDTW ↑ |"
    rule = "|---|---:|---:|---:|---:|---:|---:|"
    body = [
        f"| {r.method} | {r.sr:.3f} | {r.spl:.3f} | {r.ne:.3f} | {r.os:.3f} | {r.ndtw:.3f} | {r.sdtw:.3f} |"
        for r in rows
    ]
    return "\n".join([header, rule] + body)


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python analysis/summarize_results.py results.csv")
        return 2

    rows = load_results(Path(argv[1]))
    print(to_markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
