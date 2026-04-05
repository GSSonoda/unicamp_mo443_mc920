import sys
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import load_grayscale_image, save_grayscale_outputs
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_05"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}

def image_binary_thresholding(image: list[list[int]], threshold: int) -> list[list[int]]:
    """
    Apply binary thresholding to a grayscale image.

    Binary thresholding is a simple image segmentation technique that converts a
    grayscale image into a binary image based on a specified intensity threshold.
    Each pixel is classified as either foreground (white) or background (black)
    depending on whether its intensity is above or below the threshold.

    Thresholding rule:
        If pixel intensity >= threshold: set to 255 (white)
        Else: set to 0 (black)

    Parameters
    ----------
    image : list[list[int]]
        Input grayscale image as a 2D list with pixel values in [0, 255].
    threshold : int
        Threshold value in the range [0, 255].

    Returns
    -------
    list[list[int]]
        Binary image with pixel values either 0 or 255.
    """
    # Convert input to numpy array for efficient processing
    img_array = np.array(image, dtype=np.uint8)

    # Apply binary thresholding using vectorized operations
    binary_array = np.where(img_array >= threshold, 255, 0).astype(np.uint8)

    # Convert back to list of lists for output
    return binary_array.tolist()

def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    outputs = {
        f"baboon_threshold_{threshold}.png": image_binary_thresholding(
            load_grayscale_image(input_paths["imagem"]), threshold
        )
        for threshold in [50, 100, 150, 200]
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
