from __future__ import annotations

from pathlib import Path

from src.common.inputs import InputSpec, prepare_inputs
from src.common.paths import input_dir_for, results_dir_for


def run_exercise(
    exercise: int | str,
    inputs: dict[str, InputSpec],
    process,
    overwrite: bool = False,
) -> list[Path]:
    input_dir = input_dir_for(exercise)
    output_dir = results_dir_for(exercise)

    print(f"[info] inputs directory: {input_dir}")
    print(f"[info] results directory: {output_dir}")

    input_paths = prepare_inputs(exercise, inputs, overwrite=overwrite)
    output_dir.mkdir(parents=True, exist_ok=True)

    created = process(input_paths, output_dir)
    if created is None:
        return []

    if isinstance(created, Path):
        created = [created]

    for path in created:
        print(f"[ok] saida gerada: {path}")

    return list(created)
