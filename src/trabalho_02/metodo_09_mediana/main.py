"""
1.1 Limiarização Global e Local — Método da Mediana
====================================================
Seleciona o limiar como a mediana da distribuição local de intensidade.
Se o valor de um pixel (x, y) for maior do que a mediana de sua vizinhança,
o pixel será objeto (preto); caso contrário, fundo (branco).

Entrada:  imagem PGM monocromática
Saída:    imagem PNG binária
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from scipy.ndimage import median_filter

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_09_mediana"
INPUTS = {
    "imagem": "http://www.ic.unicamp.br/~helio/imagens_pgm/baboon.pgm",
}
N = 15


def threshold_mediana_loop(image: list[list[int]], n: int = N) -> list[list[int]]:
    """Método da mediana com janela deslizante em laços Python."""
    img = np.array(image, dtype=np.float64)
    h, w = img.shape
    pad = n // 2
    padded = np.pad(img, pad, mode="edge")
    result = np.empty((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            window = padded[i : i + n, j : j + n]
            t = np.median(window)
            result[i, j] = 0 if img[i, j] > t else 255
    return result.tolist()


def threshold_mediana(image: list[list[int]], n: int = N) -> list[list[int]]:
    """Método da mediana vetorizado com scipy median_filter."""
    img = np.array(image, dtype=np.float64)
    t = median_filter(img, size=n, mode="nearest")
    return np.where(img > t, 0, 255).astype(np.uint8).tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "mediana_original.png": image,
        "mediana_binaria.png": threshold_mediana(image, N),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "mediana_original.png": output_dir / "mediana_original.png",
        "mediana_binaria.png": output_dir / "mediana_binaria.png",
    }


def run_benchmarks(
    repeats: int = 5,
    warmup: int = 1,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    image = load_grayscale_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks = {
        "threshold_mediana": {
            "loop": benchmark_function(
                threshold_mediana_loop, image, N,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                threshold_mediana, image, N,
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
            "params": {"n": N},
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
