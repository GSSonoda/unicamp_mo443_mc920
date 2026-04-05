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

    missing_sources = [source for source in files.values() if not source.exists()]
    if missing_sources:
        missing = ", ".join(str(path) for path in missing_sources)
        raise FileNotFoundError(f"Arquivos necessarios para o relatorio nao encontrados: {missing}")

    copied: dict[str, Path] = {}
    for filename, source in files.items():
        destination = target_dir / filename
        copy2(source, destination)
        copied[filename] = destination

    print(f"[info] Pasta das figuras do relatorio: {target_dir}")
    return copied


def sync_report_assets() -> None:
    from src.exercicio_01.main import report_files as exercicio_01_report_files
    from src.exercicio_02.main import report_files as exercicio_02_report_files
    from src.exercicio_03.main import report_files as exercicio_03_report_files

    print("[info] Atualizando figuras do relatorio", flush=True)
    copy_report_files("exercicio_01", exercicio_01_report_files())
    copy_report_files("exercicio_02", exercicio_02_report_files())
    copy_report_files("exercicio_03", exercicio_03_report_files())

    print("[ok] Figuras do relatorio atualizadas", flush=True)

def build_report() -> Path:
    tex_path = REPORT_DIR / "relatorio.tex"
    pdf_path = REPORT_DIR / "relatorio.pdf"

    print(f"[info] Fonte do relatorio: {tex_path}", flush=True)
    print(f"[info] PDF do relatorio: {pdf_path}", flush=True)

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

    print(f"[ok] PDF gerado: {pdf_path}", flush=True)
    return pdf_path
