"""
1.1 Limiarização Global e Local — Método do Contraste
=====================================================
Atribui o valor de um pixel como fundo (branco) ou objeto (preto),
dependendo se seu valor está mais próximo do máximo ou mínimo local:

    |p - z_max| <= |p - z_min|  →  fundo (255)
    |p - z_max|  > |p - z_min|  →  objeto (0)

Entrada:  imagem PGM monocromática
Saída:    imagem PNG binária
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from scipy.ndimage import maximum_filter, minimum_filter

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_07_contraste"
INPUTS = {
    "imagem": "http://www.ic.unicamp.br/~helio/imagens_pgm/baboon.pgm",
}
N = 15


def threshold_contraste_loop(image: list[list[int]], n: int = N) -> list[list[int]]:
    """Método do contraste com janela deslizante em laços Python."""
    img = np.array(image, dtype=np.float64)
    h, w = img.shape
    pad = n // 2
    padded = np.pad(img, pad, mode="edge")
    result = np.empty((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            window = padded[i : i + n, j : j + n]
            zmin = window.min()
            zmax = window.max()
            p = img[i, j]
            result[i, j] = 255 if abs(p - zmax) <= abs(p - zmin) else 0
    return result.tolist()


def threshold_contraste(image: list[list[int]], n: int = N) -> list[list[int]]:
    """Método do contraste vetorizado com scipy minimum_filter e maximum_filter."""
    img = np.array(image, dtype=np.float64)
    zmin = minimum_filter(img, size=n, mode="nearest")
    zmax = maximum_filter(img, size=n, mode="nearest")
    result = np.where(np.abs(img - zmax) <= np.abs(img - zmin), 255, 0).astype(np.uint8)
    return result.tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    image = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "contraste_original.png": image,
        "contraste_binaria.png": threshold_contraste(image, N),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "contraste_original.png": output_dir / "contraste_original.png",
        "contraste_binaria.png": output_dir / "contraste_binaria.png",
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
        "threshold_contraste": {
            "loop": benchmark_function(
                threshold_contraste_loop, image, N,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                threshold_contraste, image, N,
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
