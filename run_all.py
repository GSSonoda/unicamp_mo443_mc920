from __future__ import annotations

import argparse

from src.trabalho_01.exercicio_01.main import run as run_exercicio_01
from src.trabalho_01.exercicio_02.main import run as run_exercicio_02
from src.trabalho_01.exercicio_03.main import run as run_exercicio_03
from src.trabalho_01.exercicio_04.main import run as run_exercicio_04
from src.trabalho_01.exercicio_05.main import run as run_exercicio_05
from src.trabalho_01.exercicio_06.main import run as run_exercicio_06
from src.trabalho_01.exercicio_07.main import run as run_exercicio_07
from src.trabalho_01.exercicio_08.main import run as run_exercicio_08
from src.trabalho_01.exercicio_09.main import run as run_exercicio_09
from src.trabalho_01.exercicio_10.main import run as run_exercicio_10
from src.trabalho_01.exercicio_11.main import run as run_exercicio_11
from src.trabalho_01.exercicio_12.main import run as run_exercicio_12
from src.trabalho_01.exercicio_13.main import run as run_exercicio_13
from src.trabalho_02.secao_01.metodo_01_global.main import run as run_metodo_01
from src.trabalho_02.secao_01.metodo_02_otsu.main import run as run_metodo_02
from src.trabalho_02.secao_01.metodo_03_bernsen.main import run as run_metodo_03
from src.trabalho_02.secao_01.metodo_04_niblack.main import run as run_metodo_04
from src.trabalho_02.secao_01.metodo_05_sauvola.main import run as run_metodo_05
from src.trabalho_02.secao_01.metodo_06_phansalskar.main import run as run_metodo_06
from src.trabalho_02.secao_01.metodo_07_contraste.main import run as run_metodo_07
from src.trabalho_02.secao_01.metodo_08_media.main import run as run_metodo_08
from src.trabalho_02.secao_01.metodo_09_mediana.main import run as run_metodo_09
from src.trabalho_02.secao_02.metodo_10_pixels.main import run as run_metodo_10
from src.trabalho_02.secao_02.metodo_11_blocos.main import run as run_metodo_11
from src.trabalho_02.secao_02.metodo_12_histogramas.main import run as run_metodo_12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa tudo que ja esta implementado no repositorio."
    )
    parser.add_argument(
        "--trabalho",
        type=int,
        choices=[1, 2],
        default=None,
        metavar="{1,2}",
        help="Limita a execucao a um trabalho especifico (padrao: ambos).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve arquivos ja gerados.",
    )
    return parser.parse_args()


def run_trabalho_01(overwrite: bool) -> None:
    print("[info] Executando trabalho 1", flush=True)
    run_exercicio_01(overwrite=overwrite)
    run_exercicio_02(overwrite=overwrite)
    run_exercicio_03(overwrite=overwrite)
    run_exercicio_04(overwrite=overwrite)
    run_exercicio_05(overwrite=overwrite)
    run_exercicio_06(overwrite=overwrite)
    run_exercicio_07(overwrite=overwrite)
    run_exercicio_08(overwrite=overwrite)
    run_exercicio_09(overwrite=overwrite)
    run_exercicio_10(overwrite=overwrite)
    run_exercicio_11(overwrite=overwrite)
    run_exercicio_12(overwrite=overwrite)
    run_exercicio_13(overwrite=overwrite)
    print("[ok] Trabalho 1 concluido", flush=True)


def run_trabalho_02(overwrite: bool) -> None:
    print("[info] Executando trabalho 2", flush=True)
    run_metodo_01(overwrite=overwrite)
    run_metodo_02(overwrite=overwrite)
    run_metodo_03(overwrite=overwrite)
    run_metodo_04(overwrite=overwrite)
    run_metodo_05(overwrite=overwrite)
    run_metodo_06(overwrite=overwrite)
    run_metodo_07(overwrite=overwrite)
    run_metodo_08(overwrite=overwrite)
    run_metodo_09(overwrite=overwrite)
    run_metodo_10(overwrite=overwrite)
    run_metodo_11(overwrite=overwrite)
    run_metodo_12(overwrite=overwrite)
    print("[ok] Trabalho 2 concluido", flush=True)


def main() -> int:
    args = parse_args()

    try:
        if args.trabalho in (None, 1):
            run_trabalho_01(overwrite=args.overwrite)
        if args.trabalho in (None, 2):
            run_trabalho_02(overwrite=args.overwrite)
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
