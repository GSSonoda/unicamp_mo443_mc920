from __future__ import annotations

import argparse

from src.exercicio_01.main import run as run_exercicio_01


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Runs all implemented exercises."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing inputs and outputs when possible.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        print("[info] running implemented exercises")
        run_exercicio_01(overwrite=args.overwrite)

        for numero in range(2, 14):
            print(f"[skip] exercicio_{numero:02d} ainda nao foi implementado.")

        print("[info] exercise execution finished")
        print("[info] to build the PDF report, run: python3 build_report.py")
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
