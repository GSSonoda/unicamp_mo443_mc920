from __future__ import annotations

from src.common.report import build_report, sync_report_assets


def main() -> int:
    try:
        print("[info] Gerando o PDF do relatorio", flush=True)
        sync_report_assets()
        build_report()
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
