import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_12"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}


def image_quantization(image: list[list[int]], factor: int) -> list[list[int]]:
    if factor <= 0:
        raise ValueError(
            "O fator de quantização deve ser um inteiro positivo."
        )
    if factor > 256:
        raise ValueError("O fator de quantização não pode ser maior que 256.")
    step = 256 // factor
    quantized_image = []
    for row in image:
        quantized_row = []
        for pixel in row:
            quantized_pixel = (pixel // step) * step
            quantized_row.append(quantized_pixel)
        quantized_image.append(quantized_row)
    return quantized_image


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "quantizacao_256_niveis.png": image_quantization(img, 256),
        "quantizacao_64_niveis.png": image_quantization(img, 64),
        "quantizacao_32_niveis.png": image_quantization(img, 32),
        "quantizacao_16_niveis.png": image_quantization(img, 16),
        "quantizacao_8_niveis.png": image_quantization(img, 8),
        "quantizacao_4_niveis.png": image_quantization(img, 4),
        "quantizacao_2_niveis.png": image_quantization(img, 2),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
