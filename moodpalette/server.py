from pathlib import Path
import threading
import webbrowser

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from generator import generate_palette
from export import export_png


ROOT_DIR = Path(__file__).parent.parent
STATIC_DIR = ROOT_DIR / "static"


app = FastAPI()


class GenerateRequest(BaseModel):

    text: str
    scheme: str = "default"
    creativity: float = 0.5


@app.get("/")
def home():

    return FileResponse(
        STATIC_DIR / "index.html"
    )


@app.post("/api/generate")
def generate(req: GenerateRequest):

    palette = generate_palette(
        req.text,
        req.scheme,
        req.creativity
    )

    return {
        "palette": palette
    }


@app.get("/export")
def export(colors: str):

    color_list = colors.split(",")

    filepath = ROOT_DIR / "palette.png"

    export_png(
        color_list,
        filepath
    )

    return FileResponse(
        path=filepath,
        filename="palette.png",
        media_type="image/png"
    )


app.mount(
    "/static",
    StaticFiles(
        directory=STATIC_DIR
    ),
    name="static"
)


def open_browser():

    webbrowser.open(
        "http://localhost:8080"
    )


def run():

    threading.Timer(
        1,
        open_browser
    ).start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080
    )