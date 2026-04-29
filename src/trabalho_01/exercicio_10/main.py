"""
1.10 Image Combination
======================
Combine two monochromatic images of the same size via a weighted average of
their gray levels:

  output(i, j) = w1 * image1(i, j) + w2 * image2(i, j)

Test with weight pairs: (0.5, 0.5), (0.7, 0.3), (0.3, 0.7).
"""

import sys
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_10"
INPUTS = {
    "baboon": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
    "butterfly": "https://www.ic.unicamp.br/~helio/imagens_png/butterfly.png",
}


def image_combination(
    image1: list[list[int]],
    image2: list[list[int]],
    weight1: float = 0.5,
    weight2: float = 0.5,
) -> list[list[int]]:
    """
    Combine two same-size grayscale images by weighted average.

    Solution: for each pixel position (i, j), compute
    output = int(w1 * p1 + w2 * p2). When w1 + w2 = 1 the result stays
    within [0, 255] without explicit clamping.
    """
    output_image = [[0] * len(image1[0]) for _ in range(len(image1))]
    for i in range(len(image1)):
        for j in range(len(image1[0])):
            output_image[i][j] = int(
                weight1 * image1[i][j] + weight2 * image2[i][j]
            )
    return output_image


def image_combination_vectorized(
    image1: list[list[int]],
    image2: list[list[int]],
    weight1: float = 0.5,
    weight2: float = 0.5,
) -> list[list[int]]:
    """
    Combine two grayscale images by weighted average using NumPy operations.

    Identical result as ``image_combination`` but uses vectorized array
    arithmetic instead of nested Python loops.
    """
    arr1 = np.array(image1, dtype=np.float32)
    arr2 = np.array(image2, dtype=np.float32)
    result = np.clip(weight1 * arr1 + weight2 * arr2, 0, 255).astype(np.uint8)
    return result.tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    baboon = load_grayscale_image(input_paths["baboon"])
    butterfly = load_grayscale_image(input_paths["butterfly"])

    outputs = {
        f"combination_{weight1}_{weight2}.png": image_combination(
            baboon, butterfly, weight1, weight2
        )
        for weight1, weight2 in [(0.5, 0.5), (0.7, 0.3), (0.3, 0.7)]
    }
    return save_grayscale_outputs(output_dir, outputs)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    files: dict[str, Path] = {
        "baboon_monocromatica.png": (
            input_dir / "baboon_monocromatica.png"
        ),
        "butterfly.png": input_dir / "butterfly.png",
    }
    for w1, w2 in [(0.5, 0.5), (0.7, 0.3), (0.3, 0.7)]:
        name = f"combination_{w1}_{w2}.png"
        files[name] = output_dir / name
    return files


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def run_benchmarks(
    repeats: int = 20,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
    baboon = load_grayscale_image(input_paths["baboon"])
    butterfly = load_grayscale_image(input_paths["butterfly"])
    height = len(baboon)
    width = len(baboon[0]) if height else 0

    benchmarks = {
        "image_combination": {
            "loop": benchmark_function(
                image_combination,
                baboon,
                butterfly,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_combination_vectorized,
                baboon,
                butterfly,
                repeats=repeats,
                warmup=warmup,
            ),
        },
    }

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "image": {
                "filename": input_paths["baboon"].name,
                "width": width,
                "height": height,
            },
            "benchmarks": benchmarks,
        },
    )
    print(f"[ok] Benchmark salvo em: {output_path}")
    return output_path


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
