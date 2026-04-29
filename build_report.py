from __future__ import annotations

import argparse

from src.common.report import build_report, sync_report_assets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera o PDF do relatorio."
    )
    parser.add_argument(
        "--sync-figures",
        action="store_true",
        help=(
            "Atualiza as figuras do relatorio a partir dos arquivos "
            "locais antes de compilar o PDF."
        ),
    )
    parser.add_argument(
        "--report",
        type=int,
        choices=[1, 2],
        default=1,
        metavar="{1,2}",
        help="Número do trabalho cujo relatório deve ser gerado (padrão: 1).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        print(f"[info] Gerando o PDF do relatorio {args.report}", flush=True)
        if args.sync_figures:
            sync_report_assets(args.report)
        build_report(args.report)
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
