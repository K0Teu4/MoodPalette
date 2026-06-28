import hashlib
import colorsys

from emotion import (
    tokenize,
    build_emotion_vector
)

from palette import (
    optimize_palette,
    monochromatic,
    complementary,
    triadic
)

from semantic_search import (
    generate_semantic_palette,
    find_similar_palettes
)


def seed_from_text(text):
    return int(
        hashlib.md5(
            text.encode()
        ).hexdigest(),
        16
    )


def clamp(
    x,
    a=0.0,
    b=1.0
):
    return max(
        a,
        min(
            b,
            x
        )
    )


def apply_emotion_shift(
    palette,
    text,
    emotion
):
    """
    Apply VERY subtle emotion-based HSL shifts.
    Preserves the original semantic color meaning.
    """
    seed = seed_from_text(text)

    result = []

    for i, color in enumerate(palette):
        hex_color = color.lstrip("#")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

        # Very subtle shifts - max 3% to preserve semantic color
        shift_strength = 0.03

        # Warmth: tiny hue shift toward warm
        if emotion["warmth"] > 0.3:
            h = (h + 0.02 * emotion["warmth"] * shift_strength) % 1

        # Darkness: tiny lightness reduction
        if emotion["darkness"] > 0.3:
            l = max(0.05, l - 0.03 * emotion["darkness"] * shift_strength)

        # Energy: tiny saturation boost
        if emotion["energy"] > 0.3:
            s = min(1.0, s + 0.03 * emotion["energy"] * shift_strength)

        # Seed-based micro-variation for uniqueness (very small)
        micro = ((seed + i * 7) % 100 - 50) / 2000
        h = (h + micro) % 1

        l = clamp(l)
        s = clamp(s)

        nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
        result.append(
            f"#{int(nr*255):02X}{int(ng*255):02X}{int(nb*255):02X}"
        )

    return result


def generate_palette(
    text,
    scheme
):
    """
    Generate palette using semantic neural search.

    Pipeline:
    1. Semantic search: find closest palettes using sentence-transformers
    2. Apply subtle emotion-based color shifts
    3. Apply harmony scheme (mono/complementary/triadic)
    4. Optimize and return
    """

    # Step 1: Semantic palette generation (always use top 3 for richness)
    semantic_palette = generate_semantic_palette(text, creativity=0.3)

    # Step 2: Emotion analysis
    tokens = tokenize(text)
    emotion = build_emotion_vector(tokens)

    # Step 3: Apply emotion shifts (very subtle, preserves semantic meaning)
    palette = apply_emotion_shift(
        semantic_palette,
        text,
        emotion
    )

    # Step 4: Palette optimization
    palette = optimize_palette(palette)

    # Step 5: Harmony schemes
    if scheme == "monochromatic":
        palette = monochromatic(palette[2])

    elif scheme == "complementary":
        palette = complementary(palette[2])

    elif scheme == "triadic":
        palette = triadic(palette[2])

    # Build result with semantic info
    similar_palettes, scores = find_similar_palettes(text, top_k=1)
    base_name = similar_palettes[0]["name"] if similar_palettes else "custom"

    return [
        {
            "hex": color,
            "name": base_name if i == 2 else f"{base_name}-{i+1}"
        }
        for i, color in enumerate(palette)
    ]