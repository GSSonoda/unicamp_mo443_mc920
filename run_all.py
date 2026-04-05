from __future__ import annotations

import argparse

from src.exercicio_01.main import run as run_exercicio_01
from src.exercicio_02.main import run as run_exercicio_02
from src.exercicio_03.main import run as run_exercicio_03


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa tudo que ja esta implementado no repositorio."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve arquivos ja gerados.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        print("[info] Executando o exercicio 1")
        run_exercicio_01(overwrite=args.overwrite)
        run_exercicio_02(overwrite=args.overwrite)
        run_exercicio_03(overwrite=args.overwrite)
        print("[ok] Execucao concluida")
        print("[info] Entrada: data/input/exercicio_01/baboon_monocromatica.png")
        print("[info] Resultados: results/exercicio_01/")
        print("[info] Figuras do relatorio: docs/relatorio/figuras/exercicio_01/")
        print("[info] Relatorio pronto: docs/relatorio/relatorio.pdf")
        print("[info] Para atualizar o PDF, execute opcionalmente: python3 build_report.py")
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
