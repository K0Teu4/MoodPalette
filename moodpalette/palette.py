import colorsys


def hex_to_rgb(
    color: str
):

    color = color.lstrip(
        "#"
    )

    return (

        int(
            color[0:2],
            16
        ),

        int(
            color[2:4],
            16
        ),

        int(
            color[4:6],
            16
        )

    )


def rgb_to_hex(
    r,
    g,
    b
):

    return (
        f"#{r:02X}"
        f"{g:02X}"
        f"{b:02X}"
    )


def clamp(
    value
):

    return max(
        0,
        min(
            255,
            int(value)
        )
    )


def monochromatic(
    color
):

    r,g,b = hex_to_rgb(
        color
    )

    h,l,s = colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255

    )

    palette=[]

    values=[

        0.25,
        0.40,
        0.55,
        0.70,
        0.85

    ]

    for lightness in values:

        nr,ng,nb=colorsys.hls_to_rgb(

            h,
            lightness,
            s

        )

        palette.append(

            rgb_to_hex(

                clamp(
                    nr*255
                ),

                clamp(
                    ng*255
                ),

                clamp(
                    nb*255
                )

            )

        )

    return palette


def complementary(
    color
):

    r,g,b=hex_to_rgb(
        color
    )

    h,l,s=colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255
    )

    complement=(h+0.5)%1


    result=[]

    values=[

        h,
        h,
        complement,
        complement,
        h

    ]


    for hue in values:

        nr,ng,nb=colorsys.hls_to_rgb(

            hue,
            l,
            s
        )

        result.append(

            rgb_to_hex(

                clamp(
                    nr*255
                ),

                clamp(
                    ng*255
                ),

                clamp(
                    nb*255
                )

            )

        )

    return result


def triadic(
    color
):

    r,g,b=hex_to_rgb(
        color
    )

    h,l,s=colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255
    )

    hues=[

        h,

        (h+0.33)%1,

        (h+0.66)%1,

        h,

        (h+0.33)%1

    ]

    result=[]

    for hue in hues:

        nr,ng,nb=colorsys.hls_to_rgb(

            hue,
            l,
            s
        )

        result.append(

            rgb_to_hex(

                clamp(
                    nr*255
                ),

                clamp(
                    ng*255
                ),

                clamp(
                    nb*255
                )

            )

        )

    return result