import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_rgb_image,
    save_grayscale_outputs,
    save_rgb_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_08"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/watch.png",
}

"""
(a) Dada uma imagemcolorida no formatoRGB, alterar a imagemconforme as seguintes
operac¸˜oes:
R’=0.393R+0.769G+0.189B
G’=0.349R+0.686G+0.168B
B’=0.272R+0.534G+0.131B
"""
RED_TRANSFORM = [0.393, 0.769, 0.189]
GREEN_TRANSFORM = [0.349, 0.686, 0.168]
BLUE_TRANSFORM = [0.272, 0.534, 0.131]

"""
(b) Dada uma imagem colorida no formato RGB, alterar a imagem tal que ela contenha apenas
uma banda de cor, cujos valores s˜ ao calculados pela m´ edia ponderada:
I = 0.2989R+0.5870G+0.1140B
"""
TRANSFORM_RGB = [0.2989, 0.5870, 0.1140]


def image_color_transform(
    image: list[list[tuple[int, int, int]]],
    red_transform: list[float] = RED_TRANSFORM,
    green_transform: list[float] = GREEN_TRANSFORM,
    blue_transform: list[float] = BLUE_TRANSFORM,
) -> list[list[tuple[int, int, int]]]:
    output_image = [[(0, 0, 0)] * len(image[0]) for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            r, g, b = image[i][j]
            new_r = int(
                red_transform[0] * r
                + red_transform[1] * g
                + red_transform[2] * b
            )
            new_g = int(
                green_transform[0] * r
                + green_transform[1] * g
                + green_transform[2] * b
            )
            new_b = int(
                blue_transform[0] * r
                + blue_transform[1] * g
                + blue_transform[2] * b
            )
            output_image[i][j] = (
                min(new_r, 255),
                min(new_g, 255),
                min(new_b, 255),
            )
    return output_image


def image_to_grayscale(
    image: list[list[tuple[int, int, int]]],
    weights: list[float] = TRANSFORM_RGB,
) -> list[list[int]]:
    return [
        [
            min(int(weights[0] * r + weights[1] * g + weights[2] * b), 255)
            for r, g, b in row
        ]
        for row in image
    ]


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_rgb_image(input_paths["imagem"])
    transformed_img = image_color_transform(img)
    grayscale_img = image_to_grayscale(img)

    saved = save_rgb_outputs(
        output_dir, {"watch_transformed.png": transformed_img}
    )
    saved += save_grayscale_outputs(
        output_dir, {"watch_grayscale.png": grayscale_img}
    )
    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
