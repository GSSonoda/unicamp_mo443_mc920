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
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import numpy as np

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "metodo_10_pixels"
INPUTS = {
    "video": "https://www.ic.unicamp.br/~helio/videos_mp4/lisa.mpg",
}
T1 = 30
T2_FRACTION = 0.30


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
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    cap.release()
    return frames


def _save_transition_video(
    frames: list[np.ndarray],
    transitions: list[int],
    output_path: Path,
) -> None:
    """Salva vídeo MP4 com os quadros de transição detectados."""
    try:
        import cv2
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "OpenCV não encontrado. Instale com: pip install opencv-python"
        ) from exc
    if not transitions:
        print("[info] Nenhuma transição detectada; vídeo MP4 não gerado.")
        return
    h, w = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, 25.0, (w, h))
    for idx in transitions:
        writer.write(cv2.cvtColor(frames[idx], cv2.COLOR_GRAY2BGR))
        if idx + 1 < len(frames):
            writer.write(cv2.cvtColor(frames[idx + 1], cv2.COLOR_GRAY2BGR))
    writer.release()
    print(f"[info] Vídeo de transições salvo em: {output_path}")


def _save_metric_plot(
    metrics: list[int],
    transitions: list[int],
    threshold: float,
    output_path: Path,
    title: str,
) -> None:
    import matplotlib
    matplotlib.use("Agg")  # backend sem display para salvar em arquivo
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 4))
    # Plota a série temporal da métrica (pixels alterados por quadro)
    ax.plot(
        range(len(metrics)), metrics,
        color="steelblue", linewidth=0.8, label="Métrica",
    )
    # Linha horizontal tracejada no limiar T2 absoluto
    ax.axhline(
        y=threshold, color="orange", linestyle="--", linewidth=1.0,
        label=f"T2 = {threshold:.0f}",
    )
    # Marca cada transição detectada com uma linha vertical vermelha
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
    # T2 absoluto: número mínimo de pixels para declarar transição
    t2 = t2_fraction * h * w
    metrics: list[int] = []
    for i in range(len(frames) - 1):
        count = 0
        for row in range(h):
            for col in range(w):
                # Conta pixels com diferença de intensidade acima de T1
                if abs(int(frames[i][row, col])
                       - int(frames[i + 1][row, col])) > t1:
                    count += 1
        metrics.append(count)
    # Quadros onde a métrica supera T2 são classificados como transições
    transitions = [i for i, m in enumerate(metrics) if m > t2]
    return metrics, transitions


def detect_transitions_pixels(
    frames: list[np.ndarray], t1: int = T1, t2_fraction: float = T2_FRACTION
) -> tuple[list[int], list[int]]:
    """Detecção vetorizada: diferença absoluta entre frames consecutivos."""
    h, w = frames[0].shape
    # T2 absoluto: número mínimo de pixels para declarar transição
    t2 = t2_fraction * h * w
    metrics: list[int] = []
    for i in range(len(frames) - 1):
        # Diferença absoluta pixel a pixel entre quadros consecutivos
        diff = np.abs(
            frames[i].astype(np.int32) - frames[i + 1].astype(np.int32)
        )
        # Conta quantos pixels ultrapassam o limiar T1
        metrics.append(int((diff > t1).sum()))
    # Quadros onde a métrica supera T2 são classificados como transições
    transitions = [i for i, m in enumerate(metrics) if m > t2]
    return metrics, transitions


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    frames = _load_frames_gray(input_paths["video"])
    if not frames:
        raise RuntimeError("Nenhum quadro carregado do vídeo.")

    h, w = frames[0].shape
    # Converte fração T2 para valor absoluto de pixels
    t2 = T2_FRACTION * h * w
    metrics, transitions = detect_transitions_pixels(frames, T1, T2_FRACTION)

    print(f"[info] Quadros processados: {len(frames)}")
    print(
        f"[info] Transições detectadas: {len(transitions)}"
        f" (quadros: {transitions})"
    )

    plot_path = output_dir / "pixels_transicoes.png"
    _save_metric_plot(metrics, transitions, t2, plot_path, "Diferenças entre Pixels")

    video_path = output_dir / "pixels_transicoes.mp4"
    _save_transition_video(frames, transitions, video_path)

    saved = [plot_path]
    if video_path.exists():
        saved.append(video_path)
    return saved


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
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
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
            "video": {
                "filename": input_paths["video"].name,
                "n_frames": len(frames),
            },
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
