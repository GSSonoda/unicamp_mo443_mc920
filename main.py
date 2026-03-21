from __future__ import annotations

import argparse


IMPLEMENTADOS = {
    1: "Rotacao de Imagens em Multiplos de 90 Graus",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa um exercicio implementado do Trabalho 1."
    )
    parser.add_argument(
        "exercicio",
        type=int,
        help="Numero do exercicio. Atualmente, apenas o exercicio 1 esta implementado.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve arquivos de entrada e saida ja existentes.",
    )
    return parser.parse_args()


def run_exercicio(numero: int, overwrite: bool) -> int:
    if numero == 1:
        from src.exercicio_01.main import run

        run(overwrite=overwrite)
        return 0

    if 1 <= numero <= 13:
        print("[erro] Apenas o exercicio 1 esta implementado no momento.")
        return 1

    print("[erro] O trabalho possui exercicios de 1 a 13.")
    return 1


def main() -> int:
    args = parse_args()
    try:
        return run_exercicio(args.exercicio, args.overwrite)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
