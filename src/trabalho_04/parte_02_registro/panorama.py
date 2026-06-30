"""
Trabalho 4 — Parte 2: Registro de Imagens e Geração de Panorama
================================================================
Pipeline de correspondência e costura de um par de imagens, seguindo os passos
do enunciado:

  (1) converter as imagens coloridas em níveis de cinza;
  (2) detectar pontos de interesse e descritores invariantes locais;
  (3) computar distâncias (similaridades) entre os descritores;
  (4) selecionar as melhores correspondências (teste de razão de Lowe);
  (5) estimar a homografia via RANSAC (cv2.findHomography);
  (6) aplicar a projeção de perspectiva (cv2.warpPerspective);
  (7) unir as imagens alinhadas formando o panorama;
  (8) desenhar as retas entre os pontos correspondentes.

Diferentes detectores/descritores são comparados: SIFT, SURF, BRIEF e ORB
(além de AKAZE como alternativa livre). A detecção/descrição e o casamento
são deixados a cargo do OpenCV — como autorizado pelo enunciado nesta parte.
"""

from __future__ import annotations

from time import perf_counter

import cv2
import numpy as np

# Detectores candidatos. SURF é nonfree e normalmente indisponível nos pacotes
# pip do OpenCV; AKAZE entra como alternativa livre de descritor robusto.
CANDIDATE_DETECTORS = ("sift", "surf", "brief", "orb", "akaze")

# Limite de área do canvas do panorama (evita estourar memória com homografias ruins).
_MAX_CANVAS_AREA = 60_000_000


class _BriefPipeline:
    """STAR (detector) + BRIEF (descritor), expostos como detectAndCompute."""

    def __init__(self) -> None:
        self._star = cv2.xfeatures2d.StarDetector_create()
        self._brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

    def detectAndCompute(self, image, mask):  # noqa: N802 (API do OpenCV)
        keypoints = self._star.detect(image, mask)
        keypoints, descriptors = self._brief.compute(image, keypoints)
        return keypoints, descriptors


def build_detector(name: str):
    """Constrói o detector/descritor e o tipo de norma usado no casamento."""
    key = name.lower()
    if key == "sift":
        return cv2.SIFT_create(), cv2.NORM_L2
    if key == "surf":
        return cv2.xfeatures2d.SURF_create(400), cv2.NORM_L2
    if key == "orb":
        return cv2.ORB_create(nfeatures=4000), cv2.NORM_HAMMING
    if key == "akaze":
        return cv2.AKAZE_create(), cv2.NORM_HAMMING
    if key == "brief":
        return _BriefPipeline(), cv2.NORM_HAMMING
    raise ValueError(f"Detector desconhecido: {name!r}")


def detector_available(name: str) -> bool:
    """Verifica se o detector pode ser instanciado e executado neste OpenCV."""
    try:
        detector, _ = build_detector(name)
    except (AttributeError, cv2.error, ValueError):
        return False

    # Imagem-sonda com textura suficiente para gerar pontos de interesse.
    yy, xx = np.indices((96, 96))
    probe = ((xx * 7 + yy * 13) % 256).astype(np.uint8)
    try:
        detector.detectAndCompute(probe, None)
    except cv2.error:
        return False
    return True


def available_detectors(candidates=CANDIDATE_DETECTORS) -> list[str]:
    return [name for name in candidates if detector_available(name)]


def _match_descriptors(desc_a, desc_b, norm, ratio: float):
    """Casamento por força bruta + teste de razão de Lowe (knn, k=2)."""
    if desc_a is None or desc_b is None or len(desc_a) < 2 or len(desc_b) < 2:
        return []

    matcher = cv2.BFMatcher(norm)
    knn = matcher.knnMatch(desc_a, desc_b, k=2)

    good = []
    for pair in knn:
        if len(pair) < 2:
            continue
        m, n = pair
        if m.distance < ratio * n.distance:
            good.append(m)
    return good


def _warp_pair(image_a: np.ndarray, image_b: np.ndarray, homography: np.ndarray):
    """Une A e B num único canvas: B é projetada para o referencial de A."""
    h_a, w_a = image_a.shape[:2]
    h_b, w_b = image_b.shape[:2]

    corners_b = np.float32(
        [[0, 0], [0, h_b], [w_b, h_b], [w_b, 0]]
    ).reshape(-1, 1, 2)
    corners_a = np.float32(
        [[0, 0], [0, h_a], [w_a, h_a], [w_a, 0]]
    ).reshape(-1, 1, 2)

    warped_corners_b = cv2.perspectiveTransform(corners_b, homography)
    all_corners = np.concatenate([warped_corners_b, corners_a], axis=0)

    x_min, y_min = np.int32(all_corners.min(axis=0).ravel() - 0.5)
    x_max, y_max = np.int32(all_corners.max(axis=0).ravel() + 0.5)

    width = x_max - x_min
    height = y_max - y_min
    if width <= 0 or height <= 0 or width * height > _MAX_CANVAS_AREA:
        return None

    translation = np.array(
        [[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]], dtype=np.float64
    )
    panorama = cv2.warpPerspective(image_b, translation @ homography, (width, height))
    panorama[-y_min:h_a - y_min, -x_min:w_a - x_min] = image_a
    return panorama


def build_panorama(
    image_a: np.ndarray,
    image_b: np.ndarray,
    detector_name: str,
    ratio: float = 0.75,
    reproj_thresh: float = 5.0,
    min_matches: int = 4,
) -> dict:
    """Executa o pipeline completo de registro para um par de imagens.

    Retorna um dicionário com status, métricas, a matriz de homografia e as
    imagens de correspondências e de panorama (ou ``None`` quando não foi
    possível registrar o par).
    """
    detector, norm = build_detector(detector_name)

    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    start = perf_counter()
    kp_a, desc_a = detector.detectAndCompute(gray_a, None)
    kp_b, desc_b = detector.detectAndCompute(gray_b, None)
    good = _match_descriptors(desc_a, desc_b, norm, ratio)
    elapsed = perf_counter() - start

    result: dict = {
        "detector": detector_name,
        "keypoints_a": 0 if kp_a is None else len(kp_a),
        "keypoints_b": 0 if kp_b is None else len(kp_b),
        "matches": len(good),
        "inliers": 0,
        "inlier_ratio": 0.0,
        "seconds": elapsed,
        "homography": None,
        "correspondencias": None,
        "panorama": None,
        "status": "ok",
    }

    if len(good) < min_matches:
        result["status"] = "matches_insuficientes"
        return result

    pts_a = np.float32([kp_a[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts_b = np.float32([kp_b[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(pts_b, pts_a, cv2.RANSAC, reproj_thresh)
    if homography is None:
        result["status"] = "homografia_falhou"
        return result

    inliers = int(mask.sum()) if mask is not None else 0
    result["homography"] = homography.tolist()
    result["inliers"] = inliers
    result["inlier_ratio"] = inliers / max(1, len(good))

    matches_mask = mask.ravel().tolist() if mask is not None else None
    result["correspondencias"] = cv2.drawMatches(
        image_a, kp_a, image_b, kp_b, good, None,
        matchColor=(0, 255, 0),
        singlePointColor=None,
        matchesMask=matches_mask,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    panorama = _warp_pair(image_a, image_b, homography)
    if panorama is None:
        result["status"] = "panorama_invalido"
    result["panorama"] = panorama

    return result
