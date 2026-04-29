"""
1.2 Detecção de Transições em Vídeos — Diferenças entre Pixels
==============================================================
Dois quadros consecutivos são considerados significativamente diferentes se
a contagem de pixels com variação de intensidade superior a T1 exceder T2.

Parâmetros:
    T1 = 30    tolerância de intensidade por pixel
    T2 = 5 %   fração mínima de pixels alterados para considerar transição

Entrada:  vídeo MP4
Saída:    gráfico PNG da métrica por quadro
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_10_pixels"
INPUTS = {
    "video": "http://www.ic.unicamp.br/~helio/videos_mp4/Buster_Keaton.mp4",
}
T1 = 30
T2_FRACTION = 0.05


def _load_frames_gray(video_path: Path) -> list[np.ndarray]:
    try:
        import cv2
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "OpenCV não encontrado. Instale com: pip install opencv-python"
        ) from exc
    cap = cv2.VideoCapture(str(video_path))
    frames: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        import cv2 as _cv2
        frames.append(_cv2.cvtColor(frame, _cv2.COLOR_BGR2GRAY))
    cap.release()
    return frames


def _save_metric_plot(
    metrics: list[int],
    transitions: list[int],
    threshold: float,
    output_path: Path,
    title: str,
) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(range(len(metrics)), metrics, color="steelblue", linewidth=0.8, label="Métrica")
    ax.axhline(y=threshold, color="orange", linestyle="--", linewidth=1.0, label=f"T2 = {threshold:.0f}")
    for t in transitions:
        ax.axvline(x=t, color="red", linestyle="--", alpha=0.6, linewidth=0.8)
    ax.set_xlabel("Quadro")
    ax.set_ylabel("Pixels alterados")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=100)
    plt.close(fig)


def detect_transitions_pixels_loop(
    frames: list[np.ndarray], t1: int = T1, t2_fraction: float = T2_FRACTION
) -> tuple[list[int], list[int]]:
    """Detecção por laços Python: compara pixels consecutivos."""
    h, w = frames[0].shape
    t2 = t2_fraction * h * w
    metrics: list[int] = []
    for i in range(len(frames) - 1):
        count = 0
        for row in range(h):
            for col in range(w):
                if abs(int(frames[i][row, col]) - int(frames[i + 1][row, col])) > t1:
                    count += 1
        metrics.append(count)
    transitions = [i for i, m in enumerate(metrics) if m > t2]
    return metrics, transitions


def detect_transitions_pixels(
    frames: list[np.ndarray], t1: int = T1, t2_fraction: float = T2_FRACTION
) -> tuple[list[int], list[int]]:
    """Detecção vetorizada: diferença absoluta entre frames consecutivos."""
    h, w = frames[0].shape
    t2 = t2_fraction * h * w
    metrics: list[int] = []
    for i in range(len(frames) - 1):
        diff = np.abs(frames[i].astype(np.int32) - frames[i + 1].astype(np.int32))
        metrics.append(int((diff > t1).sum()))
    transitions = [i for i, m in enumerate(metrics) if m > t2]
    return metrics, transitions


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    frames = _load_frames_gray(input_paths["video"])
    if not frames:
        raise RuntimeError("Nenhum quadro carregado do vídeo.")

    h, w = frames[0].shape
    t2 = T2_FRACTION * h * w
    metrics, transitions = detect_transitions_pixels(frames, T1, T2_FRACTION)

    print(f"[info] Quadros processados: {len(frames)}")
    print(f"[info] Transições detectadas: {len(transitions)} (quadros: {transitions})")

    output_path = output_dir / "pixels_transicoes.png"
    _save_metric_plot(metrics, transitions, t2, output_path, "Diferenças entre Pixels")
    return [output_path]


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "pixels_transicoes.png": output_dir / "pixels_transicoes.png",
    }


def run_benchmarks(
    repeats: int = 5,
    warmup: int = 1,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    frames = _load_frames_gray(input_paths["video"])

    benchmarks = {
        "detect_transitions_pixels": {
            "loop": benchmark_function(
                detect_transitions_pixels_loop, frames, T1, T2_FRACTION,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                detect_transitions_pixels, frames, T1, T2_FRACTION,
                repeats=repeats, warmup=warmup,
            ),
        },
    }

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "video": {"filename": input_paths["video"].name, "n_frames": len(frames)},
            "params": {"t1": T1, "t2_fraction": T2_FRACTION},
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
