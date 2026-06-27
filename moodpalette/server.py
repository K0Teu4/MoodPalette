import threading
import webbrowser
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    FileResponse,
    StreamingResponse
)

from pydantic import BaseModel

from generator import (
    generate_palette
)

from export import (
    create_palette_png
)


app = FastAPI()


class GenerateRequest(
    BaseModel
):

    text: str

    scheme: str = "default"

    creativity: float = 0.5


app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static"

)


@app.get("/")
async def index():

    return FileResponse(
        "static/index.html"
    )


@app.post(
    "/api/generate"
)
async def generate(
    request: GenerateRequest
):

    palette = generate_palette(

        text=request.text,

        scheme=request.scheme,

        creativity=request.creativity
    )

    return {

        "palette": palette

    }


@app.get(
    "/api/export"
)
async def export(
    colors: str
):

    parsed = colors.split(
        ","
    )

    image = create_palette_png(
        parsed
    )

    return StreamingResponse(

        image,

        media_type="image/png",

        headers={

            "Content-Disposition":
            "attachment; filename=palette.png"

        }

    )


def open_browser():

    webbrowser.open(
        "http://localhost:8080"
    )


def run():

    print(
        "MoodPalette running at http://localhost:8080"
    )

    threading.Timer(
        1,
        open_browser
    ).start()

    uvicorn.run(

        app,

        host="127.0.0.1",

        port=8080

    )