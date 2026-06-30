"""
Trabalho 4 — Parte 1: Transformações Geométricas
=================================================
Para cada imagem de entrada (PNG), aplica escala (ampliação e redução) e
rotação usando os quatro métodos de interpolação implementados em
``geometria.py`` e salva os resultados para comparação no relatório.

Entrada:  imagens PNG (coloridas ou em tons de cinza)
Saída:    imagens PNG (original + transformadas por cada interpolador)
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
from src.trabalho_04.parte_01_transformacoes.geometria import (
    INTERPOLATION_METHODS,
    rotate_image,
    scale_image,
)

EXERCISE_NAME = "t4_transformacoes_geometricas"
PNG_BASE = "http://www.ic.unicamp.br/~helio/imagens_png/"
INPUTS = {
    "baboon":   PNG_BASE + "baboon_colorida.png",
    "butterfly": PNG_BASE + "butterfly.png",
    "city":     PNG_BASE + "city.png",
    "house":    PNG_BASE + "house.png",
    "monalisa": PNG_BASE + "monalisa.png",
    "peppers":  PNG_BASE + "peppers.png",
    "watch":    PNG_BASE + "watch.png",
}

# Parâmetros das transformações exibidas no relatório.
FATOR_AMPLIACAO = 1.8
FATOR_REDUCAO = 0.4
ANGULO_ROTACAO = 30.0


def _load_image(path: Path) -> np.ndarray:
    from PIL import Image

    with Image.open(path) as image:
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")
        return np.asarray(image)


def _save_image(array: np.ndarray, path: Path) -> Path:
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array).save(path)
    return path


def _output_names(stem: str) -> dict[str, str]:
    """Mapa lógico -> nome de arquivo das saídas de uma imagem."""
    names = {"original": f"geo_{stem}_original.png"}
    for method in INTERPOLATION_METHODS:
        names[f"ampliacao_{method}"] = f"geo_{stem}_ampliacao_{method}.png"
        names[f"reducao_{method}"] = f"geo_{stem}_reducao_{method}.png"
        names[f"rotacao_{method}"] = f"geo_{stem}_rotacao_{method}.png"
    return names


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    saved: list[Path] = []
    for stem, img_path in input_paths.items():
        image = _load_image(img_path)
        names = _output_names(stem)

        saved.append(_save_image(image, output_dir / names["original"]))

        for method in INTERPOLATION_METHODS:
            ampliada = scale_image(image, FATOR_AMPLIACAO, method)
            reduzida = scale_image(image, FATOR_REDUCAO, method)
            rotacionada = rotate_image(image, ANGULO_ROTACAO, method)

            saved.append(
                _save_image(
                    ampliada, output_dir / names[f"ampliacao_{method}"]
                )
            )
            saved.append(
                _save_image(
                    reduzida, output_dir / names[f"reducao_{method}"]
                )
            )
            saved.append(
                _save_image(
                    rotacionada, output_dir / names[f"rotacao_{method}"]
                )
            )

    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    files: dict[str, Path] = {}
    for stem in INPUTS:
        for filename in _output_names(stem).values():
            files[filename] = output_dir / filename
    return files


def run_benchmarks(
    repeats: int = 10,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
    image = _load_image(input_paths["baboon"])
    height, width = image.shape[:2]

    benchmarks: dict = {}
    for method in INTERPOLATION_METHODS:
        benchmarks[f"escala_{method}"] = benchmark_function(
            scale_image, image, FATOR_AMPLIACAO, method,
            repeats=repeats, warmup=warmup,
        )
        benchmarks[f"rotacao_{method}"] = benchmark_function(
            rotate_image, image, ANGULO_ROTACAO, method,
            repeats=repeats, warmup=warmup,
        )

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "image": {
                "filename": input_paths["baboon"].name,
                "width": width,
                "height": height,
                "channels": 1 if image.ndim == 2 else image.shape[2],
            },
            "fator_ampliacao": FATOR_AMPLIACAO,
            "angulo_rotacao": ANGULO_ROTACAO,
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
