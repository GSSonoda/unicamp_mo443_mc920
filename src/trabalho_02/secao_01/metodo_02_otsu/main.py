"""
1.1 Limiarização Global e Local — Método de Otsu
=================================================
Calcula automaticamente um limiar ótimo para dividir a imagem em duas classes
de pixels por meio da minimização da variância intraclasse (equivalente à
maximização da variância interclasse).

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

EXERCISE_NAME = "metodo_02_otsu"
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


def compute_otsu_threshold_loop(image: list[list[int]]) -> int:
    """Calcula o limiar de Otsu iterando sobre todos os candidatos (laços).

    Para cada valor t, calcula a variância interclasse e retorna o t ótimo.
    """
    # Histograma com laços Python
    hist = [0] * 256
    for row in image:
        for pixel in row:
            hist[pixel] += 1

    # Normaliza o histograma para obter probabilidades
    total = sum(hist)
    hist_norm = [h / total for h in hist]

    best_t = 0
    best_sigma = 0.0
    cumsum = 0.0      # peso acumulado da classe 0 (fundo)
    cumsum_w = 0.0    # média ponderada acumulada da classe 0
    mu_total = sum(j * hist_norm[j] for j in range(256))

    for t in range(255):
        cumsum += hist_norm[t]
        cumsum_w += t * hist_norm[t]
        w0 = cumsum        # peso da classe fundo
        w1 = 1.0 - w0      # peso da classe objeto
        if w0 == 0 or w1 == 0:
            continue
        mu0 = cumsum_w / w0                        # média da classe fundo
        mu1 = (mu_total - cumsum_w) / w1           # média da classe objeto
        # Variância interclasse: maximizada no limiar ótimo
        sigma_b = w0 * w1 * (mu0 - mu1) ** 2
        if sigma_b > best_sigma:
            best_sigma = sigma_b
            best_t = t

    return best_t


def compute_otsu_threshold(image: list[list[int]]) -> int:
    """Calcula o limiar de Otsu de forma vetorizada com NumPy."""
    img = np.array(image, dtype=np.uint8)
    # Histograma normalizado: probabilidade de cada nível de intensidade
    hist, _ = np.histogram(img, bins=256, range=(0, 256))
    hist = hist.astype(np.float64) / hist.sum()

    # Somas cumulativas para calcular pesos e médias de cada classe
    cum_w = np.cumsum(hist)
    cum_wmu = np.cumsum(hist * np.arange(256, dtype=np.float64))
    mu_total = cum_wmu[-1]

    # Pesos e médias das duas classes para cada candidato a limiar
    w0 = cum_w[:-1]
    w1 = 1.0 - w0
    mu0 = np.where(w0 > 0, cum_wmu[:-1] / w0, 0.0)
    mu1 = np.where(w1 > 0, (mu_total - cum_wmu[:-1]) / w1, 0.0)
    # Variância interclasse: argmax é o limiar de Otsu
    sigma_b = w0 * w1 * (mu0 - mu1) ** 2

    return int(np.argmax(sigma_b))


def threshold_otsu_loop(image: list[list[int]]) -> list[list[int]]:
    """Otsu com cálculo de limiar por laços."""
    t = compute_otsu_threshold_loop(image)
    # Aplica o limiar calculado: acima → objeto (0), abaixo → fundo (255)
    return [[0 if pixel > t else 255 for pixel in row] for row in image]


def threshold_otsu(image: list[list[int]]) -> list[list[int]]:
    """Otsu vetorizado: limiar calculado com NumPy, binarização com np.where.
    """
    t = compute_otsu_threshold(image)
    img = np.array(image, dtype=np.uint8)
    # Aplica o limiar ótimo de Otsu à imagem inteira
    return np.where(img > t, 0, 255).astype(np.uint8).tolist()


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
        0.98, 0.95, f"T (Otsu) = {threshold_val:.0f}",
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
        # Calcula o limiar ótimo de Otsu e binariza
        t = compute_otsu_threshold(image)
        binary = threshold_otsu(image)

        # Salva original e binarizada
        saved += save_grayscale_outputs(output_dir, {
            f"otsu_{stem}_original.png": image,
            f"otsu_{stem}_binaria.png": binary,
        })

        # Salva histograma com o limiar de Otsu como linha de referência
        hist_path = output_dir / f"otsu_{stem}_histograma.png"
        _save_histogram(
            image, binary, float(t), hist_path,
            f"Otsu — {stem}",
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
        files[f"otsu_{stem}_original.png"] = (
            output_dir / f"otsu_{stem}_original.png"
        )
        files[f"otsu_{stem}_binaria.png"] = (
            output_dir / f"otsu_{stem}_binaria.png"
        )
        files[f"otsu_{stem}_histograma.png"] = (
            output_dir / f"otsu_{stem}_histograma.png"
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
        "compute_threshold": {
            "loop": benchmark_function(
                compute_otsu_threshold_loop, image,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                compute_otsu_threshold, image,
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
