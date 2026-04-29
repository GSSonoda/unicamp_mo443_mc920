from __future__ import annotations

import argparse
import importlib

_T1_EXERCISES = {
    1: "src.trabalho_01.exercicio_01.main",
    2: "src.trabalho_01.exercicio_02.main",
    3: "src.trabalho_01.exercicio_03.main",
    4: "src.trabalho_01.exercicio_04.main",
    5: "src.trabalho_01.exercicio_05.main",
    6: "src.trabalho_01.exercicio_06.main",
    7: "src.trabalho_01.exercicio_07.main",
    8: "src.trabalho_01.exercicio_08.main",
    9: "src.trabalho_01.exercicio_09.main",
    10: "src.trabalho_01.exercicio_10.main",
    11: "src.trabalho_01.exercicio_11.main",
    12: "src.trabalho_01.exercicio_12.main",
    13: "src.trabalho_01.exercicio_13.main",
}

_T2_METHODS = {
    1: "src.trabalho_02.secao_01.metodo_01_global.main",
    2: "src.trabalho_02.secao_01.metodo_02_otsu.main",
    3: "src.trabalho_02.secao_01.metodo_03_bernsen.main",
    4: "src.trabalho_02.secao_01.metodo_04_niblack.main",
    5: "src.trabalho_02.secao_01.metodo_05_sauvola.main",
    6: "src.trabalho_02.secao_01.metodo_06_phansalskar.main",
    7: "src.trabalho_02.secao_01.metodo_07_contraste.main",
    8: "src.trabalho_02.secao_01.metodo_08_media.main",
    9: "src.trabalho_02.secao_01.metodo_09_mediana.main",
    10: "src.trabalho_02.secao_02.metodo_10_pixels.main",
    11: "src.trabalho_02.secao_02.metodo_11_blocos.main",
    12: "src.trabalho_02.secao_02.metodo_12_histogramas.main",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa um exercicio/metodo implementado."
    )
    parser.add_argument(
        "numero",
        type=int,
        help=(
            "Numero do exercicio (trabalho 1: 1-13) "
            "ou do metodo (trabalho 2: 1-12)."
        ),
    )
    parser.add_argument(
        "--trabalho",
        type=int,
        choices=[1, 2],
        default=1,
        metavar="{1,2}",
        help="Numero do trabalho (padrao: 1).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve arquivos de entrada e saida ja existentes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = _T1_EXERCISES if args.trabalho == 1 else _T2_METHODS
    limit = max(registry)

    if args.numero not in registry:
        print(
            f"[erro] Trabalho {args.trabalho} possui itens de 1 a {limit}. "
            f"Recebido: {args.numero}."
        )
        return 1

    try:
        mod = importlib.import_module(registry[args.numero])
        mod.run(overwrite=args.overwrite)
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
