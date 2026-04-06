"""
1.4 Brightness Adjustment via Gamma Correction
===============================================
Apply gamma correction to adjust the brightness of a monochromatic image A
and produce a corrected output image B:
  (i)   Normalize pixel intensities from [0, 255] to [0, 1].
  (ii)  Apply B = A^(1/gamma).
  (iii) Convert the result back to [0, 255].

Test with gamma values: 0.25, 0.5, 1.0, 2.0, 4.0.
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

EXERCISE_NAME = "exercicio_04"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}

# Gamma values to test: values < 1 brighten the image, > 1 darken it
GAMMA_VALUES = [0.25, 0.5, 1.0, 2.0, 4.0]


def image_gamma_correction(image: list[list[int]], gamma: float) -> list[list[int]]:
    """
    Apply gamma correction to a grayscale image.

    Gamma correction is a non-linear intensity transformation commonly used to
    adjust the perceived brightness of an image. The transformation follows the
    power-law relationship:

        B = A^(1/gamma)

    where A is the normalized input intensity in [0, 1] and B is the
    corrected output intensity, also in [0, 1].

    Effect of gamma on brightness
    ------------------------------
    - gamma < 1 : the exponent 1/gamma > 1, which compresses dark tones and
                  expands bright tones → image becomes darker overall.
    - gamma = 1 : the exponent 1/gamma = 1, so B = A (identity, no change).
    - gamma > 1 : the exponent 1/gamma < 1, which expands dark tones and
                  compresses bright tones → image becomes brighter overall.

    Processing steps
    ----------------
    (i)   Normalize pixel intensities from [0, 255] to [0, 1] by dividing by 255.
    (ii)  Apply the gamma correction equation: B = A^(1/gamma).
    (iii) Convert the result back to [0, 255] by multiplying by 255, then
          clip to the valid range and cast to uint8.

    Parameters
    ----------
    image : list[list[int]]
        Input grayscale image as a 2D list with pixel values in [0, 255].
    gamma : float
        Gamma parameter γ. Must be positive (non-zero).

    Returns
    -------
    list[list[int]]
        Gamma-corrected image with pixel values in [0, 255].
    """
    arr = np.array(image, dtype=np.float32)

    # Step (i): normalize to [0, 1]
    # Dividing by 255 maps the integer range [0, 255] to the continuous
    # range [0.0, 1.0], which is required for the power-law to behave correctly.
    normalized = arr / 255.0

    # Step (ii): apply gamma correction  B = A^(1/gamma)
    # The exponent 1/gamma controls the shape of the tone curve.
    # numpy's power function handles element-wise exponentiation efficiently.
    corrected = np.power(normalized, 1.0 / gamma)

    # Step (iii): convert back to [0, 255]
    # Multiply by 255 to restore the original integer scale, clip to [0, 255]
    # to handle any floating-point overshoot, then cast to uint8.
    result = np.clip(corrected * 255.0, 0, 255).astype(np.uint8)

    return result.tolist()


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    """
    Apply gamma correction to the input image using multiple gamma values.

    For each gamma in GAMMA_VALUES, the function:
    (i)   Normalizes pixel intensities to [0, 1].
    (ii)  Applies B = A^(1/gamma).
    (iii) Rescales the result back to [0, 255].

    The original image is also saved for visual comparison.
    """
    image = load_grayscale_image(input_paths["imagem"])

    outputs = {}

    for gamma in GAMMA_VALUES:
        corrected = image_gamma_correction(image, gamma)
        # Use gamma value in filename; replace '.' with '_' for compatibility.
        gamma_str = str(gamma).replace(".", "_")
        filename = f"baboon_gamma_{gamma_str}.png"
        outputs[filename] = corrected

    return save_grayscale_outputs(output_dir, outputs)


def image_gamma_correction_vectorized(
    image: list[list[int]], gamma: float
) -> list[list[int]]:
    """
    Apply gamma correction using NumPy vectorized operations.

    Identical mathematics to ``image_gamma_correction`` but operates on the
    entire array at once instead of element-by-element, which is much faster.
    """
    arr = np.array(image, dtype=np.float32) / 255.0
    corrected = np.power(arr, 1.0 / gamma)
    return np.clip(corrected * 255.0, 0, 255).astype(np.uint8).tolist()


def report_files() -> dict[str, Path]:
    input_dir = input_dir_for(EXERCISE_NAME)
    output_dir = results_dir_for(EXERCISE_NAME)

    files: dict[str, Path] = {
        "baboon_monocromatica.png": input_dir / "baboon_monocromatica.png",
    }
    for gamma in GAMMA_VALUES:
        gamma_str = str(gamma).replace(".", "_")
        filename = f"baboon_gamma_{gamma_str}.png"
        files[filename] = output_dir / filename
    return files


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
    gamma = 2.0

    benchmarks = {
        "gamma_correction": {
            "loop": benchmark_function(
                image_gamma_correction,
                image,
                gamma,
                repeats=repeats,
                warmup=warmup,
            ),
            "vetorizado": benchmark_function(
                image_gamma_correction_vectorized,
                image,
                gamma,
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
