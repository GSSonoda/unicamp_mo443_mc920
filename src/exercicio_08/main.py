"""
1.8 Transformation of Colored Images
======================================
(a) Given a color image in RGB format, apply the following linear transform:
      R' = 0.393R + 0.769G + 0.189B
      G' = 0.349R + 0.686G + 0.168B
      B' = 0.272R + 0.534G + 0.131B
    Values exceeding 255 are clipped to 255.

(b) Given a color image in RGB format, convert it to a single-band
    grayscale image using the weighted average:
      I = 0.2989R + 0.5870G + 0.1140B
"""

import sys
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import (
    load_rgb_image,
    save_grayscale_outputs,
    save_rgb_outputs,
)
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_08"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/watch.png",
}

# (a) Per-channel weights for the sepia-like color transformation
RED_TRANSFORM = [0.393, 0.769, 0.189]
GREEN_TRANSFORM = [0.349, 0.686, 0.168]
BLUE_TRANSFORM = [0.272, 0.534, 0.131]

# (b) Luminance weights for RGB-to-grayscale conversion (ITU-R BT.601)
TRANSFORM_RGB = [0.2989, 0.5870, 0.1140]


def image_color_transform(
    image: list[list[tuple[int, int, int]]],
    red_transform: list[float] = RED_TRANSFORM,
    green_transform: list[float] = GREEN_TRANSFORM,
    blue_transform: list[float] = BLUE_TRANSFORM,
) -> list[list[tuple[int, int, int]]]:
    """
    Apply a per-channel linear color transformation to an RGB image.

    Solution: for each pixel (R, G, B), compute new channel values as the dot
    product of each transform row with [R, G, B]. Results are cast to int and
    clipped to 255. This produces a sepia-like warm tone shift.
    """
    output_image = [[(0, 0, 0)] * len(image[0]) for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            r, g, b = image[i][j]
            new_r = int(
                red_transform[0] * r
                + red_transform[1] * g
                + red_transform[2] * b
            )
            new_g = int(
                green_transform[0] * r
                + green_transform[1] * g
                + green_transform[2] * b
            )
            new_b = int(
                blue_transform[0] * r
                + blue_transform[1] * g
                + blue_transform[2] * b
            )
            output_image[i][j] = (
                min(new_r, 255),
                min(new_g, 255),
                min(new_b, 255),
            )
    return output_image


def image_to_grayscale(
    image: list[list[tuple[int, int, int]]],
    weights: list[float] = TRANSFORM_RGB,
) -> list[list[int]]:
    """
    Convert an RGB image to grayscale using a weighted average.

    Solution: each pixel becomes I = w_R·R + w_G·G + w_B·B, where the
    default weights (0.2989, 0.5870, 0.1140) follow the ITU-R BT.601
    luma coefficients, which reflect human perceptual sensitivity to each
    color channel. Result is clipped to [0, 255].
    """
    return [
        [
            min(int(weights[0] * r + weights[1] * g + weights[2] * b), 255)
            for r, g, b in row
        ]
        for row in image
    ]


def image_color_transform_vectorized(
    image: list[list[tuple[int, int, int]]],
    red_transform: list[float] = RED_TRANSFORM,
    green_transform: list[float] = GREEN_TRANSFORM,
    blue_transform: list[float] = BLUE_TRANSFORM,
) -> list[list[tuple[int, int, int]]]:
    """
    Apply per-channel linear color transformation using NumPy matrix multiply.

    Stacks the three row vectors into a (3, 3) matrix and uses a single
    matrix multiply instead of per-pixel Python loops.
    """
    arr = np.array(image, dtype=np.float32)  # (H, W, 3)
    mat = np.array(
        [red_transform, green_transform, blue_transform], dtype=np.float32
    )  # (3, 3)
    result = np.clip(arr @ mat.T, 0, 255).astype(np.uint8)
    return [
        [tuple(int(v) for v in pixel) for pixel in row]
        for row in result.tolist()
    ]


def image_to_grayscale_vectorized(
    image: list[list[tuple[int, int, int]]],
    weights: list[float] = TRANSFORM_RGB,
) -> list[list[int]]:
    """
    Convert RGB to grayscale using NumPy dot product along the channel axis.
    """
    arr = np.array(image, dtype=np.float32)  # (H, W, 3)
    w = np.array(weights, dtype=np.float32)
    result = np.clip(arr @ w, 0, 255).astype(np.uint8)
    return result.tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_rgb_image(input_paths["imagem"])
    transformed_img = image_color_transform(img)
    grayscale_img = image_to_grayscale(img)

    saved = save_rgb_outputs(
        output_dir, {"watch_transformed.png": transformed_img}
    )
    saved += save_grayscale_outputs(
        output_dir, {"watch_grayscale.png": grayscale_img}
    )
    return saved


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "watch.png": input_dir / "watch.png",
        "watch_transformed.png": output_dir / "watch_transformed.png",
        "watch_grayscale.png": output_dir / "watch_grayscale.png",
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
    image = load_rgb_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks = {
        "color_transform": {
            "loop": benchmark_function(
                image_color_transform,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_color_transform_vectorized,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "to_grayscale": {
            "loop": benchmark_function(
                image_to_grayscale,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_to_grayscale_vectorized,
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
