"""
Trabalho 4 — Parte 1: Transformações Geométricas
=================================================
Implementação, a partir das formulações do enunciado, de transformações
geométricas de escala e rotação com valores contínuos (ponto flutuante),
usando mapeamento inverso (cada pixel da saída é amostrado a partir da
posição correspondente na entrada).

Quatro métodos de interpolação são implementados do zero (sem usar rotinas
prontas de reamostragem de bibliotecas como ``cv2.warpAffine`` ou
``scipy.ndimage``):

  * vizinho mais próximo   (eqs. 1-3)
  * bilinear               (eq. 4)
  * bicúbica (B-spline)    (eqs. 5-7)
  * polinômios de Lagrange (vizinhança 4x4)

As imagens são representadas como ``np.ndarray`` de shape ``(H, W)`` (tons de
cinza) ou ``(H, W, C)`` (colorida), em ``uint8``. A amostragem é totalmente
vetorizada em NumPy, mas a aritmética de cada interpolador segue exatamente as
fórmulas do enunciado.
"""

from __future__ import annotations

import numpy as np

# Aliases aceitos para cada método de interpolação.
INTERPOLATION_METHODS = ("vizinho", "bilinear", "bicubica", "lagrange")

_METHOD_ALIASES = {
    "vizinho": "vizinho",
    "vizinho_mais_proximo": "vizinho",
    "nearest": "vizinho",
    "nn": "vizinho",
    "bilinear": "bilinear",
    "bicubica": "bicubica",
    "bicubico": "bicubica",
    "bicubic": "bicubica",
    "lagrange": "lagrange",
}


def normalize_method(method: str) -> str:
    """Normaliza o nome do método de interpolação."""
    key = method.strip().lower()
    if key not in _METHOD_ALIASES:
        validos = ", ".join(sorted(set(_METHOD_ALIASES)))
        raise ValueError(
            f"Método de interpolação inválido: {method!r}. Use um de: {validos}."
        )
    return _METHOD_ALIASES[key]


# ---------------------------------------------------------------------------
# Amostragem por interpolação (mapeamento inverso)
# ---------------------------------------------------------------------------

def _broadcast_weight(weight: np.ndarray, sample: np.ndarray) -> np.ndarray:
    """Multiplica um peso ``(H, W)`` por amostras ``(H, W)`` ou ``(H, W, C)``."""
    if sample.ndim == 3:
        return weight[..., None] * sample
    return weight * sample


def _gather(image: np.ndarray, row: np.ndarray, col: np.ndarray) -> np.ndarray:
    """Lê ``image[row, col]`` com índices recortados às bordas (replicação)."""
    h, w = image.shape[:2]
    row = np.clip(row, 0, h - 1)
    col = np.clip(col, 0, w - 1)
    return image[row, col].astype(np.float64)


def _sample_vizinho(image, sx, sy):
    """Interpolação pelo vizinho mais próximo: f(x',y') = f(round(x), round(y))."""
    col = np.round(sx).astype(np.int64)
    row = np.round(sy).astype(np.int64)
    return _gather(image, row, col)


def _sample_bilinear(image, sx, sy):
    """Interpolação bilinear (eq. 4)."""
    x = np.floor(sx).astype(np.int64)
    y = np.floor(sy).astype(np.int64)
    dx = sx - x
    dy = sy - y

    f00 = _gather(image, y, x)
    f10 = _gather(image, y, x + 1)
    f01 = _gather(image, y + 1, x)
    f11 = _gather(image, y + 1, x + 1)

    out = (
        _broadcast_weight((1 - dx) * (1 - dy), f00)
        + _broadcast_weight(dx * (1 - dy), f10)
        + _broadcast_weight((1 - dx) * dy, f01)
        + _broadcast_weight(dx * dy, f11)
    )
    return out


def _P(t: np.ndarray) -> np.ndarray:
    """Parte positiva: P(t) = t se t > 0, senão 0 (eq. 7)."""
    return np.where(t > 0, t, 0.0)


def _R(s: np.ndarray) -> np.ndarray:
    """Núcleo B-spline cúbico (eq. 6)."""
    return (
        _P(s + 2) ** 3
        - 4 * _P(s + 1) ** 3
        + 6 * _P(s) ** 3
        - 4 * _P(s - 1) ** 3
    ) / 6.0


def _sample_bicubica(image, sx, sy):
    """Interpolação bicúbica por B-spline cúbica (eqs. 5-7), vizinhança 4x4."""
    x = np.floor(sx).astype(np.int64)
    y = np.floor(sy).astype(np.int64)
    dx = sx - x
    dy = sy - y

    acc = None
    for m in (-1, 0, 1, 2):
        rm = _R(m - dx)
        for n in (-1, 0, 1, 2):
            sample = _gather(image, y + n, x + m)
            weight = rm * _R(dy - n)
            term = _broadcast_weight(weight, sample)
            acc = term if acc is None else acc + term
    return acc


def _sample_lagrange(image, sx, sy):
    """Interpolação por polinômios de Lagrange, vizinhança 4x4."""
    x = np.floor(sx).astype(np.int64)
    y = np.floor(sy).astype(np.int64)
    dx = sx - x
    dy = sy - y

    # Coeficientes em x (compartilhados pelas quatro linhas L(n)).
    a1 = -dx * (dx - 1) * (dx - 2) / 6.0
    a2 = (dx + 1) * (dx - 1) * (dx - 2) / 2.0
    a3 = -dx * (dx + 1) * (dx - 2) / 2.0
    a4 = dx * (dx + 1) * (dx - 1) / 6.0

    def L(n: int) -> np.ndarray:
        row = y + (n - 2)  # n = 1..4  ->  linhas y-1, y, y+1, y+2
        fm1 = _gather(image, row, x - 1)
        f0 = _gather(image, row, x)
        fp1 = _gather(image, row, x + 1)
        fp2 = _gather(image, row, x + 2)
        return (
            _broadcast_weight(a1, fm1)
            + _broadcast_weight(a2, f0)
            + _broadcast_weight(a3, fp1)
            + _broadcast_weight(a4, fp2)
        )

    b1 = -dy * (dy - 1) * (dy - 2) / 6.0
    b2 = (dy + 1) * (dy - 1) * (dy - 2) / 2.0
    b3 = -dy * (dy + 1) * (dy - 2) / 2.0
    b4 = dy * (dy + 1) * (dy - 1) / 6.0

    return (
        _broadcast_weight(b1, L(1))
        + _broadcast_weight(b2, L(2))
        + _broadcast_weight(b3, L(3))
        + _broadcast_weight(b4, L(4))
    )


_SAMPLERS = {
    "vizinho": _sample_vizinho,
    "bilinear": _sample_bilinear,
    "bicubica": _sample_bicubica,
    "lagrange": _sample_lagrange,
}


def _resample(
    image: np.ndarray,
    sx: np.ndarray,
    sy: np.ndarray,
    method: str,
) -> np.ndarray:
    """Amostra ``image`` nas posições-fonte ``(sx, sy)`` da imagem de saída.

    Posições que caem fora do domínio da imagem de entrada recebem 0 (preto).
    """
    method = normalize_method(method)
    sampled = _SAMPLERS[method](image, sx, sy)

    h, w = image.shape[:2]
    inside = (sx >= 0) & (sx <= w - 1) & (sy >= 0) & (sy <= h - 1)
    if sampled.ndim == 3:
        inside = inside[..., None]
    sampled = np.where(inside, sampled, 0.0)

    return np.clip(np.rint(sampled), 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Transformações geométricas (mapeamento inverso)
# ---------------------------------------------------------------------------

def scale_image(
    image: np.ndarray,
    factor: float,
    method: str = "bilinear",
    out_shape: tuple[int, int] | None = None,
) -> np.ndarray:
    """Aplica um fator de escala contínuo à imagem.

    A posição de cada pixel de saída ``(x', y')`` é mapeada para a posição
    correspondente na entrada por ``(x'/s, y'/s)`` e amostrada com o método de
    interpolação escolhido.

    Args:
        image: array ``(H, W)`` ou ``(H, W, C)`` em uint8.
        factor: fator de escala (> 0). 2.0 amplia, 0.5 reduz.
        method: método de interpolação.
        out_shape: dimensão ``(altura, largura)`` da saída. Se ``None``, é
            ``round(H*factor) x round(W*factor)``.
    """
    if factor <= 0:
        raise ValueError(f"Fator de escala deve ser positivo: {factor}")

    h, w = image.shape[:2]
    if out_shape is None:
        out_h = max(1, int(round(h * factor)))
        out_w = max(1, int(round(w * factor)))
    else:
        out_h, out_w = out_shape

    yo, xo = np.indices((out_h, out_w), dtype=np.float64)
    sx = xo / factor
    sy = yo / factor
    return _resample(image, sx, sy, method)


def rotate_image(
    image: np.ndarray,
    angle_deg: float,
    method: str = "bilinear",
    out_shape: tuple[int, int] | None = None,
) -> np.ndarray:
    """Rotaciona a imagem por um ângulo contínuo, no sentido anti-horário.

    A rotação é feita em torno do centro da imagem por mapeamento inverso: para
    cada pixel da saída calcula-se a posição-fonte na entrada aplicando a
    rotação inversa.

    Convenção de coordenadas de imagem (x = coluna, y = linha para baixo): uma
    rotação anti-horária (como vista na tela) por ``theta`` corresponde, no
    mapeamento inverso, a::

        x_src = cos(theta)*(x' - cx) - sin(theta)*(y' - cy) + cx
        y_src = sin(theta)*(x' - cx) + cos(theta)*(y' - cy) + cy
    """
    h, w = image.shape[:2]
    if out_shape is None:
        out_h, out_w = h, w
    else:
        out_h, out_w = out_shape

    theta = np.deg2rad(angle_deg)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    cx_in = (w - 1) / 2.0
    cy_in = (h - 1) / 2.0
    cx_out = (out_w - 1) / 2.0
    cy_out = (out_h - 1) / 2.0

    yo, xo = np.indices((out_h, out_w), dtype=np.float64)
    xr = xo - cx_out
    yr = yo - cy_out
    sx = cos_t * xr - sin_t * yr + cx_in
    sy = sin_t * xr + cos_t * yr + cy_in
    return _resample(image, sx, sy, method)
