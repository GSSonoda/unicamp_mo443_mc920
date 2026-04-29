from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
INPUTS_DIR = ROOT_DIR / "data" / "input"
RESULTS_DIR = ROOT_DIR / "results"
DOCS_DIR = ROOT_DIR / "docs"
REPORT_DIR = DOCS_DIR / "relatorio"
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


def input_dir_for(exercise: int | str) -> Path:
    return INPUTS_DIR / normalize_exercise(exercise)


def results_dir_for(exercise: int | str) -> Path:
    return RESULTS_DIR / normalize_exercise(exercise)


def benchmarks_dir_for(exercise: int | str) -> Path:
    return BENCHMARKS_DIR / normalize_exercise(exercise)


def report_figures_dir_for(exercise: int | str) -> Path:
    return REPORT_FIGURES_DIR / normalize_exercise(exercise)


def normalize_section(section: int | str) -> str:
    text = str(section)
    if text.isdigit():
        return f"secao_{int(text):02d}"
    if text.startswith("secao_"):
        return text
    raise ValueError(f"Nome de secao invalido: {section}")


def report_02_figures_dir_for(section: int | str) -> Path:
    return REPORT_02_FIGURES_DIR / normalize_section(section)
