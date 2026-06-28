from pathlib import Path
import threading
import webbrowser

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from generator import generate_palette
from export import export_png
from semantic_search import find_similar_palettes


ROOT_DIR = Path(__file__).parent.parent
STATIC_DIR = ROOT_DIR / "static"


app = FastAPI()


class GenerateRequest(BaseModel):
    text: str
    scheme: str = "default"


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/generate")
def generate(req: GenerateRequest):
    palette = generate_palette(req.text, req.scheme)
    return {"palette": palette}


@app.get("/api/similar")
def similar(text: str, limit: int = 3):
    """Get semantically similar palettes for a query (for debugging/UI)."""
    palettes, scores = find_similar_palettes(text, top_k=limit)

    return {
        "query": text,
        "results": [
            {
                "name": p["name"],
                "colors": p["colors"],
                "tags": p.get("tags", []),
                "similarity": round(score, 4)
            }
            for p, score in zip(palettes, scores)
        ]
    }


@app.get("/export")
def export(colors: str):
    color_list = colors.split(",")
    filepath = ROOT_DIR / "palette.png"
    export_png(color_list, filepath)

    return FileResponse(
        path=filepath,
        filename="palette.png",
        media_type="image/png"
    )


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def open_browser():
    webbrowser.open("http://localhost:8080")


def run():
    threading.Timer(1, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8080)