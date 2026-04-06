import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_10"
INPUTS = {
    "baboon": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
    "butterfly": "https://www.ic.unicamp.br/~helio/imagens_png/butterfly.png",
}

"""
1.10 Combinac¸˜ao de Imagens
Combinar duas imagens monocrom´aticas de mesmo tamanho por meio da m´edia ponderada de
seus n´ıveis de cinza.
"""


def image_combination(
    image1: list[list[int]],
    image2: list[list[int]],
    weight1: float = 0.5,
    weight2: float = 0.5,
) -> list[list[int]]:
    output_image = [[0] * len(image1[0]) for _ in range(len(image1))]
    for i in range(len(image1)):
        for j in range(len(image1[0])):
            output_image[i][j] = int(
                weight1 * image1[i][j] + weight2 * image2[i][j]
            )
    return output_image


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    baboon = load_grayscale_image(input_paths["baboon"])
    butterfly = load_grayscale_image(input_paths["butterfly"])

    outputs = {
        f"combination_{weight1}_{weight2}.png": image_combination(
            baboon, butterfly, weight1, weight2
        )
        for weight1, weight2 in [(0.5, 0.5), (0.7, 0.3), (0.3, 0.7)]
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
