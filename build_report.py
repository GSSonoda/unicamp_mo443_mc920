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
        help="Atualiza as figuras do relatorio a partir dos arquivos locais antes de compilar o PDF.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        print("[info] Gerando o PDF do relatorio", flush=True)
        if args.sync_figures:
            sync_report_assets()
        build_report()
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
