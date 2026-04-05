import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_06"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}
BLOCK_SORT = [[6, 11, 13, 3], [8, 16, 1, 9], [12, 14, 2, 7], [4, 15, 10, 5]]
MOSAIC_SHAPE = (4, 4)


def mosaic_4x4(
    image: list[list[int]],
    mosaic_shape: tuple[int, int] = MOSAIC_SHAPE,
    block_sort: list[list[int]] = BLOCK_SORT,
) -> list[list[int]]:
    """
    Construct a 4 × 4 block mosaic from a monochromatic image.
    The arrangement of the blocks must follow the numbering shown in figure (c).
    """
    block_height = len(image) // mosaic_shape[0]
    block_width = len(image[0]) // mosaic_shape[1]
    output_image = [[0] * len(image[0]) for _ in range(len(image))]
    for i in range(mosaic_shape[0]):
        for j in range(mosaic_shape[1]):
            block_number = block_sort[i][j]
            block_row = (block_number - 1) // mosaic_shape[1]
            block_col = (block_number - 1) % mosaic_shape[1]
            for k in range(block_height):
                for l in range(block_width):
                    output_image[i * block_height + k][j * block_width + l] = (
                        image[block_row * block_height + k][
                            block_col * block_width + l
                        ]
                    )
    return output_image


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    mosaic = mosaic_4x4(img)

    outputs = {
        "baboon_mosaic.png": mosaic,
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
