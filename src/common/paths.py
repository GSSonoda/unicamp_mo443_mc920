from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
INPUTS_DIR = ROOT_DIR / "data" / "input"
RESULTS_DIR = ROOT_DIR / "results"
DOCS_DIR = ROOT_DIR / "docs"
REPORT_DIR = DOCS_DIR / "relatorio_01"
REPORT_FIGURES_DIR = REPORT_DIR / "figuras"
REPORT_02_DIR = DOCS_DIR / "relatorio_02"
REPORT_02_FIGURES_DIR = REPORT_02_DIR / "figuras"
BENCHMARKS_DIR = ROOT_DIR / "results" / "benchmarks"


def normalize_exercise(exercise: int | str) -> str:
    text = str(exercise)
    if text.isdigit():
        return f"exercicio_{int(text):02d}"
    if not text:
        raise ValueError(f"Nome de exercicio invalido: {exercise}")
    return text


def _method_section(name: str) -> str:
    """Returns 'secao_01' or 'secao_02' for a metodo_XX_* name."""
    num = int(name.split("_")[1])
    return "secao_01" if num <= 9 else "secao_02"


def input_dir_for(exercise: int | str) -> Path:
    name = normalize_exercise(exercise)
    if name.startswith("exercicio_"):
        return INPUTS_DIR / "trabalho_01" / name
    return INPUTS_DIR / "trabalho_02" / _method_section(name) / name


def results_dir_for(exercise: int | str) -> Path:
    name = normalize_exercise(exercise)
    if name.startswith("exercicio_"):
        return RESULTS_DIR / "trabalho_01" / name
    return RESULTS_DIR / "trabalho_02" / _method_section(name) / name


def benchmarks_dir_for(exercise: int | str) -> Path:
    name = normalize_exercise(exercise)
    if name.startswith("exercicio_"):
        return BENCHMARKS_DIR / "trabalho_01" / name
    return BENCHMARKS_DIR / "trabalho_02" / _method_section(name) / name


def report_figures_dir_for(exercise: int | str) -> Path:
    return REPORT_FIGURES_DIR / normalize_exercise(exercise)


def report_02_figures_dir_for(method: str) -> Path:
    return REPORT_02_FIGURES_DIR / _method_section(method) / method
