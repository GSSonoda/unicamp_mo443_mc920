"""
1.3 Pencil Sketch Effect
========================
Implement a pencil sketch effect through the following steps:
  (i)   Convert the color image to grayscale.
  (ii)  Apply a 21×21 Gaussian blur to smooth fine details.
  (iii) Divide the grayscale image by the blurred version (dodge blend)
        to enhance contours and produce a sketch-like appearance.
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

EXERCISE_NAME = "exercicio_03"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/watch.png",
}


def image_gaussian_blur(
    image: list[list[int]], kernel_size: int = 21
) -> list[list[int]]:
    """
    Apply a Gaussian blur filter to a grayscale image using a square kernel.

    The Gaussian blur is a low-pass filter that replaces each pixel with a
    weighted average of its neighborhood. Pixels closer to the center of the
    kernel receive higher weights, following a Gaussian (normal) distribution.
    This effectively suppresses high-frequency components (sharp edges, noise)
    while preserving low-frequency content (smooth regions).

    Parameters
    ----------
    image : list[list[int]]
        Input grayscale image as a 2D list with pixel values in [0, 255].
    kernel_size : int
        Side length of the square Gaussian kernel (default: 21).
        Must be odd so the kernel has a well-defined center pixel.

    Returns
    -------
    list[list[int]]
        Blurred image with the same dimensions as the input.
    """
    arr = np.array(image, dtype=np.uint8)

    # --- Build the 1D Gaussian function ---
    # The Gaussian function is defined as:
    #
    #   f(x) = a * exp( -0.5 * ((x - b) / c)^2 )
    #
    # where:
    #   a = peak height (amplitude) — set to 1.0 here; normalization handles scale
    #   b = mean (center of the kernel, i.e., kernel_size // 2)
    #   c = standard deviation — controls how quickly weights decay with distance
    #
    # A common heuristic is sigma = kernel_size / 6, so that roughly 99.7% of
    # the Gaussian mass falls within the kernel window (the "3-sigma rule").
    peak_height = 1.0
    mean = kernel_size // 2
    std_dev = kernel_size / 6  # 3-sigma rule: kernel covers ±3*sigma
    f_x = lambda x: peak_height * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

    # --- Build the 2D Gaussian kernel via outer product ---
    # Because the 2D Gaussian is separable (G(x,y) = G(x) * G(y)), the kernel
    # can be constructed as the outer product of two 1D Gaussian vectors.
    # This is equivalent to evaluating G(x, y) = exp(-0.5*((x-b)^2+(y-b)^2)/c^2)
    # at every (x, y) position on the grid.
    kernel = np.outer(
        f_x(np.arange(kernel_size)),
        f_x(np.arange(kernel_size)),
    )

    # Normalize the kernel so its elements sum to 1.
    # This ensures that applying the filter does not change the overall
    # brightness of a uniform image (energy conservation).
    kernel /= kernel.sum()

    # --- Apply the filter via direct (spatial) convolution ---
    # The image is zero-padded on all sides by pad_size = kernel_size // 2
    # pixels using "edge" mode, which replicates border pixels instead of
    # introducing artificial black borders (zero-padding artifacts).
    pad_size = kernel_size // 2
    padded_image = np.pad(arr, pad_size, mode="edge")

    blurred_image = np.zeros_like(arr)
    for row in range(arr.shape[0]):
        for col in range(arr.shape[1]):
            # Extract the local neighborhood (region of interest) centered at
            # pixel (row, col) with the same shape as the kernel.
            region = padded_image[
                row : row + kernel_size, col : col + kernel_size
            ]
            # Compute the weighted sum (dot product) between the neighborhood
            # and the normalized kernel — this is the convolution output.
            blurred_value = np.sum(region * kernel)
            blurred_image[row, col] = int(blurred_value)

    return blurred_image.tolist()


def divide_images(
    image1: list[list[int]], image2: list[list[int]]
) -> list[list[int]]:
    """
    Compute a pixel-wise division of two grayscale images to produce a sketch effect.

    This operation is known as "dodge blending" in image processing.  Dividing
    the original grayscale image by its blurred version highlights regions
    where the two images differ — i.e., edges and fine details — while
    suppressing flat (low-frequency) areas where both images are similar.

    Mathematically, for each pixel position (i, j):

        result(i, j) = original(i, j) / blurred(i, j) * 255

    In smooth (flat) regions, original ≈ blurred, so the ratio ≈ 1 and the
    output ≈ 255 (white). Near edges, the blurred value is noticeably lower
    or higher than the original, producing darker strokes — resembling a
    pencil sketch on a white background.

    The ratio is scaled by 255 to map the normalized [0, 1] range back into
    the displayable [0, 255] uint8 range. Pixels where the denominator is
    zero (or produces non-finite values) are set to 0 to avoid undefined
    behavior.

    Parameters
    ----------
    image1 : list[list[int]]
        Original grayscale image (numerator).
    image2 : list[list[int]]
        Blurred grayscale image (denominator).

    Returns
    -------
    list[list[int]]
        Sketch-effect image with pixel values in [0, 255].
    """
    arr1 = np.array(image1, dtype=np.float32)
    arr2 = np.array(image2, dtype=np.float32)

    # Perform element-wise division; suppress divide-by-zero warnings since
    # non-finite results are explicitly handled in the next step.
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.true_divide(arr1, arr2)
        result[~np.isfinite(result)] = 0  # set inf and NaN to 0

    # Scale the ratio from [0, ~1] to [0, 255] so the output can be stored
    # as a standard 8-bit grayscale image.  Without this step, values close
    # to 1.0 would be truncated to 0 or 1 by uint8 casting, yielding a black image.
    result = np.clip(result * 255, 0, 255)
    return result.astype(np.uint8).tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    """
    Full processing pipeline for the sketch-effect exercise.

    Steps
    -----
    (i)   Load the input image and convert it to grayscale.
    (ii)  Apply a 21×21 Gaussian blur to obtain a smoothed version.
    (iii) Divide the grayscale image by the blurred image (dodge blend)
          to produce the final pencil-sketch effect.
    """
    # (i) Convert the color image to grayscale.
    # Grayscale conversion reduces the image to a single luminance channel,
    # which is sufficient for edge-enhancement techniques.
    img_grayscale = load_grayscale_image(input_paths["imagem"])

    # (ii) Apply the Gaussian blur to suppress high-frequency details.
    # The blurred image serves as a low-frequency baseline; any deviation of
    # the original from this baseline corresponds to edges or texture.
    img_gaussian_blur = image_gaussian_blur(img_grayscale)

    # (iii) Divide the grayscale image by the blurred version.
    # Flat regions (where original ≈ blurred) become white; edges and fine
    # details (where the two images differ) produce dark strokes.
    img_sketch_effect = divide_images(img_grayscale, img_gaussian_blur)

    outputs = {
        "watch_grayscale.png": img_grayscale,
        "watch_gaussian_blur.png": img_gaussian_blur,
        "watch_sketch_effect.png": img_sketch_effect,
    }
    return save_grayscale_outputs(output_dir, outputs)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "watch.png": input_dir / "watch.png",
        "watch_grayscale.png": output_dir / "watch_grayscale.png",
        "watch_gaussian_blur.png": output_dir / "watch_gaussian_blur.png",
        "watch_sketch_effect.png": output_dir / "watch_sketch_effect.png",
    }


def image_gaussian_blur_vectorized(
    image: list[list[int]], kernel_size: int = 21
) -> list[list[int]]:
    """
    Apply a Gaussian blur using NumPy's vectorized array operations.

    Builds the same separable 1-D Gaussian kernel as the loop version, but
    applies it with ``np.apply_along_axis`` and ``np.convolve`` instead of
    explicit Python loops, which is significantly faster on large images.
    """
    arr = np.array(image, dtype=np.float32)
    mean = kernel_size // 2
    std_dev = kernel_size / 6
    x = np.arange(kernel_size, dtype=np.float32)
    kernel_1d = np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    kernel_1d /= kernel_1d.sum()

    # Separable convolution: convolve rows then columns
    pad = kernel_size // 2
    padded = np.pad(arr, pad, mode="edge")
    # Convolve along rows
    row_conv = np.apply_along_axis(
        lambda row: np.convolve(row, kernel_1d, mode="valid"),
        axis=1,
        arr=padded,
    )
    # Convolve along columns
    col_conv = np.apply_along_axis(
        lambda col: np.convolve(col, kernel_1d, mode="valid"),
        axis=0,
        arr=row_conv,
    )
    return np.clip(col_conv, 0, 255).astype(np.uint8).tolist()


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
        "gaussian_blur": {
            "loop": benchmark_function(
                image_gaussian_blur,
                image,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_gaussian_blur_vectorized,
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
