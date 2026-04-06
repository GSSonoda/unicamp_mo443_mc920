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

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
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


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
