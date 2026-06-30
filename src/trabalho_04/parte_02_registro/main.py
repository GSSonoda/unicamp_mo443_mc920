"""
Trabalho 4 — Parte 2: Registro de Imagens e Panorama
=====================================================
Para cada par de imagens (foto{N}A, foto{N}B), aplica o pipeline de registro
de ``panorama.py`` com os detectores disponíveis e salva, para o relatório:
imagens originais, linhas de correspondência e a imagem panorâmica.

Entrada:  pares de imagens JPEG
Saída:    imagens JPEG (originais, correspondências e panorama por detector)
          + reg_resultados.json (métricas e matrizes de homografia)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import cv2

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise
from src.trabalho_04.parte_02_registro.panorama import (
    CANDIDATE_DETECTORS,
    available_detectors,
    build_detector,
    build_panorama,
)
from src.trabalho_04.parte_02_registro.panorama import (
    _match_descriptors as match_descriptors,
)

EXERCISE_NAME = "t4_registro_imagens"
REG_BASE = "http://www.ic.unicamp.br/~helio/imagens_registro/"
PAIRS = ["foto1", "foto2", "foto3", "foto4", "foto5"]
INPUTS = {
    f"{pair}{side}": REG_BASE + f"{pair}{side}.jpg"
    for pair in PAIRS
    for side in ("A", "B")
}

# Lado máximo (px); imagens maiores são reduzidas para acelerar a costura.
MAX_SIDE = 1000
RESULTS_JSON = "reg_resultados.json"


def _read_resized(path: Path):
    image = cv2.imread(str(path))
    if image is None:
        return None
    height, width = image.shape[:2]
    longest = max(height, width)
    if longest > MAX_SIDE:
        scale = MAX_SIDE / longest
        image = cv2.resize(
            image,
            (int(round(width * scale)), int(round(height * scale))),
            interpolation=cv2.INTER_AREA,
        )
    return image


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    detectors = available_detectors()
    indisponiveis = [d for d in CANDIDATE_DETECTORS if d not in detectors]
    print(f"[info] Detectores disponiveis: {detectors}")
    if indisponiveis:
        print(f"[info] Detectores indisponiveis neste OpenCV: {indisponiveis}")

    saved: list[Path] = []
    resultados: dict = {"detectores": detectors, "indisponiveis": indisponiveis, "pares": {}}

    for pair in PAIRS:
        img_a = _read_resized(input_paths[f"{pair}A"])
        img_b = _read_resized(input_paths[f"{pair}B"])
        if img_a is None or img_b is None:
            print(f"[aviso] Par {pair} nao pode ser lido; pulando.")
            continue

        path_a = output_dir / f"reg_{pair}_A.jpg"
        path_b = output_dir / f"reg_{pair}_B.jpg"
        cv2.imwrite(str(path_a), img_a)
        cv2.imwrite(str(path_b), img_b)
        saved += [path_a, path_b]

        resultados["pares"][pair] = {}
        for det in detectors:
            try:
                res = build_panorama(img_a, img_b, det)
            except cv2.error as exc:
                print(f"[aviso] {pair}/{det} falhou: {str(exc)[:80]}")
                continue

            resultados["pares"][pair][det] = {
                "keypoints_a": res["keypoints_a"],
                "keypoints_b": res["keypoints_b"],
                "matches": res["matches"],
                "inliers": res["inliers"],
                "inlier_ratio": res["inlier_ratio"],
                "seconds": res["seconds"],
                "homography": res["homography"],
                "status": res["status"],
            }

            if res["correspondencias"] is not None:
                corr_path = output_dir / f"reg_{pair}_correspondencias_{det}.jpg"
                cv2.imwrite(str(corr_path), res["correspondencias"])
                saved.append(corr_path)
            if res["panorama"] is not None:
                pano_path = output_dir / f"reg_{pair}_panorama_{det}.jpg"
                cv2.imwrite(str(pano_path), res["panorama"])
                saved.append(pano_path)

            print(
                f"[ok] {pair}/{det}: matches={res['matches']} "
                f"inliers={res['inliers']} status={res['status']}"
            )

    json_path = output_dir / RESULTS_JSON
    json_path.write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    saved.append(json_path)
    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    """Figuras geradas (apenas imagens existentes em results/)."""
    output_dir = results_dir_for(EXERCISE_NAME)
    files: dict[str, Path] = {}
    for path in sorted(output_dir.glob("reg_*.jpg")):
        files[path.name] = path
    return files


def run_benchmarks(
    repeats: int = 5,
    warmup: int = 1,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    detectors = available_detectors()

    img_a = _read_resized(input_paths["foto1A"])
    img_b = _read_resized(input_paths["foto1B"])
    gray_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)

    benchmarks: dict = {}
    for det in detectors:
        detector, norm = build_detector(det)

        def detect_and_match(detector=detector, norm=norm):
            kp_a, desc_a = detector.detectAndCompute(gray_a, None)
            kp_b, desc_b = detector.detectAndCompute(gray_b, None)
            match_descriptors(desc_a, desc_b, norm, 0.75)

        benchmarks[det] = benchmark_function(
            detect_and_match, repeats=repeats, warmup=warmup
        )

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "pair": "foto1",
            "image": {
                "width": img_a.shape[1],
                "height": img_a.shape[0],
            },
            "detectores": detectors,
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
