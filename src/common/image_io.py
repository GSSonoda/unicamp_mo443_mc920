from __future__ import annotations

from pathlib import Path


def _require_pillow():
    try:
        from PIL import Image
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Pillow nao encontrado. Instale com: python3 -m pip install -r requirements.txt"
        ) from exc
    return Image


def load_grayscale_image(path: Path) -> list[list[int]]:
    Image = _require_pillow()

    with Image.open(path) as image:
        image = image.convert("L")
        width, height = image.size
        pixels = list(image.getdata())

    return [pixels[row * width : (row + 1) * width] for row in range(height)]


def save_grayscale_image(image_data: list[list[int]], path: Path) -> Path:
    Image = _require_pillow()

    height = len(image_data)
    width = len(image_data[0]) if height else 0
    pixels = [value for row in image_data for value in row]

    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("L", (width, height))
    image.putdata(pixels)
    image.save(path)
    return path


def load_rgb_image(path: Path) -> list[list[tuple[int, int, int]]]:
    Image = _require_pillow()

    with Image.open(path) as image:
        image = image.convert("RGB")
        width, height = image.size
        pixels = list(image.getdata())

    return [pixels[row * width : (row + 1) * width] for row in range(height)]


def save_rgb_image(
    image_data: list[list[tuple[int, int, int]]],
    path: Path,
) -> Path:
    Image = _require_pillow()

    height = len(image_data)
    width = len(image_data[0]) if height else 0
    pixels = [value for row in image_data for value in row]

    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (width, height))
    image.putdata(pixels)
    image.save(path)
    return path


def save_grayscale_outputs(
    output_dir: Path,
    outputs: dict[str, list[list[int]]],
) -> list[Path]:
    created: list[Path] = []
    for filename, image_data in outputs.items():
        created.append(save_grayscale_image(image_data, output_dir / filename))
    return created


def save_rgb_outputs(
    output_dir: Path,
    outputs: dict[str, list[list[tuple[int, int, int]]]],
) -> list[Path]:
    created: list[Path] = []
    for filename, image_data in outputs.items():
        created.append(save_rgb_image(image_data, output_dir / filename))
    return created
