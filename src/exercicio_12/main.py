"""
1.12 Quantizac¸˜ao de Imagens
Quantizac¸˜ao refere-se ao n´umero de n´ıveis de cinza usados para representar uma imagem mono-
crom´atica. A quantizac¸˜ao est´a relacionada `a profundidade de uma imagem, a qual corresponde ao
n´umero de bits necess´arios para armazenar a imagem. Representar uma imagem com diferentes
n´ıveis de quantizac¸˜ao.
"""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_12"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {}
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
