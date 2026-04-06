"""
1.13 Image Filtering
====================
Image filtering is a local operation that alters pixel intensity values by
taking into account both the pixel itself and its neighbors. The process uses
convolution of a mask (kernel) over the image: slide the kernel across every
pixel, compute the weighted sum of the neighborhood, and write the result.

Apply filters H1 through H11 to a monochromatic digital image.

Filters requiring a normalization scale factor:
  H2  x (1/256) — Gaussian blur (5x5)
  H6  x (1/9)   — Box blur (3x3)
  H9  x (1/9)   — Diagonal motion blur (9x9)
  H10 x (1/8)   — Unsharp masking (5x5)

H3 and H4 are also combined as sqrt(H3^2 + H4^2) (Sobel magnitude).
"""

import math
import sys
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.inputs import prepare_inputs
from src.common.paths import input_dir_for, results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_13"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}

# H1: sharpening — large positive center, negative ring; enhances fine detail
H1 = [
    [0, 0, -1, 0, 0],
    [0, -1, -2, -1, 0],
    [-1, -2, 16, -2, -1],
    [0, -1, -2, -1, 0],
    [0, 0, -1, 0, 0],
]

# H2 (x 1/256): Gaussian blur — smooths the image with a bell-shaped kernel
H2 = [
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1],
]

# H3: Sobel-X — detects vertical edges (horizontal gradient)
H3 = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
]

# H4: Sobel-Y — detects horizontal edges (vertical gradient)
H4 = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1],
]

# H5: Laplacian — detects edges in all directions
H5 = [
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
]

# H6 (x 1/9): box blur — uniform average of the 3x3 neighborhood
H6 = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]

# H7: emboss (diagonal ↗) — highlights the secondary diagonal direction
H7 = [
    [-1, -1, 2],
    [-1, 2, -1],
    [2, -1, -1],
]

# H8: emboss (diagonal ↘) — highlights the primary diagonal direction
H8 = [
    [2, -1, -1],
    [-1, 2, -1],
    [-1, -1, 2],
]

# H9 (x 1/9): diagonal motion blur — identity along the main diagonal
H9 = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
]

# H10 (x 1/8): unsharp masking — mild sharpening with outer suppression
H10 = [
    [-1, -1, -1, -1, -1],
    [-1, 2, 2, 2, -1],
    [-1, 2, 8, 2, -1],
    [-1, 2, 2, 2, -1],
    [-1, -1, -1, -1, -1],
]

# H11: diagonal emboss — subtle edge/texture enhancement along a diagonal
H11 = [
    [-1, -1, 0],
    [-1, 0, 1],
    [0, 1, 1],
]


def convolve(
    image: list[list[int]], kernel: list[list[int]], scale: float = 1.0
) -> list[list[float]]:
    """
    Compute the 2D discrete convolution of an image with a kernel.

    Solution: slide the kernel centered at each pixel (i, j), multiply
    overlapping values, sum them, then multiply by scale. Out-of-bounds
    positions use zero-padding (missing neighbors contribute 0).

    Returns raw float values — clamping is left to the caller.
    """
    height = len(image)
    width = len(image[0])
    kh = len(kernel) // 2
    kw = len(kernel[0]) // 2
    result = []
    for i in range(height):
        row = []
        for j in range(width):
            total = 0.0
            for ki in range(len(kernel)):
                for kj in range(len(kernel[0])):
                    ni = i + ki - kh
                    nj = j + kj - kw
                    if 0 <= ni < height and 0 <= nj < width:
                        total += image[ni][nj] * kernel[ki][kj]
            row.append(total * scale)
        result.append(row)
    return result


def apply_filter(
    image: list[list[int]], kernel: list[list[int]], scale: float = 1.0
) -> list[list[int]]:
    """
    Apply a convolution filter and clamp the result to [0, 255].

    Delegates the raw convolution to `convolve`, then rounds each value
    and clips it to the valid uint8 range.
    """
    raw = convolve(image, kernel, scale)
    return [[max(0, min(255, round(v))) for v in row] for row in raw]


def apply_filter_magnitude(
    image: list[list[int]],
    kernel_a: list[list[int]],
    kernel_b: list[list[int]],
) -> list[list[int]]:
    """
    Combine two filter responses as the gradient magnitude sqrt(A^2 + B^2).

    Solution: compute raw convolution responses for both kernels, then for
    each pixel compute sqrt(a^2 + b^2) and clamp to [0, 255]. Used for the
    Sobel edge magnitude: sqrt(H3^2 + H4^2) detects edges in all directions.
    """
    raw_a = convolve(image, kernel_a)
    raw_b = convolve(image, kernel_b)
    return [
        [
            max(0, min(255, round(math.sqrt(
                raw_a[i][j] ** 2 + raw_b[i][j] ** 2
            ))))
            for j in range(len(raw_a[i]))
        ]
        for i in range(len(raw_a))
    ]


def apply_filter_vectorized(
    image: list[list[int]], kernel: list[list[int]], scale: float = 1.0
) -> list[list[int]]:
    """
    Apply a convolution filter using NumPy's ``np.pad`` and stride tricks.

    Zero-pads the image, then uses a vectorized sliding-window sum via
    ``np.lib.stride_tricks.sliding_window_view`` to replace the inner Python
    loops.  Results are scaled, rounded, and clamped to [0, 255].
    """
    arr = np.array(image, dtype=np.float32)
    k = np.array(kernel, dtype=np.float32) * scale
    kh, kw = k.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(arr, ((ph, ph), (pw, pw)), mode="constant")
    windows = np.lib.stride_tricks.sliding_window_view(padded, (kh, kw))
    result = np.einsum("ijkl,kl->ij", windows, k)
    return np.clip(np.round(result), 0, 255).astype(np.uint8).tolist()


def apply_filter_magnitude_vectorized(
    image: list[list[int]],
    kernel_a: list[list[int]],
    kernel_b: list[list[int]],
) -> list[list[int]]:
    """
    Compute gradient magnitude sqrt(A^2 + B^2) using vectorized convolutions.
    """
    arr = np.array(image, dtype=np.float32)
    ka = np.array(kernel_a, dtype=np.float32)
    kb = np.array(kernel_b, dtype=np.float32)

    def _conv(img: np.ndarray, k: np.ndarray) -> np.ndarray:
        kh, kw = k.shape
        ph, pw = kh // 2, kw // 2
        padded = np.pad(img, ((ph, ph), (pw, pw)), mode="constant")
        windows = np.lib.stride_tricks.sliding_window_view(
            padded, (kh, kw)
        )
        return np.einsum("ijkl,kl->ij", windows, k)

    raw_a = _conv(arr, ka)
    raw_b = _conv(arr, kb)
    magnitude = np.sqrt(raw_a ** 2 + raw_b ** 2)
    return np.clip(np.round(magnitude), 0, 255).astype(np.uint8).tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "h1.png": apply_filter(img, H1),
        "h2.png": apply_filter(img, H2, scale=1 / 256),
        "h3.png": apply_filter(img, H3),
        "h4.png": apply_filter(img, H4),
        "h3_h4_combined.png": apply_filter_magnitude(img, H3, H4),
        "h5.png": apply_filter(img, H5),
        "h6.png": apply_filter(img, H6, scale=1 / 9),
        "h7.png": apply_filter(img, H7),
        "h8.png": apply_filter(img, H8),
        "h9.png": apply_filter(img, H9, scale=1 / 9),
        "h10.png": apply_filter(img, H10, scale=1 / 8),
        "h11.png": apply_filter(img, H11),
    }
    return save_grayscale_outputs(output_dir, outputs)


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    return {
        "baboon_monocromatica.png": input_dir / "baboon_monocromatica.png",
        "h1.png": output_dir / "h1.png",
        "h2.png": output_dir / "h2.png",
        "h3.png": output_dir / "h3.png",
        "h4.png": output_dir / "h4.png",
        "h3_h4_combined.png": output_dir / "h3_h4_combined.png",
        "h5.png": output_dir / "h5.png",
        "h6.png": output_dir / "h6.png",
        "h7.png": output_dir / "h7.png",
        "h8.png": output_dir / "h8.png",
        "h9.png": output_dir / "h9.png",
        "h10.png": output_dir / "h10.png",
        "h11.png": output_dir / "h11.png",
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
        "apply_filter_h6": {
            "loop": benchmark_function(
                apply_filter,
                image,
                H6,
                1 / 9,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                apply_filter_vectorized,
                image,
                H6,
                1 / 9,
                repeats=repeats,
                warmup=warmup,
            ),
        },
        "apply_filter_magnitude_h3_h4": {
            "loop": benchmark_function(
                apply_filter_magnitude,
                image,
                H3,
                H4,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                apply_filter_magnitude_vectorized,
                image,
                H3,
                H4,
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
