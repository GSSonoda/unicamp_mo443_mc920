"""
1.11 Intensity Transformation
==============================
Given a monochromatic image, transform its intensity space (gray levels):
  (b) Obtain the negative: gray level 0 -> 255, level 1 -> 254, etc.
  (c) Remap intensities to a new interval [new_min, new_max].
  (d) Invert (horizontally flip) the pixels of every even-indexed row.
  (e) Mirror the upper half of the image onto the lower half.
  (f) Apply a vertical flip to the entire image.
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

EXERCISE_NAME = "exercicio_11"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/city.png",
}


def image_negative(image: list[list[int]]) -> list[list[int]]:
    """
    Compute the photographic negative of a grayscale image.

    Solution: subtract each pixel value from 255 — p' = 255 - p.
    This maps black (0) to white (255) and vice versa.
    """
    return [[255 - pixel for pixel in row] for row in image]


def image_convert_interval(
    image: list[list[int]], new_min: int = 0, new_max: int = 100
) -> list[list[int]]:
    """
    Linearly remap pixel intensities from [fmin, fmax] to [new_min, new_max].

    Solution: standard linear interpolation
      g = (new_max - new_min) / (fmax - fmin) * (f - fmin) + new_min
    where fmin and fmax are the actual minimum and maximum of the image.
    """
    fmin = min(min(row) for row in image)
    fmax = max(max(row) for row in image)
    return [
        [
            int((new_max - new_min) / (fmax - fmin) * (pixel - fmin) + new_min)
            for pixel in row
        ]
        for row in image
    ]


def image_invert_even_rows(image: list[list[int]]) -> list[list[int]]:
    """
    Horizontally flip every even-indexed row (rows 0, 2, 4, ...).

    Solution: use Python slice reversal `row[::-1]` conditionally on the
    row index parity. Odd rows are returned unchanged.
    """
    return [row[::-1] if i % 2 == 0 else row for i, row in enumerate(image)]


def image_mirror_upper_half(image: list[list[int]]) -> list[list[int]]:
    """
    Replace the lower half of the image with a reversed copy of the upper half.

    Solution: slice the first half, concatenate it with its reversed version.
    The output has the same height as the input.
    """
    half_height = len(image) // 2
    return image[:half_height] + image[:half_height][::-1]


def image_mirror_vertical(image: list[list[int]]) -> list[list[int]]:
    """
    Flip the image vertically (reverse the row order).

    Solution: reverse the outer list with `image[::-1]`.
    """
    return image[::-1]


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "negative.png": image_negative(img),
        "interval_100_200.png": image_convert_interval(
            img, new_min=100, new_max=200
        ),
        "interval_0_100.png": image_convert_interval(
            img, new_min=0, new_max=100
        ),
        "interval_50_150.png": image_convert_interval(
            img, new_min=50, new_max=150
        ),
        "interval_0_255.png": image_convert_interval(
            img, new_min=0, new_max=255
        ),
        "invert_even_rows.png": image_invert_even_rows(img),
        "mirror_upper_half.png": image_mirror_upper_half(img),
        "mirror_vertical.png": image_mirror_vertical(img),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
