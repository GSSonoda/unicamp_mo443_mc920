"""
1.12 Image Quantization
=======================
Quantization determines the number of gray levels used to represent a
monochromatic image, and is tied to the bit depth of the image. Represent an
image at different quantization levels: 256, 64, 32, 16, 8, 4, and 2.
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

EXERCISE_NAME = "exercicio_12"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def image_quantization(image: list[list[int]], factor: int) -> list[list[int]]:
    """
    Reduce the number of gray levels in a grayscale image.

    Solution: divide the [0, 255] range into `factor` equal bins of width
    step = 256 // factor. Each pixel is mapped to the lower boundary of its
    bin: p' = (p // step) * step. This preserves the full [0, 255] output
    range while reducing the number of distinct values to `factor`.
    """
    if factor <= 0:
        raise ValueError(
            "O fator de quantização deve ser um inteiro positivo."
        )
    if factor > 256:
        raise ValueError("O fator de quantização não pode ser maior que 256.")
    step = 256 // factor
    quantized_image = []
    for row in image:
        quantized_row = []
        for pixel in row:
            quantized_pixel = (pixel // step) * step
            quantized_row.append(quantized_pixel)
        quantized_image.append(quantized_row)
    return quantized_image


def image_quantization_vectorized(
    image: list[list[int]], factor: int
) -> list[list[int]]:
    """
    Reduce gray levels using NumPy integer arithmetic.

    Identical semantics as ``image_quantization`` but operates on the entire
    array at once with vectorized floor-division and multiplication.
    """
    if factor <= 0:
        raise ValueError(
            "O fator de quantizacao deve ser um inteiro positivo."
        )
    if factor > 256:
        raise ValueError("O fator de quantizacao nao pode ser maior que 256.")
    step = 256 // factor
    arr = np.array(image, dtype=np.uint8)
    return ((arr // step) * step).tolist()


QUANTIZATION_LEVELS = [256, 64, 32, 16, 8, 4, 2]


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "quantizacao_256_niveis.png": image_quantization(img, 256),
        "quantizacao_64_niveis.png": image_quantization(img, 64),
        "quantizacao_32_niveis.png": image_quantization(img, 32),
        "quantizacao_16_niveis.png": image_quantization(img, 16),
        "quantizacao_8_niveis.png": image_quantization(img, 8),
        "quantizacao_4_niveis.png": image_quantization(img, 4),
        "quantizacao_2_niveis.png": image_quantization(img, 2),
    }
    return save_grayscale_outputs(output_dir, outputs)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    files: dict[str, Path] = {
        "baboon_monocromatica.png": input_dir / "baboon_monocromatica.png",
    }
    for level in QUANTIZATION_LEVELS:
        name = f"quantizacao_{level}_niveis.png"
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
    factor = 16

    benchmarks = {
        "quantization": {
            "loop": benchmark_function(
                image_quantization,
                image,
                factor,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_quantization_vectorized,
                image,
                factor,
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
