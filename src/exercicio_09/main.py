"""
1.9 Bit Planes
==============
Extract the bit planes of a monochromatic image. The gray level of each pixel
can be expressed as a base-2 polynomial:

  p = a_(m-1)*2^(m-1) + ... + a_1*2^1 + a_0*2^0

Bit plane k is formed by the coefficient a_k of each pixel. For an 8-bit
image, this yields 8 binary planes (planes 0 through 7).
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

EXERCISE_NAME = "exercicio_09"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def image_grayscale_bit_plane(
    image: list[list[int]], plane: int
) -> list[list[int]]:
    """
    Extract a single bit plane from a grayscale image.

    Solution: right-shift each pixel by `plane` bits and mask the LSB with
    `& 1`, yielding 0 or 1. Multiply by 255 to produce a displayable binary
    image (black = 0, white = 255).
    """
    img = [[(pixel >> plane) & 1 for pixel in row] for row in image]
    img = [[pixel * 255 for pixel in row] for row in img]
    return img


def image_grayscale_bit_plane_vectorized(
    image: list[list[int]], plane: int
) -> list[list[int]]:
    """
    Extract a single bit plane using NumPy bitwise operations.

    Right-shifts the entire array by ``plane`` bits, masks the LSB, then
    multiplies by 255 — all as vectorized numpy operations.
    """
    arr = np.array(image, dtype=np.uint8)
    return ((arr >> plane & 1) * 255).tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        f"plano_bit_{plane}.png": image_grayscale_bit_plane(img, plane)
        for plane in range(8)
    }
    return save_grayscale_outputs(output_dir, outputs)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    files: dict[str, Path] = {
        "baboon_monocromatica.png": input_dir / "baboon_monocromatica.png",
    }
    for plane in range(8):
        name = f"plano_bit_{plane}.png"
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
    image = load_grayscale_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0
    plane = 7

    benchmarks = {
        "bit_plane": {
            "loop": benchmark_function(
                image_grayscale_bit_plane,
                image,
                plane,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_grayscale_bit_plane_vectorized,
                image,
                plane,
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
