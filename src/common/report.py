from __future__ import annotations

from pathlib import Path
from shutil import copy2
from subprocess import CalledProcessError, run

from src.common.paths import REPORT_DIR, report_figures_dir_for


def copy_report_files(
    exercise: int | str,
    files: dict[str, Path],
) -> dict[str, Path]:
    target_dir = report_figures_dir_for(exercise)
    target_dir.mkdir(parents=True, exist_ok=True)

    copied: dict[str, Path] = {}
    for filename, source in files.items():
        destination = target_dir / filename
        copy2(source, destination)
        copied[filename] = destination

    print(f"[info] report figures directory: {target_dir}")
    return copied


def build_report() -> Path:
    tex_path = REPORT_DIR / "relatorio.tex"
    pdf_path = REPORT_DIR / "relatorio.pdf"

    print(f"[info] report source: {tex_path}", flush=True)
    print(f"[info] report output: {pdf_path}", flush=True)

    try:
        run(
            [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-file-line-error",
                tex_path.name,
            ],
            cwd=REPORT_DIR,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("latexmk nao encontrado no sistema.") from exc
    except CalledProcessError as exc:
        raise RuntimeError("Falha ao gerar o PDF do relatorio.") from exc

    print(f"[ok] report generated: {pdf_path}", flush=True)
    return pdf_path
