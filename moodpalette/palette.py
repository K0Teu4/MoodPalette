import colorsys


def clamp(x,a=0,b=1):

    return max(
        a,
        min(
            b,
            x
        )
    )


def hex_to_rgb(color):

    color=color.lstrip("#")

    return (

        int(color[0:2],16),
        int(color[2:4],16),
        int(color[4:6],16)

    )


def rgb_to_hex(r,g,b):

    return (

        f"#{r:02X}"
        f"{g:02X}"
        f"{b:02X}"

    )


def monochromatic(base):

    r,g,b=hex_to_rgb(base)

    h,l,s=colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255

    )

    result=[]

    for i in range(5):

        nl=clamp(

            l+(i-2)*0.12

        )

        nr,ng,nb=colorsys.hls_to_rgb(

            h,
            nl,
            s

        )

        result.append(

            rgb_to_hex(

                int(nr*255),
                int(ng*255),
                int(nb*255)

            )

        )

    return result


def complementary(base):

    r,g,b=hex_to_rgb(base)

    h,l,s=colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255

    )

    result=[]

    for i in range(5):

        nh=(

            h
            if i<3
            else (h+0.5)%1

        )

        nr,ng,nb=colorsys.hls_to_rgb(

            nh,
            l,
            s

        )

        result.append(

            rgb_to_hex(

                int(nr*255),
                int(ng*255),
                int(nb*255)

            )

        )

    return result


def triadic(base):

    r,g,b=hex_to_rgb(base)

    h,l,s=colorsys.rgb_to_hls(

        r/255,
        g/255,
        b/255

    )

    shifts=[

        0,
        0.33,
        0.66,
        0,
        0.33

    ]

    result=[]

    for shift in shifts:

        nr,ng,nb=colorsys.hls_to_rgb(

            (h+shift)%1,
            l,
            s

        )

        result.append(

            rgb_to_hex(

                int(nr*255),
                int(ng*255),
                int(nb*255)

            )

        )

    return result


def color_distance(c1,c2):

    r1,g1,b1=hex_to_rgb(c1)

    r2,g2,b2=hex_to_rgb(c2)

    return (

        ((r1-r2)**2)+
        ((g1-g2)**2)+
        ((b1-b2)**2)

    )**0.5


def optimize_palette(colors):

    result=[]

    threshold=35

    for color in colors:

        keep=True

        for existing in result:

            if (

                color_distance(
                    color,
                    existing
                )

                <threshold

            ):

                keep=False
                break

        if keep:

            result.append(
                color
            )

    while len(result)<5:

        result.append(

            result[-1]

        )

    return result[:5]