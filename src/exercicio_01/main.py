from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.report import copy_report_files
from src.common.runner import run_exercise


EXERCISE_NAME = "exercicio_01"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def rotate_90_clockwise(image: list[list[int]]) -> list[list[int]]:
    height = len(image)
    width = len(image[0]) if height else 0
    rotated = [[0 for _ in range(height)] for _ in range(width)]

    # B[j][H - 1 - i] = A[i][j]
    for row in range(height):
        for col in range(width):
            rotated[col][height - 1 - row] = image[row][col]

    return rotated


def rotate_180(image: list[list[int]]) -> list[list[int]]:
    height = len(image)
    width = len(image[0]) if height else 0
    rotated = [[0 for _ in range(width)] for _ in range(height)]

    # B[H - 1 - i][W - 1 - j] = A[i][j]
    for row in range(height):
        for col in range(width):
            rotated[height - 1 - row][width - 1 - col] = image[row][col]

    return rotated


def rotate_270_clockwise(image: list[list[int]]) -> list[list[int]]:
    height = len(image)
    width = len(image[0]) if height else 0
    rotated = [[0 for _ in range(height)] for _ in range(width)]

    # B[W - 1 - j][i] = A[i][j]
    for row in range(height):
        for col in range(width):
            rotated[width - 1 - col][row] = image[row][col]

    return rotated


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])

    outputs = {
        "baboon_rotacao_90_horario.png": rotate_90_clockwise(image),
        "baboon_rotacao_180.png": rotate_180(image),
        "baboon_rotacao_270_horario.png": rotate_270_clockwise(image),
    }
    created = save_grayscale_outputs(output_dir, outputs)

    # Keep a local copy of the input and outputs next to the report.
    copy_report_files(
        EXERCISE_NAME,
        {
            "input_baboon_monocromatica.png": input_paths["imagem"],
            **{path.name: path for path in created},
        },
    )

    return created


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
