"""
1.13 Filtragem de Imagens
A ﬁltragem aplicada a uma imagem digital ´e uma operac¸˜ao local que altera os valores de intensi-
dade dos pixels da imagem levando-se em conta tanto o valor do pixel em quest˜ao quanto valores
de pixels vizinhos.
No processo de ﬁltragem, utiliza-se uma operac¸˜ao de convoluc¸˜ao de uma m´ascara pela imagem.
Este processo equivale a percorrer toda a imagem alterando seus valores conforme os pesos da
m´ascara e as intensidades da imagem.
Aplicar os ﬁltros h1 a h11 em uma imagem digital monocrom´atica.
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

EXERCISE_NAME = "exercicio_13"
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
