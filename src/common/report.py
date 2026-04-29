from __future__ import annotations

from pathlib import Path
from shutil import copy2
from subprocess import CalledProcessError, run

from src.common.paths import (
    REPORT_02_DIR,
    REPORT_DIR,
    report_02_figures_dir_for,
    report_figures_dir_for,
)


def copy_report_files_02(
    section: int | str,
    files: dict[str, Path],
) -> dict[str, Path]:
    target_dir = report_02_figures_dir_for(section)
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

    print(f"[info] Pasta das figuras do relatorio 2: {target_dir}")
    return copied


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


def _sync_report_assets_01() -> None:
    from src.trabalho_01.exercicio_01.main import (
        report_files as ex01_report_files,
    )
    from src.trabalho_01.exercicio_02.main import (
        report_files as ex02_report_files,
    )
    from src.trabalho_01.exercicio_03.main import (
        report_files as ex03_report_files,
    )
    from src.trabalho_01.exercicio_04.main import (
        report_files as ex04_report_files,
    )
    from src.trabalho_01.exercicio_05.main import (
        report_files as ex05_report_files,
    )
    from src.trabalho_01.exercicio_06.main import (
        report_files as ex06_report_files,
    )
    from src.trabalho_01.exercicio_07.main import (
        report_files as ex07_report_files,
    )
    from src.trabalho_01.exercicio_08.main import (
        report_files as ex08_report_files,
    )
    from src.trabalho_01.exercicio_09.main import (
        report_files as ex09_report_files,
    )
    from src.trabalho_01.exercicio_10.main import (
        report_files as ex10_report_files,
    )
    from src.trabalho_01.exercicio_11.main import (
        report_files as ex11_report_files,
    )
    from src.trabalho_01.exercicio_12.main import (
        report_files as ex12_report_files,
    )
    from src.trabalho_01.exercicio_13.main import (
        report_files as ex13_report_files,
    )

    print("[info] Atualizando figuras do relatorio 1", flush=True)
    copy_report_files("exercicio_01", ex01_report_files())
    copy_report_files("exercicio_02", ex02_report_files())
    copy_report_files("exercicio_03", ex03_report_files())
    copy_report_files("exercicio_04", ex04_report_files())
    copy_report_files("exercicio_05", ex05_report_files())
    copy_report_files("exercicio_06", ex06_report_files())
    copy_report_files("exercicio_07", ex07_report_files())
    copy_report_files("exercicio_08", ex08_report_files())
    copy_report_files("exercicio_09", ex09_report_files())
    copy_report_files("exercicio_10", ex10_report_files())
    copy_report_files("exercicio_11", ex11_report_files())
    copy_report_files("exercicio_12", ex12_report_files())
    copy_report_files("exercicio_13", ex13_report_files())

    print("[ok] Figuras do relatorio 1 atualizadas", flush=True)


def sync_report_assets_02() -> None:
    from src.trabalho_02.metodo_01_global.main import (
        report_files as m01_report_files,
    )
    from src.trabalho_02.metodo_02_otsu.main import (
        report_files as m02_report_files,
    )
    from src.trabalho_02.metodo_03_bernsen.main import (
        report_files as m03_report_files,
    )
    from src.trabalho_02.metodo_04_niblack.main import (
        report_files as m04_report_files,
    )
    from src.trabalho_02.metodo_05_sauvola.main import (
        report_files as m05_report_files,
    )
    from src.trabalho_02.metodo_06_phansalskar.main import (
        report_files as m06_report_files,
    )
    from src.trabalho_02.metodo_07_contraste.main import (
        report_files as m07_report_files,
    )
    from src.trabalho_02.metodo_08_media.main import (
        report_files as m08_report_files,
    )
    from src.trabalho_02.metodo_09_mediana.main import (
        report_files as m09_report_files,
    )
    from src.trabalho_02.metodo_10_pixels.main import (
        report_files as m10_report_files,
    )
    from src.trabalho_02.metodo_11_blocos.main import (
        report_files as m11_report_files,
    )
    from src.trabalho_02.metodo_12_histogramas.main import (
        report_files as m12_report_files,
    )

    print("[info] Atualizando figuras do relatorio 2", flush=True)
    copy_report_files_02("metodo_01_global", m01_report_files())
    copy_report_files_02("metodo_02_otsu", m02_report_files())
    copy_report_files_02("metodo_03_bernsen", m03_report_files())
    copy_report_files_02("metodo_04_niblack", m04_report_files())
    copy_report_files_02("metodo_05_sauvola", m05_report_files())
    copy_report_files_02("metodo_06_phansalskar", m06_report_files())
    copy_report_files_02("metodo_07_contraste", m07_report_files())
    copy_report_files_02("metodo_08_media", m08_report_files())
    copy_report_files_02("metodo_09_mediana", m09_report_files())
    copy_report_files_02("metodo_10_pixels", m10_report_files())
    copy_report_files_02("metodo_11_blocos", m11_report_files())
    copy_report_files_02("metodo_12_histogramas", m12_report_files())
    print("[ok] Figuras do relatorio 2 atualizadas", flush=True)


def sync_report_assets(report_num: int = 1) -> None:
    if report_num == 1:
        _sync_report_assets_01()
    elif report_num == 2:
        sync_report_assets_02()
    else:
        raise ValueError(f"Número de relatório inválido: {report_num}. Use 1 ou 2.")

def build_report(report_num: int = 1) -> Path:
    if report_num == 1:
        report_dir = REPORT_DIR
    elif report_num == 2:
        report_dir = REPORT_02_DIR
    else:
        raise ValueError(f"Número de relatório inválido: {report_num}. Use 1 ou 2.")

    tex_path = report_dir / "relatorio.tex"
    pdf_path = report_dir / "relatorio.pdf"

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
            cwd=report_dir,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("latexmk nao encontrado no sistema.") from exc
    except CalledProcessError as exc:
        raise RuntimeError("Falha ao gerar o PDF do relatorio.") from exc

    print(f"[ok] PDF gerado: {pdf_path}", flush=True)
    return pdf_path
