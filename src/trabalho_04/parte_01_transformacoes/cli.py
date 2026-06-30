"""
Trabalho 4 — Parte 1: programa de linha de comando.

Realiza UMA transformação geométrica (escala OU rotação) sobre uma imagem PNG,
conforme a especificação do enunciado::

    prog [-a angulo] [-e escala] [-d largura altura] [-m interpolacao]
         [-i entrada] [-o saida]

Exemplos:
    python3 -m src.trabalho_04.parte_01_transformacoes.cli \\
        -e 2.25 -m bilinear -i entrada.png -o saida.png

    python3 -m src.trabalho_04.parte_01_transformacoes.cli \\
        -a 30 -m bicubica -i entrada.png -o saida.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np

from src.trabalho_04.parte_01_transformacoes.geometria import (
    INTERPOLATION_METHODS,
    normalize_method,
    rotate_image,
    scale_image,
)


def _load_png(path: Path) -> np.ndarray:
    from PIL import Image

    with Image.open(path) as image:
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB" if image.mode != "L" else "L")
        return np.asarray(image)


def _save_png(array: np.ndarray, path: Path) -> None:
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array).save(path)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="prog",
        description=(
            "Aplica uma transformacao geometrica (escala ou rotacao) a uma "
            "imagem PNG usando interpolacao."
        ),
    )
    parser.add_argument(
        "-a",
        dest="angulo",
        type=float,
        default=None,
        help="angulo de rotacao em graus (sentido anti-horario).",
    )
    parser.add_argument(
        "-e",
        dest="escala",
        type=float,
        default=None,
        help="fator de escala (>0).",
    )
    parser.add_argument(
        "-d",
        dest="dimensao",
        type=int,
        nargs=2,
        metavar=("LARGURA", "ALTURA"),
        default=None,
        help="dimensao da imagem de saida em pixels.",
    )
    parser.add_argument(
        "-m",
        dest="metodo",
        type=str,
        default="bilinear",
        help=f"metodo de interpolacao ({', '.join(INTERPOLATION_METHODS)}).",
    )
    parser.add_argument(
        "-i",
        dest="entrada",
        type=str,
        required=True,
        help="imagem de entrada (PNG).",
    )
    parser.add_argument(
        "-o",
        dest="saida",
        type=str,
        required=True,
        help="imagem de saida (PNG).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if (args.angulo is None) == (args.escala is None):
        print(
            "[erro] Informe exatamente uma transformacao por execucao: "
            "rotacao (-a) OU escala (-e)."
        )
        return 1

    try:
        method = normalize_method(args.metodo)
    except ValueError as exc:
        print(f"[erro] {exc}")
        return 1

    entrada = Path(args.entrada)
    if not entrada.exists():
        print(f"[erro] Imagem de entrada nao encontrada: {entrada}")
        return 1

    image = _load_png(entrada)

    out_shape = None
    if args.dimensao is not None:
        largura, altura = args.dimensao
        out_shape = (altura, largura)

    if args.escala is not None:
        resultado = scale_image(
            image, args.escala, method, out_shape=out_shape
        )
        descricao = f"escala={args.escala}"
    else:
        resultado = rotate_image(
            image, args.angulo, method, out_shape=out_shape
        )
        descricao = f"rotacao={args.angulo} graus"

    saida = Path(args.saida)
    _save_png(resultado, saida)
    print(
        f"[ok] {descricao}, interpolacao={method}: "
        f"{entrada.name} ({image.shape}) -> {saida} ({resultado.shape})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
