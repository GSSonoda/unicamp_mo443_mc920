"""
1.1 Limiarização Global e Local — Método Global
================================================
Se o valor de intensidade de um pixel (x, y) for maior do que um limiar T
(por exemplo, T = 128), o pixel será considerado como pertencente ao objeto
(preto, valor 0); caso contrário, será considerado como fundo (branco, valor 255).

Entrada:  imagem PGM monocromática
Saída:    imagem PNG binária
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_01_global"
INPUTS = {
    "imagem": "http://www.ic.unicamp.br/~helio/imagens_pgm/baboon.pgm",
}
THRESHOLD = 128


def threshold_global_loop(image: list[list[int]], threshold: int = THRESHOLD) -> list[list[int]]:
    """Limiarização global com laços Python.

    Referência não-vetorizada para comparação de desempenho.
    """
    return [[0 if pixel > threshold else 255 for pixel in row] for row in image]


def threshold_global(image: list[list[int]], threshold: int = THRESHOLD) -> list[list[int]]:
    """Limiarização global vetorizada com NumPy.

    pixel > threshold → 0 (objeto/preto)
    pixel <= threshold → 255 (fundo/branco)
    """
    img = np.array(image, dtype=np.uint8)
    return np.where(img > threshold, 0, 255).astype(np.uint8).tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "global_original.png": image,
        "global_binaria.png": threshold_global(image, THRESHOLD),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "global_original.png": output_dir / "global_original.png",
        "global_binaria.png": output_dir / "global_binaria.png",
    }


def run_benchmarks(
    repeats: int = 10,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    image = load_grayscale_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks = {
        "threshold_global": {
            "loop": benchmark_function(
                threshold_global_loop, image, THRESHOLD,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                threshold_global, image, THRESHOLD,
                repeats=repeats, warmup=warmup,
            ),
        },
    }

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "image": {"filename": input_paths["imagem"].name, "width": width, "height": height},
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
