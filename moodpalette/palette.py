import colorsys


def clamp(x, a=0, b=1):
    return max(a, min(b, x))


def hex_to_rgb(color):
    color = color.lstrip("#")
    return (
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:6], 16)
    )


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def monochromatic(base):
    r, g, b = hex_to_rgb(base)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

    result = []
    for i in range(5):
        nl = clamp(l + (i - 2) * 0.12)
        nr, ng, nb = colorsys.hls_to_rgb(h, nl, s)
        result.append(rgb_to_hex(int(nr*255), int(ng*255), int(nb*255)))

    return result


def complementary(base):
    r, g, b = hex_to_rgb(base)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

    result = []
    for i in range(5):
        nh = h if i < 3 else (h + 0.5) % 1
        nr, ng, nb = colorsys.hls_to_rgb(nh, l, s)
        result.append(rgb_to_hex(int(nr*255), int(ng*255), int(nb*255)))

    return result


def triadic(base):
    r, g, b = hex_to_rgb(base)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

    shifts = [0, 0.33, 0.66, 0, 0.33]

    result = []
    for shift in shifts:
        nr, ng, nb = colorsys.hls_to_rgb((h + shift) % 1, l, s)
        result.append(rgb_to_hex(int(nr*255), int(ng*255), int(nb*255)))

    return result


def color_distance(c1, c2):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return (((r1-r2)**2) + ((g1-g2)**2) + ((b1-b2)**2))**0.5


def optimize_palette(colors):
    """Remove duplicate colors and ensure exactly 5 unique colors."""
    result = []
    threshold = 35

    for color in colors:
        keep = True
        for existing in result:
            if color_distance(color, existing) < threshold:
                keep = False
                break
        if keep:
            result.append(color)

    # Generate new variations by varying lightness/saturation, alternating directions
    attempt = 0
    directions = [1, -1, 1, -1]  # alternate up/down to avoid clustering
    while len(result) < 5 and attempt < 30:
        base = result[-1] if result else "#808080"
        r, g, b = hex_to_rgb(base)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

        dir_sign = directions[attempt % len(directions)]
        variation = (attempt // 2 + 1) * 0.06

        new_l = clamp(l + dir_sign * variation)
        new_s = clamp(s + dir_sign * variation * 0.3)

        nr, ng, nb = colorsys.hls_to_rgb(h, new_l, new_s)
        new_color = rgb_to_hex(int(nr*255), int(ng*255), int(nb*255))

        # Check not too close to existing
        too_close = False
        for existing in result:
            if color_distance(new_color, existing) < threshold:
                too_close = True
                break

        if not too_close:
            result.append(new_color)
        else:
            # Try hue shift as last resort
            new_h = (h + 0.08 * (attempt + 1)) % 1
            nr, ng, nb = colorsys.hls_to_rgb(new_h, l, s)
            new_color = rgb_to_hex(int(nr*255), int(ng*255), int(nb*255))

            too_close = False
            for existing in result:
                if color_distance(new_color, existing) < threshold:
                    too_close = True
                    break

            if not too_close:
                result.append(new_color)

        attempt += 1

    return result[:5]