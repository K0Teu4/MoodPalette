from PIL import Image
from PIL import ImageDraw


def export_png(
    colors,
    path="palette.png"
):

    width = 800
    height = 200

    image = Image.new(
        "RGB",
        (width, height)
    )

    draw = ImageDraw.Draw(image)

    block_width = width // len(colors)

    for i, color in enumerate(colors):

        draw.rectangle(

            [
                i * block_width,
                0,
                (i + 1) * block_width,
                height
            ],

            fill=color
        )

    image.save(path)