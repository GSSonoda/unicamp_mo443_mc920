import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_11"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/city.png",
}


def image_negative(image: list[list[int]]) -> list[list[int]]:
    """
    # 1.11 Transformac¸˜ao de Intensidade
    Dada (a) uma imagem monocrom´atica, transformar seu espac¸o de intensidades (n´ıveis de cinza)
    para (b) obter o negativo da imagem, ou seja, o n´ıvel de cinza 0 ser´a convertido para 255, o n´ıvel
    1 para 254 e assim por diante,
    """
    return [[255 - pixel for pixel in row] for row in image]


def image_convert_interval(
    image: list[list[int]], new_min: int = 100, new_max: int = 200
) -> list[list[int]]:
    """
        Seja uma imagem de entrada com valores de n ́ıveis de cinza m ́ınimo e m ́aximo fmin efmax, respectivamente.Para mapear o intervalo de intensidade [fmin, fmax] dessa imagem em uma nova
    imagem com intervalo [gmin, gmax], pode-se utilizar a transforma ̧c ̃aog = gmax − gminfmax − fmin(f − fmin) + gmin
    """
    fmin = min(min(row) for row in image)
    fmax = max(max(row) for row in image)
    return [
        [
            int((new_max - new_min) / (fmax - fmin) * (pixel - fmin) + new_min)
            for pixel in row
        ]
        for row in image
    ]


def image_invert_even_rows(image: list[list[int]]) -> list[list[int]]:
    """
    (d) inverter os valores dos pixels das linhas pares da imagem, ou seja, os valores dos pixels da linha 0
    ser˜ao posicionados da direita para esquerda, os valores dos pixels da linha 2 ser˜ao posicionados da
    direita para a esquerda e assim por diante,
    """
    return [row[::-1] if i % 2 == 0 else row for i, row in enumerate(image)]


def image_mirror_upper_half(image: list[list[int]]) -> list[list[int]]:
    """
    (e) espelhar as linhas da metade superior da imagem na parte inferior da imagem
    """
    height = len(image)
    half_height = height // 2
    return image[:half_height] + image[:half_height][::-1]


def image_mirror_vertical(image: list[list[int]]) -> list[list[int]]:
    """
    (f) aplicar um espelhamento vertical na imagem levando-se em conta
    todas as linhas da imagem
    """
    return image[::-1]


def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    img = load_grayscale_image(input_paths["imagem"])
    outputs = {
        "negative.png": image_negative(img),
        "interval_100_200.png": image_convert_interval(
            img, new_min=100, new_max=200
        ),
        "interval_0_100.png": image_convert_interval(
            img, new_min=0, new_max=100
        ),
        "interval_50_150.png": image_convert_interval(
            img, new_min=50, new_max=150
        ),
        "interval_0_255.png": image_convert_interval(
            img, new_min=0, new_max=255
        ),
        "invert_even_rows.png": image_invert_even_rows(img),
        "mirror_upper_half.png": image_mirror_upper_half(img),
        "mirror_vertical.png": image_mirror_vertical(img),
    }
    return save_grayscale_outputs(output_dir, outputs)


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
