from __future__ import annotations

import json
from datetime import datetime, UTC
from math import sqrt
from pathlib import Path
from time import perf_counter

from src.common.paths import benchmarks_dir_for


def benchmark_function(
    func,
    *args,
    repeats: int = 20,
    warmup: int = 2,
):
    for _ in range(warmup):
        func(*args)

    runs: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        func(*args)
        end = perf_counter()
        runs.append(end - start)

    mean = sum(runs) / len(runs)
    variance = sum((run - mean) ** 2 for run in runs) / len(runs)

    return {
        "runs_seconds": runs,
        "mean_seconds": mean,
        "min_seconds": min(runs),
        "max_seconds": max(runs),
        "std_seconds": sqrt(variance),
        "repeats": repeats,
        "warmup": warmup,
    }


def write_benchmark_results(
    exercise: int | str,
    filename: str,
    payload: dict,
) -> Path:
    output_dir = benchmarks_dir_for(exercise)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        **payload,
    }
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path
