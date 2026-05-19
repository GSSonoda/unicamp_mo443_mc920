"""
Trabalho 3 — Transformada de Fourier Bidimensional
Análise 1: Espectro de Magnitude e Histograma Angular de Energia
================================================================
Para cada imagem de entrada:
  1. Calcula a transformada de Fourier 2D e o espectro de magnitude.
  2. Exibe o espectro em escala logarítmica como imagem colorida.
  3. Constrói o histograma angular de energia do espectro centrado.
  4. Identifica as direções dominantes e as sobrepõe ao espectro.

Entrada:  imagens PGM monocromáticas
Saída:    imagens PNG (original, espectro, histograma, orientações dominantes)
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

EXERCISE_NAME = "analise_01_espectro_histograma"
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

N_BINS = 36  # número de bins no histograma angular (cada bin abrange 5°)
N_TOP = 3    # número de orientações dominantes a identificar


# ---------------------------------------------------------------------------
# TODO 1: Transformada de Fourier e espectro de magnitude
# ---------------------------------------------------------------------------

def compute_fft_magnitude_spectrum(image: list[list[int]]) -> np.ndarray:
    """Calcula o espectro de magnitude da FFT 2D, centrado na baixa frequência.

    Passos esperados:
      1. Converter a imagem para array NumPy float64.
      2. Aplicar a FFT 2D: use np.fft.fft2().
      3. Centralizar o espectro (componente DC no centro): use np.fft.fftshift().
      4. Calcular a magnitude: use np.abs().
      5. Retornar o array 2D de magnitudes (float64, mesmas dimensões da entrada).

    Returns:
        np.ndarray: espectro de magnitude 2D, shape (H, W), dtype float64.
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar compute_fft_magnitude_spectrum — "
        "use np.fft.fft2() + np.fft.fftshift() + np.abs()"
    )


def compute_log_spectrum(magnitude: np.ndarray) -> np.ndarray:
    """Aplica a transformação logarítmica ao espectro de magnitude.

    Fórmula:  log_spectrum = log(1 + magnitude)

    O +1 evita log(0) para pixels com magnitude zero.

    Returns:
        np.ndarray: espectro em escala logarítmica (float64).
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar compute_log_spectrum — use np.log1p(magnitude)"
    )


# ---------------------------------------------------------------------------
# TODO 2: Histograma angular de energia
# ---------------------------------------------------------------------------

def compute_angular_histogram(
    log_spectrum: np.ndarray,
    n_bins: int = N_BINS,
) -> np.ndarray:
    """Constrói o histograma angular de energia do espectro centrado.

    Algoritmo esperado:
      1. Determinar o centro do espectro: cy = H // 2, cx = W // 2.
      2. Para cada ponto (row, col) do espectro (exceto o centro):
           dy = row - cy
           dx = col - cx
           theta = np.arctan2(dy, dx)   # em [-pi, pi]
           bin_idx = int((theta + np.pi) / (2 * np.pi) * n_bins) % n_bins
           histogram[bin_idx] += log_spectrum[row, col]
      3. Opcionalmente, ignorar uma região circular de raio mínimo ao centro
         para descartar as baixas frequências muito dominantes.

    Args:
        log_spectrum: espectro em escala logarítmica, centrado, shape (H, W).
        n_bins: número de bins angulares (padrão 36 → cada bin abrange 10°).

    Returns:
        np.ndarray: vetor 1D de tamanho n_bins com a energia por direção.
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar compute_angular_histogram — "
        "use np.arctan2() para calcular os ângulos e acumule as magnitudes por bin"
    )


def identify_dominant_orientations(
    histogram: np.ndarray,
    n_top: int = N_TOP,
) -> list[float]:
    """Identifica as orientações (ângulos) com maior energia no histograma.

    Converte os índices dos bins mais energéticos para ângulos em radianos,
    usando o centro de cada bin:
        angle = -pi + (bin_idx + 0.5) / n_bins * 2 * pi

    Args:
        histogram: vetor de energia por bin angular, shape (n_bins,).
        n_top: número de orientações dominantes a retornar.

    Returns:
        list[float]: ângulos (em radianos) das orientações dominantes,
                     do mais energético ao menos energético.
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar identify_dominant_orientations — "
        "use np.argsort(histogram)[::-1][:n_top] para encontrar os bins mais energéticos"
    )


# ---------------------------------------------------------------------------
# Visualizações (infraestrutura pronta — não precisa modificar)
# ---------------------------------------------------------------------------

def _save_spectrum_image(log_spectrum: np.ndarray, path: Path) -> None:
    """Salva o espectro logarítmico como imagem colorida (colormap 'inferno')."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    vmax = np.percentile(log_spectrum, 99)
    ax.imshow(log_spectrum, cmap="inferno", vmin=0, vmax=vmax)
    ax.set_title("espectro (log)")
    ax.axis("off")
    plt.tight_layout(pad=0.5)
    plt.savefig(str(path), dpi=100, bbox_inches="tight")
    plt.close(fig)


def _save_angular_histogram(
    histogram: np.ndarray,
    path: Path,
) -> None:
    """Salva o histograma angular de energia como gráfico de linhas."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(histogram)
    ax.set_xlabel("bin angular")
    ax.set_ylabel("energia")
    ax.set_title("histograma angular")
    plt.tight_layout()
    plt.savefig(str(path), dpi=100)
    plt.close(fig)


def _save_dominant_orientations(
    log_spectrum: np.ndarray,
    dominant_angles: list[float],
    path: Path,
) -> None:
    """Salva o espectro com linhas sobrepostas indicando as orientações dominantes."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    h, w = log_spectrum.shape
    cy, cx = h // 2, w // 2
    half = min(h, w) // 2 - 5

    fig, ax = plt.subplots(figsize=(5, 5))
    vmax = np.percentile(log_spectrum, 99)
    ax.imshow(log_spectrum, cmap="inferno", vmin=0, vmax=vmax)
    ax.set_title("orientações dominantes")

    for angle in dominant_angles:
        dx = np.cos(angle) * half
        dy = np.sin(angle) * half
        ax.plot(
            [cx - dx, cx + dx],
            [cy - dy, cy + dy],
            color="cyan",
            linewidth=1.5,
        )

    ax.axis("off")
    plt.tight_layout(pad=0.5)
    plt.savefig(str(path), dpi=100, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    saved: list[Path] = []
    for stem, img_path in input_paths.items():
        image = load_grayscale_image(img_path)

        # Salva cópia da imagem original para o relatório
        saved += save_grayscale_outputs(output_dir, {
            f"fourier_{stem}_original.png": image,
        })

        try:
            # TODO 1: preencha compute_fft_magnitude_spectrum e compute_log_spectrum
            magnitude = compute_fft_magnitude_spectrum(image)
            log_spectrum = compute_log_spectrum(magnitude)

            _save_spectrum_image(
                log_spectrum,
                output_dir / f"fourier_{stem}_espectro_log.png",
            )
            saved.append(output_dir / f"fourier_{stem}_espectro_log.png")

            # TODO 2: preencha compute_angular_histogram e identify_dominant_orientations
            histogram = compute_angular_histogram(log_spectrum, n_bins=N_BINS)
            dominant_angles = identify_dominant_orientations(histogram, n_top=N_TOP)

            _save_angular_histogram(
                histogram,
                output_dir / f"fourier_{stem}_histograma_angular.png",
            )
            saved.append(output_dir / f"fourier_{stem}_histograma_angular.png")

            _save_dominant_orientations(
                log_spectrum,
                dominant_angles,
                output_dir / f"fourier_{stem}_orientacoes_dominantes.png",
            )
            saved.append(output_dir / f"fourier_{stem}_orientacoes_dominantes.png")

        except NotImplementedError as exc:
            print(f"[todo] {exc}")

    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    stems = ["baboon", "fiducial", "monarch", "peppers", "retina", "sonnet", "wedge"]
    files: dict[str, Path] = {}
    for stem in stems:
        files[f"fourier_{stem}_original.png"] = (
            output_dir / f"fourier_{stem}_original.png"
        )
        files[f"fourier_{stem}_espectro_log.png"] = (
            output_dir / f"fourier_{stem}_espectro_log.png"
        )
        files[f"fourier_{stem}_histograma_angular.png"] = (
            output_dir / f"fourier_{stem}_histograma_angular.png"
        )
        files[f"fourier_{stem}_orientacoes_dominantes.png"] = (
            output_dir / f"fourier_{stem}_orientacoes_dominantes.png"
        )
    return files


def run_benchmarks(
    repeats: int = 10,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    image = load_grayscale_image(input_paths["baboon"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks: dict = {}
    try:
        magnitude = compute_fft_magnitude_spectrum(image)
        log_spectrum = compute_log_spectrum(magnitude)

        benchmarks["compute_fft_magnitude_spectrum"] = benchmark_function(
            compute_fft_magnitude_spectrum, image,
            repeats=repeats, warmup=warmup,
        )
        benchmarks["compute_log_spectrum"] = benchmark_function(
            compute_log_spectrum, magnitude,
            repeats=repeats, warmup=warmup,
        )
        benchmarks["compute_angular_histogram"] = benchmark_function(
            compute_angular_histogram, log_spectrum,
            repeats=repeats, warmup=warmup,
        )
    except NotImplementedError as exc:
        print(f"[todo] Benchmark nao disponivel: {exc}")

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
            "n_bins": N_BINS,
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
