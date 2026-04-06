from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mede tempos de execucao de um exercicio e salva os resultados em JSON."
    )
    parser.add_argument(
        "exercicio",
        type=int,
        help="Numero do exercicio. Atualmente, apenas o exercicio 1 possui benchmark.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=20,
        help="Numero de repeticoes medidas para cada transformacao.",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=2,
        help="Numero de execucoes de aquecimento antes da medicao.",
    )
    parser.add_argument(
        "--overwrite-inputs",
        action="store_true",
        help="Sobrescreve arquivos de entrada locais, se necessario.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.exercicio == 1:
            from src.exercicio_01.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0
        
        if args.exercicio == 2:
            from src.exercicio_02.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 3:
            from src.exercicio_03.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 4:
            from src.exercicio_04.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 5:
            from src.exercicio_05.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 6:
            from src.exercicio_06.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 7:
            from src.exercicio_07.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 8:
            from src.exercicio_08.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 9:
            from src.exercicio_09.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 10:
            from src.exercicio_10.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 11:
            from src.exercicio_11.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 12:
            from src.exercicio_12.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        if args.exercicio == 13:
            from src.exercicio_13.main import run_benchmarks

            run_benchmarks(
                repeats=args.repeats,
                warmup=args.warmup,
                overwrite_inputs=args.overwrite_inputs,
            )
            return 0

        print("[erro] numero de exercicio invalido.")
        return 1
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[erro] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
