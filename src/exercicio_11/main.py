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

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
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


def image_negative_vectorized(image: list[list[int]]) -> list[list[int]]:
    """Compute photographic negative using NumPy subtraction."""
    return (255 - np.array(image, dtype=np.uint8)).tolist()


def image_convert_interval_vectorized(
    image: list[list[int]], new_min: int = 0, new_max: int = 100
) -> list[list[int]]:
    """Linearly remap pixel intensities using NumPy vectorized arithmetic."""
    arr = np.array(image, dtype=np.float32)
    fmin = float(arr.min())
    fmax = float(arr.max())
    result = (new_max - new_min) / (fmax - fmin) * (arr - fmin) + new_min
    return result.astype(np.uint8).tolist()


def image_invert_even_rows_vectorized(
    image: list[list[int]],
) -> list[list[int]]:
    """Horizontally flip every even-indexed row using NumPy slice reversal."""
    arr = np.array(image, dtype=np.uint8)
    arr[::2, :] = arr[::2, ::-1]
    return arr.tolist()


def image_mirror_upper_half_vectorized(
    image: list[list[int]],
) -> list[list[int]]:
    """Replace the lower half with a mirrored upper half using NumPy stacking."""
    arr = np.array(image, dtype=np.uint8)
    half = arr.shape[0] // 2
    return np.vstack([arr[:half], arr[:half][::-1]]).tolist()


def image_mirror_vertical_vectorized(
    image: list[list[int]],
) -> list[list[int]]:
    """Flip image vertically using NumPy row reversal."""
    return np.array(image, dtype=np.uint8)[::-1].tolist()


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


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "city.png": input_dir / "city.png",
        "negative.png": output_dir / "negative.png",
        "interval_100_200.png": output_dir / "interval_100_200.png",
        "interval_0_100.png": output_dir / "interval_0_100.png",
        "interval_50_150.png": output_dir / "interval_50_150.png",
        "interval_0_255.png": output_dir / "interval_0_255.png",
        "invert_even_rows.png": output_dir / "invert_even_rows.png",
        "mirror_upper_half.png": output_dir / "mirror_upper_half.png",
        "mirror_vertical.png": output_dir / "mirror_vertical.png",
    }


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
    image = load_grayscale_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks = {
        "negative": {
            "loop": benchmark_function(
                image_negative,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_negative_vectorized,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "convert_interval": {
            "loop": benchmark_function(
                image_convert_interval,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_convert_interval_vectorized,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "invert_even_rows": {
            "loop": benchmark_function(
                image_invert_even_rows,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_invert_even_rows_vectorized,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "mirror_upper_half": {
            "loop": benchmark_function(
                image_mirror_upper_half,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_mirror_upper_half_vectorized,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "mirror_vertical": {
            "loop": benchmark_function(
                image_mirror_vertical,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_mirror_vertical_vectorized,
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
