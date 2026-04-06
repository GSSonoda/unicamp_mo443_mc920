"""
1.7 Color Alteration — Old Photograph Effect
=============================================
Simulate the look of old photographs by applying a linear color
transformation to each pixel via the matrix:

  R' = 0.393R + 0.769G + 0.189B
  G' = 0.349R + 0.686G + 0.168B
  B' = 0.272R + 0.534G + 0.131B

After the transformation, pixel values are clipped to [0, 255].
"""

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
    """
    Apply a 3×3 linear color transformation to an RGB image.

    Solution: for each pixel (R, G, B), compute the new channels by taking
    the dot product of the transformation matrix rows with [R, G, B]. Results
    are cast to int and clipped to [0, 255] to handle values that exceed the
    valid range.
    """
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
