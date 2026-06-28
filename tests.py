"""All tests for MoodPalette. Run from project root: python tests.py"""

import sys
from pathlib import Path

# Auto-detect: if moodpalette/ subfolder exists, add it to path
# so we can write 'from semantic_search import ...' without 'moodpalette.' prefix
_PROJECT_ROOT = Path(__file__).parent.resolve()
_MOODPALETTE_DIR = _PROJECT_ROOT / "moodpalette"
if _MOODPALETTE_DIR.is_dir():
    sys.path.insert(0, str(_MOODPALETTE_DIR))
else:
    sys.path.insert(0, str(_PROJECT_ROOT))

from semantic_search import find_similar_palettes, generate_semantic_palette
from generator import generate_palette, apply_emotion_shift, clamp, seed_from_text
from palette import optimize_palette, monochromatic, complementary, triadic, color_distance
from clip_embedder import get_clip_embedder


def test_similar():
    print("=" * 60)
    print("TEST: Semantic Similarity Search")
    print("=" * 60)

    queries = [
        "night",
        "dark forest",
        "warm summer morning",
        "cyberpunk city neon",
        "melancholic rain",
        "ocean waves",
        "autumn leaves falling",
        "зелёный лес",
        "тёмный лес",
        "осенний лес",
        "ночь",
        "рассвет",
    ]

    for q in queries:
        print()
        print("Query: '%s'" % q)
        palettes, scores = find_similar_palettes(q, top_k=3)
        for p, s in zip(palettes, scores):
            print("   - %-20s | sim=%.3f | %s" % (p['name'], s, p['colors']))


def test_generation():
    print()
    print("=" * 60)
    print("TEST: Palette Generation (semantic_search)")
    print("=" * 60)

    queries = [
        "лес",
        "зелёный лес",
        "тёмный лес",
        "ночь",
        "рассвет",
        "cyberpunk",
    ]

    for q in queries:
        print()
        print("Query: '%s'" % q)
        palette = generate_semantic_palette(q)
        print("   -> %s" % palette)


def test_clip_colors():
    print()
    print("=" * 60)
    print("TEST: CLIP Color Embedder")
    print("=" * 60)

    queries = [
        "deep red",
        "ocean blue",
        "forest green",
        "зелёный лес",
        "тёмная ночь",
        "золотой закат",
    ]

    embedder = get_clip_embedder()
    for q in queries:
        colors = embedder.get_colors_for_text(q, num_colors=5)
        print("   %-20s -> %s" % (q, colors))


def test_harmony_schemes():
    print()
    print("=" * 60)
    print("TEST: Harmony Schemes")
    print("=" * 60)

    base = "#3A86FF"
    print("Base: %s" % base)
    print("   Monochromatic: %s" % monochromatic(base))
    print("   Complementary: %s" % complementary(base))
    print("   Triadic:       %s" % triadic(base))


def test_optimize_palette():
    print()
    print("=" * 60)
    print("TEST: Optimize Palette (deduplication)")
    print("=" * 60)

    # Almost identical colors
    dupes = ["#FF0000", "#FF0101", "#00FF00", "#00FF00", "#0000FF"]
    optimized = optimize_palette(dupes)
    print("Input:  %s" % dupes)
    print("Output: %s" % optimized)
    print("Count:  %d (expected 5)" % len(optimized))

    # Too few colors
    short = ["#FF0000", "#00FF00"]
    optimized2 = optimize_palette(short)
    print("\nInput:  %s" % short)
    print("Output: %s" % optimized2)
    print("Count:  %d (expected 5)" % len(optimized2))

    # All same
    same = ["#808080"] * 5
    optimized3 = optimize_palette(same)
    print("\nInput:  %s" % same)
    print("Output: %s" % optimized3)
    print("Count:  %d (expected 5)" % len(optimized3))

    # Verify distances
    for i in range(len(optimized3)):
        for j in range(i + 1, len(optimized3)):
            d = color_distance(optimized3[i], optimized3[j])
            assert d >= 35, "Colors too close: %s vs %s (dist=%.1f)" % (optimized3[i], optimized3[j], d)
    print("Distance check passed.")


def test_full_pipeline():
    print()
    print("=" * 60)
    print("TEST: Full Pipeline (generate_palette)")
    print("=" * 60)

    queries = [
        ("autumn forest", "default"),
        ("night", "monochromatic"),
        ("ocean", "complementary"),
        ("cyberpunk", "triadic"),
        ("зелёный лес", "default"),
        ("осенний лес", "default"),
    ]

    for q, scheme in queries:
        result = generate_palette(q, scheme)
        colors = [c["hex"] for c in result]
        name = result[2]["name"] if result else "none"
        print("   %-20s | %-15s | %-15s | %s" % (q, scheme, name, colors))


def test_russian_queries():
    print()
    print("=" * 60)
    print("TEST: Russian Queries (multilingual model)")
    print("=" * 60)

    pairs = [
        ("лес", "forest"),
        ("зелёный лес", "green forest"),
        ("ночь", "night"),
        ("осень", "autumn"),
        ("город", "city"),
        ("свобода", "freedom"),
    ]

    for ru, en in pairs:
        ru_pal = generate_semantic_palette(ru)
        en_pal = generate_semantic_palette(en)
        print("   %-15s -> %s" % (ru, ru_pal))
        print("   %-15s -> %s" % (en, en_pal))
        print()


def test_emotion_shift():
    print()
    print("=" * 60)
    print("TEST: Emotion Shift")
    print("=" * 60)

    base = ["#3A86FF", "#8338EC", "#FF006E", "#FB5607", "#FFBE0B"]

    from emotion import tokenize, build_emotion_vector

    for text in ["warm sunset", "dark night", "bright energy"]:
        tokens = tokenize(text)
        emotion = build_emotion_vector(tokens)
        shifted = apply_emotion_shift(base, text, emotion)
        print("   %-15s | emotion=%s | %s" % (text, emotion, shifted))


if __name__ == "__main__":
    test_similar()
    test_generation()
    test_clip_colors()
    test_harmony_schemes()
    test_optimize_palette()
    test_full_pipeline()
    test_russian_queries()
    test_emotion_shift()