"""
1.1 Limiarização Global e Local — Método Global
================================================
Se o valor de intensidade de um pixel (x, y) for maior do que um limiar T
(por exemplo, T = 128), o pixel será considerado como pertencente ao objeto
(preto, valor 0); caso contrário, será considerado como fundo
(branco, valor 255).

Entrada:  imagem PGM monocromática
Saída:    imagem PNG binária
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import numpy as np

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_01_global"
PGM_BASE = "http://www.ic.unicamp.br/~helio/imagens_pgm/"
INPUTS = {
    "baboon":   PGM_BASE + "baboon.pgm",
    "fiducial": PGM_BASE + "fiducial.pgm",
    "monarch":  PGM_BASE + "monarch.pgm",
    "peppers":  PGM_BASE + "peppers.pgm",
    "retina":   PGM_BASE + "retina.pgm",
    "sonnet":   PGM_BASE + "sonnet.pgm",
    "wedge":    PGM_BASE + "wedge.pgm",
}
THRESHOLD = 128


def threshold_global_loop(
    image: list[list[int]], threshold: int = THRESHOLD
) -> list[list[int]]:
    """Limiarização global com laços Python.

    Referência não-vetorizada para comparação de desempenho.
    """
    # Percorre cada pixel: > threshold → objeto (0), senão fundo (255)
    return [
        [0 if pixel > threshold else 255 for pixel in row]
        for row in image
    ]


def threshold_global(
    image: list[list[int]], threshold: int = THRESHOLD
) -> list[list[int]]:
    """Limiarização global vetorizada com NumPy.

    pixel > threshold → 0 (objeto/preto)
    pixel <= threshold → 255 (fundo/branco)
    """
    # Converte para array NumPy para operar sobre toda a imagem de uma vez
    img = np.array(image, dtype=np.uint8)
    # np.where aplica condição elemento a elemento: True → 0, False → 255
    return np.where(img > threshold, 0, 255).astype(np.uint8).tolist()


def _save_histogram(
    original: list[list[int]],
    binary: list[list[int]],
    threshold_val: float,
    output_path: Path,
    title: str,
) -> None:
    """Salva histograma da imagem binarizada com frações de pixels pretos e brancos."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bin_arr = np.array(binary, dtype=np.uint8).ravel()
    n_black = int((bin_arr == 0).sum())
    n_white = int((bin_arr == 255).sum())
    total = bin_arr.size
    frac_black = n_black / total * 100
    frac_white = n_white / total * 100

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(
        [0, 255], [n_black, n_white], width=30,
        color=["#222222", "#eeeeee"], edgecolor="gray",
    )
    ax.text(0,   n_black, f"{frac_black:.1f}%", ha="center", va="bottom",
            fontsize=10, fontweight="bold")
    ax.text(255, n_white, f"{frac_white:.1f}%", ha="center", va="bottom",
            fontsize=10, fontweight="bold")
    ax.set_xlim(-40, 295)
    ax.set_xticks([0, 255])
    ax.set_xticklabels(["0\n(preto)", "255\n(branco)"])
    ax.set_xlabel("Valor do pixel")
    ax.set_ylabel("Pixels")
    ax.set_title(title)
    ax.text(
        0.98, 0.95, f"T = {threshold_val:.0f}",
        transform=ax.transAxes, ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=100)
    plt.close(fig)


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    saved = []
    for stem, img_path in input_paths.items():
        # Carrega a imagem em escala de cinza como lista de listas
        image = load_grayscale_image(img_path)
        # Aplica limiarização global com limiar fixo THRESHOLD
        binary = threshold_global(image, THRESHOLD)

        # Salva original e binarizada
        saved += save_grayscale_outputs(output_dir, {
            f"global_{stem}_original.png": image,
            f"global_{stem}_binaria.png": binary,
        })

        # Salva histograma com linha do limiar fixo
        hist_path = output_dir / f"global_{stem}_histograma.png"
        _save_histogram(
            image, binary, float(THRESHOLD), hist_path,
            f"Global — {stem}",
        )
        saved.append(hist_path)
    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    stems = [
        "baboon", "fiducial", "monarch", "peppers", "retina", "sonnet", "wedge"
    ]
    files = {}
    for stem in stems:
        files[f"global_{stem}_original.png"] = (
            output_dir / f"global_{stem}_original.png"
        )
        files[f"global_{stem}_binaria.png"] = (
            output_dir / f"global_{stem}_binaria.png"
        )
        files[f"global_{stem}_histograma.png"] = (
            output_dir / f"global_{stem}_histograma.png"
        )
    return files


def run_benchmarks(
    repeats: int = 10,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
    # Usa apenas baboon para o benchmark (imagem de referência)
    image = load_grayscale_image(input_paths["baboon"])
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
            "image": {
                "filename": input_paths["baboon"].name,
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
