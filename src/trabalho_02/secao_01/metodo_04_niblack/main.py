"""
1.1 Limiarização Global e Local — Método de Niblack
====================================================
O valor de limiar em um pixel (x, y) é calculado como:

    T(x, y) = mu(x, y) + k * sigma(x, y)

onde mu(x, y) e sigma(x, y) são a média e o desvio padrão em uma vizinhança
local de (x, y). k é usado para ajustar a fração da borda do objeto.

Entrada:  imagem PGM monocromática
Saída:    imagem PNG binária
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import numpy as np
from scipy.ndimage import uniform_filter

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_04_niblack"
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
N = 15
K = -0.2


def threshold_niblack_loop(
    image: list[list[int]], n: int = N, k: float = K
) -> list[list[int]]:
    """Niblack com janela deslizante em laços Python."""
    img = np.array(image, dtype=np.float64)
    h, w = img.shape
    pad = n // 2
    # Expande bordas para que a janela caiba em todos os pixels
    padded = np.pad(img, pad, mode="edge")
    result = np.empty((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            window = padded[i : i + n, j : j + n]
            mu = window.mean()
            sigma = window.std()
            # Limiar local: média + k * desvio padrão
            t = mu + k * sigma
            result[i, j] = 0 if img[i, j] > t else 255
    return result.tolist()


def threshold_niblack(
    image: list[list[int]], n: int = N, k: float = K
) -> list[list[int]]:
    """Niblack vetorizado com scipy uniform_filter.

    Variância local: Var = E[X²] - E[X]², evitando laços sobre a imagem.
    """
    img = np.array(image, dtype=np.float64)
    # Média local por filtro de média uniforme
    mu = uniform_filter(img, size=n, mode="nearest")
    # E[X²] calculado com filtro uniforme sobre os quadrados
    mu2 = uniform_filter(img ** 2, size=n, mode="nearest")
    # Desvio padrão local: sqrt(Var), clampado em 0 para evitar NaN
    sigma = np.sqrt(np.maximum(mu2 - mu ** 2, 0.0))
    # Limiar local de Niblack: T = mu + k * sigma
    t = mu + k * sigma
    return np.where(img > t, 0, 255).astype(np.uint8).tolist()


def _threshold_niblack_map(
    image: list[list[int]], n: int = N, k: float = K
) -> np.ndarray:
    """Retorna o mapa de limiares locais (para visualização no histograma)."""
    img = np.array(image, dtype=np.float64)
    mu = uniform_filter(img, size=n, mode="nearest")
    mu2 = uniform_filter(img ** 2, size=n, mode="nearest")
    sigma = np.sqrt(np.maximum(mu2 - mu ** 2, 0.0))
    return mu + k * sigma


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
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=100)
    plt.close(fig)


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    saved = []
    for stem, img_path in input_paths.items():
        # Carrega a imagem em escala de cinza como lista de listas
        image = load_grayscale_image(img_path)
        # Binariza com Niblack e obtém a média do mapa de limiares locais
        binary = threshold_niblack(image, N, K)
        t_map = _threshold_niblack_map(image, N, K)
        threshold_val = float(t_map.mean())

        # Salva original e binarizada
        saved += save_grayscale_outputs(output_dir, {
            f"niblack_{stem}_original.png": image,
            f"niblack_{stem}_binaria.png": binary,
        })

        # Salva histograma com a média dos limiares locais
        hist_path = output_dir / f"niblack_{stem}_histograma.png"
        _save_histogram(
            image, binary, threshold_val, hist_path,
            f"Niblack — {stem}",
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
        files[f"niblack_{stem}_original.png"] = (
            output_dir / f"niblack_{stem}_original.png"
        )
        files[f"niblack_{stem}_binaria.png"] = (
            output_dir / f"niblack_{stem}_binaria.png"
        )
        files[f"niblack_{stem}_histograma.png"] = (
            output_dir / f"niblack_{stem}_histograma.png"
        )
    return files


def run_benchmarks(
    repeats: int = 5,
    warmup: int = 1,
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
        "threshold_niblack": {
            "loop": benchmark_function(
                threshold_niblack_loop, image, N, K,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                threshold_niblack, image, N, K,
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
            "params": {"n": N, "k": K},
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
