from io import BytesIO

from PIL import Image
from PIL import ImageDraw


def create_palette_png(
    colors
):

    width=800
    height=200

    image=Image.new(
        "RGB",
        (
            width,
            height
        ),
        "white"
    )

    draw=ImageDraw.Draw(
        image
    )

    block_width=width//len(colors)


    for i,color in enumerate(colors):

        x1=i*block_width

        x2=(
            i+1
        )*block_width

        draw.rectangle(

            [
                x1,
                0,
                x2,
                150
            ],

            fill=color

        )

        draw.text(

            (
                x1+20,
                165
            ),

            color,

            fill="black"

        )


    buffer=BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    buffer.seek(
        0
    )

    return buffer