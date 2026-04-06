import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_09"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}
"""
Extrair os planos de bits de uma imagem monocrom´atica. Os n´ ıveis de cinza de uma imagem
monocrom´ atica com m bits podem ser representados na forma de um polinˆomio de base 2:
am−1 2m−1 +am−2 2m−2 +...+a1 21 +a0 20
(1)
Oplano de bits de ordem 0 ´ e formado pelos coeficientes a0 de cada pixel, enquanto o plano de
bits de ordem m−1 ´ e formado pelos coeficientes am−1.
"""


def image_grayscale_bit_plane(
    image: list[list[int]], plane: int
) -> list[list[int]]:
    img = [[(pixel >> plane) & 1 for pixel in row] for row in image]
    img = [[pixel * 255 for pixel in row] for row in img]
    return img


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        f"plano_bit_{plane}.png": image_grayscale_bit_plane(img, plane)
        for plane in range(8)
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
