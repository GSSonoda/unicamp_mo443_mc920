import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import load_rgb_image, save_rgb_outputs
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_07"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/watch.png",
}
TRANSFORMATION_MATRIX = [
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131],
]


def image_color_transform(
    image: list[list[tuple[int, int, int]]],
    transform_matrix: list[list[float]] = TRANSFORMATION_MATRIX,
) -> list[list[tuple[int, int, int]]]:
    output_image = [[(0, 0, 0)] * len(image[0]) for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            r, g, b = image[i][j]
            new_r = int(
                transform_matrix[0][0] * r
                + transform_matrix[0][1] * g
                + transform_matrix[0][2] * b
            )
            new_g = int(
                transform_matrix[1][0] * r
                + transform_matrix[1][1] * g
                + transform_matrix[1][2] * b
            )
            new_b = int(
                transform_matrix[2][0] * r
                + transform_matrix[2][1] * g
                + transform_matrix[2][2] * b
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
        "whatch_transformed.png": transformed_img,
    }
    return save_rgb_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
