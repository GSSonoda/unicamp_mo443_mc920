"""
1.2 Detecção de Transições em Vídeos — Diferenças entre Blocos
==============================================================
Dois quadros são divididos em blocos N×N sem sobreposição. O MSE de cada par
de blocos correspondentes é calculado e testado contra T1. Se o número de
blocos com MSE > T1 exceder T2, o quadro é uma transição abrupta.

Parâmetros:
    BLOCK_SIZE = 16     tamanho do bloco (pixels)
    T1 = 500            limiar de MSE por bloco
    T2_FRACTION = 10%   fração de blocos alterados para considerar transição

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

EXERCISE_NAME = "metodo_11_blocos"
INPUTS = {
    "video": "http://www.ic.unicamp.br/~helio/videos_mp4/toy.mp4",
}
BLOCK_SIZE = 16
T1 = 500.0
T2_FRACTION = 0.10


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
    # Plota a série temporal da métrica (blocos com MSE > T1 por quadro)
    ax.plot(
        range(len(metrics)), metrics,
        color="steelblue", linewidth=0.8, label="Métrica",
    )
    # Linha horizontal tracejada no limiar T2 absoluto (número de blocos)
    ax.axhline(
        y=threshold, color="orange", linestyle="--", linewidth=1.0,
        label=f"T2 = {threshold:.0f}",
    )
    # Marca cada transição detectada com uma linha vertical vermelha
    for t in transitions:
        ax.axvline(x=t, color="red", linestyle="--", alpha=0.6, linewidth=0.8)
    ax.set_xlabel("Quadro")
    ax.set_ylabel("Blocos com MSE > T1")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=100)
    plt.close(fig)


def detect_transitions_blocos_loop(
    frames: list[np.ndarray],
    block_size: int = BLOCK_SIZE,
    t1: float = T1,
    t2_fraction: float = T2_FRACTION,
) -> tuple[list[int], list[int]]:
    """Detecção por laços: MSE de blocos calculado com laços Python."""
    h, w = frames[0].shape
    # Número de blocos inteiros em cada dimensão
    bh = h // block_size
    bw = w // block_size
    n_blocks = bh * bw
    # T2 absoluto: número mínimo de blocos afetados para declarar transição
    t2 = t2_fraction * n_blocks
    metrics: list[int] = []

    for i in range(len(frames) - 1):
        count = 0
        for bi in range(bh):
            for bj in range(bw):
                # Coordenadas do canto superior esquerdo do bloco
                r0 = bi * block_size
                c0 = bj * block_size
                b1 = frames[i][
                    r0 : r0 + block_size, c0 : c0 + block_size
                ].astype(np.float64)
                b2 = frames[i + 1][
                    r0 : r0 + block_size, c0 : c0 + block_size
                ].astype(np.float64)
                # MSE entre blocos correspondentes nos dois quadros
                mse = np.mean((b1 - b2) ** 2)
                if mse > t1:
                    count += 1
        metrics.append(count)

    # Quadros onde a contagem de blocos supera T2 são transições
    transitions = [i for i, m in enumerate(metrics) if m > t2]
    return metrics, transitions


def detect_transitions_blocos(
    frames: list[np.ndarray],
    block_size: int = BLOCK_SIZE,
    t1: float = T1,
    t2_fraction: float = T2_FRACTION,
) -> tuple[list[int], list[int]]:
    """Detecção vetorizada: blocos extraídos com reshape e MSE por eixo."""
    h, w = frames[0].shape
    bh = h // block_size
    bw = w // block_size
    n_blocks = bh * bw
    # T2 absoluto: número mínimo de blocos afetados para declarar transição
    t2 = t2_fraction * n_blocks
    metrics: list[int] = []

    for i in range(len(frames) - 1):
        # Recorta a região divisível por block_size (descarta borda residual)
        f1 = frames[i][
            :bh * block_size, :bw * block_size
        ].astype(np.float64)
        f2 = frames[i + 1][
            :bh * block_size, :bw * block_size
        ].astype(np.float64)
        # Reshape: (bh, block_size, bw, block_size) → (n_blocks, block_size²)
        b1 = (
            f1.reshape(bh, block_size, bw, block_size)
            .transpose(0, 2, 1, 3)
            .reshape(n_blocks, -1)
        )
        b2 = (
            f2.reshape(bh, block_size, bw, block_size)
            .transpose(0, 2, 1, 3)
            .reshape(n_blocks, -1)
        )
        # MSE por bloco: média dos quadrados das diferenças ao longo dos pixels
        mse_per_block = np.mean((b1 - b2) ** 2, axis=1)
        metrics.append(int((mse_per_block > t1).sum()))

    # Quadros onde a contagem de blocos supera T2 são transições
    transitions = [i for i, m in enumerate(metrics) if m > t2]
    return metrics, transitions


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    frames = _load_frames_gray(input_paths["video"])
    if not frames:
        raise RuntimeError("Nenhum quadro carregado do vídeo.")

    h, w = frames[0].shape
    bh = h // BLOCK_SIZE
    bw = w // BLOCK_SIZE
    # T2 em número absoluto de blocos
    t2 = T2_FRACTION * bh * bw
    metrics, transitions = detect_transitions_blocos(
        frames, BLOCK_SIZE, T1, T2_FRACTION
    )

    print(f"[info] Quadros processados: {len(frames)}")
    print(
        f"[info] Transições detectadas: {len(transitions)}"
        f" (quadros: {transitions})"
    )

    output_path = output_dir / "blocos_transicoes.png"
    _save_metric_plot(
        metrics, transitions, t2, output_path, "Diferenças entre Blocos"
    )
    return [output_path]


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    return {
        "blocos_transicoes.png": output_dir / "blocos_transicoes.png",
    }


def run_benchmarks(
    repeats: int = 3,
    warmup: int = 1,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
    frames = _load_frames_gray(input_paths["video"])

    benchmarks = {
        "detect_transitions_blocos": {
            "loop": benchmark_function(
                detect_transitions_blocos_loop,
                frames, BLOCK_SIZE, T1, T2_FRACTION,
                repeats=repeats, warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                detect_transitions_blocos,
                frames, BLOCK_SIZE, T1, T2_FRACTION,
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
            "params": {
                "block_size": BLOCK_SIZE, "t1": T1, "t2_fraction": T2_FRACTION
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
