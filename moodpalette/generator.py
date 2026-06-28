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


def shift_color(
    hex_color,
    shift
):

    hex_color = hex_color.lstrip("#")

    r = int(
        hex_color[0:2],
        16
    )

    g = int(
        hex_color[2:4],
        16
    )

    b = int(
        hex_color[4:6],
        16
    )

    h,l,s = colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255

    )

    h = (

        h +

        shift

    ) % 1

    r,g,b = colorsys.hls_to_rgb(

        h,
        l,
        s

    )

    return (

        f"#{int(r*255):02X}"
        f"{int(g*255):02X}"
        f"{int(b*255):02X}"

    )


def generate_palette(

    text,
    scheme,
    creativity

):

    tokens = tokenize(
        text
    )

    emotion = build_emotion_vector(
        tokens
    )


    seed = seed_from_text(
        text
    )


    # -----------------------------
    # Emotion → HSL
    # -----------------------------

    base_h = (

        seed % 360

    ) / 360


    base_s = (

        0.4 +

        emotion[
            "saturation"
        ] * 0.6

    )


    base_l = (

        0.35 +

        emotion[
            "warmth"
        ] * 0.3 -

        emotion[
            "darkness"
        ] * 0.25

    )


    base_s = clamp(
        base_s
    )

    base_l = clamp(
        base_l
    )


    palette = []


    # -----------------------------
    # Base generation
    # -----------------------------

    for i in range(5):

        t = i / 4


        h = (

            base_h +

            t * 0.20 +

            emotion[
                "energy"
            ] * 0.15

        ) % 1


        s = clamp(

            base_s *

            (

                0.7 +

                t * 0.3

            )

        )


        l = clamp(

            base_l +

            (

                t - 0.5

            ) * 0.25

        )


        r,g,b = colorsys.hls_to_rgb(

            h,
            l,
            s

        )


        color = (

            f"#{int(r*255):02X}"
            f"{int(g*255):02X}"
            f"{int(b*255):02X}"

        )


        palette.append(
            color
        )


    # -----------------------------
    # Creativity layer
    # -----------------------------

    if creativity > 0:

        shift = (

            creativity *

            0.12

        )

        palette = [

            shift_color(
                color,
                shift
            )

            for color

            in palette

        ]


    # -----------------------------
    # Palette optimization
    # -----------------------------

    palette = optimize_palette(
        palette
    )


    # -----------------------------
    # Harmony schemes
    # -----------------------------

    if scheme == "monochromatic":

        palette = monochromatic(

            palette[2]

        )


    elif scheme == "complementary":

        palette = complementary(

            palette[2]

        )


    elif scheme == "triadic":

        palette = triadic(

            palette[2]

        )


    # default ничего не делает


    return [

        {

            "hex": color,

            "name": "generated"

        }

        for color

        in palette

    ]