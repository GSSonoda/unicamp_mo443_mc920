"""
1.1 Limiarização Global e Local — Método de Phansalskar, More e Sabale
======================================================================
Variação do método de Sauvola para imagens de baixo contraste. O limiar é:

    T = mu(x,y) * [1 + p*exp(-q*mu(x,y)) + k*(sigma(x,y)/R - 1)]

A imagem é normalizada para [0, 1] antes do cálculo.
Valores sugeridos: k=0.25, R=0.5, p=2, q=10.

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

EXERCISE_NAME = "metodo_06_phansalskar"
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
K = 0.25
R = 0.5
P = 2.0
Q = 10.0


def threshold_phansalskar_loop(
    image: list[list[int]], n: int = N, k: float = K, r: float = R,
    p: float = P, q: float = Q,
) -> list[list[int]]:
    """Phansalskar com janela deslizante em laços Python (normalizada)."""
    # Normaliza para [0, 1] conforme a formulação original do método
    img = np.array(image, dtype=np.float64) / 255.0
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
            # Termo exponencial penaliza regiões escuras (baixo contraste)
            t = mu * (1.0 + p * np.exp(-q * mu) + k * (sigma / r - 1.0))
            result[i, j] = 0 if img[i, j] > t else 255
    return result.tolist()


def threshold_phansalskar(
    image: list[list[int]], n: int = N, k: float = K, r: float = R,
    p: float = P, q: float = Q,
) -> list[list[int]]:
    """Phansalskar vetorizado com scipy uniform_filter (normalizada)."""
    # Normaliza para [0, 1] conforme a formulação original do método
    img = np.array(image, dtype=np.float64) / 255.0
    # Média local e E[X²] via filtro uniforme
    mu = uniform_filter(img, size=n, mode="nearest")
    mu2 = uniform_filter(img ** 2, size=n, mode="nearest")
    # Desvio padrão local clampado para evitar NaN
    sigma = np.sqrt(np.maximum(mu2 - mu ** 2, 0.0))
    # Limiar com termo exponencial para regiões de baixo contraste
    t = mu * (1.0 + p * np.exp(-q * mu) + k * (sigma / r - 1.0))
    return np.where(img > t, 0, 255).astype(np.uint8).tolist()


def _threshold_phansalskar_map(
    image: list[list[int]], n: int = N, k: float = K, r: float = R,
    p: float = P, q: float = Q,
) -> np.ndarray:
    """Retorna mapa de limiares locais em [0,1] escalado para [0,255]."""
    img = np.array(image, dtype=np.float64) / 255.0
    mu = uniform_filter(img, size=n, mode="nearest")
    mu2 = uniform_filter(img ** 2, size=n, mode="nearest")
    sigma = np.sqrt(np.maximum(mu2 - mu ** 2, 0.0))
    # Retorna limiares em escala de pixel [0, 255] para o histograma
    return (mu * (1.0 + p * np.exp(-q * mu) + k * (sigma / r - 1.0))) * 255.0


def _save_histogram(
    original: list[list[int]],
    binary: list[list[int]],
    threshold_val: float,
    output_path: Path,
    title: str,
) -> None:
    """Salva histograma com linha do limiar e anotação de pixels pretos."""
    import matplotlib
    matplotlib.use("Agg")  # backend sem display para salvar em arquivo
    import matplotlib.pyplot as plt

    # Achata a imagem para array 1-D de intensidades
    arr = np.array(original, dtype=np.uint8).ravel()
    bin_arr = np.array(binary, dtype=np.uint8).ravel()
    # Fração de pixels binarizados como preto (objeto)
    black_fraction = float((bin_arr == 0).sum()) / bin_arr.size * 100

    fig, ax = plt.subplots(figsize=(8, 4))
    # Histograma com 256 bins cobrindo [0, 255]
    ax.hist(arr, bins=256, range=(0, 255), color="steelblue", alpha=0.8)
    # Linha vertical na média dos limiares locais (escalada para [0,255])
    ax.axvline(
        x=threshold_val, color="red", linestyle="--", linewidth=1.5,
        label=f"Limiar médio = {threshold_val:.1f}",
    )
    # Anotação com percentual de pixels pretos na imagem binarizada
    ax.text(
        0.98, 0.95, f"Pixels pretos: {black_fraction:.1f}%",
        transform=ax.transAxes, ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    ax.set_xlabel("Intensidade")
    ax.set_ylabel("Frequência")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=100)
    plt.close(fig)


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    saved = []
    for stem, img_path in input_paths.items():
        # Carrega a imagem em escala de cinza como lista de listas
        image = load_grayscale_image(img_path)
        # Binariza com Phansalskar; obtém média do mapa de limiares [0,255]
        binary = threshold_phansalskar(image, N, K, R, P, Q)
        t_map = _threshold_phansalskar_map(image, N, K, R, P, Q)
        threshold_val = float(t_map.mean())

        # Salva original e binarizada
        saved += save_grayscale_outputs(output_dir, {
            f"phansalskar_{stem}_original.png": image,
            f"phansalskar_{stem}_binaria.png": binary,
        })

        # Salva histograma com a média dos limiares locais
        hist_path = output_dir / f"phansalskar_{stem}_histograma.png"
        _save_histogram(
            image, binary, threshold_val, hist_path,
            f"Phansalskar — {stem}",
        )
        saved.append(hist_path)
    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    stems = [
        "baboon", "fiducial", "monarch", "peppers",
        "retina", "sonnet", "wedge",
    ]
    files = {}
    for stem in stems:
        files[f"phansalskar_{stem}_original.png"] = (
            output_dir / f"phansalskar_{stem}_original.png"
        )
        files[f"phansalskar_{stem}_binaria.png"] = (
            output_dir / f"phansalskar_{stem}_binaria.png"
        )
        files[f"phansalskar_{stem}_histograma.png"] = (
            output_dir / f"phansalskar_{stem}_histograma.png"
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
        "threshold_phansalskar": {
            "loop": benchmark_function(
                threshold_phansalskar_loop, image, N, K, R, P, Q,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                threshold_phansalskar, image, N, K, R, P, Q,
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
            "params": {"n": N, "k": K, "r": R, "p": P, "q": Q},
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
