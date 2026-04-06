"""
1.6 Mosaic
==========
Construct a 4×4 block mosaic from a monochromatic image. The arrangement of
the blocks follows the numbering defined in BLOCK_SORT: each position (i, j)
in the output grid holds the block whose original 1-based index is
BLOCK_SORT[i][j].
"""

import sys
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
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
    Rearrange image blocks into a 4×4 mosaic according to BLOCK_SORT.

    Solution: divide the image into mosaic_shape[0] × mosaic_shape[1] equal
    blocks. For each output position (i, j), look up BLOCK_SORT[i][j] to find
    the 1-based source block index, convert it to (block_row, block_col), and
    copy the corresponding pixel region into the output.
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


def mosaic_4x4_vectorized(
    image: list[list[int]],
    mosaic_shape: tuple[int, int] = MOSAIC_SHAPE,
    block_sort: list[list[int]] = BLOCK_SORT,
) -> list[list[int]]:
    """
    Rearrange image blocks into a 4x4 mosaic using NumPy array slicing.

    Identical result as ``mosaic_4x4`` but uses numpy slice assignment
    instead of nested Python loops.
    """
    arr = np.array(image, dtype=np.uint8)
    bh = arr.shape[0] // mosaic_shape[0]
    bw = arr.shape[1] // mosaic_shape[1]
    output = np.empty_like(arr)
    for i in range(mosaic_shape[0]):
        for j in range(mosaic_shape[1]):
            block_number = block_sort[i][j]
            src_r = (block_number - 1) // mosaic_shape[1]
            src_c = (block_number - 1) % mosaic_shape[1]
            output[
                i * bh : (i + 1) * bh,
                j * bw : (j + 1) * bw,
            ] = arr[
                src_r * bh : (src_r + 1) * bh,
                src_c * bw : (src_c + 1) * bw,
            ]
    return output.tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    mosaic = mosaic_4x4(img)

    outputs = {
        "baboon_mosaic.png": mosaic,
    }
    return save_grayscale_outputs(output_dir, outputs)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "baboon_monocromatica.png": input_dir / "baboon_monocromatica.png",
        "baboon_mosaic.png": output_dir / "baboon_mosaic.png",
    }


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def run_benchmarks(
    repeats: int = 20,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(
        EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs
    )
    image = load_grayscale_image(input_paths["imagem"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks = {
        "mosaic_4x4": {
            "loop": benchmark_function(
                mosaic_4x4,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                mosaic_4x4_vectorized,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
        },
    }

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "image": {
                "filename": input_paths["imagem"].name,
                "width": width,
                "height": height,
            },
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
