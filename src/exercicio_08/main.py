import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import load_rgb_image, save_rgb_outputs
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_08"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/watch.png",
}
RED_TRANSFORM = [0.393, 0.769, 0.189]
GREEN_TRANSFORM = [0.349, 0.686, 0.168]
BLUE_TRANSFORM = [0.272, 0.534, 0.131]


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


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_rgb_image(input_paths["imagem"])
    transformed_img = image_color_transform(img)

    outputs = {
        "watch_transformed.png": transformed_img,
    }
    return save_rgb_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
