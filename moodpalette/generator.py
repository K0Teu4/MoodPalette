import hashlib
import colorsys

from emotion import (
    tokenize,
    build_emotion_vector
)


def seed_from_text(text: str):
    return int(hashlib.md5(text.encode()).hexdigest(), 16)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def generate_palette(text: str, scheme: str, creativity: float):

    tokens = tokenize(text)
    emotion = build_emotion_vector(tokens)

    seed = seed_from_text(text)

    # -------------------------
    # BASE HSL FROM EMOTION
    # -------------------------

    base_h = (seed % 360) / 360.0

    base_s = 0.4 + emotion["saturation"] * 0.6
    base_l = 0.35 + emotion["warmth"] * 0.35 - emotion["darkness"] * 0.3

    base_s = clamp(base_s)
    base_l = clamp(base_l)

    palette = []

    # -------------------------
    # GENERATION CORE
    # -------------------------

    for i in range(5):

        t = i / 5.0

        h = (base_h + t * 0.22 + emotion["energy"] * 0.08) % 1.0

        s = base_s * (0.7 + t * 0.3)

        l = base_l + (t - 0.5) * 0.25

        l = clamp(l)

        r, g, b = colorsys.hls_to_rgb(h, l, s)

        palette.append(
            f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
        )

    # -------------------------
    # CREATIVITY LAYER
    # -------------------------

    if creativity > 0:

        noise = seed % 997

        step = max(1, int(10 - creativity * 8))

        for i in range(len(palette)):

            if (noise + i * 13) % step == 0:

                h = (base_h + 0.1 * i) % 1.0

                s = base_s * (0.5 + creativity)

                l = base_l + (creativity - 0.5) * 0.2

                r, g, b = colorsys.hls_to_rgb(h, clamp(l), clamp(s))

                palette[i] = f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"

    return [
        {
            "hex": c,
            "name": "generated"
        }
        for c in palette
    ]