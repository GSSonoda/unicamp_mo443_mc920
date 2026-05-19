"""
Trabalho 3 — Transformada de Fourier Bidimensional
Análise 2: Invariância da FFT sob Transformações Geométricas
=============================================================
Para cada imagem de entrada, aplica três transformações geométricas
(translação, rotação, mudança de escala) e compara os espectros de
magnitude resultantes com o espectro da imagem original.

Propriedades esperadas a verificar experimentalmente:
  - Translação:   o espectro de magnitude é invariante (só a fase muda).
  - Rotação:      o espectro gira na mesma direção e no mesmo ângulo.
  - Mudança de escala: a distribuição radial das frequências é afetada
                       (comprimir a imagem → espalha as frequências).

Entrada:  imagens PGM monocromáticas
Saída:    imagens PNG (pares imagem + espectro para cada transformação)
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import numpy as np

from src.common.benchmark import benchmark_function, write_benchmark_results
from src.common.image_io import load_grayscale_image
from src.common.inputs import prepare_inputs
from src.common.paths import results_dir_for
from src.common.runner import run_exercise

EXERCISE_NAME = "analise_02_invariancia"
PGM_BASE = "http://www.ic.unicamp.br/~helio/imagens_pgm/"
INPUTS = {
    "baboon":   PGM_BASE + "baboon.pgm",
    "fiducial": PGM_BASE + "fiducial.pgm",
    "monarch":  PGM_BASE + "monarch.pgm",
    "peppers":  PGM_BASE + "peppers.pgm",
    "retina":   PGM_BASE + "retina.pgm",
    "sonnet":   PGM_BASE + "sonnet.pgm",
    "wedge":    PGM_BASE + "wedge.pgm",
}

# Parâmetros das transformações
TRANSLATION_DX = 50    # deslocamento horizontal em pixels
TRANSLATION_DY = 30    # deslocamento vertical em pixels
ROTATION_ANGLE = 45.0  # ângulo de rotação em graus
SCALE_FACTOR = 0.5     # fator de escala (0.5 = reduz à metade)


# ---------------------------------------------------------------------------
# TODO 1: Transformações geométricas
# ---------------------------------------------------------------------------

def translate_image(
    image: list[list[int]],
    dx: int,
    dy: int,
) -> list[list[int]]:
    """Translada a imagem circularmente (deslocamento toroidal) em dx, dy pixels.

    Translação circular significa que os pixels que saem por um lado
    reaparecem pelo outro (comportamento de np.roll).

    Passos esperados:
      1. Converter para numpy array uint8.
      2. Deslocar verticalmente:   np.roll(img, dy, axis=0)
      3. Deslocar horizontalmente: np.roll(img, dx, axis=1)
      4. Converter de volta para list[list[int]].

    Args:
        dx: deslocamento na direção horizontal (colunas).
        dy: deslocamento na direção vertical (linhas).

    Returns:
        list[list[int]]: imagem transladada, mesmo tamanho da entrada.
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar translate_image — use np.roll(img, dy, axis=0) "
        "seguido de np.roll(img, dx, axis=1)"
    )


def rotate_image(
    image: list[list[int]],
    angle_degrees: float,
) -> list[list[int]]:
    """Rotaciona a imagem em torno do centro, preenchendo bordas com zero.

    Passos esperados:
      1. Converter para numpy array float64.
      2. Usar scipy.ndimage.rotate(img, angle_degrees, reshape=False, cval=0).
      3. Clipar valores ao intervalo [0, 255]: np.clip(..., 0, 255).
      4. Converter para uint8 e depois para list[list[int]].

    Args:
        angle_degrees: ângulo de rotação em graus (sentido anti-horário).

    Returns:
        list[list[int]]: imagem rotacionada, mesmo tamanho da entrada.
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar rotate_image — use scipy.ndimage.rotate() "
        "com reshape=False para manter o tamanho original"
    )


def scale_image(
    image: list[list[int]],
    factor: float,
) -> list[list[int]]:
    """Redimensiona a imagem pelo fator dado, mantendo o tamanho do canvas original.

    Passos esperados:
      1. Converter para numpy array float64.
      2. Usar scipy.ndimage.zoom(img, factor) para redimensionar.
      3. Criar um canvas preto (zeros) do tamanho original.
      4. Se factor < 1 (imagem ficou menor): centralizar a imagem reduzida
         no canvas e deixar bordas pretas.
         Se factor > 1 (imagem ficou maior): recortar o centro para o
         tamanho original.
      5. Converter para list[list[int]].

    Args:
        factor: fator de escala (ex.: 0.5 = metade, 2.0 = dobro).

    Returns:
        list[list[int]]: imagem redimensionada, mesmo tamanho da entrada.
    """
    # --- Implemente aqui ---
    raise NotImplementedError(
        "TODO: implementar scale_image — use scipy.ndimage.zoom() "
        "e centralize no canvas original"
    )


# ---------------------------------------------------------------------------
# TODO 2: Cálculo do espectro de magnitude (mesmo da Análise 1)
# ---------------------------------------------------------------------------

def compute_fft_magnitude_spectrum(image: list[list[int]]) -> np.ndarray:
    """Calcula log(1 + |FFT2D(imagem)|), centrado na baixa frequência.

    Passos esperados (mesma lógica da Análise 1):
      1. Converter para float64.
      2. np.fft.fft2() → np.fft.fftshift() → np.abs() → np.log1p().

    Returns:
        np.ndarray: espectro em escala logarítmica (float64), shape (H, W).
    """
    # --- Implemente aqui (pode copiar/importar de analise_01) ---
    raise NotImplementedError(
        "TODO: implementar compute_fft_magnitude_spectrum — "
        "use np.fft.fft2() + np.fft.fftshift() + np.abs() + np.log1p()"
    )


# ---------------------------------------------------------------------------
# Visualizações (infraestrutura pronta — não precisa modificar)
# ---------------------------------------------------------------------------

def _save_gray_image(array: np.ndarray, path: Path) -> None:
    """Salva array NumPy como imagem PNG em tons de cinza."""
    from PIL import Image as PILImage
    PILImage.fromarray(array.astype(np.uint8)).save(path)


def _save_spectrum_image(log_spectrum: np.ndarray, path: Path) -> None:
    """Salva o espectro logarítmico como imagem colorida (colormap 'inferno')."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    vmax = np.percentile(log_spectrum, 99)
    ax.imshow(log_spectrum, cmap="inferno", vmin=0, vmax=vmax)
    ax.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(str(path), dpi=100, bbox_inches="tight")
    plt.close(fig)


def _process_variant(
    image: list[list[int]],
    stem: str,
    variant_name: str,
    output_dir: Path,
    saved: list[Path],
) -> None:
    """Salva o par (imagem transformada, espectro) para uma variante."""
    img_arr = np.array(image, dtype=np.uint8)
    img_path = output_dir / f"inv_{stem}_{variant_name}.png"
    spec_path = output_dir / f"inv_{stem}_espectro_{variant_name}.png"

    _save_gray_image(img_arr, img_path)
    saved.append(img_path)

    log_spectrum = compute_fft_magnitude_spectrum(image)
    _save_spectrum_image(log_spectrum, spec_path)
    saved.append(spec_path)


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def process(input_paths: dict[str, Path], output_dir: Path) -> list[Path]:
    saved: list[Path] = []
    for stem, img_path in input_paths.items():
        image = load_grayscale_image(img_path)

        # Salva imagem original sem nenhuma transformação
        img_arr = np.array(image, dtype=np.uint8)
        _save_gray_image(img_arr, output_dir / f"inv_{stem}_original.png")
        saved.append(output_dir / f"inv_{stem}_original.png")

        try:
            # Espectro da imagem original
            log_spectrum = compute_fft_magnitude_spectrum(image)
            _save_spectrum_image(
                log_spectrum,
                output_dir / f"inv_{stem}_espectro_original.png",
            )
            saved.append(output_dir / f"inv_{stem}_espectro_original.png")

            # TODO 1a: translação — preencha translate_image
            translated = translate_image(image, TRANSLATION_DX, TRANSLATION_DY)
            _process_variant(translated, stem, "translacao", output_dir, saved)

            # TODO 1b: rotação — preencha rotate_image
            rotated = rotate_image(image, ROTATION_ANGLE)
            _process_variant(rotated, stem, "rotacao", output_dir, saved)

            # TODO 1c: mudança de escala — preencha scale_image
            scaled = scale_image(image, SCALE_FACTOR)
            _process_variant(scaled, stem, "escala", output_dir, saved)

        except NotImplementedError as exc:
            print(f"[todo] {exc}")

    return saved


def run(overwrite: bool = False) -> list[Path]:
    return run_exercise(EXERCISE_NAME, INPUTS, process, overwrite=overwrite)


def report_files() -> dict[str, Path]:
    output_dir = results_dir_for(EXERCISE_NAME)
    stems = ["baboon", "fiducial", "monarch", "peppers", "retina", "sonnet", "wedge"]
    files: dict[str, Path] = {}
    for stem in stems:
        for variant in [
            "original", "espectro_original",
            "translacao", "espectro_translacao",
            "rotacao", "espectro_rotacao",
            "escala", "espectro_escala",
        ]:
            key = f"inv_{stem}_{variant}.png"
            files[key] = output_dir / key
    return files


def run_benchmarks(
    repeats: int = 10,
    warmup: int = 2,
    overwrite_inputs: bool = False,
) -> Path:
    input_paths = prepare_inputs(EXERCISE_NAME, INPUTS, overwrite=overwrite_inputs)
    image = load_grayscale_image(input_paths["baboon"])
    height = len(image)
    width = len(image[0]) if height else 0

    benchmarks: dict = {}
    try:
        benchmarks["translate_image"] = benchmark_function(
            translate_image, image, TRANSLATION_DX, TRANSLATION_DY,
            repeats=repeats, warmup=warmup,
        )
        benchmarks["rotate_image"] = benchmark_function(
            rotate_image, image, ROTATION_ANGLE,
            repeats=repeats, warmup=warmup,
        )
        benchmarks["scale_image"] = benchmark_function(
            scale_image, image, SCALE_FACTOR,
            repeats=repeats, warmup=warmup,
        )
    except NotImplementedError as exc:
        print(f"[todo] Benchmark nao disponivel: {exc}")

    output_path = write_benchmark_results(
        EXERCISE_NAME,
        "tempos_execucao.json",
        {
            "exercise": EXERCISE_NAME,
            "image": {
                "filename": input_paths["baboon"].name,
                "width": width,
                "height": height,
            },
            "parametros": {
                "translation_dx": TRANSLATION_DX,
                "translation_dy": TRANSLATION_DY,
                "rotation_angle_degrees": ROTATION_ANGLE,
                "scale_factor": SCALE_FACTOR,
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
