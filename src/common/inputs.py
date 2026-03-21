from __future__ import annotations

from pathlib import Path
from shutil import copy2
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

from src.common.paths import ROOT_DIR, input_dir_for


InputSpec = str | tuple[str, str]


def is_url(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")


def filename_from_source(source: str) -> str:
    if is_url(source):
        name = Path(urlparse(source).path).name
    else:
        name = Path(source).name

    if not name:
        raise ValueError(f"Nao foi possivel determinar o nome do arquivo para: {source}")
    return name


def normalize_input_spec(spec: InputSpec) -> tuple[str, str]:
    if isinstance(spec, tuple):
        source, filename = spec
        return source, filename
    return spec, filename_from_source(spec)


def download_file(url: str, destination: Path, overwrite: bool) -> Path:
    if destination.exists() and not overwrite:
        print(f"[skip] {destination} ja existe.")
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urlopen(url) as response:
            destination.write_bytes(response.read())
    except URLError as exc:
        raise RuntimeError(f"Falha ao baixar {url}: {exc.reason}") from exc

    print(f"[ok] {url} -> {destination}")
    return destination


def copy_file(source: str, destination: Path, overwrite: bool) -> Path:
    source_path = Path(source)
    if not source_path.is_absolute():
        source_path = ROOT_DIR / source_path

    if not source_path.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {source_path}")

    if destination.exists() and not overwrite:
        print(f"[skip] {destination} ja existe.")
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != destination.resolve():
        copy2(source_path, destination)

    print(f"[ok] {source_path} -> {destination}")
    return destination


def prepare_inputs(
    exercise: int | str,
    inputs: dict[str, InputSpec],
    overwrite: bool = False,
) -> dict[str, Path]:
    input_dir = input_dir_for(exercise)
    input_dir.mkdir(parents=True, exist_ok=True)

    prepared: dict[str, Path] = {}
    for name, spec in inputs.items():
        source, filename = normalize_input_spec(spec)
        destination = input_dir / filename

        if is_url(source):
            prepared[name] = download_file(source, destination, overwrite)
        else:
            prepared[name] = copy_file(source, destination, overwrite)

    return prepared
