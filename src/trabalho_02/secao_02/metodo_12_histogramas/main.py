"""
1.2 Detecção de Transições em Vídeos — Diferenças entre Histogramas
===================================================================
A diferença D_i dos histogramas de intensidade para dois quadros consecutivos:

    D_i = sum_{j=1}^{B} |H_i(j) - H_{i+1}(j)|

Um limiar adaptativo é estimado como:

    T = mu + alpha * sigma

onde mu e sigma são o valor médio e o desvio padrão da série D_i.
Valores sugeridos: B = 256, alpha = 4.

Entrada:  vídeo MP4
Saída:    gráfico PNG da métrica por quadro
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import numpy as np

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_12_histogramas"
INPUTS = {
    "video": "http://www.ic.unicamp.br/~helio/videos_mp4/toy.mp4",
}
BINS = 256
ALPHA = 4.0


def _load_frames_gray(video_path: Path) -> list[np.ndarray]:
    try:
        import cv2
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "OpenCV não encontrado. Instale com: pip install opencv-python"
        ) from exc
    # Abre o arquivo de vídeo com OpenCV
    cap = cv2.VideoCapture(str(video_path))
    frames: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        import cv2 as _cv2
        # Converte cada quadro de BGR para escala de cinza
        frames.append(_cv2.cvtColor(frame, _cv2.COLOR_BGR2GRAY))
    cap.release()
    return frames


def _save_metric_plot(
    metrics: list[float],
    transitions: list[int],
    threshold: float,
    output_path: Path,
    title: str,
) -> None:
    import matplotlib
    matplotlib.use("Agg")  # backend sem display para salvar em arquivo
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 4))
    # Plota a série temporal da métrica D_i (diferença de histogramas)
    ax.plot(
        range(len(metrics)), metrics,
        color="steelblue", linewidth=0.8, label="D_i",
    )
    # Linha horizontal no limiar adaptativo T = mu + alpha*sigma
    ax.axhline(
        y=threshold, color="orange", linestyle="--", linewidth=1.0,
        label=f"T = {threshold:.1f}",
    )
    # Marca cada transição detectada com uma linha vertical vermelha
    for t in transitions:
        ax.axvline(x=t, color="red", linestyle="--", alpha=0.6, linewidth=0.8)
    ax.set_xlabel("Quadro")
    ax.set_ylabel("Diferença de histograma")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=100)
    plt.close(fig)


def detect_transitions_histogramas_loop(
    frames: list[np.ndarray], bins: int = BINS, alpha: float = ALPHA
) -> tuple[list[float], list[int], float]:
    """Detecção por laços: histograma calculado bin a bin."""
    hists: list[list[float]] = []
    for frame in frames:
        flat = frame.flatten()
        hist = [0.0] * bins
        # Incrementa o bin correspondente a cada pixel
        for p in flat:
            hist[int(p)] += 1
        total = float(len(flat))
        # Normaliza para obter frequências relativas
        hists.append([h / total for h in hist])

    metrics: list[float] = []
    for i in range(len(frames) - 1):
        # D_i = soma das diferenças absolutas bin a bin
        d = sum(abs(hists[i][j] - hists[i + 1][j]) for j in range(bins))
        metrics.append(d)

    # Limiar adaptativo: mu + alpha * sigma da série D_i
    mu = sum(metrics) / len(metrics)
    sigma = (sum((m - mu) ** 2 for m in metrics) / len(metrics)) ** 0.5
    t = mu + alpha * sigma
    # Quadros onde D_i supera o limiar adaptativo são transições
    transitions = [i for i, m in enumerate(metrics) if m > t]
    return metrics, transitions, t


def detect_transitions_histogramas(
    frames: list[np.ndarray], bins: int = BINS, alpha: float = ALPHA
) -> tuple[list[float], list[int], float]:
    """Detecção vetorizada: histogramas normalizados com np.histogram."""
    # Calcula histograma normalizado (densidade) para cada quadro
    hists = [
        np.histogram(f, bins=bins, range=(0, 256), density=True)[0]
        .astype(np.float64)
        for f in frames
    ]

    metrics: list[float] = []
    for i in range(len(frames) - 1):
        # D_i = L1 entre histogramas consecutivos normalizados
        metrics.append(float(np.sum(np.abs(hists[i] - hists[i + 1]))))

    arr = np.array(metrics)
    # Limiar adaptativo: mu + alpha * sigma da série D_i
    t = float(arr.mean() + alpha * arr.std())
    # Quadros onde D_i supera o limiar adaptativo são transições
    transitions = [i for i, m in enumerate(metrics) if m > t]
    return metrics, transitions, t


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    frames = _load_frames_gray(input_paths["video"])
    if not frames:
        raise RuntimeError("Nenhum quadro carregado do vídeo.")

    metrics, transitions, threshold = detect_transitions_histogramas(
        frames, BINS, ALPHA
    )

    print(f"[info] Quadros processados: {len(frames)}")
    print(f"[info] Limiar estimado: {threshold:.4f}")
    print(
        f"[info] Transições detectadas: {len(transitions)}"
        f" (quadros: {transitions})"
    )

    output_path = output_dir / "histogramas_transicoes.png"
    _save_metric_plot(
        metrics, transitions, threshold, output_path,
        "Diferenças entre Histogramas",
    )
    return [output_path]


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "histogramas_transicoes.png": (
            output_dir / "histogramas_transicoes.png"
        ),
    }


def run_benchmarks(
    repeats: int = 5,
    warmup: int = 1,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
    frames = _load_frames_gray(input_paths["video"])

    benchmarks = {
        "detect_transitions_histogramas": {
            "loop": benchmark_function(
                detect_transitions_histogramas_loop, frames, BINS, ALPHA,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                detect_transitions_histogramas, frames, BINS, ALPHA,
                repeats=repeats, warmup=warmup,
            ),
        },
    }

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "video": {
                "filename": input_paths["video"].name,
                "n_frames": len(frames),
            },
            "params": {"bins": BINS, "alpha": ALPHA},
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
