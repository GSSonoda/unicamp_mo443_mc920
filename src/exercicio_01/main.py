"""
1.1 Image Rotation in Multiples of 90 Degrees
==============================================
Given a monochromatic image, implement rotation at the following angles:
  (a) 90 degrees clockwise
  (b) 180 degrees
  (c) 270 degrees clockwise

The rotation must be performed without library rotation functions — pixel
indices must be remapped directly in the output matrix.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise


EXERCISE_NAME = "exercicio_01"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def rotate_90_clockwise(image: list[list[int]]) -> list[list[int]]:
    """
    Rotate a grayscale image 90 degrees clockwise.

    Solution: index remapping B[j][H-1-i] = A[i][j]. The output dimensions
    are transposed (height becomes width and vice versa).
    """
    height = len(image)
    width = len(image[0]) if height else 0
    rotated = [[0 for _ in range(height)] for _ in range(width)]

    # B[j][H - 1 - i] = A[i][j]
    for row in range(height):
        for col in range(width):
            rotated[col][height - 1 - row] = image[row][col]

    return rotated


def rotate_180(image: list[list[int]]) -> list[list[int]]:
    """
    Rotate a grayscale image 180 degrees.

    Solution: index remapping B[H-1-i][W-1-j] = A[i][j]. Equivalent to
    reversing both the row order and the column order.
    """
    height = len(image)
    width = len(image[0]) if height else 0
    rotated = [[0 for _ in range(width)] for _ in range(height)]

    # B[H - 1 - i][W - 1 - j] = A[i][j]
    for row in range(height):
        for col in range(width):
            rotated[height - 1 - row][width - 1 - col] = image[row][col]

    return rotated


def rotate_270_clockwise(image: list[list[int]]) -> list[list[int]]:
    """
    Rotate a grayscale image 270 degrees clockwise (90 degrees CCW).

    Solution: index remapping B[W-1-j][i] = A[i][j]. The output dimensions
    are transposed (height becomes width and vice versa).
    """
    height = len(image)
    width = len(image[0]) if height else 0
    rotated = [[0 for _ in range(height)] for _ in range(width)]

    # B[W - 1 - j][i] = A[i][j]
    for row in range(height):
        for col in range(width):
            rotated[width - 1 - col][row] = image[row][col]

    return rotated


def rotate_90_clockwise_alt(image: list[list[int]]) -> list[list[int]]:
    """Rotate 90 degrees clockwise using zip transpose and row reversal."""
    return [list(row) for row in zip(*image[::-1])]


def rotate_180_alt(image: list[list[int]]) -> list[list[int]]:
    """Rotate 180 degrees by reversing all rows and each row's elements."""
    return [row[::-1] for row in image[::-1]]


def rotate_270_clockwise_alt(image: list[list[int]]) -> list[list[int]]:
    """Rotate 270 degrees clockwise using zip transpose and column reversal."""
    return [list(row) for row in zip(*image)][::-1]


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])

    outputs = {
        "baboon_rotacao_90_horario.png": rotate_90_clockwise(image),
        "baboon_rotacao_180.png": rotate_180(image),
        "baboon_rotacao_270_horario.png": rotate_270_clockwise(image),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "input_baboon_monocromatica.png": input_dir / "baboon_monocromatica.png",
        "baboon_rotacao_90_horario.png": output_dir / "baboon_rotacao_90_horario.png",
        "baboon_rotacao_180.png": output_dir / "baboon_rotacao_180.png",
        "baboon_rotacao_270_horario.png": output_dir / "baboon_rotacao_270_horario.png",
    }


def run_benchmarks(
    repeats: int = 20,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    image = load_grayscale_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks = {
        "rotation_90": {
            "nao_vetorizado": benchmark_function(
                rotate_90_clockwise,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "alternativa_compreensao": benchmark_function(
                rotate_90_clockwise_alt,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "rotation_180": {
            "nao_vetorizado": benchmark_function(
                rotate_180,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "alternativa_compreensao": benchmark_function(
                rotate_180_alt,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "rotation_270": {
            "nao_vetorizado": benchmark_function(
                rotate_270_clockwise,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "alternativa_compreensao": benchmark_function(
                rotate_270_clockwise_alt,
                image,
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
                "filename": input_paths["imagem"].name,
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
