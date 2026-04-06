"""
1.13 Filtragem de Imagens
A ﬁltragem aplicada a uma imagem digital ´e uma operac¸˜ao local que altera os valores de intensi-
dade dos pixels da imagem levando-se em conta tanto o valor do pixel em quest˜ao quanto valores
de pixels vizinhos.
No processo de ﬁltragem, utiliza-se uma operac¸˜ao de convoluc¸˜ao de uma m´ascara pela imagem.
Este processo equivale a percorrer toda a imagem alterando seus valores conforme os pesos da
m´ascara e as intensidades da imagem.
Aplicar os ﬁltros h1 a h11 em uma imagem digital monocrom´atica.
"""

"""
h1 =
0 0 -1 0 0
0 -1 -2 -1 0
-1 -2 16 -2 -1
0 -1 -2 -1 0
0 0 -1 0 0
h2 = 1
256
1 4 6 4 1
4 16 24 16 4
6 24 36 24 6
4 16 24 16 4
1 4 6 4 1
h3 =
-1 0 1
-2 0 2
-1 0 1
h4 =
-1 -2 -1
0 0 0
1 2 1
h5 =
-1 -1 -1
-1 8 -1
-1 -1 -1
h6 = 1
9
1 1 1
1 1 1
1 1 1
h7 =
-1 -1 2
-1 2 -1
2 -1 -1
h8 =
2 -1 -1
-1 2 -1
-1 -1 2
h9 = 1
9
1 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 1
h10 = 1
8
-1 -1 -1 -1 -1
-1 2 2 2 -1
-1 2 8 2 -1
-1 2 2 2 -1
-1 -1 -1 -1 -1
h11 =
-1 -1 0
-1 0 1
0 1 1
"""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.common.image_io import (
    load_grayscale_image,
    save_grayscale_outputs,
)
from src.common.runner import run_exercise

EXERCISE_NAME = "exercicio_13"
INPUTS = {
    "imagem": "https://www.ic.unicamp.br/~helio/imagens_png/baboon_monocromatica.png",
}
H1 = [
    [0, 0, -1, 0, 0],
    [0, -1, -2, -1, 0],
    [-1, -2, 16, -2, -1],
    [0, -1, -2, -1, 0],
    [0, 0, -1, 0, 0],
]
H2 = [
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1],
]
H3 = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
]
H4 = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1],
]
H5 = [
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
]
H6 = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]
H7 = [
    [-1, -1, 2],
    [-1, 2, -1],
    [2, -1, -1],
]
H8 = [
    [2, -1, -1],
    [-1, 2, -1],
    [-1, -1, 2],
]
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
H10 = [
    [-1, -1, -1, -1, -1],
    [-1, 2, 2, 2, -1],
    [-1, 2, 8, 2, -1],
    [-1, 2, 2, 2, -1],
    [-1, -1, -1, -1, -1],
]
H11 = [
    [-1, -1, 0],
    [-1, 0, 1],
    [0, 1, 1],
]

"""
1.13 Filtragem de Imagens
A ﬁltragem aplicada a uma imagem digital ´e uma operac¸˜ao local que altera os valores de intensi-
dade dos pixels da imagem levando-se em conta tanto o valor do pixel em quest˜ao quanto valores
de pixels vizinhos.
No processo de ﬁltragem, utiliza-se uma operac¸˜ao de convoluc¸˜ao de uma m´ascara pela imagem.
Este processo equivale a percorrer toda a imagem alterando seus valores conforme os pesos da
m´ascara e as intensidades da imagem.
Aplicar os ﬁltros h1 a h11 em uma imagem digital monocrom´atica.
"""


def convolve(
    image: list[list[int]], kernel: list[list[int]], scale: float = 1.0
) -> list[list[float]]:
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
    raw = convolve(image, kernel, scale)
    return [[max(0, min(255, round(v))) for v in row] for row in raw]


def apply_filter_magnitude(
    image: list[list[int]],
    kernel_a: list[list[int]],
    kernel_b: list[list[int]],
) -> list[list[int]]:
    import math
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


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


if __name__ == "__main__":
    try:
        run()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
