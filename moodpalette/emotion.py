def tokenize(text: str):
    return text.lower().split()


def build_emotion_vector(tokens):

    darkness = 0.0
    warmth = 0.0
    energy = 0.0
    saturation = 0.5

    NEGATIVE = {"dark", "night", "rain", "cold", "empty", "void", "black"}
    POSITIVE = {"light", "sun", "warm", "joy", "love", "happy"}
    ENERGY = {"fire", "storm", "electric", "cyber", "speed", "noise"}

    for t in tokens:

        if t in NEGATIVE:
            darkness += 0.4

        if t in POSITIVE:
            warmth += 0.4

        if t in ENERGY:
            energy += 0.5

        if "cold" in t:
            warmth -= 0.2
            darkness += 0.2

        if "bright" in t:
            saturation += 0.2

        if "soft" in t:
            saturation -= 0.2

    darkness = min(1.0, darkness)
    warmth = min(1.0, warmth)
    energy = min(1.0, energy)
    saturation = min(1.0, max(0.0, saturation))

    return {
        "darkness": darkness,
        "warmth": warmth,
        "energy": energy,
        "saturation": saturation
    }


def mix(a, b, t):
    return a + (b - a) * t