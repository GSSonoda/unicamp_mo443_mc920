"""
1.1 Limiarização Global e Local — Método de Sauvola e Pietaksinen
=================================================================
Melhora o método de Niblack para imagens de documentos com má iluminação.
O limiar em (x, y) é calculado como:

    T(x, y) = mu(x, y) * [1 + k * (sigma(x, y) / R - 1)]

Valores sugeridos: k = 0.5, R = 128.

Entrada:  imagem PGM monocromática
Saída:    imagem PNG binária
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from scipy.ndimage import uniform_filter

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_05_sauvola"
INPUTS = {
    "imagem": "http://www.ic.unicamp.br/~helio/imagens_pgm/baboon.pgm",
}
N = 15
K = 0.5
R = 128.0


def threshold_sauvola_loop(
    image: list[list[int]], n: int = N, k: float = K, r: float = R
) -> list[list[int]]:
    """Sauvola com janela deslizante em laços Python."""
    img = np.array(image, dtype=np.float64)
    h, w = img.shape
    pad = n // 2
    padded = np.pad(img, pad, mode="edge")
    result = np.empty((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            window = padded[i : i + n, j : j + n]
            mu = window.mean()
            sigma = window.std()
            t = mu * (1.0 + k * (sigma / r - 1.0))
            result[i, j] = 0 if img[i, j] > t else 255
    return result.tolist()


def threshold_sauvola(
    image: list[list[int]], n: int = N, k: float = K, r: float = R
) -> list[list[int]]:
    """Sauvola vetorizado com scipy uniform_filter."""
    img = np.array(image, dtype=np.float64)
    mu = uniform_filter(img, size=n, mode="nearest")
    mu2 = uniform_filter(img ** 2, size=n, mode="nearest")
    sigma = np.sqrt(np.maximum(mu2 - mu ** 2, 0.0))
    t = mu * (1.0 + k * (sigma / r - 1.0))
    return np.where(img > t, 0, 255).astype(np.uint8).tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "sauvola_original.png": image,
        "sauvola_binaria.png": threshold_sauvola(image, N, K, R),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "sauvola_original.png": output_dir / "sauvola_original.png",
        "sauvola_binaria.png": output_dir / "sauvola_binaria.png",
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
        "threshold_sauvola": {
            "loop": benchmark_function(
                threshold_sauvola_loop, image, N, K, R,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                threshold_sauvola, image, N, K, R,
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
            "params": {"n": N, "k": K, "r": R},
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
