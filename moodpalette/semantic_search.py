"""Semantic search and palette blending engine."""

import math
import colorsys
from typing import List, Dict, Any, Tuple

import numpy as np

from embedder import get_embedder


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two normalized vectors."""
    return float(np.dot(a, b))


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
    """Convert hex to HSL tuple."""
    r, g, b = hex_to_rgb(hex_color)
    return colorsys.rgb_to_hls(r/255, g/255, b/255)


def hsl_to_hex(h: float, l: float, s: float) -> str:
    """Convert HSL to hex."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex(int(r*255), int(g*255), int(b*255))


def sort_palette_by_lightness(colors: List[str]) -> List[str]:
    """Sort palette from dark to light."""
    def lightness(c):
        _, l, _ = hex_to_hsl(c)
        return l
    return sorted(colors, key=lightness)


def blend_colors_hsl(colors: List[str], weights: List[float]) -> str:
    """Blend multiple hex colors by weights in HSL space."""
    total_weight = sum(weights)
    if total_weight == 0:
        return colors[0] if colors else "#000000"

    weights = [w / total_weight for w in weights]
    hsl_colors = [hex_to_hsl(c) for c in colors]

    x_sum = 0.0
    y_sum = 0.0
    l_sum = 0.0
    s_sum = 0.0

    for (h, l, s), w in zip(hsl_colors, weights):
        x_sum += math.cos(h * 2 * math.pi) * w
        y_sum += math.sin(h * 2 * math.pi) * w
        l_sum += l * w
        s_sum += s * w

    avg_h = math.atan2(y_sum, x_sum) / (2 * math.pi)
    if avg_h < 0:
        avg_h += 1

    avg_l = max(0.0, min(1.0, l_sum))
    avg_s = max(0.0, min(1.0, s_sum))

    return hsl_to_hex(avg_h, avg_l, avg_s)


def interpolate_palettes(
    palettes: List[Dict[str, Any]],
    weights: List[float]
) -> List[str]:
    """Interpolate multiple palettes into one, color-by-color using HSL."""
    if not palettes:
        return ["#000000"] * 5

    total = sum(weights)
    weights = [w / total for w in weights]

    # Sort each palette by lightness so indices correspond (dark->light)
    sorted_palettes = [
        {**p, "colors": sort_palette_by_lightness(p["colors"])}
        for p in palettes
    ]

    num_colors = len(sorted_palettes[0]["colors"])
    result = []

    for i in range(num_colors):
        colors_at_idx = [p["colors"][i] for p in sorted_palettes]
        blended = blend_colors_hsl(colors_at_idx, weights)
        result.append(blended)

    return sort_palette_by_lightness(result)


def find_similar_palettes(
    query: str,
    top_k: int = 5
) -> Tuple[List[Dict[str, Any]], List[float]]:
    """Find top-K most semantically similar palettes to query text."""
    embedder = get_embedder()

    if len(embedder) == 0:
        return [], []

    query_vec = embedder.encode_query(query)
    query_lower = query.lower().strip()

    similarities = []
    for i in range(len(embedder)):
        palette = embedder.get_palette(i)
        sim = cosine_similarity(query_vec, embedder.get_embedding(i))

        # Exact / partial match bonuses
        name_lower = palette.get("name", "").lower()
        tags = [t.lower() for t in palette.get("tags", [])]

        if query_lower == name_lower:
            sim = min(1.0, sim + 0.5)
        elif query_lower in tags:
            sim = min(1.0, sim + 0.4)
        else:
            # Partial tag match
            for tag in tags:
                if len(tag) > 2 and (query_lower in tag or tag in query_lower):
                    sim = min(1.0, sim + 0.25)
                    break

        similarities.append((sim, i))

    similarities.sort(key=lambda x: x[0], reverse=True)

    top_palettes = []
    top_scores = []

    for sim, idx in similarities[:top_k]:
        top_palettes.append(embedder.get_palette(idx))
        top_scores.append(max(0.0, sim))

    return top_palettes, top_scores


def generate_semantic_palette(
    text: str,
    creativity: float = 0.3
) -> List[str]:
    """
    Generate palette from text using semantic search + CLIP fallback.
    """
    k = 3
    palettes, scores = find_similar_palettes(text, top_k=k)

    # Strong exact match -> return as-is (preserves author intent)
    if palettes and scores[0] > 0.70:
        return sort_palette_by_lightness(palettes[0]["colors"])

    if not palettes:
        # No palettes in DB — use CLIP directly
        from clip_embedder import get_clip_embedder
        return get_clip_embedder().get_colors_for_text(text, num_colors=5)

    if len(palettes) == 1:
        return sort_palette_by_lightness(palettes[0]["colors"])

    # Blend top palettes (sorted by lightness for index alignment)
    weights = [scores[0], scores[1] * 0.7, scores[2] * 0.4]
    blended = interpolate_palettes(palettes, weights)

    # If blend quality is low, mix with CLIP for semantic accuracy
    if scores[0] < 0.40:
        from clip_embedder import get_clip_embedder
        clip_colors = get_clip_embedder().get_colors_for_text(text, num_colors=5)
        # Merge: take darkest/lightest from CLIP, middle from blend
        blended[0] = clip_colors[0]
        blended[4] = clip_colors[4]
        blended[2] = clip_colors[2]

    return blended