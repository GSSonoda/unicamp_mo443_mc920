"""
1.2 Image Amplification by Replication
=======================================
From a monochromatic image, generate an enlarged image using pixel
replication:
  (a) amplification by a factor of 2
  (b) amplification by a factor of 4

Each pixel of the original image is replicated to form an N×N block of
identical pixels in the enlarged image.
"""

import sys
from pathlib import Path

import numpy as np

from src.common.paths import input_dir_for, results_dir_for

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_02"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def image_upscaling_4x_vectorized(image: list[list[int]]) -> list[list[int]]:
    """
    Upscale a grayscale image by a factor of 4 using NumPy replication.

    Solution: np.repeat applied twice — once along rows (axis=0) and once
    along columns (axis=1) — replicates each pixel into a 4×4 block.
    """
    arr = np.array(image, dtype=np.uint8)
    upscaled_axis0 = np.repeat(arr, 4, axis=0)
    upscaled = np.repeat(upscaled_axis0, 4, axis=1)
    return upscaled.tolist()


def image_upscaling_2x(image: list[list[int]]) -> list[list[int]]:
    """
    Upscale a grayscale image by a factor of 2 using NumPy replication.

    Solution: np.repeat applied twice — once along rows (axis=0) and once
    along columns (axis=1) — replicates each pixel into a 2×2 block.
    """
    arr = np.array(image, dtype=np.uint8)
    upscaled_axis0 = np.repeat(arr, 2, axis=0)
    upscaled = np.repeat(upscaled_axis0, 2, axis=1)
    return upscaled.tolist()


def image_upscaling_2x_loop(image: list[list[int]]) -> list[list[int]]:
    """
    Upscale a grayscale image by a factor of 2 using explicit loops.

    Solution: for each source pixel at (row, col), write its value to the
    four corresponding positions in the output: (2r, 2c), (2r, 2c+1),
    (2r+1, 2c), (2r+1, 2c+1).
    """
    image_height = len(image)
    image_width = len(image[0]) if image_height else 0
    upscaled_height = image_height * 2
    upscaled_width = image_width * 2
    image_output = [
        [0 for _ in range(upscaled_width)] for _ in range(upscaled_height)
    ]
    for row in range(image_height):
        for col in range(image_width):
            pixel_value = image[row][col]
            image_output[row * 2][col * 2] = pixel_value
            image_output[row * 2][col * 2 + 1] = pixel_value
            image_output[row * 2 + 1][col * 2] = pixel_value
            image_output[row * 2 + 1][col * 2 + 1] = pixel_value
    return image_output


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])

    outputs = {
        "baboon_2x.png": image_upscaling_2x(image),
        "baboon_4x.png": image_upscaling_4x_vectorized(image),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "baboon_1x.png": input_dir / "baboon_monocromatica.png",
        "baboon_2x.png": output_dir / "baboon_2x.png",
        "baboon_4x.png": output_dir / "baboon_4x.png",
    }


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
        "image_upscaling_2x": benchmark_function(
            image_upscaling_2x,
            image,
            repeats=repeats,
            warmup=warmup,
        ),
        "image_upscaling_2x_loop": benchmark_function(
            image_upscaling_2x_loop,
            image,
            repeats=repeats,
            warmup=warmup,
        ),
        "image_upscaling_4x_vectorized": benchmark_function(
            image_upscaling_4x_vectorized,
            image,
            repeats=repeats,
            warmup=warmup,
        ),
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
